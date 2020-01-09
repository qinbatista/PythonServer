import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random
import user_behavior_simulation

lukseun = tool_lukseun_client.LukseunClient('aliya', port = 8880)
world = "0"
token = ""
role_list=[i for i in range(1,2)]

def role_dialog(_token,_world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'level_up_role', 'data' : {'token' : token, "role":random.choice(role_list),"amount":random.randint(0,30000)}})#升级请求

	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'level_up_star_role', 'data' : {'token' : token, "role":random.choice(role_list)}})#升级请求


if __name__ == "__main__":
	world = "s6"
	token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzkxNDM1ODMsInVpZCI6ImgwIn0.sqnbjsCJ_8OefTY-M9IHFARhqQ6cm6kATzUUlRekwjY"
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'unlock_passive_role', 'data' : {'token' : token, "role": 1, 'passive': 102}})#升级请求
	# response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_all_role', 'data' : {'token' : token, "role": 1, 'passive': 101}})#升级请求

