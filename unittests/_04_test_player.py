import requests
import configparser


CONFIG = configparser.ConfigParser()
CONFIG.read('../Application/GameAliya/Configuration/server/1.0/server.conf')
MANAGER_BAG_BASE_URL = 'http://localhost:' + CONFIG['bag_manager']['port']
MANAGER_WEAPON_BASE_URL = 'http://localhost:' + CONFIG['_01_Manager_Weapon']['port']
MANAGER_PLAYER_BASE_URL = 'http://localhost:' + CONFIG['_04_Manager_Game']['port']
MANAGER_LEVEL_BASE_URL = 'http://localhost:' + CONFIG['stage_manager']['port']
MANAGER_SKILL_BASE_URL = 'http://localhost:' + CONFIG['skill_manager']['port']
MANAGER_LOTTERY_BASE_URL = 'http://localhost:' + CONFIG['lottery_manager']['port']



def try_coin():
	result = requests.post(MANAGER_BAG_BASE_URL + '/try_coin', data={'unique_id': "4", "value": 255})
	print(str(result.text))


def try_iron():
	result = requests.post(MANAGER_BAG_BASE_URL + '/try_iron', data={'unique_id': "4", "value": -50})
	print(str(result.text))


def try_diamond():
	# result = requests.post(MANAGER_BAG_BASE_URL + '/try_diamond', data={'unique_id': "4", "value": -1000})
	result = requests.post(MANAGER_PLAYER_BASE_URL + '/try_diamond', data={'unique_id': "4", "value": -1000})
	print(str(result.text))


def level_up_weapon():
	result = requests.post(MANAGER_WEAPON_BASE_URL + '/level_up_weapon', data={'unique_id': "4", "weapon": "weapon1", "iron": 1000})
	# result = requests.post(MANAGER_PLAYER_BASE_URL + '/level_up_weapon', data={'unique_id': "4", "weapon": "weapon1", "iron": 1000})
	print(str(result.text))


def pass_stage():
	result = requests.post(MANAGER_LEVEL_BASE_URL + '/pass_stage', data={'unique_id': "4", "stage": 2})
	# result = requests.post(MANAGER_PLAYER_BASE_URL + '/pass_stage', data={'unique_id': "4", "stage": 1})
	print(str(result.text))


def get_skill():
	result = requests.post(MANAGER_SKILL_BASE_URL + '/get_skill', data={'unique_id': "4", "skill_id": "m1_level"})
	# result = requests.post(MANAGER_PLAYER_BASE_URL + '/get_skill', data={'unique_id': "4", "stage": 1})
	print(str(result.text))


def get_all_skill_level():
	result = requests.post(MANAGER_SKILL_BASE_URL + '/get_all_skill_level', data={'unique_id': "4"})
	# result = requests.post(MANAGER_PLAYER_BASE_URL + '/get_all_skill_level', data={'unique_id': "4"})
	print(str(result.text))


def level_up_skill():
	result = requests.post(MANAGER_SKILL_BASE_URL + '/level_up_skill', data={'unique_id': "4", "skill_id": "m1_level",  "scroll_id": "skill_scroll_10"})
	# result = requests.post(MANAGER_PLAYER_BASE_URL + '/level_up_skill', data={'unique_id': "4"})
	print(str(result.text))


def random_gift_skill():
	result = requests.post(MANAGER_LOTTERY_BASE_URL + '/random_gift_skill', data={'unique_id': "4"})
	# result = requests.post(MANAGER_PLAYER_BASE_URL + '/random_gift_skill', data={'unique_id': "4"})
	print(str(result.text))


def random_gift_weapon():
	result = requests.post(MANAGER_LOTTERY_BASE_URL + '/random_gift_weapon', data={'unique_id': "4"})
	# result = requests.post(MANAGER_PLAYER_BASE_URL + '/random_gift_skill', data={'unique_id': "4"})
	print(str(result.text))


def level_up_scroll():
	result = requests.post(MANAGER_BAG_BASE_URL + '/level_up_scroll', data={'unique_id': "4", "scroll_id": "skill_scroll_100"})
	# result = requests.post(MANAGER_PLAYER_BASE_URL + '/random_gift_skill', data={'unique_id': "4"})
	print(str(result.text))


def get_all_weapon():
	result = requests.post(MANAGER_WEAPON_BASE_URL + '/get_all_weapon', data={'unique_id': "4"})
	# result = requests.post(MANAGER_PLAYER_BASE_URL + '/random_gift_skill', data={'unique_id': "4"})
	print(str(result.text))


def level_up_passive():
	result = requests.post(MANAGER_WEAPON_BASE_URL + '/level_up_passive', data={'unique_id': "4", "weapon": "weapon1", "passive": "passive_skill_1_level"})
	# result = requests.post(MANAGER_PLAYER_BASE_URL + '/random_gift_skill', data={'unique_id': "4"})
	print(str(result.text))


def reset_weapon_skill_point():
	result = requests.post(MANAGER_WEAPON_BASE_URL + '/reset_weapon_skill_point', data={'unique_id': "4", "weapon": "weapon1"})
	# result = requests.post(MANAGER_PLAYER_BASE_URL + '/random_gift_skill', data={'unique_id': "4"})
	print(str(result.text))


def level_up_weapon_star():
	result = requests.post(MANAGER_WEAPON_BASE_URL + '/level_up_weapon_star', data={'unique_id': "4", "weapon": "weapon1"})
	# result = requests.post(MANAGER_PLAYER_BASE_URL + '/random_gift_skill', data={'unique_id': "4"})
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
	level_up_weapon_star()