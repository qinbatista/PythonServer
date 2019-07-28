import requests
import configparser


CONFIG = configparser.ConfigParser()
CONFIG.read('../Application/GameAliya/Configuration/server/1.0/server.conf', encoding="utf-8")
# GAME_MANAGER_BASE_URL = 'http://localhost:' + CONFIG['game_manager']['port']
GAME_MANAGER_BASE_URL = 'http://localhost:8004'



def try_coin():
	result = requests.post(GAME_MANAGER_BASE_URL + '/try_coin', data={'unique_id': "4", "value": 255})
	print(str(result.text))


def try_iron():
	result = requests.post(GAME_MANAGER_BASE_URL + '/try_iron', data={'unique_id': "4", "value": -50})
	print(str(result.text))


def try_diamond():
	result = requests.post(GAME_MANAGER_BASE_URL + '/try_diamond', data={'unique_id': "4", "value": -1000})
	print(str(result.text))


def level_up_weapon():
	result = requests.post(GAME_MANAGER_BASE_URL + '/level_up_weapon', data={'unique_id': "4", "weapon": "weapon1", "iron": 1000})
	print(str(result.text))


def pass_stage():
	result = requests.post(GAME_MANAGER_BASE_URL + '/pass_stage', data={'world':0, 'unique_id': "4", "stage": 2, "customs_clearance_time": "2019-07-25 18:34:53"})
	print(str(result.text))


def get_skill():
	result = requests.post(GAME_MANAGER_BASE_URL + '/get_skill', data={'unique_id': "4", "skill_id": "m1_level"})
	print(str(result.text))


def get_all_skill_level():
	result = requests.post(GAME_MANAGER_BASE_URL + '/get_all_skill_level', data={'unique_id': "4"})
	print(str(result.text))


def level_up_skill():
	result = requests.post(GAME_MANAGER_BASE_URL + '/level_up_skill', data={'unique_id': "4", "skill_id": "m1_level",  "scroll_id": "skill_scroll_10"})
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
	result = requests.post(GAME_MANAGER_BASE_URL + '/get_all_weapon', data={'unique_id': "4"})
	print(str(result.text))


def level_up_passive():
	result = requests.post(GAME_MANAGER_BASE_URL + '/level_up_passive', data={'unique_id': "4", "weapon": "weapon1", "passive": "passive_skill_1_level"})
	print(str(result.text))


def reset_weapon_skill_point():
	result = requests.post(GAME_MANAGER_BASE_URL + '/reset_weapon_skill_point', data={'unique_id': "4", "weapon": "weapon1"})
	print(str(result.text))


def level_up_weapon_star():
	result = requests.post(GAME_MANAGER_BASE_URL + '/level_up_weapon_star', data={'unique_id': "4", "weapon": "weapon1"})
	print(str(result.text))


def try_all_material():
	result = requests.post(GAME_MANAGER_BASE_URL + '/try_all_material', data={'unique_id': "4", "stage": "5"})
	print(str(result.text))


def try_energy():
	result = requests.post(GAME_MANAGER_BASE_URL + '/try_energy', data={'unique_id': "4", "amount": "2"})
	print(str(result.text))


def start_hang_up():
	result = requests.post(GAME_MANAGER_BASE_URL + '/start_hang_up', data={"world": 0, 'unique_id': "4", "stage": "1"})
	print(str(result.text))


def get_hang_up_reward():
	result = requests.post(GAME_MANAGER_BASE_URL + '/get_hang_up_reward', data={"world": 0, 'unique_id': "4"})
	print(str(result.text))


def enter_stage():
	result = requests.post(GAME_MANAGER_BASE_URL + '/enter_stage', data={"world": 0, 'unique_id': "4", 'stage': 1})
	print(str(result.text))


def disintegrate_weapon():
	result = requests.post(GAME_MANAGER_BASE_URL + '/disintegrate_weapon', data={"world": 0, 'unique_id': "4", 'weapon': 'weapon1'})
	print(str(result.text))


def automatically_refresh_store():
	result = requests.post(GAME_MANAGER_BASE_URL + '/automatically_refresh_store', data={"world": 0, 'unique_id': "4"})
	print(str(result.text))


if __name__ == "__main__":
	# try_remove_coin()
	# try_remove_iron()
	# try_remove_diamond()
	# level_up_weapon()
	# pass_stage()
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
	# enter_stage()
	# disintegrate_weapon()
	automatically_refresh_store()