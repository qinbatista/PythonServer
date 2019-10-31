'''
factory.py
'''

from module import enums
from module import common
from datetime import datetime, timezone, timedelta

BASIC_FACTORIES    = {enums.Factory.CRYSTAL : None, enums.Factory.ARMOR : None, \
				      enums.Factory.IRON    : None, enums.Factory.FOOD  : None}

RESOURCE_FACTORIES = {enums.Factory.FOOD : None, enums.Factory.IRON : None, enums.Factory.CRYSTAL : None}


async def refresh(uid, **kwargs):
	now              = datetime.now(timezone.utc)
	steps, refresh_t = await steps_since(uid, now, **kwargs)
	remainder        = kwargs['config']['factory']['general']['step'] % int((now-refresh_t).total_seconds())
	await set_timer(uid, enums.Timer.FACTORY_REFRESH, now - timedelta(seconds = remainder), **kwargs)
	level, worker, storage = await get_state(uid, **kwargs)
	storage, delta         = update_state(steps, level, worker, storage, **kwargs)
	await record_resources(uid, storage, **kwargs)
	aid   = await get_armor(uid, **kwargs)
	_, aq = await common.try_armor(uid, aid, 1, delta[enums.Factory.ARMOR], **kwargs)

	return common.mt(0, 'success', {'steps' : steps, 'resource' : \
			{'remaining' : {k : storage[k] for k in RESOURCE_FACTORIES}, \
			'reward' : {k : delta[k] for k in RESOURCE_FACTORIES}}, \
			'armor' : {'aid' : aid.value, 'remaining' : aq, 'reward' : delta[enums.Factory.ARMOR]}})

######################################################
def update_state(steps, level, worker, storage, **kwargs):
	initial_storage = {k : v for k, v in storage.items()}
	for _ in range(steps):
		storage = step(level, worker, storage, **kwargs)
	delta = {k : storage[k] - initial_storage[k] for k in storage}
	return (storage, delta)

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

async def steps_since(uid, now, **kwargs):
	accel_start_t = await get_timer(uid, enums.Timer.FACTORY_ACCELERATION_START, **kwargs)
	accel_end_t   = await get_timer(uid, enums.Timer.FACTORY_ACCELERATION_END,   **kwargs)
	refresh_t     = await get_timer(uid, enums.Timer.FACTORY_REFRESH,            **kwargs)
	if refresh_t is None:
		return (0, now)
	if accel_start_t is None:
		accel_start_t, accel_end_t = refresh_t, refresh_t
	def sb(b, s, step):
		return int((b - s).total_seconds()) // step
	delta = kwargs['config']['factory']['general']['step']
	steps = int(sb(max(accel_start_t, refresh_t), refresh_t, delta) + \
			sb(min(accel_end_t, now), max(accel_start_t, refresh_t), delta / 2) + \
			sb(now, min(accel_end_t, now), delta))
	return (steps, refresh_t)

async def get_timer(uid, tid, timeformat = '%Y-%m-%d %H:%M:%S', **kwargs):
	data = await common.execute(f'SELECT `time` FROM `timer` WHERE `uid` = "{uid}" AND \
			`tid` = {tid.value};', **kwargs)
	return datetime.strptime(data[0][0], timeformat).replace(tzinfo = timezone.utc) if data != () else None

async def set_timer(uid, tid, time, timeformat = '%Y-%m-%d %H:%M:%S', **kwargs):
	await common.execute(f'INSERT INTO `timer` VALUES ("{uid}", {tid.value}, \
			"{time.strftime(timeformat)}") ON DUPLICATE KEY UPDATE \
			`time` = "{time.strftime(timeformat)}";', **kwargs)

async def get_state(uid, **kwargs):
	data = await common.execute(f'SELECT `fid`, `level`, `workers`, `storage` FROM `factory` WHERE \
			uid = "{uid}";', **kwargs)
	l, w, s = {e:1 for e in BASIC_FACTORIES}, {e:0 for e in BASIC_FACTORIES}, {e:0 for e in BASIC_FACTORIES}
	for f in data:
		if f[0] in BASIC_FACTORIES:
			l[enums.Factory(f[0])] = f[1]
			w[enums.Factory(f[0])] = f[2]
			s[enums.Factory(f[0])] = f[3]
	return (l, w, s)

async def record_resources(uid, storage, **kwargs):
	for factory in RESOURCE_FACTORIES:
		await common.execute(f'INSERT INTO `factory` (`uid`, `fid`, `storage`) VALUES ("{uid}", \
				{factory.value}, {storage[factory]}) ON DUPLICATE KEY UPDATE \
				`storage` = {storage[factory]};', **kwargs)

async def get_armor(uid, **kwargs):
	data = await common.execute(f'SELECT `storage` FROM `factory` WHERE uid = "{uid}" AND \
			`fid` = {enums.Factory.ARMOR.value};', **kwargs)
	return enums.Armor.A1
