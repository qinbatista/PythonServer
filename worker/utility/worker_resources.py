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

class WorkerResources:
	def __init__(self, redis_addr):
		self.redis_addr = redis_addr

		self.resources = {}
	
	async def init(self):
		self.resources['session']   = aiohttp.ClientSession()
		self.resources['redis']     = await aioredis.create_redis(self.redis_addr)
		self.resources['db']        = await aiomysql.create_pool(maxsize = 10, host = '192.168.1.102', \
				user = 'root', password = 'lukseun', charset = 'utf8', autocommit = True)
		self.resources['accountdb'] = await aiomysql.create_pool(maxsize =  4, host = '192.168.1.102',  \
				user = 'root', password = 'lukseun', charset = 'utf8', autocommit = True, db = 'user')

	async def shutdown(self):
		self.resources['db'].close()
		await self.resources['db'].wait_closed()

		self.resources['accountdb'].close()
		await self.resources['accountdb'].wait_closed()

		await self.resources['session'].close()


	def __getitem__(self, key):
		return self.resources[key]

class ModuleConfigurations:
	def __init__(self, baseurl = 'http://localhost:8000'):
		self.baseurl = baseurl
		self.configs = {}
		self.refresh()
	
	def refresh(self):
		r = requests.get(self.baseurl + '/get_game_manager_config')
		self.configs['lottery']  = r.json()['lottery']
		self.configs['family']   = r.json()['family']
		self.configs['factory']  = r.json()['factory']
		self.configs['world']    = r.json()['world']
		self.configs['weapon']   = r.json()['weapon']
		self.configs['skill']   = r.json()['skill']
		self.configs['role']     = r.json()['role']
		self.configs['package']  = r.json()['package']
		self.configs['vip']      = r.json()['vip']
		self.configs['exp']   = r.json()['player_experience']

	def __getitem__(self, key):
		return self.configs[key]
	



















