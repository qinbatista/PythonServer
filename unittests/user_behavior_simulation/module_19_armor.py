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
	def wrapper(world=0, token=None, *args, **kwargs):
		func(world, token, *args, **kwargs) if token else (lambda response=send_tcp_message({'function': 'login_unique', 'data': {'unique_id': '1'}}): func(world, response['data']['token'], *args, **kwargs))()
	return wrapper

@login_decoration
def get_all_armor(world, token, **kwargs):
	response = send_tcp_message({'world': world, 'function': 'get_all_armor', 'data': {'token': token}})
	logger.debug(response)

@login_decoration
def upgrade_armor(world, token, aid=1, level=2, **kwargs):
	response = send_tcp_message({'world': world, 'function': 'upgrade_armor', 'data': {'token': token, 'aid': aid, 'level': level}})
	logger.debug(response)


def darkmarket_dialog(world, token, aid, level, **kwargs):
	get_all_armor(world, token, **kwargs)
	upgrade_armor(world, token, aid, level, **kwargs)


armor_func = {
	0: get_all_armor,
	1: upgrade_armor,
}

if __name__ == '__main__':
	response = send_tcp_message({'function': 'login_unique', 'data': {'unique_id': '1'}})
	darkmarket_dialog(0, response['data']['token'], 1, 2)
	# armor_func[int(input('请输入需要执行的方法（0-1）：'))](0)
	# get_all_armor(0)
	# upgrade_armor(0, None, 1, 2)




