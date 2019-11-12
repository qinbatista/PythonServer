'''
task.py
'''

from module import enums
from module import common
from module import achievement
import time


async def get_all_task(uid, **kwargs):
	task = await common.execute(f'SELECT tid, value, reward, timer FROM task WHERE uid = "{uid}";', **kwargs)
	kwargs.update({"tid": enums.Task.LOGIN})
	await record_task(uid, **kwargs)

	# 世界boss自动通关
	kwargs.update({"tid": enums.Task.PASS_WORLD_BOSS})
	await record_task(uid, **kwargs)

	# 工厂领取物品
	kwargs.update({"tid": enums.Task.CHECK_FACTORY})
	await record_task(uid, **kwargs)

	# 家族签到
	kwargs.update({"tid": enums.Task.FAMILY_CHECK_IN})
	await record_task(uid, **kwargs)

	return common.mt(0, 'success', {'tasks': [{'tid': t[0], 'task_value': t[1], 'reward': t[2], 'timer': t[3]} for t in task]})


async def record_task(uid, **kwargs):
	data = await common.execute(
		f'INSERT INTO task (uid, tid, value,reward,timer) VALUES ("{uid}", {kwargs["tid"]},1,0,"{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}") ON DUPLICATE KEY UPDATE `value`= {kwargs["task_value"]}',
		**kwargs)
	return common.mt(0, 'record:' + str(kwargs["tid"]) + " success")


async def get_task_reward(uid, task_id, **kwargs):
	if task_id not in enums.Task._value2member_map_.keys(): return common.mt(98, 'task id type error')
	my_task = enums.Task(task_id).name.lower()
	item = kwargs["config"][my_task]["item_id"]
	quantity = kwargs["config"][my_task]["quantity"]
	data = await common.execute(f'SELECT value, reward FROM task WHERE uid = "{uid}" AND tid = "{task_id}"', **kwargs)
	if data[0][0] == 1 and data[0][1] == 0:
		_, remaining = await common.try_item(uid, enums.Item(item), quantity, **kwargs)
		await common.execute_update(f'UPDATE task set reward = 1 WHERE uid = "{uid}" AND tid = "{task_id}";', **kwargs)
		return common.mt(0, 'get reward success', {"reward": [{item: {"value": remaining, "reward": quantity}}], "task": task_id})
	return common.mt(99, f'no reward for this task:{task_id}')
