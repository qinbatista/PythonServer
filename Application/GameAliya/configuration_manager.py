#
# Configuration Manager
#
###############################################################################


import json
import threading
import configparser
from aiohttp import web

SERVER_CONFIG = './Configuration/server/1.0/server.conf'

MONSTER = './Configuration/client/1.0/monster_config.json'
REWARD_LIST = './Configuration/client/1.0/stage_reward_config.json'
ENEMY_LAYOUT = './Configuration/client/1.0/level_enemy_layouts_config.json'
HANG_REWARD = './Configuration/client/1.0/hang_reward_config.json'


MYSQL_DATA = './Configuration/server/1.0/mysql_data_config.json'
LOTTERY = './Configuration/server/1.0/lottery.json'
WEAPON = './Configuration/server/1.0/weapon.json'
SKILL = './Configuration/server/1.0/skill.json'

class ConfigurationManager:
	def __init__(self):
		self._refresh_configurations()
		self._start_timer(600)


	def _refresh_configurations(self):
		self._read_game_manager_config()
		self._read_level_enemy_layouts_config()
		self._read_monster_config()
		self._read_stage_reward_config()
		self._read_hang_reward_config()
		self._read_mysql_data_config()
	
	async def get_game_manager_config(self):
		return self._game_manager_config

	async def get_level_enemy_layouts_config(self):
		return self._level_enemy_layouts_config

	async def get_monster_config(self):
		return self._monster_config

	async def get_stage_reward_config(self):
		return self._stage_reward_config

	async def get_hang_reward_config(self):
		return self._hang_reward_config

	async def get_mysql_data_config(self):
		return self._mysql_data_config

	def _read_game_manager_config(self):
		reward_list = [v for v in (json.load(open(REWARD_LIST, encoding = 'utf-8'))).values()]
		lottery = json.load(open(LOTTERY, encoding = 'utf-8'))
		weapon = json.load(open(WEAPON, encoding = 'utf-8'))
		skill = json.load(open(SKILL, encoding = 'utf-8'))
		self._game_manager_config = {'reward_list' : reward_list, 'lottery' : lottery, 'weapon' : weapon, 'skill' : skill}

	def _read_level_enemy_layouts_config(self):
		self._level_enemy_layouts_config = json.load(open(ENEMY_LAYOUT, encoding = 'utf-8'))

	def _read_monster_config(self):
		self._monster_config = json.load(open(MONSTER, encoding = 'utf-8'))

	def _read_stage_reward_config(self):
		self._stage_reward_config = json.load(open(REWARD_LIST, encoding = 'utf-8'))

	def _read_hang_reward_config(self):
		self._hang_reward_config = json.load(open(HANG_REWARD, encoding = 'utf-8'))

	def _read_mysql_data_config(self):
		self._mysql_data_config = json.load(open(MYSQL_DATA, encoding = 'utf-8'))

	def _start_timer(self, seconds: int):
		threading.Timer(seconds, self._refresh_configurations).start()



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



@ROUTES.get('/get_game_manager_config')
async def __get_game_manager_config(request: web.Request) -> web.Response:
	return _json_response(await MANAGER.get_game_manager_config())

@ROUTES.get('/get_level_enemy_layouts_config')
async def __get_level_enemy_layouts_config(request: web.Request) -> web.Response:
	return _json_response(await MANAGER.get_level_enemy_layouts_config())

@ROUTES.get('/get_monster_config')
async def __get_monster_config(request: web.Request) -> web.Response:
	return _json_response(await MANAGER.get_monster_config())

@ROUTES.get('/get_stage_reward_config')
async def __get_stage_reward_config(request: web.Request) -> web.Response:
	return _json_response(await MANAGER.get_stage_reward_config())

@ROUTES.get('/get_hang_reward_config')
async def __get_hang_reward_config(request: web.Request) -> web.Response:
	return _json_response(await MANAGER.get_hang_reward_config())

@ROUTES.get('/get_mysql_data_config')
async def __get_mysql_data_config(request: web.Request) -> web.Response:
	return _json_response(await MANAGER.get_mysql_data_config())


def run():
	app = web.Application()
	app.add_routes(ROUTES)
	server_config = configparser.ConfigParser()
	server_config.read(SERVER_CONFIG)
	web.run_app(app, port=server_config.getint('configuration_manager', 'port'))


if __name__ == '__main__':
	run()
