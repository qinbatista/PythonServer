'''
factory.py
'''
import random

from module import enums
from module import common
from module import weapon

from datetime import datetime, timezone, timedelta

BASIC_FACTORIES = {enums.Factory.FOOD, enums.Factory.IRON, enums.Factory.CRYSTAL}


async def refresh(uid, **kwargs):
	steps = await _steps_since(uid, enums.Timer.FACTORY_REFRESH, **kwargs)
	if steps is None:
		await common.execute(f'INSERT INTO timer VALUES ("{uid}", {enums.Timer.FACTORY_REFRESH.value}, "{datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}");', **kwargs)
		return common.mt(1, 'factory initiated')
	await common.execute(f'UPDATE timer SET time = "{datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}" WHERE uid = "{uid}" AND tid = {enums.Timer.FACTORY_REFRESH.value};', **kwargs)
	levels, workers, storage = await _get_factory_info(uid, **kwargs)
	for _ in range(steps):
		storage = step(storage, workers, levels, **kwargs)
	await _record_storage(uid, storage, **kwargs)
	return common.mt(0, 'success', storage)

# TODO max level checking
async def upgrade(uid, fid, **kwargs):
	fid = enums.Factory(fid)
	if fid not in BASIC_FACTORIES: return common.mt(99, 'invalid fid')
	levels, _, storage = await _get_factory_info(uid, **kwargs)
	upgrade_cost = kwargs['config']['factory']['general']['upgrade_cost'][str(fid.value)][str(levels[fid] + 1)]
	if storage[fid] < upgrade_cost: return common.mt(98, 'insufficient funds')
	await common.execute(f'UPDATE factory SET level = {levels[fid] + 1}, storage = {storage[fid] - upgrade_cost} WHERE uid = "{uid}" AND fid = {fid.value};', **kwargs)
	return common.mt(0, 'success', {'level' : levels[fid] + 1, 'storage' : storage[fid] - upgrade_cost})

async def buy_worker(uid, **kwargs):
	existing, workers, max_workers = await _get_unassigned_workers(uid, **kwargs)
	if max_workers >= kwargs['config']['factory']['workers']['max']:
		return common.mt(99, 'already max workers')
	upgrade_cost = kwargs['config']['factory']['workers']['cost'][str(max_workers + 1)]
	_, __, storage = await _get_factory_info(uid, **kwargs)
	if storage[enums.Factory.FOOD] < upgrade_cost:return common.mt(98,'insufficient funds')
	await common.execute(f'UPDATE factory SET storage = {storage[enums.Factory.FOOD] - upgrade_cost} WHERE uid = "{uid}" AND fid = {enums.Factory.FOOD.value};', **kwargs)
	if existing:
		stmt = f'UPDATE factory SET workers = {workers + 1}, storage = {max_workers + 1} WHERE uid = "{uid}" AND fid = {enums.Factory.UNASSIGNED.value};'
	else:
		stmt = f'INSERT INTO factory (uid, fid, workers, storage) VALUES ("{uid}", {enums.Factory.UNASSIGNED.value}, {workers + 1}, {max_workers + 1});'
	await common.execute(stmt, **kwargs) 
	return common.mt(0, 'success', {'unassigned' : workers + 1, 'total' : max_workers + 1, 'food' : storage[enums.Factory.FOOD] - upgrade_cost})

async def increase_worker(uid, fid, num, **kwargs):
	fid = enums.Factory(fid)
	_, unassigned, max_workers = await _get_unassigned_workers(uid, **kwargs)
	levels, current_workers, _ = await _get_factory_info(uid, **kwargs)
	if num > unassigned: return common.mt(99, 'insufficient unassigned workers')
	if current_workers[fid] + num > kwargs['config']['factory']['general']['worker_limits'][str(fid.value)][str(levels[fid])]: return common.mt(98, 'cant increase past max worker')
	await common.execute(f'UPDATE factory SET workers = {unassigned - num} WHERE uid = "{uid}" AND fid = {enums.Factory.UNASSIGNED.value};', **kwargs)
	await common.execute(f'INSERT INTO factory (uid, fid, workers) VALUES ("{uid}", {fid.value}, {current_workers[fid] + num}) ON DUPLICATE KEY UPDATE workers = {current_workers[fid] + num};', **kwargs)
	return common.mt(0, 'success', {'unassigned' : unassigned - num, 'workers' : current_workers[fid] + num})

async def decrease_worker(uid, fid, num, **kwargs):
	fid = enums.Factory(fid)
	_, current_workers, __ = await _get_factory_info(uid, **kwargs)
	_, unassigned, __ = await _get_unassigned_workers(uid, **kwargs)
	if num > current_workers[fid]: return common.mt(99, 'insufficient assigned workers')
	await common.execute(f'INSERT INTO factory (uid, fid, workers) VALUES ("{uid}", {fid.value}, {current_workers[fid] - num}) ON DUPLICATE KEY UPDATE workers = {current_workers[fid] - num};', **kwargs)
	await common.execute(f'UPDATE factory SET workers = {unassigned + num} WHERE uid = "{uid}" AND fid = {enums.Factory.UNASSIGNED.value};', **kwargs)
	return common.mt(0, 'success', {'unassigned' : unassigned + num, 'workers' : current_workers[fid] - num})

async def purchase_acceleration(uid, **kwargs):
	can_pay, remaining_diamond = await common.try_item(uid, enums.Item.DIAMOND, -kwargs['config']['factory']['general']['acceleration_cost'], **kwargs)
	if not can_pay: return common.mt(99, 'insufficient funds')
	accel_start, accel_end = await _acceleration_time(uid, **kwargs)
	now = datetime.now(timezone.utc)
	if accel_start is None:
		await common.execute(f'INSERT INTO `timer` VALUES ("{uid}", {enums.Timer.FACTORY_ACCELERATION_START.value}, "{now.strftime("%Y-%m-%d %H:%M:%S")}");', **kwargs)
		await common.execute(f'INSERT INTO `timer` VALUES ("{uid}", {enums.Timer.FACTORY_ACCELERATION_END.value}, "{(now + timedelta(days = 1)).strftime("%Y-%m-%d %H:%M:%S")}");', **kwargs)
	else:
		if now > accel_start:
			await common.execute(f'UPDATE `timer` SET `time` = "{now.strftime("%Y-%m-%d %H:%M:%S")}" WHERE uid = "{uid}" AND tid = {enums.Timer.FACTORY_ACCELERATION_START.value};', **kwargs)
		await common.execute(f'UPDATE `timer` SET `time` = "{max(accel_end + timedelta(days = 1), now + timedelta(days = 1)).strftime("%Y-%m-%d %H:%M:%S")}" WHERE uid = "{uid}" AND tid = {enums.Timer.FACTORY_ACCELERATION_END.value};', **kwargs)
	accel_start, accel_end = await _acceleration_time(uid, **kwargs)
	return common.mt(0, 'success', {'start' : accel_start.strftime('%Y-%m-%d %H:%M:%S'), 'end' : accel_end.strftime('%Y-%m-%d %H:%M:%S'), 'diamond' : remaining_diamond})

# adds random number of segments to the given weapon, regardless if they have unlocked that weapon or not
# TODO bad code, should refactor
# TODO update return formats
async def activate_wishing_pool(uid, wid, **kwargs):
	wid = enums.Weapon(wid)
	first_time, timer = await _get_time_since_last_wishing_pool(uid, **kwargs)
	level = await _get_wishing_pool_level(uid, **kwargs)
	_, remaining_diamond = await common.try_item(uid, enums.Item.DIAMOND, 0, **kwargs)
	if first_time:
		await common.execute(f'INSERT INTO timer VALUES ("{uid}", {enums.Timer.FACTORY_WISHING_POOL.value}, "{datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}");', **kwargs)
		await common.execute(f'INSERT INTO limits VALUES ("{uid}", {enums.Limits.FACTORY_WISHING_POOL_COUNT.value}, 0);', **kwargs)
	else:
		seconds_since = int((datetime.now(timezone.utc) - datetime.strptime(timer, '%Y-%m-%d %H:%M:%S').replace(tzinfo = timezone.utc)).total_seconds())
		if seconds_since >= (kwargs['config']['factory']['wishing_pool']['base_recover'] - level) * 3600:
			await common.execute(f'UPDATE timer SET time = "{datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}" WHERE uid = "{uid}" AND tid = {enums.Timer.FACTORY_WISHING_POOL.value};', **kwargs)
			await common.execute(f'UPDATE limits SET value = 0 WHERE uid = "{uid}" AND lid = {enums.Limits.FACTORY_WISHING_POOL_COUNT.value};', **kwargs)
		else:
			_, count = await _get_wishing_pool_count(uid, **kwargs)
			can_pay, remaining_diamond = await common.try_item(uid, enums.Item.DIAMOND, -1 * count * kwargs['config']['factory']['wishing_pool']['base_diamond'], **kwargs)
			if not can_pay: return common.mt(99, 'insufficient diamonds')
			await common.execute(f'INSERT INTO limits VALUES ("{uid}", {enums.Limits.FACTORY_WISHING_POOL_COUNT.value}, {count + 1}) ON DUPLICATE KEY UPDATE value = {count + 1};', **kwargs)
	remaining_seg = await weapon._update_segment(uid, wid, roll_segment_value(**kwargs), **kwargs)
	return common.mt(0, 'success', {'wid' : wid.value, 'seg' : remaining_seg, 'diamond' : remaining_diamond})

async def upgrade_wishing_pool(uid, **kwargs):
	level = await _get_wishing_pool_level(uid, **kwargs)
	return common.mt(0, 'success')


async def set_armor(uid, aid, **kwargs):
	aid = enums.Armor(aid)
	await common.execute(f'INSERT INTO factory (uid, fid, storage) VALUES ("{uid}", {enums.Factory.ARMOR.value}, {aid.value}) ON DUPLICATE KEY UPDATE storage = {aid.value};', **kwargs)
	return common.mt(0, 'success', {'aid' : aid.value})

async def get_armor(uid, **kwargs):
	data = await common.execute(f'SELECT storage FROM factory WHERE uid = "{uid}" AND fid = {enums.Factory.ARMOR.value};', **kwargs)
	return common.mt(0, 'success', {'aid' : enums.Armor.A1.value if data == () else data[0][0]})

async def refresh_equipment(uid, **kwargs):
	steps = await _get_steps(uid, enums.Timer.FACTORY_EQUIPMENT, **kwargs)
	if steps is None:
		await common.execute(f'INSERT INTO timer VALUES ("{uid}", {enums.Timer.FACTORY_EQUIPMENT.value}, "{datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}");', **kwargs)
		return common.mt(1, 'factory initiated')
	return common.mt(0, 'success')

async def test(uid, tid, **kwargs):
	tid = enums.Timer(tid)
	return common.mt(0, 'test function success', {'steps' : await _steps_since(uid, tid, **kwargs)})



###################################################################################
def roll_segment_value(**kwargs):
	base_seg = kwargs['config']['factory']['wishing_pool']['base_segment']
	rng = random.randint(0, 100)
	if 0 <= rng < 10:
		base_seg *= 3
	elif 10 <= rng < 55:
		base_seg *= 2
	return base_seg

def can_produce(current, factory_type, levels, **kwargs):
	cost = {}
	if current[factory_type] + 1 > kwargs['config']['factory']['general']['storage_limits'][str(factory_type.value)][str(levels[factory_type])]:
		return False
	for material, amount in kwargs['config']['factory']['general']['costs'][str(factory_type.value)].items():
		if current[enums.Factory(int(material))] < amount:
			return False
		cost[enums.Factory(int(material))] = amount
	for material, amount in cost.items():
		current[material] -= amount
	return True

def step(current, workers, levels, **kwargs):
	for fac in reversed(enums.Factory):
		if fac in BASIC_FACTORIES:
			for _ in range(workers[fac]):
				if can_produce(current, fac, levels, **kwargs):
					current[fac] += 1
				else: break
	return current

# NEW
def _steps_between(big, small, step, **kwargs):
	return int((big - small).total_seconds()) // step

# NEW
# returns None if factory has not started yet
async def _steps_since(uid, tid, **kwargs):
	accel_start, accel_end = await _acceleration_time(uid, **kwargs)
	first_time, timer = await _get_timer(uid, tid, **kwargs)
	if first_time: return None
	if accel_start is None:
		accel_start, accel_end = timer, timer
	now = datetime.now(timezone.utc)
	return int(_steps_between(max(accel_start, timer), timer, kwargs['config']['factory']['general']['step']) + \
			_steps_between(min(accel_end, now), max(accel_start, timer), kwargs['config']['factory']['general']['step'] / 2) + \
			_steps_between(now, min(accel_end, now), kwargs['config']['factory']['general']['step']))


# NEW
async def _acceleration_time(uid, **kwargs):
	data = await common.execute(f'SELECT `time` FROM `timer` WHERE uid = "{uid}" AND (tid = {enums.Timer.FACTORY_ACCELERATION_START} OR tid = {enums.Timer.FACTORY_ACCELERATION_END}) ORDER BY `tid`;', **kwargs)
	return (None, None) if data == () else tuple(datetime.strptime(t[0], '%Y-%m-%d %H:%M:%S').replace(tzinfo = timezone.utc) for t in data) # (start, end)

# NEW
async def _get_timer(uid, tid, **kwargs):
	data = await common.execute(f'SELECT `time` FROM `timer` WHERE uid = "{uid}" AND tid = {tid.value};', **kwargs)
	return (True, None) if data == () else (False, datetime.strptime(data[0][0], '%Y-%m-%d %H:%M:%S').replace(tzinfo = timezone.utc))

async def _record_storage(uid, storage, **kwargs):
	for fac, amount in storage.items():
		await common.execute(f'INSERT INTO factory (uid, fid, storage) VALUES ("{uid}", {fac.value}, {amount}) ON DUPLICATE KEY UPDATE storage = {amount};', **kwargs)

async def _get_factory_info(uid, **kwargs):
	data = await common.execute(f'SELECT fid, level, workers, storage FROM factory WHERE uid = "{uid}";', **kwargs)
	storage = {e : 0 for e in enums.Factory if e in BASIC_FACTORIES}
	workers = {e : 0 for e in enums.Factory if e in BASIC_FACTORIES}
	levels  = {e : 1 for e in enums.Factory if e in BASIC_FACTORIES}
	for fac in data:
		if fac[0] != enums.Factory.UNASSIGNED.value:
			levels[enums.Factory(fac[0])]  = fac[1]
			workers[enums.Factory(fac[0])] = fac[2]
			storage[enums.Factory(fac[0])] = fac[3]
	return (levels, workers, storage)

async def _get_unassigned_workers(uid, **kwargs):
	data = await common.execute(f'SELECT workers, storage FROM factory WHERE uid = "{uid}" AND fid = {enums.Factory.UNASSIGNED.value};', **kwargs)
	return (False, 0, 0) if data == () else (True, data[0][0], data[0][1])

async def _get_time_since_last_wishing_pool(uid, **kwargs):
	data = await common.execute(f'SELECT time FROM timer WHERE uid = "{uid}" AND tid = {enums.Timer.FACTORY_WISHING_POOL.value};', **kwargs)
	return (True, None) if data == () else (False, data[0][0])


async def _get_wishing_pool_count(uid, **kwargs):
	data = await common.execute(f'SELECT value FROM limits WHERE uid = "{uid}" AND lid = {enums.Limits.FACTORY_WISHING_POOL_COUNT.value};', **kwargs)
	return (True, 0) if data == () else (False, data[0][0])

async def _get_wishing_pool_level(uid, **kwargs):
	data = await common.execute(f'SELECT level FROM factory WHERE uid = "{uid}" AND fid = {enums.Factory.WISHING_POOL.value};', **kwargs)
	return 0 if data == () else data[0][0]

