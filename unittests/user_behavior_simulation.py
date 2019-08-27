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
	msg = {'function' : 'login_unique', 'data' : {'unique_id' : unique_id}}
	response = asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))
	myjson = response
	if myjson["status"]==0:
		print("[registered_account] login success")
		return myjson["data"]["token"]
	print("[registered_account] login failed, try login again")
	registered_account(world,unique_id)
def enter_level():
	global token
	while True:
		my_number = random.randint(0,0)
		if my_number==0:#剧情
			stage = random.randint(1,8)
			msg = {'world' : world, 'function' : 'enter_stage', 'data' : {'token' : token, 'stage' : str(stage)}}
			response = send_tcp_message(msg)
			if response["status"]==0:
				msg = {'world' : '0', 'function' : 'pass_stage', 'data' : {'token' : token, 'stage' : str(stage), 'clear_time' : 'we dont care what this string is'}}
				response = send_tcp_message(msg)
				print(response)
			else:
				purchase_energy()
		if my_number==1:#世界boss
			pass
		if my_number==2:#无尽试炼
			pass
		if my_number==3:#剧情
			pass
		if my_number==4:#退出
			break

if __name__ == "__main__":
	token = registered_account("0",unique_id)
	enter_level()
