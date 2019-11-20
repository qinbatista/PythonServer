import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random


lukseun = tool_lukseun_client.LukseunClient('aliya', port = 8880)
world = "0"
unique_id = "4"
token = ""
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))

def login_decoration(func):
	def wrapper(*args, **kwargs):
		func(*args, **kwargs) if kwargs.__contains__("world") else (lambda response=send_tcp_message({'function': 'login_unique', 'data': {'unique_id': '1'}}): func(*args, **{'token': response['data']['token'], 'world': 0}))()
	return wrapper

def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def friend_request(nonce):
	print_method("friend_request")
	new_response = send_tcp_message({'world' : world, 'function' : 'request_friend', 'data' : {'token' : token,"nonce":nonce}})
	return new_response

def gift_request(world,token, key):
	print_method("gift_request")
	new_response = send_tcp_message({'world' : world, 'function' : 'accept_gift', 'data' : {'token' : token,"key":key}})
	return new_response

def family_request(nonce):
	print_method("response_family")
	new_response = send_tcp_message({'world' : world, 'function' : 'response_family', 'data' : {'token' : token,"nonce":nonce}})
	return new_response

def accpet_all_request(nonce):
	pass
def get_all_new_mail():
	pass
def send_friend():
	new_response = send_tcp_message({'world' : world, 'function' : 'request_friend', 'data' : {'token' : module_1_login.get_token("unique_id19"),"friend_name":"name_unique_id"+str(10)}})#发送好友信息
	print_method("[request_friend] requst_friend:"+str(new_response))

	new_response = send_tcp_message({'world' : world, 'function' : 'request_friend', 'data' : {'token' : module_1_login.get_token("unique_id18"),"friend_name":"name_unique_id"+str(10)}})#发送好友信息
	print_method("[request_friend] requst_friend:"+str(new_response))

	new_response = send_tcp_message({'world' : world, 'function' : 'request_friend', 'data' : {'token' : module_1_login.get_token("unique_id17"),"friend_name":"name_unique_id"+str(10)}})#发送好友信息
	print_method("[request_friend] requst_friend:"+str(new_response))

	new_response = send_tcp_message({'world' : world, 'function' : 'request_friend', 'data' : {'token' : module_1_login.get_token("unique_id16"),"friend_name":"name_unique_id"+str(10)}})#发送好友信息
	print_method("[request_friend] requst_friend:"+str(new_response))

	new_response = send_tcp_message({'world' : world, 'function' : 'request_friend', 'data' : {'token' : module_1_login.get_token("unique_id15"),"friend_name":"name_unique_id"+str(10)}})#发送好友信息
	print_method("[request_friend] requst_friend:"+str(new_response))

def send_family():
	new_response = send_tcp_message({'world' : world, 'function' : 'request_join_family', 'data' : {'token' : module_1_login.get_token("unique_id19"),"friend_name":"name_unique_id"+str(10)}})#发送好友信息
	print_method("[request_friend] requst_friend:"+str(new_response))

# @login_decoration
def send_gift(**kwargs):
	# new_response = send_tcp_message({'world' : kwargs['world'], 'function' : 'request_friend', 'data' : {'token' : kwargs['token'],"gn_target": "qqw"}})#发送好友信息
	# new_response = send_tcp_message({'world' : kwargs['world'], 'function' : 'send_gift_friend', 'data' : {'token' : kwargs['token'],"gn_target": "qqw"}})#发送好友信息
	# print("[request_friend] requst_friend:"+str(new_response))
	new_response = send_tcp_message({'world': world, 'function': 'request_friend', 'data': {'token': module_1_login.get_token("unique_id19"), "friend_name": "name_unique_id" + str(10)}})  # 发送好友信息
	print_method("[request_friend] requst_friend:"+str(new_response))
def get_all_mail():#获取所有邮件
	response = send_tcp_message({'world' : world, 'function' : 'get_all_mail', 'data' : {'token' : token}})#升级请求
	print("[get_all_mail]"+str(response))
	return response
def mail_dialog(_token,_world,_all_info,_name):
	name = _name
	token = _token
	world = _world
	all_info = _all_info
	# send_friend()
	# send_family()
	# send_gift()
	print_module("mail_dialog")
	if _all_info["status"]==62:
		return print_method("your email is empty")
	for i in range(len(_all_info["data"]["mail"])):
		request_type = _all_info["data"]["mail"][i]["type"]
		print_method("request_type:"+request_type)
		if request_type == '0':#simple
			friend_request(_all_info["data"]["mail"][i]["key"])
		if request_type == '1':#gift
			gift_request(world,token,_all_info["data"]["mail"][i]["key"])
		if request_type == '2':#friend_request
			friend_request(_all_info["data"]["mail"][i]["key"])
		if request_type == '3':#family_request
			gift_request(_all_info["data"]["mail"][i]["key"])

if __name__ == '__main__':
	send_gift()