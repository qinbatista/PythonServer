'''
worker_resources.py

A group of resources used by workers.
Provides a centralized location for instantiating frequently used connections
such as mysql connection pools.

The worker provides these resources to the message handler.
'''

import time
import aiohttp
import aioredis
import aiomysql
import requests
import threading

from datetime import datetime, timezone

class WorkerResources:
	def __init__(self, redis_addr, db_addr, db_user, db_pw):
		self.redis_addr = redis_addr
		self.db_addr = db_addr
		self.db_user = db_user
		self.db_pw = db_pw

		self.resources = {}

	async def init(self):
		self.resources['session']   = aiohttp.ClientSession()
		self.resources['redis']     = await aioredis.create_redis(f'redis://{self.redis_addr}')
		self.resources['db']        = await aiomysql.create_pool(maxsize = 10, host = self.db_addr, \
				user = self.db_user, password = self.db_pw, charset = 'utf8', autocommit = True)
		self.resources['accountdb'] = await aiomysql.create_pool(maxsize =  4, host = self.db_addr,  \
				user = self.db_user, password = self.db_pw, charset = 'utf8', autocommit = True, db = 'user')
		self.resources['malldb'] = await aiomysql.create_pool(maxsize = 4, host = self.db_addr, \
				user = self.db_user, password = self.db_pw, charset = 'utf8', autocommit = True, db = 'mall')
		self.resources['exchangedb'] = await aiomysql.create_pool(maxsize = 4, host = self.db_addr, \
				user = self.db_user, password = self.db_pw, charset = 'utf8', autocommit = True, db = 'exchange')


	async def shutdown(self):
		self.resources['db'].close()
		await self.resources['db'].wait_closed()

		self.resources['accountdb'].close()
		await self.resources['accountdb'].wait_closed()

		self.resources['malldb'].close()
		await self.resources['malldb'].wait_closed()

		self.resources['exchangedb'].close()
		await self.resources['exchangedb'].wait_closed()

		await self.resources['session'].close()


	def __getitem__(self, key):
		return self.resources[key]


class RepeatingTimer(threading.Thread):
	def __init__(self, dt, fn, *args, **kwargs):
		super().__init__(daemon = True)
		self.dt     = dt
		self.fn     = fn
		self.args   = args
		self.kwargs = kwargs
	
	def run(self):
		while True:
			print(f'sleeping for {self.dt} seconds...')
			time.sleep(self.dt)
			self.fn(*self.args, **self.kwargs)


class ModuleConfigurations:
	def __init__(self, config_addr, config_port):
		self.configs = {}
		self.baseurl = f'http://{config_addr}:{config_port}'
		self.repeat  = RepeatingTimer(600, self.refresh, refresh_world_boss = False)
		self.repeat.start()
		self.refresh()
	
	def refresh(self, *, refresh_world_boss = True, already_refreshed_world_boss = False):
		r = requests.get(self.baseurl + '/get_game_manager_config')
		self.configs['lottery']           = r.json()['lottery']
		self.configs['family']            = r.json()['family']
		self.configs['factory']           = r.json()['factory']
		self.configs['world']             = r.json()['world']
		self.configs['weapon']            = r.json()['weapon']
		self.configs['skill']             = r.json()['skill']
		self.configs['role']              = r.json()['role']
		self.configs['package']           = r.json()['package']
		self.configs['vip']               = r.json()['vip']
		self.configs['exp']               = r.json()['player_experience']
		self.configs['mall']              = r.json()['mall']
		self.configs['hang_reward']       = r.json()['hang_reward']
		self.configs['stage_reward']      = r.json()['reward']
		self.configs['player']            = r.json()['player']
		self.configs['entry_consumables'] = r.json()['entry_consumables']
		self.configs['monster']           = r.json()['monster_config']
		self.configs['enemy_layouts']     = r.json()['level_enemy_layouts']
		self.configs['achievement']       = r.json()['achievement']
		self.configs['task']              = r.json()['task']
		self.configs['check_in']          = r.json()['check_in']
		self.configs['version']           = r.json()['version']

		if refresh_world_boss and not already_refreshed_world_boss:
			refresh_world_boss, already_refreshed_world_boss = False, True
			self.configs['world_boss'] = r.json()['world_boss']
			self.configs['world_boss']['boss_life_remaining'] = \
					[self.configs['world_boss'][f'boss{i}']['life_value'] for i in range(10)]
			self.configs['world_boss']['boss_life'] = \
					[self.configs['world_boss'][f'boss{i}']['life_value'] for i in range(10)]

		if datetime.now(timezone.utc).day == 1 and not already_refreshed_world_boss:
			refreshed_world_boss = True
		if datetime.now(timezone.utc).day != 1 and already_refreshed_world_boss:
			already_refreshed_world_boss = False


	def __getitem__(self, key):
		return self.configs[key]
	



















