'''
skill.py

CHECKED WITH LIANG
'''

import random

from module import enums
from module import common


async def get_skill(uid, sid, **kwargs):
	# 0 - success
	skill = enums.Skill(sid)
	level = await common.execute(f'SELECT level FROM skill WHERE uid = "{uid}" AND sid = {skill.value};', **kwargs)
	return common.mt(0, 'success', {'sid' : skill.value, 'level' : level[0][0]}) if level != () else common.mt(1, 'invalid skill name')

async def level_up(uid, sid, iid, **kwargs):
	"""
	0 - success
	1 - unlucky
	96 - skill not yet unlocked
	97 - invalid scroll id
	98 - insufficient materials
	99 - already max level
	"""
	skill_scroll_id = kwargs['skill']['skill_scroll_id']
	level = await get_skill(uid, sid, **kwargs)
	if level['status'] != 0: return common.mt(96, 'skill not yet unlocked')
	elif level['data']['level'] >= 10: return common.mt(99, 'already max level')
	if str(iid) not in skill_scroll_id: return common.mt(97, 'invalid scroll id')
	can_pay, remaining = await common.try_item(uid, enums.Item(iid), -1, **kwargs)
	if not can_pay: return common.mt(98, 'insufficient materials')
	if not _roll_for_upgrade(iid, **kwargs): return common.mt(1, 'unlucky', {'sid': sid, 'level': level['data']['level'], 'iid': iid, 'value': remaining})
	await common.execute(f'UPDATE skill SET level = level + 1 WHERE uid = "{uid}" AND sid = {sid};', **kwargs)
	return common.mt(0, 'success', {'sid': sid, 'level': level['data']['level'] + 1, 'iid': iid, 'value': remaining})

async def get_all_levels(uid, **kwargs):
	# 0 - success
	skills = await common.execute(f'SELECT sid, level FROM skill WHERE uid = "{uid}";', **kwargs)
	return common.mt(0, 'success', {'skills' : [{'sid' : s[0], 'level' : s[1]} for s in skills]})

######################################################################################################

def _roll_for_upgrade(iid, **kwargs):
	upgrade_chance = kwargs['skill']['upgrade_chance']
	return random.random() < upgrade_chance[str(iid)]
