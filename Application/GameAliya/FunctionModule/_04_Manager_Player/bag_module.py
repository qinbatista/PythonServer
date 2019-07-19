import random
import json
import os
import configparser
import tormysql
from aiohttp import web

CONFIG = configparser.ConfigParser()
CONFIG.read('../../Configuration/server/1.0/server.conf')
JSON_NAME = "../../Configuration/client/1.0/stage_reward_config.json"


class BagSystemClass:
	def __init__(self, *args, **kwargs):
		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive.
		# 这是SQL服务器的连接池。 只要这个类还活着，这些连接就会保持打开状态。
		# TODO verify that this is true :D
		self._pool = tormysql.ConnectionPool(max_connections=10, host='192.168.1.102', user='root', passwd='lukseun', db='aliya', charset='utf8')
		self.reward_list = self.__read_json_data()

	async def get_all_head(self) -> dict:
		"""
		Used to get information such as the title of the database
		用于获取数据库的标题等信息
		:return:返回所有数据库的标题等信息，json数据
		"""
		data = list(await self._execute_statement("desc player;"))
		return self.__internal_format(status=0, remaining=data)

	async def get_all_material(self, unique_id: str) -> dict:
		"""
		Used to get all numeric or string information
		用于获取所有的数字或字符串信息
		:param unique_id: 用户的唯一标识
		:return:返回所有材料名对应的值，json数据
		"""
		data = await self._execute_statement("SELECT * FROM player WHERE unique_id='" + str(unique_id) + "'")
		return self.__internal_format(status=0, remaining=data[0])

	async def get_all_supplies(self, unique_id: str) -> dict:
		data_tuple = (await self.get_all_head())["remaining"]
		heads = []
		for col in data_tuple:
			heads.append(col[0])
		content = list((await self.get_all_material(unique_id=unique_id))["remaining"])
		heads.pop(0)
		content.pop(0)
		return self.message_typesetting(status=0, message="get supplies success", data={"key": heads, "value": content})

	async def add_supplies(self, unique_id: str, key: str, value: int):
		if value <= 0: return self.message_typesetting(status=9, message="not a positive number")
		json_data = await self.__try_material(unique_id=unique_id, key=key, value=value)
		if json_data["status"] == 0:
			return self.message_typesetting(status=0, message="success", data={"keys": [key], "values": [json_data["remaining"]]})
		return self.message_typesetting(status=1, message="failure")

	async def level_up_scroll(self, unique_id: str, scroll_id: str) -> dict:
		# 0 success
		# 1 advanced reels are not upgradeable
		# 2 insufficient scroll
		# 3 unexpected parameter
		# 4 parameter error
		# 9 database operation error
		print("scroll_id：" + scroll_id)
		if scroll_id == "skill_scroll_100": return self.message_typesetting(status=1, message="advanced reels are not upgradeable!")
		try:
			scroll_id_count = await self.__get_material(unique_id=unique_id, material=scroll_id)
			if scroll_id_count < 3:
				return self.message_typesetting(status=2, message="Insufficient scroll")
			elif scroll_id == "skill_scroll_10":
				dict1 = await self.try_skill_scroll_10(unique_id=unique_id, value=-3)
				dict2 = await self.try_skill_scroll_30(unique_id=unique_id, value=1)
				if dict1["status"] == 1 or dict2["status"] == 1:
					return self.message_typesetting(status=9, message="database operation error!")
				return self.message_typesetting(status=0, message="level up scroll success!", data={"keys":["skill_scroll_10", "skill_scroll_30"], "values": [dict1["remaining"], dict2["remaining"]]})
			elif scroll_id == "skill_scroll_30":
				dict1 = await self.try_skill_scroll_30(unique_id=unique_id, value=-3)
				dict2 = await self.try_skill_scroll_100(unique_id=unique_id, value=1)
				if dict1["status"] == 1 or dict2["status"] == 1:
					return self.message_typesetting(status=9, message="database operation error!")
				return self.message_typesetting(status=0, message="level up scroll success!", data={"keys":["skill_scroll_30", "skill_scroll_100"], "values": [dict1["remaining"], dict2["remaining"]]})
			else:
				return self.message_typesetting(status=3, message="unexpected parameter --> " + scroll_id)
		except:
			return self.message_typesetting(status=9, message="parameter error!")

	async def try_all_material(self, unique_id: str, stage: int) -> dict:
		sql_stage = await self.__get_material(unique_id=unique_id, material="stage")
		if stage <= 0 or sql_stage + 1 < stage:
			print("[try_all_material] -> stage:" + str(stage))
			return self.__internal_format(status=9, remaining=0)  # abnormal data!
		if sql_stage + 1 == stage:  # 通过新关卡
			material_dict = dict(self.reward_list[stage])
			material_dict.update({"stage": 1})
		else:  # 老关卡
			material_dict = dict(self.reward_list[sql_stage])
		update_str, select_str = self.__sql_str_operating(unique_id=unique_id, material_dict=material_dict)
		data = 1 - await self._execute_statement_update(statement=update_str)  # 0, 1反转
		remaining = list(await self._execute_statement(statement=select_str))  # 数据库设置后的值
		# 通过新关卡有关卡数据的返回，老关卡没有关卡数据的返回
		return self.__internal_format(status=data, remaining=[material_dict, remaining[0]])  # 0 成功， 1 失败

	async def __update_material(self, unique_id: str, material: str, material_value: int) -> int:
		"""
		Used to set information such as numeric values
		用于设置数值等信息
		:param unique_id:用户唯一识别码
		:param material:材料名
		:param material_value:要设置的材料对应的值
		:return:返回是否更新成功的标识，1为成功，0为失败
		"""
		return await self._execute_statement_update("UPDATE player SET " + material + "=" + str(material_value) + " where unique_id='" + unique_id + "'")

	async def __get_material(self, unique_id: str, material: str) -> int or str:
		"""
		Used to get numeric or string information
		用于获取数字或字符串信息
		:param unique_id: 用户的唯一标识
		:param material:材料名
		:return:返回材料名对应的值
		"""
		data = await self._execute_statement("SELECT " + material + " FROM player WHERE unique_id='" + str(unique_id) + "'")
		return data[0][0]

	async def __set_material(self, unique_id: str, material: str, material_value: str) -> int:
		"""
		Used to set string information such as user name
		用于设置用户名等字符串信息
		:param unique_id:用户的唯一标识
		:param material:材料名
		:param material_value:要存入数据库的值
		:return:update的状态返回量，1：成功，0：失败（未改变数据统一返回0）
		"""
		return await self._execute_statement_update("UPDATE player SET " + material + "='" + str(material_value) + "' where unique_id='" + unique_id + "'")

	async def __try_material(self, unique_id: str, key: str, value: int) -> dict:
		"""
		Try to change the database information
		A status of 0 is a success and a 1 is a failure.
		Return json data format
		尝试更改数据库信息
		状态为0表示成功，1表示失败。
		返回json数据格式
		:param unique_id:用户唯一识别码
		:param key:材料名
		:param value: 改变的材料值，正数是加运算，负数是减运算，0是给值
		:return:返回数据格式为 {"status": status, "remaining": remaining}
		"""
		num = await self.__get_material(unique_id=unique_id, material=key)
		if value == 0: return self.__internal_format(0, num)
		num += value
		if num < 0: return self.__internal_format(1, num)
		if await self.__update_material(unique_id=unique_id, material=key, material_value=num) == 0:
			return self.__internal_format(1, num)
		return self.__internal_format(status=0, remaining=num)

	async def try_coin(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="coin", value=value)

	async def try_iron(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="iron", value=value)

	async def try_diamond(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="diamond", value=value)

	async def try_energy(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="energy", value=value)

	async def try_experience(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="experience", value=value)

	async def try_level(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="level", value=value)

	async def try_role(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="role", value=value)

	async def try_stage(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="stage", value=value)

	async def try_skill_scroll_10(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="skill_scroll_10", value=value)

	async def try_skill_scroll_30(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="skill_scroll_30", value=value)

	async def try_skill_scroll_100(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="skill_scroll_100", value=value)

	async def try_experience_potion(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="experience_potion", value=value)

	async def try_small_energy_potion(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="small_energy_potion", value=value)

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

	def __read_json_data(self) -> list:
		data = []
		if os.path.exists(JSON_NAME):
			data_dict = json.load(open(JSON_NAME, encoding="utf-8"))
			for key in data_dict.keys():
				data.append(data_dict[key])
		print("[__read_json_data] -> data:" + str(data))
		return data

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

	def __internal_format(self, status: int, remaining: int or tuple or list) -> dict:
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


MANAGER = BagSystemClass()
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


@ROUTES.post('/try_coin')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_coin(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_iron')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_iron(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_diamond')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_diamond(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_energy')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_energy(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_experience')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_experience(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_level')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_level(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_role')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_role(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_stage')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_stage(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_skill_scroll_10')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_skill_scroll_10(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_skill_scroll_30')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_skill_scroll_30(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_skill_scroll_100')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_skill_scroll_100(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_experience_potion')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_experience_potion(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_small_energy_potion')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_small_energy_potion(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_all_material')
async def __try_all_material(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_all_material(unique_id=post['unique_id'], stage=int(post['stage']))
	return _json_response(result)


@ROUTES.post('/get_all_head')
async def __get_all_head(request: web.Request) -> web.Response:
	result = await MANAGER.get_all_head()
	return _json_response(result)


@ROUTES.post('/get_all_material')
async def __get_all_material(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.get_all_material(unique_id=post['unique_id'])
	return _json_response(result)


@ROUTES.post('/get_all_supplies')
async def __get_all_supplies(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.get_all_supplies(unique_id=post['unique_id'])
	return _json_response(result)


@ROUTES.post('/level_up_scroll')
async def __level_up_scroll(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.level_up_scroll(unique_id=post['unique_id'], scroll_id=post["scroll_id"])
	return _json_response(result)


@ROUTES.post('/add_supplies')
async def __add_supplies(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.add_supplies(unique_id=post['unique_id'], key=post["key"], value=int(post["value"]))
	return _json_response(result)


def run():
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port=CONFIG.getint('bag_manager', 'port'))


if __name__ == "__main__":
	run()
