'''
stage.py
'''

from module import enums
from module import common
from module import task
from module import achievement
from datetime import datetime, timedelta
import time
import random
import asyncio

GENERAL_BASE_STAGE = 0
TOWER_BASE_STAGE = 1000
BOSS_BASE_STAGE = 3000

# 进入关卡
async def enter_stage(uid, stage, **kwargs):
	if stage < 1000: return await e_general_stage(uid, stage, **kwargs)
	elif 1000 <= stage < 2000: return await e_tower_stage(uid, stage, **kwargs)
	elif 2000 <= stage < 3000: return await e_tower_stage(uid, stage, **kwargs)
	elif 3000 <= stage < 4000: return await e_boss_stage(uid, stage, **kwargs)
	else: return common.mt(50, 'Abnormal parameter')


# 通过关卡
async def pass_stage(uid, stage, **kwargs):
	damage = kwargs['data'].get('damage', 0)
	if 0 < stage < 1000:
		kwargs.update({"task_id":enums.Task.PASS_MAIN_STAGE})
		await task.record_task(uid,**kwargs)

		kwargs.update({"aid":enums.Achievement.PASS_STAGE})
		await achievement.record_achievement(kwargs['data']['unique_id'], **kwargs)

		return await p_general_stage(uid, stage, **kwargs)
	elif 1000 <= stage < 2000:
		kwargs.update({"task_id":enums.Task.PASS_SPECIAL_STAGE})
		await task.record_task(uid,**kwargs)
		return await p_tower_stage(uid, stage, **kwargs)
	elif 2000 <= stage < 3000:
		kwargs.update({"task_id":enums.Task.PASS_WORLD_BOSS})
		await task.record_task(uid,**kwargs)
		return await p_general_stage(uid, stage, **kwargs)
	elif 3000 <= stage < 4000:
		return await leave_world_boss_stage(uid, stage, damage, **kwargs)
	else: return common.mt(50, 'Abnormal parameter')


# #################################################################################################
# ########################################## GENERAL STAGE ########################################
# #################################################################################################
# 进入普通关卡
async def e_general_stage(uid, stage, **kwargs):
	# 0 - success
	# 97 - Insufficient energy
	# 98 - key insufficient
	# 99 - parameter error
	enter_stages = []
	entry_consume = kwargs['config']['entry_consumables']
	enemy_layouts = kwargs['config']['enemy_layouts']['enemyLayouts']
	monster_config = kwargs['config']['monster']
	enemy_layout = enemy_layouts[-1]['enemyLayout'] if stage > len(enemy_layouts) else enemy_layouts[stage - 1]['enemyLayout']
	enemy_list = []
	key_words = []
	for layout in enemy_layout:
		for enemy in layout['enemyList']:
			enemy_name = enemy['enemysPrefString']
			if enemy_name not in key_words:
				key_words.append(enemy_name)
				enemy_list.append({enemy_name: monster_config[enemy_name]})
	del key_words

	stage_s = await get_progress(uid, 'stage', **kwargs)
	if stage <= 0 or stage > stage_s + 1:
		return common.mt(99, 'Parameter error')
	exp = await get_progress(uid, 'exp', **kwargs)

	stages = [int(x) for x in entry_consume.keys() if x.isdigit()]
	for i in range(stage, GENERAL_BASE_STAGE, -1):
		if i in stages:
			stage = i
			break
	if stage not in stages: return common.mt(96, 'No stage config file')

	stage = str(stage)
	iid_s = [k for k in entry_consume[stage].keys() if k != 'cost']
	values = [-1 * int(v) for k, v in list(entry_consume[stage].items()) if k != 'cost']
	energy_consume = entry_consume[stage]['cost']  # 消耗能量数

	for i, iid in enumerate(iid_s):
		data = await common.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = "{iid}";', **kwargs)
		if data == ():
			await common.execute_update(f'INSERT INTO item (uid, iid) VALUES ("{uid}", "{iid}");', **kwargs)
			data = await common.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = "{iid}";', **kwargs)
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
		enter_stages.append({'iid': int(iid), 'remaining': data[0][0], 'reward': -entry_consume[stage][iid]})
	exp_info = await increase_exp(uid, 0, **kwargs)
	energy = {'time': energy_data['data']['cooling_time'], 'remaining': energy_data['data']['energy'], 'reward': -energy_consume}
	await set_progress(uid, 'unstage', stage, **kwargs)
	return common.mt(0, 'success', {'enter_stages': enter_stages, 'exp_info': exp_info, 'world_boss': {}, 'energy': energy, 'enemy_layout': enemy_layout, 'monster': enemy_list})


# 通过普通关卡
async def p_general_stage(uid, stage, **kwargs):
	# success ===> 0
	# 0 : success
	# 96 : No stage config file
	# 98 : stage error
	# 99 : Parameter error
	# print(f'stage:{stage}, type:{type(stage)}')

	unstage = await get_progress(uid, 'unstage', **kwargs)
	if unstage != stage: return common.mt(98, 'stage error')
	await set_progress(uid, 'unstage', 0, **kwargs)
	stage_s = await get_progress(uid, 'stage', **kwargs)
	if stage <= 0 or stage_s + 1 < stage:
		return common.mt(99, 'stage level is not correct, cant be '+str(stage))

	pass_stages = []
	pass_rewards = kwargs['config']['stage_reward']
	stages = [int(x) for x in pass_rewards.keys() if str.isdigit(x) and int(x) < 1000]
	for i in range(stage, GENERAL_BASE_STAGE, -1):
		if i in stages:
			stage = i
			break
	if stage not in stages: return common.mt(96, 'No stage config file')
	pass_reward = pass_rewards[str(stage)]

	p_exp = {'remaining': -1, 'reward': -1}
	for key, value in pass_reward.items():
		if key == 'exp':
			await common.execute_update(f'UPDATE progress SET exp = exp + {value} WHERE uid = "{uid}";', **kwargs)
			exp_data = await common.execute(f'SELECT exp FROM progress WHERE uid = "{uid}";', **kwargs)
			p_exp['remaining'] = exp_data[0][0]
			p_exp['reward'] = value
		else:
			data = await common.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = "{key}";', **kwargs)
			if data == ():
				await common.execute_update(f'INSERT INTO item (uid, iid) VALUES ("{uid}", "{key}");', **kwargs)
				data = await common.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = "{key}";', **kwargs)
			await common.execute_update(f'UPDATE item SET value = value + {value} WHERE uid = "{uid}" AND iid = "{key}";', **kwargs)
			pass_stages.append({'iid': key, 'remaining': data[0][0] + value, 'reward': value})

	p_stage = {'finally': stage_s, 'vary': 0}
	if stage_s + 1 == stage:  # 通过新关卡
		await common.execute_update(f'UPDATE progress SET stage = {stage} WHERE uid = "{uid}"', **kwargs)
		p_stage['finally'] = stage
		p_stage['vary'] = 1
	return common.mt(0, 'success', data={'pass_stages': pass_stages, 'p_exp': p_exp, 'p_stage': p_stage})


# #################################################################################################
# ########################################## TOWER STAGE ##########################################
# #################################################################################################
# 进入闯塔关卡
async def e_tower_stage(uid, stage, **kwargs):
	# 0 - success
	# 97 - Insufficient energy
	# 98 - key insufficient
	# 99 - parameter error
	enter_stages = []
	entry_consume = kwargs['config']['entry_consumables']
	enemy_layouts = kwargs['config']['enemy_layouts']['enemyLayouts']
	monster_config = kwargs['config']['monster']
	enemy_layout = enemy_layouts[-1]['enemyLayout'] if stage > len(enemy_layouts) else enemy_layouts[stage - 1]['enemyLayout']
	enemy_list = []
	key_words = []
	for layout in enemy_layout:
		for enemy in layout['enemyList']:
			enemy_name = enemy['enemysPrefString']
			if enemy_name not in key_words:
				key_words.append(enemy_name)
				enemy_list.append({enemy_name: monster_config[enemy_name]})
	del key_words

	stage_s = await get_progress(uid, 'towerstage', **kwargs)
	if stage <= TOWER_BASE_STAGE or stage > stage_s + 1:
		return common.mt(99, 'Parameter error')
	exp = await get_progress(uid, 'exp', **kwargs)

	stages = [int(x) for x in entry_consume.keys() if x.isdigit()]

	for i in range(stage, TOWER_BASE_STAGE, -1):
		if i in stages:
			stage = i
			break
	if stage not in stages: return common.mt(96, 'No stage config file')

	stage = str(stage)
	iid_s = [k for k in entry_consume[stage].keys() if k != 'cost']
	values = [-1 * int(v) for k, v in list(entry_consume[stage].items()) if k != 'cost']
	energy_consume = entry_consume[stage]['cost']  # 消耗能量数

	for i, iid in enumerate(iid_s):
		data = await common.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = "{iid}";', **kwargs)
		if data == ():
			await common.execute_update(f'INSERT INTO item (uid, iid) VALUES ("{uid}", "{iid}");', **kwargs)
			data = await common.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = "{iid}";', **kwargs)
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
		enter_stages.append({'iid': int(iid), 'remaining': data[0][0], 'reward': -entry_consume[stage][iid]})

	exp_info = await increase_exp(uid, 0, **kwargs)
	energy = {'time': energy_data['data']['cooling_time'], 'remaining': energy_data['data']['energy'], 'reward': -energy_consume}
	await set_progress(uid, 'unstage', stage, **kwargs)
	return common.mt(0, 'success', {'enter_stages': enter_stages, 'exp_info': exp_info, 'world_boss': {}, 'energy': energy, 'enemy_layout': enemy_layout, 'monster': enemy_list})


# 通过闯塔关卡
async def p_tower_stage(uid, stage, **kwargs):
	# success ===> 0
	# 0 : success
	# 96 : No stage config file
	# 98 : stage error
	# 99 : Parameter error
	# print(f'stage:{stage}, type:{type(stage)}')
	unstage = await get_progress(uid, 'unstage', **kwargs)
	if unstage != stage: return common.mt(98, 'stage error')
	await set_progress(uid, 'unstage', 0, **kwargs)
	stage_s = await get_progress(uid, 'towerstage', **kwargs)
	if stage <= TOWER_BASE_STAGE or stage_s + 1 < stage:
		return common.mt(99, 'Parameter error')

	p_stage = {'finally': stage_s, 'vary': 0}
	if stage_s + 1 == stage:  # 通过新关卡
		await common.execute_update(f'UPDATE progress SET towerstage = {stage} WHERE uid = "{uid}"', **kwargs)
		p_stage['finally'] = stage
		p_stage['vary'] = 1

	pass_towers = []
	pass_rewards = kwargs['config']['stage_reward']
	stages = [int(x) for x in pass_rewards.keys() if str.isdigit(x)]

	for i in range(stage, TOWER_BASE_STAGE, -1):
		if i in stages:
			stage = i
			break
	if stage not in stages: return common.mt(96, 'No stage config file')

	pass_reward = pass_rewards[str(stage)]

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
				data = await common.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = "{key}";', **kwargs)
				if data == ():
					await common.execute_update(f'INSERT INTO item (uid, iid) VALUES ("{uid}", "{key}");', **kwargs)
					data = await common.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = "{key}";', **kwargs)
				await common.execute_update(f'UPDATE item SET value = value + {value} WHERE uid = "{uid}" AND iid = "{key}";', **kwargs)
				pass_towers.append({'iid': key, 'remaining': data[0][0] + value, 'reward': value})
	return common.mt(0, 'success', data={'pass_stages': pass_towers, 'p_exp': p_exp, 'p_stage': p_stage})


# #################################################################################################
# ########################################## HANG UP ##############################################
# #################################################################################################
# 启动挂机方法
async def start_hang_up(uid, stage, **kwargs):
	"""
	success ===> 0 , 1
	# 0 - hang up success
	# 1 - Repeated hang up successfully
	# 2 - same stage
	# 99 - Parameter error
	"""
	# 挂机方法是挂普通关卡
	stage_s = await get_progress(uid, 'stage', **kwargs)
	if stage <= 0 or stage_s < stage:
		return common.mt(99, 'stage level is not correct, cant be '+str(stage))

	data = await common.execute(f'SELECT time FROM timer WHERE uid = "{uid}" AND tid = "{enums.Timer.HANG_UP_TIME.value}";', **kwargs)
	if data == ():
		await common.execute_update(f'INSERT INTO timer (uid, tid) VALUES ("{uid}", "{enums.Timer.HANG_UP_TIME.value}");', **kwargs)
		data = await common.execute(f'SELECT time FROM timer WHERE uid = "{uid}" AND tid = "{enums.Timer.HANG_UP_TIME.value}";', **kwargs)
	hang_up_time = data[0][0]

	current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
	if hang_up_time == '':
		await common.execute_update(f'UPDATE timer SET time = "{current_time}" WHERE uid = "{uid}" AND tid = "{enums.Timer.HANG_UP_TIME.value}";', **kwargs)
		await common.execute_update(f'UPDATE progress SET hangstage = "{stage}" WHERE uid = "{uid}";', **kwargs)
		return common.mt(0, 'hang up success', {'start_hang_up_reward': [], 'hang_up_info': {'hang_stage': stage, 'time': '0:00:00'}})
	else:
		hang_stage = await get_progress(uid, 'hangstage', **kwargs)
		if hang_stage == stage: return common.mt(2, 'same stage')

		start_hang_up_reward = []
		probability_reward = kwargs['hang_rewards']['probability_reward']  # self._hang_reward["probability_reward"]
		hang_stage_rewards = kwargs['hang_rewards'][str(hang_stage)]  # self._hang_reward[str(hang_stage)]
		delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(hang_up_time, '%Y-%m-%d %H:%M:%S')
		minute = int(delta_time.total_seconds()) // 60
		# current_time = (datetime.strptime(hang_up_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=minute)).strftime("%Y-%m-%d %H:%M:%S")
		for iid, value in hang_stage_rewards.items():
			# value[抽中得到的数目，分子， 分母]    minute是次数，value[0]单次奖励的数值
			increment = value * minute if iid not in probability_reward else sum(random.choices(value[1]*[value[0]] + (value[2] - value[1])*[0], k=minute))  # 耗内存，省时间
			# increment = value * minute if iid not in probability_reward else sum([value[0] * int(random.randint(0, value[2]) - value[1] < 0) for i in range(minute)])  # 耗时间，省内存
			_, value = await common.try_item(uid, enums.Item(int(iid)), increment, **kwargs)
			start_hang_up_reward.append({'iid': iid, 'remaining': value, 'reward': increment})
		await common.execute_update(f'UPDATE timer SET time = "{current_time}" WHERE uid = "{uid}" AND tid = "{enums.Timer.HANG_UP_TIME.value}";', **kwargs)
		await common.execute_update(f'UPDATE progress SET hangstage = "{stage}" WHERE uid = "{uid}";', **kwargs)
		return common.mt(1, 'Repeated hang up successfully', {'start_hang_up_reward': start_hang_up_reward, 'hang_up_info': {'hang_stage': stage, 'time': int(delta_time.total_seconds())}})


# 获取挂机奖励
async def get_hang_up_reward(uid, **kwargs):
	"""
	success ===> 0
	# 0 - Settlement reward success
	# 99 - Temporarily no on-hook record
	"""
	data = await common.execute(f'SELECT time FROM timer WHERE uid = "{uid}" AND tid = "{enums.Timer.HANG_UP_TIME.value}";', **kwargs)
	if data == ():
		await common.execute_update(f'INSERT INTO timer (uid, tid) VALUES ("{uid}", "{enums.Timer.HANG_UP_TIME.value}");', **kwargs)
		data = await common.execute(f'SELECT time FROM timer WHERE uid = "{uid}" AND tid = "{enums.Timer.HANG_UP_TIME.value}";', **kwargs)
	hang_up_time = data[0][0]
	if hang_up_time == '':
		return common.mt(99, 'Temporarily no on-hook record')

	current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
	get_hang_up_rewards = []
	hang_stage = await get_progress(uid, 'hangstage', **kwargs)
	probability_reward = kwargs['config']['hang_reward']['probability_reward']
	stages = [int(s) for s in kwargs['config']['hang_reward'].keys() if s.isdigit()]

	for i in range(hang_stage, GENERAL_BASE_STAGE, -1):
		if i in stages:
			hang_stage = i
			break
	if hang_stage not in stages: return common.mt(96, 'No stage config file')

	hang_stage_rewards = kwargs['config']['hang_reward'][str(hang_stage)]  # self._hang_reward[str(hang_stage)]
	delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(hang_up_time, '%Y-%m-%d %H:%M:%S')
	minute = int(delta_time.total_seconds()) // 60
	# current_time = (datetime.strptime(hang_up_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=minute)).strftime("%Y-%m-%d %H:%M:%S")
	for iid, value in hang_stage_rewards.items():
		# value[抽中得到的数目，分子， 分母]    minute是次数，value[0]单次奖励的数值
		increment = value * minute if iid not in probability_reward else sum(random.choices(value[1] * [value[0]] + (value[2] - value[1]) * [0], k=minute))  # 耗内存，省时间
		# increment = value * minute if iid not in probability_reward else sum([value[0] * int(random.randint(0, value[2]) - value[1] < 0) for i in range(minute)])  # 耗时间，省内存
		_, value = await common.try_item(uid, enums.Item(int(iid)), increment, **kwargs)
		get_hang_up_rewards.append({'iid': iid, 'remaining': value, 'reward': increment})
	await common.execute_update(f'UPDATE timer SET time = "{current_time}" WHERE uid = "{uid}" AND tid = "{enums.Timer.HANG_UP_TIME.value}";', **kwargs)
	return common.mt(0, 'Settlement reward success', {'get_hang_up_rewards': get_hang_up_rewards, 'hang_up_info': {'hang_stage': hang_stage, 'time': int(delta_time.total_seconds())}})


# 获取挂机信息
async def get_hang_up_info(uid, **kwargs):
	"""
	success ===> 0
	# 0 - Successfully get hook information
	# 99 - Temporarily no on-hook record
	"""
	data = await common.execute(f'SELECT time FROM timer WHERE uid = "{uid}" AND tid = "{enums.Timer.HANG_UP_TIME.value}";', **kwargs)
	if data == ():
		await common.execute_update(f'INSERT INTO timer (uid, tid) VALUES ("{uid}", "{enums.Timer.HANG_UP_TIME.value}");', **kwargs)
		data = await common.execute(f'SELECT time FROM timer WHERE uid = "{uid}" AND tid = "{enums.Timer.HANG_UP_TIME.value}";', **kwargs)
	hang_up_time = data[0][0]
	if hang_up_time == '':
		return common.mt(99, 'Temporarily no on-hook record')

	current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
	get_hang_up_infos = []
	hang_stage = await get_progress(uid, 'hangstage', **kwargs)
	probability_reward = kwargs['config']['hang_reward']['probability_reward']  # self._hang_reward["probability_reward"]
	stages = [int(s) for s in kwargs['config']['hang_reward'].keys() if s.isdigit()]

	for i in range(hang_stage, GENERAL_BASE_STAGE, -1):
		if i in stages:
			hang_stage = i
			break
	if hang_stage not in stages: return common.mt(96, 'No stage config file')

	hang_stage_rewards = kwargs['config']['hang_reward'][str(hang_stage)]  # self._hang_reward[str(hang_stage)]
	delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(hang_up_time, '%Y-%m-%d %H:%M:%S')
	minute = int(delta_time.total_seconds()) // 60
	# current_time = (datetime.strptime(hang_up_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=minute)).strftime("%Y-%m-%d %H:%M:%S")
	for iid, value in hang_stage_rewards.items():
		# value[抽中得到的数目，分子， 分母]    minute是次数，value[0]单次奖励的数值
		increment = value * minute if iid not in probability_reward else sum(random.choices(value[1] * [value[0]] + (value[2] - value[1]) * [0], k=minute))  # 耗内存，省时间
		# increment = value * minute if iid not in probability_reward else sum([value[0] * int(random.randint(0, value[2]) - value[1] < 0) for i in range(minute)])  # 耗时间，省内存
		_, value = await common.try_item(uid, enums.Item(int(iid)), 0, **kwargs)
		get_hang_up_infos.append({'iid': iid, 'value': value, 'increment': increment})
	return common.mt(0, 'Successfully get hook information', {'get_hang_up_info': get_hang_up_infos, 'hang_up_info': {'hang_stage': hang_stage, 'time': int(delta_time.total_seconds())}})


# #################################################################################################
# ########################################## WORLD BOSS ###########################################
# #################################################################################################
async def check_boss_status(uid,**kwargs):
	timer = await common.execute(f'SELECT time FROM timer WHERE uid = "{uid}" and tid = {enums.Timer.WORLD_BOSS_CHALLENGE_TIME};', **kwargs)
	current_time = datetime.now(tz=common.TZ_SH).strftime('%Y-%m-%d')
	sql_time = current_time if timer == () else timer[0][0]
	delta_time = datetime.strptime(current_time, '%Y-%m-%d').replace(tzinfo=common.TZ_SH) - datetime.strptime(sql_time, '%Y-%m-%d').replace(tzinfo=common.TZ_SH)

	limits = await common.execute(f'SELECT value FROM limits WHERE uid = "{uid}" and lid = {enums.Limits.WORLD_BOSS_CHALLENGE_LIMITS};', **kwargs)
	enter_times, sql_time = (3, current_time) if limits == () or delta_time.days >= 1 else (limits[0][0], sql_time)

	await asyncio.gather(
		common.execute(f'INSERT INTO timer (uid, tid, time) VALUES ("{uid}", {enums.Timer.WORLD_BOSS_CHALLENGE_TIME},"{sql_time}") ON DUPLICATE KEY UPDATE `time`= "{sql_time}"',**kwargs),
		common.execute(f'INSERT INTO limits (uid, lid, value) VALUES ("{uid}", {enums.Limits.WORLD_BOSS_CHALLENGE_LIMITS},"{enter_times}") ON DUPLICATE KEY UPDATE `value`= {enter_times}',**kwargs)
	)

	world_boss = {'remaining': enter_times, 'time': common.remaining_cd(), 'month_time': common.remaining_month_cd()}
	remain_life = kwargs['config']['world_boss']["boss_life_remaining"]
	boss_life = kwargs['config']['world_boss']["boss_life"]
	boss_life_ratio = {}
	for i in range(0, len(remain_life)):
		boss_life_ratio[f'boss{i}'] = "%.2f" % (remain_life[i]/boss_life[i])
	return common.mt(0, 'Successfully get hook information', {'world_boss': world_boss, 'boss_life_ratio': boss_life_ratio})


async def e_boss_stage(uid, stage, **kwargs):
	if kwargs["config"]["world_boss"]["boss_life_remaining"][-1] <= 0: return common.mt(99, "boss all died")
	limits = await common.execute(f'SELECT value FROM limits WHERE uid = "{uid}" AND lid = {enums.Limits.WORLD_BOSS_CHALLENGE_LIMITS};', **kwargs)
	if limits[0][0] >= 1:
		status, data, consume = await try_stage(uid, stage, BOSS_BASE_STAGE, **kwargs)
		if status == 0:
			data.pop('recover_time')
			data['times'] = limits[0][0] - 1
			data['consume'] = consume
			data['cd_time'] = common.remaining_cd()
			await common.execute(f'UPDATE limits SET value = value - 1 WHERE uid = "{uid}" AND lid = {enums.Limits.WORLD_BOSS_CHALLENGE_LIMITS};', **kwargs)
			await set_progress(uid, 'unstage', stage, **kwargs)
			return common.mt(0, "enter world boss success", data)
		elif status == 97:
			return common.mt(97, "no more energy")
		else:
			return common.mt(96, 'No stage config file')
	else:
		return common.mt(98, "no more ticket, try tomorrow")

async def get_top_damage(uid, page, **kwargs):
	if page < 1: return common.mt(99, 'Page number error')
	uid_str = f"""
	SELECT c.value, c.NO FROM (
		SELECT * FROM (
			SELECT p.gn, l.value, (@i:=@i + 1) AS NO
			FROM player p, leaderboard l
			WHERE p.uid = l.uid AND l.lid = {enums.LeaderBoard.WORLD_BOSS.value} ORDER BY l.value DESC) temp,
			(SELECT (@i:=0)) t ORDER BY temp.`value` DESC
		) c, player p
	WHERE p.uid = "{uid}" AND c.gn = p.gn
	"""
	damage = 0  # 玩家造成的伤害
	ranking = -1  # 玩家在世界boss表中的排行
	uid_data = await common.execute(uid_str, **kwargs)
	if uid_data != ():
		damage = uid_data[0][0]
		if uid_data[0][1] is None: uid_data = await common.execute(uid_str, **kwargs)
		ranking = int(uid_data[0][1])
	data = await common.execute( f'SELECT p.gn, l.value, p.fid, p.uid FROM player p, leaderboard l WHERE p.uid = l.uid AND l.lid = {enums.LeaderBoard.WORLD_BOSS.value} ORDER BY l.value DESC LIMIT {(page - 1)*10},10;', **kwargs)
	if data == (): return common.mt(98, 'No data for this page')
	rank = []
	for i, d in enumerate(data):
		rank.append({'NO': (page - 1)*10 + 1 + i, 'name': d[0], 'damage': d[1], 'fid': '' if d[2] is None else d[2], 'level': (await increase_exp(d[3], 0, **kwargs))['level']})
	return common.mt(0, 'success', {'page': page, 'damage': damage, 'ranking': ranking, 'rank': rank})

async def leave_world_boss_stage(uid, stage, damage, **kwargs):
	"""
	0 - success
	98 - stage error
	99 - abnormal data
	"""
	unstage = await get_progress(uid, 'unstage', **kwargs)
	if unstage != stage: return common.mt(98, 'stage error')
	await set_progress(uid, 'unstage', 0, **kwargs)
	max_upload_damage = kwargs['config']['world_boss']['max_upload_damage']
	if damage < 0 or damage >= max_upload_damage: return common.mt(status=99, message="abnormal data")

	new_record = 0  # 0代表不是最新记录，1代表是最新记录
	data = await common.execute(f'SELECT value FROM leaderboard WHERE uid = "{uid}" AND lid = {enums.LeaderBoard.WORLD_BOSS.value};', **kwargs)
	if data == ():
		new_record, highest_damage = 1, damage
		await common.execute(f'INSERT INTO leaderboard (uid, lid, value) VALUES ("{uid}", {enums.LeaderBoard.WORLD_BOSS.value}, {damage});', **kwargs)
	elif damage > data[0][0]:
		new_record, highest_damage = 1, damage
		await common.execute(f'UPDATE leaderboard SET value={damage} WHERE uid = "{uid}" AND lid = {enums.LeaderBoard.WORLD_BOSS.value};', **kwargs)
	else:
		highest_damage = data[0][0]

	remain_life = kwargs['config']['world_boss']["boss_life_remaining"]
	boss_life = kwargs['config']['world_boss']["boss_life"]
	boss_life_ratio = {}
	for i in range(0, len(remain_life)):
		if remain_life[i] > 0 and damage > 0:
			if remain_life[i] - damage <= 0:
				damage -= remain_life[i]
				remain_life[i] = 0
			else:
				remain_life[i] -= damage
				damage = 0
		boss_life_ratio[f'boss{i}'] = "%.2f" % (remain_life[i]/boss_life[i])
	return common.mt(0, 'success', {'new_record': new_record, 'highest_damage': highest_damage, 'boss_life_ratio': boss_life_ratio})


############################################ 私有方法 ############################################


async def try_unlock_skill(uid, sid, **kwargs):
	# success ===> 0 and 1
	# True - success unlocked new skill
	# False - skill already unlocked
	skill = await common.execute(f'SELECT level FROM skill WHERE uid = "{uid}";', **kwargs)
	if skill == ():
		await common.execute_update(f'INSERT INTO skill (uid, sid, level) VALUES ("{uid}", "{sid}", 1);', **kwargs)
		return True
	elif skill[0][0] == 0:
		await common.execute_update(f'UPDATE skill SET level = 1 WHERE uid = "{uid}" AND sid = "{sid};"', **kwargs)
		return True
	return False


async def get_progress(uid, pid, **kwargs):
	data = await common.execute(f'SELECT {pid} FROM progress WHERE uid = "{uid}";', **kwargs)
	if data == ():
		await common.execute_update(f'INSERT INTO progress (uid) VALUE ("{uid}");', **kwargs)
		data = await common.execute(f'SELECT {pid} FROM progress WHERE uid = "{uid}";', **kwargs)
	return data[0][0]


async def set_progress(uid, pid, value, **kwargs):
	await common.execute(f'UPDATE progress SET {pid}="{value}" WHERE uid = "{uid}";', **kwargs)

async def increase_exp(uid, exp, **kwargs):
	"""
	exp:Need to increase the experience value
	exp = exp_increase
	exp_s:Exp data in the server
	exp_s = exp_server
	exp_config:Level configuration information
	exp_config = self._player['player_level']['experience']
	"""
	exp_config = kwargs['config']['exp']['player_level']['experience']
	exp_data = await common.execute(f'SELECT exp FROM progress WHERE uid = "{uid}";', **kwargs)
	if exp_data == ():
		await common.execute(f'INSERT INTO progress (uid) VALUE ("{uid}");', **kwargs)
		exp_data = await common.execute(f'SELECT exp FROM progress WHERE uid = "{uid}";', **kwargs)

	exp_s = exp_data[0][0]
	exp_list = [e for e in exp_config if e > exp_s]
	level, need = exp_config.index(exp_list[0]) if exp_list != [] else len(exp_config), exp_list[0] - exp_s if exp_list != [] else 0
	if exp == 0: return {'exp': exp_s, 'level': level, 'need': need}

	exp_s += exp
	exp_list = [e for e in exp_config if e > exp_s]
	level, need = exp_config.index(exp_list[0]) if exp_list != [] else len(exp_config), exp_list[0] - exp_s if exp_list != [] else 0
	await common.execute_update(f'UPDATE progress SET exp = {exp_s} WHERE uid = "{uid}";', **kwargs)
	return {'exp': exp_s, 'level': level, 'need': need}


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

async def try_stage(uid, stage, stage_type, **kwargs):
	entry_consume = kwargs['config']['entry_consumables']
	stages = [int(x) for x in entry_consume.keys() if x.isdigit()]
	for i in range(stage, stage_type, -1):
		if i in stages:
			stage = i
			break
	if stage not in stages: return 96, None, None
	energy_consume = entry_consume[str(stage)]['cost']  # 消耗能量数
	# try_energy 扣体力看是否足够
	energy_data = await common.try_energy(uid, -energy_consume, **kwargs)
	return (97, energy_data['data'], -energy_consume) if energy_data["status"] >= 97 else (0, energy_data['data'], -energy_consume)

