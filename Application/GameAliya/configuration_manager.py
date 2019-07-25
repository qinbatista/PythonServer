#
# Configuration Manager
#
###############################################################################


import os
import json
import threading
import configparser
from aiohttp import web
from datetime import datetime

def loc():
	return os.path.dirname(os.path.realpath(__file__))

VERSION = loc() + '/Configuration/config_timer_setting.json'

MONSTER = loc() + '/Configuration/client/{}/monster_config.json'
REWARD_LIST = loc() + '/Configuration/client/{}/stage_reward_config.json'
ENEMY_LAYOUT = loc() + '/Configuration/client/{}/level_enemy_layouts_config.json'
HANG_REWARD = loc() + '/Configuration/client/{}/hang_reward_config.json'


MYSQL_DATA = loc() + '/Configuration/server/{}/mysql_data_config.json'
LOTTERY = loc() + '/Configuration/server/{}/lottery.json'
WEAPON = loc() + '/Configuration/server/{}/weapon.json'
SKILL = loc() + '/Configuration/server/{}/skill.json'

class ConfigurationManager:
	def __init__(self):
		self._read_version()
		self._refresh_configurations()
		self._start_timer(600)


	def _refresh_configurations(self):
		self._read_version()
		self._read_level_enemy_layouts_config()
		self._read_monster_config()
		self._read_stage_reward_config()
		self._read_hang_reward_config()
		self._read_mysql_data_config()
		self._read_game_manager_config()
	

	async def get_server_config_location(self):
		return {'file' : loc() + '/Configuration/server/' + self._sv + '/server.conf'}

	async def get_server_version(self):
		return {'version' : self._sv}

	async def get_client_version(self):
		return {'version' : self._cv}

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
		reward_list = [v for v in (json.load(open(REWARD_LIST.format(self._cv), encoding = 'utf-8'))).values()]
		lottery = json.load(open(LOTTERY.format(self._sv), encoding = 'utf-8'))
		weapon = json.load(open(WEAPON.format(self._sv), encoding = 'utf-8'))
		skill = json.load(open(SKILL.format(self._sv), encoding = 'utf-8'))
		self._game_manager_config = {'reward_list' : reward_list, 'lottery' : lottery, 'weapon' : weapon, 'skill' : skill, 'hang_reward' : self._hang_reward_config}

	def _read_level_enemy_layouts_config(self):
		self._level_enemy_layouts_config = json.load(open(ENEMY_LAYOUT.format(self._cv), encoding = 'utf-8'))

	def _read_monster_config(self):
		self._monster_config = json.load(open(MONSTER.format(self._cv), encoding = 'utf-8'))

	def _read_stage_reward_config(self):
		self._stage_reward_config = json.load(open(REWARD_LIST.format(self._cv), encoding = 'utf-8'))

	def _read_hang_reward_config(self):
		d = json.load(open(HANG_REWARD.format(self._cv), encoding = 'utf-8'))
		self._hang_reward_config = [v for v in d.values()]

	def _read_mysql_data_config(self):
		self._mysql_data_config = json.load(open(MYSQL_DATA.format(self._sv), encoding = 'utf-8'))

	def _read_version(self):
		version = json.load(open(VERSION, encoding = 'utf-8'))
		today = datetime.today()
		for date in version.keys():
			if today > datetime.strptime(date, '%Y-%m-%d'):
				most_recent = date
		self._cv = version[most_recent]['client']
		self._sv = version[most_recent]['server']



	def _start_timer(self, seconds: int):
		t = threading.Timer(seconds, self._refresh_configurations)
		t.daemon = True
		t.start()



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

@ROUTES.get('/get_server_version')
async def __get_server_version(request: web.Request) -> web.Response:
	return _json_response(await MANAGER.get_server_version())

@ROUTES.get('/get_client_version')
async def __get_client_version(request: web.Request) -> web.Response:
	return _json_response(await MANAGER.get_client_version())

@ROUTES.get('/get_server_config_location')
async def __get_server_config_location(request: web.Request) -> web.Response:
	return _json_response(await MANAGER.get_server_config_location())




def run():
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port=8000)


if __name__ == '__main__':
	run()
