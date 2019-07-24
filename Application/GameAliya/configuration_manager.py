#
# Configuration Manager
#
###############################################################################


import json
import threading
import configparser
from aiohttp import web


REWARD_LIST = './Configuration/client/1.0/stage_reward_config.json'
LOTTERY = './Configuration/server/1.0/lottery.json'
WEAPON = './Configuration/server/1.0/weapon.json'
SKILL = './Configuration/server/1.0/skill.json'

class ConfigurationManager:
	def __init__(self):
		self._refresh_configurations()
		self._start_timer(600)


	
	async def get_game_manager_configuration(self):
		return self.game_manager_config



	def _refresh_configurations(self):
		self._read_game_manager_configuration()

	def _read_game_manager_configuration(self):
		reward_list = [v for v in (json.load(open(REWARD_LIST, encoding = 'utf-8'))).values()]
		lottery = json.load(open(LOTTERY, encoding = 'utf-8'))
		weapon = json.load(open(WEAPON, encoding = 'utf-8'))
		skill = json.load(open(SKILL, encoding = 'utf-8'))
		self.game_manager_config = {'reward_list' : reward_list, 'lottery' : lottery, 'weapon' : weapon, 'skill' : skill}


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



@ROUTES.get('/get_game_manager_configuration')
async def __get_game_manager_configuration(request: web.Request) -> web.Response:
	data = await MANAGER.get_game_manager_configuration()
	return _json_response(data)





def run():
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port=8002)


if __name__ == '__main__':
	run()
