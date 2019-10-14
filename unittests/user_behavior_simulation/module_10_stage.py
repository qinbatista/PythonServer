import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random


lukseun = tool_lukseun_client.LukseunClient('aliya', port = 8880)


def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))

def enter_stage(**kwargs):
	response = send_tcp_message({'world': kwargs['world'], 'function': 'enter_stage', 'data': {'token': kwargs['token'], 'stage': random.randint(1,1)}})
	print(response)

def pass_stage(**kwargs):
	response = send_tcp_message({'world': kwargs['world'], 'function': 'pass_stage', 'data': {'token': kwargs['token'], 'stage': random.randint(1,1)}})
	print(response)

def start_hang_up(**kwargs):
	response = send_tcp_message({'world': kwargs['world'], 'function': 'start_hang_up', 'data': {'token': kwargs['token'], 'stage': random.randint(1,1)}})
	print(response)

def get_hang_up_reward(**kwargs):
	response = send_tcp_message({'world': kwargs['world'], 'function': 'get_hang_up_reward', 'data': {'token': kwargs['token'], 'stage': random.randint(1,1)}})
	print(response)

def stage_dialog(token,world,info_list):
	enter_stage(**{"world":world,"token":token})
	pass_stage(**{"world":world,"token":token})
	start_hang_up(**{"world":world,"token":token})
	get_hang_up_reward(**{"world":world,"token":token})

if __name__ == '__main__':
	pass


