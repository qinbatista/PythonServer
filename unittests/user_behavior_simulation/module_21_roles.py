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
role_list=[i for i in range(1,2)]
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

	new_response = send_tcp_message({'world' : world, 'function' : 'level_up_role', 'data' : {'token' : token, "role":random.choice(role_list),"amount":random.randint(0,30000)}})#升级请求
	print("[level_up_role] level up role:"+str(new_response))

	new_response = send_tcp_message({'world' : world, 'function' : 'level_up_star_role', 'data' : {'token' : token, "role":random.choice(role_list)}})#升级请求
	print("[level_up_star_role] level up role star:"+str(new_response))

if __name__ == "__main__":
	pass
