import json
import tormysql
import os
import configparser
import random
from aiohttp import web
from aiohttp import ClientSession


format_sql = {
	"smallint": "%s",
	"varchar": "'%s'",
	"char": "'%s'"
}
CONFIG = configparser.ConfigParser()
CONFIG.read('../../Configuration/server/1.0/server.conf')
MANAGER_BAG_BASE_URL = CONFIG['bag_manager']['address'] + ":" + CONFIG['bag_manager']['port']


class StageSystemClass:
	def __init__(self, *args, **kwargs):
		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive.
		# 这是SQL服务器的连接池。 只要这个类还活着，这些连接就会保持打开状态。
		# TODO verify that this is true :D
		self._pool = tormysql.ConnectionPool(max_connections=10, host='192.168.1.102', user='root', passwd='lukseun', db='aliya', charset='utf8')


	async def pass_stage(self, unique_id: str, stage: int) -> dict:
		# 0 : passed customs ===> success
		# 1 : database operation error
		# 9 : abnormal data!
		if self.__class__.__name__ == "PlayerManager":
			json_data = self.try_all_material(unique_id=unique_id, stage=stage)
		else:
			async with ClientSession() as session:
				async with session.post(MANAGER_BAG_BASE_URL + '/try_all_material', data = {'unique_id' : unique_id, 'stage': stage}) as resp:
					json_data = json.loads(await resp.text())
		status = int(json_data["status"])
		if status == 9:
			return self.message_typesetting(status=9, message="abnormal data!")
		elif status == 1:
			return self.message_typesetting(status=1, message="database operation error")
		else:
			material_dict = json_data["remaining"][0]
			data = {"key": list(material_dict.keys()), "reward": list(material_dict.values()), "item": json_data["remaining"][1]}
			return self.message_typesetting(status=0, message="passed customs!", data=data)

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

	def message_typesetting(self, status: int, message: str, data: dict = {}) -> dict:
		"""
		Format the information
		:param message:说明语句
		:param data:json数据
		:return:返回客户端需要的json数据
		"""
		return {"status": status, "message": message, "random": random.randint(-1000, 1000), "data": data}


MANAGER = StageSystemClass()
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


@ROUTES.post('/pass_stage')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.pass_stage(unique_id=post['unique_id'], stage=int(post['stage']))
	return _json_response(result)


def run():
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port=CONFIG.getint('stage_manager', 'port'))


if __name__ == "__main__":
	run()
