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
def automatically_refresh(**kwargs):
	response = send_tcp_message({'world': kwargs['world'], 'function': 'automatically_refresh', 'data': {'token' : kwargs['token']}})
	logger.debug(response)

@login_decoration
def free_refresh(**kwargs):
	response = send_tcp_message({'world': kwargs['world'], 'function': 'free_refresh', 'data': {'token' : kwargs['token']}})
	logger.debug(response)

def darkmarket_dialog(token,world,info_list):
	automatically_refresh(**{"world": world, "token": token})
	free_refresh(**{"world": world, "token": token})

if __name__ == '__main__':
	# response = send_tcp_message({'function': 'login_unique', 'data': {'unique_id': '1'}})
	# kwargs = {"world": 0, "token": response['data']['token']}
	# automatically_refresh(**kwargs)
	# free_refresh(**kwargs)
	# automatically_refresh(**{'token': response['data']['token'], 'world': 0})
	# automatically_refresh()
	free_refresh()




