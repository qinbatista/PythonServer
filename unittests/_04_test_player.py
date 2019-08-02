import json

import requests
import configparser


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
	result = requests.post(GAME_MANAGER_BASE_URL + '/enter_stage', data={"world": 0, 'unique_id': "4", 'stage': stage})
	print(str(result.text))


def enter_tower(stage: int):
	result = requests.post(GAME_MANAGER_BASE_URL + '/enter_tower', data={"world": 0, 'unique_id': "4", 'stage': stage})
	print(str(result.text))


def disintegrate_weapon():
	result = requests.post(GAME_MANAGER_BASE_URL + '/disintegrate_weapon', data={"world": 0, 'unique_id': "4", 'weapon': 'weapon1'})
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


def upgrade_armor(armor_id: int):
	result = requests.post('http://localhost:8007/upgrade_armor', data={"world": 0, 'unique_id': "4", "armor_kind": "armor1", "armor_id": armor_id})
	print(str(result.text))


def random_gift_segment():
	result = requests.post('http://localhost:8007/random_gift_segment', data={"world": 0, 'unique_id': "4"})
	print(str(result.text))


def send_friend_gift():
	result = requests.post('http://localhost:8004/send_friend_gift', data={"world": 0, 'unique_id': "4", "friend_id": 5})
	print(str(result.text))


def get_new_mail():
	result = requests.post('http://localhost:8004/get_new_mail', data={"world": 0, 'unique_id': "5"})
	print(str(result.text))
	return result.json()['data']['mail'][0]['data']['nonce']


def redeem_nonce(nonce: str):
	result = requests.post('http://localhost:8004/redeem_nonce', data={"world": 0, 'unique_id': "5", "friend_id": 5, "type": "gift", "nonce": nonce})
	print(str(result.text))

def test():
	s22k = "999"
	s21k = "939"
	print(eval("s2%sk"%2))

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

if __name__ == "__main__":
	# try_coin()
	# try_iron()
	# try_diamond()
	# level_up_weapon()
	# pass_stage(stage=6)
	# pass_tower(stage=3)
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
	# enter_tower(stage=3)
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
	send_friend_gift()
	nonce = get_new_mail()
	redeem_nonce(nonce=nonce)