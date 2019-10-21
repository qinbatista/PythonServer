'''
black_market.py
'''

from module import enums
from module import common
from module import weapon
import time
import random
from datetime import datetime, timedelta


async def transaction(uid, pid, **kwargs):
	# 0  : Purchase success
	# 94 : The server found an abnormal group id
	# 95 : You already have this skill
	# 96 : Insufficient currency
	# 97 : The item has been purchased
	# 98 : You have not yet done an automatic refresh
	# 99 : parameter error
	if pid < 0 or pid > 7:
		return common.mt(99, 'parameter error')

	data = await common.execute(f'SELECT gid, mid, qty, cid, amt From darkmarket WHERE uid = "{uid}" AND pid = "{pid}";', **kwargs)
	if data == ():
		return common.mt(98, 'You have not yet done an automatic refresh')

	gid, mid, qty, cid, amt = data[0]
	if amt < 0:
		return common.mt(97, 'The item has been purchased')

	transactions = {'pid': pid, 'gid': gid, 'mid': mid, 'qty': qty, 'cid': cid, 'amt': amt}
	amt = -amt
	can, currency = await common.try_item(uid, enums.Item(cid), amt, **kwargs)
	if not can:
		return common.mt(96, 'Insufficient currency')
	remaining = {'gid': gid, 'mid': mid, 'qty': qty, 'cid': cid, 'amt': currency}

	if gid == enums.Group.WEAPON.value:
		remaining['qty'] = await weapon._update_segment(uid, mid, qty, **kwargs)
	elif gid == enums.Group.SKILL.value:
		data = await common.execute(f'SELECT level FROM skill WHERE uid = "{uid}" AND sid = "{mid}";', **kwargs)
		if data == ():
			await common.execute_update(f'INSERT INTO skill (uid, sid, level) VALUES ("{uid}", {mid}, {qty});', **kwargs)
			remaining['qty'] = qty
		else:
			await common.try_item(uid, enums.Item(cid), abs(amt), **kwargs)
			return common.mt(95, 'You already have this skill')
	elif gid == enums.Group.ITEM.value:
		_, _qty = await common.try_item(uid, enums.Item(mid), qty, **kwargs)
		remaining['qty'] = _qty
	else:
		return common.mt(94, 'The server found an abnormal group id')
	await set_darkmarket(uid, pid, gid, mid, qty, cid, amt, **kwargs)
	return common.mt(0, 'Purchase success', {'transactions': transactions, 'remaining': remaining})


async def get_all_market(uid, **kwargs):
	"""
	# kwargs['dark_market']  self._player['dark_market']
	success -> 0 and 1
	# 0 - Dark market refreshed successfully
	# 1 - Get all black market information
	"""
	data = await common.execute(f'SELECT time FROM timer WHERE uid = "{uid}" AND tid = "{enums.Timer.DARK_MARKET_TIME.value}";', **kwargs)
	if data == ():
		await common.execute_update(f'INSERT INTO timer (uid, tid) VALUES ("{uid}", "{enums.Timer.DARK_MARKET_TIME.value}");', **kwargs)
		data = await common.execute(f'SELECT time FROM timer WHERE uid = "{uid}" AND tid = "{enums.Timer.DARK_MARKET_TIME.value}";', **kwargs)
	refresh_time = data[0][0]

	limit_data = await common.execute(f'SELECT value FROM limits WHERE uid = "{uid}" AND lid = "{enums.Limits.DARK_MARKET_LIMITS.value}";', **kwargs)
	if limit_data == ():
		await common.execute_update(f'INSERT INTO limits (uid, lid) VALUES ("{uid}", "{enums.Limits.DARK_MARKET_LIMITS.value}");', **kwargs)
		limit_data = await common.execute(f'SELECT value FROM limits WHERE uid = "{uid}" AND lid = "{enums.Limits.DARK_MARKET_LIMITS.value}";', **kwargs)
	refreshable = limit_data[0][0]

	current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
	dark_markets = []
	if refresh_time == '':
		refreshable = 3  # 免费刷新次数
		refresh_time = current_time
		dark_markets = await refresh_darkmarket(uid, **kwargs)
	else:
		delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(refresh_time, '%Y-%m-%d %H:%M:%S')
		if delta_time.total_seconds() // 3600 >= 3:  # 满足3个小时进行一次刷新
			frequency = delta_time.total_seconds() // 3600 // 3
			refreshable = 3 if refreshable + frequency >= 3 else int(refreshable + frequency)
			refresh_time = (datetime.strptime(refresh_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours = frequency*3)).strftime('%Y-%m-%d %H:%M:%S')
			dark_markets = await refresh_darkmarket(uid, **kwargs)
	if not dark_markets:
		data = await common.execute(f'SELECT pid, gid, mid, qty, cid, amt From darkmarket WHERE uid = "{uid}";', **kwargs)
		for d in data:
			dark_markets.append({'pid': d[0], 'gid': d[1], 'mid': d[2], 'qty': d[3], 'cid': d[4], 'amt': d[5]})
		return common.mt(1, 'Get all black market information', {'dark_markets': dark_markets, 'refresh_time': refresh_time, 'refreshable': refreshable})
	await common.execute_update(f'UPDATE timer SET time = "{refresh_time}" WHERE uid = "{uid}" AND tid = "{enums.Timer.DARK_MARKET_TIME.value}";', **kwargs)
	await common.execute_update(f'UPDATE limits SET value = {refreshable} WHERE uid = "{uid}" AND lid = "{enums.Limits.DARK_MARKET_LIMITS.value}";', **kwargs)
	return common.mt(0, 'Dark market refreshed successfully', {'dark_markets': dark_markets, 'refresh_time': refresh_time, 'refreshable': refreshable})


async def refresh_market(uid, **kwargs):
	"""
	# diamond_refresh
	0- Dark market refreshed successfully
	98 - Insufficient diamond
	99 - You have not yet done an automatic refresh
	# free_refresh
	0 - Dark market refreshed successfully
	98 - Insufficient free refresh
	99 - You have not yet done an automatic refresh

	refresh_market:
	0 - Dark market refreshed successfully
	97 - Insufficient free refresh
	98 - Insufficient diamond
	99 - You have not yet done an automatic refresh
	"""
	limit_data = await common.execute(f'SELECT value FROM limits WHERE uid = "{uid}" AND lid = "{enums.Limits.DARK_MARKET_LIMITS.value}";', **kwargs)
	if limit_data == ():
		await common.execute_update(f'INSERT INTO limits (uid, lid) VALUES ("{uid}", "{enums.Limits.DARK_MARKET_LIMITS.value}");', **kwargs)
		limit_data = await common.execute(f'SELECT value FROM limits WHERE uid = "{uid}" AND lid = "{enums.Limits.DARK_MARKET_LIMITS.value}";', **kwargs)
	refreshable = limit_data[0][0]
	if refreshable > 0:
		free_data = await free_refresh(uid, **kwargs)
		if free_data['status'] == 98: free_data['status'] = 97
		return free_data
	else:
		return await diamond_refresh(uid, **kwargs)


async def diamond_refresh(uid, **kwargs):
	"""
	0- Dark market refreshed successfully
	98 - Insufficient diamond
	99 - You have not yet done an automatic refresh
	"""
	data = await common.execute(f'SELECT time FROM timer WHERE uid = "{uid}" AND tid = "{enums.Timer.DARK_MARKET_TIME.value}";', **kwargs)
	if data == ():
		await common.execute_update(f'INSERT INTO timer (uid, tid) VALUES ("{uid}", "{enums.Timer.DARK_MARKET_TIME.value}");', **kwargs)
		data = await common.execute(f'SELECT time FROM timer WHERE uid = "{uid}" AND tid = "{enums.Timer.DARK_MARKET_TIME.value}";', **kwargs)
	refresh_time = data[0][0]
	if refresh_time == '':
		return common.mt(99, 'You have not yet done an automatic refresh')

	limit_data = await common.execute(f'SELECT value FROM limits WHERE uid = "{uid}" AND lid = "{enums.Limits.DARK_MARKET_LIMITS.value}";', **kwargs)
	if limit_data == ():
		await common.execute_update(f'INSERT INTO limits (uid, lid) VALUES ("{uid}", "{enums.Limits.DARK_MARKET_LIMITS.value}");', **kwargs)
		limit_data = await common.execute(f'SELECT value FROM limits WHERE uid = "{uid}" AND lid = "{enums.Limits.DARK_MARKET_LIMITS.value}";', **kwargs)
	refreshable = limit_data[0][0]

	need_diamond = -kwargs['dark_market']['diamond_refresh_store']['diamond']
	can, diamond = await common.try_item(uid, enums.Item.DIAMOND, need_diamond, **kwargs)
	current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
	if not can:
		return common.mt(98, 'Insufficient diamond')
	else:
		refresh_time = current_time
		dark_markets = await refresh_darkmarket(uid, **kwargs)
		await common.execute_update(f'UPDATE timer SET time = "{refresh_time}" WHERE uid = "{uid}" AND tid = "{enums.Timer.DARK_MARKET_TIME.value}";', **kwargs)
		return common.mt(0, 'Dark market refreshed successfully', {'dark_markets': dark_markets, 'refresh_time': refresh_time, 'refreshable': refreshable, 'diamond': diamond})


async def free_refresh(uid, **kwargs):
	"""
	0 - Dark market refreshed successfully
	98 - Insufficient free refresh
	99 - You have not yet done an automatic refresh
	"""
	data = await common.execute(f'SELECT time FROM timer WHERE uid = "{uid}" AND tid = "{enums.Timer.DARK_MARKET_TIME.value}";', **kwargs)
	if data == ():
		await common.execute_update(f'INSERT INTO timer (uid, tid) VALUES ("{uid}", "{enums.Timer.DARK_MARKET_TIME.value}");', **kwargs)
		data = await common.execute(f'SELECT time FROM timer WHERE uid = "{uid}" AND tid = "{enums.Timer.DARK_MARKET_TIME.value}";', **kwargs)
	refresh_time = data[0][0]

	limit_data = await common.execute(f'SELECT value FROM limits WHERE uid = "{uid}" AND lid = "{enums.Limits.DARK_MARKET_LIMITS.value}";', **kwargs)
	if limit_data == ():
		await common.execute_update(f'INSERT INTO limits (uid, lid) VALUES ("{uid}", "{enums.Limits.DARK_MARKET_LIMITS.value}");', **kwargs)
		limit_data = await common.execute(f'SELECT value FROM limits WHERE uid = "{uid}" AND lid = "{enums.Limits.DARK_MARKET_LIMITS.value}";', **kwargs)
	refreshable = limit_data[0][0]

	current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
	if refresh_time == '':
		return common.mt(99, 'You have not yet done an automatic refresh')
	elif refreshable <= 0:
		return common.mt(98, 'Insufficient free refresh')
	else:
		refreshable -= 1
		refresh_time = current_time
		dark_markets = await refresh_darkmarket(uid, **kwargs)
		await common.execute_update(f'UPDATE timer SET time = "{refresh_time}" WHERE uid = "{uid}" AND tid = "{enums.Timer.DARK_MARKET_TIME.value}";', **kwargs)
		await common.execute_update(f'UPDATE limits SET value = {refreshable} WHERE uid = "{uid}" AND lid = "{enums.Limits.DARK_MARKET_LIMITS.value}";', **kwargs)
		return common.mt(0, 'Dark market refreshed successfully', {'dark_markets': dark_markets, 'refresh_time': refresh_time, 'refreshable': refreshable})


########################################### 私有方法 private ###########################################


async def refresh_darkmarket(uid, **kwargs):
	dark_markets = []
	dark_market_data = kwargs['dark_market']  # self._player['dark_market']
	tier_choice = random.choices(dark_market_data['names'], dark_market_data['weights'], k=8)
	key_list = [(random.choices(dark_market_data[tier], k=1))[0] for tier in tier_choice]
	for pid, merchandise in enumerate(key_list):
		if merchandise in dark_market_data['weapon']:
			currency_type = (random.choices(list(dark_market_data['segment'].keys()), k=1))[0]
			merchandise_quantity = random.randint(int(dark_market_data['segment'][currency_type]['quantity_min']), int(dark_market_data['segment'][currency_type]['quantity_max']))
			currency_type_price = random.randint(int(dark_market_data['segment'][currency_type]['cost_range_min']), int(dark_market_data['segment'][currency_type]['cost_range_max']))
			gid = enums.Group.WEAPON.value
			mid = int(merchandise.replace('weapon', ''))
			qty = merchandise_quantity
			cid = dark_market_data['cid'][currency_type]
			amt = currency_type_price
			await set_darkmarket(uid, pid, gid, mid, qty, cid, amt, **kwargs)
			dark_markets.append({'pid': pid, 'gid': gid, 'mid': mid, 'qty': qty, 'cid': cid, 'amt': amt})
		elif merchandise in dark_market_data['skill']:  # 技能只加1级
			mid = 999999  # 设置mid的默认值
			for mpg, value in dark_market_data['skill_MPG'].items():
				if f'skill_{mpg}' in merchandise:
					mid = int(merchandise.replace(f'skill_{mpg}', '')) + value
					break
			if mid == 999999:
				print(f'WARNING 未知技能 -> {merchandise}')
			else:
				currency_type = (random.choices(list(dark_market_data['reward_skill'].keys()), k=1))[0]
				merchandise_quantity = 1
				currency_type_price = random.randint(int(dark_market_data['reward_skill'][currency_type]['cost_range_min']), int(dark_market_data['reward_skill'][currency_type]['cost_range_max']))
				gid = enums.Group.SKILL.value
				qty = merchandise_quantity
				cid = dark_market_data['cid'][currency_type]
				amt = currency_type_price
				await set_darkmarket(uid, pid, gid, mid, qty, cid, amt, **kwargs)
				dark_markets.append({'pid': pid, 'gid': gid, 'mid': mid, 'qty': qty, 'cid': cid, 'amt': amt})
		elif merchandise in dark_market_data['items'].keys():
			currency_type = (random.choices(list(dark_market_data['items'][merchandise].keys()), k=1))[0]
			merchandise_quantity = random.randint(int(dark_market_data['items'][merchandise][currency_type]['quantity_min']), int(dark_market_data['items'][merchandise][currency_type]['quantity_max']))
			currency_type_price = random.randint(int(dark_market_data['items'][merchandise][currency_type]['cost_range_min']), int(dark_market_data['items'][merchandise][currency_type]['cost_range_max']))
			gid = enums.Group.ITEM.value
			mid = int(merchandise)
			qty = merchandise_quantity
			cid = dark_market_data['cid'][currency_type]
			amt = currency_type_price
			await set_darkmarket(uid, pid, gid, mid, qty, cid, amt, **kwargs)
			dark_markets.append({'pid': pid, 'gid': gid, 'mid': mid, 'qty': qty, 'cid': cid, 'amt': amt})
		else:
			print(f'WARNING 未知商品 -> {merchandise}')
	return dark_markets


async def set_darkmarket(uid, pid, gid, mid, qty, cid, amt, **kwargs):
	await common.execute_update(f'INSERT INTO darkmarket (uid, pid, gid, mid, qty, cid, amt) VALUES ("{uid}", {pid}, {gid}, {mid}, {qty}, {cid}, {amt}) ON DUPLICATE KEY UPDATE `gid`= values(`gid`), `mid`= values(`mid`), `qty`= values(`qty`), `cid`= values(`cid`), `amt`= values(`amt`);', **kwargs)


