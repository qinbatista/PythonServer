'''
factory.py
'''

from module import enums
from module import common

from datetime import datetime, timezone

async def refresh(uid, **kwargs):
	first_time, timer = await _get_time_since_last_refresh(uid, **kwargs)
	if first_time:
		await common.execute(f'INSERT INTO timer VALUES ("{uid}", {enums.Timer.FACTORY_REFRESH.value}, {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")});', **kwargs)
		return common.mt(1, 'factory initiated')
	time = datetime.strptime(timer, '%Y-%m-%d %H:%M:%S').replace(tzinfo = timezone.utc)
	delta = datetime.now(timezone.utc) - time
	print(f'seconds since: {int(delta.total_seconds())}')
	levels, workers, storage = await _get_factory_info(uid, **kwargs)
	storage = step(storage, workers, levels, **kwargs)
	await _record_storage(uid, storage, **kwargs)
	return common.mt(0, 'success', storage)

async def upgrade(uid, fid, **kwargs):
	fid = enums.Factory(fid)
	if fid == enums.Factory.UNASSIGNED: return common.mt(99, 'invalid fid')
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



###################################################################################
def can_produce(current, factory_type, **kwargs):
	cost = {}
	for material, amount in kwargs['config']['factory']['general']['costs'][str(factory_type.value)].items():
		if current[enums.Factory(int(material))] < amount:
			return False
		cost[enums.Factory(int(material))] = amount
	for material, amount in cost.items():
		current[material] -= amount
	return True

def step(current, workers, levels, **kwargs):
	for fac in reversed(enums.Factory):
		if fac != enums.Factory.UNASSIGNED:
			for _ in range(workers[fac]):
				if fac == enums.Factory.FOOD or can_produce(current, fac, **kwargs):
					current[fac] = min(current[fac] + 1, kwargs['config']['factory']['general']['storage_limits'][str(fac.value)][str(levels[fac])])
				else: break
	return current

async def _record_storage(uid, storage, **kwargs):
	for fac, amount in storage.items():
		await common.execute(f'INSERT INTO factory (uid, fid, storage) VALUES ("{uid}", {fac.value}, {amount}) ON DUPLICATE KEY UPDATE storage = {amount};', **kwargs)

async def _get_factory_info(uid, **kwargs):
	data = await common.execute(f'SELECT fid, level, workers, storage FROM factory WHERE uid = "{uid}";', **kwargs)
	storage = {e : 0 for e in enums.Factory if e != enums.Factory.UNASSIGNED}
	workers = {e : 0 for e in enums.Factory if e != enums.Factory.UNASSIGNED}
	levels  = {e : 1 for e in enums.Factory if e != enums.Factory.UNASSIGNED}
	for fac in data:
		if fac[0] != enums.Factory.UNASSIGNED.value:
			levels[enums.Factory(fac[0])]  = fac[1]
			workers[enums.Factory(fac[0])] = fac[2]
			storage[enums.Factory(fac[0])] = fac[3]
	return (levels, workers, storage)

async def _get_unassigned_workers(uid, **kwargs):
	data = await common.execute(f'SELECT workers, storage FROM factory WHERE uid = "{uid}" AND fid = {enums.Factory.UNASSIGNED.value};', **kwargs)
	return (False, 0, 0) if data == () else (True, data[0][0], data[0][1])

async def _get_time_since_last_refresh(uid, **kwargs):
	data = await common.execute(f'SELECT time FROM timer WHERE uid = "{uid}" AND tid = {enums.Timer.FACTORY_REFRESH.value};', **kwargs)
	return (True, None) if data == () else (False, data[0][0])
