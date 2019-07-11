
import json
import pyDes
import base64



DESIv = '67891234'
DESKey = '6789123467891234'



class MessageHandler:

	def __init__(self):
		self._functions = FUNCTION_LIST
		self._k = pyDes.triple_des(DESKey, pyDes.CBC, DESIv, pad=None, padmode=pyDes.PAD_PKCS5)

	def process_message_out(self, message: dict) -> bytes:
		'''
		Called before sending message response to client.
		Serializes the dictionary into JSON format, encodes and encrypts the resulting
		string, and returns a bytes object.
		'''
		string = json.dumps(message)
		return base64.encodestring(self._k.encrypt(string.encode()))

	def process_message_in(self, message: bytes) -> dict:
		'''
		Called upon receiving the message payload from client.
		Decrypts and decodes the incoming bytes message and returns a dictionary.
		'''
		decoded = self._k.decrypt(base64.decodebytes(message))
		return json.loads(decoded)

	async def resolve(self, message: dict, session) -> dict:
		try:
			fn = self._functions[message['function']]
			return await fn(self, message, session)
		except KeyError:
			pass


	async def _login(self, message: dict, session) -> dict:
		pass

	async def _login_unique(self, message: dict, session) -> dict:
		async with session.post('http://localhost:8080/login_unique', data = {'unique_id' : '4'}) as resp:
			print(await resp.json(content_type='text/json'))




FUNCTION_LIST = {
				'login' : MessageHandler._login,
				'login_unique' : MessageHandler._login_unique
				}
