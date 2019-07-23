import json
import pyDes
import base64
import configparser
import os

# DESIv = '67891234'
# DESKey = '6789123467891234'
#
# MD5_ALIYA = b'e3cb970693574ea75d091a6049f8a3ff'
def PythonLocation():
    return os.path.dirname(os.path.realpath(__file__))

CONFIG = configparser.ConfigParser()
CONFIG.read(PythonLocation() + '/Configuration/server/1.0/server.conf')
DESIv = CONFIG['_00_Message_Handler']['DESIv']
DESKey = CONFIG['_00_Message_Handler']['DESKey']
MD5_ALIYA = b'e3cb970693574ea75d091a6049f8a3ff'
TOKEN_BASE_URL = CONFIG['_00_Token_Server']['address'] + ":" + CONFIG['_00_Token_Server']['port']
MANAGER_WEAPON_BASE_URL = CONFIG['_01_Manager_Weapon']['address'] + ":" + CONFIG['_01_Manager_Weapon']['port']
MANAGER_LEVEL_BASE_URL = CONFIG['_03_Manager_Level']['address'] + ":" + CONFIG['_03_Manager_Level']['port']
MANAGER_GAME_BASE_URL = CONFIG['_04_Manager_Game']['address'] + ":" + CONFIG['_04_Manager_Game']['port']
MANAGER_ACCOUNT_BASE_URL = CONFIG['_05_Manager_Account']['address'] + ":" + CONFIG['_05_Manager_Account']['port']


class InvalidHeaderError(Exception):
	pass


class MessageHandler:
	def __init__(self):
		self._functions = FUNCTION_LIST
		self._k = pyDes.triple_des(DESKey, pyDes.CBC, DESIv, pad=None, padmode=pyDes.PAD_PKCS5)

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

	def _format_message_size(self, size: int) -> bytes:
		'''
		0 pads the size of the message and outputs bytes.
		'''
		return str(size).zfill(4).encode()
#
	async def _login(self, message: dict, session) -> str:
		async with session.post(MANAGER_ACCOUNT_BASE_URL + '/login', data={'identifier': message['data']['identifier'], 'value': message['data']['value'], 'password': message['data']['password']}) as resp:
			return await resp.text()

	async def _login_unique(self, message: dict, session) -> str:
		async with session.post(MANAGER_ACCOUNT_BASE_URL + '/login_unique', data={'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _bind_account(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/bind_account', data={'unique_id': message['data']['unique_id'], 'account': message["data"]["account"], 'password': message['data']['password']}) as resp:
			return await resp.text()

	async def _level_up_skill(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/level_up_skill', data={'unique_id': message['data']['unique_id'], 'skill_id': message['data']['skill_id'], 'scroll_id': message['data']['scroll_id']}) as resp:
			return await resp.text()

	async def _get_all_skill_level(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/get_all_skill_level', data={'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _get_all_supplies(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/get_all_supplies', data={'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _random_gift_skill(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/random_gift_skill', data={'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _random_gift_segment(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/random_gift_segment', data={'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _get_skill(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/get_skill', data={'unique_id': message['data']['unique_id'], 'skill_id': message["data"]["skill_id"]}) as resp:
			return await resp.text()

	async def _update_energy(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/try_energy', data={'unique_id': message['data']['unique_id'], 'amount': message["data"]["amount"]}) as resp:
			return await resp.text()

	async def _level_up_scroll(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/level_up_scroll', data={'unique_id': message['data']['unique_id'], 'scroll_id': message['data']['scroll_id']}) as resp:
			return await resp.text()
	
	# region _01_Manager_Weapon.py
	async def _level_up_weapon(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/level_up_weapon', data={'unique_id': message['data']['unique_id'], 'weapon': message['data']['weapon'], 'iron': message['data']['iron']}) as resp:
			return await resp.text()

	async def _level_up_passive(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/level_up_passive', data={'unique_id': message['data']['unique_id'], 'weapon': message['data']['weapon'], 'passive': message['data']['passive']}) as resp:
			return await resp.text()

	async def _reset_weapon_skill_point(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/reset_weapon_skill_point', data={'unique_id': message['data']['unique_id'], 'weapon': message['data']['weapon']}) as resp:
			return await resp.text()

	async def _level_up_weapon_star(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/level_up_weapon_star', data={'unique_id': message['data']['unique_id'], 'weapon': message['data']['weapon']}) as resp:
			return await resp.text()

	async def _get_all_weapon(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/get_all_weapon', data={'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()
	# endregion
	
	async def _pass_stage(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/pass_stage', data={'unique_id': message['data']['unique_id'], 'stage': message['data']['stage']}) as resp:
			return await resp.text()

	async def _decrease_energy(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/decrease_energy', data={'unique_id': message['data']['unique_id'], 'energy': message['data']['energy']}) as resp:
			return await resp.text()

	async def _increase_energy(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/increase_energy', data={'unique_id': message['data']['unique_id'], 'energy': message['data']['energy']}) as resp:
			return await resp.text()

	# 以后会删除这个方法
	async def _add_supplies(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/add_supplies', data={'unique_id': message['data']['unique_id'], 'key': message['data']['key'], 'value': message['data']['value']}) as resp:
			return await resp.text()


DOES_NOT_NEED_TOKEN = {'login', 'login_unique'}

FUNCTION_LIST = {
	#Manager_Weapon
	'get_all_weapon': MessageHandler._get_all_weapon,
	'level_up_passive': MessageHandler._level_up_passive,
	'reset_weapon_skill_point': MessageHandler._reset_weapon_skill_point,
	'level_up_weapon_star': MessageHandler._level_up_weapon_star,
	'level_up_weapon': MessageHandler._level_up_weapon,

	#Manager_weapon
	# 'get_level_setting': MessageHandler._get_level_setting,

	#Manager_Level

	#Manager_skill

	#Manager_PlayerState(player_state_module.py,bag_module.py,lottery_module,skill_module)
	# 'decrease_energy': MessageHandler._decrease_energy,
	# 'increase_energy': MessageHandler._increase_energy,

	'random_gift_skill': MessageHandler._random_gift_skill,
	'random_gift_segment': MessageHandler._random_gift_segment,
	'level_up_skill': MessageHandler._level_up_skill,
	'level_up_scroll': MessageHandler._level_up_scroll,
	'pass_stage': MessageHandler._pass_stage,

	'get_all_skill_level': MessageHandler._get_all_skill_level,
	'get_skill': MessageHandler._get_skill,
	'update_energy': MessageHandler._update_energy,
	'get_all_supplies': MessageHandler._get_all_supplies,

	'add_supplies': MessageHandler._add_supplies,

	#Manager_account
	'login': MessageHandler._login,
	'login_unique': MessageHandler._login_unique,
	'bind_account': MessageHandler._bind_account,

}
