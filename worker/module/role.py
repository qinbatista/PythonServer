'''
role.py
'''

from module import enums
from module import common
from module import task
from module import achievement
from collections import defaultdict


async def level_up(uid, rid, delta, **kwargs):
	kwargs.update({"task_id": enums.Task.ROLE_LEVEL_UP})
	await task.record_task(uid,**kwargs)

	kwargs.update({"aid":enums.Achievement.LEVEL_UP_ROLE})
	await achievement.record_achievement(kwargs['data']['unique_id'],**kwargs)

	rid = enums.Role(rid)
	exists, payload = await _get_role_info(uid, rid, 'star', 'level', **kwargs)
	if not exists: return common.mt(99, 'invalid target')
	star, level = payload
	if star == 0: return common.mt(96, "You don't have the role")
	if delta <= 0: return common.mt(98, 'The delta must be a positive integer')
	max_lv = kwargs['config']['role']['standard_costs']['upgrade_lv']['max']
	config = kwargs['config']['role']['standard_costs']['upgrade_lv']['exp_pot']
	if max_lv <= level: return common.mt(95, 'max lv')
	delta = delta if delta + level <= max_lv else (max_lv - level)
	consume = config[level + delta - 1] - config[level - 1]
	can_pay, remain = await common.try_item(uid, enums.Item.EXPERIENCE_POTION, -consume, **kwargs)
	if not can_pay: return common.mt(97, 'can not pay for upgrade')
	await common.execute(f'UPDATE role SET level = {level + delta} WHERE uid = "{uid}" AND rid = {rid.value}', **kwargs)
	return common.mt(0, 'success', {'remaining': {enums.Group.ROLE.value: {'rid': rid.value, 'level' : level + delta},
													enums.Group.ITEM.value: [{'iid': enums.Item.EXPERIENCE_POTION.value, 'value': remain}]},
										'reward': {enums.Group.ROLE.value: {'rid': rid.value, 'level' : delta},
													enums.Group.ITEM.value: [{'iid': enums.Item.EXPERIENCE_POTION.value, 'value': consume}]}})


async def level_up_star(uid, rid, **kwargs):
	rid = enums.Role(rid)
	exists, payload = await _get_role_info(uid, rid, 'star', 'segment', **kwargs)
	if not exists: return common.mt(99, 'invalid target')
	star, segment = payload
	if star >= 10: return common.mt(97, 'max star')
	cost = kwargs['config']['role']['standard_costs']['seg'] * (1 + star)
	if segment < cost: return common.mt(98, 'insufficient segments')
	await common.execute(f'UPDATE role SET star = {star + 1}, segment = {segment - cost} WHERE uid = "{uid}" AND rid = {rid.value};', **kwargs)
	return common.mt(0, 'success', {'remaining': {'rid' : rid.value, 'star' : star + 1, 'seg' : segment - cost}, 'reward': {'rid' : rid.value, 'star' : 1, 'seg' : cost}})


async def unlock_passive(uid, rid, pid, **kwargs):
	"""解锁被动技能"""


async def get_all(uid, **kwargs):
	return common.mt(0, 'success', {'roles' : await _get_all_role_info(uid, **kwargs),"config":{'seg' : kwargs['config']['role']['standard_costs']['seg'], 'exp_pot' : kwargs['config']['role']['standard_costs']['upgrade_lv']['exp_pot']}})


async def get_config(**kwargs):
	return common.mt(0, 'success', kwargs['config']['role'])

#################################################################################

async def _get_role_info(uid, rid, *args, **kwargs):
	data = await common.execute(f'SELECT {",".join(args)} FROM role WHERE uid = "{uid}" AND rid = {rid.value}', **kwargs)
	return (True, data[0]) if data != () else (False, ())

async def _get_all_role_info(uid, **kwargs):
	data = await common.execute(f'SELECT rid, star, level, segment FROM role WHERE uid = "{uid}";', **kwargs)
	return [{'rid' : r[0], 'star' : r[1], 'level' : r[2], 'seg' : r[3]} for r in data]

# unused right now
async def _get_all_role_passives(uid, **kwargs):
	data = await common.execute(f'SELECT rid, pid, level FROM rolepassive WHERE uid = "{uid}";', **kwargs)
	passives = defaultdict(dict)
	for rid, pid, level in data:
		passives[rid][pid] = level
	return passives
