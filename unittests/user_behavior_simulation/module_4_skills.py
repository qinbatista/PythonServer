import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random
import module_12_store

lukseun = tool_lukseun_client.LukseunClient('aliya', '127.0.0.1', port = 8880)
world = "0"
unique_id = "4"
token = ""
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))

def skill_dialog(_token,_world,get_all_skill_info):
	print_module("[skill_dialog]")
	global token, world
	token = _token
	world = _world
	while True:
		skill_id = random.choice(["m1_level", "p1_level", "g1_level", "m11_level", "m12_level", "m13_level", "p11_level", "p12_level", "p13_level", "g11_level", "g12_level", "g13_level",
				"m111_level", "m112_level", "m113_level", "m121_level", "m122_level", "m123_level", "m131_level", "m132_level", "m133_level",
				"p111_level", "p112_level", "p113_level", "p121_level", "p122_level", "p123_level", "p131_level", "p132_level", "p133_level",
				"g111_level", "g112_level", "g113_level", "g121_level", "g122_level", "g123_level", "g131_level", "g132_level", "g133_level"])
		skill_level = get_all_skill_info["data"]["remaining"][skill_id]
		if skill_level==0:
			get_random_skill()
		else:
			response = send_tcp_message({'world' : world, 'function' : 'level_up_skill', 'data' : {'token' : token,"skill_id":skill_id,"scroll_id":random.choice(["skill_scroll_10","skill_scroll_30","skill_scroll_100"])}})#升级请求
			print_method("[skill_dialog] level up skill success"+str(response))
			if response["status"]==98:
				module_12_store.purchase_skill_scroll()
		if random.randint(0,1)==0:
			print_method("[skill_dialog] quit skill dialog")
			break
def purchase_skill_stuff():
	module_12_store.purchase_basic_summon_scroll()
def get_random_skill():
	print_module("[get_random_skill]")
	while True:
		int_n = random.randint(0,2)
		if int_n == 0: #朋友召唤
			print_method("[freind_dialog] friend gift to get skill")
			is_10 = random.choice([0,1])#是否十连抽
			if is_10==0:
				new_response = send_tcp_message({'world' : world, 'function' : 'basic_summon_skill', 'data' : {'token' : token,"cost_item":"friend_gift"}})
			else:
				new_response = send_tcp_message({'world' : world, 'function' : 'basic_summon_skill_10_times', 'data' : {'token' : token,"cost_item":"friend_gift"}})
			print_method("[get_random_skill] friend summon:"+str(new_response))
			if new_response["status"]!=0:
				purchase_skill_stuff()#购买流程
		elif int_n == 1:#高级召唤
			print_method("[freind_dialog] diamond gift to get skill")
			is_10 = random.choice([0,1])#是否十连抽
			if is_10==0:
				new_response = send_tcp_message({'world' : world, 'function' : 'pro_summon_skill', 'data' : {'token' : token,"cost_item":"basic_summon_scroll"}})
			else:
				new_response = send_tcp_message({'world' : world, 'function' : 'pro_summon_skill_10_times', 'data' : {'token' : token,"cost_item":"basic_summon_scroll"}})
			print_method("[get_random_skill] basic summon:"+str(new_response))
			if new_response["status"]!=0:
				purchase_skill_stuff()#购买流程
def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

if __name__ == "__main__":
	pass