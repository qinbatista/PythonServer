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
from Utility import LogRecorder,EncryptionAlgorithm
from Utility.LogRecorder import LogUtility as Log
from Utility.sql_manager import game_aliya as gasql
from Utility.sql_manager import game_aliya_update as gasql_update
from Utility.AnalysisHeader import message_constructor as mc


class LevelSystemClass():
	experience_potion_basis = 100
	experience_potion_multiple = 25

	experience_basis = 10
	experience_multiple = 0

	iron_basis = 100
	iron_multiple = 25

	coin_basis = 300
	coin_multiple = 75
	item_list = [# 经验药水， 玩家经验， 铁， 金币
		{
			"item1": ["experience_potion", 100],
			"item2": ["experience", 100],
			"item3": ["iron", 100],
			"item4": ["coin", 100],
		},
		{
			"item1": ["experience_potion", 100],
			"item2": ["experience", 100],
			"item3": ["iron", 100],
			"item4": ["coin", 100],
		},
		{
			"item1": ["experience_potion", 100],
			"item2": ["experience", 100],
			"item3": ["iron", 100],
			"item4": ["coin", 100],
		},
		{
			"item1": ["experience_potion", 100],
			"item2": ["experience", 100],
			"item3": ["iron", 100],
			"item4": ["coin", 100],
		},
		{
			"item1": ["experience_potion", 100],
			"item2": ["experience", 100],
			"item3": ["iron", 100],
			"item4": ["coin", 100],
		},
		{
			"item1": ["experience_potion", 100],
			"item2": ["experience", 100],
			"item3": ["iron", 100],
			"item4": ["coin", 100],
		},
		{
			"item1": ["experience_potion", 100],
			"item2": ["experience", 100],
			"item3": ["iron", 100],
			"item4": ["coin", 100],
		},
		{
			"item1": ["experience_potion", 100],
			"item2": ["experience", 100],
			"item3": ["iron", 100],
			"item4": ["coin", 100],
		}
	]
	def __init__(self, session,*args, **kwargs):
		self.unique_id = self.__get_unique_id(session)

	def _pass_level(self, message) -> str:
		info = json.loads(message, encoding="utf-8")
		customs_clearance_time = list(info["data"].keys())[0]# 通关时间
		level_client = int(list(info["data"].values())[0])
		level, experience_potion, experience = self.__get_level()
		iron, coin = self.__get_bag_data()
		data = {
			"item1": ["experience_potion", experience_potion],
			"item2": ["experience", experience],
			"item3": ["iron", iron],
			"item4": ["coin", coin],
		}
		if level_client <= 0:
			return mc("9", "abnormal data!", data=data)
		experience_potion += self.item_list[level_client - 1]["item1"][1]
		experience += self.item_list[level_client - 1]["item2"][1]
		iron += self.item_list[level_client - 1]["item3"][1]
		coin += self.item_list[level_client - 1]["item4"][1]
		data["item1"] = ["experience_potion", experience_potion]
		data["item2"] = ["experience", experience]
		data["item3"] = ["iron", iron]
		data["item4"] = ["coin", coin]
		if level + 1 == level_client:# 通过新关卡
			if gasql_update("UPDATE player_status SET level=" + str(level_client) + ",experience_potion=" + str(experience_potion) + ",experience=" + str(experience) + " where unique_id='" + self.unique_id + "'") == 1\
				and gasql_update("UPDATE bag SET iron=" + str(iron) + ", coin=" + str(coin) + " where unique_id='" + self.unique_id + "'") == 1:
				return mc("0", "pass new level!", data=data)
			return mc("1", "abnormal data!", data=data)
		elif level >= level_client:# 通过老关卡
			if gasql_update("UPDATE player_status SET experience_potion=" + str(experience_potion) + ",experience=" + str(experience) + " where unique_id='" + self.unique_id + "'") == 1\
				and gasql_update("UPDATE bag SET iron=" + str(iron) + ", coin=" + str(coin) + " where unique_id='" + self.unique_id + "'") == 1:
				return mc("0", "pass old level!", data=data)
			return mc("3", "abnormal data!", data=data)
		return mc("4", "abnormal data!", data=data)# 通过的关卡数超过服务器上的记录数+1

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

	def __get_bag_data(self):
		sql_result = gasql("select iron, coin from bag where  unique_id='" + self.unique_id + "'")
		print("[LevelSystemClass][__get_bag_data] -> sql_result:" + str(sql_result))
		return sql_result[0][0], sql_result[0][1]

	def __get_level(self):
		sql_result = gasql("select level, experience_potion, experience from player_status where  unique_id='" + self.unique_id + "'")
		print("[LevelSystemClass][__get_level] -> sql_result:" + str(sql_result))
		return sql_result[0]

	def __get_unique_id(self,session):
		sql_result = gasql("select unique_id from userinfo where  session='" + session + "'")
		if len(sql_result) == 0:
			return ""
		else:
			self.__check_table(sql_result[0][0])
			return sql_result[0][0]

	def __check_table(self, unique_id):
		sql_result = gasql("select * from player_status where  unique_id='" + unique_id + "'")
		if len(sql_result) == 0:  # userinfo表中没得用户就不执行
			gasql("INSERT INTO player_status(unique_id) VALUES ('" + unique_id + "')")
		else:
			print("[LevelSystemClass][__check_table] -> sql_result:" + str(sql_result))


if __name__ == "__main__":
	pass

