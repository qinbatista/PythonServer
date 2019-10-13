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

def login_decoration(func):
	def wrapper():
		response = send_tcp_message({'function': 'login_unique', 'data': {'unique_id': '1'}})
		global token
		token = response['data']['token']
		func()
	return wrapper


@ login_decoration
def enter_stage():
	response = send_tcp_message({'world': world, 'function': 'enter_stage', 'data': {'token': token, 'stage': 1}})
	print(response)

@ login_decoration
def pass_stage():
	response = send_tcp_message({'world': world, 'function': 'pass_stage', 'data': {'token': token, 'stage': 1}})
	print(response)

@ login_decoration
def enter_tower():
	response = send_tcp_message({'world': world, 'function': 'enter_tower', 'data': {'token': token, 'stage': 1}})
	print(response)

@ login_decoration
def pass_tower():
	response = send_tcp_message({'world': world, 'function': 'pass_tower', 'data': {'token': token, 'stage': 1}})
	print(response)

@ login_decoration
def start_hang_up():
	response = send_tcp_message({'world': world, 'function': 'start_hang_up', 'data': {'token': token, 'stage': 1}})
	print(response)


if __name__ == '__main__':
	# enter_stage()
	# pass_stage()
	# enter_tower()
	# pass_tower()
	start_hang_up()


