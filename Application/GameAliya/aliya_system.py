import sys
import json
import time
import os
import codecs
import threading
import pymysql
import datetime;
def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
from Utility import LogRecorder,EncryptionAlgorithm
from Utility.LogRecorder import LogUtility as Log
from Application.GameAliya import account_module
from Application.GameAliya import configuration_module
from Application.GameAliya import level_module
from Application.GameAliya import skill_module
from Application.GameAliya import weapon_module
from Application.GameAliya import bag_module
from Application.GameAliya import lottery_module
from Utility.AnalysisHeader import message_constructor as mc
from Utility.sql_manager import game_aliya as gasql
DESKey = "67891234"
DESVector = "6789123467891234"

"""
0 success callback
1 error callback
"""
MessageList=[
	"{\"status\":\"0\",\"message\":\"success\"}",
	"{\"status\":\"1\",\"message\":\"failed\"}"
]
class AliyaSystemClass():
	def __init__(self, *args, **kwargs):
		pass
	def _login(self,message_info):
		pass
	def VerifyMessageIntegrity(self,message,IPAdress):
		LogRecorder.LogUtility("[Server][WorkingTimeRecoder][StaffCheckIn]["+IPAdress+"]->recived encrypted message:"+str(message))
		des = EncryptionAlgorithm.DES(DESKey,DESVector)
		message = des.decrypt(message)  #decrypt byte message
		message = bytes.decode(message) #byte to string
		LogRecorder.LogUtility("[Server][WorkingTimeRecoder][StaffCheckIn]["+IPAdress+"]->decrypted message:"+message)
		message_dic  = eval(message)
		if "session" in message_dic.keys():
			session = message_dic["session"]
		if "function" in message_dic.keys():
			function = message_dic["function"]
		return session,function,message

	def _ResolveMsg(self, message, ip_address):# 客户端的数据、IP地址
		mutex = threading.Lock()
		mutex.acquire()
		des = EncryptionAlgorithm.DES(DESKey,DESVector)
		session,function,msg_data = self.VerifyMessageIntegrity(message,ip_address)
		callback_message=""

		if function == "login":
			login_class = account_module.LoginSystemClass()
			callback_message = login_class._login(msg_data)
		elif function == "bind_account":

			login_class = account_module.LoginSystemClass()
			callback_message = login_class._bind_account(msg_data)

		elif function =="skill_level_up":
			skill_class = skill_module.SkillSystemClass(session)
			callback_message = skill_class._skill_level_up(msg_data)

		elif function =="get_all_skill_level":
			skill_class = skill_module.SkillSystemClass(session)
			callback_message = skill_class._get_all_skill_level(msg_data)

		elif function =="increase_supplies":
			bag_class = bag_module.BagSystemClass(session)
			callback_message = bag_class._increase_supplies(msg_data)

		elif function =="get_all_supplies":
			bag_class = bag_module.BagSystemClass(session)
			callback_message = bag_class._get_all_supplies(msg_data)

		# elif function == "random_gift":
		# 	bag_class = bag_module.BagSystemClass(session)
		# 	callback_message = bag_class._random_gift(msg_data)
		elif function =="random_gift_skill":
			lottery_class = lottery_module.LotterySystemClass(session)
			callback_message = lottery_class._random_gift_skill(msg_data)

		elif function =="get_skill":
			skill_class = skill_module.SkillSystemClass(session)
			dc = skill_class._get_skill(msg_data)
			callback_message = mc("0","got new skill success",dc)

		elif function =="level_up_scroll":
			bag_class = bag_module.BagSystemClass(session)
			callback_message = bag_class._level_up_scroll(msg_data)

		elif function =="level_up_weapon":
			weapon_class = weapon_module.WeaponSystemClass(session)
			callback_message = weapon_class._level_up_weapon(msg_data)

		elif function =="passive_skill_upgrade":
			weapon_class = weapon_module.WeaponSystemClass(session)
			callback_message = weapon_class._passive_skill_upgrade(msg_data)

		elif function =="reset_skill_point":
			weapon_class = weapon_module.WeaponSystemClass(session)
			callback_message = weapon_class._reset_skill_point(msg_data)

		elif callback_message=="":
			callback_message=mc("1","no function->"+function)
		Log("[GameAliya][ResolveMsg] callback_message="+callback_message)
		retval = des.encrypt(str.encode(str(callback_message)))
		mutex.release()
		return retval

if __name__ == "__main__":
	pass

