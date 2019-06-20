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
from Utility.AnalysisHeader import message_constructor as mc


class WeaponSystemClass:
	skill_dict = {
		"passive_skill_1_level": 0,
		"passive_skill_2_level": 0,
		"passive_skill_3_level": 0,
		"passive_skill_4_level": 0,
	}
	all_weapon_count = 40
	def __init__(self, session, standard_iron_count=20, standard_segment_count=100):
		self.unique_id = self.__get_unique_id(session)
		self.standard_iron_count = standard_iron_count# 升级武器等级消耗的铁数量要求
		self.standard_segment_count = standard_segment_count# 升级武器阶数消耗的碎片数量要求

	def _level_up_weapon(self, message) -> str:
		print("[WeaponSystemClass][_level_up_weapon]->message:" + message)
		info = json.loads(message, encoding="utf-8")
		weapon_kind = list(info["data"].keys())[0]
		skill_upgrade_number = int(list(info["data"].values())[0]) // self.standard_iron_count
		weapon_level, passive_skill_1_level, passive_skill_2_level, passive_skill_3_level, passive_skill_4_level, skill_point, segment = self.__get_weapon_level(weapon_kind)
		iron_count = self.__get_iron()
		data = {
			"weapon_bag1": [weapon_kind, weapon_level, passive_skill_1_level, passive_skill_2_level, passive_skill_3_level, passive_skill_4_level, skill_point, segment],
			"item1": ["iron", iron_count],
		}
		print("[WeaponSystemClass][_level_up_weapon]->weapon_kind:" + weapon_kind)
		print("[WeaponSystemClass][_level_up_weapon]->skill_upgrade_number:" + str(skill_upgrade_number))
		print("[WeaponSystemClass][_level_up_weapon]->weapon_level, passive_skill_1_level, passive_skill_2_level, passive_skill_3_level, passive_skill_4_level, skill_point, segment:", str(weapon_level), str(passive_skill_1_level), str(passive_skill_2_level), str(passive_skill_3_level), str(passive_skill_4_level), str(skill_point), str(segment))
		if self.__get_weapon_star(weapon_kind) == 0:
			return mc("1", "no weapon!", data=data)
		elif weapon_level == 100:
			return mc("9", "has reached full level, can not be upgraded!", data=data)
		elif skill_upgrade_number != 0 and (iron_count // self.standard_iron_count) >= skill_upgrade_number:
			if (weapon_level + skill_upgrade_number) > 100:
				skill_upgrade_number = 100 - weapon_level
			weapon_level += skill_upgrade_number
			skill_point += skill_upgrade_number
			if self.__set_weapon_level(weapon_kind, weapon_level, skill_point) == 0:
				# weapon_level和skill_point没有写入成功，所以不用恢复数据
				return mc("3", "abnormal data!", data=data)
			iron_count -= self.standard_iron_count * skill_upgrade_number
			if self.__set_iron_count(iron_count) == 0:
				# iron_count没有写入成功，所以不用恢复数据
				weapon_level -= skill_upgrade_number
				skill_point -= skill_upgrade_number
				if self.__set_weapon_level(weapon_kind, weapon_level, skill_point) == 0:
					# 材料未消耗，武器等级异常加一
					print("[WeaponSystemClass][_level_up_weapon] -> Material is not consumed, weapon level is abnormally plus one")
				return mc("4", "abnormal data!", data=data)
			data["weapon_bag1"] = [weapon_kind, weapon_level, passive_skill_1_level, passive_skill_2_level, passive_skill_3_level, passive_skill_4_level, skill_point, segment]
			data["item1"] = ["iron", iron_count]
			return mc("0", weapon_kind + " update success!", data=data)
		else:
			return mc("2", "insufficient materials, upgrade failed!", data=data)

	def _passive_skill_upgrade(self, message):
		print("[WeaponSystemClass][_passive_skill_upgrade]->message:" + message)
		info = json.loads(message, encoding="utf-8")
		weapon_kind = list(info["data"].keys())[0]
		skill_kind = list(info["data"].values())[0]
		weapon_level, passive_skill_1_level, passive_skill_2_level, passive_skill_3_level, passive_skill_4_level, skill_point, segment = self.__get_weapon_level(weapon_kind)
		self.skill_dict["passive_skill_1_level"] = passive_skill_1_level
		self.skill_dict["passive_skill_2_level"] = passive_skill_2_level
		self.skill_dict["passive_skill_3_level"] = passive_skill_3_level
		self.skill_dict["passive_skill_4_level"] = passive_skill_4_level
		data = {
			"weapon_bag1": [weapon_kind, weapon_level, self.skill_dict["passive_skill_1_level"], self.skill_dict["passive_skill_2_level"], self.skill_dict["passive_skill_3_level"], self.skill_dict["passive_skill_4_level"], skill_point, segment]
		}
		if self.__get_weapon_star(weapon_kind) == 0:
			return mc("1", "no weapon!", data=data)
		elif skill_kind not in self.skill_dict.keys():
			return mc("9", "no skill kind!", data=data)
		elif skill_point > 0:
			skill_point -= 1
			self.skill_dict[skill_kind] += 1
			if self.__set_skill_level(weapon_kind, skill_kind, self.skill_dict[skill_kind], skill_point) == 0:
				return mc("3", "abnormal data!", data=data)
			data["weapon_bag1"] = [weapon_kind, weapon_level, self.skill_dict["passive_skill_1_level"], self.skill_dict["passive_skill_2_level"], self.skill_dict["passive_skill_3_level"], self.skill_dict["passive_skill_4_level"], skill_point, segment]
			return mc("0", skill_kind + " update success!", data=data)
		else:
			return mc("2", "insufficient skill points, upgrade failed!", data=data)

	def _reset_skill_point(self, message):
		print("[WeaponSystemClass][_reset_skill_point]->message:" + message)
		info = json.loads(message, encoding="utf-8")
		weapon_kind = list(info["data"].keys())[0]
		coin = int(list(info["data"].values())[0])
		bag_coin = self.__get_coin()
		weapon_level, passive_skill_1_level, passive_skill_2_level, passive_skill_3_level, passive_skill_4_level, skill_point, segment = self.__get_weapon_level(weapon_kind)
		self.skill_dict["passive_skill_1_level"] = passive_skill_1_level
		self.skill_dict["passive_skill_2_level"] = passive_skill_2_level
		self.skill_dict["passive_skill_3_level"] = passive_skill_3_level
		self.skill_dict["passive_skill_4_level"] = passive_skill_4_level
		data = {
			"weapon_bag1": [weapon_kind, weapon_level, self.skill_dict["passive_skill_1_level"], self.skill_dict["passive_skill_2_level"], self.skill_dict["passive_skill_3_level"], self.skill_dict["passive_skill_4_level"], skill_point, segment]
		}
		if self.__get_weapon_star(weapon_kind) == 0:
			return mc("1", "no weapon!", data=data)
		elif bag_coin < coin:
			return mc("9", "there is not enough gold coins to reset!", data=data)
		else:
			bag_coin -= coin
			if self.__set_coin(bag_coin) == 0:
				return mc("3", "abnormal data!", data=data)
			self.skill_dict["passive_skill_1_level"] = 0
			self.skill_dict["passive_skill_2_level"] = 0
			self.skill_dict["passive_skill_3_level"] = 0
			self.skill_dict["passive_skill_4_level"] = 0
			skill_point = weapon_level
			if self.__set_skill_point(weapon_kind, self.skill_dict["passive_skill_1_level"], self.skill_dict["passive_skill_1_level"], self.skill_dict["passive_skill_1_level"], self.skill_dict["passive_skill_1_level"], skill_point) == 0:
				bag_coin += coin
				if self.__set_coin(bag_coin) == 0:
					# 材料已消耗，重置技能失败，或者技能已经重置过
					print("[WeaponSystemClass][_reset_skill_point] -> Material has been consumed, reset skill failed")
				return mc("4", "abnormal data!", data=data)

			data["weapon_bag1"] = [weapon_kind, weapon_level, self.skill_dict["passive_skill_1_level"],self.skill_dict["passive_skill_2_level"], self.skill_dict["passive_skill_3_level"],self.skill_dict["passive_skill_4_level"], skill_point, segment]
			return mc("0", weapon_kind + " reset skill point success!", data=data)

	def _upgrade_weapons_stars(self, message):
		print("[WeaponSystemClass][_upgrade_weapons_stars]->message:" + message)
		info = json.loads(message, encoding="utf-8")
		weapon_kind = info["data"]
		weapon_level, passive_skill_1_level, passive_skill_2_level, passive_skill_3_level, passive_skill_4_level, skill_point, segment = self.__get_weapon_level(weapon_kind)
		weapon_star = self.__get_weapon_star(weapon_kind)
		data = {
			"weapon_bag1": [weapon_kind, weapon_level, passive_skill_1_level, passive_skill_2_level, passive_skill_3_level, passive_skill_4_level, skill_point, segment, weapon_star]
		}
		if segment < self.standard_segment_count:
			return mc("1", "fragmentation insufficient!", data=data)
		else:
			segment -= self.standard_segment_count
			weapon_star += 1
			if self.__set_segment(weapon_kind, segment) == 0:
				return mc("3", "abnormal data!", data=data)
			if self.__set_weapon_star(weapon_kind, weapon_star) == 0:
				segment += self.standard_segment_count
				if self.__set_segment(weapon_kind, segment) == 0:
					# 碎片已消耗，升级星数失败
					print("[WeaponSystemClass][_reset_skill_point] -> Fragmentation has been consumed, upgrade star failed")
				return mc("4", "abnormal data!", data=data)
			data["weapon_bag1"] = [weapon_kind, weapon_level, passive_skill_1_level, passive_skill_2_level, passive_skill_3_level, passive_skill_4_level, skill_point, segment, weapon_star]
			return mc("0", weapon_kind + " upgrade success!", data=data)

	def _all_weapon(self):
		data = {}
		for i in range(self.all_weapon_count):
			pass

	def __get_weapon_star(self, weapon_kind):
		sql_result = gasql("select " + weapon_kind + " from weapon_bag where unique_id='" + self.unique_id + "'")
		print("[WeaponSystemClass][__get_iron]->sql_result:" + str(sql_result))
		return sql_result[0][0]

	def __get_iron(self) -> int:
		sql_result = gasql("select iron from bag where unique_id='" + self.unique_id + "'")
		print("[WeaponSystemClass][__get_iron]->sql_result:" + str(sql_result))
		return sql_result[0][0]

	def __get_coin(self) -> int:
		sql_result = gasql("select coin from bag where unique_id='" + self.unique_id + "'")
		print("[WeaponSystemClass][__get_coin]->sql_result:" + str(sql_result))
		return sql_result[0][0]

	def __get_weapon_level(self, weapon_kind):
		sql_result = gasql("select weapon_level, passive_skill_1_level, passive_skill_2_level, passive_skill_3_level, passive_skill_4_level, skill_point, segment from " + weapon_kind + " where unique_id='" + self.unique_id + "'")
		print("[WeaponSystemClass][__get_weapon_level]->sql_result:" + str(sql_result))
		return sql_result[0][0], sql_result[0][1], sql_result[0][2], sql_result[0][3], sql_result[0][4], sql_result[0][5], sql_result[0][6]

	def __set_coin(self, coin) -> int:
		sql_value = gasql_update("UPDATE bag SET coin=" + str(coin) + " where unique_id='" + self.unique_id + "'")
		return sql_value

	def __set_skill_point(self, weapon_kind, passive_skill_1_level, passive_skill_2_level, passive_skill_3_level, passive_skill_4_level, skill_point) -> int:
		sql_value = gasql_update("UPDATE " + weapon_kind + " SET passive_skill_1_level=" + str(passive_skill_1_level) + ", passive_skill_2_level=" + str(passive_skill_2_level) + ", passive_skill_3_level=" + str(passive_skill_3_level) + ", passive_skill_4_level=" + str(passive_skill_4_level) + ", skill_point=" + str(skill_point) + " where unique_id='" + self.unique_id + "'")
		return sql_value

	def __set_skill_level(self, weapon_kind, skill_kind, skill_value, skill_point) -> int:
		sql_value = gasql_update("UPDATE " + weapon_kind + " SET " + skill_kind + "=" + str(skill_value) + ",skill_point=" + str(skill_point) + " where unique_id='" + self.unique_id + "'")
		return sql_value

	def __set_weapon_level(self, weapon_kind, weapon_level, skill_point) -> int:
		sql_value = gasql_update("UPDATE " + weapon_kind + " SET weapon_level=" + str(weapon_level) + ",skill_point=" + str(skill_point) + " where unique_id='" + self.unique_id + "'")
		return sql_value

	def __set_iron_count(self, iron_count) -> int:
		sql_value = gasql_update("UPDATE bag SET iron=" + str(iron_count) + " where unique_id='" + self.unique_id + "'")
		return sql_value

	def __set_segment(self, weapon_kind, segment):
		sql_value = gasql_update("UPDATE " + weapon_kind + " SET segment=" + str(segment) + " where unique_id='" + self.unique_id + "'")
		return sql_value

	def __set_weapon_star(self, weapon_kind, weapon_star):
		sql_value = gasql_update("UPDATE weapon_bag SET " + weapon_kind + "=" + str(weapon_star) + " where unique_id='" + self.unique_id + "'")
		return sql_value

	def __get_unique_id(self, session):  # 返回session对应的用户id
		sql_result = gasql("select unique_id from userinfo where  session='" + session + "'")  # 通过session查用户id
		if len(sql_result) <= 0:  # userinfo表中没得用户就不执行
			return ""
		else:
			self.__check_table(sql_result[0][0])
			return sql_result[0][0]

	def __check_table(self, unique_id):  # 通过用户id来查用户的武器背包信息
		sql_result = gasql("select unique_id from weapon_bag where unique_id='" + unique_id + "'")
		if len(sql_result) <= 0:  # 如果用户的武器背包没有信息，就插入用户武器背包信息
			gasql("INSERT INTO weapon_bag(unique_id) VALUES ('" + unique_id + "')")
			gasql("INSERT INTO skill(unique_id) VALUES ('" + unique_id + "')")
			for i in range(1, 40):  # 在所有的武器表中都插入用户id信息
				gasql("INSERT INTO weapon" + str(i) + "(unique_id) VALUES ('" + unique_id + "')")

if __name__ == "__main__":
	pass
