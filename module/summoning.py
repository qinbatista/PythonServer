'''
summoning.py
'''

from module import common
from module import enums

# Tier
# basic, friend, pro, prophet
# RewardGroup
# weapon, skill, role

async def summon(uid, item, tier, reward, **kwargs):
	return await _base_summon(uid, item, tier, reward, **kwargs)

##############################################################

async def _base_summon(uid, item, tier, reward, **kwargs):
	can_pay, _ = await common.try_item(uid, item, -100, **kwargs)
	if not can_pay: return common.mt(99, 'insufficient materials')
	return common.mt(0, 'success')

