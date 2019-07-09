#
# WeaponManager.py
#
###############################################################################


import json
import tormysql
from aiohttp import web
from aiohttp import ClientSession

BAG_MANAGER_BASE_URL = 'http://localhost:8082'

class WeaponUpgradeError(Exception):
	pass


class WeaponManager:
	def __init__(self, standard_iron_count = 20, standard_segment_count = 30):
		self._standard_iron_count = standard_iron_count
		self._standard_segment_count = standard_segment_count
		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive. 
		self._pool = tormysql.ConnectionPool(max_connections = 10, host = '127.0.0.1', user = 'root', passwd = 'lukseun', db = 'aliya', charset = 'utf8')


	# levels up a particular weapon. costs iron.
	async def level_up_weapon_level(self, unique_id: str, weapon: str, iron: int):

		star = await self._get_weapon_star(unique_id, weapon)
		if star == 0:
			raise WeaponUpgradeError('User does not have that weapon')

		weapon_level = await self._get_weapon_level(unique_id, weapon)
		if weapon_level == 100:
			raise WeaponUpgradeError('Weapon has reached max level!')

		skill_upgrade_number = int(iron) // self._standard_iron_count
		async with ClientSession() as session:
			async with session.post(BAG_MANAGER_BASE_URL + '/get_iron', data = {'unique_id' : unique_id}) as resp:
				resp = await resp.json(content_type='text/json')
				current_iron = resp['iron']
		if skill_upgrade_number > 0 and (current_iron // self._standard_iron_count) >= skill_upgrade_number:
			if (weapon_level + skill_upgrade_number) > 100:
				skill_upgrade_number = 100 - weapon_level
			weapon_level += skill_upgrade_number





	# levels up a particular passive skill. costs skill points.
	async def level_up_weapon_passive_skill(self, unique_id: str, weapon: str, passive_skill: str):
		pass

	# resets all weapon passive skill points. refunds all skill points back. costs coins.
	async def reset_weapon_skill_points(self, unique_id: str, weapon: str):
		pass

	# levels up the weapon star. costs segments.
	async def level_up_weapon_star(self, unique_id: str, weapon: str):
		pass


	async def _get_weapon_star(self, unique_id: str, weapon: str) -> int:
		data = await self._execute_statement("SELECT `" + str(weapon) + "` FROM weapon_bag WHERE unique_id='" + str(unique_id) + "';")
		if () in data or data == None:
			return 0
		return data[0][0]

	async def _get_weapon_level(self, unique_id: str, weapon: str) -> int:
		data = await self._execute_statement("SELECT weapon_level FROM `" + str(weapon) + "` WHERE unique_id='" + str(unique_id) + "';")
		if () in data or data == None:
			return 0
		return data[0][0]








	

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



# Part (2 / 2)
MANAGER = WeaponManager() # we want to define a single instance of the class
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
			async with session.get('http://localhost:8080/validate', headers = {'authorization' : str(request.headers.get('authorization'))}) as resp:
				if resp.status == 200:
					return await fn(request)
		return _json_response({'message' : 'You need to be logged in to access this resource'}, status = 401)
	return wrapper


# Try running the server and then visiting http://localhost:[PORT]/public_method
@ROUTES.get('/public_method')
async def __public_method(request: web.Request) -> web.Response:
	await MANAGER.public_method()
	return _json_response({'message' : 'asyncio code is awesome!'}, status = 200)


@ROUTES.get('/protected_method')
@login_required
async def __protected_method(request: web.Request) -> web.Response:
	return _json_response({'message' : 'if you can see this, you are logged in!!'})


def run(port: int):
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port = port)


if __name__ == '__main__':
	run(8082)
