import json
import pyDes
import base64



DESIv = '67891234'
DESKey = '6789123467891234'

MD5_ALIYA = b'e3cb970693574ea75d091a6049f8a3ff'


TOKEN_BASE_URL = 'http://localhost:8080'
WEAPON_MANAGER_BASE_URL = 'http://localhost:8083'

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
		try:
			fn = self._functions[message['function']]
			if message['function'] not in DOES_NOT_NEED_TOKEN:
				async with session.get(TOKEN_BASE_URL + '/validate', headers = {'Authorization' : message['data']['token']}) as resp:
					if resp.status != 200:
						return json.dumps({'status' : 11, 'message' : 'Authorization required', 'data' : {'bad_token' : message['data']['token']}})
					token_response = await resp.json(content_type='text/json')
					message['data']['unique_id'] = token_response['unique_id']
			return await fn(self, message, session)
		except KeyError:
			return json.dumps({'status' : 10, 'message' : 'Invalid message format', 'data':{}})

	def _format_message_size(self, size: int) -> bytes:
		'''
		0 pads the size of the message and outputs bytes.
		'''
		return str(size).zfill(4).encode()


	async def _login(self, message: dict, session) -> str:
		async with session.post(TOKEN_BASE_URL + '/login', data = {'identifier' : message['data']['identifier'], 'value' : message['data']['value'], 'password' : message['data']['password']}) as resp:
			return await resp.text()

	async def _login_unique(self, message: dict, session) -> str:
		async with session.post(TOKEN_BASE_URL + '/login_unique', data = {'unique_id' : message['data']['unique_id']}) as resp:
			return await resp.text()

	
	async def _level_up_weapon(self, message: dict, session) -> str:
		async with session.post(WEAPON_MANAGER_BASE_URL + '/level_up_weapon', data = {'unique_id' : message['data']['unique_id'], 'weapon' : message['data']['weapon'], 'iron' : message['data']['iron']}) as resp:
			return await resp.text()

	async def _level_up_passive(self, message: dict, session) -> str:
		async with session.post(WEAPON_MANAGER_BASE_URL + '/level_up_passive', data = {'unique_id' : message['data']['unique_id'], 'weapon' : message['data']['weapon'], 'passive' : message['data']['passive']}) as resp:
			return await resp.text()




DOES_NOT_NEED_TOKEN = {'login', 'login_unique'}

FUNCTION_LIST = {
				'login' : MessageHandler._login,
				'login_unique' : MessageHandler._login_unique,
				'level_up_weapon': MessageHandler._level_up_weapon,
				'level_up_passive': MessageHandler._level_up_passive
				}

