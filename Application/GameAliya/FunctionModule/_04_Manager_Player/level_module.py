import json
import tormysql
import os
import configparser
import random
from aiohttp import web
from aiohttp import ClientSession


JSON_NAME = "../../Configuration/1.0/level_reward_config.json"
format_sql = {
	"smallint": "%s",
	"varchar": "'%s'",
	"char": "'%s'"
}
CONFIG = configparser.ConfigParser()
CONFIG.read('../../Configuration/server.conf')
MANAGER_BAG_BASE_URL = 'http://localhost:' + CONFIG['bag_manager']['port']


class LevelSystemClass:
	def __init__(self, *args, **kwargs):
		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive.
		# 这是SQL服务器的连接池。 只要这个类还活着，这些连接就会保持打开状态。
		# TODO verify that this is true :D
		self._pool = tormysql.ConnectionPool(max_connections=10, host='192.168.1.102', user='root', passwd='lukseun', db='aliya', charset='utf8')

	async def pass_level(self, unique_id: str, level_client: int) -> dict:
		reward_list = self.__read_json_data()
		async with ClientSession() as session:
			if self.__class__.__name__ == "LevelSystemClass":
				async with session.post(MANAGER_BAG_BASE_URL + '/get_all_head') as resp:
					data_head_tuple = json.loads(await resp.text())["remaining"]
				async with session.post(MANAGER_BAG_BASE_URL + '/get_all_material', data={'unique_id': unique_id}) as resp:
					content_tuple = json.loads(await resp.text())["remaining"]
			else:
				data_head_tuple = await self.get_all_head()
				content_tuple = await self.get_all_material(unique_id=unique_id)
			head_list, format_list = self.__get_head_list(data_head_tuple=data_head_tuple)
			item_dict = self.__structure_item_dict(head_list, content_tuple)

			if level_client <= 0 or (item_dict["level"] + 1) < level_client:
				return self.message_typesetting(9, "abnormal data!")

			# 改变所有该变的变量
			if item_dict["level"] + 1 == level_client:  # 通过新关卡
				item_dict["level"] = level_client

			reward_data = reward_list[level_client]  # 获得奖励
			reward_data_len = len(reward_data.keys()) + 1
			data = self.__structure_data(reward_data=reward_data, item_dict=item_dict, reward_data_len=reward_data_len)

			sql_str = self.__sql_str_operating(unique_id=unique_id, table_name="player", head_list=head_list, format_list=format_list, item_dict=item_dict)
			if self.__class__.__name__ == "LevelSystemClass":
				async with session.post(MANAGER_BAG_BASE_URL + '/set_all_material', data={"statement": sql_str}) as resp:
					sql_result = json.loads(await resp.text())
			else:
				sql_result = json.loads(await self.set_all_material(statement=sql_str))
			if int(sql_result["status"]) == 1:
				return self.message_typesetting(1, "abnormal data!")
			return self.message_typesetting(0, "passed customs!", data=data)

	def __read_json_data(self) -> list:
		data = []
		if os.path.exists(JSON_NAME):
			data_dict = json.load(open(JSON_NAME, encoding="utf-8"))
			for key in data_dict.keys():
				data.append(data_dict[key])
		print("[level_module.py][read_json_data] -> data:" + str(data))
		return data

	def __get_head_list(self, data_head_tuple: tuple) -> (list, list):
		"""
		获取到列标题列表
		获取构造mysql语句的单字符
		:param data_head_tuple:二维元组
		:return:列标题列表，格式列表
		"""
		head_list = []
		format_list = []
		for col in data_head_tuple:
			head_list.append(col[0])
			format_list.append(format_sql[col[1][:col[1].find("(")]])  # 将smallint(6)截取出smallint，然后用标准转换成字符，用于后面替换成sql的替换
		return head_list, format_list

	def __structure_data(self, reward_data: dict, item_dict: dict, reward_data_len: int) -> dict:
		"""
		构造一个返回给客户端的通关奖励与设置字典，包含奖励与设置项
		:param reward_data:奖励的字典
		:param item_dict:所有的字段对应的字典
		:param reward_data_len:奖励的字典的长度
		:return:返回的是一个字典，包含奖励与设置
		"""
		temp_list = []
		data = {}
		for key in reward_data.keys():
			temp_list.append(reward_data[key])  # [key, value]
		for i in range(1, reward_data_len):
			reward = "reward" + str(i)
			data.update({reward: temp_list[i - 1]})

		for i in range(1, reward_data_len):
			reward = "reward" + str(i)
			key = data[reward][0]
			item_dict[key] += data[reward][1]
			data.update({"item" + str(i): [key, item_dict[key]]})
		data.update({"item" + str(reward_data_len): ["level", item_dict["level"]]})
		return data

	def __structure_item_dict(self, head_list, content_tuple) -> dict:
		item_dict = {}
		for i in range(len(head_list)):
			item_dict.update({head_list[i]: content_tuple[i]})
		return item_dict

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


MANAGER = LevelSystemClass()
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


@ROUTES.post('/pass_level')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.pass_level(unique_id=post['unique_id'], level_client=int(post['level']))
	return _json_response(result)


def run():
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port=CONFIG.getint('level_manager', 'port'))


if __name__ == "__main__":
	run()
