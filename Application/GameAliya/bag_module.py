import sys
import json
import time
import os
import codecs
import threading
import pymysql
import datetime
import random


def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))


from Utility import LogRecorder, EncryptionAlgorithm
from Utility.LogRecorder import LogUtility as Log
from Utility.sql_manager import game_aliya as gasql
from Utility.sql_manager import game_aliya_update as gasql_update
from Utility.sql_manager import game_aliya_table as gasql_t
from Utility.AnalysisHeader import message_constructor as mc


class BagSystemClass():
	def __init__(self, session, *args, **kwargs):
		self.unique_id = self.__get_unique_id(session)


	def _increase_supplies(self, message_info):
		message_dic = json.loads(message_info, encoding="utf-8")
		title_list = self.__get_title_list("bag")
		content_list = self.__get_content_list("bag")
		return_dic = {}
		for key in message_dic["data"].keys():
			if key not in title_list:
				return mc("1", "increase supplies failed", {key: 0})
			value = content_list[title_list.index(key)] + int(message_dic["data"][key])
			content_list[title_list.index(key)] = value
			return_dic.update({"item" + str(len(return_dic.keys()) + 1): [key, value]})
		content_list.pop(title_list.index("unique_id"))
		if gasql_update(self.__sql_str_operating(table_name="bag", title_list=title_list, content_list=content_list)) == 1:
			return mc("0", "increase supplies success", return_dic)
		return mc("2", "increase supplies failed")

	def _random_gift(self, message_info):
		print("[BagSystemClass][_random_gift] -> 方法未写！")
		return mc("9", "random gift")

	def _get_all_supplies(self, message_info):
		"""
		give all skills' level to client
		"""
		table, result = gasql_t("select * from bag where unique_id='" + self.unique_id + "'")
		data_dic = {}
		for i in range(1, len(result[0])):
			data_dic.update({"item" + str(i): [table[i][0], result[0][i]]})
		return mc("0", "get all suypplies", data_dic)

	def __sql_str_operating(self, table_name, title_list, content_list) -> str:
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

	def __get_title_list(self, table_name) -> list:
		sql_result = gasql("desc " + table_name + ";")
		col_list = []
		for col in sql_result:
			col_list.append(col[0])
		return col_list

	def __get_content_list(self, table_name) -> list:
		sql_result = gasql("select * from " + table_name + " where  unique_id='" + self.unique_id + "'")
		print("[BagSystemClass][__get_table_content] -> sql_result:" + str(sql_result))
		return list(sql_result[0])

	def __get_unique_id(self, session):
		sql_result = gasql("select unique_id from userinfo where  session='" + session + "'")
		if len(sql_result[0][0]) <= 0:
			return ""
		else:
			self.__check_table(sql_result[0][0])
			return sql_result[0][0]

	def __check_table(self, unique_id):
		sql_result = gasql("select count(unique_id) from bag where  unique_id='" + unique_id + "'")
		if sql_result[0][0] <= 0:
			gasql("INSERT INTO bag(unique_id) VALUES ('" + unique_id + "')")

	def __get_skill_level(self, skill_id):
		"""
		get skill level
		"""
		sql_result = gasql("select " + skill_id + " from skill where unique_id='" + self.unique_id + "'")
		return sql_result[0][0]

	def _level_up_scroll(self, message_info):
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


if __name__ == "__main__":
	pass
