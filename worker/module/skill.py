'''
skill.py

CHECKED WITH LIANG
'''

import random

from module import enums
from module import common
# FIB = [1]  # 第一次升级需要消耗2个卷轴
FIB = [1, 1]  # 第一次升级需要消耗1个卷轴


async def level_up(uid, sid, iid, **kwargs):
	"""
	0 - success
	1 - unlucky
	96 - skill not yet unlocked
	97 - invalid scroll id
	98 - insufficient materials
	99 - already max level
	"""
	cfg = kwargs['config']['skill']['common']['upgrade']
	level = await _get_skill(uid, sid, **kwargs)
	if level['status'] != 0: return common.mt(96, 'skill not yet unlocked')
	level = level['data']['level'] + 1
	if level > 10: return common.mt(99, 'already max level')
	if str(iid) not in cfg: return common.mt(97, 'invalid scroll id')
	qty = cache_fib(level)
	can_pay, _qty = await common.try_item(uid, enums.Item(iid), -qty, **kwargs)
	if not can_pay: return common.mt(98, 'insufficient materials')
	gid = enums.Group.ITEM
	data = {'remain': [f'{gid}:{iid}:{_qty}'], 'reward': [f'{gid}:{iid}:{qty}']}
	gid = enums.Group.SKILL
	if not _roll_for_upgrade(iid, cfg):
		data['remain'].append(f'{gid}:{sid}:{level-1}')
		data['reward'].append(f'{gid}:{sid}:0')
		return common.mt(1, 'unlucky', data)
	data['remain'].append(f'{gid}:{sid}:{level}')
	data['reward'].append(f'{gid}:{sid}:1')
	await common.execute(f'UPDATE skill SET level = level + 1 WHERE uid = "{uid}" AND sid = {sid};', **kwargs)
	return common.mt(0, 'success', data)


async def get_all(uid, **kwargs):
	# 0 - success
	skills = await common.execute(f'SELECT sid, level FROM skill WHERE uid = "{uid}";', **kwargs)
	return common.mt(0, 'success', {'skills' : [{'sid' : s[0], 'level' : s[1]} for s in skills]})


async def config(**kwargs):
	return common.mt(0, 'success', {'config': kwargs['config']['skill']})


######################################################################################################


async def _get_skill(uid, sid, **kwargs):
	# 0 - success
	level = await common.execute(f'SELECT level FROM skill WHERE uid = "{uid}" AND sid = {sid};', **kwargs)
	return common.mt(0, 'success', {'sid' : sid, 'level' : level[0][0]}) if level != () else common.mt(1, 'invalid skill name')


def _roll_for_upgrade(iid, upgrade_chance):
	return random.random() < upgrade_chance[f'{iid}']


def fib(lv):
	"""1 1 2 3 5 8 13 21 34 55"""
	if len(FIB) >= lv: return FIB[lv - 1]
	return lv if lv < 2 else (fib(lv - 1) + fib(lv - 2))


def cache_fib(lv):
	fl = len(FIB)
	if fl < lv:
		for i in range(fl + 1, lv + 1):
			FIB.append(fib(i))
	return FIB[lv - 1]
