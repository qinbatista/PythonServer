'''
stage.py
'''

from module import enums
from module import common
import random


# 进入普通关卡
async def enter_stage(uid, stage, **kwargs):
	# 0 - success
	# 97 - Insufficient energy
	# 98 - key insufficient
	# 99 - parameter error
	enter_stages = []
	energy_consume = 2  # 虚拟消耗能量为2
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
	energy_data = await common.try_energy(uid, -1 * energy_consume, **kwargs)
	if energy_data["status"] >= 97:
		return common.mt(97, "Insufficient energy")

	# 根据消耗体力来增加用户经验，10*energy
	exp += 10 * energy_consume  # 这里模拟消耗energy_consume点体力
	await common.execute(f'UPDATE progress set exp = {exp} WHERE uid = "{uid}";', **kwargs)

	for i, iid in enumerate(iid_s):
		await common.execute_update(f'UPDATE item set value = {values[i]} WHERE uid = "{uid}" AND iid = "{iid}";', **kwargs)
		data = await common.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = "{iid}";', **kwargs)
		enter_stages.append({'iid': iid, 'value': data[0][0], 'consume': entry_consume[stage][iid]})

	_, exp_info = await increase_exp(uid, 0, **kwargs)
	return common.mt(0, 'success', {'enter_stages': enter_stages, 'exp_info': exp_info, 'enemy_layout': enemy_layout, 'energy_data': energy_data['data']})


# 通过普通关卡
async def pass_stage(uid, stage, **kwargs):
	# success ===> 0
	# 0 : success
	# 99 : Parameter error
	# print(f'stage:{stage}, type:{type(stage)}')
	can_s, stage_s = await get_progress(uid, 'stage', **kwargs)
	if not can_s or stage <= 0 or stage_s + 1 < stage:
		return common.mt(99, 'Parameter error')

	pass_stages = []
	pass_rewards = kwargs['pass_rewards']  # self._stage_reward["stage"]
	stages = [int(x) for x in pass_rewards.keys() if str.isdigit(x)]
	pass_reward = pass_rewards[str(max(stages))] if stage not in stages else pass_rewards[str(stage)]

	p_exp = {'remaining': -1, 'reward': -1}
	for key, value in pass_reward.items():
		if key == 'exp':
			await common.execute_update(f'UPDATE progress SET exp = exp + {value} WHERE uid = "{uid}";', **kwargs)
			exp_data = await common.execute(f'SELECT exp FROM progress WHERE uid = "{uid}";', **kwargs)
			p_exp['remaining'] = exp_data[0][0]
			p_exp['reward'] = value
		else:
			await common.execute_update(f'UPDATE item SET value = value + {value} WHERE uid = "{uid}" AND iid = "{key}";', **kwargs)
			data = await common.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = "{key}";', **kwargs)
			pass_stages.append({'iid': key, 'remaining': data[0][0], 'reward': value})

	p_stage = {'finally': stage_s, 'vary': 0}
	if stage_s + 1 == stage:  # 通过新关卡
		await common.execute_update(f'UPDATE progress SET stage = {stage} WHERE uid = "{uid}"', **kwargs)
		p_stage['finally'] = stage
		p_stage['vary'] = 1
	return common.mt(0, 'success', data={'pass_stages': pass_stages, 'p_exp': p_exp, 'p_stage': p_stage})


# 进入闯塔关卡
async def enter_tower(uid, stage, **kwargs):
	# 0 - success
	# 97 - Insufficient energy
	# 98 - key insufficient
	# 99 - parameter error
	enter_towers = []
	energy_consume = 2  # 虚拟消耗能量为2
	entry_consume = kwargs['entry_consume']  # self._entry_consumables["tower"]

	can_s, stage_s = await get_progress(uid, 'towerstage', **kwargs)
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
	energy_data = await common.try_energy(uid, -1 * energy_consume, **kwargs)
	if energy_data["status"] >= 97:
		return common.mt(97, "Insufficient energy")

	# 根据消耗体力来增加用户经验，10*energy
	exp += 10 * energy_consume  # 这里模拟消耗energy_consume点体力
	await common.execute(f'UPDATE progress set exp = {exp} WHERE uid = "{uid}";', **kwargs)

	for i, iid in enumerate(iid_s):
		await common.execute_update(f'UPDATE item set value = {values[i]} WHERE uid = "{uid}" AND iid = "{iid}";', **kwargs)
		data = await common.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = "{iid}";', **kwargs)
		enter_towers.append({'iid': iid, 'value': data[0][0], 'consume': entry_consume[stage][iid]})

	_, exp_info = await increase_exp(uid, 0, **kwargs)
	return common.mt(0, 'success', {'enter_towers': enter_towers, 'exp_info': exp_info, 'energy_data': energy_data['data']})


# 通过闯塔关卡
async def pass_tower(uid, stage, **kwargs):
	# success ===> 0
	# 0 : success
	# 99 : Parameter error
	# print(f'stage:{stage}, type:{type(stage)}')
	can_s, stage_s = await get_progress(uid, 'towerstage', **kwargs)
	if not can_s or stage <= 0 or stage_s + 1 < stage:
		return common.mt(99, 'Parameter error')

	p_stage = {'finally': stage_s, 'vary': 0}
	if stage_s + 1 == stage:  # 通过新关卡
		await common.execute_update(f'UPDATE progress SET stage = {stage} WHERE uid = "{uid}"', **kwargs)
		p_stage['finally'] = stage
		p_stage['vary'] = 1

	pass_towers = []
	pass_rewards = kwargs['pass_rewards']  # self._stage_reward["tower"]
	stages = [int(x) for x in pass_rewards.keys() if str.isdigit(x)]
	pass_reward = pass_rewards[str(max(stages))] if stage not in stages else pass_rewards[str(stage)]

	if stage % 10 == 0:
		reward = random.choices(population=pass_reward)[0]
		if reward in pass_rewards['skill']:
			skill_mpg = pass_rewards['skill_MPG']
			if 'skill_M' in reward:
				sid = skill_mpg['M'] + int(reward.replace('skill_M', ''))
			elif 'skill_P' in reward:
				sid = skill_mpg['P'] + int(reward.replace('skill_P', ''))
			else:
				sid = skill_mpg['G'] + int(reward.replace('skill_G', ''))
			if await try_unlock_skill(uid, sid, **kwargs):
				return common.mt(1, 'Successfully unlock new skills', {'pass_tower': [{'reward_kind': 'skill', 'sid': sid, 'level': 1, 'p_stage': p_stage}]})
			else:
				scroll_iid = random.choices(population=pass_rewards["skill_scroll"], weights=pass_rewards["weights"])[0]
				_, scroll_value = await common.try_item(uid, enums.Item(scroll_iid), 1, **kwargs)
				return common.mt(2, 'Get a scroll', {'pass_tower': [{'reward_kind': 'scroll', 'iid': scroll_iid, 'value': scroll_value, 'reward': 1, 'p_stage': p_stage}]})
		elif reward in pass_rewards['weapon']:  # weapon
			wid = int(reward.replace('weapon', ''))
			segment_range = pass_rewards['segment_range']
			segment = random.randint(segment_range[0], segment_range[1]) if len(segment_range) == 2 else segment_range[0]
			weapon_data = await increase_weapon_segment(uid, wid, segment, **kwargs)
			return common.mt(3, 'Get weapon segment', {'pass_tower': [{'reward_kind': 'weapon', 'wid': wid, 'segment': weapon_data[0][0], 'reward': segment, 'p_stage': p_stage}]})
		else:
			scroll_range = pass_rewards['scroll_range']
			scroll_iid = random.choices(population=pass_rewards["skill_scroll"], weights=pass_rewards["weights"])[0]
			_, scroll_value = await common.try_item(uid, enums.Item(scroll_iid), scroll_range, **kwargs)
			return common.mt(4, 'Get scroll', {'pass_tower': [{'reward_kind': 'scroll', 'iid': scroll_iid, 'value': scroll_value, 'reward': scroll_range, 'p_stage': p_stage}]})
	else:
		p_exp = {'remaining': -1, 'reward': -1}
		for key, value in pass_reward.items():
			if key == 'exp':
				await common.execute_update(f'UPDATE progress SET exp = exp + {value} WHERE uid = "{uid}";', **kwargs)
				exp_data = await common.execute(f'SELECT exp FROM progress WHERE uid = "{uid}";', **kwargs)
				p_exp['remaining'] = exp_data[0][0]
				p_exp['reward'] = value
			else:
				await common.execute_update(f'UPDATE item SET value = value + {value} WHERE uid = "{uid}" AND iid = "{key}";', **kwargs)
				data = await common.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = "{key}";', **kwargs)
				pass_towers.append({'iid': key, 'remaining': data[0][0], 'reward': value})

	return common.mt(0, 'success', data={'pass_stages': pass_towers, 'p_exp': p_exp, 'p_stage': p_stage})

############################################ 私有方法 ############################################


async def try_unlock_skill(uid, sid, **kwargs):
	# success ===> 0 and 1
	# True - success unlocked new skill
	# False - skill already unlocked
	skill = await common.execute(f'SELECT level FROM skill WHERE uid = "{uid}";', **kwargs)
	if skill == ():
		await common.execute_update(f'INSERT INTO skill (uid, sid, value) VALUES ("{uid}", "{sid}", 1);', **kwargs)
		return True
	elif skill[0][0] == 0:
		await common.execute_update(f'UPDATE skill SET level = 1 WHERE uid = "{uid}" AND sid = "{sid};"', **kwargs)
		return True
	return False


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
	await common.execute_update(f'UPDATE progress SET exp = {exp_s} WHERE uid = "{uid}";', **kwargs)
	return True, {'exp': exp_s, 'level': exp_config.index(exp_list[0]) if exp_list != [] else len(exp_config), 'need': exp_list[0] - exp_s if exp_list != [] else 0}


async def increase_weapon_segment(uid, wid, segment, **kwargs):
	data = await common.execute(f'SELECT segment FROM weapon WHERE uid = "{uid}" AND wid = "{wid}";', **kwargs)
	if data == ():
		await common.execute_update(f'INSERT INTO weapon (uid, wid, segment) VALUES ("{uid}", "{wid}", "{segment}");', **kwargs)
	else:
		await common.execute_update(f'UPDATE weapon SET segment = segment + {segment} WHERE uid = "{uid}" AND wid = "{wid}";', **kwargs)
	data = await common.execute(f'SELECT segment FROM weapon WHERE uid = "{uid}" AND wid = "{wid}";', **kwargs)
	return data


async def increase_role_segment(uid, rid, segment, **kwargs):
	data = await common.execute(f'SELECT segment FROM role WHERE uid = "{uid}" AND wid = "{rid}";', **kwargs)
	if data == ():
		await common.execute_update(f'INSERT INTO role (uid, rid, segment) VALUES ("{uid}", "{rid}", "{segment}");', **kwargs)
	else:
		await common.execute_update(f'UPDATE role SET segment = segment + {segment} WHERE uid = "{uid}" AND wid = "{rid}";', **kwargs)
	data = await common.execute(f'SELECT segment FROM weapon WHERE uid = "{uid}" AND wid = "{wid}";', **kwargs)
	return data
