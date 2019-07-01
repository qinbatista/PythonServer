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


class LevelSystemClass:
	experience_potion_basis = 100
	experience_potion_multiple = 25

	experience_basis = 10
	experience_multiple = 0

	iron_basis = 100
	iron_multiple = 25

	coin_basis = 300
	coin_multiple = 75
	reward_list = [  # 经验药水， 玩家经验， 铁， 金币
		{  # 0
			"reward1": ["experience_potion", 0],
			"reward2": ["experience", 0],
			"reward3": ["iron", 0],
			"reward4": ["coin", 0],
			"reward5": ["small_energy_potion", 0]
		},
		{  # 1
			"reward1": ["experience_potion", 100],
			"reward2": ["experience", 10],
			"reward3": ["iron", 100],
			"reward4": ["coin", 300],
			"reward5": ["small_energy_potion", 1]
		},
		{  # 2
			"reward1": ["experience_potion", 125],
			"reward2": ["experience", 10],
			"reward3": ["iron", 125],
			"reward4": ["small_energy_potion", 1],
			"reward5": ["coin", 375]
		},
		{  # 3
			"reward1": ["experience_potion", 150],
			"reward2": ["experience", 10],
			"reward3": ["iron", 150],
			"reward4": ["coin", 450],
			"reward5": ["small_energy_potion", 1]
		},
		{  # 4
			"reward1": ["experience_potion", 175],
			"reward2": ["experience", 10],
			"reward3": ["iron", 175],
			"reward4": ["coin", 525],
			"reward5": ["small_energy_potion", 1]
		},
		{  # 5
			"reward1": ["experience_potion", 200],
			"reward2": ["experience", 10],
			"reward3": ["iron", 200],
			"reward4": ["coin", 600],
			"reward5": ["small_energy_potion", 1]
		},
		{  # 6
			"reward1": ["experience_potion", 225],
			"reward2": ["experience", 10],
			"reward3": ["iron", 225],
			"reward4": ["coin", 675],
			"reward5": ["small_energy_potion", 1]
		},
		{  # 7
			"reward1": ["experience_potion", 250],
			"reward2": ["experience", 10],
			"reward3": ["iron", 250],
			"reward4": ["coin", 750],
			"reward5": ["small_energy_potion", 1]
		},
		{  # 8
			"reward1": ["experience_potion", 275],
			"reward2": ["experience", 10],
			"reward3": ["iron", 275],
			"reward4": ["coin", 825],
			"reward5": ["small_energy_potion", 1]
		}
	]

	def __init__(self, session, *args, **kwargs):
		self.unique_id = self.__get_unique_id(session)

	def _pass_level(self, message) -> str:
		info = json.loads(message, encoding="utf-8")
		customs_clearance_time = list(info["data"].keys())[0]  # 通关时间
		level_client = int(list(info["data"].values())[0])

		item_dict = self.__structure_item_dict()

		data_len = len(self.reward_list[0].keys()) + 1
		self.__structure_data(self.reward_list[0], item_dict, data_len)
		# 异常触发，后续方法不会进行
		if level_client <= 0 or (item_dict["level"] + 1) < level_client:
			return mc("9", "abnormal data!", data=self.reward_list[0])

		# 改变所有该变的变量
		# item_dict["energy"] -= 1
		if item_dict["level"] + 1 == level_client:  # 通过新关卡
			item_dict["level"] = level_client

		data = self.reward_list[level_client] # 获得奖励
		data_len = len(self.reward_list[level_client].keys()) + 1
		self.__structure_data(data, item_dict, data_len)

		player_status_list = [str(item_dict["level"]), str(item_dict["experience_potion"]),
			str(item_dict["experience"]), str(item_dict["energy"]), str(item_dict["small_energy_potion"]), self.unique_id]
		player_status_str = """UPDATE player_status SET level=%s, experience_potion=%s, experience=%s, energy=%s, small_energy_potion=%s
				where unique_id='%s'""" % tuple(player_status_list)

		bag_list = [str(item_dict["iron"]), str(item_dict["coin"]), self.unique_id]
		bag_str = """UPDATE bag SET iron=%s, coin=%s where unique_id='%s'""" % tuple(bag_list)
		if gasql_update(player_status_str) == 1 and gasql_update(bag_str) == 1:
			data["item" + str(data_len)][1] = item_dict["level"]
			return mc("0", "passed customs!", data=data)
		return mc("1", "abnormal data!", data=self.reward_list[0])

	def __structure_item_dict(self) -> dict:
		level, experience_potion, experience, energy, small_energy_potion = self.__get_level()
		iron, coin = self.__get_bag_data()
		item_dict = {
			"experience_potion": experience_potion,
			"experience": experience,
			"iron": iron,
			"coin": coin,
			"level": level,
			"energy": energy,
			"small_energy_potion": small_energy_potion
		}
		return item_dict


	def __structure_data(self, data, item_dict, data_len):
		for i in range(1, data_len):
			reward = "reward" + str(i)
			key = data[reward][0]
			item_dict[key] += data[reward][1]
			data.update({"item" + str(i): [key, item_dict[key]]})
		data.update({"item" + str(data_len): ["level", item_dict["level"]]})
		# data.update({"item" + str(data_len + 1): ["energy", item_dict["energy"]]})

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
		return sql_result[0]

	def __get_level(self):
		sql_result = gasql("select level, experience_potion, experience, energy, small_energy_potion from player_status where  unique_id='" + self.unique_id + "'")
		print("[LevelSystemClass][__get_level] -> sql_result:" + str(sql_result))
		return sql_result[0]

	def __get_unique_id(self, session):
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
