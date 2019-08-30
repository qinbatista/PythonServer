import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random
lukseun = tool_lukseun_client.LukseunClient('aliya', '127.0.0.1', port = 8880)

def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))
world=""
unique_id=""

def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def login_unique():
	print_module("[login_unique]")
	response = send_tcp_message({'function' : 'login_unique', 'data' : {'unique_id' : unique_id}})
def login():
	print_module("[login]")
	num = random.choice(["account","email","phone_number"])
	if num =="account": account = unique_id+"account"
	if num =="email": account = unique_id+"@email.com"
	if num =="phone_number": account = "86"+unique_id[9:]
	response = send_tcp_message({'function' : 'login_unique', 'data' : {'identifier':random.choice(["account","email","phone_number"]), "value":account, "password":"123456"}})

def registered_account(world:str, unique_id: str):
	print_module("[registered_account]")
	response = send_tcp_message({'function' : 'login_unique', 'data' : {'unique_id' : unique_id}})
	if response["status"]==0:
		print_method("[registered_account] login success")
		return response["data"]["token"]
	else:
		print_method("[registered_account] login failed, try login again")
		registered_account(world,unique_id)
def login_module(world:str, unique_id: str):
	global world,unique_id
	world = world
	unique_id = unique_id
	login()

if __name__ == "__main__":
	pass