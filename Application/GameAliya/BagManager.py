#
# BagManager.py
#
###############################################################################


# Some safe default includes. Feel free to add more if you need.
import json
import tormysql
from aiohttp import web
from aiohttp import ClientSession


# Part (1 / 2)
class BagManager:
	def __init__(self):
		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive. 
		self._pool = tormysql.ConnectionPool(max_connections=10, host='192.168.1.102', user='root', passwd='lukseun', db='aliya', charset='utf8')
	
	async def get_iron(self, unique_id: str) -> int:
		iron = await self._execute_statement("SELECT iron FROM bag WHERE unique_id='" + str(unique_id) + "';")
		if () in iron or iron is None:
			return 0
		return iron[0][0]
	
	# Returns the remaining iron after removal
	# Does not check if there is enough iron to remove the total amount.
	async def remove_iron(self, unique_id: str, amount: int) -> int:
		current = await self.get_iron(unique_id)
		await self._update_quantity(unique_id, 'iron', max(current - int(amount), 0))
		return max(current - int(amount), 0)  # ################### 待检测 #########################
	
	# Returns the resulting iron after addition
	async def add_iron(self, unique_id: str, amount: int):
		current = await self.get_iron(unique_id)
		await self._update_quantity(unique_id, 'iron', current + int(amount))
		return current + int(amount)
	
	async def get_diamonds(self, unique_id: str):
		diamonds = await self._execute_statement("SELECT diamonds FROM bag WHERE unique_id='" + str(unique_id) + "';")
		if () in diamonds or diamonds == None:
			return 0
		return diamonds[0][0]
	
	# Returns the remaining diamonds after removal
	# Does not check if there is enough diamonds to remove the total amount.
	async def remove_diamonds(self, unique_id: str, amount: int):
		current = await self.get_diamonds(unique_id)
		await self._update_quantity(unique_id, 'diamonds', max(current - int(amount), 0))
		return max(current - int(amount), 0)
	
	# Returns the resulting diamonds after addition
	async def add_diamonds(self, unique_id: str, amount: int):
		current = await self.get_diamonds(unique_id)
		await self._update_quantity(unique_id, 'diamonds', current + int(amount))
		return current + int(amount)
	
	async def get_experience_potion(self, unique_id: str):
		potions = await self._execute_statement("SELECT experience_potion FROM bag WHERE unique_id='" + str(unique_id) + "';")
		if () in potions or potions is None:
			return 0
		return potions[0][0]
	
	# Returns the remaining experience potions after removal
	# Does not check if there is enough experience potions to remove the total amount.
	async def remove_experience_potions(self, unique_id: str, amount: int):
		current = await self.get_experience_potion(unique_id)
		await self._update_quantity(unique_id, 'experience_potion', max(current - int(amount), 0))
		return max(current - int(amount), 0)
	
	# Returns the resulting experience potions after addition
	async def add_experience_potions(self, unique_id: str, amount: int):
		current = await self.get_experience_potion(unique_id)
		await self._update_quantity(unique_id, 'experience_potion', current + int(amount))
		return current + int(amount)
	
	async def get_coin(self, unique_id: str):
		coins = await self._execute_statement("SELECT coin FROM bag WHERE unique_id='" + str(unique_id) + "';")
		if () in coins or coins is None:
			return 0
		return coins[0][0]
	
	# Returns the remaining coins after removal
	# Does not check if there is enough coins to remove the total amount.
	async def remove_coins(self, unique_id: str, amount: int):
		current = await self.get_coin(unique_id)
		await self._update_quantity(unique_id, 'coin', max(current - int(amount), 0))
		return max(current - int(amount), 0)
	
	# Returns the resulting coins after addition
	async def add_coins(self, unique_id: str, amount: int):
		current = await self.get_coin(unique_id)
		await self._update_quantity(unique_id, 'coin', current + int(amount))
		return current + int(amount)
	
	async def get_small_energy_potion(self, unique_id: str):
		potions = await self._execute_statement(
			"SELECT small_energy_potion FROM bag WHERE unique_id='" + str(unique_id) + "';")
		if () in potions or potions is None:
			return 0
		return potions[0][0]
	
	# Returns the remaining coins after removal
	# Does not check if there is enough coins to remove the total amount.
	async def remove_small_energy_potions(self, unique_id: str, amount: int):
		current = await self.get_small_energy_potion(unique_id)
		await self._update_quantity(unique_id, 'small_energy_potion', max(current - int(amount), 0))
		return max(current - int(amount), 0)
	
	# Returns the resulting coins after addition
	async def add_small_energy_potions(self, unique_id: str, amount: int):
		current = await self.get_small_energy_potion(unique_id)
		await self._update_quantity(unique_id, 'small_energy_potion', current + int(amount))
		return current + int(amount)
	
	async def _update_quantity(self, unique_id: str, column_name: str, quantity: int):
		await self._execute_statement(
			"UPDATE bag SET `" + str(column_name) + "`='" + str(quantity) + "' WHERE unique_id='" + str(unique_id) + "';")
	
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
MANAGER = BagManager()  # we want to define a single instance of the class
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
			async with session.get('http://localhost:8080/validate', headers={'authorization': str(request.headers.get('authorization'))}) as resp:
				if resp.status == 200:
					return await fn(request)
		return _json_response({'message': 'You need to be logged in to access this resource'}, status=401)
	
	return wrapper


@ROUTES.post('/get_iron')
async def __get_iron(request: web.Request) -> web.Response:
	post = await request.post()
	iron = await MANAGER.get_iron(post['unique_id'])
	return _json_response({'iron': iron})


@ROUTES.post('/remove_iron')
async def __remove_iron(request: web.Request) -> web.Response:
	post = await request.post()
	remaining = await MANAGER.remove_iron(post['unique_id'], post['amount'])
	return _json_response({'remaining': remaining})


@ROUTES.post('/try_remove_iron')
async def __try_remove_iron(request: web.Request) -> web.Response:
	post = await request.post()
	current = await MANAGER.get_iron(post['unique_id'])
	if int(current) - int(post['amount']) < 0:
		return _json_response({'message': 'Insufficient iron'}, status=400)
	remaining = await MANAGER.remove_iron(post['unique_id'], post['amount'])
	return _json_response({'remaining': remaining})


@ROUTES.post('/add_iron')
async def __add_iron(request: web.Request) -> web.Response:
	post = await request.post()
	remaining = await MANAGER.add_iron(post['unique_id'], post['amount'])
	return _json_response({'remaining': remaining})


@ROUTES.post('/get_diamonds')
async def __get_diamonds(request: web.Request) -> web.Response:
	post = await request.post()
	diamonds = await MANAGER.get_diamonds(post['unique_id'])
	return _json_response({'diamonds': diamonds})


@ROUTES.post('/remove_diamonds')
async def __remove_diamonds(request: web.Request) -> web.Response:
	post = await request.post()
	remaining = await MANAGER.remove_diamonds(post['unique_id'], post['amount'])
	return _json_response({'remaining': remaining})


@ROUTES.post('/try_remove_diamonds')
async def __try_remove_diamonds(request: web.Request) -> web.Response:
	post = await request.post()
	current = await MANAGER.get_diamonds(post['unique_id'])
	if int(current) - int(post['amount']) < 0:
		return _json_response({'message': 'Insufficient diamonds'}, status=400)
	remaining = await MANAGER.remove_diamonds(post['unique_id'], post['amount'])
	return _json_response({'remaining': remaining})


@ROUTES.post('/add_diamonds')
async def __add_diamonds(request: web.Request) -> web.Response:
	post = await request.post()
	remaining = await MANAGER.add_diamonds(post['unique_id'], post['amount'])
	return _json_response({'remaining': remaining})


@ROUTES.post('/get_experience_potion')
async def __get_experience_potion(request: web.Request) -> web.Response:
	post = await request.post()
	potions = await MANAGER.get_experience_potion(post['unique_id'])
	return _json_response({'potions': potions})


@ROUTES.post('/remove_experience_potions')
async def __remove_experience_potions(request: web.Request) -> web.Response:
	post = await request.post()
	remaining = await MANAGER.remove_experience_potions(post['unique_id'], post['amount'])
	return _json_response({'remaining': remaining})


@ROUTES.post('/add_experience_potions')
async def __add_experience_potions(request: web.Request) -> web.Response:
	post = await request.post()
	remaining = await MANAGER.add_experience_potions(post['unique_id'], post['amount'])
	return _json_response({'remaining': remaining})


@ROUTES.post('/get_coin')
async def __get_coin(request: web.Request) -> web.Response:
	post = await request.post()
	coins = await MANAGER.get_coin(post['unique_id'])
	return _json_response({'coins': coins})


@ROUTES.post('/remove_coins')
async def __remove_coins(request: web.Request) -> web.Response:
	post = await request.post()
	remaining = await MANAGER.remove_coins(post['unique_id'], post['amount'])
	return _json_response({'remaining': remaining})


@ROUTES.post('/try_remove_coins')
async def __try_remove_coins(request: web.Request) -> web.Response:
	post = await request.post()
	current = await MANAGER.get_coin(post['unique_id'])
	if int(current) - int(post['amount']) < 0:
		return _json_response({'message': 'Insufficient coins'}, status=400)
	remaining = await MANAGER.remove_coins(post['unique_id'], post['amount'])
	return _json_response({'remaining': remaining})


@ROUTES.post('/add_coins')
async def __add_coins(request: web.Request) -> web.Response:
	post = await request.post()
	remaining = await MANAGER.add_coins(post['unique_id'], post['amount'])
	return _json_response({'remaining': remaining})


@ROUTES.post('/get_small_energy_potion')
async def __get_small_energy_potion(request: web.Request) -> web.Response:
	post = await request.post()
	remaining = await MANAGER.get_small_energy_potion(post['unique_id'])
	return _json_response({'remaining': remaining})


@ROUTES.post('/remove_small_energy_potions')
async def __remove_small_energy_potions(request: web.Request) -> web.Response:
	post = await request.post()
	remaining = await MANAGER.remove_small_energy_potions(post['unique_id'], post['amount'])
	return _json_response({'remaining': remaining})


@ROUTES.post('/try_remove_small_energy_potions')
async def __try_remove_small_energy_potions(request: web.Request) -> web.Response:
	post = await request.post()
	current = await MANAGER.get_small_energy_potion(post['unique_id'])
	if int(current) - int(post['amount']) < 0:
		return _json_response({'message': 'Insufficient potions'}, status=400)
	remaining = await MANAGER.remove_small_energy_potions(post['unique_id'], post['amount'])
	return _json_response({'remaining': remaining})


@ROUTES.post('/add_small_energy_potions')
async def __add_small_energy_potions(request: web.Request) -> web.Response:
	post = await request.post()
	remaining = await MANAGER.add_small_energy_potions(post['unique_id'], post['amount'])
	return _json_response({'remaining': remaining})


def run(port: int):
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port=port)


if __name__ == '__main__':
	run(8082)
