import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client as tc
import random


lukseun = tc.LukseunClient('aliya', port = 8880)
logger = tc.logger


def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))

def login_decoration(func):
	def wrapper(**kwargs):
		func(**kwargs) if kwargs.__contains__("world") else (lambda response=send_tcp_message({'function': 'login_unique', 'data': {'unique_id': '1'}}): func(**{'token': response['data']['token'], 'world': 0}))()
	return wrapper

@login_decoration
def basic_summon(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'basic_summon', 'data' : {'token' : kwargs['token'],"item":random.choice([1,5,11])}})
	logger.debug(response)

@login_decoration
def pro_summon(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'pro_summon', 'data' : {'token' : kwargs['token'],"item":random.choice([1,5,12])}})
	logger.debug(response)

@login_decoration
def friend_summon(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'friend_summon', 'data' : {'token' : kwargs['token'],"item":random.choice([1,5,16])}})
	logger.debug(response)

@login_decoration
def basic_summon_skill(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'basic_summon_skill', 'data' : {'token' : kwargs['token'],"item":random.choice([1,5,11])}})
	logger.debug(response)

@login_decoration
def pro_summon_skill(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'pro_summon_skill', 'data' : {'token' : kwargs['token'],"item":random.choice([1,5,12])}})
	logger.debug(response)

@login_decoration
def friend_summon_skill(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'friend_summon_skill', 'data' : {'token' : kwargs['token'],"item":random.choice([1,5,16])}})
	logger.debug(response)

@login_decoration
def basic_summon_role(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'basic_summon_role', 'data' : {'token' : kwargs['token'],"item":random.choice([1,5,11])}})
	logger.debug(response)

@login_decoration
def pro_summon_role(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'pro_summon_role', 'data' : {'token' : kwargs['token'],"item":random.choice([1,5,12])}})
	logger.debug(response)

@login_decoration
def friend_summon_role(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'friend_summon_role', 'data' : {'token' : kwargs['token'],"item":random.choice([1,5,16])}})
	logger.debug(response)

@login_decoration
def basic_summon_10_times(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'basic_summon_10_times', 'data' : {'token' : kwargs['token'],"item":random.choice([1,5,11])}})
	logger.debug(response)

@login_decoration
def pro_summon_10_times(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'basic_summon_10_times', 'data' : {'token' : kwargs['token'],"item":random.choice([1,5,12])}})
	logger.debug(response)

@login_decoration
def friend_summon_10_times(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'friend_summon_10_times', 'data' : {'token' : kwargs['token'],"item":random.choice([1,3,16])}})#能量包，1是1张， 2是3张，3是10张
	logger.debug(response)

@login_decoration
def basic_summon_skill_10_times(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'basic_summon_skill_10_times', 'data' : {'token' : kwargs['token'],"item":random.choice([1,3,11])}})#能量包，1是1张， 2是3张，3是10张
	logger.debug(response)

@login_decoration
def pro_summon_skill_10_times(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'pro_summon_skill_10_times', 'data' : {'token' : kwargs['token'],"item":random.choice([1,3,12])}})#能量包，1是1张， 2是3张，3是10张
	logger.debug(response)

@login_decoration
def friend_summon_skill_10_times(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'friend_summon_skill_10_times', 'data' : {'token' : kwargs['token'],"item":random.choice([1,3,16])}})#能量包，1是1张， 2是3张，3是10张
	logger.debug(response)

@login_decoration
def basic_summon_role_10_times(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'basic_summon_role_10_times', 'data' : {'token' : kwargs['token'],"item":random.choice([1,3,11])}})#能量包，1是1张， 2是3张，3是10张
	logger.debug(response)

@login_decoration
def pro_summon_role_10_times(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'pro_summon_role_10_times', 'data' : {'token' : kwargs['token'],"item":random.choice([1,3,12])}})#能量包，1是1张， 2是3张，3是10张
	logger.debug(response)

@login_decoration
def friend_summon_role_10_times(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'friend_summon_role_10_times', 'data' : {'token' : kwargs['token'],"item":random.choice([1,3,16])}})#能量包，1是1张， 2是3张，3是10张
	logger.debug(response)

def summon_dialog(**kwargs):
	basic_summon(**kwargs)
	pro_summon(**kwargs)
	friend_summon(**kwargs)

	basic_summon_skill(**kwargs)
	pro_summon_skill(**kwargs)
	friend_summon_skill(**kwargs)

	basic_summon_role(**kwargs)
	pro_summon_role(**kwargs)
	friend_summon_role(**kwargs)

	basic_summon_10_times(**kwargs)
	pro_summon_10_times(**kwargs)
	friend_summon_10_times(**kwargs)

	basic_summon_skill_10_times(**kwargs)
	pro_summon_skill_10_times(**kwargs)
	friend_summon_skill_10_times(**kwargs)

	basic_summon_role_10_times(**kwargs)
	pro_summon_role_10_times(**kwargs)
	friend_summon_role_10_times(**kwargs)



if __name__ == '__main__':
	response = send_tcp_message({'function': 'login_unique', 'data': {'unique_id': '1'}})
	print(response)
	token = response['data']['token']
	# response = send_tcp_message({'world': 0, 'function': 'basic_summon', 'data': {'token': token, "item":random.choice([1, 5, 11])}})
	# response = send_tcp_message({'world': 0, 'function': 'friend_summon', 'data': {'token': token, "item":random.choice([1, 5, 11])}})
	# response = send_tcp_message({'world': 0, 'function': 'check_boss_status', 'data': {'token': token, "item": 11}})
	response = send_tcp_message({'world': 0, 'function': 'get_config_factory', 'data': {'token': token, "item": 11}})
	# response = send_tcp_message({'world': 0, 'function': 'get_top_damage', 'data': {'token': token, "page": 1}})
	# response = send_tcp_message({'world': 0, 'function': 'enter_stage', 'data': {'token': token, "stage": 3000, "damange": 110000}})
	# response = send_tcp_message({'world': 0, 'function': 'pass_stage', 'data': {'token': token, "stage": 3000, "damange": 110001}})
	print(str(response).replace("'", "\""))



