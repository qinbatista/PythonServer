import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random


lukseun = tool_lukseun_client.LukseunClient('aliya', port = 8880)

def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))

def enter_stage(**kwargs):
	print("stage:"+str(kwargs['stage']))
	response = send_tcp_message({'world': kwargs['world'], 'function': 'enter_stage', 'data': {'token': kwargs['token'], 'stage': kwargs['stage']}})
	print("[enter_stage]"+str(response))

def pass_stage(**kwargs):
	print("stage:"+str(kwargs['stage']))
	response = send_tcp_message({'world': kwargs['world'], 'function': 'pass_stage', 'data': {'token': kwargs['token'], 'stage': kwargs['stage']}})
	print("[pass_stage]"+str(response))

def start_hang_up(**kwargs):
	response = send_tcp_message({'world': kwargs['world'], 'function': 'start_hang_up', 'data': {'token': kwargs['token'], 'stage': kwargs['stage']}})
	print_method("[start_hang_up]"+str(response)+" stage:"+str(kwargs['stage']))

def get_hang_up_reward(**kwargs):
	response = send_tcp_message({'world': kwargs['world'], 'function': 'get_hang_up_reward', 'data': {'token': kwargs['token'], 'stage': kwargs['stage']}})
	print_method("[get_hang_up_reward]"+str(response)+" stage:"+str(kwargs['stage']))

def check_boss_status(**kwargs):
	response = send_tcp_message({'world': kwargs['world'], 'function': 'check_boss_status', 'data': {'token': kwargs['token']}})
	print("[check_boss_status]"+str(response))

def enter_stage(**kwargs):
	response = send_tcp_message({'world': kwargs['world'], 'function': 'enter_stage', 'data': {'token': kwargs['token'], 'stage': kwargs['stage']}})
	print("[enter_stage]"+str(response))

def get_top_damage(**kwargs):
	response = send_tcp_message({'world': 0, 'function': 'get_top_damage', 'data': {'token': token, "page": 1}})
	print("[get_top_damage]"+str(response))

def stage_dialog(token,world,info_list):
	# while True:
	my_choice =  random.randint(1,1)
	normal_stage = random.randint(1,1)
	boss_stage = 3000
	if my_choice==0: enter_stage(**{"world":world,"token":token,"stage":normal_stage})
	if my_choice==1: pass_stage(**{"world":world,"token":token,"stage":normal_stage})
	if my_choice==2: start_hang_up(**{"world":world,"token":token,"stage":normal_stage})
	if my_choice==3: get_hang_up_reward(**{"world":world,"token":token,"stage":normal_stage})
	if my_choice==4: pass#break
	if my_choice==5: check_boss_status(**{"world":world,"token":token})
	if my_choice==6: enter_stage(**{"world":world,"token":token,"stage":boss_stage})
	if my_choice==7: pass_stage(**{"world":world,"token":token,"stage":boss_stage,"damage":random.randint(0,10000)})
	if my_choice==8: get_top_damage(**{"world":world,"token":token})

if __name__ == '__main__':
	unique_id = '1'
	response = send_tcp_message({'function': 'login_unique', 'data': {'unique_id': unique_id}})
	print(response)
	token = response['data']['token']
	response = send_tcp_message({'world': 0, 'function': 'pass_stage', 'data': {'token': token, 'stage': 3000, 'damage': 30000}})
	# response = send_tcp_message({'world': 0, 'function': 'get_config_stage', 'data': {'token': token, 'stage': 2}})
	# response = send_tcp_message({'world': 0, 'function': 'get_config_player', 'data': {'token': token}})
	print(str(response))
	# response = send_tcp_message({'world': 0, 'function': 'start_hang_up', 'data': {'token': token, 'stage': 1}})
	# print(str(response))
	# response = send_tcp_message({'world': 0, 'function': 'start_hang_up', 'data': {'token': token, 'stage': 1}})
	# print(str(response))



# player_info = await common.execute(f'select * from player;', **kwargs)
# print(player_info)



