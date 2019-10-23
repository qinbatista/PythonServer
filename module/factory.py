'''
factory.py
'''

from module import enums
from module import common

async def refresh(uid, **kwargs):
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
	existing, workers = await _get_unassigned_workers(uid, **kwargs)
	print(f'existing: {existing}')
	print(f'workers : {workers}')
	return common.mt(0, 'success')


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
	data = await common.execute(f'SELECT workers FROM factory WHERE uid = "{uid}" AND fid = {enums.Factory.UNASSIGNED.value};', **kwargs)
	return (False, 0) if data == () else (True, data[0][0])
