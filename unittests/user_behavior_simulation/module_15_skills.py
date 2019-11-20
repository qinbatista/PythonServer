import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client as tc
import random


lukseun = tc.LukseunClient('aliya',  port = 8880)

def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))

def skill_dialog(token,world,get_all_skill_info):
	print_module("[skill_dialog]")
	response = send_tcp_message({'world' : world, 'function' : 'level_up_skill', 'data' : {'token' : token,"skill":random.choice([i for i in range(0,38)]),"item":random.choice([6,7,8])}})#升级请求
	print(response)
	# while True:
	# 	skill_id = random.choice([i for i in range(0,38)])
	# 	skill_level = get_all_skill_info["data"]["remaining"][skill_id]
	# 	if skill_level==0:
	# 		get_random_skill()
	# 	else:
	# 		response = send_tcp_message({'world' : world, 'function' : 'level_up_skill', 'data' : {'token' : token,"skill_id":skill_id,"scroll_id":random.choice([6,7,8])}})#升级请求
	# 		print_method("[skill_dialog] level up skill success"+str(response))
	# 		if response["status"]==98:
	# 			module_12_store.purchase_skill_scroll()
	# 			break
	# 	if random.randint(0,1)==0:
	# 		print_method("[skill_dialog] quit skill dialog")
	# 		break
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
		else:
			break
def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")


logger = tc.logger
def login_decoration(func):
	def wrapper(*args, **kwargs):
		func(*args, **kwargs) if kwargs.__contains__("world") else (lambda response=send_tcp_message({'function': 'login_unique', 'data': {'unique_id': '1'}}): func(*args, **{'token': response['data']['token'], 'world': 0}))()
	return wrapper


# @login_decoration
def get_all_skill(**kwargs):
	response = send_tcp_message({'world': kwargs['world'], 'function': 'get_all_skill', 'data': {'token' : kwargs['token']}})
	logger.debug(response)

# @login_decoration
def level_up_skill(**kwargs):
	response = send_tcp_message({'world': kwargs['world'], 'function': 'level_up_skill', 'data' : {'token' : token,"skill_id":random.choice([i for i in range(0,38)]),"scroll_id":random.choice([6,7,8])}})#升级请求
	logger.debug(response)

# def skill_dialog(_token,_world,get_all_skill_info,**kwargs):
# 	level_up_skill(**kwargs)


skill_test = {
	1: get_all_skill,
	2: level_up_skill,
}

if __name__ == "__main__":
	skill_test[int(input('测试(1-2):'))]()
