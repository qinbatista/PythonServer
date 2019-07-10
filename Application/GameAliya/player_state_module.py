import sys
import json
import os
import codecs
import threading
import pymysql
import random
import time
from datetime import datetime

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
	def _decrease_energy(self,message_info):
		message_dic = eval(message_info)
		if "data" in message_dic.keys():
			cost_energy = message_dic["data"]["energy"]
			sql_result = gasql("select energy, energy_recover_time from player_status where unique_id='" + self.unique_id + "'")
			remain_energy = int(sql_result[0][0])
			energy_time = sql_result[0][1]
			cost_energy_int = int(cost_energy)
			if sql_result[0][1]=="":
				if remain_energy >=0:
					if remain_energy>=self.full_energy:
						# if energy is more than cast, reduce energy,if energy over 10, record time
						Log("[PlayerStateSystemClass][_decrease_energy] remain_energy>=self.full_energy")
						gasql("UPDATE player_status SET " + "energy" + "=" + str(remain_energy) + "-" + str(cost_energy) + " WHERE unique_id='" + self.unique_id + "'")
						return mc("0", "decrease energy success, reamian energy is over full energy")
					else:
						Log("[PlayerStateSystemClass][_decrease_energy] remain_energy<=self.full_energy")
						gasql("UPDATE player_status SET " + "energy" + "=" + str(remain_energy) + "-" + str(cost_energy) + ", energy_recover_time = '"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"' WHERE unique_id='" + self.unique_id + "'")
						return mc("0", "decrease energy success, remain energy is lessing than full energy, start recovering energy")
				else:
					return mc("1", "energy is not enough")
			else:
				if remain_energy-cost_energy_int >=0:
					y = datetime.strptime(energy_time, '%Y-%m-%d %H:%M:%S')
					z = datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '%Y-%m-%d %H:%M:%S')
					diff = z-y
					recover_energy = int(diff.seconds/60/20)
					total_energy = recover_energy+remain_energy
					if total_energy>=10:
						gasql("UPDATE player_status SET " + "energy" + "=" + str(10) + "-" + str(cost_energy) + ", energy_recover_time = '"+""+"' WHERE unique_id='" + self.unique_id + "'")
						return mc("0", "energy is over full energy, remove time recoerd")
					else:
						gasql("UPDATE player_status SET " + "energy" + "=" + str(total_energy) + "-" + str(cost_energy) + " WHERE unique_id='" + self.unique_id + "'")
						return mc("0", "energy is recovering")
				else:
					return mc("1", "energy is not enough")
		else:
			return mc("1", "data is null")

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
		if sql_result[0][0] <= 0:
			gasql("INSERT INTO player_status(unique_id) VALUES ('" + unique_id + "')")


if __name__ == "__main__":
	pass
