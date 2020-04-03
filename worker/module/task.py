'''
task.py
'''

from module import enums
from module import common
from datetime import datetime


async def get_all_task(uid, **kwargs):
	await record(uid, enums.Task.LOGIN, **kwargs)
	await delete_old_data(uid, **kwargs)
	ts = await common.execute(f'SELECT tid, value, reward, timer FROM task WHERE uid = "{uid}";', **kwargs)
	return common.mt(0, 'success', {'tasks': [{'tid': t[0], 'task_value': t[1], 'reward': t[2], 'timer': t[3]} for t in ts]})


async def record(uid, tid, **kwargs):
	await delete_old_data(uid, **kwargs)
	now = datetime.now(tz=common.TZ_SH).strftime("%Y-%m-%d %H:%M:%S")
	await set_task(uid, tid, time=now, **kwargs)
	await common.execute(f'INSERT INTO task (uid, tid, value, reward, timer) SELECT "{uid}", {enums.Task.DONE_10_TASK}, IF((@i:=COUNT(*)) >= 10, 1, 0), 0, IF(COUNT(*) >= 10, "{now}", "") FROM task WHERE uid = "{uid}" ON DUPLICATE KEY UPDATE value=IF(@i >= 11 AND reward != 1, 1, value), timer=IF(@i >= 11 AND reward != 1 AND timer = "", "{now}", timer);', **kwargs)
	return common.mt(0, f'record:{tid} success')


async def get_task_reward(uid, tid, **kwargs):
	if tid not in enums.Task._value2member_map_.keys(): return common.mt(98, 'task id type error')
	tn = enums.Task(tid).name.lower()
	item = kwargs["config"]["task"][tn]["item_id"]
	quantity = kwargs["config"]["task"][tn]["quantity"]
	data = await common.execute(f'SELECT value, reward FROM task WHERE uid = "{uid}" AND tid = "{tid}"', **kwargs)
	if data==(): return common.mt(99, f'no reward for this task:{tid}')
	if data[0][0] == 1 and data[0][1] == 0:
		_, remaining = await common.try_item(uid, enums.Item(item), quantity, **kwargs)
		await common.execute_update(f'UPDATE task set reward = 1 WHERE uid = "{uid}" AND tid = "{tid}";', **kwargs)
		return common.mt(0, 'get reward success', {"reward": [{item: {"value": remaining, "reward": quantity}}], "task": tid})
	return common.mt(99, f'no reward for this task:{tid}')


async def delete_old_data(uid, **kwargs):
	now = datetime.now(tz=common.TZ_SH).strftime("%Y-%m-%d 00:00:00")
	await common.execute(f'DELETE FROM task WHERE uid="{uid}" AND timer<"{now}";', **kwargs)



async def set_task(uid, tid, value=1, reward=0, time=datetime.now(tz=common.TZ_SH).strftime("%Y-%m-%d %H:%M:%S"), **kwargs):
	await common.execute(f'INSERT INTO task (uid, tid, value,reward,timer) VALUES ("{uid}", {tid}, 1, 0, "{time}") ON DUPLICATE KEY UPDATE `value`= {value}, `reward`={reward}', **kwargs)

