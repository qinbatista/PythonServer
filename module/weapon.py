'''
weapon.py

CHECKED WITH LIANG
'''

import asyncio

from module import enums
from module import common

from collections import defaultdict
from module import task

STANDARD_IRON = 40
STANDARD_RESET = 100
STANDARD_SEGMENT = 25

async def get_config(**kwargs):
	return common.mt(0, 'success', {'seg' : STANDARD_SEGMENT, 'reset' : STANDARD_RESET, 'cost' : STANDARD_IRON})

async def level_up(uid, wid, amount, **kwargs):
	wid = enums.Weapon(wid)
	exists, payload = await _get_weapon_info(uid, wid, 'star', 'level', 'skillpoint', **kwargs)
	if not exists: return common.mt(99, 'invalid target')
	star, level, sp = payload
	upgrade_cnt = min(amount // STANDARD_IRON, 100 - level)
	if upgrade_cnt == 0: return common.mt(98, 'too few incoming materials')
	can_pay, remaining = await common.try_item(uid, enums.Item.IRON, -upgrade_cnt * STANDARD_IRON, **kwargs)
	if not can_pay: return common.mt(97, 'can not pay for upgrade')
	kwargs.update({"tid":enums.Task.ROLE_LEVEL_UP,"task_value":1})
	await task.record_task(uid,**kwargs)
	await common.execute(f'UPDATE weapon SET level = {level + upgrade_cnt}, skillpoint = {sp + upgrade_cnt} WHERE uid = "{uid}" AND wid = {wid.value}', **kwargs)
	return common.mt(0, 'success', {'remaining' : {enums.Group.WEAPON.value : {'wid' : wid.value, \
			'level' : level + upgrade_cnt, 'sp' : sp + upgrade_cnt}, enums.Group.ITEM.value : \
			{'iid' : enums.Item.IRON.value, 'value' : remaining}}, 'reward' : {enums.Group.WEAPON.value : \
			{'wid' : wid.value, 'level' : level, 'sp' : sp}, enums.Group.ITEM.value : \
			{'iid' : enums.Item.IRON.value, 'value' : upgrade_cnt * STANDARD_IRON}}})

async def level_up_passive(uid, wid, pid, **kwargs):
	wid, pid = enums.Weapon(wid), enums.WeaponPassive(pid)
	exists, payload = await _get_weapon_info(uid, wid, 'skillpoint', **kwargs)
	if not exists or payload[0] <= 0: return common.mt(99, 'insufficient materials')
	level = await _increase_passive_level(uid, wid, pid, **kwargs)
	return common.mt(0, 'success', {'wid' : wid.value, 'pid' : pid.value, 'level' : level, 'sp' : payload[0] - 1})

async def level_up_star(uid, wid, **kwargs):
	wid = enums.Weapon(wid)
	exists, payload = await _get_weapon_info(uid, wid, 'star', 'segment', **kwargs)
	if not exists: return common.mt(99, 'invalid target')
	star, segment = payload
	cost = STANDARD_SEGMENT * (1 + star)
	if segment < cost: return common.mt(98, 'insufficient segments')
	await common.execute(f'UPDATE weapon SET star = {star + 1}, segment = {segment - cost} WHERE uid = "{uid}" AND wid = {wid.value};', **kwargs)
	return common.mt(0, 'success', {'wid' : wid.value, 'star' : star + 1, 'seg' : segment - cost})

async def reset_skill_point(uid, wid, **kwargs):
	wid = enums.Weapon(wid)
	exists, payload = await _get_weapon_info(uid, wid, 'skillpoint', **kwargs)
	if not exists: return common.mt(99, 'invalid target')
	can_pay, remaining = await common.try_item(uid, enums.Item.COIN, -STANDARD_RESET, **kwargs)
	if not can_pay: return common.mt(98, 'insufficient coins')
	reclaimed = await _reset_skill_point(uid, wid, **kwargs)
	return common.mt(0, 'success', {enums.Group.WEAPON.value : {'wid' : wid.value, 'sp' : payload[0] + reclaimed}, enums.Group.ITEM.value : {'iid' : enums.Item.COIN.value, 'value' : remaining}})

async def get_all(uid, **kwargs):
	weps = await _get_all_weapon_info(uid, **kwargs)
	passives = await _get_all_weapon_passives(uid, **kwargs)
	for wep in weps:
		for pid in enums.WeaponPassive:
			try:
				wep[f'p{str(pid.value)}'] = passives[wep['wid']][pid.value]
			except KeyError:
				wep[f'p{str(pid.value)}'] = 0
	return common.mt(0, 'success', {'weapons' : weps})




####################################################################################

async def _update_segment(uid, wid, segment, **kwargs):
	await common.execute_update( f'INSERT INTO weapon (uid, wid, segment) VALUES ("{uid}", {wid}, {segment}) ON DUPLICATE KEY UPDATE segment = segment + {segment};', **kwargs)
	data = await common.execute(f'SELECT segment FROM weapon WHERE uid = "{uid}" AND wid = "{wid}"', **kwargs)
	return data[0][0]

async def _get_weapon_info(uid, wid, *args, **kwargs):
	data = await common.execute(f'SELECT {",".join(args)} FROM weapon WHERE uid = "{uid}" AND wid = {wid.value}', **kwargs)
	return (True, data[0]) if data != () else (False, ())

async def _increase_passive_level(uid, wid, pid, **kwargs):
	await asyncio.gather(common.execute(f'UPDATE weapon SET skillpoint = skillpoint - 1 WHERE uid = "{uid}" AND wid = {wid.value};', **kwargs), common.execute(f'INSERT INTO weaponpassive (uid, wid, pid, level) VALUES ("{uid}", {wid.value}, {pid.value}, 1) ON DUPLICATE KEY UPDATE level = level + 1;', **kwargs))
	level = await common.execute(f'SELECT level FROM weaponpassive WHERE uid = "{uid}" AND wid = {wid.value} AND pid = {pid.value};', **kwargs)
	return level[0][0]

async def _reset_skill_point(uid, wid, **kwargs):
	reclaimed = sum(level[0] for level in await common.execute(f'SELECT level FROM weaponpassive WHERE uid = "{uid}" AND wid = {wid.value};', **kwargs))
	await asyncio.gather(common.execute(f'UPDATE weaponpassive SET level = 0 WHERE uid = "{uid}" AND wid = {wid.value};', **kwargs), common.execute(f'UPDATE weapon SET skillpoint = skillpoint + {reclaimed} WHERE uid = "{uid}" AND wid = {wid.value};', **kwargs))
	return reclaimed

async def _get_all_weapon_info(uid, **kwargs):
	data = await common.execute(f'SELECT wid, star, level, skillpoint, segment FROM weapon WHERE uid = "{uid}";', **kwargs)
	return [{'wid' : w[0], 'star' : w[1], 'level' : w[2], 'sp' : w[3], 'seg' : w[4]} for w in data]

async def _get_all_weapon_passives(uid, **kwargs):
	data = await common.execute(f'SELECT wid, pid, level FROM weaponpassive WHERE uid = "{uid}";', **kwargs)
	passives = defaultdict(dict)
	for wid, pid, level in data:
		passives[wid][pid] = level
	return passives



