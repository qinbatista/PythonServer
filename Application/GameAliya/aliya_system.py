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
		if function == "_bind_account":
			login_class = account_module.LoginSystemClass()
			callback_message = login_class._bind_account(msg_data)

		if callback_message=="":
			callback_message="{\"status\":\"1\",\"message\":\"no function->"+function+"\"}"
		Log("[WorkingTimeRecoder][ResolveMsg] callback_message="+callback_message)
		retval = des.encrypt(str.encode(str(callback_message)))
		mutex.release()
		return retval

if __name__ == "__main__":
	pass

