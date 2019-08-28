import json
import time
import os
import requests
import configparser
import asyncio
import lukseun_client
import random
"""
print(str(time.time()))
print(str(time.time() % 1 * 1e6))
print(str(os.getpid()))
"""

CONFIG = configparser.ConfigParser()
CONFIG.read('../Application/GameAliya/Configuration/server/1.0/server.conf', encoding="utf-8")
# GAME_MANAGER_BASE_URL = 'http://localhost:' + CONFIG['game_manager']['port']
GAME_MANAGER_BASE_URL = 'http://localhost:8100'
# GAME_MANAGER_BASE_URL = 'http://localhost:8007'
# GAME_MANAGER_BASE_URL = 'http://localhost:8006'



def try_coin():
	result = requests.post(GAME_MANAGER_BASE_URL + '/try_coin', data={'unique_id': "4", "value": 255})
	print(str(result.text))


def try_iron():
	result = requests.post(GAME_MANAGER_BASE_URL + '/try_iron', data={'unique_id': "4", "value": -50})
	print(str(result.text))


def try_diamond():
	result = requests.post(GAME_MANAGER_BASE_URL + '/try_diamond', data={'world':0, 'unique_id': "4", "value": -1000})
	print(str(result.text))


def level_up_weapon():
	result = requests.post(GAME_MANAGER_BASE_URL + '/level_up_weapon', data={'world':0, 'unique_id': "4", "weapon": "weapon1", "iron": 1000})
	print(str(result.text))


def pass_stage(stage: int):
	result = requests.post(GAME_MANAGER_BASE_URL + '/pass_stage', data={'world':0, 'unique_id': "4", "stage": stage, "clear_time": "2019-07-25 18:34:53"})
	print(str(result.text))


def pass_tower(stage: int):
	result = requests.post(GAME_MANAGER_BASE_URL + '/pass_tower', data={"world": 0, 'unique_id': "4", 'stage': stage, "clear_time": "2019-07-25 18:34:53"})
	print(str(result.text))


def get_skill():
	result = requests.post(GAME_MANAGER_BASE_URL + '/get_skill', data={'world':0, 'unique_id': "4", "skill_id": "m1_level"})
	print(str(result.text))


def get_all_skill_level():
	result = requests.post(GAME_MANAGER_BASE_URL + '/get_all_skill_level', data={'world':0, 'unique_id': "4"})
	print(str(result.text))


def level_up_skill():
	result = requests.post(GAME_MANAGER_BASE_URL + '/level_up_skill', data={'world':0, 'unique_id': "4", "skill_id": "m1_level",  "scroll_id": "skill_scroll_10"})
	print(str(result.text))


def random_gift_skill():
	result = requests.post(GAME_MANAGER_BASE_URL + '/random_gift_skill', data={'unique_id': "4"})
	print(str(result.text))


def random_gift_weapon():
	result = requests.post(GAME_MANAGER_BASE_URL + '/random_gift_weapon', data={'unique_id': "4"})
	print(str(result.text))


def level_up_scroll():
	result = requests.post(GAME_MANAGER_BASE_URL + '/level_up_scroll', data={'unique_id': "4", "scroll_id": "skill_scroll_100"})
	print(str(result.text))


def get_all_weapon():
	result = requests.post(GAME_MANAGER_BASE_URL + '/get_all_weapon', data={'world': 0, 'unique_id': "4"})
	print(str(result.text))


def level_up_passive():
	result = requests.post(GAME_MANAGER_BASE_URL + '/level_up_passive', data={'world': 0, 'unique_id': "4", "weapon": "weapon1", "passive": "passive_skill_1_level"})
	print(str(result.text))


def reset_weapon_skill_point():
	result = requests.post(GAME_MANAGER_BASE_URL + '/reset_weapon_skill_point', data={'world': 0, 'unique_id': "4", "weapon": "weapon1"})
	print(str(result.text))


def level_up_weapon_star():
	result = requests.post(GAME_MANAGER_BASE_URL + '/level_up_weapon_star', data={'world': 0, 'unique_id': "4", "weapon": "weapon10"})
	print(str(result.text))


def try_all_material():
	result = requests.post(GAME_MANAGER_BASE_URL + '/try_all_material', data={'unique_id': "4", "stage": "5"})
	print(str(result.text))


def try_energy():
	result = requests.post(GAME_MANAGER_BASE_URL + '/try_energy', data={'unique_id': "4", "amount": "2"})
	print(str(result.text))


def start_hang_up():
	result = requests.post(GAME_MANAGER_BASE_URL + '/start_hang_up', data={"world": 0, 'unique_id': "4", "stage": "2"})
	print(str(result.text))


def get_hang_up_reward():
	result = requests.post(GAME_MANAGER_BASE_URL + '/get_hang_up_reward', data={"world": 0, 'unique_id': "4"})
	print(str(result.text))


def enter_stage(stage: int):
	result = requests.post('http://localhost:8004/enter_stage', data={"world": 0, 'unique_id': "4", 'stage': stage})
	print(str(result.text))


def enter_tower(stage: int):
	result = requests.post(GAME_MANAGER_BASE_URL + '/enter_tower', data={"world": 0, 'unique_id': "4", 'stage': stage})
	print(str(result.text))


def disintegrate_weapon():
	result = requests.post(GAME_MANAGER_BASE_URL + '/disintegrate_weapon', data={"world": 0, 'unique_id': "4", 'weapon': 'weapon12'})
	print(str(result.text))


def automatically_refresh_store():
	result = requests.post(GAME_MANAGER_BASE_URL + '/automatically_refresh_store', data={"world": 0, 'unique_id': "4"})
	print(str(result.text))


def manually_refresh_store():
	result = requests.post(GAME_MANAGER_BASE_URL + '/manually_refresh_store', data={"world": 0, 'unique_id': "4"})
	print(str(result.text))


def diamond_refresh_store():
	result = requests.post(GAME_MANAGER_BASE_URL + '/diamond_refresh_store', data={"world": 0, 'unique_id': "4"})
	print(str(result.text))


def black_market_transaction(code: int=0):
	result = requests.post(GAME_MANAGER_BASE_URL + '/black_market_transaction', data={"world": 0, 'unique_id': "4", 'code': code})
	print(str(result.text))


def show_energy():
	result = requests.post(GAME_MANAGER_BASE_URL + '/show_energy', data={"world": 0, 'unique_id': "4"})
	print(str(result.text))


def get_all_supplies():
	result = requests.post(GAME_MANAGER_BASE_URL + '/get_all_supplies', data={"world": 0, 'unique_id': "4"})
	print(str(result.text))


def basic_summon():
	result = requests.post(GAME_MANAGER_BASE_URL + '/basic_summon', data={"world": 0, 'unique_id': "4", "cost_item": "diamond"})
	print(str(result.text))


def get_hang_up_info():
	result = requests.post(GAME_MANAGER_BASE_URL + '/get_hang_up_info', data={"world": 0, 'unique_id': "4"})
	print(str(result.text))


def upgrade_armor(level: int):
	result = requests.post('http://localhost:8004/upgrade_armor', data={"world": 0, 'unique_id': "4", "armor_id": "armor1", "level": level})
	print(str(result.text))


def random_gift_segment():
	result = requests.post('http://localhost:8007/random_gift_segment', data={"world": 0, 'unique_id': "4"})
	print(str(result.text))


def send_friend_gift(unique_id: str, friend_name: str):
	result = requests.post('http://localhost:8004/send_friend_gift', data={"world": 0, 'unique_id': unique_id, "friend_name": friend_name})
	print(str(result.text))


def get_new_mail(unique_id: str):
	result = requests.post('http://localhost:8004/get_new_mail', data={"world": 0, 'unique_id': unique_id})
	print(str(result.text))
	return result.json()['data']['mail'][0]['data']['nonce']


def get_all_mail(unique_id: str):
	result = requests.post('http://localhost:8004/get_all_mail', data={"world": 0, 'unique_id': unique_id})
	print(str(result.text))


def redeem_nonce(unique_id: str, nonce: str):
	result = requests.post('http://localhost:8004/redeem_nonce', data={"world": 0, 'unique_id': unique_id, "nonce": nonce})
	print(str(result.text))


def request_friend(unique_id: str, friend_name: str):
	# result = requests.post('http://localhost:8006/request_friend', data={"world": 0, 'unique_id': 4, "friend_name": "曲永杰"})
	# result = requests.post('http://localhost:8006/request_friend', data={"world": 0, 'unique_id': 4, "friend_name": "quyongjie"})
	result = requests.post('http://localhost:8004/request_friend', data={"world": 0, 'unique_id': unique_id, "friend_name": friend_name})
	print(str(result.text))


def response_friend(unique_id: str, nonce: str):
	result = requests.post('http://localhost:8004/response_friend', data={"world": 0, 'unique_id': unique_id, "nonce": nonce})
	print(str(result.text))


def send_all_friend_gift(unique_id: str):
	result = requests.post('http://localhost:8004/send_all_friend_gift', data={"world": 0, 'unique_id': unique_id})
	print(str(result.text))


def get_new_mail_nonce_list(unique_id: str) -> (list, list):
	result = requests.post('http://localhost:8100/get_new_mail', data={"world": 0, 'unique_id': unique_id})
	print(str(result.text))
	type_list = []
	nonce_list = []
	for data in result.json()['data']['mail']:
		type_list.append(data['type'])
		nonce_list.append(data['data']['nonce'])
	print(f"type_list: {type_list}")
	print(f"nonce_list: {nonce_list}")
	return type_list, nonce_list

def redeem_all_nonce(unique_id: str, type_list: list, nonce_list: list):
	result = requests.post('http://localhost:8004/redeem_all_nonce', data={"world": 0, 'unique_id': unique_id, "type_list": type_list, "nonce_list": nonce_list})
	print(str(result.text))

def leave_world_boss_stage(unique_id: str,total_damage:int):
	result = requests.post('http://localhost:8100/leave_world_boss_stage', data={"world": 0, 'unique_id': unique_id, "total_damage": total_damage})
	print(str(result.text))

def enter_world_boss_stage(unique_id: str):
	result = requests.post('http://localhost:8004/enter_world_boss_stage', data={"world": 0, 'unique_id': unique_id})
	print(str(result.text))

def check_boss_status(unique_id: str):
	result = requests.post('http://localhost:8004/check_boss_status', data={"world": 0, 'unique_id': unique_id})
	print(str(result.text))

def get_top_damage(unique_id: str,range_number:str):
	result = requests.post('http://localhost:8004/get_top_damage', data={"world": 0, 'unique_id': unique_id,"range_number":range_number})
	print(str(result.text))

def active_wishing_pool(unique_id: str,range_number:str):
	result = requests.post('http://localhost:8100/active_wishing_pool', data={"world": 0, 'unique_id': unique_id,"weapon_id":"weapon1"})
	print(str(result.text))


lukseun = lukseun_client.LukseunClient('aliya', '127.0.0.1', port = 8880)
world = "0"
unique_id = "4"
token = ""
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))
def purchase_energy():
	global token
	# msg = {'world' : world, 'function' : 'enter_stage', 'data' : {'token' : token, 'stage' : '1'}}
	# response = send_tcp_message(msg)
	return True
def registered_account(world:str, unique_id: str):
	print_module("[registered_account]")
	msg = {'function' : 'login_unique', 'data' : {'unique_id' : unique_id}}
	response = asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))
	myjson = response
	if myjson["status"]==0:
		print_method("[registered_account] login success")
		return myjson["data"]["token"]
	else:
		print_method("[registered_account] login failed, try login again")
		registered_account(world,unique_id)
def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")
def enter_level():
	global token
	while True:
		print_module("[enter_level]")
		my_number = random.randint(0,4)
		if my_number==0:#剧情
			print_method("[registered_account][enter_level] play normal level")
			stage = random.randint(1,8)
			msg = {'world' : world, 'function' : 'enter_stage', 'data' : {'token' : token, 'stage' : str(stage)}}
			response = send_tcp_message(msg)#进入关卡
			if response["status"]==0:
				msg = {'world' : '0', 'function' : 'pass_stage', 'data' : {'token' : token, 'stage' : str(stage), 'clear_time' : 'we dont care what this string is'}}
				response = send_tcp_message(msg)#挑战成功
			else:
				purchase_energy()
		elif my_number==1:#世界boss
			print_method("[registered_account][enter_level] play world boss")
			msg = {'world' : world, 'function' : 'enter_world_boss_stage', 'data' : {'token' : token}}
			response = send_tcp_message(msg)
			if response["status"]==0:
				msg = {'world' : world, 'function' : 'leave_world_boss_stage', 'data' : {'token' : token,"total_damage":random.randint(1,100000)}}
				response = send_tcp_message(msg)
				print_method("[registered_account][enter_level] challange boss success")
			else:
				msg = {'world' : world, 'function' : 'get_top_damage', 'data' : {'token' : token,"range_number":random.randint(1,5)}}
				response = send_tcp_message(msg)
				print_method("[registered_account][enter_level] get top damage")
		elif my_number==2:#无尽试炼
			print_method("[registered_account][enter_level] endless training")
		elif my_number==3:#活动试炼
			print_method("[registered_account][enter_level] party training")
		elif my_number==4:#退出
			print_method("[registered_account][enter_level] quit level playing")
			break
def freind_dialog():
	print_module("[freind_dialog]")
	global token
	msg = {'world' : '0', 'function' : 'get_all_friend_info', 'data' : {'token' : token}}
	response = send_tcp_message(msg)#获取所有好友信息
	# print(str(response))
	while True:
		int_random = random.randint(0,4)
		if int_random==0:#发送一个好友
			for i in range(0,len(response["data"]["remaining"]["f_name"])):
				send_msg = {'world' : '0', 'function' : 'send_friend_gift', 'data' : {'token' : token,"friend_name":str(response["data"]["remaining"]["f_name"][i])}}
				new_response = send_tcp_message(send_msg)#发送好友信息
				if new_response["status"]=="0":
					print_method("[freind_dialog] send friend gift:"+new_response["data"]["remaining"]["f_name"][i])
				else:
					print_method(f'[freind_dialog] send {response["data"]["remaining"]["f_name"][i]} gift but failed, error:{new_response["message"]}')
		elif int_random==1:#发送所有好友信息
			send_msg = {'world' : '0', 'function' : 'send_all_friend_gift', 'data' : {'token' : token}}
			new_response = send_tcp_message(send_msg)#发送好友信息s
			print_method("[freind_dialog] send all gift:"+str(new_response))
		elif int_random==2:#加好友
			friend_name = random.randint(0,100)
			send_msg = {'world' : '0', 'function' : 'request_friend', 'data' : {'token' : token,"friend_name":str(friend_name)}}
			new_response = send_tcp_message(send_msg)#发送好友信息
			print_method("[freind_dialog] requst_friend:"+str(friend_name)+" "+str(new_response))
		elif int_random==3:#删好友
			friend_name = random.randint(0,100)
			send_msg = {'world' : '0', 'function' : 'delete_friend', 'data' : {'token' : token,"friend_name":str(friend_name)}}
			new_response = send_tcp_message(send_msg)#发送好友信息
			print_method("[freind_dialog] delete_friend:"+str(friend_name)+" "+str(new_response))
		elif int_random ==4:
			print_method("[freind_dialog] quit friend dialog")
			break
def get_random_skill():
	print_module("[get_random_skill]")
	while True:
		int_n = random.randint(0,1)
		if int_n == 0: #朋友召唤
			print_method("[freind_dialog] friend gift to get skill")
			is_10 = random.choice([0,1])
			if is_10==0:
				send_msg = {'world' : '0', 'function' : 'basic_summon_skill', 'data' : {'token' : token,"cost_item":"friend_gift"}}
			else:
				send_msg = {'world' : '0', 'function' : 'basic_summon_skill_10_times', 'data' : {'token' : token,"cost_item":"friend_gift"}}
			new_response = send_tcp_message(send_msg)#发送好友信息
		elif int_n == 1:#高级召唤
			print_method("[freind_dialog] diamond gift to get skill")
			is_10 = random.choice([0,1])
			if is_10==0:
				send_msg = {'world' : '0', 'function' : 'pro_summon_skill', 'data' : {'token' : token,"cost_item":"basic_summon_scroll"}}
			else:
				send_msg = {'world' : '0', 'function' : 'pro_summon_skill_10_times', 'data' : {'token' : token,"cost_item":"basic_summon_scroll"}}
			new_response = send_tcp_message(send_msg)#发送好友信息
			if new_response["status"]!=0:
				pass#购买卷轴
				if random.choice([0,1])==0:
					continue
				else:
					break
			else:
				break
	#朋友召唤
	#高级召唤
def skill_dialog():
	print_module("[skill_dialog]")
	send_msg = {'world' : '0', 'function' : 'get_all_skill_level', 'data' : {'token' : token}}
	new_response = send_tcp_message(send_msg)#升级请求
	while True:
		skill_id = random.choice(["m1_level", "p1_level", "g1_level", "m11_level", "m12_level", "m13_level", "p11_level", "p12_level", "p13_level", "g11_level", "g12_level", "g13_level", 
				"m111_level", "m112_level", "m113_level", "m121_level", "m122_level", "m123_level", "m131_level", "m132_level", "m133_level",
				"p111_level", "p112_level", "p113_level", "p121_level", "p122_level", "p123_level", "p131_level", "p132_level", "p133_level",
				"g111_level", "g112_level", "g113_level", "g121_level", "g122_level", "g123_level", "g131_level", "g132_level", "g133_level"])
		skill_level = new_response["data"]["remaining"][skill_id]
		print("skill_level="+str(skill_level))
		if skill_level==0:
			int_n = random.randint(0,1)
			if int_n == 0:
				get_random_skill()
			else:
				break
		else:
			scroll_id = random.choice(["m1_level", "p1_level", "g1_level"])
			send_msg = {'world' : '0', 'function' : 'level_up_skill', 'data' : {'token' : token,"skill_id":skill_id,"scroll_id":scroll_id}}
			new_response = send_tcp_message(send_msg)#升级请求
			print_method("[skill_dialog] level up skill success" + str(new_response))
if __name__ == "__main__":
	token = registered_account("0",unique_id)#账号注册
	# enter_level()#关卡界面
	# freind_dialog()#朋友界面
	# skill_dialog()#技能界面
	get_random_skill()
