import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random
import user_behavior_simulation

lukseun = tool_lukseun_client.LukseunClient('aliya', '127.0.0.1', port = 8880)
world = ""
token = ""
all_info =""
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))

def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def send_friend_gift():
	print_method("[send_friend_gift]="+str(all_info))
	if all_info["status"]==99:
		print_method(f'[freind_dialog] you have no friend')
		request_friend()
		return
	for i in range(0,len(all_info["data"]["remaining"]["f_name"])):
		new_response = send_tcp_message({'world' : world, 'function' : 'send_friend_gift', 'data' : {'token' : token,"friend_name":str(all_info["data"]["remaining"]["f_name"][i])}})
		if new_response["status"]==0:#给一个好友发送礼物
			print_method("[freind_dialog] send friend gift:"+new_response["data"]["remaining"]["f_name"][i])
		else:#朋友发送失败
			print_method(f'[freind_dialog] send {all_info["data"]["remaining"]["f_name"][i]} gift but failed, error:{new_response["message"]}')

def send_all_friend_gift():
	if all_info["status"]=="99":
		print_method(f'[freind_dialog] you have no friend')
		request_friend()
		return
	new_response = send_tcp_message({'world' : world, 'function' : 'send_all_friend_gift', 'data' : {'token' : token}})#发送好友信息
	print_method("[send_all_friend_gift]"+str(new_response))

def request_friend():
	print_method("[request_friend]")
	new_response = send_tcp_message({'world' : world, 'function' : 'request_friend', 'data' : {'token' : token,"friend_name":"name_unique_id"+str(random.randint(0,user_behavior_simulation.get_number()))}})#发送好友信息
	print_method("[freind_dialog] requst_friend:"+str(new_response))

def delete_friend():
	print_method("[delete_friend]")
	new_response = send_tcp_message({'world' : world, 'function' : 'delete_friend', 'data' : {'token' : token,"friend_name":"name_unique_id"+str(random.randint(0,user_behavior_simulation.get_number()))}})#发送好友信息
	print_method("[freind_dialog] delete_friend:"+str(new_response))

def freind_dialog(_token,_world,_all_info):
	print_module("[freind_dialog]")
	global world,token,all_info
	token = _token
	world = _world
	all_info = _all_info
	while True:
		int_random = random.randint(0,4)
		if int_random==0:#挨个发送好友爱心
			send_friend_gift()
		elif int_random==1:#发送所有好友信息
			send_all_friend_gift()
		elif int_random==2:#加好友
			request_friend()
		elif int_random==3:#删好友
			delete_friend()
		elif int_random ==4:
			print_method("[freind_dialog] quit friend dialog")
			break

if __name__ == "__main__":
	pass
