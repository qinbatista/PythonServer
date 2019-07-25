#
# account manager
#
###############################################################################


import re
import time
import json
import random
import tormysql
import requests
import configparser
from aiohttp import web
from aiohttp import ClientSession


TOKEN_SERVER_BASE_URL = ''

# Part (1 / 2)
class AccountManager:
	def __init__(self):
		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive.
		self._pool = tormysql.ConnectionPool(max_connections=10, host='192.168.1.102', user='root', passwd='lukseun', db='user', charset='utf8')
		self._password_re = re.compile(r'\A([a-zA-Z0-9]){6,}\Z')
		self._account_re = re.compile(r'\A([a-zA-Z0-9])+([A-Za-z0-9_\-.@]){,24}\Z')


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
			status, message, prev_token = 1, 'new account created', ''
		elif await self._account_is_bound(unique_id):
			return self.message_typesetting(2, 'account already bound')
		else:
			status, message, prev_token = 0, 'success', await self._get_prev_token('unique_id', unique_id)
		resp = await self._request_new_token(unique_id, prev_token)
		await self._register_token(unique_id, resp['token'])
		return self.message_typesetting(status, message, resp)

	# TODO run check_exists as a task
	async def bind_account(self, unique_id: str, password: str, account: str, email: str, phone: str) -> dict:
		is_bound = await self._account_is_bound(unique_id)
		account_exists = await self._check_exists('account', account)
		email_exists = await self._check_exists('email', email)
		phone_exists = await self._check_exists('phone_number', phone)
		if is_bound:
			return self.message_typesetting(1, 'account already bound before')
		if account_exists:
			return self.message_typesetting(2, 'account name already exists')
		if email_exists:
			return self.message_typesetting(3, 'email already exists')
		if phone_exists:
			return self.message_typesetting(4, 'phone number already exists')
		await self._bind_account(unique_id, password, account, email, phone)
		return self.message_typesetting(0, 'success')




			####################################
			#          P R I V A T E		   #
			####################################

	#TODO return success or failure
	async def _bind_account(self, unique_id: str, password: str, account: str, email: str, phone: str):
		await self._execute_statement('UPDATE `info` SET password = "' + password + '", account = "' + account + '", email = "' + email + '", phone_number = "' + phone + '" WHERE unique_id = "' + unique_id + '";')

	#TODO return success or failure
	async def _create_new_user(self, unique_id: str):
		await self._execute_statement('INSERT INTO info (unique_id) VALUES ("' + unique_id + '");')

	async def _check_exists(self, identifier: str, value: str) -> bool:
		data = await self._execute_statement('SELECT * FROM info WHERE `' + identifier + '` = "' + value + '";')
		if () == data:
			return False
		return True

	async def _account_is_bound(self, unique_id: str) -> bool:
		data = await self._execute_statement('SELECT account FROM info WHERE unique_id = "' + unique_id + '";')
		if ('',) in data or () == data or (None,) in data:
			return False
		return True

	async def _register_token(self, unique_id: str, token: str) -> None:
		await self._execute_statement('UPDATE info SET token = "' + token + '" WHERE unique_id = "' + unique_id + '";')

	async def _get_prev_token(self, identifier: str, value: str) -> str:
		data = await self._execute_statement('SELECT token FROM info WHERE `' + identifier + '` = "' + value + '";')
		return data[0][0]

	def _is_valid_password(self, password: str) -> bool:
		return bool(self._password_re.match(password))

	def _is_valid_account_name(self, account: str) -> bool:
		return bool(self._account_re.match(account))

	async def _valid_credentials(self, identifier: str, value: str, password: str) -> bool:
		if not self._is_valid_password(password): return False
		if identifier == 'account':
			if not self._is_valid_account_name(value): return False
		p = await self._execute_statement('SELECT password FROM info WHERE `' + identifier + '` = "' + value + '";')
		return (password,) in p

	async def _request_new_token(self, unique_id: str, prev_token: str = ''):
		async with ClientSession() as session:
			async with session.post(TOKEN_SERVER_BASE_URL + '/issue_token', data = {'unique_id' : unique_id, 'prev_token' : prev_token}) as resp:
				return await resp.json(content_type = 'text/json')


	async def _get_unique_id(self, identifier: str, value: str) -> str:
		'''
		Returns unique_id associated with the identifier. None if identifier invalid.
		'''
		data = await self._execute_statement('SELECT unique_id FROM info WHERE `' + identifier + '` = "' + value + '";')
		if data == () or (None,) in data or ('',) in data:
			return ""
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
ROUTES = web.RouteTableDef()



# Call this method whenever you return from any of the following functions.
# This makes it very easy to construct a json response back to the caller.
def _json_response(body: dict = '', **kwargs) -> web.Response:
	'''
	A simple wrapper for aiohttp.web.Response return value.
	'''
	kwargs['body'] = json.dumps(body or kwargs['kwargs']).encode('utf-8')
	kwargs['content_type'] = 'text/json'
	return web.Response(**kwargs)


@ROUTES.post('/login')
async def __login(request: web.Request) -> web.Response:
	post = await request.post()
	data = await (request.app['MANAGER']).login(post['identifier'], post['value'], post['password'])
	return _json_response(data)


@ROUTES.post('/login_unique')
async def __login(request: web.Request) -> web.Response:
	post = await request.post()
	data = await (request.app['MANAGER']).login_unique(post['unique_id'])
	return _json_response(data)

@ROUTES.post('/bind_account')
async def __login(request: web.Request) -> web.Response:
	post = await request.post()
	data = await (request.app['MANAGER']).bind_account(post['unique_id'], post['password'], post['account'], post['email'], post['phone_number'])
	return _json_response(data)


def get_config() -> configparser.ConfigParser:
	'''
	Fetches the server's configuration file from the config server.
	Waits until the configuration server is online.
	'''
	while True:
		try:
			r = requests.get('http://localhost:8000/get_server_config_location')
			parser = configparser.ConfigParser()
			parser.read(r.json()['file'])
			return parser
		except requests.exceptions.ConnectionError:
			print('Could not find configuration server, retrying in 5 seconds...')
			time.sleep(5)

def run():
	app = web.Application()
	app.add_routes(ROUTES)
	app['MANAGER'] = AccountManager()
	config = get_config()
	global TOKEN_SERVER_BASE_URL
	TOKEN_SERVER_BASE_URL = 'http://localhost:' + config['token_server']['port']
	web.run_app(app, port = config.getint('account_manager', 'port'))


if __name__ == '__main__':
	run()
