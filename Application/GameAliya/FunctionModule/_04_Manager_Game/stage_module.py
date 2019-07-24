import json
import tormysql
import time
import os
import datetime
import configparser
import random
from aiohttp import web
from aiohttp import ClientSession


CONFIG = configparser.ConfigParser()
CONFIG.read('../../Configuration/server/1.0/server.conf')
MANAGER_BAG_BASE_URL = CONFIG['bag_manager']['address'] + ":" + CONFIG['bag_manager']['port']
HANG_JSON_NAME = "../../Configuration/client/1.0/stage_reward_config.json"


class StageSystemClass:
	def __init__(self, *args, **kwargs):
		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive.
		# 这是SQL服务器的连接池。 只要这个类还活着，这些连接就会保持打开状态。
		# TODO verify that this is true :D
		self._pool = tormysql.ConnectionPool(max_connections=10, host='192.168.1.102', user='root', passwd='lukseun', db='aliya', charset='utf8')
		self.format_sql = {
			"smallint": "%s",
			"varchar": "'%s'",
			"char": "'%s'"
		}
		self.stage_reward_list = self.__read_json_data(path=HANG_JSON_NAME)

	async def pass_stage(self, unique_id: str, stage: int) -> dict:
		# success ===> 0
		# 0 : passed customs ===> success
		# 1 : database operation error
		# 9 : abnormal data!
		if self.__class__.__name__ == "PlayerManager":
			json_data = await self.try_all_material(unique_id=unique_id, stage=stage)
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
			data = {"keys": list(material_dict.keys()), "values": json_data["remaining"][1], "rewards": list(material_dict.values())}
			return self.message_typesetting(status=0, message="passed customs!", data=data)

#  ############################# 2019-7-23 16:18 header #############################
	async def start_hang_up(self, unique_id: str, stage: int):
		"""
		success ===> 0 , 1 , 2 , 3 , 4 , 5

		1分钟奖励有可能奖励1颗钻石，30颗金币，10个铁
		minute = 1 ==> reward 0 or 1 diamond and 30 coin and 10 iron
		minute = 2 ==> reward 0 or 1 or 2 diamond and 60 coin and 20 iron
		"""
		hang_up_time = self._get_hang_up_time(unique_id=unique_id)
		material_dict = self.stage_reward_list[stage]
		if hang_up_time == "":
			hang_up_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
			if self._set_hang_up_time(unique_id=unique_id, hang_up_time=hang_up_time) == 0:
				return self.message_typesetting(status=1, message="database operating error")
			return self.message_typesetting(status=0, message="hang up success", data={"hang_up_time": hang_up_time})
		update_str, select_str = self.__sql_str_operating(unique_id=unique_id, material_dict=material_dict)
		return self.message_typesetting(status=2, message="repeat hang up")

	# 同bag_module下的__read_json_data
	def __read_json_data(self, path: str) -> list:
		data = []
		if os.path.exists(path):
			data_dict = json.load(open(path, encoding="utf-8"))
			for key in data_dict.keys():
				data.append(data_dict[key])
		print("[__read_json_data] -> data:" + str(data))
		return data

	# 同bag_module下的__sql_str_operating
	def __sql_str_operating(self, unique_id: str, material_dict: dict) -> (str, str):
		update_str = "UPDATE player SET "
		update_end_str = " where unique_id='%s'" % unique_id
		select_str = "SELECT "
		select_end_str = " FROM player WHERE unique_id='%s'" % unique_id
		for key in material_dict.keys():
			update_str += "%s=%s+%s, " % (key, key, material_dict[key])
			select_str += "%s, " % key
		update_str = update_str[: len(update_str) - 2] + update_end_str
		select_str = select_str[: len(select_str) - 2] + select_end_str
		print("[__sql_str_operating] -> update_str:" + update_str)
		print("[__sql_str_operating] -> select_str:" + select_str)
		return update_str, select_str

	async def _set_hang_up_time(self, unique_id: str, hang_up_time: str) -> str:
		return await self._execute_statement_update("update player set hang_up_time = '" + hang_up_time + "' where unique_id=%s" % unique_id)

	async def _get_hang_up_time(self, unique_id: str) -> str:
		data = await self._execute_statement("select hang_up_time from player where unique_id=%s" % unique_id)
		return data[0][0]



#  ############################# 2019-7-23 16:18   end  #############################

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
