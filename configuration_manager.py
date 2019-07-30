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

VERSION = loc() + '/configuration/config_timer_setting.json'

ENEMY_LAYOUT = loc() + '/configuration/client/{}/level_enemy_layouts_config.json'
MONSTER = loc() + '/configuration/client/{}/monster_config.json'

WORLD_DISTRIBUTION = loc() + '/configuration/server/{}/world_distribution.json'
REWARD = loc() + '/configuration/server/{}/stage_reward_config.json'
HANG_REWARD = loc() + '/configuration/server/{}/hang_reward_config.json'
ENTRY_CONSUMABLES = loc() + '/configuration/server/{}/entry_consumables_config.json'
MYSQL_DATA = loc() + '/configuration/server/{}/mysql_data_config.json'
LOTTERY = loc() + '/configuration/server/{}/lottery_config.json'
WEAPON = loc() + '/configuration/server/{}/weapon_config.json'
SKILL = loc() + '/configuration/server/{}/skill_level_up_config.json'
PLAYER = loc() + '/configuration/server/{}/player_config.json'

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
		self._read_entry_consumables_config()
		self._read_world_distribution_config()
		self._read_game_manager_config()

	async def get_server_config_location(self):
		return {'file' : loc() + '/configuration/server/' + self._sv + '/server.conf'}

	async def get_server_version(self):
		return {'version' : self._sv}

	async def get_client_version(self):
		return {'version' : self._cv}

	async def get_entry_consumables_config(self):
		return self._entry_consumables_config

	async def get_game_manager_config(self):
		return self._game_manager_config

	async def get_world_distribution_config(self):
		return self._world_distribution_config

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
		# reward_list = [v for v in (json.load(open(REWARD_LIST.format(self._cv), encoding = 'utf-8'))).values()]
		reward = json.load(open(REWARD.format(self._cv), encoding = 'utf-8'))
		lottery = json.load(open(LOTTERY.format(self._sv), encoding = 'utf-8'))
		weapon = json.load(open(WEAPON.format(self._sv), encoding = 'utf-8'))
		skill = json.load(open(SKILL.format(self._sv), encoding = 'utf-8'))
		player = json.load(open(PLAYER.format(self._sv), encoding = 'utf-8'))
		self._game_manager_config = {'reward' : reward, 'lottery' : lottery, 'weapon' : weapon, 'skill' : skill, 'hang_reward' : self._hang_reward_config,'player':player, 'entry_consumables' : self._entry_consumables_config}

	def _read_level_enemy_layouts_config(self):
		self._level_enemy_layouts_config = json.load(open(ENEMY_LAYOUT.format(self._cv), encoding = 'utf-8'))

	def _read_entry_consumables_config(self):
		self._entry_consumables_config = json.load(open(ENTRY_CONSUMABLES.format(self._cv), encoding = 'utf-8'))

	def _read_monster_config(self):
		self._monster_config = json.load(open(MONSTER.format(self._cv), encoding = 'utf-8'))

	def _read_world_distribution_config(self):
		d = json.load(open(WORLD_DISTRIBUTION.format(self._cv), encoding = 'utf-8'))
		for server in d['servers']:
			d['servers'][server]['worlds'] = self._world_range_parser(d['servers'][server]['worlds'])
		self._world_distribution_config = d

	def _read_stage_reward_config(self):
		self._stage_reward_config = json.load(open(REWARD.format(self._cv), encoding = 'utf-8'))

	def _read_hang_reward_config(self):
		self._hang_reward_config = json.load(open(HANG_REWARD.format(self._cv), encoding = 'utf-8'))

	def _read_mysql_data_config(self):
		self._mysql_data_config = json.load(open(MYSQL_DATA.format(self._sv), encoding = 'utf-8'))

	def _world_range_parser(self, s: str) -> [int]:
		'''
		Parses a valid input sequence into a list containing the specified values.
		A valid input sequence is a single string containing any number of comma separated valid ranges.
		A valid range can be either a single positive number, or a positive number followed by a '-' character,
		followed by an equal or larger number.
		Raises ValueError if input contains non valid characters.

		Examples of valid input:
		'1' -> [1]
		'1, 12-13' -> [1, 12, 13]
		'4-7, 1, 2-3' -> [1, 2, 3, 4, 5, 6, 7]
		'''
		ret = []
		for sequence in s.split(','):
			end = None
			start = None
			is_range = False
			for c in sequence:
				if c in {'0','1','2','3','4','5','6','7','8','9'}:
					if not is_range:
						start = int(c) if start == None else (10 * start) + int(c)
					else:
						end = int(c) if end == None else (10 * end) + int(c)
				elif c == '-':
					is_range = True
				elif c != ' ':
					raise ValueError
			ret.extend([_ for _ in range(start, (start if end == None else end) + 1)])
		return list(set(ret))

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

@ROUTES.get('/get_entry_consumables_config')
async def __get_entry_consumables_config(request: web.Request) -> web.Response:
	return _json_response(await MANAGER.get_entry_consumables_config())

@ROUTES.get('/get_world_distribution_config')
async def __get_world_distribution_config(request: web.Request) -> web.Response:
	return _json_response(await MANAGER.get_world_distribution_config())

def run():
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port=8000)


if __name__ == '__main__':
	run()
