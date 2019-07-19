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
import tormysql
from aiohttp import web
from aiohttp import ClientSession
import os
import time
import threading
import configparser
# Part (1 / 2)


class ConfigurationManager:
	def __init__(self):
		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive.
		self._pool = tormysql.ConnectionPool(
			max_connections=10, host='192.168.1.102', user='root', passwd='lukseun', db='aliya', charset='utf8')
		# client setting
		self.level_enemy_layouts_config = ""
		self.monster_config = ""
		self.stage_reward_config = ""
		# server setting
		self.lottery_conf = configparser.ConfigParser()
		self.server_conf = configparser.ConfigParser()
		self.mysql_data_config = ""
		self.config_timer()
	async def public_method(self) -> None:
		# Something interesting
		# await self._execute_statement('STATEMENT')
		pass

	async def public_method(self) -> None:
		# Something interesting
		# await self._execute_statement('STATEMENT')
		pass

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
	def PythonLocation(self):
		return os.path.dirname(os.path.realpath(__file__))
	async def _get_client_level_enemy_layouts_config(self):
		return self.level_enemy_layouts_config
	async def _get_client_monster_config(self):
		return self.monster_config
	async def _get_client_stage_reward_config(self):
	 	return self.stage_reward_config
	async def _get_server_lottery_conf(self):
	 	return self.lottery_conf
	async def _get_server_server_conf(self):
	 	return self.server_conf
	async def _get_server_mysql_data_config(self):
	 	return self.mysql_data_config
	def set_server_config(self):
		json_content = json.load(open(self.PythonLocation(
		)+"/configuration/config_timer_setting.json", 'r', encoding="UTF-8"))
		time_list = json_content.keys()
		for config_time in time_list:
			my_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
			if my_time >= config_time:
				setting_time = config_time
		version = json_content[setting_time]["client"]

		# client side
		self.level_enemy_layouts_config = json.load(open(self.PythonLocation(
		)+"/configuration/client/"+version+"/level_enemy_layouts_config.json", 'r', encoding="UTF-8"))
		self.monster_config = json.load(open(self.PythonLocation(
		)+"/configuration/client/"+version+"/monster_config.json", 'r', encoding="UTF-8"))
		self.stage_reward_config = json.load(open(self.PythonLocation(
		)+"/configuration/client/"+version+"/stage_reward_config.json", 'r', encoding="UTF-8"))

		# server side
		location  = self.PythonLocation()+"/configuration/server/" + version+"/server.conf"
		self.mysql_data_config = json.load(open(self.PythonLocation(
		)+"/configuration/server/"+version+"/mysql_data_config.json", 'r', encoding="UTF-8"))
		self.server_conf.read(self.PythonLocation()+"/configuration/server/" + version+"/server.conf")
		self.lottery_conf.read(self.PythonLocation()+"/configuration/server/" + version+"/lottery.conf")
	def config_timer(self):
		self.set_server_config()
		timer = threading.Timer(10, self.set_server_config)
		timer.start()


# Part (2 / 2)
# we want to define a single instance of the class
MANAGER = ConfigurationManager()
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


# Defines a function decorator that will require a valid token to be
# presented in the Authorization headers. To make a public facing API call
# required a valid token, put @login_required above the name of the function.
def login_required(fn):
	async def wrapper(request):
		async with ClientSession() as session:
			async with session.get('http://localhost:8080/validate', headers={'authorization': str(request.headers.get('authorization'))}) as resp:
				if resp.status == 200:
					return await fn(request)
		return _json_response({'message': 'You need to be logged in to access this resource'}, status=401)
	return wrapper


# Try running the server and then visiting http://localhost:[PORT]/public_method
@ROUTES.get('/public_method')
async def __public_method(request: web.Request) -> web.Response:
	await MANAGER.public_method()
	return _json_response({'message': 'asyncio code is awesome!'}, status=200)

@ROUTES.get('/protected_method')
@login_required
async def __protected_method(request: web.Request) -> web.Response:
	return _json_response({'message': 'if you can see this, you are logged in!!'})

@ROUTES.post('/_get_client_level_enemy_layouts_config')
async def __get_client_level_enemy_layouts_config(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER._get_client_level_enemy_layouts_config()
	return _json_response(data)

@ROUTES.post('/_get_client_monster_config')
async def _get_client_monster_config(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER._get_client_monster_config()
	return _json_response(data)

@ROUTES.post('/_get_client_stage_reward_config')
async def _get_client_stage_reward_config(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER._get_client_stage_reward_config()
	return _json_response(data)

@ROUTES.post('/_get_server_lottery_conf')
async def _get_server_lottery_conf(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER._get_server_lottery_conf()
	return _json_response(data)

@ROUTES.post('/_get_server_server_conf')
async def _get_server_server_conf(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER._get_server_server_conf()
	return _json_response(data)

@ROUTES.post('/_get_server_mysql_data_config')
async def _get_server_mysql_data_config(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER._get_server_mysql_data_config()
	return _json_response(data)

def run(port):
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port=port)


if __name__ == '__main__':
	run(8002)
