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
from datetime import datetime
import json
import random
import tormysql
import configparser
from aiohttp import web
from aiohttp import ClientSession

CONFIG = configparser.ConfigParser()
CONFIG.read('../../Configuration/server.conf')

BAG_BASE_URL = 'http://localhost:' + CONFIG['bag_manager']['port']


# Part (1 / 2)
class PlayerStateManager:
	def __init__(self):
		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive. 
		self._pool = tormysql.ConnectionPool(max_connections=10, host=CONFIG['database']['ip'], user='root', passwd='lukseun', db='aliya', charset='utf8')
		self._recover_time = 30
		self._full_energy = 10
	

	async def try_energy(self, unique_id: str, amount: int) -> dict:
		if amount > 0:
			return await self._decrease_energy(unique_id, -1 * amount)
		elif amount < 0:
			return await self._decrease_energy(unique_id, amount)
		else:
			energy, last_time = await self._get_energy_information(unique_id)
			return self.message_typesetting(0, 'success', {'energy' : energy, 'recover_time' : last_time})


			####################################
			#          P R I V A T E		   #
			####################################
	async def _decrease_energy(self, unique_id: str, amount: int) -> dict:
		current_energy, recover_time = await self._get_energy_information(unique_id)
		if recover_time == '':
			if current_energy - amount > self._full_energy:
				await self._execute_statement('UPDATE player SET energy = "' + str(current_energy - amount) + '", recover_time = "" WHERE unique_id = "' + unique_id + '";')
				return self.message_typesetting(0, 'decrease success, remaining energy is over full energy, removed recover time', {'energy' : current_energy - amount})
			elif current_energy - amount == self._full_energy:
				await self._execute_statement('UPDATE player SET energy = "' + str(current_energy - amount) + '", recover_time = "' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '" WHERE unique_id = "' + unique_id + '";')
				return self.message_typesetting(0, 'decrease success, remaining energy full, recovering energy', {'energy' : current_energy - amount})
			else:
				await self._execute_statement('UPDATE player SET energy = "' + str(current_energy - amount) + '", recover_time = "' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '" WHERE unique_id = "' + unique_id + '";')
				return self.message_typesetting(0, 'decrease success, start recovering energy', {'energy' : current - amount})
		else:
			delta_time = datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), '%Y-%m-%d %H:%M:%S') - datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S')
			recovered_energy = int(delta_time.seconds / 60 / 20)
			if recovered_energy + current_energy - amount >= 0:
				if recovered_energy + current_energy - amount > 10:
					await self._execute_statement('UPDATE player SET energy = "' + str(10 - amount) + '", recover_time = "" WHERE unique_id = "' + unique_id + '";')
					return self.message_typesetting(0, 'energy over full energy, remove record time', {'energy' : 10 - amount})
				else:
					await self._execute_statement('UPDATE player SET energy = "' + str(recovered_energy + current_energy - amount) + '", recover_time = "' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '" WHERE unique_id = "' + unique_id + '";')
					return self.message_typesetting(0, 'success, recovering energy', {'energy' : recovered_energy + current_energy - amount})
		return self.message_typesetting(1, 'energy error')






	async def _get_energy_information(self, unique_id: str) -> tuple:
		data = await self._execute_statement('SELECT energy, recover_time FROM player WHERE unique_id = "' + unique_id + '";')
		return (data[0][0], data[0][1])
		
		

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
def _json_response(body: str = '', **kwargs) -> web.Response:
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
