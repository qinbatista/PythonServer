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
token = ""
weapon_list = ["weapon1", "weapon2", "weapon3", "weapon4", "weapon5", "weapon6", "weapon7", "weapon8", "weapon9", "weapon10", "weapon11", "weapon12", "weapon13", "weapon14", "weapon15", "weapon16", "weapon17", "weapon18", "weapon19", "weapon20", "weapon21", "weapon22", "weapon23", "weapon24", "weapon25", "weapon26", "weapon27", "weapon28", "weapon29", "weapon30", "weapon31", "weapon32", "weapon33", "weapon34", "weapon35", "weapon36", "weapon37", "weapon38", "weapon39", "weapon40"]

def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))

def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def get_random_weapon():
	print_module("[get_random_weapon]")
	while True:
		int_n = random.randint(0,1)
		if int_n == 0: #金币召唤
			print_method("[get_random_weapon] coin to get weapon")
			is_10 = random.choice([0,1])
			if is_10==0:
				send_msg = {'world' : world, 'function' : 'basic_summon', 'data' : {'token' : token,"cost_item":"coin"}}
			else:
				send_msg = {'world' : world, 'function' : 'basic_summon_10_times', 'data' : {'token' : token,"cost_item":"coin"}}
			new_response = send_tcp_message(send_msg)#发送好友信息
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
			print_method("[get_random_weapon] diamond gift to get weapon")
			is_10 = random.choice([0,1])
			if is_10==0:
				send_msg = {'world' : world, 'function' : 'pro_summon', 'data' : {'token' : token,"cost_item":"basic_summon_scroll"}}
			else:
				send_msg = {'world' : world, 'function' : 'pro_summon_10_times', 'data' : {'token' : token,"cost_item":"basic_summon_scroll"}}
			new_response = send_tcp_message(send_msg)#发送好友信息
			if new_response["status"]!=0:
				purchase_item_success("basic_summon_scroll")#购买卷轴
				if random.choice([0,1])==0:
					continue
				else:
					break
			else:
				break
def enter_level():
	pass#未完成
def purchase_item_success(item_id):
	pass#未完成
def weapon_dialog(_token,_world,get_all_skill_info):
	print_module("[weapon_dialog]")
	while True:
		random_int = random.randint(0,4)
		if random_int ==0:#升级武器
			new_response = send_tcp_message({'world' : world, 'function' : 'level_up_weapon', 'data' : {'token' : token, "weapon":random.choice(weapon_list),"iron":random.randint(30,400)}})#升级请求
			print_method("[weapon_dialog] level up weapon:"+str(new_response))
			if new_response["status"]==95:#武器没有抽武器
				get_random_weapon()
			if new_response["status"]==95:#材料不足冲关卡
				enter_level()
		elif random_int ==1:#突破武器
			new_response = send_tcp_message({'world' : world, 'function' : 'level_up_weapon_star', 'data' : {'token' : token, "weapon":random.choice(weapon_list)}})#升级请求
			print_method("[weapon_dialog] level up weapon star:"+str(new_response))
			if new_response["status"]==98:
				get_random_weapon()
		elif random_int ==2:#升级被动
			new_response = send_tcp_message({'world' : world, 'function' : 'level_up_passive', 'data' : {'token' : token, "weapon":random.choice(weapon_list)}})#升级请求
			print_method("[weapon_dialog] level up weapon skill"+str(new_response))
		elif random_int ==3:#重制技能
			new_response = send_tcp_message({'world' : world, 'function' : 'reset_weapon_skill_point', 'data' : {'token' : token, "weapon":random.choice(weapon_list)}})#升级请求
			print_method("[weapon_dialog] reset weapon skill"+str(new_response))
		elif random_int ==4:#退出
			print_method("[weapon_dialog] quit weapon_dialog")
			break