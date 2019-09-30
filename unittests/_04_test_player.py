import json
import time
import os
import requests
import configparser
import asyncio
try:
	from unittests.user_behavior_simulation import tool_lukseun_client
except:
	from user_behavior_simulation import tool_lukseun_client

import random
"""
print(str(time.time()))
print(str(time.time() % 1 * 1e6))
print(str(os.getpid()))
"""

CONFIG = configparser.ConfigParser()
CONFIG.read('../Application/GameAliya/Configuration/server/1.0/server.conf', encoding="utf-8")
# GAME_MANAGER_BASE_URL = 'http://localhost:' + CONFIG['game_manager']['port']
GAME_MANAGER_BASE_URL = 'http://localhost:8004'
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
	result = requests.post('http://localhost:8004/enter_stage', data={"world": 0, 'unique_id': "4", 'stage': 1})
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
	result = requests.post('http://localhost:8100/get_new_mail', data={"world": 0, 'unique_id': unique_id})
	print(str(result.text))
	return result.json()['data']['mail'][0]['data']['nonce']


def get_all_mail(unique_id: str):
	result = requests.post('http://localhost:8004/get_all_mail', data={"world": 0, 'unique_id': unique_id})
	print(str(result.text))


def redeem_nonce(unique_id: str, nonce: str):
	result = requests.post('http://localhost:8004/redeem_nonce', data={"world": 0, 'unique_id': unique_id, "nonce": nonce})
	print(str(result.text))


def request_friend(unique_id: str, friend_name: str):
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
	
def test():
	# s22k = "999"
	# s21k = "939"
	# print(eval("s2%sk"%2))
	for i in range(1, 5):
		print(f'"{11+i}": {250+30*i},')

def all_function(unique_id: str):
	result = requests.post('http://localhost:8004/get_all_task', data={"world": 0, "unique_id": "3"})
	print(str(result.text))
	# result = requests.post('http://localhost:8004/login_task', data={"world": 0, "unique_id": "3"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/family_change_name', data={"world": 0, "unique_id": "3", "family_name": "bs"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/dismissal_family_officer', data={"world": 0, "unique_id": "3", "target": "e"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/family_officer', data={"world": 0, "unique_id": "3", "target": "f", "position": 0})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/purchase_item', data={"world": 0, "unique_id": "1", "item_id": "diamond_pack_5"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/update_login_in_time', data={"world": 0, "unique_id": "1"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/send_merchandise', data={"world": 0, "unique_id": "1", "merchandise": "coin", "quantities": 20})
	# print(str(result.text))
	# nonce = get_new_mail(unique_id="1")
	# redeem_nonce(unique_id="1", nonce=nonce)

	# result = requests.post('http://localhost:8100/get_all_friend_info', data={"world": 0, "unique_id": "4"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/get_player_info')
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/cancel_disbanded_family', data={"world": 0, "unique_id": "3"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/disbanded_family', data={"world": 0, "unique_id": "3"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/family_sign_in', data={"world": 0, "unique_id": "4"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/get_all_family_info', data={"world": 0, "unique_id": "4"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/get_stage_info', data={"world": 0, "unique_id": "8"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/get_monster_info', data={"world": 0, "unique_id": "5"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/get_role_config', data={"world": 0, "unique_id": "5"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/get_all_roles', data={"world": 0, "unique_id": "5"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/get_skill_level_up_config', data={"world": 0, "unique_id": "9"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/get_factory_info', data={"world": 0, "unique_id": "9"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/create_player', data={"world": 0, "unique_id": "2", "game_name": "b"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/choice_world', data={"world": 0, "unique_id": "4", "target_world": 1})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/get_account_world_info', data={"unique_id": "4"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/equipment_manufacturing_armor', data={"world": 0, "unique_id": "4", "armor_kind": "armor3"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/level_up_role_star', data={"world": 0, "unique_id": "4", "role": "role1"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/level_up_role', data={"world": 0, "unique_id": "4", "role": "role1", "experience_potion": 60})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/purchase_scroll_mall', data={"world": 0, "unique_id": unique_id, "scroll_type": "pro_summon_scroll", "quantity": 2})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/request_friend', data={"world": 0, "unique_id": unique_id, "friend_name": "a"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/leave_family', data={"world": 0, "unique_id": "1"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/create_family', data={"world": 0, "unique_id": "5", "fname": "dad"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/invite_user_family', data={"world": 0, "unique_id": unique_id, "target": "b"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/respond_family', data={"world": 0, "unique_id": "2", "nonce": "76423808527358951453001346758379398626552379051138955107055357315188545186541"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/remove_user_family', data={"world": 0, "unique_id": "1", "user": "b"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/request_join_family', data={"world": 0, "unique_id": "2", "fname": "dadaed"})
	# print(str(result.text))

	# result = requests.post('http://localhost:8100/acceleration_technology', data={"world": 0, 'unique_id': unique_id})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/upgrade_wishing_pool', data={"world": 0, 'unique_id': unique_id})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/upgrade_crystal_factory', data={"world": 0, 'unique_id': unique_id})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/upgrade_mine_factory', data={"world": 0, 'unique_id': unique_id, 'workers_quantity': 10})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/upgrade_food_factory', data={"world": 0, 'unique_id': unique_id, 'workers_quantity': 10})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/buy_workers', data={"world": 0, 'unique_id': unique_id, 'workers_quantity': 10})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/distribution_workers', data={"world": 0, 'unique_id': unique_id, 'workers_quantity': -2, 'factory_kind': "food"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/distribution_workers', data={"world": 0, 'unique_id': "4", 'workers_quantity': 1, 'factory_kind': "mine"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/distribution_workers', data={"world": 0, 'unique_id': unique_id, 'workers_quantity': 1, 'factory_kind': "crystal"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8100/distribution_workers', data={"world": 0, 'unique_id': "111", 'workers_quantity': 2, 'factory_kind': "equipment"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/refresh_all_storage', data={"world": 0, 'unique_id': unique_id})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/refresh_food_storage', data={"world": 0, 'unique_id': unique_id})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/refresh_mine_storage', data={"world": 0, 'unique_id': unique_id})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/refresh_crystal_storage', data={"world": 0, 'unique_id': unique_id})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/refresh_equipment_storage', data={"world": 0, 'unique_id': unique_id})
	# print(str(result.text))

	# result = requests.post('http://localhost:8004/basic_summon', data={"world": 0, 'unique_id': unique_id, "cost_item": "diamond", "summon_kind": "weapons"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/friend_summon', data={"world": 0, 'unique_id': unique_id, "cost_item": "diamond", "summon_kind": "weapons"})
	# print(str(result.text))
	# # result = requests.post('http://localhost:8004/friend_summon', data={"world": 0, 'unique_id': unique_id, "cost_item": "diamond", "summon_kind": "roles"})
	# # result = requests.post('http://localhost:8004/friend_summon', data={"world": 0, 'unique_id': unique_id, "cost_item": "diamond", "summon_kind": "skills"})
	# # result = requests.post('http://localhost:8004/fortune_wheel_basic', data={"world": 0, 'unique_id': unique_id, "cost_item": "diamond"})
	# # result = requests.post('http://localhost:8004/fortune_wheel_pro', data={"world": 0, 'unique_id': unique_id, "cost_item": "diamond"})
	# result = requests.post('http://localhost:8004/basic_summon_10_times', data={"world": 0, 'unique_id': unique_id, "cost_item": "diamond"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/pro_summon_10_times', data={"world": 0, 'unique_id': unique_id, "cost_item": "diamond"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/friend_summon_10_times', data={"world": 0, 'unique_id': unique_id, "cost_item": "diamond"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/prophet_summon_10_times', data={"world": 0, 'unique_id': unique_id, "cost_item": "diamond"})
	# print(str(result.text))
	#
	#
	# result = requests.post('http://localhost:8004/basic_summon_skill_10_times', data={"world": 0, 'unique_id': unique_id, "cost_item": "diamond"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/pro_summon_skill_10_times', data={"world": 0, 'unique_id': unique_id, "cost_item": "diamond"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/friend_summon_skill_10_times', data={"world": 0, 'unique_id': unique_id, "cost_item": "diamond"})
	# print(str(result.text))
	#
	# result = requests.post('http://localhost:8004/basic_summon_roles_10_times', data={"world": 0, 'unique_id': unique_id, "cost_item": "diamond"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/pro_summon_roles_10_times', data={"world": 0, 'unique_id': unique_id, "cost_item": "diamond"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/friend_summon_roles_10_times', data={"world": 0, 'unique_id': unique_id, "cost_item": "diamond"})
	# print(str(result.text))

	# result = requests.post('http://localhost:8004/get_all_mail', data={"world": 0, 'unique_id': unique_id, "cost_item": "diamond"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/delete_all_mail', data={"world": 0, 'unique_id': unique_id})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/get_all_mail', data={"world": 0, 'unique_id': unique_id, "cost_item": "diamond"})
	# print(str(result.text))
	# result = requests.post('http://localhost:8004/delete_friend', data={"world": 0, 'unique_id': unique_id, "friend_name": "d"})
	# print(str(result.text))

"""
json_data = {
	"world": world,
	"uid_to": unique_id,
	"kwargs":
		{
			"from": "server",
			"subject": "You have a gift!",
			"body": "Your gift is waiting",
			"type": "gift",
			"items": "friend_gift",
			"quantities": "1"
		}
}
result = requests.post('http://localhost:8020/send_mail', json=json_data)
print(str(result.text))
"""


lukseun = tool_lukseun_client.LukseunClient('aliya', port = 8880)

def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))

def new_server_test(world):
	# response = send_tcp_message({'function' : 'login_unique', 'data' : {'unique_id' : '4'}})
	# print(response)
	# token = response['data']['token']
	# response = send_tcp_message({'world' : 0, 'function' : 'invite_user_family', 'data' : {'token': token, 'target': 'aasskkk'}})
	# print(response)

	# response = send_tcp_message({'world' : 0, 'function' : 'family_gift_package', 'data' : {'token': token}})
	# print(response)
	# response = send_tcp_message({'world' : 0, 'function' : 'family_market_purchase', 'data' : {'token': token, 'merchandise': 'skill_scroll_10'}})
	# print(response)

	# response = send_tcp_message({'world' : 0, 'function' : 'send_merchandise', 'data' : {'token': token, 'merchandise': 'coin', 'quantities': '20'}})
	# print(response)

	response = send_tcp_message({'function' : 'login_unique', 'data' : {'unique_id' : 'aass'}})
	token = response['data']['token']
	# response = send_tcp_message({'world' : world, 'function' : 'get_all_task', 'data' : {'token': token}})
	# print(response)
	# response = send_tcp_message({'world' : world, 'function' : 'get_task_pack_diamond', 'data' : {'token': token}})
	# print(response)

	# # 测试level_up_role_task
	# response = send_tcp_message({'world' : world, 'function' : 'upgrade_role_level', 'data' : {'token': token, 'role': 'role1', 'experience_potion': 100}})
	# print(response)
	#
	# # 测试level_up_weapon_task
	# response = send_tcp_message({'world' : world, 'function' : 'level_up_weapon', 'data' : {'token': token, 'weapon': 'weapon1', 'iron': 100}})
	# print(response)
	#
	# # 测试pass_stage_task
	# response = send_tcp_message({'world' : world, 'function' : 'pass_stage', 'data' : {'token': token, 'stage': 1, 'clear_time': ''}})
	# print(response)
	#
	# # 测试pass_tower_task
	# response = send_tcp_message({'world' : world, 'function' : 'pass_tower', 'data' : {'token': token, 'stage': 1, 'clear_time': ''}})
	# print(response)
	#
	# # 测试leave_world_boss_stage_task
	# response = send_tcp_message({'world' : world, 'function' : 'leave_world_boss_stage', 'data' : {'token': token, 'total_damage': 1}})
	# print(response)
	#
	# # 测试basic_summon_task
	# response = send_tcp_message({'world' : world, 'function' : 'basic_summon', 'data' : {'token': token, 'cost_item': 'diamond', 'summon_kind': 'weapon'}})
	# print(response)
	#
	# # 测试pro_summon_task
	# response = send_tcp_message({'world' : world, 'function' : 'pro_summon', 'data' : {'token': token, 'cost_item': 'diamond', 'summon_kind': 'weapon'}})
	# print(response)
	#
	# # 测试refresh_all_storage_task
	# # response = send_tcp_message({'world' : world, 'function' : 'refresh_all_storage', 'data' : {'token': token}})
	# # print(response)
	#
	# # 测试send_friend_gift_task
	# response = send_tcp_message({'world' : world, 'function' : 'send_friend_gift', 'data' : {'token': token, 'friend_name': '0000005'}})
	# print(response)
	#
	# # 测试check_in_family_task
	# response = send_tcp_message({'world' : world, 'function' : 'family_sign_in', 'data' : {'token': token}})
	# print(response)
	#
	# # 测试get_all_task
	# response = send_tcp_message({'world' : world, 'function' : 'get_all_task', 'data' : {'token': token}})
	# print(response)
	#
	# # 测试 check_in
	# response = send_tcp_message({'world' : world, 'function' : 'check_in', 'data' : {'token': token}})
	# print(response)
	#
	# # 测试 supplement_check_in
	response = send_tcp_message({'world' : world, 'function' : 'supplement_check_in', 'data' : {'token': token}})
	print(response)
	#
	# # 测试 get_all_check_in_table
	# response = send_tcp_message({'world' : world, 'function' : 'get_all_check_in_table', 'data' : {'token': token}})
	# print(response)

	# 测试get_daily_task_reward
	# response = send_tcp_message({'world' : world, 'function' : 'get_daily_task_reward', 'data' : {'token': token, 'task_id': 'level_up_role'}})
	# print(response)
	# response = send_tcp_message({'world' : world, 'function' : 'get_daily_task_reward', 'data' : {'token': token, 'task_id': 'level_up_weapon'}})
	# print(response)
	# response = send_tcp_message({'world' : world, 'function' : 'get_daily_task_reward', 'data' : {'token': token, 'task_id': 'pass_stage'}})
	# print(response)
	# response = send_tcp_message({'world' : world, 'function' : 'get_daily_task_reward', 'data' : {'token': token, 'task_id': 'pass_tower'}})
	# print(response)
	# response = send_tcp_message({'world' : world, 'function' : 'get_daily_task_reward', 'data' : {'token': token, 'task_id': 'pass_world_boss'}})
	# print(response)
	# response = send_tcp_message({'world' : world, 'function' : 'get_daily_task_reward', 'data' : {'token': token, 'task_id': 'basic_summon'}})
	# print(response)
	# response = send_tcp_message({'world' : world, 'function' : 'get_daily_task_reward', 'data' : {'token': token, 'task_id': 'pro_summon'}})
	# print(response)
	# response = send_tcp_message({'world' : world, 'function' : 'get_daily_task_reward', 'data' : {'token': token, 'task_id': 'send_friend_gift'}})
	# print(response)
	# response = send_tcp_message({'world' : world, 'function' : 'get_daily_task_reward', 'data' : {'token': token, 'task_id': 'check_in_family'}})
	# print(response)

	# response = send_tcp_message({'world' : world, 'function' : 'get_new_mail', 'data' : {'token': token}})
	# print(response)
	# response = send_tcp_message({'world' : world, 'function' : 'response_family', 'data' : {'token': token, 'nonce': '78337956676184997857706980485225384889478708200314904499946514947315907719455'}})
	# print(response)


	# nonce = '109859617373153377003944302714374895868816002944800435692483366741142151128392'
	# response = send_tcp_message({'world' : 0, 'function' : 'respond_family', 'data' : {'token': token, 'nonce': nonce}})
	# print(response)

	# response = send_tcp_message({'world' : 0, 'function' : 'redeem_nonce', 'data' : {'token': token, 'nonce': nonce}})
	# print(response)
	# input('继续... ...')

if __name__ == "__main__":
	# result = requests.post('http://localhost:8100/get_stage_info', data={})
	# print(str(result.text))
	# try_coin()
	# try_iron()
	# try_diamond()
	# level_up_weapon()
	# pass_stage(stage=2)
	# pass_tower(stage=1)
	# get_skill()
	# get_all_skill_level()
	# level_up_skill()
	# random_gift_skill()
	# random_gift_weapon()
	# level_up_scroll()
	# get_all_weapon()
	# level_up_passive()
	# reset_weapon_skill_point()
	# level_up_weapon_star()
	# try_all_material()
	# try_energy()
	# start_hang_up()
	# get_hang_up_reward()
	# enter_stage(stage=1)
	# enter_tower(stage=1)
	# disintegrate_weapon()
	# automatically_refresh_store()
	# manually_refresh_store()
	# diamond_refresh_store()
	# black_market_transaction(1)
	# show_energy()
	# get_all_supplies()
	# basic_summon()
	# get_hang_up_info()
	# upgrade_armor(1)
	# random_gift_segment()
	# start ########################################################
	# get_all_mail(unique_id="1")
	# send_friend_gift(unique_id="4", friend_name="a")
	# nonce = get_new_mail(unique_id="1")
	# redeem_nonce(unique_id="1", nonce=nonce)
	# get_all_mail(unique_id="1")

	# request_friend(unique_id="5", friend_name="a")
	# nonce = get_new_mail(unique_id="1")
	# response_friend(unique_id="1", nonce=nonce)
	# response_friend(unique_id="1", nonce="32963693688928993319733151846953915999978396660497710378095972836181446004813")

	# request_friend(unique_id="4", friend_name="g")
	# request_friend(unique_id="2", friend_name="g")
	# request_friend(unique_id="3", friend_name="g")

	# send_friend_gift(unique_id="1", friend_name="g")
	# send_friend_gift(unique_id="2", friend_name="g")
	# send_friend_gift(unique_id="3", friend_name="g")
	# send_all_friend_gift(unique_id="1")
	# get_new_mail(unique_id="7")
	# get_all_mail(unique_id="7")
	# enumerate
	# test()
	# type_list, nonce_list=get_new_mail_nonce_list(unique_id="7")
	# redeem_all_nonce(unique_id="7", type_list=type_list, nonce_list=nonce_list)
	# get_all_mail(unique_id="7")
	# end   ########################################################
	# enter_stage(stage=1)
	# enter_tower(stage=1)
	# all_function(unique_id="4")

	# check_boss_status(unique_id="4")
	# check_boss_status(unique_id="4")
	# enter_world_boss_stage(unique_id="4")
	# check_boss_status('4')
	# enter_world_boss_stage("4")
	# leave_world_boss_stage('4','10000')
	# get_top_damage(4,4)
	# active_wishing_pool(4,"weapon1")

	new_server_test(0)