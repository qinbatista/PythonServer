import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client as tc
import random
import user_behavior_simulation as user

lukseun = tc.LukseunClient('aliya', port = 8880)
logger = tc.logger


def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))

def login_decoration(func):
	def wrapper(world=0, token=None, *args, **kwargs):
		print("user.unique_id="+user.unique_id)
		func(world, token, *args, **kwargs) if token else (lambda response=send_tcp_message({'function': 'login_unique', 'data': {'unique_id': user.unique_id}}): func(world, response['data']['token'], *args, **kwargs))()
	return wrapper

# @login_decoration 此方法不再使用
# def get_all_market(token,world, **kwargs):
# 	response = send_tcp_message({'world': world, 'function': 'get_all_market', 'data': {'token' : token}})
# 	logger.debug(response)

# @login_decoration
def refresh_market(token,world, **kwargs):
	response = send_tcp_message({'world': world, 'function': 'refresh_market', 'data': {'token' : token}})
	logger.debug(response)

# @login_decoration
def darkmarket_transaction( token, world, pid, **kwargs):
	response = send_tcp_message({'world': world, 'function': 'darkmarket_transaction', 'data': {'token' : token, 'pid': pid}})
	logger.debug(response)

def darkmarket_dialog(token, world,**kwargs):
	refresh_market(token, world, **kwargs)
	darkmarket_transaction(token, world, random.randint(0,7), **kwargs)

if __name__ == '__main__':
	get_all_market()

	# refresh_market()
	# darkmarket_transaction(pid=1)




