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
		self.Path = os.path.dirname(os.path.realpath(__file__))

		# client setting
		self.level_enemy_layouts_config = ""
		self.monster_config = ""

		# server setting
		self.entry_consumables_config = ""
		self.hang_reward_config = ""
		self.lottery = ""
		self.mysql_data_config = ""
		self.player_setting = ""
		self.server_conf = configparser.ConfigParser()
		self.skill_level_up = ""
		self.stage_reward_config = ""
		self.weapon = ""

		#timer setting
		self.config_timer()
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

	async def _get_client_level_enemy_layouts_config(self) -> object:
		'''
		return enemy layouts config, this config contain where monster come from, how many waves,
		how lang to generate time
		'''
		return self.level_enemy_layouts_config

	async def _get_client_monster_config(self) -> object:
		'''
		return all the monsters' configuration, such as hp, mp, attchk and so on
		'''
		return self.monster_config

	async def _get_server_stage_reward_config(self) -> object:
		'''
		return a result of all reward of stages, so users can get different resource after we change server
		'''
		return self.stage_reward_config

	async def _get_server_entry_consumables_config(self) -> object:
		'''
		return a result of all cost of enter stage
		'''
		return self.entry_consumables_config

	async def _get_server_hang_reward_config(self) -> object:
		'''
		get all hang up reward info
		'''
		return self.hang_reward_config

	async def _get_server_lottery_conf(self) -> object:
		'''
		get all lottery info
		'''
		return self.lottery

	async def _get_server_player_config(self) -> object:
		'''
		there have some functions need to know talbe detal info in our server, give detail when request
		'''
		return self.player_setting_config

	async def _get_server_skill_level_up_config(self) -> object:
		'''
		there have some functions need to know talbe detal info in our server, give detail when request
		'''
		return self.skill_level_up

	async def _get_server_stage_reward_config(self) -> object:
		'''
		there have some functions need to know talbe detal info in our server, give detail when request
		'''
		return self.stage_reward_config

	async def _get_server_weapon_config(self) -> object:
		'''
		there have some functions need to know talbe detal info in our server, give detail when request
		'''
		return self.weapon

	async def _get_server_server_config(self) -> object:
		'''
		get server config, those config include server's ip address, how many server want to create and what's game setting
		'''
		return self.server_conf

	def set_server_config(self):
		"""
		read all config in memory, it will be excute in every 10 mins
		"""
		json_content = json.load(open(self.Path+"/configuration/config_timer_setting.json", 'r', encoding="UTF-8"))
		time_list = json_content.keys()
		for config_time in time_list:
			my_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
			if my_time >= config_time:
				setting_time = config_time
		version = json_content[setting_time]["client"]

		# client side
		self.level_enemy_layouts_config = json.load(open(self.Path+"/configuration/client/"+version+"/level_enemy_layouts_config.json", 'r', encoding="UTF-8"))
		self.monster_config = json.load(open(self.Path+"/configuration/client/"+version+"/monster_config.json", 'r', encoding="UTF-8"))

		# server side
		self.entry_consumables_config = json.load(open(self.Path+"/configuration/server/"+version+"/entry_consumables_config.json", 'r', encoding="UTF-8"))
		self.hang_reward_config = json.load(open(self.Path+"/configuration/server/"+version+"/hang_reward_config.json", 'r', encoding="UTF-8"))
		self.lottery = json.load(open(self.Path+"/configuration/server/"+version+"/lottery.py", 'r', encoding="UTF-8"))
		self.player_setting = json.load(open(self.Path+"/configuration/server/"+version+"/player_setting.json", 'r', encoding="UTF-8"))
		location  = self.Path+"/configuration/server/" + version+"/server.conf"
		self.skill_level_up = json.load(open(self.Path+"/configuration/server/"+version+"/skill_level_up.json", 'r', encoding="UTF-8"))
		self.stage_reward_config = json.load(open(self.Path+"/configuration/server/"+version+"/stage_reward_config.json", 'r', encoding="UTF-8"))
		self.weapon = json.load(open(self.Path+"/configuration/server/"+version+"/weapon.json", 'r', encoding="UTF-8"))

	def config_timer(self):
		"""
		server will refresh configration every 10 mins
		"""
		self.set_server_config()
		timer = threading.Timer(600, self.set_server_config)
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

@ROUTES.post('/_get_server_entry_consumables_config')
async def _get_server_entry_consumables_config(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER._get_server_entry_consumables_config()
	return _json_response(data)

@ROUTES.post('/_get_server_hang_reward_config')
async def _get_server_hang_reward_config(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER._get_server_hang_reward_config()
	return _json_response(data)

@ROUTES.post('/_get_server_lottery_conf')
async def _get_server_lottery_conf(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER._get_server_lottery_conf()
	return _json_response(data)

@ROUTES.post('/_get_server_player_config')
async def _get_server_player_config(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER._get_server_player_config()
	return _json_response(data)

@ROUTES.post('/_get_server_server_conf')
async def _get_server_server_conf(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER._get_server_server_conf()
	return _json_response(data)

@ROUTES.post('/_get_server_skill_level_up_config')
async def _get_server_skill_level_up_config(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER._get_server_skill_level_up_config()
	return _json_response(data)

@ROUTES.post('/_get_server_stage_reward_config')
async def _get_server_stage_reward_config(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER._get_server_stage_reward_config()
	return _json_response(data)

@ROUTES.post('/_get_server_weapon_config')
async def _get_server_weapon_config(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER._get_server_weapon_config()
	return _json_response(data)


def run(port):
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port=port)


if __name__ == '__main__':
	run(port=8002)
