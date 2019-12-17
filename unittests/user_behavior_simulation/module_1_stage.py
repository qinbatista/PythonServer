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
COLORS = {'pass' : '\033[92m', 'fail' : '\033[91m', 'end' : '\033[0m','ylw' : '\033[1;33;40m'}
def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))

def enter_stage(**kwargs):
	response = user_behavior_simulation.send_tcp_message({'world': kwargs['world'], 'function': 'enter_stage', 'data': {'token': kwargs['token'], 'stage': kwargs['stage']}})
	return response["status"]

def pass_stage(**kwargs):
	response = user_behavior_simulation.send_tcp_message({'world': kwargs['world'], 'function': 'pass_stage', 'data': {'token': kwargs['token'], 'stage': kwargs['stage'],'damage':kwargs['damage']}})

def start_hang_up(**kwargs):
	response = user_behavior_simulation.send_tcp_message({'world': kwargs['world'], 'function': 'start_hang_up', 'data': {'token': kwargs['token'], 'stage': kwargs['stage']}})

def get_hang_up_reward(**kwargs):
	response = user_behavior_simulation.send_tcp_message({'world': kwargs['world'], 'function': 'get_hang_up_reward', 'data': {'token': kwargs['token'], 'stage': kwargs['stage']}})

def check_boss_status(**kwargs):
	response = user_behavior_simulation.send_tcp_message({'world': kwargs['world'], 'function': 'check_boss_status', 'data': {'token': kwargs['token']}})

def get_top_damage(**kwargs):
	response = user_behavior_simulation.send_tcp_message({'world': kwargs['world'], 'function': 'get_top_damage', 'data': {'token': kwargs['token'], "page": 1}})

def stage_dialog(token,world,info_list):
	# while True:
	normal_stage = random.randint(1,1)
	boss_stage = 3000
	# check_boss_status(**{"world": world, "token": token})
	# enter_stage(**{"world": world, "token": token, "stage": boss_stage})
	# pass_stage(**{"world": world, "token": token, "stage": boss_stage, "damage": random.randint(0, 10000)})
	# input("继续")
	status=-1
	while status!=0:
		normal_stage = random.randint(1,1)
		status = enter_stage(**{"world":world,"token":token,"stage":normal_stage})
		if status==97:
			break
		else:
			pass_stage(**{"world":world,"token":token,"stage":normal_stage,"damage":random.randint(0,10000)})
			start_hang_up(**{"world":world,"token":token,"stage":normal_stage})
			get_hang_up_reward(**{"world":world,"token":token,"stage":normal_stage})
			check_boss_status(**{"world":world,"token":token})
			enter_stage(**{"world":world,"token":token,"stage":boss_stage})
			pass_stage(**{"world":world,"token":token,"stage":boss_stage,"damage":random.randint(0,10000)})
			get_top_damage(**{"world":world,"token":token})
			status=0

if __name__ == '__main__':
	unique_id = '1'
	# response = send_tcp_message({'function': 'login_unique', 'data': {'unique_id': unique_id}})
	# print(response)
	# token = response['data']['token']
	world = "s0"
	token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzkwNzEwNDYsInVpZCI6ImgwIn0.0etH168lGc1ORWUmcdycKytvDNfLmg5PPOVlzWlhAxM"
	n = 10
	while n <= 0:
		stage = random.choice([1, 2, 1001, 3000])
		print(f"stage:{stage}")
		check_boss_status(**{"world": world, "token": token})
		enter_stage(**{"world": world, "token": token, "stage": stage})
		pass_stage(**{"world": world, "token": token, "stage": stage, "damage": random.randint(50000, 100000)})
		n -= 1
		if n == 1: n = input("继续(n:0):")


