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

def fortune_wheel_pro():
	new_response = send_tcp_message({'world' : world, 'function' : 'fortune_wheel_pro', 'data' : {'token' : token,"item":random.choice([1,5])}})#发送好友信息
	print("[fortune_wheel_pro][fortune_wheel_ticket_basic]"+str(new_response))

def fortune_wheel_basic():
	new_response = send_tcp_message({'world' : world, 'function' : 'fortune_wheel_basic', 'data' : {'token' : token,"item":random.choice([1,5])}})#发送好友信息
	print("[fortune_wheel_basic][diamond]"+str(new_response))

def get_random_item(_token,_world):
	global token,world
	token = _token
	world = _world
	fortune_wheel_basic()
	fortune_wheel_pro()


if __name__ == '__main__':
	response = send_tcp_message({'function': 'login_unique', 'data': {'unique_id': '1'}})
	print(response)
	token = response['data']['token']
	# response = send_tcp_message({'world': 0, 'function': 'basic_summon', 'data': {'token': token, "item":random.choice([1, 5, 11])}})
	# response = send_tcp_message({'world': 0, 'function': 'friend_summon', 'data': {'token': token, "item":random.choice([1, 5, 11])}})
	# response = send_tcp_message({'world': 0, 'function': 'check_in', 'data': {'token': token}})
	for i in range(100):
		# response = send_tcp_message({'world': 0, 'function': 'fortune_wheel_basic', 'data': {'token': token, 'item': 5}})
		response = send_tcp_message({'world': 0, 'function': 'fortune_wheel_pro', 'data': {'token': token, 'item': 5}})
		print(response)

