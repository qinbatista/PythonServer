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
from Utility.AnalysisHeader import message_constructor as mc
from Application.GameAliya import skill_module
from Application.GameAliya import bag_module

class LotterySystemClass():
	def __init__(self, session,*args, **kwargs):
		self.unique_id = self.__get_unique_id(session)
		self.item_list_count=0
		self.session = session
	def _random_gift_skill(self,message_info):
		random_int = random.randint(1,39)
		if random_int==1: skill_id = "m1_level"
		if random_int==2: skill_id = "m11_level"
		if random_int==3: skill_id = "m12_level"
		if random_int==4: skill_id = "m13_level"
		if random_int==5: skill_id = "m111_level"
		if random_int==6: skill_id = "m112_level"
		if random_int==7: skill_id = "m113_level"
		if random_int==8: skill_id = "m121_level"
		if random_int==9: skill_id = "m122_level"
		if random_int==10:skill_id = "m123_level"
		if random_int==11:skill_id = "m131_level"
		if random_int==12:skill_id = "m132_level"
		if random_int==13:skill_id = "m133_level"

		if random_int==14: skill_id = "p1_level"
		if random_int==15: skill_id = "p11_level"
		if random_int==16: skill_id = "p12_level"
		if random_int==17: skill_id = "p13_level"
		if random_int==18: skill_id = "p111_level"
		if random_int==19: skill_id = "p112_level"
		if random_int==20: skill_id = "p113_level"
		if random_int==21: skill_id = "p121_level"
		if random_int==22: skill_id = "p122_level"
		if random_int==23: skill_id = "p123_level"
		if random_int==24: skill_id = "p131_level"
		if random_int==25: skill_id = "p132_level"
		if random_int==26: skill_id = "p133_level"

		if random_int==27: skill_id = "g1_level"
		if random_int==28: skill_id = "g11_level"
		if random_int==29: skill_id = "g12_level"
		if random_int==30: skill_id = "g13_level"
		if random_int==31: skill_id = "g111_level"
		if random_int==32: skill_id = "g112_level"
		if random_int==33: skill_id = "g113_level"
		if random_int==34: skill_id = "g121_level"
		if random_int==35: skill_id = "g122_level"
		if random_int==36: skill_id = "g123_level"
		if random_int==37: skill_id = "g131_level"
		if random_int==38: skill_id = "g132_level"
		if random_int==39: skill_id = "g133_level"

		skill_class = skill_module.SkillSystemClass(self.session)
		sql_result = skill_class._get_skill_level(skill_id)
		if sql_result<=0:
			dc = skill_class._get_skill(str({'data':{'skill_id':skill_id}}))
			print(dc)
			return mc("1","got new skill="+skill_id,dc)
		else:
			bag_class = bag_module.BagSystemClass(self.session)
			dc = bag_class._increase_item_quantity("scroll_skill_10","1")
			return mc("2","you already have "+skill_id+", got scroo_10 for free",dc)

	def __get_unique_id(self,session):
		sql_result=gasql("select count(unique_id) from userinfo where  session='"+session+"'")
		if len(sql_result)<=0:
			return ""
		else:
			self.__check_table(str(sql_result[0][0]))
			return sql_result[0][0]

	def __check_table(self, unique_id):
		gasql("select count(unique_id) from skill where  unique_id='"+unique_id+"'")
if __name__ == "__main__":
	pass

