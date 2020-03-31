'''
stage.py
'''

from module import enums
from module import common
from module import task
from module import achievement
from module import summoning
from module import vip
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
        return await p_general_stage(uid, stage, **kwargs)
    elif 3000 <= stage < 4000:
        kwargs.update({"task_id":enums.Task.PASS_WORLD_BOSS})
        await task.record_task(uid,**kwargs)
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

    stage_s = await common.get_progress(uid, 'stage', **kwargs)
    if stage <= 0 or stage > stage_s + 1:
        return common.mt(99, 'Parameter error')
    exp = await common.get_progress(uid, 'exp', **kwargs)

    stages = [int(x) for x in entry_consume.keys() if x.isdigit()]
    for i in range(stage, GENERAL_BASE_STAGE, -1):
        if i in stages:
            stage = i
            break
    if stage not in stages: return common.mt(96, 'No stage config file')

    stage = str(stage)
    iid_s = [k for k in entry_consume[stage].keys() if k != 'cost']
    values = [-int(v) for k, v in list(entry_consume[stage].items()) if k != 'cost']
    energy_consume = entry_consume[stage]['cost']  # 消耗能量数

    for i, iid in enumerate(iid_s):
        data = await common.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = "{iid}";', **kwargs)
        if data == ():
            await common.execute_update(f'INSERT INTO item (uid, iid) VALUES ("{uid}", "{iid}");', **kwargs)
            data = await common.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = "{iid}";', **kwargs)
        values[i] += data[0][0]
        if values[i] < 0: return common.mt(98, f'{iid} insufficient')

    # try_energy 扣体力看是否足够
    energy_data = await common.try_energy(uid, -energy_consume, **kwargs)
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
    await common.set_progress(uid, 'unstage', stage, **kwargs)
    return common.mt(0, 'success', {'enter_stages': enter_stages, 'exp_info': exp_info, 'world_boss': {}, 'energy': energy, 'enemy_layout': enemy_layout, 'monster': enemy_list})


# 通过普通关卡
async def p_general_stage(uid, stage, **kwargs):
    # success ===> 0
    # 0 : success
    # 96 : No stage config file
    # 98 : stage error
    # 99 : Parameter error
    # print(f'stage:{stage}, type:{type(stage)}')

    unstage = await common.get_progress(uid, 'unstage', **kwargs)
    if unstage != stage: return common.mt(98, 'stage error')
    await common.set_progress(uid, 'unstage', 0, **kwargs)
    stage_s = await common.get_progress(uid, 'stage', **kwargs)
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

    stage_s = await common.get_progress(uid, 'towerstage', **kwargs)
    if stage <= TOWER_BASE_STAGE or stage > stage_s + 1:
        return common.mt(99, 'Parameter error')
    exp = await common.get_progress(uid, 'exp', **kwargs)

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
    energy_data = await common.try_energy(uid, -energy_consume, **kwargs)
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
    await common.set_progress(uid, 'unstage', stage, **kwargs)
    return common.mt(0, 'success', {'enter_stages': enter_stages, 'exp_info': exp_info, 'world_boss': {}, 'energy': energy, 'enemy_layout': enemy_layout, 'monster': enemy_list})


# 通过闯塔关卡
async def p_tower_stage(uid, stage, **kwargs):
    # success ===> 0
    # 0 : success
    # 96 : No stage config file
    # 98 : stage error
    # 99 : Parameter error
    # print(f'stage:{stage}, type:{type(stage)}')
    unstage = await common.get_progress(uid, 'unstage', **kwargs)
    if unstage != stage: return common.mt(98, 'stage error')
    await common.set_progress(uid, 'unstage', 0, **kwargs)
    stage_s = await common.get_progress(uid, 'towerstage', **kwargs)
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
    stage_s = await common.get_progress(uid, 'stage', **kwargs)
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
        hang_stage = await common.get_progress(uid, 'hangstage', **kwargs)
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
    hang_stage = await common.get_progress(uid, 'hangstage', **kwargs)
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
    hang_stage = await common.get_progress(uid, 'hangstage', **kwargs)
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
    ld = await common.execute(f'SELECT value FROM leaderboard WHERE uid="{uid}" AND lid={enums.LeaderBoard.WORLD_BOSS};', **kwargs)
    return common.mt(0, 'Successfully get hook information', {'damage': 0 if ld == () else ld[0][0], 'world_boss': world_boss, 'boss_life_ratio': boss_life_ratio})


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
            await common.set_progress(uid, 'unstage', stage, **kwargs)
            return common.mt(0, "enter world boss success", data)
        elif status == 97:
            return common.mt(97, "no more energy")
        else:
            return common.mt(96, 'No stage config file')
    else:
        return common.mt(98, "no more ticket, try tomorrow")

async def get_top_damage(uid, page, **kwargs):
    if page < 1:
        return common.mt(99, 'Page number error')
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
    cached_uid_data = await kwargs['redis'].hgetall(f'leaderboard.player.{kwargs["world"]}.{uid}')
    if len(cached_uid_data) == 0:
        uid_data = await common.execute(uid_str, **kwargs)
        if uid_data != ():
            damage = uid_data[0][0]
            if uid_data[0][1] is None: uid_data = await common.execute(uid_str, **kwargs)
            ranking = int(uid_data[0][1])
            await kwargs['redis'].hmset_dict(f'leaderboard.player.{kwargs["world"]}.{uid}', \
                    {'damage' : uid_data[0][0], 'rank' : int(uid_data[0][1])})
            await kwargs['redis'].expire(f'leaderboard.player.{kwargs["world"]}.{uid}', 30)
    else:
        damage, ranking = cached_uid_data['damage'], int(cached_uid_data['rank'])

    data = await common.execute(f'SELECT p.gn, l.value, p.fid, p.uid FROM player p, leaderboard l WHERE p.uid = l.uid AND l.lid = {enums.LeaderBoard.WORLD_BOSS} ORDER BY l.value DESC LIMIT {(page - 1)*10},10;', **kwargs)
    if data == (): return common.mt(98, 'No data for this page')
    rank = [{'NO': (page - 1)*10 + 1 + i, 'name': d[0], 'damage': d[1], 'fid': '' if d[2] is None else d[2], 'level': (await increase_exp(d[3], 0, **kwargs))['level']} for i, d in enumerate(data)]
    return common.mt(0, 'success', {'page': page, 'damage': damage, 'ranking': ranking, 'rank': rank})

async def leave_world_boss_stage(uid, stage, damage, **kwargs):
    """
    0 - success
    98 - stage error
    99 - abnormal data
    """
    unstage = await common.get_progress(uid, 'unstage', **kwargs)
    if unstage != stage: return common.mt(98, 'stage error')
    await common.set_progress(uid, 'unstage', 0, **kwargs)
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


async def increase_weapon_segment(uid, wid, segment, **kwargs):
    data = await common.execute(f'SELECT segment FROM weapon WHERE uid = "{uid}" AND wid = "{wid}";', **kwargs)
    if data == ():
        await common.execute_update(f'INSERT INTO weapon (uid, wid, segment) VALUES ("{uid}", "{wid}", "{segment}");', **kwargs)
    else:
        await common.execute_update(f'UPDATE weapon SET segment = segment + {segment} WHERE uid = "{uid}" AND wid = "{wid}";', **kwargs)
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


async def old_mopping_up(uid, stage, count=1, **kwargs):
    """关于扫荡关卡的方法"""
    if count <= 0: return common.mt(96, 'Can only be a positive integer')
    if stage > await common.get_progress(uid, 'stage', **kwargs): return common.mt(99, 'Do not sweep until you pass this checkpoint')
    config = kwargs['config']['stages']['mopping-up'].get(f'{stage}', None)
    if config is None: return common.mt(98, 'There is no configuration information for this stage')  # 扫荡序章或未写配置的关卡会返回此结果
    # TODO 检查特殊物资是否能消耗
    energy = config['consumes']['special'].get('energy', 0) * count
    if (await common.try_energy(uid, 0, **kwargs))['data']['energy'] < energy: return common.mt(97, 'energy insufficient')
    # TODO 尝试消耗通用物资
    if not (await common.consume_items(uid, ','.join([f'{r[:r.rfind(":")]}:{int(r[r.rfind(":") + 1:]) * count}' for r in config['consumes']['common']]), **kwargs))[0]: return common.mt(95, 'materials insufficient')
    # TODO 消耗特殊物资(体力)
    data = (await common.try_energy(uid, -energy, **kwargs))['data']
    rewards = {'energy': {'cooling': data['cooling_time'], 'remain': data['energy'], 'reward': -energy}}
    # TODO 奖励普通物资
    results = await summoning.reward_items(uid, ','.join([f'{r[:r.rfind(":")]}:{int(r[r.rfind(":") + 1:]) * count}' for r in config['rewards']['common']]), **kwargs)
    rewards['remain'], rewards['reward'] = [f'{g}:{i}:{v}' for g, i, v, _ in results], [f'{g}:{i}:{v}' for g, i, _, v in results]
    # TODO 奖励特殊物资
    rewards['exp_info'] = await increase_exp(uid, config['rewards']['special']['exp'] * count, **kwargs)
    return common.mt(0, 'success', rewards)


# TODO 2020年1月14日
# ##################################################################
# ################### 2020年1月14日之后加入的方法 ###################
# ##################################################################
# 99 - Do not sweep until you pass this checkpoint
# 98 - There is no configuration information for this stage
# 97 - energy insufficient
# 96 - Can only be a positive integer
# 95 - materials insufficient
# 94 - stage mismatch
# 93 - abnormal damage
# 92 - no more ticket, try tomorrow
# 91 - stage error
# 90 - level insufficient
# 89 - Page number error
# 88 - No data for this page
# 87 - You didn't go pass
# 86 - You never hung up before
# 0 - success


async def enter(uid, sid, stage, **kwargs):
    """进入关卡"""
    if not STAGE_CHECK[sid](stage):
        return common.mt(91, 'stage error')
    _stage, _ = await common.get_stage(uid, sid, **kwargs)
    if stage > 1 + _stage:
        return common.mt(91, 'stage error')
    config = kwargs['config']['stages']['stage'].get(f'{stage}', None),
    if config is None:  # 关卡无配置信息
        return common.mt(98, 'There is no configuration information for this stage')
    config = dict(config[0]) if isinstance(config, tuple) else config
    if (await increase_exp(uid, 0, **kwargs))['level'] < config['constraint']['level']:
        return common.mt(90, 'level insufficient')
    results = {}
    # TODO 部分约束信息
    tim, lms = None, {}
    if sid in VERIFY:
        can, tim, lms = await VERIFY[sid](uid, **kwargs)
        if can:
            return common.mt(92, 'no more ticket, try tomorrow')
        results[sid.name] = {'limits': lms, 'cd': common.remaining_cd()}
    # TODO 检查特殊物资是否能消耗
    energy = config['consumes']['special'].get('energy', 0)
    if (await common.try_energy(uid, 0, **kwargs))['data']['energy'] < energy:
        return common.mt(97, 'energy insufficient')
    # TODO 尝试消耗通用物资
    can, cmw = await common.consume_items(uid, ','.join(config['consumes']['common']), **kwargs)
    if not can:
        return common.mt(95, 'materials insufficient')
    results['remain'], results['reward'] = rm_rw(cmw)
    # TODO 消耗特殊物资(体力)
    data = (await common.try_energy(uid, -energy, **kwargs))['data']
    # TODO 实现部分约束
    if sid in VERIFY:
        await REALIZE[sid](uid, tim, lms, **kwargs)
    # TODO 附加配置
    els, monsters = addition(stage, **kwargs)
    results['addition'] = {'els': els, 'monsters': monsters}
    # TODO 构建结果
    results['energy'] = {'cooling': data['cooling_time'], 'remain': data['energy'], 'reward': -energy}
    # TODO 设置关卡进入状态
    btm = datetime.now(tz=common.TZ_SH).strftime('%Y-%m-%d %H:%M:%S')
    await common.set_stage(uid, sid, _stage, btm, **kwargs)
    await kwargs['redis'].set(f'stage.{uid}', stage)
    return common.mt(0, 'success', results)


async def victory(uid, sid, stage, damage=0, **kwargs):
    """通关"""
    if not STAGE_CHECK[sid](stage):
        return common.mt(91, 'stage error')
    _stage, _btm = await common.get_stage(uid, sid, **kwargs)
    _stg = await kwargs['redis'].get(f'stage.{uid}')
    if _btm == '' or _stg is None or stage != int(_stg):
        return common.mt(94, 'stage mismatch')
    config, rewards = kwargs['config']['stages']['stage'].get(f'{stage}', None), {'boss': {}}
    # TODO 奖励普通物资
    rwc = config['rewards']['common']
    if config['constraint']['random'] == 1:
        rwc = random.choices(rwc, k=config['rewards']['random'])
    await rw_common(uid, rwc, rewards, **kwargs)
    # TODO 奖励特殊物资
    rewards['exp_info'] = await increase_exp(uid, config['rewards']['special'].get('exp', 0), **kwargs)
    rewards['max_stage'] = max(stage, _stage)
    # TODO 特殊处理
    if sid in VICTORY_DISPOSE:
        cm = await VICTORY_DISPOSE[sid](uid, stage, _stage, damage, rewards, **kwargs)
        if isinstance(cm, tuple):
            return common.mt(cm[0], cm[1])
    # TODO 设置关卡通过状态
    await common.set_stage(uid, sid, max(stage, _stage), '', **kwargs)
    await kwargs['redis'].delete(f'stage.{uid}')
    return common.mt(0, 'success', rewards)


async def mopping_up(uid, stage, count=1, **kwargs):
    """关于扫荡关卡的方法"""
    if count <= 0: return common.mt(96, 'Can only be a positive integer')
    _stage, _ = await common.get_stage(uid, enums.Stage.GENERAL, **kwargs)
    if stage > _stage:
        return common.mt(99, 'Do not sweep until you pass this checkpoint')
    config = kwargs['config']['stages']['mopping-up'].get(f'{stage}', None)
    if config is None:
        return common.mt(98, 'There is no configuration information for this stage')  # 扫荡序章或未写配置的关卡会返回此结果
    # TODO 检查特殊物资是否能消耗
    energy = config['consumes']['special'].get('energy', 0) * count
    if (await common.try_energy(uid, 0, **kwargs))['data']['energy'] < energy: return common.mt(97, 'energy insufficient')
    # TODO 尝试消耗通用物资
    if not (await common.consume_items(uid, ','.join([f'{r[:r.rfind(":")]}:{int(r[r.rfind(":") + 1:]) * count}' for r in config['consumes']['common']]), **kwargs))[0]:
        return common.mt(95, 'materials insufficient')
    # TODO 消耗特殊物资(体力)
    data = (await common.try_energy(uid, -energy, **kwargs))['data']
    rewards = {'energy': {'cooling': data['cooling_time'], 'remain': data['energy'], 'reward': -energy}}
    # TODO 奖励普通物资
    await rw_common(uid, config['rewards']['common'], rewards, mul=count, **kwargs)
    # TODO 奖励特殊物资
    rewards['exp_info'] = await increase_exp(uid, config['rewards']['special']['exp'] * count, **kwargs)
    return common.mt(0, 'success', rewards)


async def refresh_boss(uid, **kwargs):
    config = kwargs['config']['boss']
    now = datetime.now(tz=common.TZ_SH)
    ratio = {s: "%.2f" % (hp / config['HP'][s]) for s, hp in
             config['hp'].items()}
    damage = await get_leaderboard(uid, enums.LeaderBoard.WORLD_BOSS, **kwargs)
    tid, lid = enums.Timer.STAGE_WORLD_BOSS, enums.Limits.STAGE_WORLD_BOSS
    tim = await common.get_timer(uid, tid, timeformat='%Y-%m-%d', **kwargs)
    lim = await common.get_limit(uid, lid, **kwargs)
    if tim is None or now > tim:
        lim, tim = kwargs['config']['boss']['limit'], now + timedelta(days=1)
        await common.set_limit(uid, lid, lim, **kwargs)
        await common.set_timer(uid, tid, tim, timeformat='%Y-%m-%d', **kwargs)
    return common.mt(0, 'Successfully get hook information', {'damage': damage, 'limit': lim, 'cd': common.remaining_cd(), 'mcd': common.remaining_month_cd(), 'ratio': ratio})


async def all_infos(uid, **kwargs):
    """获取所有的关卡信息"""
    sts = await common.execute(f'SELECT `sid`, `stage` FROM `stages` WHERE `uid` = "{uid}";', **kwargs)
    ds = {s[0]: s[1] for s in sts}
    return common.mt(0, 'success', ds)


async def damage_ranking(uid, page, **kwargs):
    if page < 1:
        return common.mt(89, 'Page number error')
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
    cached_uid_data = await kwargs['redis'].hgetall(f'leaderboard.player.{kwargs["world"]}.{uid}')
    if len(cached_uid_data) == 0:
        uid_data = await common.execute(uid_str, **kwargs)
        if uid_data != ():
            damage = uid_data[0][0]
            if uid_data[0][1] is None: uid_data = await common.execute(uid_str, **kwargs)
            ranking = int(uid_data[0][1])
            await kwargs['redis'].hmset_dict(f'leaderboard.player.{kwargs["world"]}.{uid}',
                                             {'damage' : uid_data[0][0], 'rank': int(uid_data[0][1])})
            await kwargs['redis'].expire(f'leaderboard.player.{kwargs["world"]}.{uid}', 30)
    else:
        damage, ranking = cached_uid_data['damage'], int(cached_uid_data['rank'])

    data = await common.execute(f'SELECT p.gn, l.value, p.fid, p.uid FROM player p, leaderboard l WHERE p.uid = l.uid AND l.lid = {enums.LeaderBoard.WORLD_BOSS} ORDER BY l.value DESC LIMIT {(page - 1)*10},10;', **kwargs)
    if data == (): return common.mt(88, 'No data for this page')
    rank = [{'NO': (page - 1)*10 + 1 + i, 'name': d[0], 'damage': d[1], 'fid': '' if d[2] is None else d[2], 'level': (await increase_exp(d[3], 0, **kwargs))['level']} for i, d in enumerate(data)]
    return common.mt(0, 'success', {'page': page, 'damage': damage, 'ranking': ranking, 'rank': rank})


async def hang_up(uid, new=True, **kwargs):
    """开启挂机或获取挂机奖励"""
    if not new:
        return None
    now = datetime.now(tz=common.TZ_SH)
    tim = await common.get_timer(uid, enums.Timer.STAGE_HANG_UP, **kwargs)
    stage, _ = await common.get_stage(uid, enums.Stage.ENDLESS, **kwargs)
    if tim is None:
        if stage <= 1000:
            return common.mt(87, "You didn't go pass")
        await common.set_timer(uid, enums.Timer.STAGE_HANG_UP, now, **kwargs)
        return common.mt(86, "You never hung up before")
    cfc = kwargs['config']['stages']['constraint']['hang-up']['ENDLESS']
    mul = int(min((now - tim).total_seconds(), cfc['limit'])//cfc['step'])
    config = kwargs['config']['stages']['hang-up'][f'{stage}']['rewards']
    rewards = {}
    # TODO 奖励普通物资
    await rw_common(uid, config['common'], rewards, mul=mul, **kwargs)
    # TODO 奖励特殊物资
    rewards['exp_info'] = await increase_exp(uid, config['special'].get('exp', 0) * mul, **kwargs)
    await common.set_timer(uid, enums.Timer.STAGE_HANG_UP, now, **kwargs)
    return common.mt(0, 'success', rewards)


# ########################################### 私有方法 ############################################
def addition(stage, **kwargs):
    els = kwargs['config']['enemy_layouts']['enemyLayouts']
    monsters = kwargs['config']['monster']
    el = els[-1]['enemyLayout'] if stage > len(els) else els[stage - 1]['enemyLayout']
    els = []
    key_words = []
    for layout in el:
        for enemy in layout['enemyList']:
            en = enemy['enemysPrefString']
            if en not in key_words:
                key_words.append(en)
                els.append({en: monsters[en]})
    del key_words
    return els, monsters


async def b_dispose(uid, stage, damage, results, **kwargs):
    """BOSS伤害记录等信息处理"""
    config, _damage = kwargs['config']['boss'], await get_leaderboard(uid, enums.LeaderBoard.WORLD_BOSS, **kwargs)
    record = _damage < damage
    if damage < 0 or damage >= kwargs['config']['boss'].get('damage', 100_0000):
        return 93, "abnormal damage"
    else:
        hp = config['hp'][f'{stage}']
        config['hp'][f'{stage}'] = max(0, hp - damage)
        if record:
            await set_leaderboard(uid, enums.LeaderBoard.WORLD_BOSS, damage, **kwargs)
        ratio = {s: "%.2f" % (hp/config['HP'][s]) for s, hp in config['hp'].items()}
        results['boss'] = {'ratio': ratio, 'record': int(record), 'damage': max(damage, _damage)}


async def rw_common(uid, common, rewards, mul=1, **kwargs):
    """通用奖励信息的处理和修改"""
    cms = ','.join([f'{multiple_rw(mul, item)}' for item in common])
    results = await summoning.reward_items(uid, cms, **kwargs)
    rewards['remain'], rewards['reward'] = rm_rw(results)


def multiple_rw(mul, item):
    """倍数构造"""
    return f'{item[:item.rfind(":")]}:{int(item[item.rfind(":") + 1:]) * mul}'


def rm_rw(results):
    """剩余和改变情况的构造"""
    return [f'{g}:{i}:{v}' for g, i, v, _ in results], [f'{g}:{i}:{v}' for g, i, _, v in results]


async def v_coin(uid, lids, **kwargs):
    """验证金币挑战模式下的约束情况"""
    lv = (await vip.increase_exp(uid, 0, **kwargs))['level']
    config = kwargs['config']['stages']['constraint']['stage']['COIN']
    lcs = [config['limit'], config['buy']['vip'].get(f'{lv}', 2)]
    return await v_constraint(uid, enums.Timer.STAGE_COIN, lids, lcs, **kwargs)


async def v_exp(uid, lids, **kwargs):
    """验证经验挑战模式下的约束情况"""
    lv = (await vip.increase_exp(uid, 0, **kwargs))['level']
    config = kwargs['config']['stages']['constraint']['stage']['EXP']
    lcs = [config['limit'], config['buy']['vip'].get(f'{lv}', 2)]
    return await v_constraint(uid, enums.Timer.STAGE_EXP, lids, lcs, **kwargs)


async def v_constraint(uid, tid, lids, lcs, **kwargs):
    """各个模式下的验证、修改和重置"""
    now = datetime.now(tz=common.TZ_SH)
    tim = await common.get_timer(uid, tid, timeformat='%Y-%m-%d', **kwargs)
    lms = [await common.get_limit(uid, lid, **kwargs) for lid in lids]
    lms, tim = ({lids[i]: (lm - 1 if i == 0 else lm) for i, lm in enumerate(lcs)}, now + timedelta(days=1)) \
        if tim is None or now > tim else ({lids[i]: (lm - 1 if i == 0 else lm) for i, lm in enumerate(lms)}, tim)
    return lms[lids[0]] < 0, tim, lms


async def r_constraint(uid, tid, tim, lms, **kwargs):
    """实现相应模式下的修改和重置"""
    await common.set_timer(uid, tid, tim, timeformat='%Y-%m-%d', **kwargs)
    [await common.set_limit(uid, lid, lim, **kwargs) for lid, lim in lms.items()]


async def increase_exp(uid, exp, **kwargs):
    """
    exp为0则获得经验，反之增加经验，
    并返回总经验和等级，升到下一级需要的经验
    """
    # TODO 取配置和数据
    exp_config = kwargs['config']['exp']['player_level']['experience']
    sql_exp = await common.get_progress(uid, 'exp', **kwargs)
    # TODO 计算等级和需要的经验
    level, need = common.__calculate(exp_config, sql_exp)
    if exp == 0: return {'exp': sql_exp, 'level': level, 'need': need, 'reward': exp}
    # TODO 重新计算等级和需要的经验
    sql_exp += exp
    level, need = common.__calculate(exp_config, sql_exp)
    await common.set_progress(uid, 'exp', sql_exp, **kwargs)
    # TODO 返回总经验、等级、需要经验
    return {'exp': sql_exp, 'level': level, 'need': need, 'reward': exp}


async def get_leaderboard(uid, lid, **kwargs):
    data = await common.execute(f'SELECT value FROM leaderboard WHERE uid = "{uid}" AND lid = {lid};', **kwargs)
    return 0 if data == () else data[0][0]


async def set_leaderboard(uid, lid, damage, **kwargs):
    await common.execute(f'INSERT INTO leaderboard (uid, lid, value) VALUES ("{uid}", {lid}, {damage});', **kwargs)


async def init_stages(uid, **kwargs):
    await asyncio.gather(
        common.set_stage(uid, enums.Stage.GENERAL, 7, '', **kwargs),
        common.set_stage(uid, enums.Stage.ENDLESS, 1000, '', **kwargs),
        common.set_stage(uid, enums.Stage.BOSS, 3000, '', **kwargs),
        common.set_stage(uid, enums.Stage.COIN, 4000, '', **kwargs),
        common.set_stage(uid, enums.Stage.EXP, 4150, '', **kwargs),
    )


STAGE_CHECK = {
    enums.Stage.GENERAL: lambda s: 0 < s < 1000,
    enums.Stage.ENDLESS: lambda s: 1000 < s < 2000,
    enums.Stage.BOSS: lambda s: 3000 < s < 4000,
    enums.Stage.COIN: lambda s: 4000 < s < 4150,
    enums.Stage.EXP: lambda s: 4150 < s < 4300,
}


VERIFY = {
    enums.Stage.BOSS: lambda uid, **kwargs: v_constraint(uid, enums.Timer.STAGE_WORLD_BOSS, [enums.Limits.STAGE_WORLD_BOSS, ], [kwargs['config']['boss']['limit'], ], **kwargs),
    enums.Stage.COIN: lambda uid, **kwargs: v_coin(uid, [enums.Limits.STAGE_COIN, enums.Limits.STAGE_COIN_VIP], **kwargs),
    enums.Stage.EXP: lambda uid, **kwargs: v_exp(uid, [enums.Limits.STAGE_EXP, enums.Limits.STAGE_EXP_VIP], **kwargs),
}


REALIZE = {
    enums.Stage.BOSS: lambda uid, tim, lms, **kwargs: r_constraint(uid, enums.Timer.STAGE_WORLD_BOSS, tim, lms, **kwargs),
    enums.Stage.COIN: lambda uid, tim, lms, **kwargs: r_constraint(uid, enums.Timer.STAGE_COIN, tim, lms, **kwargs),
    enums.Stage.EXP: lambda uid, tim, lms, **kwargs: r_constraint(uid, enums.Timer.STAGE_EXP, tim, lms, **kwargs),
}


VICTORY_DISPOSE = {
    enums.Stage.BOSS: lambda uid, stage, _stage, damage, results, **kwargs: b_dispose(uid, stage, damage, results, **kwargs),
    enums.Stage.ENDLESS: lambda uid, stage, _stage, damage, results, **kwargs: hang_up(uid, new=stage > _stage, **kwargs),
}








