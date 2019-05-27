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
from Utility.sql_manager import working_cat as wcsql
from WorkingCat import WorkingTimeRecoder

class MessageHandlerClass():
	def __init__(self,*args, **kwargs):
		pass
	def _set_app(self,app_name):
		"""
		get to know which app is and choice correct message handler to do that
		"""
		self.app_name = app_name
	def ResolveMsg(self, message, ip_address):# 客户端的数据、IP地址
		"""
		choice correct handler fot the message
		"""
		Log('[message_handler.py][ResolveMsg] app_name='+self.app_name)
		if self.app_name=="workingcat":
			resolve_msg_class = WorkingTimeRecoder.WorkingTimeRecoderClass()
			return resolve_msg_class._ResolveMsg(message,ip_address)

if __name__ == "__main__":
	pass

