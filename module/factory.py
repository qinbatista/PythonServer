'''
factory.py
'''

import random

from module import enums
from module import common
from module import weapon
from module import task
from module import achievement
from datetime import datetime, timezone, timedelta

BASIC_FACTORIES      = {enums.Factory.CRYSTAL : None, enums.Factory.ARMOR : None, \
				        enums.Factory.IRON    : None, enums.Factory.FOOD  : None}

RESOURCE_FACTORIES   = {enums.Factory.FOOD : None, enums.Factory.IRON : None, enums.Factory.CRYSTAL : None}

HAS_LEVEL_FACTORIES  = {enums.Factory.FOOD         : None, enums.Factory.IRON  : None, \
				        enums.Factory.CRYSTAL      : None, enums.Factory.WISHING_POOL : None }

HAS_WORKER_FACTORIES = {enums.Factory.FOOD : None, enums.Factory.IRON : None, enums.Factory.CRYSTAL : None}


async def refresh(uid, **kwargs):
	kwargs.update({"task_id": enums.Task.CHECK_FACTORY})
	await task.record_task(uid,**kwargs)
	now              = datetime.now(timezone.utc)
	steps, refresh_t = await steps_since(uid, now, **kwargs)
	rem, next_ref    = await remaining_seconds(uid, now, refresh_t, **kwargs)
	await common.set_timer(uid, enums.Timer.FACTORY_REFRESH, now - timedelta(seconds = rem), **kwargs)
	level, worker, storage = await get_state(uid, **kwargs)
	storage, delta         = update_state(steps, level, worker, storage, **kwargs)
	await record_resources(uid, storage, **kwargs)
	aid    = await get_armor(uid, **kwargs)
	_, aq  = await common.try_armor(uid, aid, 1, delta[enums.Factory.ARMOR], **kwargs)
	pool   = await remaining_pool_time(uid, now, **kwargs)
	ua, mw = await get_unassigned_workers(uid, **kwargs)

	for k in RESOURCE_FACTORIES:
		if delta[k] == 0: continue
		if k == enums.Factory.FOOD: kwargs.update({"aid": enums.Achievement.COLLECT_FOOD})
		elif k == enums.Factory.IRON: kwargs.update({"aid": enums.Achievement.COLLECT_MINE})
		elif k == enums.Factory.CRYSTAL: kwargs.update({"aid": enums.Achievement.COLLECT_CRYSTAL})
		else: continue
		await achievement.record_achievement(kwargs['data']['unique_id'], achievement_value=delta[k], **kwargs)

	accel_end_t         = await common.get_timer(uid, enums.Timer.FACTORY_ACCELERATION_END,   **kwargs)
	accel_end_t         = accel_end_t   if accel_end_t   is not None else now
	accel_time = max(int((accel_end_t - now).total_seconds()), 0)
	# if accel_time == 0: await common.set_timer(uid, enums.Timer.FACTORY_ACCELERATION_END, now, **kwargs)
	return common.mt(0, 'success', {'steps' : steps, 'resource' :
			{'remaining' : {k.value : storage[k] for k in RESOURCE_FACTORIES},
			'reward' : {k.value : delta[k] for k in RESOURCE_FACTORIES}},
			'armor' : {'aid' : aid.value, 'remaining' : aq, 'reward' : delta[enums.Factory.ARMOR]},
			'pool' : pool,
			'next_refresh' : next_ref,
			'worker' : {enums.Factory.UNASSIGNED.value : ua, 'total' : mw,
					**{k.value: worker[k] for k in BASIC_FACTORIES}},
			'level' : {k.value : level[k] for k in HAS_LEVEL_FACTORIES},
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


async def update_worker(uid, workers, **kwargs):
	# refresh with current settings
	r = await refresh(uid, **kwargs)
	l, w, _ = await get_state(uid, **kwargs)
	ua, mw = await get_unassigned_workers(uid, **kwargs)
	r_ret = {'resource' : r['data']['resource'], 'armor' : r['data']['armor'], \
			'next_refresh' : r['data']['next_refresh'], 'time': r['data']['time']}

	# sum workers <= max_worker else: return refresh + current workers
	uw = sum(w for w in workers.values())
	if uw > mw:
		return common.mt(99, 'insufficient workers', {'refresh' : r_ret, 'worker' : \
				{enums.Factory.UNASSIGNED.value : ua, **{k : w[k] for k in HAS_WORKER_FACTORIES}}})

	# worker_factories each do not exceed worker limit based on level else: return refresh + current workers
	for fac, new in workers.items():
		fid = enums.Factory(int(fac))
		if fid in HAS_WORKER_FACTORIES:
			if new > kwargs['config']['factory']['general']['worker_limits'][fac][str(l[fid])]:
				return common.mt(98, 'factory worker over limits', {'refresh' : r_ret, 'worker' : \
						{enums.Factory.UNASSIGNED.value : ua, **{k : w[k] for k in HAS_WORKER_FACTORIES}}})
		else:
			return common.mt(97, 'invalid fid supplied', {'refresh' : r_ret, 'worker' : \
					{enums.Factory.UNASSIGNED.value : ua, **{k : w[k] for k in HAS_WORKER_FACTORIES}}})

	for fac, new in workers.items():
		fid = enums.Factory(int(fac))
		await set_worker(uid, fid, new, **kwargs)
	await set_worker(uid, enums.Factory.UNASSIGNED, mw - uw, **kwargs)
	return common.mt(0, 'success', {'refresh' : r_ret, \
			'worker' : {enums.Factory.UNASSIGNED.value : mw - uw, **workers}})

async def buy_worker(uid, **kwargs):
	unassigned, max_worker = await get_unassigned_workers(uid, **kwargs)
	max_cost_inc  = kwargs['config']['factory']['workers']['max']
	upgrade_cost  = kwargs['config']['factory']['workers']['cost'][str(min(max_worker + 1, max_cost_inc))]
	_, _, storage = await get_state(uid, **kwargs)
	if storage[enums.Factory.FOOD] < upgrade_cost:
		return common.mt(98, 'insufficient food')
	await common.execute(f'UPDATE `factory` SET `storage` = {storage[enums.Factory.FOOD] - upgrade_cost} \
			WHERE `uid` = "{uid}" AND `fid` = {enums.Factory.FOOD.value};', **kwargs)
	await common.execute(f'UPDATE `factory` SET `workers` = {unassigned + 1}, `storage` = {max_worker + 1} \
			WHERE `uid` = "{uid}" AND `fid` = {enums.Factory.UNASSIGNED.value};', **kwargs)
	return common.mt(0, 'success', {'worker' : {enums.Factory.UNASSIGNED.value : unassigned + 1, \
			'total' : max_worker + 1}, 'food' : {'remaining' : storage[enums.Factory.FOOD] - upgrade_cost, \
			'reward' : -upgrade_cost}})

async def upgrade(uid, fid, **kwargs):
	if fid not in HAS_LEVEL_FACTORIES: return common.mt(99, 'invalid fid')
	r = await refresh(uid, **kwargs)
	l = r['data']['level'][fid.value]
	crystal = r['data']['resource']['remaining'][enums.Factory.CRYSTAL.value]
	try:
		upgrade_cost = kwargs['config']['factory']['general']['upgrade_cost'][str(fid.value)][str(l + 1)]
	except KeyError:
		return common.mt(97, 'max level', {'refresh' : {'resource' : r['data']['resource'], \
				'armor' : r['data']['armor']}})
	if crystal < upgrade_cost:
		return common.mt(98, 'insufficient funds', {'refresh' : {'resource' : r['data']['resource'], \
				'armor' : r['data']['armor']}})
	if fid == enums.Factory.FOOD.value:
		kwargs["aid"] = enums.Achievement.COLLECT_FOOD
	elif fid == enums.Factory.IRON.value:
		kwargs["aid"] = enums.Achievement.COLLECT_MINE
	elif fid == enums.Factory.CRYSTAL.value:
		kwargs["aid"] = enums.Achievement.COLLECT_CRYSTAL
	else: kwargs["aid"] = 0
	if kwargs["aid"]: await achievement.record_achievement(kwargs['data']['unique_id'], **kwargs)
	await common.execute(f'INSERT INTO `factory` (`uid`, `fid`, `level`) VALUES ("{uid}", {fid.value}, \
			{l + 1}) ON DUPLICATE KEY UPDATE `level` = {l + 1};', **kwargs)
	await common.execute(f'UPDATE `factory` SET `storage` = {crystal - upgrade_cost} WHERE `uid` = "{uid}" \
			AND `fid` = {enums.Factory.CRYSTAL.value};', **kwargs)
	r['data']['resource']['remaining'][enums.Factory.CRYSTAL.value] = crystal - upgrade_cost
	return common.mt(0, 'success', {'refresh' : {'resource' : r['data']['resource'], \
			'armor' : r['data']['armor']}, 'upgrade' : {'cost' : upgrade_cost, 'fid' : fid.value, \
			'level' : l + 1}})

async def wishing_pool(uid, wid, **kwargs):
	now, dia_cost, count = datetime.now(timezone.utc), 0, 0
	pool                 = await remaining_pool_time(uid, now, **kwargs)
	level, _, _          = await get_state(uid, **kwargs)
	if pool == 0:
		pool  = ((kwargs['config']['factory']['wishing_pool']['base_recover'] - \
				level[enums.Factory.WISHING_POOL]) * 3600)
		await common.set_limit(uid, enums.Limits.FACTORY_WISHING_POOL, 1, **kwargs)
		await common.set_timer(uid, enums.Timer.FACTORY_WISHING_POOL, now+timedelta(seconds=pool), **kwargs)
		_, dia_remain = await common.try_item(uid, enums.Item.DIAMOND, dia_cost, **kwargs)
	else:
		count               = await common.get_limit(uid, enums.Limits.FACTORY_WISHING_POOL, **kwargs)
		dia_cost            = -1 * count * kwargs['config']['factory']['wishing_pool']['base_diamond']
		can_pay, dia_remain = await common.try_item(uid, enums.Item.DIAMOND, dia_cost, **kwargs)
		if not can_pay: return common.mt(99, 'insufficient diamonds')
		await common.set_limit(uid, enums.Limits.FACTORY_WISHING_POOL, count + 1, **kwargs)
	seg_reward     = roll_segment_value(**kwargs)
	seg_remain     = await weapon._update_segment(uid, wid, seg_reward, **kwargs)
	return common.mt(0, 'success', {'pool' : pool, 'count' : 0 if pool == 0 else count, \
			'diamond' : (count + 1) * kwargs['config']['factory']['wishing_pool']['base_diamond'], \
			'remaining' : {'wid' : wid.value, 'seg' : seg_remain, 'diamond' : dia_remain}, \
			'reward'    : {'wid' : wid.value, 'seg' : seg_reward, 'diamond' : dia_cost}})

async def buy_acceleration(uid, **kwargs):
	now                 = datetime.now(timezone.utc)
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
	await common.set_timer(uid, enums.Timer.FACTORY_ACCELERATION_END, \
			max(now + timedelta(days = 1), accel_end_t + timedelta(days = 1)), **kwargs)
	pool = max(int((accel_end_t - now).total_seconds()), 0)
	return common.mt(0, 'success', {'refresh' : {'resource' : r['data']['resource'], \
			'armor' : r['data']['armor']}, 'time' : pool, \
			'remaining' : {'diamond' : dia_remain}, 'reward' : {'diamond' : -dia_cost}})

async def set_armor(uid, aid, **kwargs):
	r = await refresh(uid, **kwargs)
	await common.execute(f'INSERT INTO `factory` (`uid`, `fid`, `storage`) VALUES \
			("{uid}", {enums.Factory.ARMOR.value}, {aid.value}) ON DUPLICATE KEY UPDATE \
			`storage` = {aid.value};', **kwargs)
	return common.mt(0, 'success', {'refresh' : {'resource' : r['data']['resource'], \
			'armor' : r['data']['armor']}, 'aid' : aid.value})

####################################################################################
def roll_segment_value(**kwargs):
	rng      = random.randint(0, 100)
	base_seg = kwargs['config']['factory']['wishing_pool']['base_segment']
	if 0 <= rng < 10:
		base_seg *= 3
	elif 10 <= rng < 55:
		base_seg *= 2
	return base_seg

def update_state(steps, level, worker, storage, **kwargs):
	initial_storage = {k : v for k, v in storage.items()}
	for _ in range(steps):
		storage = step(level, worker, storage, **kwargs)
	delta = {k : storage[k] - initial_storage[k] for k in storage}
	return storage, delta

def step(level, worker, current, **kwargs):
	for factory in BASIC_FACTORIES:
		for _ in range(worker[factory]):
			if not can_produce(current, factory, level, **kwargs):
				break
			current[factory] += 1
	return current

def can_produce(current, factory, level, **kwargs):
	cost = {}
	if factory != enums.Factory.ARMOR and current[factory] + 1 > \
		kwargs['config']['factory']['general']['storage_limits'][str(factory.value)][str(level[factory])]:
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
	if accel_end_t is not None and now < accel_end_t:
		return True
	return False

async def remaining_seconds(uid, now, refresh_t, **kwargs):
	has_accel = await has_acceleration(uid, now, **kwargs)
	delta     = kwargs['config']['factory']['general']['step'] / 2 if has_accel else \
				kwargs['config']['factory']['general']['step']
	remainder = int((now - refresh_t).total_seconds()) % delta
	next_ref  = delta - remainder
	return (remainder, next_ref)

async def steps_since(uid, now, **kwargs):
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
	data = await common.execute(f'SELECT `storage` FROM `factory` WHERE uid = "{uid}" AND \
			`fid` = {enums.Factory.ARMOR.value};', **kwargs)
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
	data = await common.execute(f'SELECT `workers`, `storage` FROM `factory` WHERE uid = "{uid}" \
			AND `fid` = {enums.Factory.UNASSIGNED.value};', **kwargs)
	return data[0][0], data[0][1]


async def record_resources(uid, storage, **kwargs):
	for factory in RESOURCE_FACTORIES:
		await common.execute(f'INSERT INTO `factory` (`uid`, `fid`, `storage`) VALUES ("{uid}", \
				{factory.value}, {storage[factory]}) ON DUPLICATE KEY UPDATE \
				`storage` = {storage[factory]};', **kwargs)

async def remaining_pool_time(uid, now, **kwargs):
	timer = await common.get_timer(uid, enums.Timer.FACTORY_WISHING_POOL, **kwargs)
	if timer is None:
		return 0
	return max(int((timer - now).total_seconds()), 0)

