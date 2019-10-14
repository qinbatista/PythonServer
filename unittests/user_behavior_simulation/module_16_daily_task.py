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
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))
def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def get_all_task(token,world):
	print_module("[get_all_task]")
	response = send_tcp_message({'world' : world, 'function' : 'get_all_task', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张
	print_method("[get_all_task]"+str(response))

def get_task_reward(token,world):
	print_module("[get_task_reward]")
	response = send_tcp_message({'world' : world, 'function' : 'get_task_reward', 'data' : {'token' : token,"task_id":1}})#能量包，1是1张， 2是3张，3是10张
	print_method("[get_task_reward]"+str(response))

def task_dialog(token,world,respons):
	get_all_task(token,world)
	get_task_reward(token,world)





