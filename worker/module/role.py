'''
role.py
'''

from module import enums
from module import common
from module import task
from module import lottery
from module import achievement
from collections import defaultdict


async def level_up(uid, rid, delta, **kwargs):
	rid = enums.Role(rid)
	exists, payload = await _get_role_info(uid, rid, 'star', 'level', **kwargs)
	if not exists: return common.mt(99, 'invalid target')
	star, level = payload
	if star == 0: return common.mt(96, "You don't have the role")
	if delta <= 0: return common.mt(98, 'The delta must be a positive integer')
	max_lv = kwargs['config']['role']['standard_costs']['upgrade_lv']['max']
	if max_lv <= level: return common.mt(95, 'max lv')
	delta = delta if delta + level <= max_lv else (max_lv - level)
	sums = sum([(50+50*max(1, int(lv/20)))*max(1, int(lv-9)) for lv in range(level, level + delta)])
	items = f'{enums.Group.ITEM}:{enums.Item.EXP_POINT}:{sums},{enums.Group.ITEM}:{enums.Item.COIN}:{sums}'
	can_pay, results = await common.consume_items(uid, items, **kwargs)
	if not can_pay: return common.mt(97, 'can not pay for upgrade')
	rm = [{'iid': r[1], 'value': r[2]} for r in results]
	rw = [{'iid': r[1], 'value': r[3]} for r in results]
	await task.record(uid, enums.Task.ROLE_LEVEL_UP, **kwargs)
	await achievement.record(uid, enums.Achievement.LV_UPR, **kwargs)
	await common.execute(f'UPDATE role SET level = {level + delta} WHERE uid = "{uid}" AND rid = {rid.value}', **kwargs)
	return common.mt(0, 'success', {'remaining': {enums.Group.ROLE: {'rid': rid, 'level' : level + delta},
													enums.Group.ITEM: rm},
										'reward': {enums.Group.ROLE: {'rid': rid, 'level' : delta},
													enums.Group.ITEM: rw}})


async def level_up_star(uid, rid, **kwargs):
	rid = enums.Role(rid)
	exists, payload = await _get_role_info(uid, rid, 'star', 'segment', **kwargs)
	if not exists: return common.mt(99, 'invalid target')
	star, segment = payload
	if star >= 10: return common.mt(97, 'max star')
	cost = kwargs['config']['role']['standard_costs']['seg'] * (1 + star)
	if segment < cost: return common.mt(98, 'insufficient segments')
	await common.execute(f'UPDATE role SET star = {star + 1}, segment = {segment - cost} WHERE uid = "{uid}" AND rid = {rid};', **kwargs)
	# H 加成就代码
	if star == 0:
		rnp = rid.name[:2]
		if rnp in lottery.RECORD_GET:
			await lottery.RECORD_GET[rnp](uid, **kwargs)
	return common.mt(0, 'success', {'remaining': {'rid' : rid, 'star' : star + 1, 'seg' : segment - cost}, 'reward': {'rid' : rid, 'star' : 1, 'seg' : cost}})


async def unlock_passive(uid, rid, pid, **kwargs):
	"""解锁被动技能"""
	if rid not in enums.Role._value2member_map_: return common.mt(99, 'Role id error')
	if pid not in enums.RolePassive._value2member_map_ or pid//100 != 1: return common.mt(98, 'Passive skill id error')
	rid, pid = enums.Role(rid), enums.RolePassive(pid)
	exists, payload = await _get_role_info(uid, rid, 'star', 'level', **kwargs)
	if not exists: return common.mt(97, 'invalid target')
	star, level = payload
	if star == 0: return common.mt(96, "You don't have the role")
	cfg = kwargs['config']['role']['standard_costs']['unlock_ps']
	iid = enums.Item(cfg['cty'])
	lv, qty = cfg['consume'][f'{pid}']['lv'], cfg['consume'][f'{pid}']['qty']
	if lv >= level: return common.mt(95, 'Your role level has not reached the unlock level')
	ps = await _get_ps(uid, rid, pid, **kwargs)
	if ps: return common.mt(94, 'This passive is unlocked', await _get_all_role_passives(uid, **kwargs))
	can, _qty = await common.try_item(uid, iid, -qty, **kwargs)
	if not can: return common.mt(93, 'insufficient materials')
	await _update_ps_lv(uid, rid, pid, 1, **kwargs)
	return common.mt(0, 'success', {'rid': rid, 'pid': pid, 'consume': f'{enums.Group.ITEM}:{iid}:{_qty}:{qty}'})


# async def get_all(uid, **kwargs):
# 	return common.mt(0, 'success', {'roles' : await _get_all_role_info(uid, **kwargs),"config":{'seg' : kwargs['config']['role']['standard_costs']['seg'], 'exp_pot' : kwargs['config']['role']['standard_costs']['upgrade_lv']['exp_pot']}})
async def get_all(uid, **kwargs):
	roles = await _get_all_role_info(uid, **kwargs)
	passives = await _get_all_role_passives(uid, **kwargs)
	for role in roles:
		for pid in enums.RolePassive:
			try:
				role[f'p{pid}'] = passives[role['rid']][pid.value]
			except KeyError:
				role[f'p{pid}'] = 0
	return common.mt(0, 'success', {'roles' : roles})


async def get_config(**kwargs):
	return common.mt(0, 'success', kwargs['config']['role'])

#################################################################################


async def _update_ps_lv(uid, rid, pid, lv, **kwargs):
	await common.execute(f'INSERT INTO rolepassive(uid, rid, pid, level) VALUES ("{uid}", {rid}, {pid}, {lv}) ON DUPLICATE KEY UPDATE level = {lv};', **kwargs)


async def _get_ps(uid, rid, pid, **kwargs):
	ps = await common.execute(f'SELECT level FROM rolepassive WHERE uid = "{uid}" AND rid = {rid} AND pid = {pid};', **kwargs)
	return False if ps == () else bool(ps[0][0] == 1)


async def _get_role_info(uid, rid, *args, **kwargs):
	data = await common.execute(f'SELECT {",".join(args)} FROM role WHERE uid = "{uid}" AND rid = {rid}', **kwargs)
	return (True, data[0]) if data != () else (False, ())


async def _get_all_role_info(uid, **kwargs):
	data = await common.execute(f'SELECT rid, star, level, segment FROM role WHERE uid = "{uid}";', **kwargs)
	return [{'rid' : r[0], 'star' : r[1], 'level' : r[2], 'seg' : r[3]} for r in data]


async def _get_all_role_passives(uid, **kwargs):
	data = await common.execute(f'SELECT rid, pid, level FROM rolepassive WHERE uid = "{uid}";', **kwargs)
	passives = defaultdict(dict)
	for rid, pid, level in data:
		passives[rid][pid] = level
	return passives
