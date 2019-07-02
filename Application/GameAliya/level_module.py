import sys
import json
import time
import os
import codecs
import threading
import pymysql
import random


def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))


from Utility import LogRecorder, EncryptionAlgorithm
from Utility.LogRecorder import LogUtility as Log
from Utility.sql_manager import game_aliya as gasql
from Utility.sql_manager import game_aliya_update as gasql_update
from Utility.AnalysisHeader import message_constructor as mc


JSON_NAME = PythonLocation() + "/Configuration/level_reward_config.json"


class LevelSystemClass:
	experience_potion_basis = 100
	experience_potion_multiple = 25

	experience_basis = 10
	experience_multiple = 0

	iron_basis = 100
	iron_multiple = 25

	coin_basis = 300
	coin_multiple = 75

	def __init__(self, session, *args, **kwargs):
		self.unique_id = self.__get_unique_id(session)
		self.reward_list = read_json_data()

	def _pass_level(self, message) -> str:
		info = json.loads(message, encoding="utf-8")
		customs_clearance_time = list(info["data"].keys())[0]  # 通关时间
		level_client = int(list(info["data"].values())[0])

		player_status_title_list = self.__get_title_list(table_name="player_status")
		player_status_content_list = self.__get_content_tuple(table_name="player_status")
		bag_title_list = self.__get_title_list(table_name="bag")
		bag_content_tuple = self.__get_content_tuple(table_name="bag")
		item_dict = self.__structure_item_dict(player_status_title_list, player_status_content_list, bag_title_list, bag_content_tuple)

		data_len = len(self.reward_list[0].keys()) + 1
		self.reward_list[0] = self.__structure_data(self.reward_list[0], item_dict, data_len)
		# 异常触发，后续方法不会进行
		if level_client <= 0 or (item_dict["level"] + 1) < level_client:
			return mc("9", "abnormal data!", data=self.reward_list[0])

		# 改变所有该变的变量
		if item_dict["level"] + 1 == level_client:  # 通过新关卡
			item_dict["level"] = level_client

		data = self.reward_list[level_client]  # 获得奖励
		data_len = len(data.keys()) + 1
		data = self.__structure_data(data, item_dict, data_len)

		player_status_str = self.__sql_str_operating(table_name="player_status", title_list=player_status_title_list, item_dict=item_dict)
		bag_str = self.__sql_str_operating(table_name="bag", title_list=bag_title_list, item_dict=item_dict)

		if gasql_update(player_status_str) == 1 or gasql_update(bag_str) == 1:
			data["item" + str(data_len)][1] = item_dict["level"]
			return mc("0", "passed customs!", data=data)
		return mc("1", "abnormal data!", data=self.reward_list[0])

	def __structure_item_dict(self, player_status_title_list, player_status_content_list, bag_title_list, bag_content_tuple) -> dict:
		item_dict = {}
		for i in range(len(player_status_title_list)):
			item_dict.update({player_status_title_list[i]: player_status_content_list[i]})
		print("[LevelSystemClass][__structure_item_dict] -> item_dict:" + str(item_dict))

		for i in range(len(bag_title_list)):
			item_dict.update({bag_title_list[i]: bag_content_tuple[i]})
		print("[LevelSystemClass][__structure_item_dict] -> item_dict:" + str(item_dict))

		return item_dict

	def __sql_str_operating(self, table_name, title_list, item_dict) -> str:
		heard_str = "UPDATE %s SET " % table_name
		end_str = " where unique_id='%s'" % self.unique_id
		result_str = ""
		temp_list = []
		for i in range(len(title_list)):
			if title_list[i] != "unique_id":
				temp_list.append(item_dict[title_list[i]])
				if i != len(title_list) - 1:
					result_str += title_list[i] + "=%s, "
				else:
					result_str += title_list[i] + "=%s"
		result_str = heard_str + result_str + end_str
		print("[LevelSystemClass][__sql_str_operating] -> result_str:" + result_str)
		print("[LevelSystemClass][__sql_str_operating] -> temp_list:" + str(temp_list))

		return result_str % tuple(temp_list)

	def __get_title_list(self, table_name) -> list:
		sql_result = gasql("desc " + table_name + ";")
		col_list = []
		for col in sql_result:
			col_list.append(col[0])
		return col_list

	def __get_content_tuple(self, table_name) -> tuple:
		sql_result = gasql("select * from " + table_name + " where  unique_id='" + self.unique_id + "'")
		print("[LevelSystemClass][__get_table_content] -> sql_result:" + str(sql_result))
		return sql_result[0]

	def __structure_data(self, data, item_dict, data_len) -> dict:
		temp_list = []
		for key in data.keys():
			temp_list.append(data[key])
		temp_data = {}
		for i in range(1, data_len):
			reward = "reward" + str(i)
			temp_data.update({reward: temp_list[i - 1]})
		data = temp_data

		for i in range(1, data_len):
			reward = "reward" + str(i)
			key = data[reward][0]
			item_dict[key] += data[reward][1]
			data.update({"item" + str(i): [key, item_dict[key]]})
		data.update({"item" + str(data_len): ["level", item_dict["level"]]})

		return data

	# def __random_data(self) -> dict:
	# 	data = {"item1": []}
	# 	if self.item_list_count == 3:
	# 		iron, diamonds, coin = self.__get_bag_data()
	# 		random_iron, random_diamonds, random_coin = random.randint(27, 32), random.randint(0, 10)//8, random.randint(187, 222)
	# 		print("[LevelSystemClass][__random_data] -> random_iron, random_diamonds, random_coin:" + str(random_iron), str(random_diamonds), str(random_coin))
	# 		iron, diamonds, coin = iron + random_iron, diamonds + random_diamonds, coin + random_coin
	# 		if gasql_update("UPDATE bag SET iron=" + str(iron) + ", diamonds=" + str(diamonds) + ", coin=" + str(coin) + " where unique_id='" + self.unique_id + "'") == 1:
	# 			data.update({"item1": ["iron", iron]})
	# 			data.update({"item2": ["diamonds", diamonds]})
	# 			data.update({"item3": ["coin", coin]})
	# 			return data
	# 		return data
	#
	# 	return data

	def __get_unique_id(self, session) -> str:
		sql_result = gasql("select unique_id from userinfo where  session='" + session + "'")
		if len(sql_result) == 0:
			return ""
		else:
			self.__check_table(sql_result[0][0])
			return sql_result[0][0]

	def __check_table(self, unique_id) -> None:
		sql_result = gasql("select * from player_status where  unique_id='" + unique_id + "'")
		if len(sql_result) == 0:  # userinfo表中没得用户就不执行
			gasql("INSERT INTO player_status(unique_id) VALUES ('" + unique_id + "')")
		else:
			print("[LevelSystemClass][__check_table] -> sql_result:" + str(sql_result))


def read_json_data() -> list:
	data = []
	if os.path.exists(JSON_NAME):
		data_dict = json.load(open(JSON_NAME, encoding="utf-8"))
		for key in data_dict.keys():
			data.append(data_dict[key])
	print("[level_module.py][read_json_data] -> data:" + str(data))
	return data


if __name__ == "__main__":
	pass
