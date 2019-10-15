'''
worker_resources.py

A group of resources used by workers.
Provides a centralized location for instantiating frequently used connections
such as mysql connection pools.

The worker provides these resources to the message handler.
'''

import aiohttp
import aioredis
import aiomysql
import requests
import concurrent

class WorkerResources:
	def __init__(self, cfg):
		self.cfg = cfg
		self.resources = {}
	
	async def init(self):
		self.resources['executor'] = concurrent.futures.ProcessPoolExecutor(max_workers = 1)
		self.resources['session'] = aiohttp.ClientSession()
		self.resources['redis'] = await aioredis.create_redis(self.cfg['redis']['addr'])
		self.resources['db'] = await aiomysql.create_pool(maxsize = 10, host = '192.168.1.102', user = 'root', password = 'lukseun', charset = 'utf8', autocommit = True, db = 'experimental')
		self.resources['accountdb'] = await aiomysql.create_pool(maxsize = 4, host = '192.168.1.102', user = 'root', password = 'lukseun', charset = 'utf8', autocommit = True, db = 'user')

	async def shutdown(self):
		self.resources['db'].close()
		await self.resources['db'].wait_closed()

		self.resources['accountdb'].close()
		await self.resources['accountdb'].wait_closed()

		await self.resources['session'].close()

		self.resources['executor'].shutdown(wait = False)

	def __getitem__(self, key):
		return self.resources[key]

class ModuleConfigurations:
	def __init__(self, baseurl = 'http://localhost:8000'):
		self.baseurl = baseurl
		self.configs = {}
		self.refresh()
	
	def refresh(self):
		r = requests.get(self.baseurl + '/get_game_manager_config')
		self.configs['lottery'] = r.json()['lottery']
		self.configs['family']  = r.json()['family']

	def __getitem__(self, key):
		return self.configs[key]
	



















