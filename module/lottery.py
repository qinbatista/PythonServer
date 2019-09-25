'''
lottery.py
'''
import random

from module import common
from module import enums

L = \
{
	"WEAPON" : {
		"weights" : {
			"BASIC" : [0.6, 0.4]
		},
		"rewards":[
			[1, 2, 3],
			[4, 5, 6, 7]
			]
	},
	"SKILL" : {
		"weights" : {
			"BASIC" : [0.6, 0.4]
		},
		"rewards":[
			[1, 2, 3],
			[4, 5, 6, 7]
			]
	},
	"ROLE" : {
		"weights" : {
			"BASIC" : [0.6, 0.4]
		},
		"rewards":[
			[1, 2, 3],
			[4, 5, 6, 7]
			]
	}
}
STANDARD_SEG_COUNT = 30

SWITCH = {}

async def random_gift(uid, tier, rewardgroup, **kwargs):
	tier = (random.choices(range(len(L[rewardgroup.name]['weights'][tier.name])), L[rewardgroup.name]['weights'][tier.name]))[0]
	gift = (random.choices(L[rewardgroup.name]['rewards'][tier]))[0]
	return await SWITCH[rewardgroup](uid, gift, **kwargs)

#######################################################################################################

async def _try_unlock_weapon(uid, gift, **kwargs):
	weapon = enums.Weapon(gift)
	if not await common.exists('weapon', ('uid', uid), ('wid', weapon.value), **kwargs):
		await common.execute(f'INSERT INTO weapon(uid, wid) VALUES ("{uid}", {weapon.value});', **kwargs)
		return (True, weapon)
	await common.execute(f'UPDATE weapon SET segment = segment + {STANDARD_SEG_COUNT} WHERE uid = "{uid}" AND wid = {weapon.value};', **kwargs)
	return (False, weapon)

async def _try_unlock_skill(uid, gift, **kwargs):
	skill = enums.Skill(gift)
	if not await common.exists('skill', ('uid', uid), ('sid', skill.value), **kwargs):
		await common.execute(f'INSERT INTO skill(uid, sid) VALUES ("{uid}", {skill.value});', **kwargs)
		return (True, skill)
	await common.execute(f'INSERT INTO item (uid, iid, value) VALUES ("{uid}", {enums.Item.SKILL_SCROLL_10.value}, 1) ON DUPLICATE KEY UPDATE value = value + 1;', **kwargs)
	return (False, enums.Item.SKILL_SCROLL_10)

async def _try_unlock_role(uid, gift, **kwargs):
	role = enums.Role(gift)
	if not await common.exists('role', ('uid', uid), ('rid', role.value), **kwargs):
		await common.execute(f'INSERT INTO role(uid, rid) VALUES ("{uid}", {role.value});', **kwargs)
		return (True, role)
	await common.execute(f'UPDATE role SET segment = segment + {STANDARD_SEG_COUNT} WHERE uid = "{uid}" AND rid = {role.value};', **kwargs)
	return (False, role)

SWITCH[enums.RewardGroup.WEAPON] = _try_unlock_weapon
SWITCH[enums.RewardGroup.SKILL] = _try_unlock_skill
SWITCH[enums.RewardGroup.ROLE] = _try_unlock_role
