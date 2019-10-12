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
	_, _ = await common.execute(f'UPDATE progress set exp = {exp} WHERE uid = "{uid}";', **kwargs)

	for i, iid in enumerate(iid_s):
		_, data = await common.execute_update(f'UPDATE item set value = {values[i]} WHERE uid = "{uid}" AND iid = "{iid}";', **kwargs)
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
	pass_reward = kwargs['pass_reward']  # self._stage_reward["stage"]
	stages = [int(x) for x in pass_reward.keys() if str.isdigit(x)]
	pass_reward = pass_reward[str(max(stages))] if stage not in stages else pass_reward[str(stage)]

	p_exp = {'remaining': -1, 'reward': -1}
	for key, value in pass_reward.items():
		if key == 'exp':
			_, exp_data = await common.execute_update(f'UPDATE progress SET exp = exp + {value} WHERE uid = "{uid}"')
			p_exp['remaining'] = exp_data[0][0]
			p_exp['reward'] = value
		else:
			_, data = await common.execute_update(f'UPDATE item SET value = value + {value} WHERE uid = "{uid}" AND iid = "{key}"')
			pass_stages.append({'iid': key, 'remaining': data[0][0], 'reward': value})

	p_stage = {'finally': stage_s, 'vary': 0}
	if stage_s + 1 == stage:  # 通过新关卡
		await common.execute_update(f'UPDATE progress SET stage = {stage} WHERE uid = "{uid}"')
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
	_, _ = await common.execute(f'UPDATE progress set exp = {exp} WHERE uid = "{uid}";', **kwargs)

	for i, iid in enumerate(iid_s):
		_, data = await common.execute_update(f'UPDATE item set value = {values[i]} WHERE uid = "{uid}" AND iid = "{iid}";', **kwargs)
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

	pass_towers = []
	pass_rewards = kwargs['pass_rewards']  # self._stage_reward["stage"]
	stages = [int(x) for x in pass_rewards.keys() if str.isdigit(x)]
	pass_reward = pass_rewards[str(max(stages))] if stage not in stages else pass_rewards[str(stage)]

	p_exp = {'remaining': -1, 'reward': -1}
	if stage % 10 == 0:
		reward = random.choices(population=pass_reward)[0]
		if 'skill' in reward:
			mpg = {'M': 0, 'P': 13, 'G': 26}
			sid = reward.replace('skill', '')
			enums.Skill
			if await try_unlock_skill(uid, sid, **kwargs):
				pass
				# TODO
			if reward_data["status"] == 0:
				tower_stage = (await self._try_material(world=world, unique_id=unique_id, material="tower_stage",
														value=1 if sql_stage + 1 == stage else 0))["remaining"]
				return self._message_typesetting(status=1, message="Successfully unlock new skills",
												 data={"remaining": {reward: 1, "tower_stage": tower_stage},
													   "reward": {reward: 1}})
			else:
				scroll = random.choices(population=pass_tower_data["skill_scroll"], weights=pass_tower_data["weights"])[
					0]
				scroll_data = await self._try_material(world=world, unique_id=unique_id, material=scroll, value=1)
				if scroll_data["status"] == 1:
					return self._message_typesetting(status=95, message="skill -> database operating error")
				tower_stage = (await self._try_material(world=world, unique_id=unique_id, material="tower_stage",
														value=1 if sql_stage + 1 == stage else 0))["remaining"]
				return self._message_typesetting(status=2, message="Gain a scroll", data={
					"remaining": {scroll: scroll_data["remaining"], "tower_stage": tower_stage}, "reward": {scroll: 1}})
		elif reward in pass_tower_data["weapon"]:  # weapon
			if len(pass_tower_data["segment"]) == 2:
				segment = random.randint(pass_tower_data["segment"][0], pass_tower_data["segment"][1])
			else:
				segment = pass_tower_data["segment"][0]
			sql_str = "update %s set segment=segment+%s where unique_id='%s'" % (reward, segment, unique_id)
			if await self._execute_statement_update(world=world, statement=sql_str) == 0:
				return self._message_typesetting(status=94, message="weapon -> database operating error")
			segment_result = await self._get_segment(world=world, unique_id=unique_id, weapon=reward)
			tower_stage = (await self._try_material(world=world, unique_id=unique_id, material="tower_stage",
													value=1 if sql_stage + 1 == stage else 0))["remaining"]
			return self._message_typesetting(status=3, message="Gain weapon fragments", data={
				"remaining": {"weapon": reward, "segment": segment_result, "tower_stage": tower_stage},
				"reward": {"segment": segment}})
		else:
			return self._message_typesetting(status=96, message="Accidental prize -> " + reward)
		_, exp_data = await common.execute_update(f'UPDATE progress SET exp = exp + {value} WHERE uid = "{uid}"')
	else:
		for key, value in pass_reward.items():
			if key == 'exp':
				_, exp_data = await common.execute_update(f'UPDATE progress SET exp = exp + {value} WHERE uid = "{uid}"')
				p_exp['remaining'] = exp_data[0][0]
				p_exp['reward'] = value
			else:
				_, data = await common.execute_update(f'UPDATE item SET value = value + {value} WHERE uid = "{uid}" AND iid = "{key}"')
				pass_towers.append({'iid': key, 'remaining': data[0][0], 'reward': value})

	p_stage = {'finally': stage_s, 'vary': 0}
	if stage_s + 1 == stage:  # 通过新关卡
		await common.execute_update(f'UPDATE progress SET stage = {stage} WHERE uid = "{uid}"')
		p_stage['finally'] = stage
		p_stage['vary'] = 1
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
		await common.execute_update(f'UPDATE skill SET value = 1 WHERE uid = "{uid}" AND sid = "{sid};"', **kwargs)
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
	_, exp_s = await common.execute_update(f'UPDATE progress SET exp = {exp_s} WHERE uid = "{uid}";', **kwargs)
	return True, {'exp': exp_s, 'level': exp_config.index(exp_list[0]) if exp_list != [] else len(exp_config), 'need': exp_list[0] - exp_s if exp_list != [] else 0}
