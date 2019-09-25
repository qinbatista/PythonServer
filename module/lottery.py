'''
lottery.py
'''
import random

from module import common
from module import enums

L = \
{
	"WEAPON" : {
		"cost" : {
			"COIN" : 100
		},
		"weights" : {
			"BASIC" : [0.6, 0.4]
		},
		"items":[
			[1, 2, 3],
			[4, 5, 6, 7]
			]
	}
}
STANDARD_SEG_COUNT = 30

SWITCH = {}

async def random_gift(uid, rewardgroup, tier, **kwargs):
	tier = (random.choices(range(len(L[rewardgroup.name]['weights'][tier.name])), L[rewardgroup.name]['weights'][tier.name]))[0]
	gift = (random.choices(L[rewardgroup.name]['items'][tier]))[0]
	return await SWITCH[rewardgroup](uid, gift, **kwargs)

#######################################################################################################

async def _try_unlock_weapon(uid, gift, **kwargs):
	weapon = enums.Weapon(gift)
	if await common.exists('weapon', ('uid', uid), ('wid', weapon.value), **kwargs):
		await common.execute(f'UPDATE weapon SET segment = segment + {STANDARD_SEG_COUNT} WHERE uid = "{uid}" AND wid = {weapon.value};', **kwargs)
		return common.mt(1, 'got segments')
	else:
		await common.execute(f'INSERT INTO weapon(uid, wid) VALUES ("{uid}", {weapon.value});', **kwargs)
		return common.mt(0, 'unlocked something new!')

async def _try_unlock_skill(uid, gift, **kwargs):
	skill = enums.Skill(gift)
	if await common.exists('skill', ('uid', uid), ('sid', skill.value), **kwargs):
		pass

async def _try_unlock_role():
	role = enums.Role(gift)

SWITCH[enums.RewardGroup.WEAPON] = _try_unlock_weapon
SWITCH[enums.RewardGroup.SKILL] = _try_unlock_skill
SWITCH[enums.RewardGroup.ROLE] = _try_unlock_role
