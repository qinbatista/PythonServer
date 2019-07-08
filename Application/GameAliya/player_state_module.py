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
from Utility.AnalysisHeader import message_constructor as mc


class PlayerStateSystemClass():
	def __init__(self, token, *args, **kwargs):
		self.unique_id = self.__get_unique_id(token)
		self.item_list_count = 0
		self.recover_time = 30
		self.full_energy = 10
	def _decrease_energy(self,msg):
		print("_decrease_energy")
		return ""
	def _increase_energy(self,msg):
		print("_increase_energy")
		return ""
	def __get_unique_id(self, token):
		sql_result = gasql("select unique_id from userinfo where  token='" + token + "'")
		if len(sql_result[0][0]) <= 0:
			return ""
		else:
			self.__check_table(sql_result[0][0])
			return sql_result[0][0]

	def __check_table(self, unique_id):
		sql_result = gasql("select count(unique_id) from player_status where  unique_id='" + unique_id + "'")
		if len(sql_result) == 0:
			gasql("INSERT INTO player_status(unique_id) VALUES ('" + unique_id + "')")


if __name__ == "__main__":
	pass
