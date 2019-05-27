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
from Utility.sql_manager import working_cat as wcsql
DESKey = "67891234"
DESVector = "6789123467891234"

MessageList=[
	"{\"status\":\"0\",\"message\":\"success\"}",
	"{\"status\":\"1\",\"message\":\"failed\",\"time\":\"%s\"}"
]
class LoginSystemClass():
	def __init__(self, *args, **kwargs):
		pass
	def _login(self,message_info):
		"""
		user send login command, we return message with session to user
		"""
		message_dic  = eval(message_info)
		if "data" in message_dic.keys():
			unique_id = message_dic["data"]["unique_id"]
			account = message_dic["data"]["account"]
			password = message_dic["data"]["password"]
			if account=="":
				#if users don't have account, auto visitor login
				Log("[login_system.py][_login] use unique_id for seesion")
				return self.__visitor_login(unique_id)
			else:
				#if users have account and password, unique id is not usable but keep the value

				Log("[login_system.py][_login] use account for seesion")
				return self.__account_login(account,password)
		else:
			return "{\"status\":\"0\",\"message\":\"data is null\"}"
	def __visitor_login(self,unique_id):
		"""
		user login only with unique_id
		"""
		sql_result=wcsql("select account from userinfo where unique_id='"+unique_id+"'")
		if sql_result[0][0]=="":
			#if account is not exist try to find session
			sql_result=wcsql("select session from userinfo where unique_id='"+unique_id+"'")
			if sql_result[0][0]=="":
				#if session is not exist, it is a new user, createa a account for them
				session = self.__create_session_by_unique_id(unique_id)
				wcsql("INSERT INTO userinfo(unique_id,account,password,session) VALUES ('"+unique_id+"','"+""+"','"+""+"','"+session+"')")
			else:
				#if session is exist, just give them session
				session = str(sql_result[0][0])
			return "{\"status\":\"0\",\"message\":\"login as visitor\",\"session\":\""+session+"\",\"random\":\""+str(random.randint(-1000, 1000))+"\"}"
		else:
			#if account is exist but use visitor login, ask user use account to login
			return "{\"status\":\"1\",\"message\":\"this phone is already binded a account,please login as account\"}"
	def __account_login(self, account, password):
		"""
		user login with account and password
		"""
		sql_result=wcsql("select * from userinfo where account='"+account +"' and password='"+password+"'")
		if len(sql_result)<=0:
			return "{\"status\":\"0\",\"message\":\"account is not exist\"}"
		else:
			return "{\"status\":\"1\",\"message\":\"login as account\",\"session\":\""+self.__create_session_by_account(account,password)+"\",\"random\":\""+str(random.randint(-1000, 1000))+"\"}"
	def __create_session_by_unique_id(self,unique_id):
		"""
		return a session to user, right now just add _session with unique id, matthew will make really session
		"""
		return unique_id+"_session"
	def __create_session_by_account(self,account,password):
		"""
		return a session to user, right now just add _session with account id, matthew will make really session
		"""
		sql_result=wcsql("select session from userinfo where  account='"+account +"' and password='"+password+"'")
		if sql_result[0][0]=="":
			session= account+"_session"
			wcsql("UPDATE userinfo SET session='"+session+"' WHERE account='"+account +"' and password='"+password+"'")
			return session
		else:
			return sql_result[0][0]
if __name__ == "__main__":
	pass

