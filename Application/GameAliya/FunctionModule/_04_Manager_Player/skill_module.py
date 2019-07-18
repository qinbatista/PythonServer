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
import json
import random
import tormysql
import configparser
from aiohttp import web
from aiohttp import ClientSession

CONFIG = configparser.ConfigParser()
CONFIG.read('../../Configuration/server/1.0/server.conf')

BAG_BASE_URL = CONFIG['bag_manager']['address'] + ':' + CONFIG['bag_manager']['port']


# Part (1 / 2)
class SkillManager:
	def __init__(self):
		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive. 
		self._pool = tormysql.ConnectionPool(max_connections=10, host='192.168.1.102', user='root', passwd='lukseun', db='aliya', charset='utf8')
	
	async def level_up_skill(self, unique_id: str, skill_id: str, scroll_id: str) -> dict:
		# 0 - Success
		# 1 - User does not have that skill
		# 4 - User does not have enough scrolls
		# 9 - Skill already at max level
		skill_level = await self._get_skill_level(unique_id, skill_id)
		if skill_level == 0:
			return self.message_typesetting(1, 'User does not have that skill')
		if skill_level >= 10:
			return self.message_typesetting(9, 'Skill already max level')

		if self.__class__.__name__ == 'PlayerManager':
			fn = {'skill_scroll_10' : self.try_skill_scroll_10, 'skill_scroll_30' : self.try_skill_scroll_30, 'skill_scroll_100' : self.try_skill_scroll_100}
			f = fn[scroll_id]
			resp = await f(unique_id, -1)
			scroll_quantity = resp['remaining']
		else:
			async with ClientSession() as session:
				async with session.post(BAG_BASE_URL + '/try_'+scroll_id, data = {'unique_id' : unique_id, 'value' : -1}) as resp:
					resp = await resp.json(content_type='text/json')
					if resp['status'] == 1:
						return self.message_typesetting(4, 'User does not have enough scrolls')
					scroll_quantity = resp['remaining']
			
		if not await self._roll_for_upgrade(scroll_id):
			return self.message_typesetting(0, 'success', {'skill1' : [skill_id, skill_level], 'item1' : [scroll_id, scroll_quantity], 'upgrade' : 1})

		await self._execute_statement('UPDATE skill SET `' + skill_id + '` = ' + str(skill_level + 1) + ' WHERE unique_id = "' + unique_id + '";')
		return self.message_typesetting(0, 'success', {'skill1' : [skill_id, skill_level + 1], 'item1' : [scroll_id, scroll_quantity], 'upgrade' : 0})

			

	async def get_all_skill_level(self, unique_id: str) -> dict:
		# 0 - Success
		names = await self._execute_statement('DESCRIBE skill;')
		values = await self._execute_statement('SELECT * from skill WHERE unique_id = "' + str(unique_id) + '";')
		data = {}
		for num, val in enumerate(zip(names[1:], values[0][1:])):
			data['skill' + str(num + 1)] = [ val[0][0] , val[1] ]
		return self.message_typesetting(0, 'success', data)


	async def get_skill(self, unique_id: str, skill_id: str) -> dict:
		# 0 - Success
		# 1 - invalid skill name
		try:
			level = await self._get_skill_level(unique_id, skill_id)
			return self.message_typesetting(0, 'success', {'skill': skill_id, 'value': level})
		except:
			return self.message_typesetting(1, 'invalid skill name')


	async def try_unlock_skill(self, unique_id: str, skill_id: str) -> dict:
		# 0 - success, unlocked new skill
		# 1 - skill already unlocked
		# 2 - invalid skill name
		# json ===> {"status": status, "remaining": remaining} ===> status 0、1、2、3
		table_tuple = ("success, unlocked new skill", "skill already unlocked", "invalid skill name")
		try:  # 0、1、2
			level = await self._get_skill_level(unique_id, skill_id)
			if level == 0 and await self._execute_statement_update('UPDATE skill SET `' + skill_id + '` = 1 WHERE unique_id = "' + unique_id + '";') == 0:
				return self.__internal_format(status=0, remaining=table_tuple)  # success, unlocked new skill
			return self.__internal_format(status=1, remaining=table_tuple)  # skill already unlocked
		except:
			return self.__internal_format(status=2, remaining=table_tuple)  # invalid skill name






			####################################
			#          P R I V A T E		   #
			####################################
		
		
	async def _get_skill_level(self, unique_id: str, skill_id: str) -> int:
		data = await self._execute_statement('SELECT ' + skill_id + ' FROM skill WHERE unique_id = "' + unique_id + '";')
		return int(data[0][0])

	async def _roll_for_upgrade(self, scroll_id: str) -> bool:
		UPGRADE = { 'skill_scroll_10' : 0.10, 'skill_scroll_30' : 0.30, 'skill_scroll_100' : 1 }
		try:
			roll = random.random()
			return roll < UPGRADE[scroll_id]
		except KeyError:
			return False

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

	async def _execute_statement_update(self, statement: str) -> int:
		"""
		Execute the update or set statement and return the result.
		执行update或set语句并返回结果。
		:param statement: Mysql执行的语句
		:return: 返回update或者是set执行的结果
		"""
		async with await self._pool.Connection() as conn:
			async with conn.cursor() as cursor:
				return await cursor.execute(statement)

	def __internal_format(self, status: int, remaining: int or tuple) -> dict:
		"""
		Internal json formatted information
		内部json格式化信息
		:param status:状态标识0：成功，1：失败
		:param remaining:改变后的结果
		:return:json格式：{"status": status, "remaining": remaining}
		"""
		return {"status": status, "remaining": remaining}

	def message_typesetting(self, status: int, message: str, data: dict={}) -> dict:
		return {'status' : status, 'message' : message, 'random' : random.randint(-1000, 1000), 'data' : data}







# Part (2 / 2)
MANAGER = SkillManager()  # we want to define a single instance of the class
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


@ROUTES.post('/level_up_skill')
async def __get_all_skill_level(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.level_up_skill(post['unique_id'], post['skill_id'], post['scroll_id'])
	return _json_response(data)


@ROUTES.post('/get_all_skill_level')
async def __get_all_skill_level(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.get_all_skill_level(post['unique_id'])
	return _json_response(data)


@ROUTES.post('/get_skill')
async def __get_skill(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.get_skill(post['unique_id'], post['skill_id'])
	return _json_response(data)


@ROUTES.post('/try_unlock_skill')
async def __try_unlock_skill(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.try_unlock_skill(post['unique_id'], post['skill_id'])
	return _json_response(data)


def run():
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port=CONFIG.getint('skill_manager', 'port'))


if __name__ == '__main__':
	run()
