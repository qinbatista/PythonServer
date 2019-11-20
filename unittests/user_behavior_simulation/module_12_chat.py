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

def purchase_energy():
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'purchase_energy', 'data' : {'token' : token,"pakage_id":random.randint(1,2)}})#能量包，1是10体力， 2是100体力


def purchase_basic_summon_scroll():
	response = send_tcp_message({'world' : world, 'function' : 'purchase_basic_summon_scroll', 'data' : {'token' : token,"pakage_id":random.randint(1,3)}})#能量包，1是1张， 2是3张，3是10张


def purchase_skill_scroll():
	response = send_tcp_message({'world' : world, 'function' : 'purchase_skill_scroll', 'data' : {'token' : token,"pakage_id":random.randint(1,3)}})#能量包，1是1张， 2是3张，3是10张

def purchase_coin():
	response = send_tcp_message({'world' : world, 'function' : 'purchase_coin', 'data' : {'token' : token,"pakage_id":random.randint(1,6)}})#能量包，1是1张， 2是3张，3是10张

def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def mail_dialog(token,world,respons):
	pass