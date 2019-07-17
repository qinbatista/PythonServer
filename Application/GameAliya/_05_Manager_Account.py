#
# An example for an SQL manager server using asyncio programming methods.
# We will use aiohttp library to network these API calls so that they can be
# accessed from different physical devices on the network.
# Additionally, we will be using tormysql library to manage the SQL server pool
# of connections.
#
# All functions that connect to the database should be async. The more async code
# we use, the faster the entire server becomes.
#
#
# The file has two parts:
#	- The DefaultManager class
#	- The aiohttp server bindings for the class methods
#
###############################################################################


# Some safe default includes. Feel free to add more if you need.
import json
import random
import tormysql
import configparser
from aiohttp import web
from aiohttp import ClientSession


CONFIG = configparser.ConfigParser()
CONFIG.read('Configuration/server/1.0/server.conf')


TOKEN_SERVER_BASE_URL = 'http://localhost:' + CONFIG['_00_Token_Server']['port']


# Part (1 / 2)
class AccountManager:
	def __init__(self):
		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive.
		self._pool = tormysql.ConnectionPool(max_connections=10, host='192.168.1.102', user='root', passwd='lukseun', db='aliya', charset='utf8')


	async def login(self, identifier: str, value: str, password: str) -> dict:
		valid = await self._valid_credentials(identifier, value, password)
		if not valid:
			return self.message_typesetting(1, 'Invalid credentials')
		unique_id = await self._get_unique_id(identifier, value)
		resp = await self._request_new_token(unique_id, await self._get_prev_token(identifier, value))
		await self._register_token(unique_id, resp['token'])
		return self.message_typesetting(0, 'success', resp)

	async def login_unique(self, unique_id: str) -> dict:
		if not await self._check_exists('unique_id', unique_id):
			await self._create_new_user(unique_id)
			prev_token = ''
		elif await self._account_is_bound(unique_id):
			return self.message_typesetting(2, 'account already bound')
		else:
			prev_token = await self._get_prev_token('unique_id', unique_id)
		resp = await self._request_new_token(unique_id, prev_token)
		await self._register_token(unique_id, resp['token'])
		return self.message_typesetting(0, 'success', resp)




			####################################
			#          P R I V A T E		   #
			####################################

	async def _check_exists(self, identifier: str, value: str) -> bool:
		data = await self._execute_statement('SELECT `' + identifier + '` FROM userinfo WHERE `' + identifier + '` = "' + value + '";')
		if () == data or ('',) in data or (None,) in data:
			return False
		return True

	async def _account_is_bound(self, unique_id: str) -> bool:
		data = await self._execute_statement('SELECT account FROM userinfo WHERE unique_id = "' + unique_id + '";')
		if ('',) in data or () == data or (None,) in data:
			return False
		return True

	async def _register_token(self, unique_id: str, token: str) -> None:
		await self._execute_statement('UPDATE userinfo SET token = "' + token + '" WHERE unique_id = "' + unique_id + '";')

	async def _get_prev_token(self, identifier: str, value: str) -> str:
		data = await self._execute_statement('SELECT token FROM userinfo WHERE `' + identifier + '` = "' + value + '";')
		return data[0][0]

	async def _valid_credentials(self, identifier: str, value: str, password: str) -> bool:
		p = await self._execute_statement('SELECT password FROM userinfo WHERE `' + identifier + '` = "' + value + '";')
		return (password,) in p

	async def _request_new_token(self, unique_id: str, prev_token: str = ''):
		async with ClientSession() as session:
			async with session.post(TOKEN_SERVER_BASE_URL + '/issue_token', data = {'unique_id' : unique_id, 'prev_token' : prev_token}) as resp:
				return await resp.json(content_type = 'text/json')


	async def _get_unique_id(self, identifier: str, value: str) -> str:
		'''
		Returns unique_id associated with the identifier. None if identifier invalid.
		'''
		data = await self._execute_statement('SELECT unique_id FROM userinfo WHERE `' + identifier + '` = "' + value + '";')
		if data == () or (None,) in data or ('',) in data:
			return None
		return data[0][0]

	async def _execute_statement(self, statement: str) -> tuple:
		'''
		Executes the given statement and returns the result.
		'''
		async with await self._pool.Connection() as conn:
			async with conn.cursor() as cursor:
				await cursor.execute(statement)
				data = cursor.fetchall()
				return data

	def message_typesetting(self, status: int, message: str, data: dict={}) -> dict:
		return {'status' : status, 'message' : message, 'random' : random.randint(-1000, 1000), 'data' : data}




# Part (2 / 2)
MANAGER = AccountManager()  # we want to define a single instance of the class
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


@ROUTES.post('/login')
async def __login(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.login(post['identifier'], post['value'], post['password'])
	return _json_response(data)


@ROUTES.post('/login_unique')
async def __login(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.login_unique(post['unique_id'])
	return _json_response(data)




def run():
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port = CONFIG.getint('_05_Manager_Account', 'port'))


if __name__ == '__main__':
	run()
