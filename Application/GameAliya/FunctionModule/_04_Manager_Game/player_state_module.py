#
# An example for an SQL manager server using asyncio programming methods.
# We will use aiohttp library to network these API calls so that they can be
# accessed from different physical devices on the network.
# Additionally, we will be using tormysql library to manage the SQL server pool
# of connections.
#
# All functions that connect to the database should be async. The more async code
# we use, the faster the entire server becomes.
#
#
# The file has two parts:
#	- The DefaultManager class
#	- The aiohttp server bindings for the class methods
#
###############################################################################


# Some safe default includes. Feel free to add more if you need.
import time
from datetime import datetime, timedelta
import json
import random
import tormysql
import configparser
from aiohttp import web
from aiohttp import ClientSession

CONFIG = configparser.ConfigParser()
CONFIG.read('../../Configuration/server/1.0/server.conf')
BAG_BASE_URL = CONFIG['bag_manager']['address'] + CONFIG['bag_manager']['port']


# Part (1 / 2)
class PlayerStateManager:
	def __init__(self):
		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive. 
		self._pool = tormysql.ConnectionPool(max_connections=10, host=CONFIG['database']['ip'], user='root', passwd='lukseun', db='aliya', charset='utf8')
		self._recover_time = CONFIG.getint("player_state_manager", "recover_time")  # 10分钟恢复一点体力
		self._full_energy = CONFIG.getint("player_state_manager", "full_energy")

	async def try_energy(self, unique_id: str, amount: int) -> dict:  # amount > 0
		# success ===> 0 , 1 , 2 , 3 , 4 , 5
		# - 0 - 获取能量成功 === Get energy successfully
		# - 1 - 能量已消耗，能量值及恢复时间更新成功 === Energy has been consumed, energy value and recovery time updated successfully
		# - 2 - 能量已完全恢复，能量更新成功 === Energy has been fully restored, successful energy update
		# - 3 - 能量尚未完全恢复，能量更新成功 === Energy has not fully recovered, successful energy update
		# - 4 - 能量刷新后已消耗，能量值及恢复时间更新成功 === After refreshing the energy, the energy value and recovery time are successfully updated.
		# - 5 - 能量已刷新，未恢复满，已消耗能量，能量值及恢复时间更新成功 === Energy has been refreshed, not fully recovered, energy has been consumed, energy value and recovery time updated successfully
		# - 6 - 参数错误 === Parameter error
		# - 7 - 无足够能量消耗 === Not enough energy consumption
		if amount < 0 or amount > self._full_energy:
			return self.message_typesetting(status=6, message="Parameter error")
		return await self._decrease_energy(unique_id=unique_id, amount=amount)

			####################################
			#          P R I V A T E		   #
			####################################
	async def _decrease_energy(self, unique_id: str, amount: int) -> dict:
		current_energy, recover_time = await self._get_energy_information(unique_id)
		current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		if recover_time == '':  # 此时 current_energy == self._full_energy 成立
			if amount == 0:  # 成功1：如果没有恢复时间且是获取能量值，则直接拿取数据库的值给客户端
				return self.message_typesetting(status=0, message='Get energy successfully', data={"keys": ['energy', 'recover_time'], "values": [current_energy, recover_time]})
			current_energy -= amount
			# 成功2：如果没有恢复时间且是消耗能量值，则直接用数据库的值减去消耗的能量值，
			# 然后存入消耗之后的能量值，以及将当前的时间存入 恢复时间项
			await self._execute_statement('UPDATE player SET energy = ' + str(current_energy) + ', recover_time = "' + current_time + '" WHERE unique_id = "' + unique_id + '";')
			return self.message_typesetting(1, 'Energy has been consumed, energy value and recovery time updated successfully', {"keys": ['energy', 'recover_time'], "values": [current_energy, current_time]})
		else:
			delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S')
			recovered_energy = delta_time.seconds // 60 // self._recover_time
			if amount == 0:
				# 成功3：如果有恢复时间且是获取能量值，则加上获取的能量值，并判断能量值是否满足上限
				# - 1 - 满足上限的情况：直接将满能量值和空字符串分别存入能量值项和恢复时间项
				# - 2 - 不满足上限的情况：将能恢复的能量值计算出来，并且计算恢复后的能量值current_energy
				#       和恢复时间与恢复能量消耗的时间相减的恢复时间值
				if current_energy + recovered_energy >= self._full_energy:
					recover_time, current_energy = "", self._full_energy
					await self._execute_statement('UPDATE player SET energy = ' + str(current_energy) + ', recover_time = "' + recover_time + '" WHERE unique_id = "' + unique_id + '";')
					return self.message_typesetting(status=2, message='Energy has been fully restored, successful energy update', data={"keys": ['energy', 'recover_time'], "values": [current_energy, recover_time]})
				else:
					recover_time, current_energy = (datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=recovered_energy * self._recover_time)).strftime("%Y-%m-%d %H:%M:%S"), current_energy + recovered_energy
					await self._execute_statement('UPDATE player SET energy = ' + str(current_energy) + ', recover_time = "' + recover_time + '" WHERE unique_id = "' + unique_id + '";')
					return self.message_typesetting(status=3, message='Energy has not fully recovered, successful energy update', data={"keys": ['energy', 'recover_time'], "values": [current_energy, recover_time]})
				# recover_time, current_energy = ("", self._full_energy) if (current_energy + recovered_energy >= self._full_energy) else ((datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=recovered_energy * self._recover_time)).strftime("%Y-%m-%d %H:%M:%S"), current_energy + recovered_energy)
				# await self._execute_statement('UPDATE player SET energy = ' + str(current_energy) + ', recover_time = "' + recover_time + '" WHERE unique_id = "' + unique_id + '";')
				# return self.message_typesetting(status=0, message='Energy has been recovered and energy is successfully acquired', data={"keys": ['energy', 'recover_time'], "values": [current_energy, recover_time]})
			if recovered_energy + current_energy >= self._full_energy:
				# 成功4：如果有恢复时间且是消耗能量
				# 满足上限的情况是用上限能量值减去要消耗的能量值，然后设置减去之后的能量值和当前的时间分别存入能量值项和恢复时间项
				current_energy = self._full_energy - amount
				await self._execute_statement('UPDATE player SET energy = ' + str(current_energy) + ', recover_time = "' + current_time + '" WHERE unique_id = "' + unique_id + '";')
				return self.message_typesetting(4, 'After refreshing the energy, the energy value and recovery time are successfully updated.', {"keys": ['energy', 'recover_time'], "values": [current_energy, current_time]})
			elif recovered_energy + current_energy - amount >= 0:
				# 成功5：如果有恢复时间且是消耗能量
				# 不满足上限的情况是用当前数据库的能量值和当前恢复的能量值相加然后减去消耗的能量值为要存入数据库的能量值项
				# 数据库中的恢复时间与恢复能量消耗的时间相减的恢复时间值存入到数据库的恢复时间项
				current_energy = recovered_energy + current_energy - amount
				recover_time = (datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=recovered_energy * self._recover_time)).strftime("%Y-%m-%d %H:%M:%S")
				await self._execute_statement('UPDATE player SET energy = ' + str(current_energy) + ', recover_time = "' + recover_time + '" WHERE unique_id = "' + unique_id + '";')
				return self.message_typesetting(5, 'Energy has been refreshed, not fully recovered, energy has been consumed, energy value and recovery time updated successfully', {"keys": ['energy', 'recover_time'], "values": [current_energy, recover_time]})
			else:  # 发生的情况是当前能量值和恢复能量值相加比需要消耗的能量值少
				return self.message_typesetting(status=7, message="Not enough energy consumption")






	async def _get_energy_information(self, unique_id: str) -> (int, str):
		data = await self._execute_statement('SELECT energy, recover_time FROM player WHERE unique_id = "' + unique_id + '";')
		return int(data[0][0]), data[0][1]



	# It is helpful to define a private method that you can simply pass
	# an SQL command as a string and it will execute. Call this method
	# whenever you issue an SQL statement.
	async def _execute_statement(self, statement: str) -> tuple:
		'''
		Executes the given statement and returns the result.
		'''
		async with await self._pool.Connection() as conn:
			async with conn.cursor() as cursor:
				await cursor.execute(statement)
				data = cursor.fetchall()
				return data

	def message_typesetting(self, status: int, message: str, data: dict={}) -> dict:
		return {'status' : status, 'message' : message, 'random' : random.randint(-1000, 1000), 'data' : data}







# Part (2 / 2)
MANAGER = PlayerStateManager()  # we want to define a single instance of the class
ROUTES = web.RouteTableDef()


# Call this method whenever you return from any of the following functions.
# This makes it very easy to construct a json response back to the caller.
def _json_response(body: dict = '', **kwargs) -> web.Response:
	'''
	A simple wrapper for aiohttp.web.Response return value.
	'''
	kwargs['body'] = json.dumps(body or kwargs['kwargs']).encode('utf-8')
	kwargs['content_type'] = 'text/json'
	return web.Response(**kwargs)


@ROUTES.post('/try_energy')
async def __decrease_energy(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.try_energy(post['unique_id'], int(post['amount']))
	return _json_response(data)



def run():
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port=CONFIG.getint('player_state_manager', 'port'))


if __name__ == '__main__':
	run()
