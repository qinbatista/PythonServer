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
	def _skill_level_up(self,message_info):
		"""
		level up skill, if skill level is 0, can't level up, level up skill need scroll, scroll have probability to level up.
		"""
		if self.unique_id=="":
			return mc("1","user is not exist")
		message_dic  = eval(message_info)
		data={}
		try:
			skill_id = message_dic["data"]["skill_id"]
			scroll_id = message_dic["data"]["scroll_id"]
			if self.__get_skill_level(skill_id)==0:
				return mc("2","skill does't get yet")
			if self.__get_scroll_quantity(scroll_id)==0:
				return mc("3","don't have enough scroll")
			if scroll_id=="scroll_skill_10":#level up with 10% scroll
				gasql("UPDATE bag SET "+scroll_id+"= "+scroll_id+"-"+str(1)+" WHERE unique_id='"+self.unique_id + "'")
				if random.randint(1,10)==10:
					gasql("UPDATE skill SET "+skill_id+"="+skill_id+"+"+str(1)+" WHERE unique_id='"+self.unique_id + "'")
					result_skill_quantity = gasql("select "+skill_id+" from skill where  unique_id='"+self.unique_id + "'")
					result_scroll_quantity = gasql("select "+scroll_id+" from bag where  unique_id='"+self.unique_id + "'")
					data = { "value":[skill_id,str(result_skill_quantity[0][0]),scroll_id,str(result_scroll_quantity[0][0])],"upgrade":"0"}
				else:
					result_skill_quantity = gasql("select "+skill_id+" from skill where  unique_id='"+self.unique_id + "'")
					result_scroll_quantity = gasql("select "+scroll_id+" from bag where  unique_id='"+self.unique_id + "'")
					data = { "value":[skill_id,str(result_skill_quantity[0][0]),scroll_id,str(result_scroll_quantity[0][0])],"upgrade":"1"}

			if scroll_id=="scroll_skill_30":#level up with 30% scroll
				gasql("UPDATE bag SET "+scroll_id+"= "+scroll_id+"-"+str(1)+" WHERE unique_id='"+self.unique_id + "'")
				if random.randint(1,10)<=7:
					gasql("UPDATE skill SET "+skill_id+"="+skill_id+"+"+str(1)+" WHERE unique_id='"+self.unique_id + "'")
					result_skill_quantity = gasql("select "+skill_id+" from skill where  unique_id='"+self.unique_id + "'")
					result_scroll_quantity = gasql("select "+scroll_id+" from bag where  unique_id='"+self.unique_id + "'")
					data = { "value":[skill_id,str(result_skill_quantity[0][0]),scroll_id,str(result_scroll_quantity[0][0])],"upgrade":"0"}
				else:
					result_skill_quantity = gasql("select "+skill_id+" from skill where  unique_id='"+self.unique_id + "'")
					result_scroll_quantity = gasql("select "+scroll_id+" from bag where  unique_id='"+self.unique_id + "'")
					data = { "value":[skill_id,str(result_skill_quantity[0][0]),scroll_id,str(result_scroll_quantity[0][0])],"upgrade":"1"}

			if scroll_id=="scroll_skill_100":#level up with 100% scroll
				gasql("UPDATE bag SET "+scroll_id+"= "+scroll_id+"-"+str(1)+" WHERE unique_id='"+self.unique_id + "'")
				gasql("UPDATE skill SET "+skill_id+"="+skill_id+"+"+str(1)+" WHERE unique_id='"+self.unique_id + "'")
				result_skill_quantity = gasql("select "+skill_id+" from skill where  unique_id='"+self.unique_id + "'")
				result_scroll_quantity = gasql("select "+scroll_id+" from bag where  unique_id='"+self.unique_id + "'")
				data = { "value":[skill_id,str(result_skill_quantity[0][0]),scroll_id,str(result_scroll_quantity[0][0])],"upgrade":"0"}
		except :
			return mc("4","client message is incomplete")
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
		"""
		get skill level
		"""
		sql_result=gasql("select "+skill_id+" from skill where  unique_id='"+self.unique_id +"'")
		return sql_result[0][0]
	def __get_scroll_quantity(self,scroll_id):
		"""
		get scroll level
		"""
		sql_result=gasql("select "+scroll_id+" from bag where unique_id='"+self.unique_id +"'")
		return sql_result[0][0]
	def __set_skill_level(self,skill_id,level):
		pass
	def __set_scroll_quantity(self,scroll_id):
		pass
	def _get_skill(self,message_info):
		try:
			message_dic  = eval(message_info)
			skill_id = message_dic["data"]["skill_id"]
			sql_result=gasql("select "+skill_id+" from skill where  unique_id='"+self.unique_id +"'")
			if sql_result[0][0]<=0:
				gasql("UPDATE skill SET "+skill_id+"="+str(1)+" WHERE unique_id='"+self.unique_id + "'")
			else:
				return mc("1","you already owned skill="+skill_id)
			return mc("0","got new skill="+skill_id)
		except :
			return mc("1","client message is incomplete")
if __name__ == "__main__":
	pass

