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
token = ""
role_list=[i for i in range(1,40)]
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))

def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")

def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def get_random_role():
	pass

def enter_level():
	pass

def role_dialog(_token,_world):
	print_module("[role_dialog]")
	global token,world
	token = _token
	world = _world
	while True:
		random_int = random.randint(0,2)
		if random_int ==0:#升级角色
			new_response = send_tcp_message({'world' : world, 'function' : 'level_up_role', 'data' : {'token' : token, "role":random.choice(role_list),"amount":random.randint(40000000000,300000000000)}})#升级请求
			print_method("[level_up_role] level up role:"+str(new_response))
		elif random_int ==1:#突破角色
			new_response = send_tcp_message({'world' : world, 'function' : 'level_up_star_role', 'data' : {'token' : token, "role":random.choice(role_list)}})#升级请求
			print_method("[level_up_star_role] level up role star:"+str(new_response))
		elif random_int ==2:#退出
			print_method("[role_dialog] quit role_dialog")
			break
if __name__ == "__main__":
	pass
