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
unique_id = "4"
token = ""
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))


def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def purchase_energy():
	pass

def enter_stage(token,world,response):
	print_module("[enter_level]:"+str(response))
	while True:
		my_number = random.randint(0,4)
		if my_number==0:#剧情
			yourstage = response["data"]["remaining"]["stage"]
			print_method("[enter_level] play normal level")
			stage = random.randint(1,yourstage+1)
			response_enter = send_tcp_message({'world' : world, 'function' : 'enter_stage', 'data' : {'token' : token, 'stage' : str(stage)}})#进入关卡
			if response_enter["status"]==0:
				response_enter = send_tcp_message({'world' : '0', 'function' : 'pass_stage', 'data' : {'token' : token, 'stage' : str(stage), 'clear_time' : 'we dont care what this string is'}})#挑战成功
				print_method("[enter_level] normal level passed")
			else:
				my_choice = random.choice([0,1])
				if my_choice==0:
					purchase_energy()
				else:
					break
		elif my_number==1:#世界boss
			print_method("[enter_level] play world boss")
			response_enter = send_tcp_message({'world' : world, 'function' : 'enter_world_boss_stage', 'data' : {'token' : token}})
			if response_enter["status"]==0:
				response_enter = send_tcp_message({'world' : world, 'function' : 'leave_world_boss_stage', 'data' : {'token' : token,"total_damage":random.randint(1,100000)}})
				print_method("[enter_level] challange boss success")
			else:
				my_choice = random.choice([0,1])
				if my_choice==0:
					response_enter = send_tcp_message({'world' : world, 'function' : 'get_top_damage', 'data' : {'token' : token,"range_number":random.randint(1,5)}})
					print_method("[enter_level] get top damage")
				else:
					break
		elif my_number==2:#无尽试炼
			print_method("[enter_level] endless training")
		elif my_number==3:#活动试炼
			print_method("[enter_level] party training")
		elif my_number==4:#退出
			print_method("[enter_level] quit level playing")
			break