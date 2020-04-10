'''
lottery.py
'''
import random

from module import common
from module import summoning
from module import enums
from module import task
from module import achievement


SEG_COUNT = 30

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
	wid = enums.wid(gift)
	wnp = wid.name[:2]
	if wnp in RECORD_SUM:
		await RECORD_SUM[wnp](uid, **kwargs)
	if await common.get_weapon(uid, wid, key='star', **kwargs) == 0:
		await common.set_weapon(uid, wid, val=1, key='star', **kwargs)
		if wnp in RECORD_GET:
			await RECORD_GET[wnp](uid, **kwargs)
		return True, wid
	await common.set_weapon(uid, wid, val=SEG_COUNT, **kwargs)
	return False, wid


async def try_unlock_skill(uid, gift, **kwargs):
	skill = enums.Skill(gift)
	if not await common.exists('skill', ('uid', uid), ('sid', skill.value), **kwargs):
		await common.execute(f'INSERT INTO skill(uid, sid) VALUES ("{uid}", {skill.value});', **kwargs)
		return True, skill
	await common.execute(f'INSERT INTO item (uid, iid, value) VALUES ("{uid}", {enums.Item.SKILL_SCROLL_10.value}, 1) ON DUPLICATE KEY UPDATE value = value + 1;', **kwargs)
	return False, enums.Item.SKILL_SCROLL_10


async def try_unlock_role(uid, gift, **kwargs):
	rid = enums.Role(gift)
	rnp = rid.name[:2]
	if rnp in RECORD_SUM:
		await RECORD_SUM[rnp](uid, **kwargs)
	if await common.get_role(uid, rid, key='star', **kwargs) == 0:
		await common.set_role(uid, rid, val=1, key='star', **kwargs)
		if rnp in RECORD_GET: await RECORD_GET[rnp](uid, **kwargs)
		return True, rid
	await common.set_role(uid, rid, val=SEG_COUNT, **kwargs)
	return False, rid


SWITCH[enums.Group.WEAPON] = try_unlock_weapon
SWITCH[enums.Group.SKILL] = try_unlock_skill
SWITCH[enums.Group.ROLE] = try_unlock_role


RECORD_GET = {
	"R4": lambda uid, **kwargs: achievement.record(uid, enums.Achievement.GET_4R, **kwargs),
	"R5": lambda uid, **kwargs: achievement.record(uid, enums.Achievement.GET_5R, **kwargs),
	"R6": lambda uid, **kwargs: achievement.record(uid, enums.Achievement.GET_6R, **kwargs),
	"W4": lambda uid, **kwargs: achievement.record(uid, enums.Achievement.GET_4W, **kwargs),
	"W5": lambda uid, **kwargs: achievement.record(uid, enums.Achievement.GET_5W, **kwargs),
	"W6": lambda uid, **kwargs: achievement.record(uid, enums.Achievement.GET_6W, **kwargs),
}


RECORD_SUM = {
	"R3": lambda uid, **kwargs: achievement.record(uid, enums.Achievement.SUMMON_3R, **kwargs),
	"R4": lambda uid, **kwargs: achievement.record(uid, enums.Achievement.SUMMON_4R, **kwargs),
	"R5": lambda uid, **kwargs: achievement.record(uid, enums.Achievement.SUMMON_5R, **kwargs),
	"W3": lambda uid, **kwargs: achievement.record(uid, enums.Achievement.SUMMON_3W, **kwargs),
	"W4": lambda uid, **kwargs: achievement.record(uid, enums.Achievement.SUMMON_4W, **kwargs),
	"W5": lambda uid, **kwargs: achievement.record(uid, enums.Achievement.SUMMON_5W, **kwargs),
}
