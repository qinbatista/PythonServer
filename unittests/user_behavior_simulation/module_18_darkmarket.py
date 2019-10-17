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

def automatically_refresh(**kwargs):
	print_module("[automatically_refresh]")
	response = send_tcp_message({'world': kwargs['world'], 'function': 'automatically_refresh', 'data': {'token' : kwargs['token']}})
	print_method("[automatically_refresh]"+str(response))

def darkmarket_dialog(token,world,info_list):
	automatically_refresh(**{"world": world, "token": token})

if __name__ == '__main__':
	darkmarket_dialog(token, 0, list)





