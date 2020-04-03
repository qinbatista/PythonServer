'''
factory.py
'''

import random

from module import enums
from module import common
from module import weapon
from module import task
from module import achievement
from datetime import datetime, timedelta

BASIC_FACTORIES      = {enums.Factory.CRYSTAL : None, enums.Factory.ARMOR : None, \
                        enums.Factory.IRON    : None, enums.Factory.FOOD  : None}

RESOURCE_FACTORIES   = {enums.Factory.FOOD: enums.Item.FOOD,
                        enums.Factory.IRON: enums.Item.IRON,
                        enums.Factory.CRYSTAL: enums.Item.CRYSTAL,
                        enums.Factory.ARMOR: None}

HAS_LEVEL_FACTORIES  = {enums.Factory.FOOD         : None, enums.Factory.IRON  : None, \
                        enums.Factory.CRYSTAL      : None, enums.Factory.WISHING_POOL : None }

HAS_WORKER_FACTORIES = {enums.Factory.FOOD : None, enums.Factory.IRON : None, enums.Factory.CRYSTAL : None, enums.Factory.ARMOR : None}

COLLECTS = {enums.Factory.FOOD: enums.Achievement.COLLECT_FOOD,
                        enums.Factory.IRON: enums.Achievement.COLLECT_MINE,
                        enums.Factory.CRYSTAL: enums.Achievement.COLLECT_CRYSTAL}

UPGRADES = {enums.Factory.FOOD: enums.Achievement.UPGRADE_FOOD_FACTORY,
                        enums.Factory.IRON: enums.Achievement.UPGRADE_MINE_FACTORY,
                        enums.Factory.CRYSTAL: enums.Achievement.UPGRADE_CRYSTAL_FACTORY}

async def refresh(uid, **kwargs):
    now                  = datetime.now(tz=common.TZ_SH)
    steps, refresh_t     = await steps_since(uid, now, **kwargs)
    rem, next_ref, steps = await remaining_seconds(uid, now, refresh_t, steps, **kwargs)
    await common.set_timer(uid, enums.Timer.FACTORY_REFRESH, now - timedelta(seconds=rem), **kwargs)
    level, worker, storage = await get_state(uid, **kwargs)
    storage, delta         = update_state(steps, level, worker, storage, **kwargs)  # storage真实剩余数据，delta变化数据
    await record_resources(uid, storage, **kwargs)  # 更新数据库资源
    ua, mw = await get_unassigned_workers(uid, **kwargs)  # ua未分配的工人数，mw总工人数
    # 记录成就和任务的代码片段
    for k in COLLECTS:
        if delta[k] <= 0: continue
        await achievement.record(uid, COLLECTS[k], value=delta[k], **kwargs)
        await task.record(uid, enums.Task.CHECK_FACTORY, **kwargs)
    # 计算加速剩余时间做后面的返回
    accel_end_t = await common.get_timer(uid, enums.Timer.FACTORY_ACCELERATION_END, **kwargs)
    accel_time  = 0 if accel_end_t is None else int((accel_end_t - now).total_seconds())
    # 计算许愿池下次许愿许愿消耗的钻石数
    pool, count = await _refresh_wishing(uid, **kwargs)
    diamond = (kwargs['config']['factory']['wishing_pool']['limit'] - count) * kwargs['config']['factory']['wishing_pool']['base_diamond']
    return common.mt(0, 'success', {'steps': steps, 'resource': {
            'remaining': {k.value: storage[k] for k in RESOURCE_FACTORIES},
            'reward': {k.value: delta[k] for k in RESOURCE_FACTORIES}},
            'pool': pool, 'pool_count': count, 'pool_diamond': diamond,
            'next_refresh' : next_ref,
            'worker': {
                enums.Factory.UNASSIGNED.value : ua, 'total' : mw,
                **{k.value: worker[k] for k in BASIC_FACTORIES}
            },
            'level': {
                enums.Factory.ARMOR.value: level[enums.Factory.ARMOR],
                **{k.value : level[k] for k in HAS_LEVEL_FACTORIES}
            },
            'accel_time': accel_time})

async def increase_worker(uid, fid, n, **kwargs):
    if n <= 0: return common.mt(96, 'number must be positive')
    if fid not in HAS_WORKER_FACTORIES: return common.mt(97, 'invalid fid')
    unassigned, max_worker    = await get_unassigned_workers(uid, **kwargs)
    level, current_workers, _ = await get_state(uid, **kwargs)
    if n > unassigned: return common.mt(99, 'insufficient unassigned workers')
    if current_workers[fid] + n > \
            kwargs['config']['factory']['general']['worker_limits'][str(fid.value)][str(level[fid])]:
        return common.mt(98, 'cant increase past max worker')
    r = await refresh(uid, **kwargs)
    await common.execute(f'UPDATE `factory` SET `workers` = {unassigned - n} WHERE `uid` = "{uid}" \
            AND `fid` = {enums.Factory.UNASSIGNED.value};', **kwargs)
    await common.execute(f'INSERT INTO `factory` (`uid`, `fid`, `workers`) VALUES ("{uid}", {fid.value}, \
            {current_workers[fid] + n}) ON DUPLICATE KEY UPDATE \
            `workers` = {current_workers[fid] + n};', **kwargs)
    return common.mt(0, 'success', {'refresh' : {'resource' : r['data']['resource'], \
            'armor' : r['data']['armor']}, 'worker' : {'fid' : fid.value, \
            enums.Factory.UNASSIGNED.value : unassigned - n, 'workers' : current_workers[fid] + n}})

async def decrease_worker(uid, fid, n, **kwargs):
    if n <= 0: return common.mt(96, 'number must be positive')
    if fid not in HAS_WORKER_FACTORIES: return common.mt(97, 'invalid fid')
    unassigned, max_worker    = await get_unassigned_workers(uid, **kwargs)
    level, current_workers, _ = await get_state(uid, **kwargs)
    if n > current_workers[fid]: return common.mt(99, 'insufficient assigned workers')
    r = await refresh(uid, **kwargs)
    await common.execute(f'UPDATE `factory` SET `workers` = {unassigned + n} WHERE `uid` = "{uid}" \
            AND `fid` = {enums.Factory.UNASSIGNED.value};', **kwargs)
    await common.execute(f'UPDATE `factory` SET `workers` = {current_workers[fid] - n} WHERE \
            `uid` = "{uid}" AND `fid` = {fid.value};', **kwargs)
    return common.mt(0, 'success', {'refresh' : {'resource' : r['data']['resource'], \
            'armor' : r['data']['armor']}, 'worker' : {'fid' : fid.value, \
            enums.Factory.UNASSIGNED.value : unassigned + n, 'workers' : current_workers[fid] - n}})


async def gather_resource(uid, resource, **kwargs):
    """收集工厂资源
    resource: {"1" : 18989. "2" : 18989}"""
    _, _, storage = await get_state(uid, **kwargs)
    resource = {enums.Factory(int(k)): v for k, v in resource.items() if enums.Factory(int(k)) in RESOURCE_FACTORIES.keys()}
    resource = {k: storage[k] for k in resource.keys()}  # 使用服务器计算的资源
    if not resource: return common.mt(99, 'invalid resource')
    data = {'remaining': [], 'reward': []}
    for k, value in resource.items():
        storage[k] = 0
        if k == enums.Factory.ARMOR:
            aid = await get_armor(uid, **kwargs)
            _, remain = await common.try_armor(uid, aid, 1, value, **kwargs)
            data['remaining'].append(f'{enums.Group.ARMOR.value}:{aid}:{remain}')
            data['reward'].append(f'{enums.Group.ARMOR.value}:{aid}:{value}')
        else:
            _, remain = await common.try_item(uid, RESOURCE_FACTORIES[k], value, **kwargs)
            data['remaining'].append(f'{enums.Group.ITEM.value}:{RESOURCE_FACTORIES[k].value}:{remain}')
            data['reward'].append(f'{enums.Group.ITEM.value}:{RESOURCE_FACTORIES[k].value}:{value}')
    await record_resources(uid, storage, **kwargs)  # 更新数据库资源
    return common.mt(0, 'success', data)


async def update_worker(uid, workers, **kwargs):
    # refresh with current settings
    l, w, _ = await get_state(uid, **kwargs)
    ua, mw = await get_unassigned_workers(uid, **kwargs)

    # sum workers <= max_worker else: return refresh + current workers
    uw = sum(w for w in workers.values())
    if uw > mw:
        return common.mt(99, 'insufficient workers', {'refresh': await _assist_refresh(uid, **kwargs)})

    # worker_factories each do not exceed worker limit based on level else: return refresh + current workers
    for fac, new in workers.items():
        fid = enums.Factory(int(fac))
        if fid in HAS_WORKER_FACTORIES:
            kind = '1' if fid == enums.Factory.ARMOR else f'{l[fid]}'
            if new > kwargs['config']['factory']['general']['worker_limits'][fac][kind]:
                return common.mt(98, 'factory worker over limits', {'refresh': await _assist_refresh(uid, **kwargs)})
        else:
            return common.mt(97, 'invalid fid supplied', {'refresh': await _assist_refresh(uid, **kwargs)})

    # 改变工人情况
    for fac, new in workers.items():
        fid = enums.Factory(int(fac))
        await set_worker(uid, fid, new, **kwargs)
    await set_worker(uid, enums.Factory.UNASSIGNED, mw - uw, **kwargs)
    return common.mt(0, 'success', {'refresh': await _assist_refresh(uid, **kwargs)})

async def buy_worker(uid, **kwargs):
    unassigned, max_worker = await get_unassigned_workers(uid, **kwargs)
    max_cost_inc  = kwargs['config']['factory']['workers']['max']
    upgrade_cost  = kwargs['config']['factory']['workers']['cost'][str(min(max_worker + 1, max_cost_inc))]
    can, food = await common.try_item(uid, enums.Item.FOOD, -upgrade_cost, **kwargs)
    if not can: return common.mt(98, 'insufficient food')
    await common.execute(f'UPDATE `factory` SET `workers` = {unassigned + 1}, `storage` = {max_worker + 1} \
            WHERE `uid` = "{uid}" AND `fid` = {enums.Factory.UNASSIGNED.value};', **kwargs)
    return common.mt(0, 'success', {'worker': {enums.Factory.UNASSIGNED.value: unassigned + 1, \
            'total': max_worker + 1}, 'food' : {'remaining': food, 'reward': -upgrade_cost}})

async def upgrade(uid, fid, **kwargs):
    if fid not in HAS_LEVEL_FACTORIES: return common.mt(99, 'invalid fid')
    r = await refresh(uid, **kwargs)
    l = r['data']['level'][fid.value]  # 获取工厂等级
    try:
        upgrade_cost = kwargs['config']['factory']['general']['upgrade_cost'][str(fid.value)][str(l + 1)]
    except KeyError:
        return common.mt(97, 'max level', {'refresh' : {'resource' : r['data']['resource']}})
    can, crystal = await common.try_item(uid, enums.Item.CRYSTAL, -upgrade_cost, **kwargs)
    if not can: return common.mt(98, 'insufficient funds', {'refresh' : {'resource' : r['data']['resource']}})
    await common.execute(f'INSERT INTO `factory` (`uid`, `fid`, `level`) VALUES ("{uid}", {fid.value}, {l + 1}) ON DUPLICATE KEY UPDATE `level` = {l + 1};', **kwargs)
    pool = r['data']['pool']
    if fid == enums.Factory.WISHING_POOL:
        pool = max(0, pool - 3600)
        await common.set_timer(uid, enums.Timer.FACTORY_WISHING_POOL, datetime.now(tz=common.TZ_SH)+timedelta(seconds=pool), **kwargs)
    # 记录成就的代码片段
    for k in UPGRADES:
        await achievement.record(uid, UPGRADES[k], **kwargs)
    return common.mt(0, 'success', {'refresh': {'resource' : r['data']['resource']},
                                    'upgrade': {'cost': upgrade_cost, 'remaining': crystal, 'fid': fid.value, 'level': l + 1, 'pool': pool}})

async def wishing_pool(uid, wid, **kwargs):
    level, _, _ = await get_state(uid, **kwargs)
    pool, count = await _refresh_wishing(uid, **kwargs)
    if count <= 0: return common.mt(98, 'The number of draws has reached the limit today')
    dia_cost = (kwargs['config']['factory']['wishing_pool']['limit']-count) * kwargs['config']['factory']['wishing_pool']['base_diamond']
    can_pay, dia_remain = await common.try_item(uid, enums.Item.DIAMOND, dia_cost, **kwargs)
    if not can_pay: return common.mt(99, 'insufficient diamonds')
    if pool == 0:
        pool = (kwargs['config']['factory']['wishing_pool']['base_recover'] - level[enums.Factory.WISHING_POOL]) * 3600
        await common.set_timer(uid, enums.Timer.FACTORY_WISHING_POOL, datetime.now(tz=common.TZ_SH)+timedelta(seconds=pool), **kwargs)
    await common.set_limit(uid, enums.Limits.FACTORY_WISHING_POOL, count - 1, **kwargs)
    seg_reward = roll_segment_value(**kwargs)
    seg_remain = await weapon._update_segment(uid, wid, seg_reward, **kwargs)
    return common.mt(0, 'success', {'pool': pool, 'count': count - 1, \
            'pool_diamond': dia_cost + kwargs['config']['factory']['wishing_pool']['base_diamond'], \
            'remaining' : {'wid' : wid.value, 'seg' : seg_remain, 'diamond' : dia_remain}, \
            'reward'    : {'wid' : wid.value, 'seg' : seg_reward, 'diamond' : dia_cost}})

async def buy_acceleration(uid, **kwargs):
    now                 = datetime.now(tz=common.TZ_SH)
    dia_cost            = kwargs['config']['factory']['general']['acceleration_cost']
    can_pay, dia_remain = await common.try_item(uid, enums.Item.DIAMOND, -dia_cost, **kwargs)
    if not can_pay: return common.mt(99, 'insufficient funds')
    accel_start_t       = await common.get_timer(uid, enums.Timer.FACTORY_ACCELERATION_START, **kwargs)
    accel_end_t         = await common.get_timer(uid, enums.Timer.FACTORY_ACCELERATION_END,   **kwargs)
    accel_start_t       = accel_start_t if accel_start_t is not None else now
    accel_end_t         = accel_end_t   if accel_end_t   is not None else now
    r                   = await refresh(uid, **kwargs)
    if now >= accel_start_t:
        await common.set_timer(uid, enums.Timer.FACTORY_ACCELERATION_START, now, **kwargs)
    accel_end_t = max(now + timedelta(days=1), accel_end_t + timedelta(days=1))
    await common.set_timer(uid, enums.Timer.FACTORY_ACCELERATION_END, accel_end_t, **kwargs)
    return common.mt(0, 'success', {'refresh': {'resource' : r['data']['resource']}, 'time': int((accel_end_t - now).total_seconds()),
            'remaining': {'diamond': dia_remain}, 'reward': {'diamond' : -dia_cost}})

async def set_armor(uid, aid, **kwargs):
    gather = await gather_resource(uid, {enums.Factory.ARMOR: 99}, **kwargs)
    await common.execute(f'INSERT INTO `factory` (`uid`, `fid`, `workers`, `level`) VALUES ("{uid}", {enums.Factory.ARMOR.value}, 0, {aid.value}) ON DUPLICATE KEY UPDATE `level` = {aid.value};', **kwargs)
    return common.mt(0, 'success', {'gather': gather['data'], 'aid': aid.value})

####################################################################################


async def _refresh_wishing(uid, **kwargs):
    now  = datetime.now(tz=common.TZ_SH)
    pool = await remaining_pool_time(uid, now, **kwargs)
    if pool == 0:
        count = kwargs['config']['factory']['wishing_pool']['limit']
        await common.set_limit(uid, enums.Limits.FACTORY_WISHING_POOL, count, **kwargs)
    else:
        count = await common.get_limit(uid, enums.Limits.FACTORY_WISHING_POOL, **kwargs)
    return pool, count

async def _assist_refresh(uid, **kwargs) -> dict:
    """辅助工厂刷新工人需要的返回值"""
    r = await refresh(uid, **kwargs)
    return r['data']


def roll_segment_value(**kwargs):
    population = kwargs['config']['factory']['wishing_pool']['roll']['population']
    weights = kwargs['config']['factory']['wishing_pool']['roll']['weights']
    return kwargs['config']['factory']['wishing_pool']['base_segment'] * random.choices(population, weights)[0]

def update_state(steps, level, worker, storage, **kwargs):
    """更新剩余量和变化量"""
    # initial_storage, need = {k: v for k, v in storage.items()}, 10000
    # multiple = max(steps / need, 1)
    # [step(level, worker, storage, **kwargs) for _ in range(min(steps, need))]
    # config = kwargs['config']['factory']['general']['storage_limits']
    # storage = {k: min(config[f'{k}']['1' if k == enums.Factory.ARMOR else f'{level[k]}'], int(v * multiple)) if k in BASIC_FACTORIES else v for k, v in storage.items()}
    # delta = {k: storage[k] - initial_storage[k] for k in storage}
    fcg = kwargs['config']['factory']['general']  # factory config general
    initial_storage, lmd = {k: v for k, v in storage.items()}, {}
    for factory in initial_storage.keys():
        if factory in BASIC_FACTORIES:
            # cmv: cost multiple value  cfk: cost factory key
            km = '1' if factory == enums.Factory.ARMOR else f'{level[factory]}'
            lmd[factory] = fcg['storage_limits'][f'{factory}'][km]
            cost, cmv = {}, steps * worker[factory]
            for cf, cv in fcg['costs'][f'{factory}'].items():
                cfk = enums.Factory(int(cf))
                cmv, cost[cfk] = min(storage[cfk] // cv, cmv), cv
            storage[factory] += cmv
            for cf, cv in cost.items():
                storage[cf] -= cv * cmv
    storage = {k: lmd[k] if (k in BASIC_FACTORIES and lmd[k] < v) else v for k, v in storage.items()}
    delta = {k: storage[k] - initial_storage[k] for k in storage}
    return storage, delta

def step(level, worker, current, **kwargs):
    """单次的步骤，计算每个工厂单个工人每步的生产效果，单位:(每步/每人/每个)"""
    for factory in BASIC_FACTORIES:
        current[factory] += sum([1 if can_produce(current, factory, level, **kwargs) else 0 for _ in range(worker[factory])])

def can_produce(current, factory, level, **kwargs):
    """计算工厂当前的是否可生产，可生产的情况下扣除需要扣除的基本材料"""
    cost = {}
    kind = '1' if factory == enums.Factory.ARMOR else str(level[factory])
    if current[factory] + 1 > kwargs['config']['factory']['general']['storage_limits'][f'{factory}'][kind]:
        return False
    for f, a in kwargs['config']['factory']['general']['costs'][f'{factory}'].items():
        if current[enums.Factory(int(f))] < a:
            return False
        cost[enums.Factory(int(f))] = a
    for f, a in cost.items():
        current[f] -= a
    return True

async def has_acceleration(uid, now, **kwargs):
    accel_end_t = await common.get_timer(uid, enums.Timer.FACTORY_ACCELERATION_END,   **kwargs)
    return accel_end_t is not None and now < accel_end_t

async def remaining_seconds(uid, now, refresh_t, steps, **kwargs):
    """存在加速卡的情况下每步时间减半"""
    has_accel = await has_acceleration(uid, now, **kwargs)
    delta     = kwargs['config']['factory']['general']['step'] / (2 if has_accel else 1)
    remainder = int((now - refresh_t).total_seconds()) % delta  # 剩余时间，单位秒
    next_ref  = int(delta - remainder)  # 距离下次刷新的剩余时间，单位秒
    return (0, delta, steps + 1) if next_ref <= 2 else (remainder, next_ref, steps)

async def steps_since(uid, now, **kwargs):
    """返回需要计算的步数和刷新时间
    ast：acceleration start time
    aet：acceleration end time
    rft：refresh time"""
    ast = await common.get_timer(uid, enums.Timer.FACTORY_ACCELERATION_START, **kwargs)
    aet = await common.get_timer(uid, enums.Timer.FACTORY_ACCELERATION_END, **kwargs)
    rft = await common.get_timer(uid, enums.Timer.FACTORY_REFRESH, **kwargs)
    if rft is None:
        return 0, now
    if aet is None or now >= aet:  # 现在时间和工厂加速结束时间比较，如果加速卡结束了
        ast, aet = rft, rft  # 加速卡的开始时间和结束时间都设置为刷新时间
    delta = kwargs['config']['factory']['general']['step']  # 跳跃步
    steps = sb(max(ast, rft), rft, delta) +\
            sb(min(aet, now), max(ast, rft), delta / 2) +\
            sb(now, min(aet, now), delta)
    return steps, rft

async def get_armor(uid, **kwargs):
    data = await common.execute(f'SELECT `level` FROM `factory` WHERE uid = "{uid}" AND `fid` = {enums.Factory.ARMOR};', **kwargs)
    return enums.Armor(data[0][0]) if data != () else enums.Armor.A1

async def set_worker(uid, fid, val, **kwargs):
    await common.execute(f'INSERT INTO `factory` (`uid`, `fid`, `workers`) VALUES \
            ("{uid}", {fid.value}, {val}) ON DUPLICATE KEY UPDATE `workers` = {val};', **kwargs)

async def get_state(uid, **kwargs):
    data = await common.execute(f'SELECT `fid`, `level`, `workers`, `storage` FROM `factory` WHERE uid = "{uid}";', **kwargs)
    l, w, s = {e: 1 for e in enums.Factory}, {e: 0 for e in enums.Factory}, {e: 0 for e in enums.Factory}
    for f in data:
        l[enums.Factory(f[0])] = f[1]
        w[enums.Factory(f[0])] = f[2]
        s[enums.Factory(f[0])] = f[3]
    return l, w, s

async def get_unassigned_workers(uid, **kwargs):
    data = await common.execute(f'SELECT `workers`, `storage` FROM `factory` WHERE uid = "{uid}" AND `fid` = {enums.Factory.UNASSIGNED.value};', **kwargs)
    return data[0]


async def record_resources(uid, storage, **kwargs):
    for factory in RESOURCE_FACTORIES:
        await common.execute(f'INSERT INTO `factory` (`uid`, `fid`, `storage`) VALUES ("{uid}", \
                {factory.value}, {storage[factory]}) ON DUPLICATE KEY UPDATE \
                `storage` = {storage[factory]};', **kwargs)

async def remaining_pool_time(uid, now, **kwargs):
    timer = await common.get_timer(uid, enums.Timer.FACTORY_WISHING_POOL, **kwargs)
    return 0 if timer is None else max(int((timer - now).total_seconds()), 0)


def sb(b, s, step):
    return int((b - s).total_seconds() // step)
