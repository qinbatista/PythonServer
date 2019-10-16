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

def supplement_check_in(token,world):
	print_module("[supplement_check_in]")
	response = send_tcp_message({'world' : world, 'function' : 'supplement_check_in', 'data' : {'token' : token}})
	print_method("[supplement_check_in]"+str(response))

def check_in(token,world):
	print_module("[check_in]")
	response = send_tcp_message({'world' : world, 'function' : 'check_in', 'data' : {'token' : token}})
	print_method("[check_in]"+str(response))

def get_all_check_in_table(token,world):
	print_module("[get_all_check_in_table]")
	response = send_tcp_message({'world' : world, 'function' : 'get_all_check_in_table', 'data' : {'token' : token}})
	print_method("[get_all_check_in_table]"+str(response))

def check_in_dialog(token,world,respons):
	get_all_check_in_table(token,world)
	# check_in(token,world)
	# supplement_check_in(token,world)






