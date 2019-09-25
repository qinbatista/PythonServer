'''
lottery.py
'''
import random

from module import common

L = \
{
	"WEAPON" : {
		"cost" : {
			"COIN" : 100
		},
		"tiers" : ["tier1", "tier2"],
		"weights" : {
			"BASIC" : [0.6, 0.4]
		},
		"items" : {
			"tier1" : [1, 2, 3],
			"tier2" : [4, 5, 6, 7]
		}
	}
}

SWITCH = {}

async def random_gift(uid, rewardgroup, tier, **kwarg):
	tier = (random.choices(L[rewardgroup.name]['tiers'], L[rewardgroup.name]['weights'][tier.name]))[0]
	gift = (random.choices(L[rewardgroup.name]['items'][tier]))[0]
	return await SWITCH[rewardgroup](uid, gift, **kwargs)

#######################################################################################################

async def _try_unlock_weapon(uid, gift, **kwargs):
	weapon = common.Weapon(gift)

async def _try_unlock_skill():
	pass

async def _try_unlock_role():
	pass

SWITCH[common.RewardGroup.WEAPON] = _try_unlock_weapon
SWITCH[common.RewardGroup.SKILL] = _try_unlock_skill
SWITCH[common.RewardGroup.ROLE] = _try_unlock_role
