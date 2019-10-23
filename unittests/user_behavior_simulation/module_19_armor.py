# -*- coding: UTF-8 -*-
"""
test armor module
"""
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
	def wrapper(*args, **kwargs):
		func(*args, **kwargs) if kwargs.__contains__("world") else (lambda response=send_tcp_message({'function': 'login_unique', 'data': {'unique_id': '1'}}): func(*args, **{'token': response['data']['token'], 'world': 0}))()
	return wrapper

@login_decoration
def get_all_armor(**kwargs):
	response = send_tcp_message({'world': kwargs['world'], 'function': 'get_all_armor', 'data': {'token' : kwargs['token']}})
	logger.debug(response)

@login_decoration
def upgrade_armor(aid=1, level=2, **kwargs):
	response = send_tcp_message({'world': kwargs['world'], 'function': 'upgrade_armor', 'data': {'token' : kwargs['token']}})
	logger.debug(response)


def darkmarket_dialog(aid, level, **kwargs):
	get_all_armor(**kwargs)
	upgrade_armor(aid, level, **kwargs)


armor_func = {
	0: get_all_armor,
	1: upgrade_armor,
}

if __name__ == '__main__':
	# response = send_tcp_message({'function': 'login_unique', 'data': {'unique_id': '1'}})
	# kwargs = {"world": 0, "token": response['data']['token']}
	# get_all_armor(**kwargs)
	armor_func[int(input('请输入需要执行的方法（0-1）：'))]()
	# get_all_armor()
	# upgrade_armor(1, 2)




