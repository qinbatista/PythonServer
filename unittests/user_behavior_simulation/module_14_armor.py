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
import user_behavior_simulation

lukseun = tc.LukseunClient('aliya', port = 8880)
logger = tc.logger


def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))

def login_decoration(func):
	def wrapper(world=0, token=None, *args, **kwargs):
		func(token, world, *args, **kwargs) if token else (lambda response=send_tcp_message({'function': 'login_unique', 'data': {'unique_id': '1'}}): func(world, response['data']['token'], *args, **kwargs))()
	return wrapper

# @login_decoration
def get_all_armor(token, world, **kwargs):
	response = user_behavior_simulation.send_tcp_message({'world': world, 'function': 'get_all_armor', 'data': {'token': token}})

# @login_decoration
def upgrade_armor(token, world, aid=1, level=2, **kwargs):
	response = user_behavior_simulation.send_tcp_message({'world': world, 'function': 'upgrade_armor', 'data': {'token': token, 'aid': aid, 'level': level}})


def armor_dialog(token, world, aid, **kwargs):
	get_all_armor(token, world, **kwargs)
	for i in range(1,10):
		upgrade_armor(token, world, 1, i, **kwargs)


armor_func = {
	0: get_all_armor,
	1: upgrade_armor,
}

if __name__ == '__main__':
	pass




