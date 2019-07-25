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
MANAGER_GAME_BASE_URL = CONFIG['game_manager']['address'] + ":" + CONFIG['game_manager']['port']


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
		async with session.post(MANAGER_ACCOUNT_BASE_URL + '/bind_account', data={'unique_id': message['data']['unique_id'], 'password' : message['data']['password'], 'account': message['data']['account'], 'email': message['data']['email'], 'phone_number' : message['data']['phone_number']}) as resp:
			return await resp.text()

	async def _level_up_skill(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/level_up_skill', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'skill_id': message['data']['skill_id'], 'scroll_id': message['data']['scroll_id']}) as resp:
			return await resp.text()

	async def _get_all_skill_level(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/get_all_skill_level', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _get_all_supplies(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/get_all_supplies', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _random_gift_skill(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/random_gift_skill', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _random_gift_segment(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/random_gift_segment', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _get_skill(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/get_skill', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'skill_id': message["data"]["skill_id"]}) as resp:
			return await resp.text()

	async def _update_energy(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/try_energy', data={'unique_id': message['data']['unique_id'], 'amount': message["data"]["amount"]}) as resp:
			return await resp.text()

	async def _level_up_scroll(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/level_up_scroll', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'scroll_id': message['data']['scroll_id']}) as resp:
			return await resp.text()
	
	# region _01_Manager_Weapon.py
	async def _level_up_weapon(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/level_up_weapon', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'weapon': message['data']['weapon'], 'iron': message['data']['iron']}) as resp:
			return await resp.text()

	async def _level_up_passive(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/level_up_passive', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'weapon': message['data']['weapon'], 'passive': message['data']['passive']}) as resp:
			return await resp.text()

	async def _reset_weapon_skill_point(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/reset_weapon_skill_point', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'weapon': message['data']['weapon']}) as resp:
			return await resp.text()

	async def _level_up_weapon_star(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/level_up_weapon_star', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'weapon': message['data']['weapon']}) as resp:
			return await resp.text()

	async def _get_all_weapon(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/get_all_weapon', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()
	# endregion
	
	async def _pass_stage(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/pass_stage', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'stage': message['data']['stage']}) as resp:
			return await resp.text()

	async def _decrease_energy(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/decrease_energy', data={'unique_id': message['data']['unique_id'], 'energy': message['data']['energy']}) as resp:
			return await resp.text()

	async def _increase_energy(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/increase_energy', data={'unique_id': message['data']['unique_id'], 'energy': message['data']['energy']}) as resp:
			return await resp.text()

	# 以后会删除这个方法
	async def _add_supplies(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/add_supplies', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'supply': message['data']['supply'], 'value': message['data']['value']}) as resp:
			return await resp.text()

	async def _get_all_head(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/get_all_head', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'table' : message['data']['table']}) as resp:
			return await resp.text()

	async def _get_all_material(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/get_all_material', data={'world' : message['world'], 'unique_id': message['data']['unique_id']}) as resp:
			return await resp.text()

	async def _try_all_material(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/try_all_material', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'stage' : message['data']['stage']}) as resp:
			return await resp.text()

	async def _try_coin(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/try_coin', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'value' : message['data']['value']}) as resp:
			return await resp.text()

	async def _try_unlock_skill(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/try_unlock_skill', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'skill_id' : message['data']['skill_id']}) as resp:
			return await resp.text()

	async def _try_unlock_weapon(self, message: dict, session) -> str:
		async with session.post(MANAGER_GAME_BASE_URL + '/try_unlock_weapon', data={'world' : message['world'], 'unique_id': message['data']['unique_id'], 'weapon' : message['data']['weapon']}) as resp:
			return await resp.text()


DOES_NOT_NEED_TOKEN = {'login', 'login_unique'}

FUNCTION_LIST = {
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
	'try_unlock_weapon' : MessageHandler._try_unlock_weapon,
	'pass_stage' : MessageHandler._pass_stage,
	'random_gift_skill' : MessageHandler._random_gift_skill,
	'random_gift_segment' : MessageHandler._random_gift_segment



}
