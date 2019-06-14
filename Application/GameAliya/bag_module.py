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
from Utility import LogRecorder,EncryptionAlgorithm
from Utility.LogRecorder import LogUtility as Log
from Utility.sql_manager import game_aliya as gasql
from Utility.sql_manager import game_aliya_table as gasql_t
from Utility.AnalysisHeader import message_constructor as mc

class BagSystemClass():
	def __init__(self,session, *args, **kwargs):
		self.unique_id = self.__get_unique_id(session)
		self.item_list_count=0
	def _increase_item_quantity(self,item_id, item_quantity):
		# try:
			self.item_list_count=self.item_list_count+1
			gasql("UPDATE bag SET "+item_id+"= "+item_id+" +"+item_quantity+" WHERE unique_id='"+self.unique_id + "'")
			result_quantity = gasql("select "+item_id+" from bag where  unique_id='"+self.unique_id + "'")
			dc = {"item"+str(self.item_list_count):[item_id,result_quantity[0][0]]}
			return dc
		# except :
		# 	return {"scroll_error":"1"}
	def _increase_supplies(self,message_info):
		message_dic  = eval(message_info)
		return_dic = {}
		int_number = random.randint(1,40)
		if(int_number==1):
			skill_level_result = self.__get_skill_level("m1_level")
			if skill_level_result>0:
				#增加卷轴
				return_dic.update (self._increase_item_quantity("m1_level","1"))
		if "scroll_skill_10" in message_dic["data"].keys():
			scroll_quantity = message_dic["data"]["scroll_skill_10"]
			return_dic.update (self._increase_item_quantity("scroll_skill_10",scroll_quantity))
		if "scroll_skill_30" in message_dic["data"].keys():
			scroll_quantity = message_dic["data"]["scroll_skill_30"]
			return_dic.update (self._increase_item_quantity("scroll_skill_30",scroll_quantity))
		if "scroll_skill_100" in message_dic["data"].keys():
			scroll_quantity = message_dic["data"]["scroll_skill_100"]
			return_dic.update (self._increase_item_quantity("scroll_skill_100",scroll_quantity))
		if "iron" in message_dic["data"].keys():
			scroll_quantity = message_dic["data"]["iron"]
			return_dic.update (self._increase_item_quantity("iron",scroll_quantity))
		if "diamonds" in message_dic["data"].keys():
			scroll_quantity = message_dic["data"]["diamonds"]
			return_dic.update (self._increase_item_quantity("diamonds",scroll_quantity))
		if "money" in message_dic["data"].keys():
			scroll_quantity = message_dic["data"]["money"]
			return_dic.update (self._increase_item_quantity("money",scroll_quantity))
		if "coin" in message_dic["data"].keys():
			scroll_quantity = message_dic["data"]["coin"]
			return_dic.update (self._increase_item_quantity("coin",scroll_quantity))
		return mc("0","increase supplies success",return_dic)
	def _random_gift(self,message_info):
		message_dic  = eval(message_info)
		return_dic = {}
		if "scroll_skill_10" in message_dic["data"].keys():
			scroll_quantity = message_dic["data"]["scroll_skill_10"]
			return_dic.update (self._increase_item_quantity("scroll_skill_10",scroll_quantity))
		if "scroll_skill_30" in message_dic["data"].keys():
			scroll_quantity = message_dic["data"]["scroll_skill_30"]
			return_dic.update (self._increase_item_quantity("scroll_skill_30",scroll_quantity))
		if "scroll_skill_100" in message_dic["data"].keys():
			scroll_quantity = message_dic["data"]["scroll_skill_100"]
			return_dic.update (self._increase_item_quantity("scroll_skill_100",scroll_quantity))
		if "iron" in message_dic["data"].keys():
			scroll_quantity = message_dic["data"]["iron"]
			return_dic.update (self._increase_item_quantity("iron",scroll_quantity))
		if "diamonds" in message_dic["data"].keys():
			scroll_quantity = message_dic["data"]["diamonds"]
			return_dic.update (self._increase_item_quantity("diamonds",scroll_quantity))
		if "money" in message_dic["data"].keys():
			scroll_quantity = message_dic["data"]["money"]
			return_dic.update (self._increase_item_quantity("money",scroll_quantity))
		if "coin" in message_dic["data"].keys():
			scroll_quantity = message_dic["data"]["coin"]
			return_dic.update (self._increase_item_quantity("coin",scroll_quantity))
	def _get_all_supplies(self,message_info):
		"""
		give all skills' level to client
		"""
		table,result=gasql_t("select * from bag where unique_id='"+self.unique_id +"'")
		data_dic={}
		for i in range(1,len(result[0])):
			data_dic.update({"item"+str(i):[table[i][0],result[0][i]]})
		return mc("0","get all suypplies",data_dic)
	def __get_unique_id(self,session):
		sql_result=gasql("select unique_id from userinfo where  session='"+session+"'")
		if len(sql_result[0][0])<=0:
			return ""
		else:
			self.__check_table(sql_result[0][0])
			return sql_result[0][0]
	def __check_table(self, unique_id):
		sql_result=gasql("select count(unique_id) from bag where  unique_id='"+unique_id+"'")
		if sql_result[0][0]<=0:
			gasql("INSERT INTO bag(unique_id) VALUES ('"+unique_id+"')")
	def __get_skill_level(self,skill_id):
		"""
		get skill level
		"""
		sql_result=gasql("select "+skill_id+" from skill where unique_id='"+self.unique_id +"'")
		return sql_result[0][0]
if __name__ == "__main__":
	pass

