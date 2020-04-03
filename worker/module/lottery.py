'''
lottery.py
'''
import random

from module import common
from module import summoning
from module import enums
from module import task
from module import achievement


STANDARD_SEG_COUNT = 30

SWITCH = {}


async def random_gift(uid, tier, rewardgroup, **kwargs):
	t = (random.choices(range(len(kwargs['config']['lottery']['random_gift'][rewardgroup.name]['weights'][tier.name])), kwargs['config']['lottery']['random_gift'][rewardgroup.name]['weights'][tier.name]))[0]
	gift = (random.choices(kwargs['config']['lottery']['random_gift'][rewardgroup.name]['rewards'][t]))[0]
	return await SWITCH[rewardgroup](uid, gift, **kwargs)


async def fortune_wheel(uid, tier, item, **kwargs):
	cost = kwargs['config']['lottery']['fortune_wheel']['cost'][tier.name][f'{enums.Group.ITEM.value}:{item.value}']
	can_pay, remaining = await common.try_item(uid, item, -cost, **kwargs)
	if not can_pay: return common.mt(99, 'insufficient materials')
	t = (random.choices(range(len(kwargs['config']['lottery']['fortune_wheel']['weights'][tier.name])), kwargs['config']['lottery']['fortune_wheel']['weights'][tier.name]))[0]
	giftcode = (random.choices(kwargs['config']['lottery']['fortune_wheel']['items'][t]))[0]
	group, enum_id = giftcode.split(':')
	if enums.Group(int(group)) == enums.Group.ITEM:
		_, quantity = await common.try_item(uid, enums.Item(int(enum_id)), kwargs['config']['lottery']['fortune_wheel']['rewards'][tier.name][giftcode], **kwargs)
		return common.mt(6, 'get item', {'remaining' : {'item_id' : enum_id, 'item_quantity' : quantity, 'cost_item' : item.value, 'cost_quantity' : remaining}, 'reward' : {'item_id' : enum_id, 'item_quantity' : kwargs['config']['lottery']['fortune_wheel']['rewards'][tier.name][giftcode], 'cost_item' : item.value, 'cost_quantity' : cost}})
	else:
		new, reward = await SWITCH[enums.Group(int(group))](uid, int(enum_id), **kwargs)
		return await summoning._response_factory(uid, enums.Group(int(group)), new, reward, item, remaining, cost, **kwargs)

#######################################################################################################


async def try_unlock_weapon(uid, gift, **kwargs):
	weapon = enums.Weapon(gift)
	if not await common.exists('weapon', ('uid', uid), ('wid', weapon.value), **kwargs):
		await common.execute(f'INSERT INTO weapon(uid, wid, star) VALUES ("{uid}", {weapon.value}, 1);', **kwargs)
		await RECORD[weapon.name[:2]](uid, **kwargs)
		return True, weapon
	await common.execute(f'UPDATE weapon SET segment = segment + {STANDARD_SEG_COUNT} WHERE uid = "{uid}" AND wid = {weapon.value};', **kwargs)
	return False, weapon


async def try_unlock_skill(uid, gift, **kwargs):
	skill = enums.Skill(gift)
	if not await common.exists('skill', ('uid', uid), ('sid', skill.value), **kwargs):
		await common.execute(f'INSERT INTO skill(uid, sid) VALUES ("{uid}", {skill.value});', **kwargs)
		return True, skill
	await common.execute(f'INSERT INTO item (uid, iid, value) VALUES ("{uid}", {enums.Item.SKILL_SCROLL_10.value}, 1) ON DUPLICATE KEY UPDATE value = value + 1;', **kwargs)
	return False, enums.Item.SKILL_SCROLL_10


async def try_unlock_role(uid, gift, **kwargs):
	role = enums.Role(gift)
	if not await common.exists('role', ('uid', uid), ('rid', role.value), **kwargs):
		await common.execute(f'INSERT INTO role(uid, rid, star) VALUES ("{uid}", {role.value}, 1);', **kwargs)
		await RECORD[role.name[:2]](uid, **kwargs)
		return True, role
	await common.execute(f'UPDATE role SET segment = segment + {STANDARD_SEG_COUNT} WHERE uid = "{uid}" AND rid = {role.value};', **kwargs)
	return False, role


SWITCH[enums.Group.WEAPON] = try_unlock_weapon
SWITCH[enums.Group.SKILL] = try_unlock_skill
SWITCH[enums.Group.ROLE] = try_unlock_role


async def ach_record(uid, aids, **kwargs):
	[await achievement.record(uid, aid, **kwargs) for aid in aids]


RECORD = {
	"R4": lambda uid, **kwargs: ach_record(uid, [enums.Achievement.GET_4_STAR_ROLE, enums.Achievement.SUMMON_4_STAR_ROLE_TIMES], **kwargs),
	"R5": lambda uid, **kwargs: ach_record(uid, [enums.Achievement.GET_5_STAR_ROLE, enums.Achievement.SUMMON_5_STAR_ROLE_TIMES], **kwargs),
	"R6": lambda uid, **kwargs: ach_record(uid, [enums.Achievement.GET_6_STAR_ROLE, enums.Achievement.SUMMON_6_STAR_ROLE_TIMES], **kwargs),
	"W4": lambda uid, **kwargs: ach_record(uid, [enums.Achievement.GET_4_STAR_WEAPON, enums.Achievement.SUMMON_4_STAR_WEAPON_TIMES], **kwargs),
	"W5": lambda uid, **kwargs: ach_record(uid, [enums.Achievement.GET_5_STAR_WEAPON, enums.Achievement.SUMMON_5_STAR_WEAPON_TIMES], **kwargs),
	"W6": lambda uid, **kwargs: ach_record(uid, [enums.Achievement.GET_6_STAR_WEAPON, enums.Achievement.SUMMON_6_STAR_WEAPON_TIMES], **kwargs),
}
