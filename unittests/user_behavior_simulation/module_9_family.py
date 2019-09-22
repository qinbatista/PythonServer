import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random


lukseun = tool_lukseun_client.LukseunClient('aliya', port = 8880)
world = "0"
token = ""
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))


def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def family_dialog(token,world,get_all_family_info):
	response = send_tcp_message({'world' : 0, 'function' : 'remove_user_family', 'data' : {'token': token, 'user': 'game name'}})
	print(response)
	response = send_tcp_message({'world' : 0, 'function' : 'leave_family', 'data' : {'token': token}})
	print(response)
	response = send_tcp_message({'world' : 0, 'function' : 'create_family', 'data' : {'token': token, 'fname': 'family name'}})
	print(response)
	response = send_tcp_message({'world' : 0, 'function' : 'get_all_family_info', 'data' : {'token': token}})
	print(response)
	response = send_tcp_message({'world' : 0, 'function' : 'family_sign_in', 'data' : {'token': token}})
	print(response)
	response = send_tcp_message({'world' : 0, 'function' : 'disbanded_family', 'data' : {'token': token}})
	print(response)
	response = send_tcp_message({'world' : 0, 'function' : 'cancel_disbanded_family', 'data' : {'token': token}})
	print(response)
	response = send_tcp_message({'world' : 0, 'function' : 'request_join_family', 'data' : {'token': token, 'fname': 'family name'}})
	print(response)
	response = send_tcp_message({'world' : 0, 'function' : 'invite_user_family', 'data' : {'token': token, 'target': 'game name'}})
	print(response)
	response = send_tcp_message({'world' : 0, 'function' : 'respond_family', 'data' : {'token': token, 'nonce': '234567899'}})
	print(response)
	response = send_tcp_message({'world' : 0, 'function' : 'family_officer', 'data' : {'token': token, 'target': 'game name', 'position': 0}})
	print(response)
	response = send_tcp_message({'world' : 0, 'function' : 'dismissal_family_officer', 'data' : {'token': token, 'target': 'game name'}})
	print(response)
	response = send_tcp_message({'world' : 0, 'function' : 'family_change_name', 'data' : {'token': token, 'family_name': 'family name'}})
	print(response)
	response = send_tcp_message({'world' : 0, 'function' : 'family_blackboard', 'data' : {'token': token}})
	print(response)
	response = send_tcp_message({'world' : 0, 'function' : 'family_announcement', 'data' : {'token': token}})
	print(response)
	response = send_tcp_message({'world' : 0, 'function' : 'get_family_store', 'data' : {'token': token}})
	print(response)
	response = send_tcp_message({'world' : 0, 'function' : 'family_market_purchase', 'data' : {'token': token, 'merchandise': 'merchandise'}})
	print(response)
	response = send_tcp_message({'world' : 0, 'function' : 'family_gift_package', 'data' : {'token': token}})
	print(response)
	response = send_tcp_message({'world' : 0, 'function' : 'get_family_config', 'data' : {'token': token}})
	print(response)

if __name__ == '__main__':
	response = send_tcp_message({'function' : 'login_unique', 'data' : {'unique_id' : '4'}})
	print(response)
	token = response['data']['token']
	family_dialog(token, 0, '')
