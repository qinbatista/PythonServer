'''
factory.py
'''

from module import enums
from module import common


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
			if fac == enums.Factory.FOOD or can_produce(fac, current, **kwargs):
				current[fac] += 1
			else: break
	return current
