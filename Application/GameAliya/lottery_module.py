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
from Application.GameAliya import skill_module
from Application.GameAliya import bag_module

class LotterySystemClass():
	def __init__(self, session,*args, **kwargs):
		self.unique_id = self.__get_unique_id(session)
		print("[LotterySystemClass][__init__] -> self.unique_id:" + str(self.unique_id))
		self.item_list_count=0
		self.session = session
		self.reward_fragment_count = 30# 奖励的碎片数量

	def _random_gift_skill(self,message_info):
		random_int = random.randint(1,10)
		level = 0
		if random_int>=1 and random_int<=6:
			level=1
			random_int = random.randint(1,3)
			if random_int==1: skill_id = "m1_level"
			if random_int==2: skill_id = "p1_level"
			if random_int==3: skill_id = "g1_level"
		elif random_int>=7 and random_int<=9:
			level=2
			random_int = random.randint(1,9)
			if random_int==1: skill_id = "m11_level"
			if random_int==2: skill_id = "m12_level"
			if random_int==3: skill_id = "m13_level"
			if random_int==4: skill_id = "p11_level"
			if random_int==5: skill_id = "p12_level"
			if random_int==6: skill_id = "p13_level"
			if random_int==7: skill_id = "g11_level"
			if random_int==8: skill_id = "g12_level"
			if random_int==9: skill_id = "g13_level"
		elif random_int==10:
			level=3
			random_int = random.randint(1,27)
			if random_int==1: skill_id = "m111_level"
			if random_int==2: skill_id = "m112_level"
			if random_int==3: skill_id = "m113_level"
			if random_int==4: skill_id = "m121_level"
			if random_int==5: skill_id = "m122_level"
			if random_int==6:skill_id = "m123_level"
			if random_int==7:skill_id = "m131_level"
			if random_int==8:skill_id = "m132_level"
			if random_int==9:skill_id = "m133_level"
			if random_int==10: skill_id = "p111_level"
			if random_int==11: skill_id = "p112_level"
			if random_int==12: skill_id = "p113_level"
			if random_int==13: skill_id = "p121_level"
			if random_int==14: skill_id = "p122_level"
			if random_int==15: skill_id = "p123_level"
			if random_int==16: skill_id = "p131_level"
			if random_int==17: skill_id = "p132_level"
			if random_int==18: skill_id = "p133_level"
			if random_int==19: skill_id = "g111_level"
			if random_int==20: skill_id = "g112_level"
			if random_int==21: skill_id = "g113_level"
			if random_int==22: skill_id = "g121_level"
			if random_int==23: skill_id = "g122_level"
			if random_int==24: skill_id = "g123_level"
			if random_int==25: skill_id = "g131_level"
			if random_int==26: skill_id = "g132_level"
			if random_int==27: skill_id = "g133_level"
		skill_class = skill_module.SkillSystemClass(self.session)
		sql_result = skill_class._get_skill_level(skill_id)
		if sql_result<=0:
			dc = skill_class._get_skill(str({"data":{"skill_id":skill_id}}))
			print(dc)
			return mc("1","got new skill="+skill_id,dc)
		else:
			bag_class = bag_module.BagSystemClass(self.session)
			if level==1:
				dc = bag_class._increase_item_quantity("scroll_skill_10","1")
			if level==2:
				dc = bag_class._increase_item_quantity("scroll_skill_30","1")
			if level==3:
				dc = bag_class._increase_item_quantity("scroll_skill_100","1")
			return mc("2","you already have "+skill_id+", got scroll for free", dc)

	def _random_gift_segment(self, message_info) :
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
				return mc("1", "abnormal data", data=data)
		else:
			segment += self.reward_fragment_count
			if gasql_update("UPDATE " + weapon_kind + " SET segment=" + str(segment) + " where unique_id='" + self.unique_id + "'") == 1:
				data["weapon_bag1"] = [weapon_kind, weapon_star, segment]
				return mc("0", "get " + weapon_kind + " weapon fragments", data=data)
			else:
				print("[LotterySystemClass][__update_segment_status] -> Weapon fragment update failed!")
				return mc("2", "abnormal data", data=data)

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

	def __get_unique_id(self,session):
		sql_result = gasql("select unique_id from userinfo where  session='"+session+"'")
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

