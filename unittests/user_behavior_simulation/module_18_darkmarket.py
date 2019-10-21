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
def automatically_refresh(**kwargs):
	response = send_tcp_message({'world': kwargs['world'], 'function': 'automatically_refresh', 'data': {'token' : kwargs['token']}})
	logger.debug(response)

@login_decoration
def free_refresh(**kwargs):
	response = send_tcp_message({'world': kwargs['world'], 'function': 'free_refresh', 'data': {'token' : kwargs['token']}})
	logger.debug(response)

@login_decoration
def diamond_refresh(**kwargs):
	response = send_tcp_message({'world': kwargs['world'], 'function': 'diamond_refresh', 'data': {'token' : kwargs['token']}})
	logger.debug(response)

@login_decoration
def darkmarket_transaction(pid, **kwargs):
	response = send_tcp_message({'world': kwargs['world'], 'function': 'darkmarket_transaction', 'data': {'token' : kwargs['token'], 'pid': pid}})
	logger.debug(response)

def darkmarket_dialog(pid, **kwargs):
	automatically_refresh(**kwargs)
	free_refresh(**kwargs)
	diamond_refresh(**kwargs)
	darkmarket_transaction(pid, **kwargs)


if __name__ == '__main__':
	# response = send_tcp_message({'function': 'login_unique', 'data': {'unique_id': '1'}})
	# kwargs = {"world": 0, "token": response['data']['token']}
	# automatically_refresh(**kwargs)
	# free_refresh(**kwargs)
	# automatically_refresh(**{'token': response['data']['token'], 'world': 0})
	# automatically_refresh()
	# free_refresh()
	# diamond_refresh()
	darkmarket_transaction(1)




