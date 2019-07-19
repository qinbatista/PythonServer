import requests
import configparser


MANAGER_CONFIGURATION_BASE_URL = 'http://localhost:8002'


def _get_client_level_enemy_layouts_config():
	result = requests.post(MANAGER_CONFIGURATION_BASE_URL + '/_get_client_level_enemy_layouts_config', data={})
	print(str(result.text))

def _get_client_monster_config():
	result = requests.post(MANAGER_CONFIGURATION_BASE_URL + '/_get_client_monster_config', data={})
	print(str(result.text))

def _get_client_stage_reward_config():
	result = requests.post(MANAGER_CONFIGURATION_BASE_URL + '/_get_client_stage_reward_config', data={})
	print(str(result.text))

def _get_server_lottery_conf():
	result = requests.post(MANAGER_CONFIGURATION_BASE_URL + '/_get_server_lottery_conf', data={})
	print(str(result.text))

def _get_server_server_conf():
	result = requests.post(MANAGER_CONFIGURATION_BASE_URL + '/_get_server_server_conf', data={})
	print(str(result.text))

def _get_server_mysql_data_config():
	result = requests.post(MANAGER_CONFIGURATION_BASE_URL + '/_get_server_mysql_data_config', data={})
	print(str(result.text))


if __name__ == "__main__":
	# _get_client_level_enemy_layouts_config()
	# _get_client_monster_config()
	# _get_client_stage_reward_config()
	# _get_server_lottery_conf()
	# _get_server_server_conf()
	_get_server_mysql_data_config()