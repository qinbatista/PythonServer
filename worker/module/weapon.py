'''
weapon.py

CHECKED WITH LIANG
'''

import asyncio

from module import enums
from module import common
from module import task
from module import lottery
from module import achievement

from collections import defaultdict


async def get_config(**kwargs):
	return common.mt(0, 'success', kwargs['config']['weapon'])

async def level_up(uid, wid, delta, **kwargs):
	wst = int(wid//100)
	max_lv = ((wst if wst < 5 else 5) if wst > 2 else 2) * 20 + 20
	wid = enums.Weapon(wid)
	exists, payload = await _get_weapon_info(uid, wid, 'star', 'level', 'skillpoint', **kwargs)
	if not exists: return common.mt(99, 'invalid target')
	star, level, sp = payload
	if star == 0: return common.mt(96, "You don't have the weapon")
	if delta <= 0: return common.mt(98, 'The delta must be a positive integer')
	config = kwargs['config']['weapon']['standard_costs']['upgrade_lv']['iron']
	if max_lv <= level: return common.mt(95, 'max lv')
	delta = delta if delta + level <= max_lv else (max_lv - level)
	consume = config[level + delta - 1] - config[level - 1]
	_, remain_i = await common.try_item(uid, enums.Item.IRON, 0, **kwargs)
	if remain_i < consume: return common.mt(97, 'can not pay for upgrade')
	can_pay, remain_c = await common.try_item(uid, enums.Item.COIN, -consume, **kwargs)
	if not can_pay: return common.mt(97, 'can not pay for upgrade')
	_, remain_i = await common.try_item(uid, enums.Item.IRON, -consume, **kwargs)
	level += delta
	_sp = 1 if level % 10 == 0 else 0
	await common.execute(f'UPDATE weapon SET level = {level}, skillpoint = {sp + _sp} WHERE uid = "{uid}" AND wid = {wid.value}', **kwargs)
	await task.record(uid, enums.Task.WEAPON_LEVEL_UP, **kwargs)
	await achievement.record(uid, enums.Achievement.LV_UPW, **kwargs)
	return common.mt(0, 'success', {'remaining': {enums.Group.WEAPON.value : {'wid' : wid.value, 'level' : level, 'sp' : sp + _sp},
													enums.Group.ITEM.value : [{'iid' : enums.Item.IRON.value, 'value' : remain_i}, {'iid' : enums.Item.COIN.value, 'value' : remain_c}]},
										'reward': {enums.Group.WEAPON.value : {'wid' : wid.value, 'level' : delta, 'sp' : _sp},
													enums.Group.ITEM.value : [{'iid' : enums.Item.IRON.value, 'value' :consume}, {'iid' : enums.Item.COIN.value, 'value' : consume}]}})

async def level_up_passive(uid, wid, pid, **kwargs):
	max_pid = 4 if wid // 100 > 2 else 3
	if pid > max_pid:
		return common.mt(99, 'pid error')
	max_lv = 1 if (max_pid == pid and wid // 100 <= 4) else 3
	wid, pid = enums.Weapon(wid), enums.WeaponPassive(pid)
	exists, payload = await _get_weapon_info(uid, wid, 'skillpoint', **kwargs)
	lv = await _get_passive_level(uid, wid, pid, **kwargs) + 1
	if lv > max_lv:
		return common.mt(99, 'max level')
	if not exists or payload[0] <= 0: return common.mt(99, 'insufficient materials')
	await _set_passive_level(uid, wid, pid, lv, **kwargs)
	return common.mt(0, 'success', {'remaining': {'wid': wid.value, 'pid': pid.value, 'level': lv,
			'sp': payload[0] - 1}, 'reward': {'wid': wid.value, 'pid': pid.value, 'level': 1, 'sp': 1}})

async def level_up_star(uid, wid, **kwargs):
	wid = enums.Weapon(wid)
	exists, payload = await _get_weapon_info(uid, wid, 'star', 'segment', **kwargs)
	if not exists: return common.mt(99, 'invalid target')
	star, segment = payload
	if star >= 10: return common.mt(97, 'max star')
	cost = kwargs['config']['weapon']['standard_costs']['seg'] * (1 + star)
	if segment < cost: return common.mt(98, 'insufficient segments')
	await common.execute(f'UPDATE weapon SET star = {star + 1}, segment = {segment - cost} WHERE \
			uid = "{uid}" AND wid = {wid.value};', **kwargs)
	# TODO 加成就代码
	if star == 0:
		wnp = wid.name[:2]
		if wnp in lottery.RECORD_GET:
			await lottery.RECORD_GET[wnp](uid, **kwargs)
	return common.mt(0, 'success', {'remaining' : {'wid' : wid.value, 'star' : star + 1, \
			'seg' : segment - cost}, 'reward' : {'wid' : wid.value, 'star' : 1, 'seg' : cost}})

async def reset_skill_point(uid, wid, **kwargs):
	wid = enums.Weapon(wid)
	exists, payload = await _get_weapon_info(uid, wid, 'skillpoint', **kwargs)
	if not exists: return common.mt(99, 'invalid target')
	can_pay, remaining = await common.try_item(uid, enums.Item.COIN, \
			-kwargs['config']['weapon']['standard_costs']['reset'], **kwargs)
	if not can_pay: return common.mt(98, 'insufficient coins')
	reclaimed = await _reset_skill_point(uid, wid, **kwargs)
	return common.mt(0, 'success', {'remaining' : {enums.Group.WEAPON.value : {'wid' : wid.value, \
			'sp' : payload[0] + reclaimed}, enums.Group.ITEM.value : {'iid' : enums.Item.COIN.value, \
			'value' : remaining}}, 'reward': {enums.Group.WEAPON.value : {'wid' : wid.value, \
			'sp' : reclaimed}, enums.Group.ITEM.value : {'iid' : enums.Item.COIN.value, \
			'value' : kwargs['config']['weapon']['standard_costs']['reset']}}})

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
	await common.execute( f'INSERT INTO weapon (uid, wid, segment) VALUES ("{uid}", {wid}, {segment}) ON DUPLICATE KEY UPDATE segment = segment + {segment};', **kwargs)
	data = await common.execute(f'SELECT segment FROM weapon WHERE uid = "{uid}" AND wid = "{wid}"', **kwargs)
	return data[0][0]

async def _get_weapon_info(uid, wid, *args, **kwargs):
	data = await common.execute(f'SELECT {",".join(args)} FROM weapon WHERE uid = "{uid}" AND wid = {wid.value}', **kwargs)
	return (True, data[0]) if data != () else (False, ())

async def _get_passive_level(uid, wid, pid, **kwargs):
	lvd = await common.execute(f'SELECT level FROM weaponpassive WHERE uid = "{uid}" AND wid = {wid} AND pid = {pid};', **kwargs)
	return 0 if lvd == () else lvd[0][0]

async def _set_passive_level(uid, wid, pid, level, **kwargs):
	await asyncio.gather(common.execute(f'UPDATE weapon SET skillpoint = skillpoint - 1 WHERE uid = "{uid}" AND wid = {wid};', **kwargs), common.execute(f'INSERT INTO weaponpassive (uid, wid, pid, level) VALUES ("{uid}", {wid}, {pid}, 1) ON DUPLICATE KEY UPDATE level = {level};', **kwargs))

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



