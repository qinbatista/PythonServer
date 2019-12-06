
import os
import sys
import time
import json
import random
import aiomysql
import requests
import calendar
from aiohttp import web

class GameManager:
	def __init__(self, worlds = []):
		pass
	async def _connect_sql(self):
		self._pool = await aiomysql.create_pool(
				maxsize = 20,
				host = '192.168.1.102',
				user = 'root',
				password = 'lukseun',
				charset = 'utf8',
				autocommit = True)
	async def _execute_statement(self, database_name: int, statement: str) -> tuple:
		"""
		Executes the given statement and returns the result.
		执行给定的语句并返回结果。
		:param statement: Mysql执行的语句
		:return: 返回执行后的二维元组表
		使用例子：data = await self._execute_statement(world, 'SELECT ' + material + ' FROM player WHERE unique_id="' + str(unique_id) + '";')
		"""
		if self._pool is None: await self._connect_sql()
		async with self._pool.acquire() as conn:
			await conn.select_db(database_name)
			async with conn.cursor() as cursor:
				await cursor.execute(statement)
				return await cursor.fetchall()
	async def _execute_statement_update(self, database_name: int, statement: str) -> int:
		"""
		Execute the update or set statement and return the result.
		执行update或set语句并返回结果。
		:param statement: Mysql执行的语句
		:return: 返回update或者是set执行的结果
		使用例子：return await self._execute_statement_update(world, f"UPDATE player SET {material}={value} where unique_id='{unique_id}'")
		"""
		if self._pool is None: await self._connect_sql()
		async with self._pool.acquire() as conn:
			await conn.select_db(database_name)
			async with conn.cursor() as cursor:
				return await cursor.execute(statement)
	def _message_typesetting(self, status: int, message: str, data: dict = {}) -> dict:
		return {"status": status, "message": message, "data": data}
	async def function_hello(self, world: int, unique_id: str):
		# card_info = await self._execute_statement(world, f'select vip_card_type from player where unique_id="{unique_id}"')
		return self._message_typesetting(200,"this is message",{"status":"200","wtf":"a"})





ROUTES = web.RouteTableDef()
def _json_response(body: dict = "", **kwargs) -> web.Response:
	kwargs['body'] = json.dumps(body or kwargs['kwargs']).encode('utf-8')
	kwargs['content_type'] = 'text/json'
	return web.Response(**kwargs)

@ROUTES.post('/function_hello')
async def _get_all_task(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).function_hello(int(post['world']), post['unique_id'])
	return _json_response(result)

def run():
	app = web.Application()
	app.add_routes(ROUTES)
	app['MANAGER'] = GameManager()
	web.run_app(app, port = "9988")


if __name__ == '__main__':
	run()
