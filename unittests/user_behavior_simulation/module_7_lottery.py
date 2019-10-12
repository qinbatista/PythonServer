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
role_list = ["role1", "role2", "role3", "role4", "role5", "role6", "role7", "role8", "role9", "role10", "role11", "role12", "role13", "role14", "role15", "role16", "role17", "role18", "role19", "role20", "role21", "role22", "role23", "role24", "role25", "role26", "role27", "role28", "role29", "role30", "role31", "role32", "role33", "role34", "role35", "role36", "role37", "role38", "role39", "role40"]
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))

def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")

def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def fortune_wheel_basic():
	print_module("[fortune_wheel_basic]")
	int_n = random.randint(0,1)
	if int_n == 0:
		new_response = send_tcp_message({'world' : world, 'function' : 'fortune_wheel_basic', 'data' : {'token' : token,"item":random.choices([1,5])}})#发送好友信息
		print_method("[fortune_wheel_basic][diamond]"+str(new_response))
	elif int_n == 1:
		new_response = send_tcp_message({'world' : world, 'function' : 'fortune_wheel_pro', 'data' : {'token' : token,"item":random.choices([1,5])}})#发送好友信息
		print_method("[fortune_wheel_basic][fortune_wheel_ticket_basic]"+str(new_response))
def get_random_item(_token,_world):
	global token,world
	token = _token
	world = _world
	print_module("[get_random_item]")
	while True:
		int_number = random.randint(0,1)
		if int_number==0: fortune_wheel_basic()
		if int_number==1: break