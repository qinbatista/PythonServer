'''
black_market.py
'''

import asyncio
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
	if pid < 0 or pid > kwargs['config']['player']['dark_market']['constraint']['grid'] - 1: return common.mt(99, 'parameter error')

	data = await common.execute(f'SELECT gid, mid, qty, cid, amt From darkmarket WHERE uid = "{uid}" AND pid = "{pid}";', **kwargs)
	if data == (): return common.mt(98, 'You have not yet done an automatic refresh')

	gid, mid, qty, cid, amt = data[0]
	if amt < 0: return common.mt(97, 'The item has been purchased')

	transactions = {'pid': pid, 'gid': gid, 'mid': mid, 'qty': qty, 'cid': cid, 'amt': -amt}
	can, currency = await common.try_item(uid, enums.Item(cid), -amt, **kwargs)
	if not can:
		return common.mt(96, 'Insufficient currency')
	remaining = {'gid': gid, 'mid': mid, 'qty': qty, 'cid': cid, 'amt': currency}

	if gid == enums.Group.WEAPON.value:
		remaining['qty'] = await common.try_weapon(uid, mid, qty, **kwargs)
	elif gid == enums.Group.ROLE.value:
		remaining['qty'] = await common.try_role(uid, mid, qty, **kwargs)
	elif gid == enums.Group.SKILL.value:
		if await common.try_skill(uid, mid, **kwargs):
			remaining['qty'] = qty
		else:
			await common.try_item(uid, enums.Item(cid), amt, **kwargs)
			return common.mt(95, 'You already have this skill')
	elif gid == enums.Group.ITEM.value:
		_, _qty = await common.try_item(uid, enums.Item(mid), qty, **kwargs)
		remaining['qty'] = _qty
	else:
		return common.mt(94, 'The server found an abnormal group id')
	await set_darkmarket(uid, pid, gid, mid, qty, cid, -amt, **kwargs)
	return common.mt(0, 'Purchase success', {'reward': transactions, 'remaining': remaining})


async def get_all_market(uid, **kwargs):
	"""
	# kwargs['dark_market']  self._player['dark_market']
	success -> 0 and 1
	# 0 - Dark market refreshed successfully
	# 1 - Get all black market information
	"""
	current_time = datetime.now(tz=common.TZ_SH)
	config = kwargs['config']['player']['dark_market']
	lim = config['constraint']['refreshable']
	refresh_hours = config['constraint']['refresh_hours']
	timer, limit = await asyncio.gather(
		common.get_timer(uid, enums.Timer.DARK_MARKET, **kwargs),
		common.get_limit(uid, enums.Limits.DARK_MARKET, **kwargs)
	)
	refresh_time = current_time if timer is None else timer
	refreshable = lim if limit is None else limit
	dark_markets = []
	if refresh_time == current_time:
		dark_markets = await refresh_darkmarket(uid, **kwargs)
	else:
		delta_time = current_time - refresh_time
		frequency = int(delta_time.total_seconds() // 3600 // refresh_hours)
		if frequency > 0:  # ??????refresh_hours???????????????????????????
			refreshable, refresh_time = (lim, current_time) if refreshable + frequency >= lim \
				else (int(refreshable + frequency), refresh_time + timedelta(hours=frequency*refresh_hours))
			dark_markets = await refresh_darkmarket(uid, **kwargs)
	if refreshable == lim:
		refresh_time = current_time
	await asyncio.gather(
		common.set_timer(uid, enums.Timer.DARK_MARKET, refresh_time, **kwargs),
		common.set_limit(uid, enums.Limits.DARK_MARKET, refreshable, **kwargs)
	)
	refresh_time_s = max(3600 * refresh_hours - int((current_time - refresh_time).total_seconds()), 0)
	if not dark_markets:
		data = await common.execute(f'SELECT pid, gid, mid, qty, cid, amt From darkmarket WHERE uid = "{uid}";', **kwargs)
		dark_markets = [{'pid': d[0], 'gid': d[1], 'mid': d[2], 'qty': d[3], 'cid': d[4], 'amt': d[5]} for d in data]
		return common.mt(1, 'Get all black market information', {'dark_markets': dark_markets, 'refresh_time': refresh_time_s, 'refreshable': refreshable, 'config': {'refresh_diamond': config['refresh_store']['diamond']}})
	return common.mt(0, 'Dark market refreshed successfully', {'dark_markets': dark_markets, 'refresh_time': refresh_time_s, 'refreshable': refreshable, 'config': {'refresh_diamond': config['refresh_store']['diamond']}})


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
	refreshable = await common.get_limit(uid, enums.Limits.DARK_MARKET, **kwargs)
	if refreshable is None:
		return await refresh_darkmarket(uid, **kwargs)
	elif refreshable > 0:
		return await free_refresh(uid, **kwargs)
	else:
		return await diamond_refresh(uid, **kwargs)


async def diamond_refresh(uid, **kwargs):
	"""
	0- Dark market refreshed successfully
	98 - Insufficient diamond
	99 - You have not yet done an automatic refresh
	"""
	refresh_time = await common.get_timer(uid, enums.Timer.DARK_MARKET, **kwargs)
	refreshable = await common.get_limit(uid, enums.Limits.DARK_MARKET, **kwargs)
	refresh_hours = kwargs['config']['player']['dark_market']['constraint']['refresh_hours']
	if refresh_time is None or refreshable is None: return common.mt(99, 'You have not yet done an automatic refresh')

	need_diamond = -kwargs['config']['player']['dark_market']['refresh_store']['diamond']
	can, diamond = await common.try_item(uid, enums.Item.DIAMOND, need_diamond, **kwargs)
	if not can:
		return common.mt(98, 'Insufficient diamond')
	else:
		cooling = 3600 * refresh_hours - int((datetime.now(tz=common.TZ_SH) - refresh_time).total_seconds())
		dark_markets = await refresh_darkmarket(uid, **kwargs)
		return common.mt(0, 'Dark market refreshed successfully', {'dark_markets': dark_markets, \
				'diamond' : {'remaining' : diamond, 'reward' : need_diamond}, \
				'refresh_time': cooling, 'refreshable': refreshable, 'refresh_diamond': need_diamond})


async def free_refresh(uid, **kwargs):
	"""
	0 - Dark market refreshed successfully
	98 - Insufficient free refresh
	99 - You have not yet done an automatic refresh
	"""
	current_time = datetime.now(tz=common.TZ_SH)
	refresh_time = await common.get_timer(uid, enums.Timer.DARK_MARKET, **kwargs)
	refreshable = await common.get_limit(uid, enums.Limits.DARK_MARKET, **kwargs)
	config = kwargs['config']['player']['dark_market']
	lim = config['constraint']['refreshable']
	refresh_hours = config['constraint']['refresh_hours']
	if refresh_time is None or refreshable is None:
		return common.mt(99, 'You have not yet done an automatic refresh')
	elif refreshable <= 0:
		return common.mt(97, 'Insufficient free refresh')
	else:
		if refreshable == lim:
			refresh_time = current_time
		cooling = 3600 * refresh_hours - int((current_time - refresh_time).total_seconds())
		refreshable -= 1
		dark_markets = await refresh_darkmarket(uid, **kwargs)
		await common.set_timer(uid, enums.Timer.DARK_MARKET, refresh_time, **kwargs)
		await common.set_limit(uid, enums.Limits.DARK_MARKET, refreshable, **kwargs)
		_, current_diamond = await common.try_item(uid, enums.Item.DIAMOND, 0, **kwargs)
		return common.mt(0, 'Dark market refreshed successfully', {'dark_markets': dark_markets, \
				'diamond' : {'remaining' : current_diamond, 'reward' : 0}, \
				'refresh_time': cooling, 'refreshable': refreshable, \
				'refresh_diamond' : kwargs['config']['player']['dark_market']['refresh_store']['diamond']})


########################################### ???????????? private ###########################################


async def refresh_darkmarket(uid, **kwargs):
	dark_markets = []
	config = kwargs['config']['player']['dark_market']
	tier_choice = random.choices(config['names'], config['weights'], k=kwargs['config']['player']['dark_market']['constraint']['grid'])
	key_list = [(random.choices(config[tier], k=1))[0] for tier in tier_choice]
	for pid, merchandise in enumerate(key_list):
		if merchandise in enums.Weapon.__members__ or merchandise in enums.Role.__members__:
			pre = merchandise[:2]
			cty = random.choice(list(config['segment'][pre]))
			cfg = config['segment'][pre][cty]
			mul = random.randint(cfg['multiple_min'], cfg['multiple_max'])
			mnq, mxq = cfg['quantity_min'] * mul, cfg['quantity_max'] * mul
			mnc, mxc = cfg['cost_range_min'] * mul, cfg['cost_range_max'] * mul
			gid = enums.Group['WEAPON' if 'W' in pre else 'ROLE']
			mid = merchandise[1:]
			qty = random.randint(mnq, mxq)
			cid = config['cid'][cty]
			amt = random.randint(mnc, mxc)
			await set_darkmarket(uid, pid, gid, mid, qty, cid, amt, **kwargs)
			dark_markets.append({'pid': pid, 'gid': gid, 'mid': mid, 'qty': qty, 'cid': cid, 'amt': amt})
		elif merchandise in enums.Skill.__members__:  # ????????????1???
			cty = random.choice(list(config['skill']))
			ctp = random.randint(int(config['skill'][cty]['cost_range_min']), int(config['skill'][cty]['cost_range_max']))
			gid = enums.Group.SKILL
			mid = enums.Skill[merchandise]
			qty = 1
			cid = config['cid'][cty]
			amt = ctp
			await set_darkmarket(uid, pid, gid, mid, qty, cid, amt, **kwargs)
			dark_markets.append({'pid': pid, 'gid': gid, 'mid': mid, 'qty': qty, 'cid': cid, 'amt': amt})
		elif merchandise in config['items']:
			cty = random.choice(list(config['items'][merchandise]))
			cfg = config['items'][merchandise][cty]
			mul = random.randint(cfg['multiple_min'], cfg['multiple_max'])
			mnq, mxq = cfg['quantity_min'] * mul, cfg['quantity_max'] * mul
			mnc, mxc = cfg['cost_range_min'] * mul, cfg['cost_range_max'] * mul
			gid = enums.Group.ITEM
			mid = int(merchandise)
			qty = random.randint(mnq, mxq)
			cid = config['cid'][cty]
			amt = random.randint(mnc, mxc)
			await set_darkmarket(uid, pid, gid, mid, qty, cid, amt, **kwargs)
			dark_markets.append({'pid': pid, 'gid': gid, 'mid': mid, 'qty': qty, 'cid': cid, 'amt': amt})
		else:
			print(f'WARNING ???????????? -> {merchandise}')
	return dark_markets


async def set_darkmarket(uid, pid, gid, mid, qty, cid, amt, **kwargs):
	await common.execute(f'INSERT INTO darkmarket (uid, pid, gid, mid, qty, cid, amt) VALUES ("{uid}", {pid}, {gid}, {mid}, {qty}, {cid}, {amt}) ON DUPLICATE KEY UPDATE `gid`= values(`gid`), `mid`= values(`mid`), `qty`= values(`qty`), `cid`= values(`cid`), `amt`= values(`amt`);', **kwargs)


