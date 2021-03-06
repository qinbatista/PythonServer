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
import copy

from datetime import datetime
from dateutil import tz
TZ_SH = tz.gettz('Asia/Shanghai')


class WorkerResources:
	def __init__(self, redis_addr, db_addr, db_user, db_pw, db_port=3306):
		self.redis_addr = redis_addr
		self.db_addr = db_addr
		self.db_user = db_user
		self.db_pw = db_pw
		self.db_port = db_port

		self.resources = {}

	async def init(self):
		# r = await aioredis.create_redis(f'redis://{self.redis_addr}', \
		# 		encoding = 'utf-8')
		# r.hmset_dict()
		# r.hgetall('')
		# r.set()
		self.resources['session']   = aiohttp.ClientSession(connector = aiohttp.TCPConnector(limit = 0))
		self.resources['redis']     = await aioredis.create_redis(f'redis://{self.redis_addr}',
				encoding = 'utf-8')
		self.resources['db']        = await aiomysql.create_pool(maxsize = 30, host = self.db_addr, port=self.db_port,
				user = self.db_user, password = self.db_pw, charset = 'utf8', autocommit = True)
		self.resources['accountdb'] = await aiomysql.create_pool(maxsize =  4, host = self.db_addr, port=self.db_port,
				user = self.db_user, password = self.db_pw, charset = 'utf8', autocommit = True, db = 'user')
		self.resources['malldb'] = await aiomysql.create_pool(maxsize = 4, host = self.db_addr, port=self.db_port,
				user = self.db_user, password = self.db_pw, charset = 'utf8', autocommit = True, db = 'mall')
		self.resources['exchangedb'] = await aiomysql.create_pool(maxsize = 4, host = self.db_addr, port=self.db_port,
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
		self.rfb = True
		self._rfb = False
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
		self.configs['player']            = r.json()['player']
		self.configs['monster']           = r.json()['monster']
		self.configs['enemy_layouts']     = r.json()['level_enemy_layouts']
		self.configs['achievement']       = r.json()['achievement']
		self.configs['task']              = r.json()['task']
		self.configs['check_in']          = r.json()['check_in']
		self.configs['version']           = r.json()['version']
		self.configs['summon']            = r.json()['summon']
		self.configs['stages']            = r.json()['stages']
		self.configs['sciences']          = r.json()['sciences']
		self.configs['notice']            = r.json()['notice']
		self.configs['markets']           = r.json()['markets']

		today = datetime.now(tz=TZ_SH).day
		if today == 1 and not self._rfb:
			self.rfb = True
		elif today != 1 and self._rfb:
			self._rfb = False
		if self.rfb and not self._rfb:
			self.rfb, self._rfb = False, True
			if self.configs.get('boss') is None:
				self.configs['boss'] = self.configs['stages']['constraint']['stage']['BOSS']
				self.configs['boss']['HP'] = {k: v['boss']['HP'] for k, v in self.configs['stages']['stage'].items() if (k.isdigit() and 3000 < int(k) < 4000)}
			self.configs['boss']['hp'] = {w['id']: copy.deepcopy(self.configs['boss']['HP']) for w in self.configs['world']['worlds']}

	def __getitem__(self, key):
		return self.configs[key]




















