'''
task.py
'''

from module import enums
from module import common
from datetime import datetime


async def get_all_task(uid, **kwargs):
	kwargs.update({"task_id":enums.Task.LOGIN})
	await record_task(uid, **kwargs)
	await delete_old_data(uid, **kwargs)
	task_sql = await common.execute(f'SELECT tid, value, reward, timer FROM task WHERE uid = "{uid}";', **kwargs)
	return common.mt(0, 'success', {'tasks': [{'tid': t[0], 'task_value': t[1], 'reward': t[2], 'timer': t[3]} for t in task_sql]})


async def record_task(uid, **kwargs):
	await delete_old_data(uid, **kwargs)
	now = datetime.now(tz=common.TZ_SH).strftime("%Y-%m-%d %H:%M:%S")
	await common.execute(f'INSERT INTO task (uid, tid, value,reward,timer) VALUES ("{uid}", {kwargs["task_id"]},1,0,"{now}") ON DUPLICATE KEY UPDATE `value`= {1}', **kwargs)
	await common.execute(f'INSERT INTO task (uid, tid, value, reward, timer) SELECT "{uid}", {enums.Task.DONE_10_TASK}, IF((@i:=COUNT(*)) >= 10, 1, 0), 0, IF(COUNT(*) >= 10, "{now}", "") FROM task WHERE uid = "{uid}" ON DUPLICATE KEY UPDATE value=IF(@i >= 11 AND reward != 1, 1, value), timer=IF(@i >= 11 AND reward != 1 AND timer = "", "{now}", timer);', **kwargs)
	return common.mt(0, 'record:' + str(kwargs["task_id"]) + " success")


async def get_task_reward(uid, task_id, **kwargs):
	if task_id not in enums.Task._value2member_map_.keys(): return common.mt(98, 'task id type error')
	my_task = enums.Task(task_id).name.lower()
	item = kwargs["config"]["task"][my_task]["item_id"]
	quantity = kwargs["config"]["task"][my_task]["quantity"]
	data = await common.execute(f'SELECT value, reward FROM task WHERE uid = "{uid}" AND tid = "{task_id}"', **kwargs)
	if data==(): return common.mt(99, f'no reward for this task:{task_id}')
	if data[0][0] == 1 and data[0][1] == 0:
		_, remaining = await common.try_item(uid, enums.Item(item), quantity, **kwargs)
		await common.execute_update(f'UPDATE task set reward = 1 WHERE uid = "{uid}" AND tid = "{task_id}";', **kwargs)
		return common.mt(0, 'get reward success', {"reward": [{item: {"value": remaining, "reward": quantity}}], "task": task_id})
	return common.mt(99, f'no reward for this task:{task_id}')


async def delete_old_data(uid, **kwargs):
	now = datetime.now(tz=common.TZ_SH).strftime("%Y-%m-%d 00:00:00")
	await common.execute(f'DELETE FROM task WHERE uid="{uid}" AND timer<"{now}";', **kwargs)
