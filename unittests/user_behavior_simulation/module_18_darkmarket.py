import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random
import logging
logging.basicConfig(
	level=logging.DEBUG,
	format='%(asctime)s %(filename)s %(levelname)s message：%(message)s',
	datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)

lukseun = tool_lukseun_client.LukseunClient('aliya', port = 8880)
world = "0"
unique_id = "4"
token = ""
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

def darkmarket_dialog(token,world,info_list):
	automatically_refresh(**{"world": world, "token": token})

if __name__ == '__main__':
	# response = send_tcp_message({'function': 'login_unique', 'data': {'unique_id': '1'}})
	# automatically_refresh(**{'token': response['data']['token'], 'world': 0})
	automatically_refresh()




