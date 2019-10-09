'''
weapon.py

CHECKED WITH LIANG
'''

import asyncio

from module import enums
from module import common

from collections import defaultdict

STANDARD_IRON = 40
STANDARD_RESET = 100
STANDARD_SEGMENT = 25

async def check_boss_status(uid, wid, amount, **kwargs):
	data = await self._execute_statement(world,f'select world_boss_enter_time,world_boss_remaining_times from player where unique_id ="{unique_id}"')
	if data[0][0]=="":
		current_time1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		data = await self._execute_statement_update(world,f'UPDATE player SET world_boss_enter_time ="{current_time1}",world_boss_remaining_times ="{str(self._max_enter_time)}" WHERE unique_id = "{unique_id}"')
	current_time1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	current_time2 = (datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")
	d1 = datetime.strptime(current_time1, '%Y-%m-%d %H:%M:%S')
	d2 = datetime.strptime(current_time2, '%Y-%m-%d %H:%M:%S')
	message_dic = {
					'remaining' :
					{
						'world_boss_enter_time':current_time1,
						'world_boss_remaining_times':int((d2-d1).total_seconds()),
						'boss1' : "%.2f" %(int(self._boss_life_remaining[0])/int(self._boss_life[0])),
						'boss2' : "%.2f" %(int(self._boss_life_remaining[1])/int(self._boss_life[1])),
						'boss3' : "%.2f" %(int(self._boss_life_remaining[2])/int(self._boss_life[2])),
						"boss4" : "%.2f" %(int(self._boss_life_remaining[3])/int(self._boss_life[3])),
						"boss5" : "%.2f" %(int(self._boss_life_remaining[4])/int(self._boss_life[4])),
						'boss6' : "%.2f" %(int(self._boss_life_remaining[5])/int(self._boss_life[5])),
						'boss7' : "%.2f" %(int(self._boss_life_remaining[6])/int(self._boss_life[6])),
						'boss8' : "%.2f" %(int(self._boss_life_remaining[7])/int(self._boss_life[7])),
						"boss9" : "%.2f" %(int(self._boss_life_remaining[8])/int(self._boss_life[8])),
						"boss10": "%.2f" %(int(self._boss_life_remaining[9])/int(self._boss_life[9]))
					}
				}
	return self._message_typesetting(status=0, message="you get all boss message",data= message_dic)
async def enter_world_boss_stage(uid, wid, pid, **kwargs):
	if self._boss_life_remaining[9]<=0:
		return self._message_typesetting(status=98, message="boss all died")
	data = await self._execute_statement(world,f'select world_boss_enter_time,world_boss_remaining_times from player where unique_id ="{unique_id}"')
	current_time1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	current_time2 = (datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")
	d1 = datetime.strptime(current_time1, '%Y-%m-%d %H:%M:%S')
	d2 = datetime.strptime(current_time2, '%Y-%m-%d %H:%M:%S')
	if data[0][0]=="":
		data = await self._execute_statement_update(world,f'UPDATE player SET world_boss_enter_time ="{current_time1}",world_boss_remaining_times ="{str(self._max_enter_time-1)}" WHERE unique_id = "{unique_id}"')
		message_dic={
			'remaining' :
			{
				"world_boss_enter_time":current_time1,
				'world_boss_remaining_times' : self._max_enter_time-1,
			},
			'reward':
			{
				"world_boss_enter_time": int((d2-d1).total_seconds()),
				'world_boss_remaining_times' : 1
			}
		}
		return self._message_typesetting(status=1, message="enter boss world success, it is first time to enter boss world", data=message_dic)
	else:
		delta_time = datetime.strptime(current_time1, '%Y-%m-%d %H:%M:%S') - datetime.strptime(data[0][0], '%Y-%m-%d %H:%M:%S')
		my_time = int(delta_time.total_seconds()/60/60/24)
		if my_time>=1:
			world_boss_remaining_times = self._max_enter_time
		else:
			world_boss_remaining_times = data[0][1]
		if world_boss_remaining_times-1>=0:
			data = await self._execute_statement_update(world,f'UPDATE player SET world_boss_enter_time ="{current_time1}",world_boss_remaining_times ="{str(int(world_boss_remaining_times)-1)}" WHERE unique_id = "{unique_id}"')
			message_dic={
				'remaining' :
				{
					"world_boss_enter_time":current_time1,
					'world_boss_remaining_times' : world_boss_remaining_times-1,
				},
				'reward':
				{
					"world_boss_enter_time": int((d2-d1).total_seconds()),
					'world_boss_remaining_times' : 1
				}
			}
			return self._message_typesetting(status=0, message="enter bass world success",data = message_dic)
		else:
			return self._message_typesetting(status=99, message="energy is not enough")
async def get_top_damage(uid, wid, **kwargs):
	if range_number<=0:
		return self._message_typesetting(status=98, message="range number should over or equal 1")
	data_leader_board = await self._execute_statement(world,f'SELECT * FROM leader_board ORDER BY world_boss_damage DESC LIMIT {10*(range_number-1)},{10}')
	if len(data_leader_board)==0:
		return self._message_typesetting(status=99, message="no data")
	data_users = await self._execute_statement(world,f'SELECT game_name FROM player where unique_id in {data_leader_board[0][0],data_leader_board[1][0],data_leader_board[2][0],data_leader_board[3][0],data_leader_board[4][0],data_leader_board[5][0],data_leader_board[6][0],data_leader_board[7][0],data_leader_board[8][0],data_leader_board[9][0]} ORDER BY FIELD(unique_id,{data_leader_board[0][0]},{data_leader_board[1][0]},{data_leader_board[2][0]},{data_leader_board[3][0]},{data_leader_board[4][0]},{data_leader_board[5][0]},{data_leader_board[6][0]},{data_leader_board[7][0]},{data_leader_board[8][0]},{data_leader_board[9][0]})')
	message_dic={"remaining":{}, "page" : range_number}
	for index in range(0,len(data_users)):
		message_dic["remaining"].update({index:{data_users[index][0]:data_leader_board[index][2]}})
	return self._message_typesetting(status=0, message="get top "+str(range_number*10)+" damage",data= message_dic)

async def leave_world_boss_stage(uid, wid, **kwargs):
	current_time = time.strftime('%Y-%m-%d', time.localtime())
	return await self._execute_statement_update(world, f'update task set timer="{current_time}", task_value=1 where unique_id="{unique_id}" and task_id={self._task["task_id"]["pass_world_boss"]}')
