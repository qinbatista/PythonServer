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
def basic_summon():
	print_module("[basic_summon]")
	response = send_tcp_message({'world' : world, 'function' : 'basic_summon', 'data' : {'token' : token,"item":random.choice([1,5,11])}})
	print_method("[basic_summon]"+str(response))

def pro_summon():
	print_module("[pro_summon]")
	response = send_tcp_message({'world' : world, 'function' : 'pro_summon', 'data' : {'token' : token,"item":random.choice([1,5,12])}})
	print_method("[pro_summon]"+str(response))

def friend_summon():
	print_module("[friend_summon]")
	response = send_tcp_message({'world' : world, 'function' : 'friend_summon', 'data' : {'token' : token,"item":random.choice([1,5,16])}})
	print_method("[friend_summon]"+str(response))

def basic_summon_skill():
	print_module("[basic_summon_skill]")
	response = send_tcp_message({'world' : world, 'function' : 'basic_summon_skill', 'data' : {'token' : token,"item":random.choice([1,5,11])}})
	print_method("[basic_summon_skill]"+str(response))

def pro_summon_skill():
	print_module("[pro_summon_skill]")
	response = send_tcp_message({'world' : world, 'function' : 'pro_summon_skill', 'data' : {'token' : token,"item":random.choice([1,5,12])}})
	print_method("[pro_summon_skill]"+str(response))

def friend_summon_skill():
	print_module("[friend_summon_skill]")
	response = send_tcp_message({'world' : world, 'function' : 'friend_summon_skill', 'data' : {'token' : token,"item":random.choice([1,5,16])}})
	print_method("[friend_summon_skill]"+str(response))

def basic_summon_role():
	print_module("[basic_summon_role]")
	response = send_tcp_message({'world' : world, 'function' : 'basic_summon_role', 'data' : {'token' : token,"item":random.choice([1,5,11])}})
	print_method("[basic_summon_role]"+str(response))

def pro_summon_role():
	print_module("[pro_summon_role]")
	response = send_tcp_message({'world' : world, 'function' : 'pro_summon_role', 'data' : {'token' : token,"item":random.choice([1,5,12])}})
	print_method("[pro_summon_role]"+str(response))

def friend_summon_role():
	print_module("[friend_summon_role]")
	response = send_tcp_message({'world' : world, 'function' : 'friend_summon_role', 'data' : {'token' : token,"item":random.choice([1,5,16])}})
	print_method("[friend_summon_role]"+str(response))

def basic_summon_10_times():
	print_module("[basic_summon_10_times]")
	response = send_tcp_message({'world' : world, 'function' : 'basic_summon_10_times', 'data' : {'token' : token,"item":random.choice([1,5,11])}})
	print_method("[basic_summon_10_times]"+str(response))

def pro_summon_10_times():
	print_module("[pro_summon_10_times]")
	response = send_tcp_message({'world' : world, 'function' : 'basic_summon_10_times', 'data' : {'token' : token,"item":random.choice([1,5,12])}})
	print_method("[pro_summon_10_times]"+str(response))

def friend_summon_10_times():
	print_module("[friend_summon_10_times]")
	response = send_tcp_message({'world' : world, 'function' : 'friend_summon_10_times', 'data' : {'token' : token,"item":random.choice([1,3,16])}})#能量包，1是1张， 2是3张，3是10张
	print_method("[friend_summon_10_times]"+str(response))

def basic_summon_skill_10_times():
	print_module("[basic_summon_skill_10_times]")
	response = send_tcp_message({'world' : world, 'function' : 'basic_summon_skill_10_times', 'data' : {'token' : token,"item":random.choice([1,3,11])}})#能量包，1是1张， 2是3张，3是10张
	print_method("[basic_summon_skill_10_times]"+str(response))

def pro_summon_skill_10_times():
	print_module("[pro_summon_skill_10_times]")
	response = send_tcp_message({'world' : world, 'function' : 'pro_summon_skill_10_times', 'data' : {'token' : token,"item":random.choice([1,3,12])}})#能量包，1是1张， 2是3张，3是10张
	print_method("[pro_summon_skill_10_times]"+str(response))

def friend_summon_skill_10_times():
	print_module("[friend_summon_skill_10_times]")
	response = send_tcp_message({'world' : world, 'function' : 'friend_summon_skill_10_times', 'data' : {'token' : token,"item":random.choice([1,3,16])}})#能量包，1是1张， 2是3张，3是10张
	print_method("[friend_summon_skill_10_times]"+str(response))

def basic_summon_role_10_times():
	print_module("[basic_summon_role_10_times]")
	response = send_tcp_message({'world' : world, 'function' : 'basic_summon_role_10_times', 'data' : {'token' : token,"item":random.choice([1,3,11])}})#能量包，1是1张， 2是3张，3是10张
	print_method("[basic_summon_role_10_times]"+str(response))

def pro_summon_role_10_times():
	print_module("[pro_summon_role_10_times]")
	response = send_tcp_message({'world' : world, 'function' : 'pro_summon_role_10_times', 'data' : {'token' : token,"item":random.choice([1,3,12])}})#能量包，1是1张， 2是3张，3是10张
	print_method("[pro_summon_role_10_times]"+str(response))

def friend_summon_role_10_times():
	print_module("[friend_summon_role_10_times]")
	response = send_tcp_message({'world' : world, 'function' : 'friend_summon_role_10_times', 'data' : {'token' : token,"item":random.choice([1,3,16])}})#能量包，1是1张， 2是3张，3是10张
	print_method("[friend_summon_role_10_times]"+str(response))

def summon_dialog(_token,_world):
	global world,token
	world = _world
	token = _token
	basic_summon()
	pro_summon()
	friend_summon()

	basic_summon_skill()
	pro_summon_skill()
	friend_summon_skill()

	basic_summon_role()
	pro_summon_role()
	friend_summon_role()

	basic_summon_10_times()
	pro_summon_10_times()
	friend_summon_10_times()

	basic_summon_skill_10_times()
	pro_summon_skill_10_times()
	friend_summon_skill_10_times()

	basic_summon_role_10_times()
	pro_summon_role_10_times()
	friend_summon_role_10_times()







