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


async def refresh(uid, **kwargs):
	kwargs.update({"task_id": enums.Task.CHECK_FACTORY})
	await task.record_task(uid, **kwargs)
	now              = datetime.now(tz=common.TZ_SH)
	steps, refresh_t = await steps_since(uid, now, **kwargs)
	rem, next_ref    = await remaining_seconds(uid, now, refresh_t, **kwargs)
	await common.set_timer(uid, enums.Timer.FACTORY_REFRESH, now - timedelta(seconds=rem), **kwargs)
	level, worker, storage = await get_state(uid, **kwargs)
	storage, delta         = update_state(steps, level, worker, storage, **kwargs)  # storage真实剩余数据，delta变化数据
	await record_resources(uid, storage, **kwargs)  # 更新数据库资源
	pool   = await remaining_pool_time(uid, now, **kwargs)
	ua, mw = await get_unassigned_workers(uid, **kwargs)  # ua未分配的工人数，mw总工人数
	# 记录成就的代码片段
	for k in RESOURCE_FACTORIES:
		if delta[k] <= 0: continue
		if k == enums.Factory.FOOD: kwargs.update({"aid": enums.Achievement.COLLECT_FOOD})
		elif k == enums.Factory.IRON: kwargs.update({"aid": enums.Achievement.COLLECT_MINE})
		elif k == enums.Factory.CRYSTAL: kwargs.update({"aid": enums.Achievement.COLLECT_CRYSTAL})
		else: continue
		await achievement.record_achievement(kwargs['data']['unique_id'], achievement_value=delta[k], **kwargs)
	# 计算加速剩余时间做后面的返回
	accel_end_t = await common.get_timer(uid, enums.Timer.FACTORY_ACCELERATION_END, **kwargs)
	accel_time  = 0 if accel_end_t is None else int((accel_end_t - now).total_seconds())
	# 计算许愿池下次许愿许愿消耗的钻石数
	count   = await common.get_limit(uid, enums.Limits.FACTORY_WISHING_POOL, **kwargs)
	diamond = 0 if count is None or pool == 0 else count * kwargs['config']['factory']['wishing_pool']['base_diamond']
	return common.mt(0, 'success', {'steps': steps, 'resource': {
			'remaining': {k.value: storage[k] for k in RESOURCE_FACTORIES},
			'reward': {k.value: delta[k] for k in RESOURCE_FACTORIES}},
			'pool': pool, 'pool_diamond': diamond,
			'next_refresh' : next_ref,
			'worker': {
				enums.Factory.UNASSIGNED.value : ua, 'total' : mw,
				**{k.value: worker[k] for k in BASIC_FACTORIES}
			},
			'level': {
				enums.Factory.ARMOR.value: level[enums.Factory.ARMOR],
				**{k.value : level[k] for k in HAS_LEVEL_FACTORIES}
			},
			'time': accel_time})

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
	data['refresh'] = (await refresh(uid, **kwargs))['data']
	return common.mt(0, 'success', data)


async def update_worker(uid, workers, **kwargs):
	# refresh with current settings
	l, w, _ = await get_state(uid, **kwargs)
	ua, mw = await get_unassigned_workers(uid, **kwargs)

	# sum workers <= max_worker else: return refresh + current workers
	uw = sum(w for w in workers.values())
	if uw > mw:
		return common.mt(99, 'insufficient workers', {'refresh': await _assist_refresh(uid, **kwargs), 'worker' : \
				{enums.Factory.UNASSIGNED.value : ua, **{k: w[k] for k in HAS_WORKER_FACTORIES}}})

	# worker_factories each do not exceed worker limit based on level else: return refresh + current workers
	for fac, new in workers.items():
		fid = enums.Factory(int(fac))
		if fid in HAS_WORKER_FACTORIES:
			if new > kwargs['config']['factory']['general']['worker_limits'][fac][str(l[fid])]:
				return common.mt(98, 'factory worker over limits', {'refresh': await _assist_refresh(uid, **kwargs), 'worker': \
						{enums.Factory.UNASSIGNED.value: ua, **{k: w[k] for k in HAS_WORKER_FACTORIES}}})
		else:
			return common.mt(97, 'invalid fid supplied', {'refresh' : await _assist_refresh(uid, **kwargs), 'worker' : \
					{enums.Factory.UNASSIGNED.value : ua, **{k : w[k] for k in HAS_WORKER_FACTORIES}}})

	# 改变工人情况
	for fac, new in workers.items():
		fid = enums.Factory(int(fac))
		await set_worker(uid, fid, new, **kwargs)
	await set_worker(uid, enums.Factory.UNASSIGNED, mw - uw, **kwargs)
	return common.mt(0, 'success', {'refresh': await _assist_refresh(uid, **kwargs), 'worker': {enums.Factory.UNASSIGNED.value : mw - uw, **workers}})

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
		return common.mt(97, 'max level', {'refresh' : {'resource' : r['data']['resource'],
				'armor' : r['data']['armor']}})
	can, crystal = await common.try_item(uid, enums.Item.CRYSTAL, -upgrade_cost, **kwargs)
	if not can: return common.mt(98, 'insufficient funds', {'refresh' : {'resource' : r['data']['resource']}})
	await common.execute(f'INSERT INTO `factory` (`uid`, `fid`, `level`) VALUES ("{uid}", {fid.value}, {l + 1}) ON DUPLICATE KEY UPDATE `level` = {l + 1};', **kwargs)
	# 记录成就的代码片段
	if fid == enums.Factory.FOOD.value:
		kwargs["aid"] = enums.Achievement.COLLECT_FOOD
	elif fid == enums.Factory.IRON.value:
		kwargs["aid"] = enums.Achievement.COLLECT_MINE
	elif fid == enums.Factory.CRYSTAL.value:
		kwargs["aid"] = enums.Achievement.COLLECT_CRYSTAL
	else: kwargs["aid"] = 0
	if kwargs["aid"]: await achievement.record_achievement(kwargs['data']['unique_id'], **kwargs)
	return common.mt(0, 'success', {'refresh': {'resource' : r['data']['resource']},
									'upgrade': {'cost': upgrade_cost, 'remain': crystal, 'fid': fid.value, 'level': l + 1}})

async def wishing_pool(uid, wid, **kwargs):
	now, dia_cost, count = datetime.now(tz=common.TZ_SH), 0, 0
	pool                 = await remaining_pool_time(uid, now, **kwargs)
	level, _, _          = await get_state(uid, **kwargs)
	if pool == 0:
		pool = (kwargs['config']['factory']['wishing_pool']['base_recover'] - level[enums.Factory.WISHING_POOL]) * 3600
		await common.set_limit(uid, enums.Limits.FACTORY_WISHING_POOL, 1, **kwargs)
		await common.set_timer(uid, enums.Timer.FACTORY_WISHING_POOL, now+timedelta(seconds=pool), **kwargs)
		_, dia_remain = await common.try_item(uid, enums.Item.DIAMOND, dia_cost, **kwargs)
	else:
		count = await common.get_limit(uid, enums.Limits.FACTORY_WISHING_POOL, **kwargs)
		if count >= kwargs['config']['factory']['wishing_pool']['limit']: return common.mt(98, 'The number of draws has reached the limit today')
		dia_cost = -count * kwargs['config']['factory']['wishing_pool']['base_diamond']
		can_pay, dia_remain = await common.try_item(uid, enums.Item.DIAMOND, dia_cost, **kwargs)
		if not can_pay: return common.mt(99, 'insufficient diamonds')
		await common.set_limit(uid, enums.Limits.FACTORY_WISHING_POOL, count + 1, **kwargs)
	seg_reward = roll_segment_value(**kwargs)
	seg_remain = await weapon._update_segment(uid, wid, seg_reward, **kwargs)
	return common.mt(0, 'success', {'pool' : pool, 'count' : (0 if pool == 0 else count) + 1, \
			'pool_diamond' : (count + 1) * kwargs['config']['factory']['wishing_pool']['base_diamond'], \
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


async def _assist_refresh(uid, **kwargs) -> dict:
	"""辅助工厂刷新工人需要的返回值"""
	r = await refresh(uid, **kwargs)
	return {'resource': r['data']['resource'], 'next_refresh': r['data']['next_refresh'], 'time': r['data']['time']}


def roll_segment_value(**kwargs):
	population = kwargs['config']['factory']['wishing_pool']['roll']['population']
	weights = kwargs['config']['factory']['wishing_pool']['roll']['weights']
	return kwargs['config']['factory']['wishing_pool']['base_segment'] * random.choices(population, weights)[0]

def update_state(steps, level, worker, storage, **kwargs):
	"""更新剩余量和变化量"""
	initial_storage = {k: v for k, v in storage.items()}
	for _ in range(steps):
		storage = step(level, worker, storage, **kwargs)
	delta = {k: storage[k] - initial_storage[k] for k in storage}
	return storage, delta

def step(level, worker, current, **kwargs):
	"""单次的步骤，计算每个工厂单个工人每步的生产效果，单位:(每步/每人/每个)"""
	for factory in BASIC_FACTORIES:
		current[factory] += sum([1 if can_produce(current, factory, level, **kwargs) else 0 for _ in range(worker[factory])])
	return current

def can_produce(current, factory, level, **kwargs):
	"""计算工厂当前的是否可生产，可生产的情况下扣除需要扣除的基本材料"""
	cost = {}
	kind = '1' if factory == enums.Factory.ARMOR else str(level[factory])
	if current[factory] + 1 > kwargs['config']['factory']['general']['storage_limits'][str(factory.value)][kind]:
		return False
	for f, a in kwargs['config']['factory']['general']['costs'][str(factory.value)].items():
		if current[enums.Factory(int(f))] < a:
			return False
		cost[enums.Factory(int(f))] = a
	for f, a in cost.items():
		current[f] -= a
	return True

async def has_acceleration(uid, now, **kwargs):
	accel_end_t = await common.get_timer(uid, enums.Timer.FACTORY_ACCELERATION_END,   **kwargs)
	return accel_end_t is not None and now < accel_end_t

async def remaining_seconds(uid, now, refresh_t, **kwargs):
	"""存在加速卡的情况下每步时间减半"""
	has_accel = await has_acceleration(uid, now, **kwargs)
	delta     = kwargs['config']['factory']['general']['step'] / (2 if has_accel else 1)
	remainder = int((now - refresh_t).total_seconds()) % delta  # 剩余时间，单位秒
	next_ref  = int(delta - remainder)  # 距离下次刷新的剩余时间，单位秒
	return remainder, next_ref

async def steps_since(uid, now, **kwargs):
	"""返回需要计算的步数和刷新时间"""
	accel_start_t = await common.get_timer(uid, enums.Timer.FACTORY_ACCELERATION_START, **kwargs)  # type => datetime or None
	accel_end_t   = await common.get_timer(uid, enums.Timer.FACTORY_ACCELERATION_END,   **kwargs)  # type => datetime or None
	refresh_t     = await common.get_timer(uid, enums.Timer.FACTORY_REFRESH,            **kwargs)  # type => datetime or None
	if refresh_t is None:
		return 0, now
	if accel_end_t is None or now >= accel_end_t:  # 现在时间和工厂加速结束时间比较，如果加速卡结束了
		accel_start_t, accel_end_t = refresh_t, refresh_t  # 加速卡的开始时间和结束时间都设置为刷新时间
	def sb(b, s, step):
		return int((b - s).total_seconds()) // step
	delta = kwargs['config']['factory']['general']['step']  # 跳跃步
	steps = int(
		sb(max(accel_start_t, refresh_t), refresh_t, delta) + \
		sb(min(accel_end_t, now), max(accel_start_t, refresh_t), delta / 2) + \
		sb(now, min(accel_end_t, now), delta)
	)
	return steps, refresh_t

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

