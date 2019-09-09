import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random


lukseun = tool_lukseun_client.LukseunClient('aliya', '127.0.0.1', port = 8880)
world = "0"
unique_id = "4"
token = ""
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))


def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def friend_request(nonce):
	print_method("friend_request")
	new_response = send_tcp_message({'world' : world, 'function' : 'response_friend', 'data' : {'token' : token,"nonce":nonce}})
	return new_response

def gift_request(nonce):
	print_method("friend_request")
	new_response = send_tcp_message({'world' : world, 'function' : 'response_friend', 'data' : {'token' : token,"nonce":nonce}})
	return new_response

def accpet_all_request(nonce):
	pass
def get_all_new_mail():
	pass

def mail_dialog(_token,_world,_all_info):
	global world,token,all_info
	token = _token
	world = _world
	all_info = _all_info
	print_module("mail_dialog")
	for i in range(len(_all_info["data"]["mail"]["new"])):
		request_type = _all_info["data"]["mail"]["new"][i]["type"]
		print("request_type:"+request_type)
		if request_type == "friend_request":
			print(friend_request(_all_info["data"]["mail"]["new"][i]["data"]["nonce"]))