#
# Configuration Manager
#
###############################################################################


import os
import json
import queue
import threading
import time
import configparser
from aiohttp import web
from datetime import datetime
from collections import defaultdict

def loc():
	return os.path.dirname(os.path.realpath(__file__))

VERSION = loc() + '/configuration/config_timer_setting.json'

LOTTERY = loc() + '/configuration/{}/server/lottery.json'
FAMILY = loc() + '/configuration/{}/server/family.json'
FACTORY = loc() + '/configuration/{}/server/factory.json'
WORLD = loc() + '/configuration/{}/server/world.json'

SKILL = loc() + '/configuration/{}/server/skills.json'
WEAPON = loc() + '/configuration/{}/server/weapon_config.json'
ROLE = loc() + '/configuration/{}/server/roles.json'
PLAYER = loc() + '/configuration/{}/server/player.json'
MALL = loc() + '/configuration/{}/server/mall.json'
MONSTER = loc() + '/configuration/{}/client/monster_config.json'
ENEMY_LAYOUT = loc() + '/configuration/{}/client/level_enemy_layouts_config.json'
ENEMY_LAYOUT_TOWER = loc() + '/configuration/{}/client/level_enemy_layouts_config_tower.json'
SERVER_CONFIG = loc() + '/configuration/{}/server/server_config.json'
NOTICE = loc() + '/configuration/{}/notice.json'
PLAYER_EXPERIENCE = loc() + '/configuration/{}/server/player_experience.json'
ACHIEVEMENT= loc() + '/configuration/{}/server/achievement.json'
TASK = loc() + '/configuration/{}/server/task.json'
CHECK_IN = loc() + '/configuration/{}/server/check_in.json'
VIP_CONFIG = loc() + '/configuration/{}/server/vip_config.json'
PACKAGE = loc() + '/configuration/{}/server/package.json'
SUMMON = loc() + '/configuration/{}/server/summon.json'
STAGES = loc() + '/configuration/{}/server/stages.json'
SCIENCES = loc() + '/configuration/{}/server/sciences.json'
MARKETS = loc() + '/configuration/{}/server/markets.json'


class RepeatingTimer(threading.Thread):
	def __init__(self, dt):
		MANAGER.refresh_configs()
		super().__init__(daemon=True)
		self.dt = dt

	def run(self):
		while True:
			time.sleep(self.dt)
			MANAGER.refresh_configs()


class ConfigurationManager:
	def __init__(self):
		self._read_version()
		self._world_map = defaultdict(lambda: defaultdict(dict))

	def refresh_configs(self):
		self._read_version()
		self._read_level_enemy_layouts_config()
		self._read_level_enemy_layouts_config_tower()
		self._read_monster_config()
		self._read_world_distribution_config()
		self._read_factory_config()
		self._read_family_config()
		self._read_mall_config()
		self._read_notice_info()
		self._read_player_experience()
		self._read_achievement_config()
		self._read_task_config()
		self._read_check_in_config()
		self._read_vip_config_config()
		self._read_package_config()
		self._read_summon_config()
		self._read_stages_config()
		self._read_sciences_config()
		self._read_markets_config()

		# read this one last
		self._read_game_manager_config()
		print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}==>refresh success")

	async def get_server_config_location(self):
		return {'file' : loc() + '/configuration/' + self._sv + '/server/server.conf'}

	async def get_server_version(self):
		return {'version' : self._sv}

	async def get_client_version(self):
		return {'version' : self._cv}

	async def get_game_manager_config(self):
		return self._game_manager_config

	async def get_world_map(self):
		return self._world_map or {'status' : 'no one has registered yet'}

	def _read_factory_config(self):
		self._factory_config = json.load(open(FACTORY.format(self._sv), encoding='utf-8'))

	def _read_family_config(self):
		self._family_config = json.load(open(FAMILY.format(self._sv), encoding='utf-8'))

	def _read_mall_config(self):
		self._mall_config = json.load(open(MALL.format(self._sv), encoding='utf-8'))

	def _read_package_config(self):
		self._package = json.load(open(PACKAGE.format(self._sv), encoding='utf-8'))

	def _read_summon_config(self):
		self._summon = json.load(open(SUMMON.format(self._sv), encoding='utf-8'))

	def _read_stages_config(self):
		self._stages = json.load(open(STAGES.format(self._sv), encoding='utf-8'))

	def _read_sciences_config(self):
		self._sciences = json.load(open(SCIENCES.format(self._sv), encoding='utf-8'))

	def _read_markets_config(self):
		self._markets = json.load(open(MARKETS.format(self._sv), encoding='utf-8'))

	def _read_game_manager_config(self):
		lottery = json.load(open(LOTTERY.format(self._sv), encoding = 'utf-8'))
		weapon = json.load(open(WEAPON.format(self._sv), encoding = 'utf-8'))
		role = json.load(open(ROLE.format(self._sv), encoding = 'utf-8'))
		skill = json.load(open(SKILL.format(self._sv), encoding = 'utf-8'))
		player = json.load(open(PLAYER.format(self._sv), encoding = 'utf-8'))
		world = json.load(open(WORLD.format(self._sv), encoding = 'utf-8'))
		self._game_manager_config = {
			'lottery' : lottery, 'weapon' : weapon, 'role' : role,
			'skill' : skill, 'player' : player, 'sciences': self._sciences,
			"factory": self._factory_config, 'family': self._family_config,
			"mall": self._mall_config, "notice": self._notice_info,
			'player_experience': self._player_experience, 'monster': self._monster,
			'level_enemy_layouts': self._level_enemy_layouts_config,
			'level_enemy_layouts_tower': self._level_enemy_layouts_config_tower,
			'achievement': self._achievement, 'task': self._tasks,
			'check_in': self._check_in, 'vip': self._vips,
			'world' : world, 'version': self._sv, 'package': self._package,
			'summon': self._summon, 'stages': self._stages, 'markets': self._markets
		}

	def _read_level_enemy_layouts_config(self):
		self._level_enemy_layouts_config = json.load(open(ENEMY_LAYOUT.format(self._cv), encoding = 'utf-8'))

	def _read_level_enemy_layouts_config_tower(self):
		self._level_enemy_layouts_config_tower = json.load(open(ENEMY_LAYOUT_TOWER.format(self._cv), encoding = 'utf-8'))

	def _read_notice_info(self):
		self._notice_info = json.load(open(NOTICE.format(self._cv), encoding = 'utf-8'))

	def _read_player_experience(self):
		self._player_experience = json.load(open(PLAYER_EXPERIENCE.format(self._sv), encoding = 'utf-8'))

	def _read_monster_config(self):
		self._monster = json.load(open(MONSTER.format(self._cv), encoding = 'utf-8'))

	def _read_achievement_config(self):
		self._achievement = json.load(open(ACHIEVEMENT.format(self._cv), encoding = 'utf-8'))

	def _read_task_config(self):
		self._tasks = json.load(open(TASK.format(self._sv), encoding = 'utf-8'))

	def _read_check_in_config(self):
		self._check_in = json.load(open(CHECK_IN.format(self._sv), encoding = 'utf-8'))

	def _read_vip_config_config(self):
		self._vips = json.load(open(VIP_CONFIG.format(self._sv), encoding = 'utf-8'))

	def _read_world_distribution_config(self):
		d = json.load(open(SERVER_CONFIG.format(self._cv), encoding = 'utf-8'))
		self._unregistered_chat_servers = queue.Queue()
		self._unregistered_game_managers = queue.Queue()
		for sid, value in d['gamemanager']['servers'].items():
			value['worlds'] = self._world_range_parser(value['worlds'])
			for world in value['worlds']:
				self._unregistered_chat_servers.put(world)
			if len(value['worlds']) == 0:
				self._unregistered_chat_servers.put('test')
			self._unregistered_game_managers.put(sid)
		self._world_distribution_config = d

	def _world_range_parser(self, s: str) -> [int]:
		'''
		'1' -> [1]
		'1, 12-13' -> [1, 12, 13]
		'4-7, 1, 2-3' -> [4, 5, 6, 7, 1, 2, 3]
		'''
		ret = []
		if s == '' or s is None: return ret
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


# Part (2 / 2)
# we want to define a single instance of the class
MANAGER = ConfigurationManager()
ROUTES = web.RouteTableDef()


# Call this method whenever you return from any of the following functions.
# This makes it very easy to construct a json response back to the caller.
def _json_response(body: dict = {}, **kwargs) -> web.Response:
	'''
	A simple wrapper for aiohttp.web.Response return value.
	'''
	kwargs['body'] = json.dumps(body or kwargs['kwargs']).encode('utf-8')
	kwargs['content_type'] = 'text/json'
	return web.Response(**kwargs)



@ROUTES.get('/get_game_manager_config')
async def __get_game_manager_config(request: web.Request) -> web.Response:
	return _json_response(await MANAGER.get_game_manager_config())

@ROUTES.get('/get_server_version')
async def __get_server_version(request: web.Request) -> web.Response:
	return _json_response(await MANAGER.get_server_version())

@ROUTES.get('/get_client_version')
async def __get_client_version(request: web.Request) -> web.Response:
	return _json_response(await MANAGER.get_client_version())

@ROUTES.get('/get_server_config_location')
async def __get_server_config_location(request: web.Request) -> web.Response:
	return _json_response(await MANAGER.get_server_config_location())

@ROUTES.get('/get_world_map')
async def __get_world_map(request: web.Request) -> web.Response:
	return _json_response(await MANAGER.get_world_map())


def start_timer(seconds: int):
	t = RepeatingTimer(seconds)
	t.start()


def run():
	start_timer(600)
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port=8000)


if __name__ == '__main__':
	run()
