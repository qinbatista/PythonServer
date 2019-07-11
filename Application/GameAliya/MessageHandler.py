
import json
import pyDes
import base64



DESIv = '67891234'
DESKey = '6789123467891234'



class MessageHandler:
	def __init__(self):
		self._functions = FUNCTION_LIST
		self._k = pyDes.triple_des(DESKey, pyDes.CBC, DESIv, pad=None, padmode=pyDes.PAD_PKCS5)

	def process_message_out(self, server_response: str) -> bytes:
		'''
		Called before sending message response to client.
		Serializes the dictionary into JSON format, encodes and encrypts the resulting
		string, and returns a bytes object.
		'''
		return base64.encodestring(self._k.encrypt(server_response.encode()))

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
				async with session.post('http://localhost:8080/validate', headers = {'Authorization' : message['data']['token']}) as resp:
					if resp.status != 200:
						return json.dumps({'status' : 2, 'message' : 'Authorization required', 'data' : {}})
					token_response = await resp.json(content_type='text/json')
					message['data']['unique_id'] = token_response['unique_id']
			return await fn(self, message, session)
		except KeyError:
			return json.dumps({'status' : 1, 'message' : 'Invalid message format', 'data':{}})

	async def _login(self, message: dict, session) -> str:
		pass

	async def _login_unique(self, message: dict, session) -> str:
		async with session.post('http://localhost:8080/login_unique', data = {'unique_id' : message['data']['unique_id']}) as resp:
			return await resp.text()




DOES_NOT_NEED_TOKEN = {'login', 'login_unique'}

FUNCTION_LIST = {
				'login' : MessageHandler._login,
				'login_unique' : MessageHandler._login_unique
				}

