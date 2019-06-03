import sys
import json
import time
import os
import codecs
import threading
import pymysql
import datetime;
import random
def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
from Utility import LogRecorder,EncryptionAlgorithm
from Utility.LogRecorder import LogUtility as Log
from Utility.sql_manager import game_aliya as gasql
from Utility.AnalysisHeader import message_constructor as mc

class SkillSystemClass():
	def __init__(self, *args, **kwargs):
		pass
	def _skill_level_up(self,session,message_info):
		"""
		level up skill, if skill level is 0, can't level up, level up skill need scroll, scroll have probability to level up.
		"""
		unique_id = self.__get_unique_id(session)
		if unique_id=="":
			return mc("1","user is not exist")
		message_dic  = eval(message_info)
		data={}
		try:
			skill_id = message_dic["data"]["skill_id"]
			scroll_id = message_dic["data"]["scroll_id"]
			if scroll_id=="scroll_skill_ten":
				if random.randint(1,10)==10:
					print("++++++++++")
					data = {"data": {"skill_id": skill_id,"skill_level":"2", "scroll_id": skill_id,"scroll_quantity":"2","upgrade":"1"}}
				else:
					data = {"data": {"skill_id": skill_id,"skill_level":"2", "scroll_id": skill_id,"scroll_quantity":"2","upgrade":"0"}}
		except:
			return mc("1","client message is incomplete")
		return mc("0","success",data)
	def _get_all_skill_level(self,session):
		"""
		give all skills' level to client
		"""
		pass
	def __get_unique_id(self,session):
		sql_result=gasql("select unique_id from userinfo where  session='"+session+"'")
		if len(sql_result[0][0])<=0:
			return ""
		else:
			return sql_result[0][0]
if __name__ == "__main__":
	pass

