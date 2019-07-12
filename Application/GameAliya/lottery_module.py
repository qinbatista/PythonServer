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
from Application.GameAliya import skill_module
from Application.GameAliya import bag_module


class LotterySystemClass:
	skill_id_list = [
		"m1_level",
		"p1_level",
		"g1_level",
		"m11_level",
		"m12_level",
		"m13_level",
		"p11_level",
		"p12_level",
		"p13_level",
		"g11_level",
		"g12_level",
		"g13_level",
		"m111_level",
		"m112_level",
		"m113_level",
		"m121_level",
		"m122_level",
		"m123_level",
		"m131_level",
		"m132_level",
		"m133_level",
		"p111_level",
		"p112_level",
		"p113_level",
		"p121_level",
		"p122_level",
		"p123_level",
		"p131_level",
		"p132_level",
		"p133_level",
		"g111_level",
		"g112_level",
		"g113_level",
		"g121_level",
		"g122_level",
		"g123_level",
		"g131_level",
		"g132_level",
		"g133_level"
	]
	
	def __init__(self, token, *args, **kwargs):
		self.unique_id = self.__get_unique_id(token)
		print("[LotterySystemClass][__init__] -> self.unique_id:" + str(self.unique_id))
		self.item_list_count = 0
		self.token = token
		self.reward_fragment_count = 30  # 奖励的碎片数量
	
	def _random_gift_skill(self, message_info):
		random_int = random.randint(1, 10)
		if 1 <= random_int <= 6:
			level = 1
			random_int = random.randint(0, 2)
			skill_id = self.skill_id_list[random_int]
		elif 7 <= random_int <= 9:
			level = 2
			random_int = random.randint(3, 11)
			skill_id = self.skill_id_list[random_int]
		else:
			level = 3
			random_int = random.randint(12, 38)
			skill_id = self.skill_id_list[random_int]
		skill_class = skill_module.SkillSystemClass(self.token)
		sql_result = skill_class._get_skill_level(skill_id)
		if sql_result == 0:
			dc = skill_class._get_skill("{\"data\": {\"skill_id\": \"%s\"}}" % skill_id)
			print(dc)
			return dc
		else:
			bag_class = bag_module.BagSystemClass(self.token)
			if level == 1:
				dc = bag_class._increase_item_quantity("scroll_skill_10", "1")
			elif level == 2:
				dc = bag_class._increase_item_quantity("scroll_skill_30", "1")
			else:
				dc = bag_class._increase_item_quantity("scroll_skill_100", "1")
			return mc("1", "you already have %s, got scroll for free" % skill_id, dc)
	
	def _random_gift_segment(self, message_info):
		random_int = random.randint(0, 999)
		all_weapon = self.__get_all_weapon_name()
		all_weapon_star = self.__get_weapon_bag()
		# 40% 概率抽中 1-10号武器的碎片 小于400
		if random_int < 400:
			weapon_code = random.randint(1, 10)
		# 30% 概率抽中 11-20号武器的碎片 大于等于400 且 小于700
		elif random_int < 700:
			weapon_code = random.randint(11, 20)
		# 20% 概率抽中 21-30号武器的碎片 大于等于700 且 小于900
		elif random_int < 900:
			weapon_code = random.randint(21, 30)
		# 10% 概率抽中 31-40号武器的碎片 大于等于900
		else:
			weapon_code = random.randint(31, 40)
		return self.__update_segment_status(all_weapon[weapon_code], all_weapon_star[weapon_code])
	
	def __update_segment_status(self, weapon_kind, weapon_star):
		segment = self.__get_weapon_segment(weapon_kind)
		data = {
			"weapon_bag1": [weapon_kind, weapon_star, segment],
		}
		if weapon_star == 0:
			weapon_star += 1
			if gasql_update("UPDATE weapon_bag SET " + weapon_kind + "=" + str(weapon_star) + " where unique_id='" + self.unique_id + "'") == 1:
				data["weapon_bag1"] = [weapon_kind, weapon_star, segment]
				return mc("0", "get the weapon " + weapon_kind, data=data)
			else:
				print("[LotterySystemClass][__update_segment_status] -> Data update error!")
				return mc("2", "abnormal data", data=data)
		else:
			segment += self.reward_fragment_count
			if gasql_update("UPDATE " + weapon_kind + " SET segment=" + str(segment) + " where unique_id='" + self.unique_id + "'") == 1:
				data["weapon_bag1"] = [weapon_kind, weapon_star, segment]
				return mc("1", "get " + weapon_kind + " weapon fragments", data=data)
			else:
				print("[LotterySystemClass][__update_segment_status] -> Weapon fragment update failed!")
				return mc("3", "abnormal data", data=data)
	
	def __get_weapon_segment(self, weapon_kind):
		sql_result = gasql("select segment from " + weapon_kind + " where unique_id='" + self.unique_id + "'")
		print("[LotterySystemClass][__get_weapon_segment]->sql_result:" + str(sql_result))
		return sql_result[0][0]
	
	def __get_all_weapon_name(self) -> list:
		sql_result = gasql("desc weapon_bag;")
		col_list = []
		for col in sql_result:
			col_list.append(col[0])
		print("[LotterySystemClass][__get_all_weapon_name]->col_list:" + str(col_list))
		return col_list
	
	def __get_weapon_bag(self) -> list:
		sql_result = gasql("select * from weapon_bag where unique_id='" + self.unique_id + "'")
		print("[LotterySystemClass][__get_weapon_bag]->sql_result:" + str(sql_result))
		return sql_result[0]
	
	def __get_unique_id(self, token):
		sql_result = gasql("select unique_id from userinfo where  token='" + token + "'")
		if len(sql_result) == 0:
			return ""
		else:
			self.__check_table(str(sql_result[0][0]))
			return sql_result[0][0]
	
	def __check_table(self, unique_id):
		sql_result = gasql("select * from skill where  unique_id='" + unique_id + "'")
		if len(sql_result) == 0:  # userinfo表中没得用户就不执行
			gasql("INSERT INTO skill(unique_id) VALUES ('" + unique_id + "')")
		else:
			print("[LotterySystemClass][__check_table] -> sql_result:" + str(sql_result))


if __name__ == "__main__":
	pass
