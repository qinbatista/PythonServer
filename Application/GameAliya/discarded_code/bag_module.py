import random
import json
import os
import tormysql
from aiohttp import web


def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))

from Utility.sql_manager import game_aliya as gasql
from Utility.sql_manager import game_aliya_update as gasql_update
from Utility.sql_manager import game_aliya_table as gasql_t
from Utility.AnalysisHeader import message_constructor as mc


# Format the information
def message_typesetting(status: int, message: str, data: dict={}) -> dict:
	return {"status": status, "message": message, "random": random.randint(-1000, 1000), "data": data}


class BagSystemClass:
	def __init__(self, *args, **kwargs):
		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive.
		# TODO verify that this is true :D
		self._pool = tormysql.ConnectionPool(max_connections=10, host='192.168.1.102', user='root', passwd='lukseun', db='aliya', charset='utf8')

	# It is helpful to define a private method that you can simply pass
	# an SQL command as a string and it will execute. Call this method
	# whenever you issue an SQL statement.
	async def _execute_statement(self, statement: str) -> tuple:
		'''
		Executes the given statement and returns the result.
		执行给定的语句并返回结果。
		'''
		async with await self._pool.Connection() as conn:
			async with conn.cursor() as cursor:
				await cursor.execute(statement)
				data = cursor.fetchall()
				return data

	async def _execute_statement_update(self, statement: str) -> int:
		'''
		Execute the update or set statement and return the result.
		执行update或set语句并返回结果。
		'''
		async with await self._pool.Connection() as conn:
			async with conn.cursor() as cursor:
				return await cursor.execute(statement)

	# Used to set information such as numeric values
	# 用于设置数值等信息
	async def __update_material(self, unique_id: str, material: str, material_value: int) -> int:
		return await self._execute_statement_update("UPDATE player SET " + material + "=" + str(material_value) + " where unique_id='" + unique_id + "'")

	# Used to get numeric or string information
	# 用于获取数字或字符串信息
	async def __get_material(self, unique_id: str, material: str) -> int or str:
		data = await self._execute_statement("SELECT " + material + " FROM player WHERE unique_id='" + str(unique_id) + "'")
		return data[0][0]

	# Used to set string information such as user name
	# 用于设置用户名等字符串信息
	async def __set_material(self, unique_id: str, material: str, material_value: str) -> int:
		return await self._execute_statement_update("UPDATE player SET " + material + "='" + str(material_value) + "' where unique_id='" + unique_id + "'")

	# Internal json formatted information
	# 内部json格式化信息
	def __internal_format(self, status: int, remaining: int) -> dict:
		return {"status": status, "remaining": remaining}

	# Try to change the database information
	# A status of 0 is a success and a 1 is a failure.
	# Return json data format
	# 尝试更改数据库信息
	# 状态为0表示成功，1表示失败。
	# 返回json数据格式
	async def __try_remove_material(self, unique_id: str,key: str, value: int) -> dict:
		num = await self.__get_material(unique_id=unique_id, material=key)
		if value == 0: return self.__internal_format(0, num)
		num += value
		if num < 0: return self.__internal_format(1, num)
		if await self.__update_material(unique_id=unique_id, material=key, material_value=num) == 0:
			return self.__internal_format(1, num)
		return self.__internal_format(0, num)

	async def try_remove_coin(self, unique_id: str, value: int) -> dict:
		return await self.__try_remove_material(unique_id=unique_id, key="coin", value=value)

	async def try_remove_iron(self, unique_id: str, value: int) -> dict:
		return await self.__try_remove_material(unique_id=unique_id, key="iron", value=value)

	async def try_remove_diamond(self, unique_id: str, value: int) -> dict:
		return await self.__try_remove_material(unique_id=unique_id, key="diamond", value=value)

	async def try_remove_energy(self, unique_id: str, value: int) -> dict:
		return await self.__try_remove_material(unique_id=unique_id, key="energy", value=value)

	async def try_remove_experience(self, unique_id: str, value: int) -> dict:
		return await self.__try_remove_material(unique_id=unique_id, key="experience", value=value)

	async def try_remove_level(self, unique_id: str, value: int) -> dict:
		return await self.__try_remove_material(unique_id=unique_id, key="level", value=value)

	async def try_remove_role(self, unique_id: str, value: int) -> dict:
		return await self.__try_remove_material(unique_id=unique_id, key="role", value=value)

	async def try_remove_stage(self, unique_id: str, value: int) -> dict:
		return await self.__try_remove_material(unique_id=unique_id, key="stage", value=value)

	async def try_remove_skill_scroll_10(self, unique_id: str, value: int) -> dict:
		return await self.__try_remove_material(unique_id=unique_id, key="skill_scroll_10", value=value)

	async def try_remove_skill_scroll_30(self, unique_id: str, value: int) -> dict:
		return await self.__try_remove_material(unique_id=unique_id, key="skill_scroll_30", value=value)

	async def try_remove_skill_scroll_100(self, unique_id: str, value: int) -> dict:
		return await self.__try_remove_material(unique_id=unique_id, key="skill_scroll_100", value=value)

	async def try_remove_experience_potion(self, unique_id: str, value: int) -> dict:
		return await self.__try_remove_material(unique_id=unique_id, key="experience_potion", value=value)

	async def try_remove_small_energy_potion(self, unique_id: str, value: int) -> dict:
		return await self.__try_remove_material(unique_id=unique_id, key="small_energy_potion", value=value)

	async def __add_material(self, unique_id: str, key: str, value: int) -> dict:
		if value <= 0: return message_typesetting(status=1, message="the added material must be greater than 0")
		material_json = await self.__try_remove_material(unique_id=unique_id, key=key, value=value)
		if material_json["status"] == 1: return message_typesetting(status=2, message="database operation error")
		return message_typesetting(status=0, message="get success!", data={"item1": [key, material_json["remaining"]]})

	async def add_coin(self, unique_id: str, value: int) -> dict:
		return await self.__add_material(unique_id=unique_id, key="coin", value=value)

	async def add_iron(self, unique_id: str, value: int) -> dict:
		return await self.__add_material(unique_id=unique_id, key="iron", value=value)

	async def add_diamond(self, unique_id: str, value: int) -> dict:
		return await self.__add_material(unique_id=unique_id, key="diamond", value=value)

	async def add_energy(self, unique_id: str, value: int) -> dict:
		return await self.__add_material(unique_id=unique_id, key="energy", value=value)

	async def add_experience(self, unique_id: str, value: int) -> dict:
		return await self.__add_material(unique_id=unique_id, key="experience", value=value)

	async def add_level(self, unique_id: str, value: int) -> dict:
		return await self.__add_material(unique_id=unique_id, key="level", value=value)

	async def add_role(self, unique_id: str, value: int) -> dict:
		return await self.__add_material(unique_id=unique_id, key="role", value=value)

	async def add_stage(self, unique_id: str, value: int) -> dict:
		return await self.__add_material(unique_id=unique_id, key="stage", value=value)

	async def add_skill_scroll_10(self, unique_id: str, value: int) -> dict:
		return await self.__add_material(unique_id=unique_id, key="skill_scroll_10", value=value)

	async def add_skill_scroll_30(self, unique_id: str, value: int) -> dict:
		return await self.__add_material(unique_id=unique_id, key="skill_scroll_30", value=value)

	async def add_skill_scroll_100(self, unique_id: str, value: int) -> dict:
		return await self.__add_material(unique_id=unique_id, key="skill_scroll_100", value=value)

	async def add_experience_potion(self, unique_id: str, value: int) -> dict:
		return await self.__add_material(unique_id=unique_id, key="experience_potion", value=value)

	async def add_small_energy_potion(self, unique_id: str, value: int) -> dict:
		return await self.__add_material(unique_id=unique_id, key="small_energy_potion", value=value)


	# region 不需要的方法
	# def _increase_item_quantity(self, item_id, item_quantity):
	# 	try:
	# 		self.item_list_count += 1
	# 		gasql("UPDATE bag SET " + item_id + "=" + item_id + " +" + item_quantity + " WHERE unique_id='" + self.unique_id + "'")
	# 		result_quantity = gasql("select " + item_id + " from bag where  unique_id='" + self.unique_id + "'")
	# 		dc = {"item" + str(self.item_list_count): [item_id, result_quantity[0][0]]}
	# 		return dc
	# 	except:
	# 		return {"scroll_error": "1"}
	#
	# def _increase_supplies(self, message_info):
	# 	message_dic = json.loads(message_info, encoding="utf-8")
	# 	title_list = self.__get_title_list("bag")
	# 	content_list = self.__get_content_list("bag")
	# 	return_dic = {}
	# 	for key in message_dic["data"].keys():
	# 		if key not in title_list:
	# 			return mc("1", "increase supplies failed", {key: 0})
	# 		value = content_list[title_list.index(key)] + int(message_dic["data"][key])
	# 		content_list[title_list.index(key)] = value
	# 		return_dic.update({"item" + str(len(return_dic.keys()) + 1): [key, value]})
	# 	content_list.pop(title_list.index("unique_id"))
	# 	if gasql_update(
	# 			self.__sql_str_operating(table_name="bag", title_list=title_list, content_list=content_list)) == 1:
	# 		return mc("0", "increase supplies success", return_dic)
	# 	return mc("2", "increase supplies failed")
	#
	# def _random_gift(self, message_info):
	# 	print("[BagSystemClass][_random_gift] -> 方法未写！")
	# 	return mc("9", "random gift")
	#
	# def _get_all_supplies(self, message_info):
	# 	"""
	# 	give all skills' level to client
	# 	"""
	# 	table, result = gasql_t("select * from bag where unique_id='" + self.unique_id + "'")
	# 	data_dic = {}
	# 	for i in range(1, len(result[0])):
	# 		data_dic.update({"item" + str(i): [table[i][0], result[0][i]]})
	# 	return mc("0", "get all suypplies", data_dic)
	#
	# def __sql_str_operating(self, table_name, title_list, content_list) -> str:
	# 	heard_str = "UPDATE %s SET " % table_name
	# 	end_str = " where unique_id='%s'" % self.unique_id
	# 	result_str = ""
	# 	for i in range(len(title_list)):
	# 		if title_list[i] != "unique_id":
	# 			if i != len(title_list) - 1:
	# 				result_str += title_list[i] + "=%s, "
	# 			else:
	# 				result_str += title_list[i] + "=%s"
	# 	result_str = heard_str + result_str + end_str
	# 	print("[BagSystemClass][__sql_str_operating] -> result_str:" + result_str)
	#
	# 	return result_str % tuple(content_list)
	#
	# def __get_title_list(self, table_name) -> list:
	# 	sql_result = gasql("desc " + table_name + ";")
	# 	col_list = []
	# 	for col in sql_result:
	# 		col_list.append(col[0])
	# 	return col_list
	#
	# def __get_content_list(self, table_name) -> list:
	# 	sql_result = gasql("select * from " + table_name + " where  unique_id='" + self.unique_id + "'")
	# 	print("[BagSystemClass][__get_table_content] -> sql_result:" + str(sql_result))
	# 	return list(sql_result[0])
	#
	# def __get_unique_id(self, token):
	# 	sql_result = gasql("select unique_id from userinfo where  token='" + token + "'")
	# 	if len(sql_result[0][0]) <= 0:
	# 		return ""
	# 	else:
	# 		self.__check_table(sql_result[0][0])
	# 		return sql_result[0][0]
	#
	# def __check_table(self, unique_id):
	# 	sql_result = gasql("select count(unique_id) from bag where  unique_id='" + unique_id + "'")
	# 	if sql_result[0][0] <= 0:
	# 		gasql("INSERT INTO bag(unique_id) VALUES ('" + unique_id + "')")
	#
	# def __get_skill_level(self, skill_id):
	# 	"""
	# 	get skill level
	# 	"""
	# 	sql_result = gasql("select " + skill_id + " from skill where unique_id='" + self.unique_id + "'")
	# 	return sql_result[0][0]
	#
	# def _level_up_scroll(self, message_info):
	# 	message_dic = eval(message_info)
	# 	scroll_id_name = ""
	# 	level_up_scroll_name = ""
	# 	if "scroll_skill_10" in message_dic["data"].keys():
	# 		scroll_id_name = "scroll_skill_10"
	# 		level_up_scroll_name = "scroll_skill_30"
	# 		quantity = message_dic["data"]["scroll_skill_10"]
	# 	elif "scroll_skill_30" in message_dic["data"].keys():
	# 		scroll_id_name = "scroll_skill_30"
	# 		level_up_scroll_name = "scroll_skill_100"
	# 		quantity = message_dic["data"]["scroll_skill_30"]
	# 	else:
	# 		return mc("2", "illegal scroll level up ")
	# 	sql_result = gasql(
	# 		"select " + scroll_id_name + "," + level_up_scroll_name + " from bag where unique_id='" + self.unique_id + "'")
	# 	current_scroll = sql_result[0][0]
	# 	level_up_scroll = sql_result[0][1]
	# 	if current_scroll < 3 or int(quantity) < 3:
	# 		return mc("1", "scroll is not eought", {"item1": [str(scroll_id_name), str(current_scroll)],
	# 		                                        "item2": [str(level_up_scroll_name), str(level_up_scroll)]})
	# 	else:
	# 		gasql("UPDATE bag SET " + scroll_id_name + "= " + scroll_id_name + "-" + str(
	# 			3) + " WHERE unique_id='" + self.unique_id + "'")
	# 		gasql("UPDATE bag SET " + level_up_scroll_name + "= " + level_up_scroll_name + "+" + str(
	# 			1) + " WHERE unique_id='" + self.unique_id + "'")
	# 		return mc("0", "level up success", {"item1": [str(scroll_id_name), str(current_scroll - 3)],
	# 		                                    "item2": [str(level_up_scroll_name), str(level_up_scroll + 1)]})
# endregion

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


@ROUTES.post('/try_remove_coin')
async def __try_remove_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_remove_coin(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_remove_iron')
async def __try_remove_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_remove_iron(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_remove_diamond')
async def __try_remove_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_remove_diamond(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_remove_energy')
async def __try_remove_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_remove_energy(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_remove_experience')
async def __try_remove_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_remove_experience(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_remove_level')
async def __try_remove_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_remove_level(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_remove_role')
async def __try_remove_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_remove_role(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_remove_stage')
async def __try_remove_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_remove_stage(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_remove_skill_scroll_10')
async def __try_remove_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_remove_skill_scroll_10(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_remove_skill_scroll_30')
async def __try_remove_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_remove_skill_scroll_30(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_remove_skill_scroll_100')
async def __try_remove_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_remove_skill_scroll_100(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_remove_experience_potion')
async def __try_remove_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_remove_experience_potion(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/try_remove_small_energy_potion')
async def __try_remove_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_remove_small_energy_potion(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


# The following methods are used for client access
# 以下方法用于客户端访问
@ROUTES.post('/add_coin')
async def __add_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.add_coin(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/add_iron')
async def __add_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.add_iron(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/add_diamond')
async def __add_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.add_diamond(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/add_energy')
async def __add_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.add_energy(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/add_experience')
async def __add_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.add_experience(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/add_level')
async def __add_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.add_level(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/add_role')
async def __add_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.add_role(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/add_stage')
async def __add_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.add_stage(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/add_skill_scroll_10')
async def __add_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.add_skill_scroll_10(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/add_skill_scroll_30')
async def __add_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.add_skill_scroll_30(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/add_skill_scroll_100')
async def __add_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.add_skill_scroll_100(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/add_experience_potion')
async def __add_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.add_experience_potion(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


@ROUTES.post('/add_small_energy_potion')
async def __add_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.add_small_energy_potion(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)


def run(port):
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port=port)


if __name__ == "__main__":
	run(9999)
