import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random
import user_behavior_simulation

lukseun = tool_lukseun_client.LukseunClient('aliya', port = 8880)
world = ""
token = ""
all_info =""
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))

def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def send_gift_friend(_all_info):
	names = _all_info["data"]["friends"]
	for name in names:
		new_response = send_tcp_message({'world' : world, 'function' : 'send_gift_friend', 'data' : {'token' : token,"gn_target":name["gn"]}})
		print_method("[send_gift_friend]"+str(new_response))

def send_gift_all():
	new_response = send_tcp_message({'world' : world, 'function' : 'send_gift_all', 'data' : {'token' : token}})#发送好友信息
	print_method("[send_all_friend_gift]"+str(new_response))

def request_friend():
	print_method("[request_friend]")
	new_response = send_tcp_message({'world' : world, 'function' : 'request_friend', 'data' : {'token' : token,"gn_target":"name_unique_id"+str(random.randint(0,user_behavior_simulation.get_number()))}})#发送好友信息
	# new_response = send_tcp_message({'world' : world, 'function' : 'request_friend', 'data' : {'token' : token,"gn_target":"哲帅蛰引瞩锑"}})#发送好友信息
	print_method("[request_friend] requst_friend:"+str(new_response))

def remove_friend():
	print_method("[remove_friend]")
	new_response = send_tcp_message({'world' : world, 'function' : 'remove_friend', 'data' : {'token' : token,"gn_target":"name_unique_id"+str(random.randint(0,user_behavior_simulation.get_number()))}})#发送好友信息
	# new_response = send_tcp_message({'world' : world, 'function' : 'remove_friend', 'data' : {'token' : token,"gn_target":"哲帅蛰引瞩锑"}})#发送好友信息
	print_method("[remove_friend] remove_friend:"+str(new_response))

def find_person():
	print_method("[find_person]")
	# new_response = send_tcp_message({'world' : world, 'function' : 'find_person', 'data' : {'token' : token,"gn_target":"name_unique_id"+str(random.randint(0,user_behavior_simulation.get_number()))}})#发送好友信息
	new_response = send_tcp_message({'world' : world, 'function' : 'find_person', 'data' : {'token' : token,"gn_target":"后起之秀"}})#发送好友信息
	print_method("[find_person]:"+str(new_response))

def freind_dialog(_token,_world,_all_info):
	print_module("[freind_dialog]"+str(_all_info))
	global world,token,all_info
	token = _token
	world = _world
	all_info = _all_info
	while True:
		int_random = random.randint(5,5)
		if int_random==0:#添加好友
			request_friend()
		elif int_random==1:#给某个朋友发送礼物
			send_gift_friend(_all_info)
		elif int_random==2:#发送所有好友信息
			send_gift_all()
		elif int_random==3:#删好友
			remove_friend()
		elif int_random ==4:
			print_method("[freind_dialog] quit friend dialog")
			break
		elif int_random ==5:#查找好友
			find_person()

if __name__ == "__main__":
	pass
