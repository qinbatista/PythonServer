'''
black_market.py
'''

from module import enums
from module import common
import time
import random
from datetime import datetime, timedelta

#


async def automatically_refresh(uid, **kwargs) -> dict:
	"""
	# kwargs['dark_market']  self._player['dark_market']
	success -> 0 and 1
	# 0 - Dark market refreshed successfully
	"""
	data = await common.execute(f'SELECT time FROM timer WHERE uid = "{uid}" AND tid = "{enums.Timer.DARK_MARKET_TIME.value}"', **kwargs)
	if data == ():
		await common.execute_update(f'INSERT INTO timer (uid, tid) VALUES ("{uid}", "{enums.Timer.DARK_MARKET_TIME.value}")', **kwargs)
		data = await common.execute(f'SELECT time FROM timer WHERE uid = "{uid}" AND tid = "{enums.Timer.DARK_MARKET_TIME.value}"', **kwargs)
	refresh_time = data[0][0]

	limit_data = await common.execute(f'SELECT time FROM limits WHERE uid = "{uid}" AND lid = "{enums.Limits.DARK_MARKET_LIMITS.value}"', **kwargs)
	if limit_data == ():
		await common.execute_update(f'INSERT INTO limits (uid, lid) VALUES ("{uid}", "{enums.Limits.DARK_MARKET_LIMITS.value}")', **kwargs)
		limit_data = await common.execute(f'SELECT time FROM limits WHERE uid = "{uid}" AND lid = "{enums.Limits.DARK_MARKET_LIMITS.value}"', **kwargs)
	refreshable = limit_data[0][0]

	current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
	if refresh_time == '':
		refreshable = 3  # 免费刷新次数
		refresh_time = current_time
	else:
		delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(refresh_time, '%Y-%m-%d %H:%M:%S')
		if delta_time.total_seconds() // 3600 >= 3:  # 满足3个小时进行一次刷新
			frequency = delta_time.total_seconds() // 3600 // 3
			refreshable = 3 if refreshable + frequency >= 3 else refreshable + frequency
			refresh_time = (datetime.strptime(refresh_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours = frequency*3)).strftime('%Y-%m-%d %H:%M:%S')
	dark_markets = await refresh_darkmarket(uid, **kwargs)
	await common.execute_update(f'UPDATE timer SET time = {refresh_time} WHERE uid = "{uid}" AND tid = "{enums.Timer.DARK_MARKET_TIME.value}"', **kwargs)
	await common.execute_update(f'UPDATE limits SET value = {refreshable} WHERE uid = "{uid}" AND lid = "{enums.Limits.DARK_MARKET_LIMITS.value}"', **kwargs)
	return common.mt(0, 'Dark market refreshed successfully', {'dark_markets': dark_markets, 'refresh_time': refresh_time, 'refreshable': refreshable})


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
				continue
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


async def get_darkmarket(uid, pid, gid, mid, qty, cid, amt, **kwargs):
	select = f'SELECT gid, mid, qty, cid, amt From darkmarket WHERE uid = "{uid}" AND pid = "{pid}";'
	insert = f'INSERT INTO darkmarket (uid, pid, gid, mid, qty, cid, amt) VALUES darkmarket ("{uid}", {pid}, {gid}, {mid}, {qty}, {cid}, {amt});'
	data = await common.execute(select, **kwargs)
	if data == ():
		await common.execute_update(insert, **kwargs)
		data = await common.execute(select, **kwargs)
	return data[0]

async def set_darkmarket(uid, pid, gid, mid, qty, cid, amt, **kwargs):
	select = f'SELECT gid, mid, qty, cid, amt From darkmarket WHERE uid = "{uid}" AND pid = "{pid}";'
	update = f'UPDATE darkmarket SET gid={gid}, mid={mid}, qty={qty}, cid={cid}, amt={amt} WHERE uid = "{uid}" AND pid = "{pid}";'
	insert = f'INSERT INTO darkmarket (uid, pid, gid, mid, qty, cid, amt) VALUES darkmarket ("{uid}", {pid}, {gid}, {mid}, {qty}, {cid}, {amt});'
	data = await common.execute(select, **kwargs)
	if data == ():
		await common.execute_update(insert, **kwargs)
	else:
		await common.execute_update(update, **kwargs)


