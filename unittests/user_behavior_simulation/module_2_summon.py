import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client as tc
import random
import user_behavior_simulation

lukseun = tc.LukseunClient('aliya', port = 8880)
logger = tc.logger


def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))

# def login_decoration(func):
# 	def wrapper(token,world):
# 		func(token,world) if kwargs.__contains__("world") else (lambda response=send_tcp_message({'function': 'login_unique', 'data': {'unique_id': '1'}}): func(**{'token': response['data['token, 'world': 0}))()
# 	return wrapper

#
def basic_summon(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'basic_summon', 'data' : {'token' : token,"item":random.choice([1,5])}})


#
def pro_summon(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'pro_summon', 'data' : {'token' : token,"item":random.choice([1,5])}})


#
def friend_summon(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'friend_summon', 'data' : {'token' : token,"item":random.choice([1,5])}})


#
def basic_summon_skill(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'basic_summon_skill', 'data' : {'token' : token,"item":random.choice([1,5])}})


#
def pro_summon_skill(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'pro_summon_skill', 'data' : {'token' : token,"item":random.choice([1,5])}})


#
def friend_summon_skill(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'friend_summon_skill', 'data' : {'token' : token,"item":random.choice([1,5])}})


#
def basic_summon_role(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'basic_summon_role', 'data' : {'token' : token,"item":random.choice([1,5])}})


#
def pro_summon_role(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'pro_summon_role', 'data' : {'token' : token,"item":random.choice([1,5])}})


#
def friend_summon_role(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'friend_summon_role', 'data' : {'token' : token,"item":random.choice([1,5])}})


#
def basic_summon_10_times(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'basic_summon_10_times', 'data' : {'token' : token,"item":random.choice([1,5])}})



def pro_summon_10_times(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'basic_summon_10_times', 'data' : {'token' : token,"item":random.choice([1,5])}})



def friend_summon_10_times(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'friend_summon_10_times', 'data' : {'token' : token,"item":random.choice([1,5])}})#能量包，1是1张， 2是3张，3是10张



def basic_summon_skill_10_times(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'basic_summon_skill_10_times', 'data' : {'token' : token,"item":random.choice([1,5])}})#能量包，1是1张， 2是3张，3是10张



def pro_summon_skill_10_times(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'pro_summon_skill_10_times', 'data' : {'token' : token,"item":random.choice([1,5])}})#能量包，1是1张， 2是3张，3是10张



def friend_summon_skill_10_times(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'friend_summon_skill_10_times', 'data' : {'token' : token,"item":random.choice([1,5])}})#能量包，1是1张， 2是3张，3是10张



def basic_summon_role_10_times(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'basic_summon_role_10_times', 'data' : {'token' : token,"item":random.choice([1,5])}})#能量包，1是1张， 2是3张，3是10张



def pro_summon_role_10_times(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'pro_summon_role_10_times', 'data' : {'token' : token,"item":random.choice([1,5])}})#能量包，1是1张， 2是3张，3是10张



def friend_summon_role_10_times(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'friend_summon_role_10_times', 'data' : {'token' : token,"item":random.choice([1,5])}})#能量包，1是1张， 2是3张，3是10张


def summon_dialog(token, world):
	user_behavior_simulation.send_tcp_message({'world': world, 'function': 'refresh_diamond_store', 'data': {'token' : token}})
	user_behavior_simulation.send_tcp_message({'world': world, 'function': 'refresh_coin_store', 'data': {'token' : token}})
	user_behavior_simulation.send_tcp_message({'world': world, 'function': 'refresh_gift_store', 'data': {'token' : token}})
	user_behavior_simulation.send_tcp_message({'world': world, 'function': 'buy_refresh_diamond', 'data': {'token' : token}})
	user_behavior_simulation.send_tcp_message({'world': world, 'function': 'buy_refresh_coin', 'data': {'token' : token}})
	user_behavior_simulation.send_tcp_message({'world': world, 'function': 'buy_refresh_gift', 'data': {'token' : token}})
	user_behavior_simulation.send_tcp_message({'world': world, 'function': 'integral_convert', 'data': {'token' : token}})
	user_behavior_simulation.send_tcp_message({'world': world, 'function': 'single_pump_gift', 'data': {'token' : token}})
	user_behavior_simulation.send_tcp_message({'world': world, 'function': 'single_pump_coin', 'data': {'token' : token}})
	user_behavior_simulation.send_tcp_message({'world': world, 'function': 'dozen_pump_diamond', 'data': {'token' : token}})
	user_behavior_simulation.send_tcp_message({'world': world, 'function': 'single_pump_diamond', 'data': {'token' : token}})
	"""
	basic_summon(token,world)
	pro_summon(token,world)
	friend_summon(token,world)

	basic_summon_skill(token,world)
	pro_summon_skill(token,world)
	friend_summon_skill(token,world)

	basic_summon_role(token,world)
	pro_summon_role(token,world)
	friend_summon_role(token,world)

	basic_summon_10_times(token,world)
	pro_summon_10_times(token,world)
	friend_summon_10_times(token,world)

	basic_summon_skill_10_times(token,world)
	pro_summon_skill_10_times(token,world)
	friend_summon_skill_10_times(token,world)

	basic_summon_role_10_times(token,world)
	pro_summon_role_10_times(token,world)
	friend_summon_role_10_times(token,world)
	"""


if __name__ == '__main__':
	world = 's6'
	uid = '000'
	# data = {"function":"supplement_check_in","random":"31","world":"s0","data":{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODE2NjIxODMsInVpZCI6IjEyMzQ1NiJ9.vzi3Esjo00IpLHCGwP3mMUoT7iIOWeARwrSiuoWCuDQ"}}
	#
	# user_behavior_simulation.send_tcp_message(data)
	# res = user_behavior_simulation.send_tcp_message({'function': 'login_unique', 'data': {'unique_id': uid}})
	# res = user_behavior_simulation.send_tcp_message({'function': 'login', 'data': {'unique_id': uid, 'identifier': 'account', "value": "account00", "password":"123456"}})
	# token = res['data']['token']
	token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODYzMTA2MjAsInVpZCI6IjAwMCJ9.peKuE6MloEhiptLs9SUVBdHdpYp5ONNvLQK6f_r8Lx0'
	# stage = 8
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'level_up_skill', 'data': {'token': token, 'skill': 1, 'item': 6}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'supplement_check_in', 'data': {'token': token}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'get_new_mail', 'data': {'token': token}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'enter_stage', 'data': {'token': token, 'stage': stage}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'pass_stage', 'data': {'token': token, 'stage': stage}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'get_config_stage', 'data': {'token': token, 'stage': stage}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'mopping_up_stage', 'data': {'token': token, 'stage': stage}})
	# user_behavior_simulation.send_tcp_message({'world': 's9', 'function': 'respond_friend', 'data': {'token': token, 'key': '1578825778.M606582P1Q158.mail-678b475767-7qwgc'}})
	# token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODEyMzY2NzYsInVpZCI6IkMxNjA0NUQ1LTNBODUtNDVFRC04OTdELTI4ODNERjlDMDA1MCJ9.iG0319v13oHAfxijOkwOvqPMwT42Rptu_TCbjTRAVrg"
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'change_player_name', 'data': {'token': token, 'gn': 'bhjb  mnjk csa'}})
	# user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'use_item', 'data' : {'token' : token, 'item_id': '3:6:12', 'exchange_id': ''}})
	# user_behavior_simulation.send_tcp_message({'function': 'register', 'data': {'unique_id' : '', 'account': 'account00', 'password': '0password'}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'welfare_purchase_family', 'data': {'token' : token}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'get_config_notice', 'data': {'token' : token}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'buy_refresh_diamond', 'data': {'token' : token}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'buy_refresh_coin', 'data': {'token' : token}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'buy_refresh_gift', 'data': {'token' : token}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'integral_convert', 'data': {'token' : token}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'refresh_diamond_store', 'data': {'token' : token}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'single_pump_diamond', 'data': {'token' : token}})
	user_behavior_simulation.send_tcp_message({'world': world, 'function': 'single_pump_coin', 'data': {'token' : token}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'single_pump_gift', 'data': {'token' : token}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'dozen_pump_diamond', 'data': {'token' : token}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'dozen_pump_coin', 'data': {'token' : token}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'dozen_pump_gift', 'data': {'token' : token}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'refresh_coin_store', 'data': {'token' : token}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'refresh_gift_store', 'data': {'token' : token}})




