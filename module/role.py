'''
role.py
'''

from module import enums
from module import common

from collections import defaultdict


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
