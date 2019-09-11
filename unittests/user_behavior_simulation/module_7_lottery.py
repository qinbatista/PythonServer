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
unique_id = "4"
token = ""
role_list = ["role1", "role2", "role3", "role4", "role5", "role6", "role7", "role8", "role9", "role10", "role11", "role12", "role13", "role14", "role15", "role16", "role17", "role18", "role19", "role20", "role21", "role22", "role23", "role24", "role25", "role26", "role27", "role28", "role29", "role30", "role31", "role32", "role33", "role34", "role35", "role36", "role37", "role38", "role39", "role40"]
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))

def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")

def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def purchase_item_success(item_id):
	pass

def enter_level():
	pass

def role_dialog():
	print_module("[role_dialog]")
	while True:
		random_int = random.randint(0,0)
		if random_int ==0:#升级角色
			new_response = send_tcp_message({'world' : world, 'function' : 'upgrade_role_level', 'data' : {'token' : token, "role":random.choice(role_list),"experience_potion":random.randint(30,400)}})#升级请求
			print_method("[role_dialog] level up role:")
			if new_response["status"]==95:#没有此角色
				get_random_role()
			if new_response["status"]==97:#材料不足冲关卡
				enter_level()
		elif random_int ==1:#突破角色
			new_response = send_tcp_message({'world' : world, 'function' : 'upgrade_role_star', 'data' : {'token' : token, "role":random.choice(role_list)}})#升级请求
			print_method("[role_dialog] level up role star:")
			if new_response["status"]==98:
				get_random_role()
		elif random_int ==2:#退出
			print_method("[role_dialog] quit role_dialog")
			break

def get_random_role():
	print_module("[get_random_role]")
	while True:
		int_n = random.randint(0,2)
		if int_n == 0: #金币召唤
			is_10 = random.choice([0,1])
			if is_10==0:
				new_response = send_tcp_message({'world' : world, 'function' : 'basic_summon_roles', 'data' : {'token' : token,"cost_item":"coin"}})#发送好友信息
			else:
				new_response = send_tcp_message({'world' : world, 'function' : 'basic_summon_roles_10_times', 'data' : {'token' : token,"cost_item":"coin"}})#发送好友信息
			print_method("[get_random_role] coin to get role new_response="+str(new_response))
			if new_response["status"]!=0:
				purchase_item_success("basic_summon_scroll")#购买卷轴
				coin_item = random.choice([0,2])
				if coin_item==0:
					continue#继续抽
				elif coin_item==1:
					enter_level()#进入关卡
					break
				elif coin_item==2:
					break#不抽
			else:
				break
		elif int_n == 1:#高级召唤
			is_10 = random.choice([0,1])
			if is_10==0:
				new_response = send_tcp_message({'world' : world, 'function' : 'pro_summon_roles', 'data' : {'token' : token,"cost_item":"basic_summon_scroll"}})#发送好友信息
			else:
				new_response = send_tcp_message({'world' : world, 'function' : 'pro_summon_roles_10_times', 'data' : {'token' : token,"cost_item":"basic_summon_scroll"}})#发送好友信息
			print_method("[get_random_role] coin to get role new_response="+str(new_response))
			if new_response["status"]!=0:
				purchase_item_success("basic_summon_scroll")#购买卷轴
				if random.choice([0,1])==0:
					continue
				else:
					break
			else:
				break
		elif int_n == 2:#朋友召唤
			is_10 = random.choice([0,1])
			if is_10==0:
				new_response = send_tcp_message({'world' : world, 'function' : 'basic_summon_roles', 'data' : {'token' : token,"cost_item":"friend_gift"}})#朋友抽
			else:
				new_response = send_tcp_message({'world' : world, 'function' : 'basic_summon_roles_10_times', 'data' : {'token' : token,"cost_item":"friend_gift"}})#朋友抽
			print_method("[get_random_role] coin to get role:"+str(new_response))
def get_random_weapon():
	print_module("[get_random_weapon]")
	while True:
		int_n = random.randint(0,1)
		if int_n == 0: #金币召唤
			is_10 = random.choice([0,1])
			if is_10==0:
				new_response = send_tcp_message({'world' : world, 'function' : 'basic_summon', 'data' : {'token' : token,"cost_item":"coin"}})
			else:
				new_response = send_tcp_message({'world' : world, 'function' : 'basic_summon_10_times', 'data' : {'token' : token,"cost_item":"coin"}})
			print_method("[get_random_weapon] coin to get weapon:"+str(new_response))
			if new_response["status"]!=0:
				purchase_item_success("coin")#购买金币
				coin_item = random.choice([0,2])
				if coin_item==0:
					continue#继续抽
				elif coin_item==1:
					enter_level()#进入关卡
					break
				elif coin_item==2:
					break#不抽
			else:
				break
		elif int_n == 1:#高级召唤
			is_10 = random.choice([0,1])
			if is_10==0:
				new_response = send_tcp_message({'world' : world, 'function' : 'pro_summon', 'data' : {'token' : token,"cost_item":"basic_summon_scroll"}})
			else:
				new_response = send_tcp_message({'world' : world, 'function' : 'pro_summon_10_times', 'data' : {'token' : token,"cost_item":"basic_summon_scroll"}})
			print_method("[get_random_weapon] diamond gift to get weapon:"+str(new_response))
			if new_response["status"]!=0:
				purchase_item_success("basic_summon_scroll")#购买卷轴
				if random.choice([0,1])==0:
					continue
				else:
					break
			else:
				break

def get_random_skill():
	print_module("[get_random_skill]")
	while True:
		int_n = random.randint(0,1)
		if int_n == 0: #朋友召唤
			is_10 = random.choice([0,1])
			if is_10==0:
				new_response = send_tcp_message({'world' : world, 'function' : 'basic_summon_skill', 'data' : {'token' : token,"cost_item":"friend_gift"}})#发送好友信息
			else:
				new_response = send_tcp_message({'world' : world, 'function' : 'basic_summon_skill_10_times', 'data' : {'token' : token,"cost_item":"friend_gift"}})#发送好友信息
			print_method("[freind_dialog] friend gift to get skill:"+str(new_response))
		elif int_n == 1:#高级召唤
			is_10 = random.choice([0,1])
			if is_10==0:
				new_response = send_tcp_message({'world' : world, 'function' : 'pro_summon_skill', 'data' : {'token' : token,"cost_item":"basic_summon_scroll"}})
			else:
				new_response = send_tcp_message({'world' : world, 'function' : 'pro_summon_skill_10_times', 'data' : {'token' : token,"cost_item":"basic_summon_scroll"}})
			print_method("[freind_dialog] diamond gift to get skill:"+str(new_response))
			if new_response["status"]!=0:
				purchase_item_success("basic_summon_scroll")#购买卷轴
				if random.choice([0,1])==0:
					continue
				else:
					break
			else:
				break

def get_random_item(_token,_world):
	global token,world
	token = _token
	world = _world
	print_module("[get_random_item]")
	while True:
		int_number = random.randint(0,3)
		if int_number==0: get_random_role()
		if int_number==1: get_random_skill()
		if int_number==2: get_random_weapon()
		if int_number==3: break