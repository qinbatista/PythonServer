'''
lottery.py
'''
import random

from module import common
from module import summoning
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
# wep = 0, skill = 1, role = 2, item = 3
unused = \
{
	"weights" : {
		"BASIC" : [0.6, 0.1, 0.25, 0.05]
		},
	"items" : [
		["2,1", "2,1", "2,1", "2,1"],
		["2,1", "2,1", "2,1", "2,1"],
		["2,1", "2,1", "2,1", "2,1"],
		["2,1", "2,1", "2,1", "2,1"],
		],
	"rewards" : {
		"BASIC" : {
			"2,1" : 1
			}
		}
}

STANDARD_SEG_COUNT = 30

SWITCH = {}

async def random_gift(uid, tier, rewardgroup, **kwargs):
	t = (random.choices(range(len(L[rewardgroup.name]['weights'][tier.name])), L[rewardgroup.name]['weights'][tier.name]))[0]
	gift = (random.choices(L[rewardgroup.name]['rewards'][t]))[0]
	return await SWITCH[rewardgroup](uid, gift, **kwargs)

async def fortune_wheel(uid, tier, item, **kwargs):
	can_pay, remaining = await common.try_item(uid, item, -100, **kwargs)
	if not can_pay: return common.mt(99, 'insufficient materials')
	t = (random.choices(range(len(kwargs['config']['lottery']['fortune_wheel']['weights'][tier.name])), kwargs['config']['lottery']['fortune_wheel']['weights'][tier.name]))[0]
	giftcode = (random.choices(kwargs['config']['lottery']['fortune_wheel']['items'][t]))[0]
	group, enum_id = giftcode.split(':')
	if enums.Group(int(group)) == enums.Group.ITEM:
		_, quantity = await common.try_item(uid, enums.Item(int(enum_id)), kwargs['config']['lottery']['fortune_wheel']['rewards'][tier.name][giftcode], **kwargs)
		return common.mt(5, 'get item', {'remaining' : {'cost_item' : item.value, 'cost_quantity' : remaining, 'group_id' : group, 'enum_id' : enum_id, 'item_quantity' : quantity}, 'reward' : {'group_id' : group, 'enum_id' : enum_id, 'item_quantity' : kwargs['config']['lottery']['fortune_wheel']['rewards'][tier.name][giftcode]}})
	else:
		new, reward = await SWITCH[enums.Group(int(group))](uid, int(enum_id), **kwargs)
		return await summoning._response_factory(uid, enums.Group(int(group)), new, reward, item, remaining, **kwargs)

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

SWITCH[enums.Group.WEAPON] = _try_unlock_weapon
SWITCH[enums.Group.SKILL] = _try_unlock_skill
SWITCH[enums.Group.ROLE] = _try_unlock_role
