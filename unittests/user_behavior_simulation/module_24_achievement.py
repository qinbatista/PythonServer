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





def purchase_basic_summon_scroll(token,world):
	response = send_tcp_message({'world' : world, 'function' : 'purchase_basic_summon_scroll', 'data' : {'token' : token,"pakage_id":random.randint(1,3)}})#能量包，1是1张， 2是3张，3是10张
	logger.debug(response)


def purchase_skill_scroll(token,world):
	response = send_tcp_message({'world' : world, 'function' : 'purchase_skill_scroll', 'data' : {'token' : token,"pakage_id":random.randint(1,3)}})#能量包，1是1张， 2是3张，3是10张
	logger.debug(response)


def purchase_coin(token,world):
	response = send_tcp_message({'world' : world, 'function' : 'purchase_coin', 'data' : {'token' : token,"pakage_id":random.randint(1,6)}})#能量包，1是1张， 2是3张，3是10张
	logger.debug(response)


def get_achievement_reward(token,world):
	response = send_tcp_message({'world' : world, 'function' : 'get_achievement_reward', 'data' : {'token' : token,"achievement_id":random.randint(1,1), "value":1}})
	logger.debug(response)


def get_all_achievement(token,world):
	response = send_tcp_message({'world' : world, 'function' : 'get_all_achievement', 'data' : {'token' : token}})
	logger.debug(response)

def achievement_dialog(token,world):
	# purchase_basic_summon_scroll(token,world)
	# purchase_skill_scroll(token,world)
	# purchase_coin(token,world)
	get_achievement_reward(token,world)
	get_all_achievement(token,world)

