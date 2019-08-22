import json
import pyDes
import base64
import requests
import configparser

# DESIv = '67891234'
# DESKey = '6789123467891234'
#
# MD5_ALIYA = b'e3cb970693574ea75d091a6049f8a3ff'

CONFIG = configparser.ConfigParser()
CONFIG.read(requests.get('http://localhost:8000/get_server_config_location').json()['file'])

DESIv = CONFIG['message_handler']['DESIv']
DESKey = CONFIG['message_handler']['DESKey']

MD5_ALIYA = b'e3cb970693574ea75d091a6049f8a3ff'
TOKEN_BASE_URL = CONFIG['token_server']['address'] + ":" + CONFIG['token_server']['port']
MANAGER_ACCOUNT_BASE_URL = CONFIG['account_manager']['address'] + ":" + CONFIG['account_manager']['port']



class InvalidHeaderError(Exception):
	pass


class MessageHandler:
	def __init__(self):
		self._functions = FUNCTION_LIST
		self._k = pyDes.triple_des(DESKey, pyDes.CBC, DESIv, pad=None, padmode=pyDes.PAD_PKCS5)
		self._map = requests.get('http://localhost:8000/get_world_map').json()

	def is_valid_header(self, raw_header: bytes) -> int:
		'''
		Decodes the raw header.
		Returns the message size of the upcoming message.
		Raises InvalidHeaderError if the header is not valid.
		'''
		decoded = raw_header.decode()
		if decoded[:32] != 'e3cb970693574ea75d091a6049f8a3ff':
			raise InvalidHeaderError
		return int(decoded[32:])

	def process_message_out(self, server_response: str) -> bytes:
		'''
		Called before sending message response to client.
		Generates a header to prepend to the message.
		Serializes the dictionary into JSON format, encodes and encrypts the resulting
		string, and returns a bytes object.
		'''
		payload = base64.encodebytes(self._k.encrypt(server_response.encode()))
		return MD5_ALIYA + self._format_message_size(len(payload)) + payload

	def process_message_in(self, message: bytes) -> dict:
		'''
		Called upon receiving the message payload from client.
		Decrypts and decodes the incoming bytes message and returns a dictionary.
		'''
		decoded = self._k.decrypt(base64.decodebytes(message))
		return json.loads(decoded)

	async def resolve(self, message: dict, session) -> str:
		'''
		Resolves the message included in the request. If required, ensures that a valid token is present.
		'''
		try:
			fn = self._functions[message['function']]
			if message['function'] not in DOES_NOT_NEED_TOKEN:
				async with session.post(TOKEN_BASE_URL + '/validate', data = {'token' : message['data']['token']}) as resp:
					data = await resp.json(content_type = 'text/json')
					if data['status'] != 0:
						return json.dumps({'status': 11, 'message': 'Authorization required', 'data': {'bad_token': message['data']['token']}})
					message['data']['unique_id'] = data['data']['unique_id']
			return await fn(self, message, session)
		except KeyError:
			return json.dumps({'status': 10, 'message': 'Invalid message format', 'data': {}})
	
	def _game_manager_base_url(self, world):
		for gm in self._map[world]['gamemanagers'].values():
			return f'http://{gm["ip"]}:{gm["port"]}'

	def _format_message_size(self, size: int) -> bytes:
		'''
		0 pads the size of the message and outputs bytes.
		'''
		return str(size).zfill(5).encode()
#
	async def _login(self, message: dict, session) -> str:
		async with session.post(MANAGER_ACCOUNT_BASE_URL + '/login', data={'identifier': message['data']['identifier'], 'value': message['data']['value'], 'password': message['data']['password']}) as resp:
			return await resp.text()

	async def _login_unique(self, message: dict, session) -> str:
		async with session.post(MANAGER_ACCOUNT_BASE_URL + '/login_unique', data={'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _bind_account(self, message: dict, session) -> str:
		async with session.post(MANAGER_ACCOUNT_BASE_URL + '/bind_account', data={'unique_id': message['data']['unique_id'], 'password' : message['data']['password'], 'account': message['data']['account'], 'email': message['data']['email'], 'phone_number' : message['data']['phone_number']}) as resp:
			return await resp.text()

	async def _level_up_skill(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/level_up_skill', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'skill_id': message['data']['skill_id'], 'scroll_id': message['data']['scroll_id']}) as resp:
			return await resp.text()

	async def _get_all_skill_level(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/get_all_skill_level', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _get_all_supplies(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/get_all_supplies', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _random_gift_skill(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/random_gift_skill', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _random_gift_segment(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/random_gift_segment', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _get_skill(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/get_skill', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'skill_id': message["data"]["skill_id"]}) as resp:
			return await resp.text()

	async def _update_energy(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/try_energy', data={'unique_id': message['data']['unique_id'], 'amount': message["data"]["amount"]}) as resp:
			return await resp.text()

	async def _level_up_scroll(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/level_up_scroll', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'scroll_id': message['data']['scroll_id']}) as resp:
			return await resp.text()
	
	# region _01_Manager_Weapon.py
	async def _level_up_weapon(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/level_up_weapon', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'weapon': message['data']['weapon'], 'iron': message['data']['iron']}) as resp:
			return await resp.text()

	async def _level_up_passive(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/level_up_passive', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'weapon': message['data']['weapon'], 'passive': message['data']['passive']}) as resp:
			return await resp.text()

	async def _reset_weapon_skill_point(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/reset_weapon_skill_point', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'weapon': message['data']['weapon']}) as resp:
			return await resp.text()

	async def _level_up_weapon_star(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/level_up_weapon_star', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'weapon': message['data']['weapon']}) as resp:
			return await resp.text()

	async def _get_all_weapon(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/get_all_weapon', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _disintegrate_weapon(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/disintegrate_weapon', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'weapon': message['data']['weapon']}) as resp:
			return await resp.text()
	# endregion

	async def _enter_tower(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/enter_tower', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'stage' : message['data']['stage']}) as resp:
			return await resp.text()

	async def _pass_tower(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/pass_tower', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'stage' : message['data']['stage'], 'clear_time' : message['data']['clear_time']}) as resp:
			return await resp.text()

	async def _get_all_stage_info(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/get_all_stage_info') as resp:
			return await resp.text()

	async def _get_all_armor_info(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/get_all_armor_info', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _pass_stage(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/pass_stage', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'stage': message['data']['stage'], 'clear_time' : message['data']['clear_time']}) as resp:
			return await resp.text()

	async def _decrease_energy(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/decrease_energy', data={'unique_id': message['data']['unique_id'], 'energy': message['data']['energy']}) as resp:
			return await resp.text()

	async def _increase_energy(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/increase_energy', data={'unique_id': message['data']['unique_id'], 'energy': message['data']['energy']}) as resp:
			return await resp.text()

	# 以后会删除这个方法
	async def _add_supplies(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/add_supplies', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'supply': message['data']['supply'], 'value': message['data']['value']}) as resp:
			return await resp.text()

	async def _get_all_head(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/get_all_head', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'table' : message['data']['table']}) as resp:
			return await resp.text()

	async def _get_all_material(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/get_all_material', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _try_all_material(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/try_all_material', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'stage' : message['data']['stage']}) as resp:
			return await resp.text()

	async def _try_coin(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/try_coin', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'value' : message['data']['value']}) as resp:
			return await resp.text()

	async def _try_unlock_skill(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/try_unlock_skill', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'skill_id' : message['data']['skill_id']}) as resp:
			return await resp.text()

	async def _try_unlock_weapon(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/try_unlock_weapon', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'weapon' : message['data']['weapon']}) as resp:
			return await resp.text()

	async def _basic_summon(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/basic_summon', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'cost_item' : message['data']['cost_item']}) as resp:
			return await resp.text()
			
	async def _basic_summon_10_times(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/basic_summon_10_times', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'cost_item' : message['data']['cost_item']}) as resp:
			return await resp.text()
	async def _pro_summon_10_times(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/pro_summon_10_times', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'cost_item' : message['data']['cost_item']}) as resp:
			return await resp.text()
			
	async def _pro_summon(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/pro_summon', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'cost_item' : message['data']['cost_item']}) as resp:
			return await resp.text()

	async def _friend_summon(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/friend_summon', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'cost_item' : message['data']['cost_item']}) as resp:
			return await resp.text()
	async def _friend_summon_10_times(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/friend_summon_10_times', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'cost_item' : message['data']['cost_item']}) as resp:
			return await resp.text()
			
			
			
	async def _basic_summon_roles(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/basic_summon_roles', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'cost_item' : message['data']['cost_item']}) as resp:
			return await resp.text()
			
	async def _basic_summon_roles_10_times(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/basic_summon_roles_10_times', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'cost_item' : message['data']['cost_item']}) as resp:
			return await resp.text()
	async def _pro_summon_roles_10_times(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/pro_summon_roles_10_times', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'cost_item' : message['data']['cost_item']}) as resp:
			return await resp.text()
			
	async def _pro_summon_roles(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/pro_summon_roles', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'cost_item' : message['data']['cost_item']}) as resp:
			return await resp.text()

	async def _friend_summon_roles(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/friend_summon_roles', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'cost_item' : message['data']['cost_item']}) as resp:
			return await resp.text()
	async def _friend_summon_roles_10_times(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/friend_summon_roles_10_times', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'cost_item' : message['data']['cost_item']}) as resp:
			return await resp.text()
			
		

	
	async def _basic_summon_skill(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/basic_summon_skill', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'cost_item' : message['data']['cost_item']}) as resp:
			return await resp.text()
			
	async def _basic_summon_skill_10_times(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/basic_summon_skill_10_times', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'cost_item' : message['data']['cost_item']}) as resp:
			return await resp.text()
	async def _pro_summon_skill_10_times(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/pro_summon_skill_10_times', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'cost_item' : message['data']['cost_item']}) as resp:
			return await resp.text()
			
	async def _pro_summon_skill(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/pro_summon_skill', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'cost_item' : message['data']['cost_item']}) as resp:
			return await resp.text()

	async def _friend_summon_skill(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/friend_summon_skill', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'cost_item' : message['data']['cost_item']}) as resp:
			return await resp.text()
	async def _friend_summon_skill_10_times(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/friend_summon_skill_10_times', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'cost_item' : message['data']['cost_item']}) as resp:
			return await resp.text()
	async def _prophet_summon_10_times(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/prophet_summon_10_times', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'cost_item' : message['data']['cost_item']}) as resp:
			return await resp.text()
	async def _start_hang_up(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/start_hang_up', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'stage' : message['data']['stage']}) as resp:
			return await resp.text()

	async def _get_hang_up_reward(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/get_hang_up_reward', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _enter_stage(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/enter_stage', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'stage' : message['data']['stage']}) as resp:
			return await resp.text()

	async def _fortune_wheel_basic(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/fortune_wheel_basic', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'cost_item' : message['data']['cost_item']}) as resp:
			return await resp.text()

	async def _fortune_wheel_pro(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/fortune_wheel_pro', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'cost_item' : message['data']['cost_item']}) as resp:
			return await resp.text()

	async def _automatically_refresh_store(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/automatically_refresh_store', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _manually_refresh_store(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/manually_refresh_store', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _diamond_refresh_store(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/diamond_refresh_store', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _black_market_transaction(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/black_market_transaction', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'code': message['data']['code']}) as resp:
			return await resp.text()

	async def _show_energy(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/show_energy', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _upgrade_armor(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/upgrade_armor', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'armor_id': message['data']['armor_id'], 'level': message['data']['level']}) as resp:
			return await resp.text()

	async def _send_friend_gift(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/send_friend_gift', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'friend_name': message['data']['friend_name']}) as resp:
			return await resp.text()

	async def _redeem_nonce(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/redeem_nonce', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'nonce': message['data']['nonce']}) as resp:
			return await resp.text()

	async def _get_new_mail(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/get_new_mail', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _get_all_mail(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/get_all_mail', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _delete_mail(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/delete_mail', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'nonce': message['data']['nonce']}) as resp:
			return await resp.text()

	async def _delete_all_mail(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/delete_all_mail', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()



	
	#async def _get_all_tower_info(self, message: dict, session) -> str:
	#	async with session.post('http://localhost:8006/get_all_tower_info', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
	#		return await resp.text()
			
	async def _level_enemy_layouts_config(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/level_enemy_layouts_config', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _monster_config(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/monster_config', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _get_stage_reward_config(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/get_stage_reward_config', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _get_lottery_config_info(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/get_lottery_config_info', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _get_hang_up_info(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/get_hang_up_info', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _get_all_friend_info(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/get_all_friend_info', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()
	async def _request_friend(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/request_friend', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'friend_name': message['data']['friend_name']}) as resp:
			return await resp.text()

	async def _response_friend(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/response_friend', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'nonce': message['data']['nonce']}) as resp:
			return await resp.text()

	async def _delete_friend(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/delete_friend', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'friend_name': message['data']['friend_name']}) as resp:
			return await resp.text()

	async def _send_all_friend_gift(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/send_all_friend_gift', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _redeem_all_nonce(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/redeem_all_nonce', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'type_list': message['data']['type_list'], 'nonce_list': message['data']['nonce_list']}) as resp:
			return await resp.text()
	
	async def _get_chat_server(self, message: dict, session):
		return self._map[message['world']]['chatserver']
		
	async def _check_boss_status(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/check_boss_status', data={'world' : message['world'], 'unique_id': message['data']['unique_id']) as resp:
			return await resp.text()		
	async def _enter_world_boss_stage(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/enter_world_boss_stage', data={'world' : message['world'], 'unique_id': message['data']['unique_id']) as resp:
			return await resp.text()	
	async def _leave_world_boss_stage(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/leave_world_boss_stage', data={'world' : message['world'], 'unique_id': message['data']['unique_id'],'total_damage': message['data']['total_damage']) as resp:
			return await resp.text()	
	async def _get_top_damage(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/get_top_damage', data={'world' : message['world'], 'unique_id': message['data']['unique_id'],'range_number': message['data']['range_number']) as resp:
			return await resp.text()
			
			
	async def _leave_family(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/leave_family', data={'world' : message['world'], 'unique_id': message['data']['unique_id']) as resp:
			return await resp.text()	
	async def _create_family(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/create_family', data={'world' : message['world'], 'unique_id': message['data']['unique_id'],'fname': message['data']['fname']) as resp:
			return await resp.text()		
			
	async def _invite_user_family(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/invite_user_family', data={'world' : message['world'], 'unique_id': message['data']['unique_id'],'target': message['data']['target']) as resp:
			return await resp.text()			
	async def _remove_user_family(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/remove_user_family', data={'world' : message['world'], 'unique_id': message['data']['unique_id'],'user': message['data']['user']) as resp:
			return await resp.text()		
	async def _request_join_family(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/request_join_family', data={'world' : message['world'], 'unique_id': message['data']['unique_id'],'fname': message['data']['fname']) as resp:
			return await resp.text()				
	async def _response_family(self, message: dict, session) -> str:
		async with session.post(self._game_manager_base_url(message['world']) + '/response_family', data={'world' : message['world'], 'unique_id': message['data']['unique_id'],'nonce': message['data']['nonce']) as resp:
			return await resp.text()
			
###############################################################################



DOES_NOT_NEED_TOKEN = {'login', 'login_unique', 'get_chat_server'}

FUNCTION_LIST = {
	# utility
	'get_chat_server' : MessageHandler._get_chat_server,
	# account_manager
	'login': MessageHandler._login,
	'login_unique': MessageHandler._login_unique,
	'bind_account': MessageHandler._bind_account,

	# game_manager
	'get_all_head' : MessageHandler._get_all_head,
	'get_all_material' : MessageHandler._get_all_material,
	'get_all_supplies' : MessageHandler._get_all_supplies,
	'add_supplies' : MessageHandler._add_supplies,
	'level_up_scroll' : MessageHandler._level_up_scroll,
	'try_all_material' : MessageHandler._try_all_material,
	'try_coin' : MessageHandler._try_coin,
	'level_up_skill' : MessageHandler._level_up_skill,
	'get_all_skill_level' : MessageHandler._get_all_skill_level,
	'get_skill' : MessageHandler._get_skill,
	'try_unlock_skill' : MessageHandler._try_unlock_skill,
	'level_up_weapon' : MessageHandler._level_up_weapon,
	'level_up_passive' : MessageHandler._level_up_passive,
	'level_up_weapon_star' : MessageHandler._level_up_weapon_star,
	'reset_weapon_skill_point' : MessageHandler._reset_weapon_skill_point,
	'get_all_weapon' : MessageHandler._get_all_weapon,
	'disintegrate_weapon' : MessageHandler._disintegrate_weapon,
	'try_unlock_weapon' : MessageHandler._try_unlock_weapon,
	'pass_stage' : MessageHandler._pass_stage,
	'basic_summon' : MessageHandler._basic_summon,
	'basic_summon_10_times' : MessageHandler._basic_summon_10_times,
	'pro_summon' : MessageHandler._pro_summon,
	'pro_summon_10_times' : MessageHandler._pro_summon_10_times,
	'friend_summon' : MessageHandler._friend_summon,
	'friend_summon_10_times' : MessageHandler._friend_summon_10_times,
	'basic_summon_roles' : MessageHandler._basic_summon_roles,
	'basic_summon_roles_10_times' : MessageHandler._basic_summon_roles_10_times,
	'pro_summon_roles' : MessageHandler._pro_summon_roles,
	'pro_summon_roles_10_times' : MessageHandler._pro_summon_roles_10_times,
	'friend_summon_roles' : MessageHandler._friend_summon_roles,
	'friend_summon_roles_10_times' : MessageHandler._friend_summon_roles_10_times,
	
	
	'basic_summon_skill' : MessageHandler._basic_summon_skill,
	'basic_summon_skill_10_times' : MessageHandler._basic_summon_skill_10_times,
	'pro_summon_skill' : MessageHandler._pro_summon_skill,
	'pro_summon_skill_10_times' : MessageHandler._pro_summon_skill_10_times,
	'friend_summon_skill' : MessageHandler._friend_summon_skill,
	'friend_summon_skill_10_times' : MessageHandler._friend_summon_skill_10_times,
	'prophet_summon_10_times' : MessageHandler._prophet_summon_10_times,
	
	
	
	'start_hang_up' : MessageHandler._start_hang_up,
	'get_hang_up_reward' : MessageHandler._get_hang_up_reward,
	'enter_stage' : MessageHandler._enter_stage,
	'fortune_wheel_basic' : MessageHandler._fortune_wheel_basic,
	'fortune_wheel_pro' : MessageHandler._fortune_wheel_pro,

	'automatically_refresh_store': MessageHandler._automatically_refresh_store,
	'manually_refresh_store': MessageHandler._manually_refresh_store,
	'diamond_refresh_store': MessageHandler._diamond_refresh_store,
	'black_market_transaction': MessageHandler._black_market_transaction,
	'show_energy': MessageHandler._show_energy,
	'upgrade_armor': MessageHandler._upgrade_armor,
	'pass_tower' : MessageHandler._pass_tower,
	'enter_tower' : MessageHandler._enter_tower,
	'get_all_stage_info' : MessageHandler._get_all_stage_info,
	'get_all_armor_info' : MessageHandler._get_all_armor_info,
	
	
	'get_lottery_config_info' : MessageHandler._get_lottery_config_info,
	#'get_all_tower_info' : MessageHandler._get_all_tower_info,
	#'get_all_armor_info' : MessageHandler._get_all_armor_info,
	'level_enemy_layouts_config' : MessageHandler._level_enemy_layouts_config,
	'monster_config' : MessageHandler._monster_config,
	'get_stage_reward_config' : MessageHandler._get_stage_reward_config,
	'get_hang_up_info' : MessageHandler._get_hang_up_info,
	

	'get_all_friend_info': MessageHandler._get_all_friend_info,
	'delete_friend': MessageHandler._delete_friend,
	'request_friend': MessageHandler._request_friend,
	'response_friend': MessageHandler._response_friend,
	'send_friend_gift': MessageHandler._send_friend_gift,
	'send_all_friend_gift': MessageHandler._send_all_friend_gift,
	'redeem_nonce': MessageHandler._redeem_nonce,
	'redeem_all_nonce': MessageHandler._redeem_all_nonce,
	'get_new_mail': MessageHandler._get_new_mail,
	'get_all_mail': MessageHandler._get_all_mail,
	'delete_mail': MessageHandler._delete_mail,
	'delete_all_mail': MessageHandler._delete_all_mail,
	
	'check_boss_status' : MessageHandler._check_boss_status,
	'enter_world_boss_stage' : MessageHandler._enter_world_boss_stage,
	'leave_world_boss_stage' : MessageHandler._leave_world_boss_stage,
	'get_top_damage' : MessageHandler._get_top_damage,
	
	'check_boss_status' : MessageHandler._check_boss_status,
	'enter_world_boss_stage' : MessageHandler._enter_world_boss_stage,
	'leave_world_boss_stage' : MessageHandler._leave_world_boss_stage,
	'get_top_damage' : MessageHandler._get_top_damage,
	
	'leave_family' : MessageHandler._leave_family,
	'create_family' : MessageHandler._create_family,
	'invite_user_family' : MessageHandler._invite_user_family,
	'remove_user_family' : MessageHandler._remove_user_family,
	'request_join_family' : MessageHandler._request_join_family,
	'response_family' : MessageHandler._response_family,


}   
    