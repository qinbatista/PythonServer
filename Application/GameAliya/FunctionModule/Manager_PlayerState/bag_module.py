import sys
import json
import time
import os
import codecs
import threading
import pymysql
import datetime
import random
import json
import random
import tormysql
from aiohttp import web
from aiohttp import ClientSession

def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))




class BagSystemClass():
	def __init__(self):
		pass

	async def increase_item_quantity(self, item_id, item_quantity):
		try:
			self.item_list_count += 1
			gasql("UPDATE bag SET " + item_id + "=" + item_id + " +" + item_quantity + " WHERE unique_id='" + self.unique_id + "'")
			result_quantity = gasql("select " + item_id + " from bag where  unique_id='" + self.unique_id + "'")
			dc = {"item" + str(self.item_list_count): [item_id, result_quantity[0][0]]}
			return dc
		except:
			return {"scroll_error": "1"}

	async def increase_supplies(self, message_info):
		message_dic = json.loads(message_info, encoding="utf-8")
		title_list = self.__get_title_list("bag")
		content_list = self.__get_content_list("bag")
		return_dic = {}
		for key in message_dic["data"].keys():
			if key not in title_list:
				return message_typesetting("1", "increase supplies failed", {key: 0})
			value = content_list[title_list.index(key)] + int(message_dic["data"][key])
			content_list[title_list.index(key)] = value
			return_dic.update({"item" + str(len(return_dic.keys()) + 1): [key, value]})
		content_list.pop(title_list.index("unique_id"))
		if gasql_update(
				self.__sql_str_operating(table_name="bag", title_list=title_list, content_list=content_list)) == 1:
			return message_typesetting("0", "increase supplies success", return_dic)
		return message_typesetting("2", "increase supplies failed")

	async def random_gift(self, message_info):
		print("[BagSystemClass][_random_gift] -> 方法未写！")
		return message_typesetting("9", "random gift")

	async def get_all_supplies(self, message_info):
		"""
		give all skills' level to client
		"""
		table, result = gasql_t("select * from bag where unique_id='" + self.unique_id + "'")
		data_dic = {}
		for i in range(1, len(result[0])):
			data_dic.update({"item" + str(i): [table[i][0], result[0][i]]})
		return message_typesetting("0", "get all suypplies", data_dic)

	async def level_up_scroll(self, unique_id,scroll_id_name):
		print("aaaaa")
		return
		message_dic = eval(message_info)
		scroll_id_name = ""
		level_up_scroll_name = ""
		if "scroll_skill_10" in message_dic["data"].keys():
			scroll_id_name = "scroll_skill_10"
			level_up_scroll_name = "scroll_skill_30"
			quantity = message_dic["data"]["scroll_skill_10"]
		elif "scroll_skill_30" in message_dic["data"].keys():
			scroll_id_name = "scroll_skill_30"
			level_up_scroll_name = "scroll_skill_100"
			quantity = message_dic["data"]["scroll_skill_30"]
		else:
			return mc("2", "illegal scroll level up ")
		sql_result = gasql(
			"select " + scroll_id_name + "," + level_up_scroll_name + " from bag where unique_id='" + self.unique_id + "'")
		current_scroll = sql_result[0][0]
		level_up_scroll = sql_result[0][1]
		if current_scroll < 3 or int(quantity) < 3:
			return mc("1", "scroll is not eought", {"item1": [str(scroll_id_name), str(current_scroll)],
			                                        "item2": [str(level_up_scroll_name), str(level_up_scroll)]})
		else:
			gasql("UPDATE bag SET " + scroll_id_name + "= " + scroll_id_name + "-" + str(
				3) + " WHERE unique_id='" + self.unique_id + "'")
			gasql("UPDATE bag SET " + level_up_scroll_name + "= " + level_up_scroll_name + "+" + str(
				1) + " WHERE unique_id='" + self.unique_id + "'")
			return mc("0", "level up success", {"item1": [str(scroll_id_name), str(current_scroll - 3)],
			                                    "item2": [str(level_up_scroll_name), str(level_up_scroll + 1)]})
	async def get_content_list(self, table_name) -> list:
		sql_result = gasql("select * from " + table_name + " where  unique_id='" + self.unique_id + "'")
		print("[BagSystemClass][__get_table_content] -> sql_result:" + str(sql_result))
		return list(sql_result[0])

	async def get_skill_level(self, skill_id):
		"""
		get skill level
		"""
		sql_result = gasql("select " + skill_id + " from skill where unique_id='" + self.unique_id + "'")
		return sql_result[0][0]

	# It is helpful to define a private method that you can simply pass
	# an SQL command as a string and it will execute. Call this method
	# whenever you issue an SQL statement.
	async def _execute_statement(self, statement: str) -> tuple:
		'''
		Executes the given statement and returns the result.
		'''
		async with await self._pool.Connection() as conn:
			async with conn.cursor() as cursor:
				await cursor.execute(statement)
				data = cursor.fetchall()
				return data

	async def _execute_statement_update(self, statement: str) -> int:
		'''
		Executes the given statement and returns the result.
		'''
		async with await self._pool.Connection() as conn:
			async with conn.cursor() as cursor:
				data = await cursor.execute(statement)
				return data

	def sql_str_operating(self, table_name, title_list, content_list) -> str:
		heard_str = "UPDATE %s SET " % table_name
		end_str = " where unique_id='%s'" % self.unique_id
		result_str = ""
		for i in range(len(title_list)):
			if title_list[i] != "unique_id":
				if i != len(title_list) - 1:
					result_str += title_list[i] + "=%s, "
				else:
					result_str += title_list[i] + "=%s"
		result_str = heard_str + result_str + end_str
		print("[BagSystemClass][__sql_str_operating] -> result_str:" + result_str)
		return result_str % tuple(content_list)

	def get_title_list(self, table_name) -> list:
		sql_result = gasql("desc " + table_name + ";")
		col_list = []
		for col in sql_result:
			col_list.append(col[0])
		return col_list

	def message_typesetting(self, status: int, message: str, data: dict=None) -> str:
		result = '{"status":"%s","message":"%s","random":"%s","data":{}}' % (
		status, message, str(random.randint(-1000, 1000)))
		# 分段保存字符串
		if data: result = result.replace("{}", json.dumps(data))
		return result
# Part (2 / 2)
MANAGER = BagSystemClass()  # we want to define a single instance of the class
ROUTES = web.RouteTableDef()

def _json_response(body: str = '', **kwargs) -> web.Response:
	'''
	A simple wrapper for aiohttp.web.Response return value.
	'''
	kwargs['body'] = json.dumps(body or kwargs['kwargs']).encode('utf-8')
	kwargs['content_type'] = 'text/json'
	return web.Response(**kwargs)

@ROUTES.post('/get_all_supplies')
async def __get_all_supplies(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.get_all_supplies(post['unique_id'], post['weapon'], int(post['iron']))
	return _json_response(data)

@ROUTES.post('/increase_supplies')
async def __increase_supplies(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.increase_supplies(post['unique_id'], post['weapon'], post['passive'])
	return _json_response(data)

@ROUTES.post('/random_gift_segment')
async def __random_gift_segment(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.random_gift_segment(post['unique_id'], post['weapon'])
	return _json_response(data)

@ROUTES.post('/level_up_scroll')
async def __level_up_scroll(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.level_up_scroll(post['unique_id'], post['scroll_id'])
	return _json_response(data)

if __name__ == "__main__":
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port=9999)
