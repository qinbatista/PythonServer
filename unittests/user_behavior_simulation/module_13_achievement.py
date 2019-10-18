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
def purchase_basic_summon_scroll(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'purchase_basic_summon_scroll', 'data' : {'token' : kwargs['token'],"pakage_id":random.randint(1,3)}})#能量包，1是1张， 2是3张，3是10张
	logger.debug(response)

@login_decoration
def purchase_skill_scroll(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'purchase_skill_scroll', 'data' : {'token' : kwargs['token'],"pakage_id":random.randint(1,3)}})#能量包，1是1张， 2是3张，3是10张
	logger.debug(response)

@login_decoration
def purchase_coin(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'purchase_coin', 'data' : {'token' : kwargs['token'],"pakage_id":random.randint(1,6)}})#能量包，1是1张， 2是3张，3是10张
	logger.debug(response)

@login_decoration
def get_achievement_reward(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'get_achievement_reward', 'data' : {'token' : kwargs['token'],"achievement_id":random.randint(1,1), "value":1}})
	logger.debug(response)

@login_decoration
def get_all_achievement(**kwargs):
	response = send_tcp_message({'world' : kwargs['world'], 'function' : 'get_all_achievement', 'data' : {'token' : kwargs['token']}})
	logger.debug(response)

def achievement_dialog(info, **kwargs):
	# purchase_basic_summon_scroll(**kwargs)
	# purchase_skill_scroll(**kwargs)
	# purchase_coin(**kwargs)
	get_achievement_reward(**kwargs)
	get_all_achievement(**kwargs)

