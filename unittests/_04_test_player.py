import requests
import configparser


CONFIG = configparser.ConfigParser()
CONFIG.read('../Application/GameAliya/Configuration/server/1.0/server.conf')
MANAGER_BAG_BASE_URL = 'http://localhost:' + CONFIG['_01_Manager_Weapon']['port']
MANAGER_PLAYER_BASE_URL = 'http://localhost:' + CONFIG['bag_manager']['port']
MANAGER_LEVEL_BASE_URL = 'http://localhost:' + CONFIG['stage_manager']['port']


def test_try_remove_coin():
	result = requests.post(MANAGER_PLAYER_BASE_URL + '/try_remove_coin', data={'unique_id': "4", "value": 255})
	print(str(result.text))
	
	
def test_try_remove_iron():
	result = requests.post(MANAGER_PLAYER_BASE_URL + '/try_remove_iron', data={'unique_id': "4", "value": -50})
	print(str(result.text))
	
	
def test_try_remove_diamond():
	result = requests.post(MANAGER_PLAYER_BASE_URL + '/try_remove_diamond', data={'unique_id': "4", "value": -1000})
	print(str(result.text))


def test_level_up_weapon():
	result = requests.post(MANAGER_BAG_BASE_URL + '/level_up_weapon', data={'unique_id': "4", "weapon": "weapon1", "iron": 1000})
	print(str(result.text))


def test_pass_stagel():
	result = requests.post(MANAGER_LEVEL_BASE_URL + '/pass_stage', data={'unique_id': "4", "stage": 1})
	print(str(result.text))


if __name__ == "__main__":
	# test_try_remove_coin()
	# test_try_remove_iron()
	# test_try_remove_diamond()
	# test_level_up_weapon()
	test_pass_stagel()