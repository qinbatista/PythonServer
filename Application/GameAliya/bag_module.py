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

class BagSystemClass():
	def __init__(self,session, *args, **kwargs):
		self.unique_id = self.__get_unique_id(session)

	def __increase_scroll_quantity(self,scroll_id, scroll_quantity):
		try:
			gasql("UPDATE bag SET "+scroll_id+"= "+scroll_id+" +"+scroll_quantity+" WHERE unique_id='"+self.unique_id + "'")
			result_quantity = gasql("select "+scroll_id+" from bag where  unique_id='"+self.unique_id + "'")
			dc = {scroll_id:result_quantity[0][0]}
			return dc
		except :
			return {"scroll_error":"1"}
	def _increase_supplies(self,message_info):
		message_dic  = eval(message_info)
		return_dic = {}
		if "scroll_skill_10" in message_dic["data"].keys():
			scroll_quantity = message_dic["data"]["scroll_skill_10"]
			return_dic.update (self.__increase_scroll_quantity("scroll_skill_10",scroll_quantity))
		if "scroll_skill_30" in message_dic["data"].keys():
			scroll_quantity = message_dic["data"]["scroll_skill_30"]
			return_dic.update (self.__increase_scroll_quantity("scroll_skill_30",scroll_quantity))
		if "scroll_skill_100" in message_dic["data"].keys():
			scroll_quantity = message_dic["data"]["scroll_skill_100"]
			return_dic.update (self.__increase_scroll_quantity("scroll_skill_100",scroll_quantity))
		return mc("0",return_dic)
	def __get_unique_id(self,session):
		sql_result=gasql("select unique_id from userinfo where  session='"+session+"'")
		if len(sql_result[0][0])<=0:
			return ""
		else:
			return sql_result[0][0]
if __name__ == "__main__":
	pass

