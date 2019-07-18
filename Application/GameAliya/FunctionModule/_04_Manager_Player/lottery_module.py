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
SKILL_BASE_URL = CONFIG['skill_manager']['address'] + ':' + CONFIG['skill_manager']['port']
WEAPON_BASE_URL = CONFIG['_01_Manager_Weapon']['address'] + ':' + CONFIG['_01_Manager_Weapon']['port']

SKILL_ID_LIST = ["m1_level", "p1_level", "g1_level", "m11_level", "m12_level", "m13_level", "p11_level", "p12_level", "p13_level", "g11_level", "g12_level", "g13_level", "m111_level", "m112_level", "m113_level", "m121_level", "m122_level", "m123_level", "m131_level", "m132_level", "m133_level", "p111_level", "p112_level", "p113_level", "p121_level", "p122_level", "p123_level", "p131_level", "p132_level", "p133_level", "g111_level", "g112_level", "g113_level", "g121_level", "g122_level", "g123_level", "g131_level", "g132_level", "g133_level"]

# Part (1 / 2)
class LotteryManager:
	def __init__(self):
		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive. 
		self._pool = tormysql.ConnectionPool(max_connections=10, host='192.168.1.102', user='root', passwd='lukseun', db='aliya', charset='utf8')
		self._skill_tier_names = []
		self._skill_tier_weights = []
		self._skill_items = {}
		self._weapon_tier_names = []
		self._weapon_tier_weights = []
		self._weapon_items = {}
		self._read_lottery_configuration()
	

	async def random_gift_skill(self, unique_id: str) -> dict:
		tier_choice = (random.choices(self._skill_tier_names, self._skill_tier_weights))[0]
		gift_skill = (random.choices(self._skill_items[tier_choice]))[0]

		if self.__class__.__name__ == 'PlayerManager':
			resp = await self.try_unlock_skill(unique_id, gift_skill)
			if resp['status'] == 2:
				if tier_choice == 'skilltier1':
					data = await self.try_skill_scroll_10(unique_id, 1)
				elif tier_choice == 'skilltier2':
					data = await self.try_skill_scroll_30(unique_id, 1)
				else:
					data = await self.try_skill_scroll_100(unique_id, 1)
				return self.message_typesetting(1, 'You received a free scroll', data['data'])
			else:
				return resp
		else:
			async with ClientSession() as session:
				async with session.post(SKILL_BASE_URL + '/try_unlock_skill', data = {'unique_id' : unique_id, 'skill_id' : gift_skill}) as resp:
					data = await resp.json(content_type = 'text/json')
				if data['status'] == 2:
					if tier_choice == 'skilltier1':
						async with session.post(BAG_BASE_URL + '/try_skill_scroll_10', data = {'unique_id' : unique_id, 'value' : 1}) as resp:
							resp = await resp.json(content_type = 'text/json')
					elif tier_choice == 'skilltier2':
						async with session.post(BAG_BASE_URL + '/try_skill_scroll_30', data = {'unique_id' : unique_id, 'value' : 1}) as resp:
							resp = await resp.json(content_type = 'text/json')
					else:
						async with session.post(BAG_BASE_URL + '/try_skill_scroll_100', data = {'unique_id' : unique_id, 'value' : 1}) as resp:
							resp = await resp.json(content_type = 'text/json')
					return self.message_typesetting(1, 'you received a free scroll')
				else:
					return data
					

		

	async def random_gift_weapon(self, unique_id: str) -> dict:
		tier_choice = (random.choices(self._weapon_tier_names, self._weapon_tier_weights))[0]
		gift_weapon = (random.choices(self._weapon_items[tier_choice]))[0]
		
		async with ClientSession() as session:
			async with session.post(WEAPON_BASE_URL + '/try_unlock_weapon', data = {'unique_id' : unique_id, 'weapon' : gift_weapon}) as resp:
				return await resp.json(content_type = 'text/json')





			####################################
			#          P R I V A T E		   #
			####################################
		

	def _read_lottery_configuration(self, conf: str = '../../Configuration/server/1.0/lottery.conf'):
		config = configparser.ConfigParser()
		config.read(conf)
		self._skill_tier_names = eval(config['skills']['names'])
		self._skill_tier_weights = eval(config['skills']['weights'])
		self._skill_items = eval(config['skills']['items'])
		self._weapon_tier_names = eval(config['weapons']['names'])
		self._weapon_tier_weights = eval(config['weapons']['weights'])
		self._weapon_items = eval(config['weapons']['items'])


			

		

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
MANAGER = LotteryManager()  # we want to define a single instance of the class
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



@ROUTES.post('/random_gift_skill')
async def __random_gift_segment(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.random_gift_skill(post['unique_id'])
	return _json_response(data)


@ROUTES.post('/random_gift_weapon')
async def __random_gift_segment(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.random_gift_weapon(post['unique_id'])
	return _json_response(data)



def run():
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port=CONFIG.getint('lottery_manager', 'port'))


if __name__ == '__main__':
	run()
