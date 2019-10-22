'''
factory.py
'''

from module import enums
from module import common

async def refresh(uid, **kwargs):
	levels, workers, storage = await _get_factory_info(uid, **kwargs)
	storage = step(storage, workers, **kwargs)
	return common.mt(0, 'success', storage)


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

def step(current, workers, **kwargs):
	for fac in reversed(enums.Factory):
		for _ in range(workers[fac]):
			if fac == enums.Factory.FOOD or can_produce(current, fac, **kwargs):
				current[fac] += 1
			else: break
	return current

async def _get_factory_info(uid, **kwargs):
	data = await common.execute(f'SELECT fid, level, workers, storage FROM factory WHERE uid = "{uid}";', **kwargs)
	storage = {e : 0 for e in enums.Factory}
	workers = {e : 0 for e in enums.Factory}
	levels  = {e : 1 for e in enums.Factory}
	for fac in data:
		levels[enums.Factory(fac[0])]  = fac[1]
		workers[enums.Factory(fac[0])] = fac[2]
		storage[enums.Factory(fac[0])] = fac[3]
	return (levels, workers, storage)
