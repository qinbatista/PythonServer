'''
skill.py
'''

import random

from module import enums
from module import common

S = \
{
	enums.Item.SKILL_SCROLL_10 : 0.10,
	enums.Item.SKILL_SCROLL_30 : 0.30,
	enums.Item.SKILL_SCROLL_100 : 1
}

async def get_skill(uid, sid, **kwargs):
	skill = enums.Skill(sid)
	level = await common.execute(f'SELECT level FROM skill WHERE uid = "{uid}" AND sid = {skill.value};', **kwargs)
	return common.mt(0, 'success', {'remaining' : { skill.value : level[0][0] }}) if level != () else common.mt(1, 'invalid skill name')

async def level_up(uid, sid, iid, **kwargs):
	level = await get_skill(uid, sid, **kwargs)
	if level['status'] != 0: return common.mt(96, 'skill not yet unlocked')
	elif level['data']['remaining'][sid] >= 10: return common.mt(99, 'already max level')
	if enums.Item(iid) not in S: return common.mt(97, 'invalid scroll id')
	can_pay, remaining = await common.try_item(uid, enums.Item(iid), -1, **kwargs)
	if not can_pay: return common.mt(98, 'insufficient materials')
	if not _roll_for_upgrade(enums.Item(iid)): return common.mt(1, 'unlucky', {'remaining' : { sid : level['data']['remaining'][sid], iid : remaining}})
	await common.execute(f'UPDATE skill SET level = level + 1 WHERE uid = "{uid}" AND sid = {sid};', **kwargs)
	return common.mt(0, 'upgrade success', {'remaining' : { sid : level['data']['remaining'][sid] + 1, iid : remaining}})

async def get_all_levels(uid, **kwargs):
	skills = await common.execute(f'SELECT sid, level FROM skill WHERE uid = "{uid}";', **kwargs)
	return common.mt(0, 'success', {'remaining' : {s[0] : s[1] for s in skills}})

######################################################################################################

def _roll_for_upgrade(iid):
	return random.random() < S[enums.Item(iid)]
