'''
task.py
'''

from module import enums
from module import common


async def get_all_task(uid, **kwargs):
	task = await common.execute(f'SELECT tid, value, reward, timer FROM task WHERE uid = "{uid}";', **kwargs)
	# kwargs.update({"tid":enums.Task.family_check_in,"value":1})
	# await record_achievement(uid,**kwargs)
	return common.mt(0, 'success', {'tasks': [{'tid': t[0], 'value': t[1], 'reward': t[2], 'timer': t[3]} for t in task]})

async def record_task(uid, **kwargs):
	data = await common.execute(f'INSERT INTO task (uid, aid, value,reward,timer) VALUES ("{uid}", {kwargs["aid"]}, {kwargs["value"]},0,"{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}") ON DUPLICATE KEY UPDATE `value`= {kwargs["value"]}',**kwargs)
	return common.mt(0, 'record:'+str(kwargs["aid"])+" success")

async def get_task_reward(uid,task_id,**kwargs):
	my_task = str.lower(enums.Task(kwargs["data"]["task_id"]).name)
	item = kwargs["config"][my_task]["item_id"]
	quantity = kwargs["config"][my_task]["quantity"]
	data = await common.execute(f'SELECT value, reward FROM task WHERE uid = "{uid}" AND tid = "{task_id}"',**kwargs)
	if data[0][0]==1 and data[0][1] == 0:
		_,remaining = await common.try_item(uid,enums.Item(item),quantity,**kwargs)
		await common.execute_update(f'UPDATE task set reward = 1 WHERE uid = "{uid}" AND tid = "{task_id}";', **kwargs)
		return common.mt(0, 'get reward success',{"reward":[{item:{"value":remaining,"reward":quantity}}],"task":enums.Achievement.TOTAL_LOGIN.value})
	return common.mt(99,'no reward for this task ')