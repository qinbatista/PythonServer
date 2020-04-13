'''
lottery.py
'''
import random

from module import common
from module import summoning
from module import enums
from module import task
from module import achievement


SEG_COUNT_W = 30
SEG_COUNT_R = 25


async def try_unlock_weapon(uid, wid, module=None, **kwargs):
	wnp = wid.name[:2]
	if module is not None and module == 'sum':
		if wnp in RECORD_SUM:
			await RECORD_SUM[wnp](uid, **kwargs)
	if await common.get_weapon(uid, wid, key='star', **kwargs) == 0:
		await common.set_weapon(uid, wid, val=1, key='star', **kwargs)
		if wnp in RECORD_GET:
			await RECORD_GET[wnp](uid, **kwargs)
		seg = await common.get_weapon(uid, wid, **kwargs)
		return True, seg
	else:
		seg = await common.try_weapon(uid, wid, val=SEG_COUNT_W, **kwargs)
		return False, seg


async def try_unlock_role(uid, rid, module=None, **kwargs):
	rnp = rid.name[:2]
	if module is not None and module == 'sum':
		if rnp in RECORD_SUM:
			await RECORD_SUM[rnp](uid, **kwargs)
	if await common.get_role(uid, rid, key='star', **kwargs) == 0:
		await common.set_role(uid, rid, val=1, key='star', **kwargs)
		if rnp in RECORD_GET: await RECORD_GET[rnp](uid, **kwargs)
		seg = await common.get_role(uid, rid, **kwargs)
		return True, seg
	else:
		seg = await common.try_role(uid, rid, val=SEG_COUNT_R, **kwargs)
		return False, seg


async def try_unlock_skill(uid, sid, **kwargs):
	if not await common.exists('skill', ('uid', uid), ('sid', sid), **kwargs):
		await common.execute(f'INSERT INTO skill(uid, sid) VALUES ("{uid}", {sid});', **kwargs)
		return True, 1
	await common.execute(f'INSERT INTO item (uid, iid, value) VALUES ("{uid}", {enums.Item.SKILL_SCROLL_10}, 1) ON DUPLICATE KEY UPDATE value = value + 1;', **kwargs)
	return False, enums.Item.SKILL_SCROLL_10


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
