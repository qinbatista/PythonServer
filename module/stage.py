'''
stage.py
'''

from module import enums
from module import common


# 进入普通关卡的方法
async def enter_stage(uid, stage, **kwargs):
	entry_consume = kwargs['entry_consume']  # self._entry_consumables["stage"]
	enemy_layouts = kwargs['enemy_layouts']  # self._level_enemy_layouts['enemyLayouts']
	enemy_layout = enemy_layouts[-1]['enemyLayout'] if stage > len(enemy_layouts) else enemy_layouts[stage - 1]['enemyLayout']

	can_s, stage_s = await get_progress(uid, 'stage', **kwargs)
	if not can_s or stage <= 0 or stage > stage_s + 1:
		return common.mt(99, 'Parameter error')
	_, exp = await get_progress(uid, 'exp', **kwargs)

	stages = [int(x) for x in entry_consume.keys() if x.isdigit()]
	if stage not in stages: stage = max(stages)

	stage = str(stage)
	iid_s = list(entry_consume[stage].keys())
	values = [-1 * int(v) for v in list(entry_consume[stage].values())]

	for i, iid in enumerate(iid_s):
		data = await common.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = "{iid}" FOR UPDATE;', **kwargs)
		values[i] += data[0][0]
		if values[i] < 0: return common.mt(98, f'{iid} insufficient')
	# try_energy 扣体力看是否足够
	# if energy_data["status"] >= 97:
	# 	return common.mt(status=97, message="Insufficient energy")

	# 根据消耗体力来增加用户经验，10*energy
	exp += 10 * 2  # 这里模拟消耗两点体力
	_, _ = await common.execute(f'UPDATE progress set exp = {exp} WHERE uid = "{uid}";', **kwargs)

	enter_stages = []
	for i, iid in enumerate(iid_s):
		_, data = await common.execute_update(f'UPDATE item set value = {values[i]} WHERE uid = "{uid}" AND iid = "{iid}";', **kwargs)
		enter_stages.append({'iid': iid, 'value': data[0][0], 'consume': entry_consume[stage][iid]})

	return common.mt(0, 'success', {'enter_stages': enter_stages, 'exp_info': await increase_exp(uid, 0, **kwargs), 'enemy_layout': enemy_layout})


############################################ 私有方法 ############################################


async def get_progress(uid, pid, **kwargs):
	pdata = await common.execute(f'SELECT {pid} FROM progress WHERE uid = "{uid}";', **kwargs)
	return (True, pdata[0][0]) if pdata != () else (False, 0)


async def increase_exp(uid, exp, **kwargs):
	"""
	exp:Need to increase the experience value
	exp = exp_increase
	exp_s:Exp data in the server
	exp_s = exp_server
	exp_config:Level configuration information
	exp_config = self._player['player_level']['experience']
	"""
	exp_config = kwargs['exp_config']  # self._player['player_level']['experience']
	exp_data = await common.execute(f'SELECT exp FROM progress WHERE uid = "{uid}";', **kwargs)
	if exp_data == (): return False, {'exp': 0, 'level': 0, 'need': 0}
	exp_s = exp_data[0][0]
	exp_list = [e for e in exp_config if e > exp_s]
	if exp == 0: return True, {'exp': exp_s, 'level': exp_config.index(exp_list[0]) if exp_list != [] else len(exp_config), 'need': exp_list[0] - exp_s if exp_list != [] else 0}
	exp_s += exp
	_, exp_s = await common.execute_update(f'UPDATE progress SET exp = {exp_s} WHERE uid = "{uid}";', **kwargs)
	return True, {'exp': exp_s, 'level': exp_config.index(exp_list[0]) if exp_list != [] else len(exp_config), 'need': exp_list[0] - exp_s if exp_list != [] else 0}
