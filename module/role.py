'''
role.py
'''

from module import enums
from module import common

from collections import defaultdict

STANDARD_EXP_POT_COUNT = 5

# invalid role name, user does not have that role, max level
async def level_up(uid, rid, amount, **kwargs):
	rid = enums.Role(rid)
	exists, payload = await _get_role_info(uid, rid, 'star', 'level', 'skillpoint', **kwargs)
	if not exists: return common.mt(99, 'invalid target')
	star, level, sp = payload
	upgrade_cnt = min(amount // STANDARD_EXP_POT_COUNT, 100 - level)
	if upgrade_cnt == 0: return common.mt(98, 'too few incoming materials or max level')
	can_pay, remaining = await common.try_item(uid, enums.Item.EXPERIENCE_POTION, -upgrade_cnt * STANDARD_EXP_POT_COUNT, **kwargs)
	if not can_pay: return common.mt(97, 'can not pay for upgrade')
	await common.execute(f'UPDATE role SET level = {level + upgrade_cnt}, skillpoint = {sp + upgrade_cnt} WHERE uid = "{uid}" AND rid = {rid.value}', **kwargs)
	return common.mt(0, 'success', {enums.Group.ROLE.value : {'rid' : rid.value, 'level' : level + upgrade_cnt, 'sp' : sp + upgrade_cnt}, enums.Group.ITEM.value : {'iid' : enums.Item.EXPERIENCE_POTION.value, 'value' : remaining}})

# invalid role name, insufficient segment, skill has been reset
async def level_up_star():
	pass

async def get_all(uid, **kwargs):
	roles = await _get_all_role_info(uid, **kwargs)
	passives = await _get_all_role_passives(uid, **kwargs)
	for role in roles:
		for pid in enums.RolePassive:
			try:
				role[f'p{str(pid.value)}'] = passives[role['rid']][pid.value]
			except KeyError:
				role[f'p{str(pid.value)}'] = 0 
	return common.mt(0, 'success', {'roles' : roles})

#################################################################################

async def _get_role_info(uid, rid, *args, **kwargs):
	data = await common.execute(f'SELECT {",".join(args)} FROM role WHERE uid = "{uid}" AND rid = {rid.value}', **kwargs)
	return (True, data[0]) if data != () else (False, ())

async def _get_all_role_info(uid, **kwargs):
	data = await common.execute(f'SELECT rid, star, level, skillpoint, segment FROM role WHERE uid = "{uid}";', **kwargs)
	return [{'rid' : r[0], 'star' : r[1], 'level' : r[2], 'sp' : r[3], 'seg' : r[4]} for r in data]

async def _get_all_role_passives(uid, **kwargs):
	data = await common.execute(f'SELECT rid, pid, level FROM rolepassive WHERE uid = "{uid}";', **kwargs)
	passives = defaultdict(dict)
	for rid, pid, level in data:
		passives[rid][pid] = level
	return passives
