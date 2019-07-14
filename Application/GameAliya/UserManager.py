#
# An asynchronous user manager that exposes a simple API to manage users.
# Currently used exclusively by token_server.py
#
################################################################################

import json
import tormysql
from aiohttp import web


# asyncio library used for testing purposes only, can be safely removed
import asyncio

class CredentialError(Exception):
	'''
	Raised when there is an issue with one or more of the supplied credentials.
	'''
	pass

class UserManager:
	def __init__(self):
		self._pool = tormysql.ConnectionPool(max_connections = 10, idle_seconds = 7200, wait_connection_timeout = 3, host = '192.168.1.102', user = 'root', passwd = 'lukseun', db = 'aliya', charset = 'utf8')

	async def register_unique_id(self, unique_id: str) -> None:
		await self._execute_statement('INSERT INTO userinfo (unique_id) VALUES ("' + str(unique_id) + '");')

	async def validate_credentials(self, password: str, identifier: str, value: str) -> None:
		'''
		Raises CredentialError if the password does not match the given identifier.
		'''
		master = await self._fetch_password(identifier, value)
		if (password,) not in master:
			raise CredentialError('Invalid credentials.')

	async def fetch_token(self, unique_id: str) -> str:
		'''
		Returns the str representation of the token issued to the following unique_id.
		Raises CredentialError if the unique_id does not exist.
		'''
		data = await self._execute_statement("SELECT token FROM userinfo WHERE unique_id = '" + str(unique_id) + "';")
		if data == ():
			raise CredentialError('The unique_id does not exist.')
		elif (None,) in data or ('',) in data:
			return None
		return data[0][0]

	async def update_token(self, unique_id: str, token: str) -> None:
		'''
		Updates the token associated with the unique_id.
		'''
		await self._execute_statement('UPDATE `userinfo` SET `token` = "' + str(token) + '" WHERE (`unique_id` = "' + str(unique_id) + '");')

	async def fetch_unique_id(self, identifier: str, value: str) -> str:
		'''
		Returns the unique_id associated with the corresponding account.
		'''
		data = await self._execute_statement("SELECT unique_id FROM userinfo WHERE `" + str(identifier) + "` = '" + str(value) + "';")
		if data == () or (None,) in data or ('',) in data:
			raise CredentialError('Could not find unique_id corresponding to these identifiers')
		return data[0][0]

	async def account_is_bound(self, unique_id: str) -> bool:
		'''
		Returns true if the unique_id refers to an account that has been bound.
		'''
		data = await self._execute_statement("SELECT account FROM userinfo WHERE unique_id = '" + str(unique_id) + "';")
		if (None,) in data or ('',) in data:
			return False
		return True

	async def check_exists(self, identifier: str, value: str, raise_error = False) -> bool:
		'''
		Returns True if the value for the given identifier exists, False otherwise.
		Optionally raises CredentialError if not found.
		'''
		exists = await self._check_exists(identifier, value)
		if raise_error and not exists:
			raise CredentialError('The value for the given identifier does not exist.')
		return exists

	async def _is_valid_account_name(self, account: str):
		'''
		TODO
		'''
		if account == '':
			raise CredentialError('Account name can not be empty.')

	def _is_valid_password(self, password: str):
		'''
		TODO
		'''
		if password == '':
			raise CredentialError('Password can not be empty.')

	async def _fetch_password(self, column_name: str, value: str) -> str:
		'''
		Returns the password associated with the attribute.
		'''
		return await self._execute_statement("SELECT password FROM userinfo WHERE `" + str(column_name) + "` = '" + str(value) + "';")

	async def _check_exists(self, column_name: str, value: str) -> bool:
		'''
		Returns True if the value exists in the column, False otherwise.
		The value must be stored as a string in the table.
		'''
		data = await self._execute_statement("SELECT 1 FROM aliya.userinfo WHERE " + str(column_name) + " = '" + str(value) + "';")
		return data != ()

	async def _execute_statement(self, statement: str) -> tuple:
		'''
		Executes the given statement and returns the result.
		'''
		async with await self._pool.Connection() as conn:
			async with conn.cursor() as cursor:
				await cursor.execute(statement)
				data = cursor.fetchall()
				return data



##############################################################################################
#
#
# Below this level are public networked API calls for the above class.
# They are not yet documented.
# Standard port number also yet to be defined.
#
##############################################################################################

ROUTES = web.RouteTableDef()
MANAGER = UserManager()


def _json_response(body: str = '', **kwargs) -> web.Response:
	'''
	A simple wrapped for aiohttp.web.Response where we dumps body to json
	and assign the correct content_type.
	'''
	kwargs['body'] = json.dumps(body or kwargs['kwargs']).encode('utf-8')
	kwargs['content_type'] = 'text/json'
	return web.Response(**kwargs)




# TODO API Documentation
@ROUTES.post('/register_unique_id')
async def __register_unique_id(request: web.Request) -> web.Response:
	post = await request.post()
	await MANAGER.register_unique_id(post['unique_id'])
	return _json_response({'message' : 'OK'})


# TODO API Documentation
@ROUTES.post('/fetch_token')
async def __fetch_token(request: web.Request) -> web.Response:
	post = await request.post()
	try:
		token = await MANAGER.fetch_token(post['unique_id'])
		if not token:
			return _json_response({'message' : 'The unique_id does not exist'}, status = 400)
	except CredentialError:
		return _json_response({'message' : 'The unique_id does not exist'}, status = 400)
	return _json_response({'token' : token})


# TODO API Documentation
@ROUTES.post('/validate_credentials')
async def __validate_credentials(request: web.Request) -> web.Response:
	post = await request.post()
	try:
		await MANAGER.validate_credentials(post['password'], post['identifier'], post['value'])
		return _json_response({'message' : 'Valid credentials'})
	except CredentialError:
		return _json_response({'message' : 'Invalid credentials'}, status = 400)


# TODO API Documentation
@ROUTES.post('/update_token')
async def __update_token(request: web.Request) -> web.Response:
	post = await request.post()
	await MANAGER.update_token(post['unique_id'], post['token'])
	return _json_response({'message' : 'OK'})



# TODO API Documentation
@ROUTES.post('/fetch_unique_id')
async def __fetch_unique_id(request: web.Request) -> web.Response:
	post = await request.post()
	try:
		unique_id = await MANAGER.fetch_unique_id(post['identifier'], post['value'])
		if not unique_id:
			return _json_response({'message' : 'Invalid credentials'}, status = 400)
	except CredentialError:
		return _json_response({'message' : 'Invalid credentials'}, status = 400)
	return _json_response({'unique_id' : unique_id})


# TODO API Documentation
@ROUTES.post('/account_is_bound')
async def __account_is_bound(request: web.Request) -> web.Response:
	post = await request.post()
	bound = await MANAGER.account_is_bound(post['unique_id'])
	if bound:
		return _json_response({'message' : 'True'})
	return _json_response({'message' : 'False'})


# TODO API Documentation
@ROUTES.post('/check_exists')
async def __check_exists(request: web.Request) -> web.Response:
	post = await request.post()
	exists = await MANAGER.check_exists(post['identifier'], post['value'])
	if exists:
		return _json_response({'message' : 'True'})
	return _json_response({'message' : 'False'}, status = 400)





def run():
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port=8081)




# TODO refactor testing code to separate module
async def test_valid_credentials(manager):
	res1 = await manager.valid_credentials('keepo', account = 'amdsucks')
	res2 = await manager.valid_credentials('keepo', email = 'matt@gmail.com')
	res3 = await manager.valid_credentials('keepo', phone = '222')
	res4 = await manager.valid_credentials('keepo2', account = 'childrensucks')
	res5 = await manager.valid_credentials('keepo', account = 'childrensucks2')
	res6 = await manager.valid_credentials('keepo')
	res7 = await manager.valid_credentials('keepo', account = 'childrensucks', email = 'matt@gmail.com', phone = '455636')
	print(f'Test 1 expected True got back: {res1}')
	print(f'Test 2 expected True got back: {res2}')
	print(f'Test 3 expected True got back: {res3}')
	print(f'Test 4 expected False got back: {res4}')
	print(f'Test 5 expected False got back: {res5}')
	print(f'Test 6 expected False got back: {res6}')
	print(f'Test 7 expected True got back: {res7}')


if __name__ == '__main__':
	run()
