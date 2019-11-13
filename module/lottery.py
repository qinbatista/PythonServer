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
	cost = kwargs['config']['lottery']['fortune_wheel']['cost'][f'{enums.Group.ITEM.value}:{item.value}']
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


async def _try_unlock_weapon(uid, gift, **kwargs):
	weapon = enums.Weapon(gift)
	if weapon.name in kwargs['config']['weapon']['star_4']:
		kwargs.update({"aid": enums.Achievement.GET_4_STAR_WEAPON})
		await achievement.record_achievement(uid,**kwargs)
	if weapon.name in kwargs['config']['weapon']['star_5']:
		kwargs.update({"aid": enums.Achievement.GET_5_STAR_WEAPON})
		await achievement.record_achievement(uid,**kwargs)
	if weapon.name in kwargs['config']['weapon']['star_6']:
		kwargs.update({"aid": enums.Achievement.GET_6_STAR_WEAPON})
		await achievement.record_achievement(uid,**kwargs)
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
	if role.name in kwargs['config']['role']['star_4']:
		kwargs.update({"aid": enums.Achievement.GET_4_STAR_ROLE})
		await achievement.record_achievement(uid,**kwargs)
	if role.name in kwargs['config']['role']['star_5']:
		kwargs.update({"aid": enums.Achievement.GET_5_STAR_ROLE})
		await achievement.record_achievement(uid,**kwargs)
	if role.name in kwargs['config']['role']['star_6']:
		kwargs.update({"aid": enums.Achievement.GET_6_STAR_ROLE})
		await achievement.record_achievement(uid,**kwargs)
	if not await common.exists('role', ('uid', uid), ('rid', role.value), **kwargs):
		await common.execute(f'INSERT INTO role(uid, rid) VALUES ("{uid}", {role.value});', **kwargs)
		return (True, role)
	await common.execute(f'UPDATE role SET segment = segment + {STANDARD_SEG_COUNT} WHERE uid = "{uid}" AND rid = {role.value};', **kwargs)
	return (False, role)

SWITCH[enums.Group.WEAPON] = _try_unlock_weapon
SWITCH[enums.Group.SKILL] = _try_unlock_skill
SWITCH[enums.Group.ROLE] = _try_unlock_role
