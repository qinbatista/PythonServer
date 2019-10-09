'''
task.py
'''

from module import enums
from module import common


async def get_all_task(uid, **kwargs):
	task = await common.execute(f'SELECT tid, value, reward, timer FROM task WHERE uid = "{uid}";', **kwargs)
	return common.mt(0, 'success', {'tasks': [{'tid': t[0], 'value': t[1], 'reward': t[2], 'timer': t[3]} for t in task]})

