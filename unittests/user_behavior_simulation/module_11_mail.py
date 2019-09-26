import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random
import module_1_login

lukseun = tool_lukseun_client.LukseunClient('aliya', port = 8880)
world = "0"
unique_id = "4"
token = ""
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))


def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def friend_request(nonce):
	print_method("friend_request")
	new_response = send_tcp_message({'world' : world, 'function' : 'response_friend', 'data' : {'token' : token,"nonce":nonce}})
	return new_response

def gift_request(nonce):
	print_method("gift_request")
	new_response = send_tcp_message({'world' : world, 'function' : 'redeem_nonce', 'data' : {'token' : token,"nonce":nonce}})
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

def send_gift():
	new_response = send_tcp_message({'world' : world, 'function' : 'request_friend', 'data' : {'token' : module_1_login.get_token("unique_id19"),"friend_name":"name_unique_id"+str(10)}})#发送好友信息
	print_method("[request_friend] requst_friend:"+str(new_response))

def mail_dialog(_token,_world,_all_info,_name):
	global world,token,all_info,name
	name = _name
	token = _token
	world = _world
	all_info = _all_info
	send_friend()
	send_family()
	print_module("mail_dialog")
	if _all_info["status"]==62:
		return print_method("your email is empty")
	for i in range(len(_all_info["data"]["mail"]["new"])):
		request_type = _all_info["data"]["mail"]["new"][i]["type"]
		print_method("request_type:"+request_type)
		if request_type == "friend_request":
			friend_request(_all_info["data"]["mail"]["new"][i]["data"]["nonce"])
		if request_type == "gift":
			gift_request(_all_info["data"]["mail"]["new"][i]["data"]["nonce"])
