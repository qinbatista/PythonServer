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
		{# 0
			"item1": ["experience_potion", 0],
			"item2": ["experience", 0],
			"item3": ["iron", 0],
			"item4": ["coin", 0],
			"item5": ["level", 0],
		},
		{# 1
			"item1": ["experience_potion", 100],
			"item2": ["experience", 10],
			"item3": ["iron", 100],
			"item4": ["coin", 300],
			"item5": ["level", 0],
		},
		{# 2
			"item1": ["experience_potion", 125],
			"item2": ["experience", 10],
			"item3": ["iron", 125],
			"item4": ["coin", 375],
			"item5": ["level", 0],
		},
		{# 3
			"item1": ["experience_potion", 150],
			"item2": ["experience", 10],
			"item3": ["iron", 150],
			"item4": ["coin", 450],
			"item5": ["level", 0],
		},
		{
			"item1": ["experience_potion", 175],
			"item2": ["experience", 10],
			"item3": ["iron", 175],
			"item4": ["coin", 525],
			"item5": ["level", 0],
		},
		{
			"item1": ["experience_potion", 200],
			"item2": ["experience", 10],
			"item3": ["iron", 200],
			"item4": ["coin", 600],
			"item5": ["level", 0],
		},
		{
			"item1": ["experience_potion", 225],
			"item2": ["experience", 10],
			"item3": ["iron", 225],
			"item4": ["coin", 675],
			"item5": ["level", 0],
		},
		{
			"item1": ["experience_potion", 250],
			"item2": ["experience", 10],
			"item3": ["iron", 250],
			"item4": ["coin", 750],
			"item5": ["level", 0],
		},
		{
			"item1": ["experience_potion", 275],
			"item2": ["experience", 10],
			"item3": ["iron", 275],
			"item4": ["coin", 825],
			"item5": ["level", 0],
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

		demo_data = self.item_list[0]
		demo_data["item1"].append(experience_potion)
		demo_data["item2"].append(experience)
		demo_data["item3"].append(iron)
		demo_data["item4"].append(coin)
		demo_data["item5"].append(level)
		if level_client <= 0 or (level + 1) < level_client:
			return mc("9", "abnormal data!", data=demo_data)

		data = self.item_list[level_client]
		experience_potion += data["item1"][1]
		experience += data["item2"][1]
		iron += data["item3"][1]
		coin += data["item4"][1]
		data["item1"].append(experience_potion)
		data["item2"].append(experience)
		data["item3"].append(iron)
		data["item4"].append(coin)

		if level + 1 == level_client:# 通过新关卡
			if gasql_update("UPDATE player_status SET level=" + str(level_client) + ",experience_potion=" + str(experience_potion) + ",experience=" + str(experience) + " where unique_id='" + self.unique_id + "'") == 1\
				and gasql_update("UPDATE bag SET iron=" + str(iron) + ", coin=" + str(coin) + " where unique_id='" + self.unique_id + "'") == 1:
				data["item5"][1] = 1
				data["item5"].append(level_client)
				return mc("0", "pass new level!", data=data)
			return mc("1", "abnormal data!", data=demo_data)
		else:# 通过老关卡
			if gasql_update("UPDATE player_status SET experience_potion=" + str(experience_potion) + ",experience=" + str(experience) + " where unique_id='" + self.unique_id + "'") == 1\
				and gasql_update("UPDATE bag SET iron=" + str(iron) + ", coin=" + str(coin) + " where unique_id='" + self.unique_id + "'") == 1:
				data["item5"].append(level)
				return mc("0", "pass old level!", data=data)
			return mc("2", "abnormal data!", data=demo_data)

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

