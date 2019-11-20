import json
import time
import os
import requests
import configparser
import asyncio
import random
import user_behavior_simulation
def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")

def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def fortune_wheel_pro():
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'fortune_wheel_pro', 'data' : {'token' : token,"item":random.choice([1,5])}})#发送好友信息

def fortune_wheel_basic():
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'fortune_wheel_basic', 'data' : {'token' : token,"item":random.choice([1,5])}})#发送好友信息


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

