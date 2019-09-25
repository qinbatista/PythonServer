'''
summoning.py
'''

from module import enums
from module import common
from module import lottery

# Tier
# basic, friend, pro, prophet
# RewardGroup
# weapon, skill, role

SWITCH = {}

async def summon(uid, item, tier, rewardgroup, **kwargs):
	return await _base_summon(uid, item, tier, rewardgroup, **kwargs)

##############################################################

async def _base_summon(uid, item, tier, rewardgroup, **kwargs):
	can_pay, remaining = await common.try_item(uid, item, -100, **kwargs)
	if not can_pay: return common.mt(99, 'insufficient materials')
	new, reward = await lottery.random_gift(uid, tier, rewardgroup, **kwargs)
	return await _response_factory(uid, rewardgroup, new, reward, item, remaining, **kwargs)

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
		return common.mt(0, 'new skill unlocked', {'remaining' : {'weapon' : reward.value, 'star' : 1, 'segment' : 0, 'cost_item' : item.value, 'cost_quantity' : remaining}, 'reward' : {'weapon' : reward.value, 'star' : 1}})
	else:
		star, segment = (await common.execute(f'SELECT star, segment FROM weapon WHERE uid = "{uid}" AND wid = "{reward.value}";', **kwargs))[0]
		return common.mt(3, 'get segment',{'remaining' : {'weapon' : reward.value, 'star' : star, 'segment' : segment, 'cost_item' : item.value, 'cost_quantity' : remaining}, 'reward' : {'weapon' : reward.value, 'star' : star}})

async def _response_factory_role(uid, rewardgroup, new, reward, item, remaining, **kwargs):
	if new:
		return common.mt(4, 'new role unlocked', {'remaining' : {'role' : reward.value, 'star' : 1, 'segment' : 0, 'cost_item' : item.value, 'cost_quantity' : remaining}, 'reward' : {'role' : reward.value, 'star' : 1}})
	else:
		star, segment = (await common.execute(f'SELECT star, segment FROM role WHERE uid = "{uid}" AND rid = "{reward.value}";', **kwargs))[0]
		return common.mt(3, 'get segment',{'remaining' : {'role' : reward.value, 'star' : star, 'segment' : segment, 'cost_item' : item.value, 'cost_quantity' : remaining}, 'reward' : {'role' : reward.value, 'star' : star}})



SWITCH[enums.RewardGroup.WEAPON] = _response_factory_weapon
SWITCH[enums.RewardGroup.SKILL] = _response_factory_skill
SWITCH[enums.RewardGroup.ROLE] = _response_factory_role
