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
	def __init__(self,session, *args, **kwargs):
		self.unique_id = self.__get_unique_id(session)
	def _skill_level_up(self,session,message_info):
		"""
		level up skill, if skill level is 0, can't level up, level up skill need scroll, scroll have probability to level up.
		"""
		if self.unique_id=="":
			return mc("1","user is not exist")
		message_dic  = eval(message_info)
		data={}
		try:
			#1:技能是否大于1级且卷轴数量是否大于1，不满足则返回升级失败
			#2:卷轴数量减1开始升级技能
			#3:升级成功技能等级加1，返回技能、技能等级、卷轴、卷轴数量、升级成功标示
			#4:升级失败，返回技能、技能等级、卷轴、卷轴数量、升级成功标示
			skill_id = message_dic["data"]["skill_id"]
			scroll_id = message_dic["data"]["scroll_id"]
			if scroll_id=="scroll_skill_ten":
				if random.randint(1,10)==10:
					data = {"data": {"skill_id": skill_id,"skill_level":"2", "scroll_id": scroll_id,"scroll_quantity":"2","upgrade":"0"}}
				else:
					data = {"data": {"skill_id": skill_id,"skill_level":"2", "scroll_id": scroll_id,"scroll_quantity":"2","upgrade":"1"}}
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
	def __get_skill_level(self,skill_id):
		pass
	def __get_scroll_quantity(self,scroll_id):
		pass
	def __set_skill_level(self,skill_id,level):
		pass
	def __set_scroll_quantity(self,scroll_id, level):
		pass

if __name__ == "__main__":
	pass

