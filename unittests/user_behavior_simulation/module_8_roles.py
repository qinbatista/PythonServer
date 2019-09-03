import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random


lukseun = tool_lukseun_client.LukseunClient('aliya', '127.0.0.1', port = 8880)
world = "0"
token = ""
role_list=["role1", "role2", "role3", "role4", "role5", "role6", "role7", "role8", "role9", "role10", "role11", "role12", "role13", "role14", "role15", "role16", "role17", "role18", "role19", "role20", "role21", "role22", "role23", "role24", "role25", "role26", "role27", "role28", "role29", "role30", "role31", "role32", "role33", "role34", "role35", "role36", "role37", "role38", "role39", "role40"]
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
			new_response = send_tcp_message({'world' : world, 'function' : 'upgrade_role_level', 'data' : {'token' : token, "role":random.choice(role_list),"experience_potion":random.randint(30,400)}})#升级请求
			print_method("[role_dialog] level up role:"+str(new_response))
			if new_response["status"]==95:#没有此角色
				get_random_role()
			if new_response["status"]==97:#材料不足冲关卡
				enter_level()
		elif random_int ==1:#突破角色
			new_response = send_tcp_message({'world' : world, 'function' : 'upgrade_role_star', 'data' : {'token' : token, "role":random.choice(role_list)}})#升级请求
			print_method("[role_dialog] level up role star:"+str(new_response))
			if new_response["status"]==98:
				get_random_role()
		elif random_int ==2:#退出
			print_method("[role_dialog] quit role_dialog")
			break
if __name__ == "__main__":
	pass
