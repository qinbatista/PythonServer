import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random
import user_behavior_simulation

def supplement_check_in(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'supplement_check_in', 'data' : {'token' : token}})

def check_in(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'check_in', 'data' : {'token' : token}})

def get_all_check_in_table(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_all_check_in_table', 'data' : {'token' : token}})

def check_in_dialog(token,world,respons):
	get_all_check_in_table(token,world)
	check_in(token,world)
	supplement_check_in(token,world)


if __name__ == '__main__':
	response = send_tcp_message({'function': 'login_unique', 'data': {'unique_id': '1'}})
	print(response)
	token = response['data']['token']
	# response = send_tcp_message({'world': 0, 'function': 'basic_summon', 'data': {'token': token, "item":random.choice([1, 5, 11])}})
	# response = send_tcp_message({'world': 0, 'function': 'friend_summon', 'data': {'token': token, "item":random.choice([1, 5, 11])}})
	# response = send_tcp_message({'world': 0, 'function': 'check_in', 'data': {'token': token}})
	response = send_tcp_message({'world': 0, 'function': 'supplement_check_in', 'data': {'token': token}})
	print(response)



