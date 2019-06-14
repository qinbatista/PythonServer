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


class WeaponSystemClass():
	def __init__(self, *args, **kwargs):
		pass
	def __get_unique_id(self,session):
		sql_result=gasql("select unique_id from userinfo where  session='"+session+"'")
		if len(sql_result[0][0])<=0:
			return ""
		else:
			self.__check_table(sql_result[0][0])
			return sql_result[0][0]
	def __check_table(self, unique_id):
		sql_result=gasql("select count(unique_id) from weapon_bag where  unique_id='"+unique_id+"'")
		if len(sql_result)<=0:
			gasql("INSERT INTO weapon_bag(unique_id, VALUES ('"+unique_id+"')")
			for i in range(1,40):
				gasql("INSERT INTO weapon_"+i+"(unique_id) VALUES ('"+unique_id+"')")
if __name__ == "__main__":
	pass

