'''
summoning.py
'''

from module import enums
from module import common
from module import lottery
from module import task

# Tier
# basic, friend, pro, prophet
# RewardGroup
# weapon, skill, role

SWITCH = {}

async def summon(uid, item, tier, rewardgroup, **kwargs):
	return await _base_summon(uid, item, tier, rewardgroup, **kwargs)

async def summon_multi(uid, item, tier, rewardgroup, num_times = 10, **kwargs):
	return await _base_summon_multi(uid, item, tier, rewardgroup, num_times, **kwargs)

##############################################################

async def _base_summon(uid, item, tier, rewardgroup, **kwargs):

	cost = kwargs['config']['lottery']['random_gift'][rewardgroup.name]['cost'][f'{enums.Group.ITEM.value}:{item.value}']
	can_pay, remaining = await common.try_item(uid, item, -cost, **kwargs)
	if not can_pay: return common.mt(99, 'insufficient materials')
	new, reward = await lottery.random_gift(uid, tier, rewardgroup, **kwargs)
	if enums.Tier.BASIC:
		kwargs.update({"tid":enums.Task.BASIC_SUMMONING,"task_value":1})
		await task.record_task(uid,**kwargs)
	if enums.Tier.PRO:
		kwargs.update({"tid":enums.Task.PRO_SUMMONING,"task_value":1})
		await task.record_task(uid,**kwargs)
	return await _response_factory(uid, rewardgroup, new, reward, item, remaining, **kwargs)

async def _base_summon_multi(uid, item, tier, rewardgroup, num_times, **kwargs):
	can_pay, remaining = await common.try_item(uid, item, -100 * num_times, **kwargs)
	if not can_pay: return common.mt(99, 'insufficient materials')
	response = {'remaining' : {}, 'reward' : {}}
	for time in range(num_times):
		new, reward = await lottery.random_gift(uid, tier, rewardgroup, **kwargs)
		result = await _response_factory(uid, rewardgroup, new, reward, item, remaining, **kwargs)
		response['remaining'][time] = result['data']['remaining']
		response['reward'][time] = result['data']['reward']
	return common.mt(0, 'success', response)


async def _response_factory(uid, rewardgroup, new, reward, item, remaining, **kwargs):
	return await SWITCH[rewardgroup](uid, rewardgroup, new, reward, item, remaining, **kwargs)

async def _response_factory_weapon(uid, rewardgroup, new, reward, item, remaining, **kwargs):
	if new:
		return common.mt(2, 'new weapon unlocked', {'remaining' : {'weapon' : reward.value, 'star' : 1, 'segment' : 0, 'cost_item' : item.value, 'cost_quantity' : remaining}, 'reward' : {'weapon' : reward.value, 'star' : 1}})
	else:
		star, segment = (await common.execute(f'SELECT star, segment FROM weapon WHERE uid = "{uid}" AND wid = "{reward.value}";', **kwargs))[0]
		return common.mt(3, 'get segment',{'remaining' : {'weapon' : reward.value, 'star' : star, 'segment' : segment, 'cost_item' : item.value, 'cost_quantity' : remaining}, 'reward' : {'weapon' : reward.value, 'star' : star}})

async def _response_factory_skill(uid, rewardgroup, new, reward, item, remaining, **kwargs):
	if new:
		return common.mt(0, 'new skill unlocked', {'remaining' : {'skill' : reward.value, 'star' : 1, 'segment' : 0, 'cost_item' : item.value, 'cost_quantity' : remaining}, 'reward' : {'skill' : reward.value, 'level' : 1}})
	else:
		scroll_quantity = (await common.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = {reward.value};', **kwargs))[0][0]
		return common.mt(1, 'get scroll', {'remaining' : {'scroll_id' : reward.value, 'scroll_quantity' : scroll_quantity, 'cost_item' : item.value, 'cost_quantity' : remaining}, 'reward' : {'scroll_id' : reward.value, 'scroll_quantity' : 1}})

async def _response_factory_role(uid, rewardgroup, new, reward, item, remaining, **kwargs):
	if new:
		return common.mt(4, 'new role unlocked', {'remaining' : {'role' : reward.value, 'star' : 1, 'segment' : 0, 'cost_item' : item.value, 'cost_quantity' : remaining}, 'reward' : {'role' : reward.value, 'star' : 1}})
	else:
		star, segment = (await common.execute(f'SELECT star, segment FROM role WHERE uid = "{uid}" AND rid = "{reward.value}";', **kwargs))[0]
		return common.mt(5, 'get segment',{'remaining' : {'role' : reward.value, 'star' : star, 'segment' : segment, 'cost_item' : item.value, 'cost_quantity' : remaining}, 'reward' : {'role' : reward.value, 'star' : star}})



SWITCH[enums.Group.WEAPON] = _response_factory_weapon
SWITCH[enums.Group.SKILL] = _response_factory_skill
SWITCH[enums.Group.ROLE] = _response_factory_role
