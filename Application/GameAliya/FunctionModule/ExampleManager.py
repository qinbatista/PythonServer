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
import tormysql
import random
from aiohttp import web
from aiohttp import ClientSession


# Part (1 / 2)
class PlayerManager:
	def __init__(self):
		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive.
		self._pool = tormysql.ConnectionPool(max_connections = 10, host = '192.168.1.102', user = 'root', passwd = 'lukseun', db = 'aliya', charset = 'utf8')

	async def public_method(self) -> None:
		# Something interesting
		# await self._execute_statement('STATEMENT')
		pass

	async def _execute_statement(self, statement: str) -> tuple:
		"""
		Executes the given statement and returns the result.
		执行给定的语句并返回结果。
		:param statement: Mysql执行的语句
		:return: 返回执行后的二维元组表
		"""
		async with await self._pool.Connection() as conn:
			async with conn.cursor() as cursor:
				await cursor.execute(statement)
				data = cursor.fetchall()
				return data

	async def _execute_statement_update(self, statement: str) -> int:
		"""
		Execute the update or set statement and return the result.
		执行update或set语句并返回结果。
		:param statement: Mysql执行的语句
		:return: 返回update或者是set执行的结果
		"""
		async with await self._pool.Connection() as conn:
			async with conn.cursor() as cursor:
				return await cursor.execute(statement)

	def __internal_format(self, status: int, remaining: int or tuple) -> dict:
		"""
		Internal json formatted information
		内部json格式化信息
		:param status:状态标识0：成功，1：失败
		:param remaining:改变后的结果
		:return:json格式：{"status": status, "remaining": remaining}
		"""
		return {"status": status, "remaining": remaining}

	def message_typesetting(self, status: int, message: str, data: dict = {}) -> dict:
		"""
		Format the information
		:param message:说明语句
		:param data:json数据
		:return:返回客户端需要的json数据
		"""
		return {"status": status, "message": message, "random": random.randint(-1000, 1000), "data": data}



# Part (2 / 2)
MANAGER = PlayerManager()  # we want to define a single instance of the class
ROUTES = web.RouteTableDef()


# Call this method whenever you return from any of the following functions.
# This makes it very easy to construct a json response back to the caller.
def _json_response(body: dict = "", **kwargs) -> web.Response:
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


def run(port):
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port=port)


if __name__ == '__main__':
	run(8004)
