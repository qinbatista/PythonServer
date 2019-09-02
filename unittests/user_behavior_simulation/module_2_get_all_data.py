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
token = ""
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))
def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def get_level_info():#获取所有关卡信息
	response = send_tcp_message({'world' : int(world), 'function' : 'get_hang_up_info', 'data' : {'token' : token}})#挑战成功
	print({'world' : world, 'function' : 'get_hang_up_info', 'data' : {'token' : token}})
	print(response)
	return response
def get_all_info(_token,_world):
	global world,token
	world = _world
	token = _token
	return get_level_info()

if __name__ == "__main__":
	response = send_tcp_message({'world' : 0, 'function' : 'get_hang_up_info', 'data' : {'token' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzAwMDA1MDQsInVuaXF1ZV9pZCI6IjQifQ.5kDXhicPXIWc1KY4RkmTCKomMTeVEuSdC8LFR6rzWZ8'}})#挑战成功
	pass