import json

from utility import config_reader

from module import family

CFG = config_reader.wait_config()

TOKEN_BASE_URL = CFG['token_server']['addr'] + ':' + CFG['token_server']['port']
MAIL_BASE_URL = CFG['mail_server']['addr'] + ':' + CFG['mail_server']['port']

class InvalidTokenError(Exception):
	pass

class MessageHandler:
	def __init__(self):
		self._functions = FUNCTION_LIST

	async def shutdown(self):
		pass

	# json.decoder.JSONDecodeError
	async def resolve(self, message: str, session, redis, db) -> str:
		'''
		Resolves the message included in the request. If required, ensures that a valid token is present.
		'''
		message = json.loads(message)
		try:
			fn = self._functions[message['function']]
		except KeyError:
			return '{"status" : 10, "message" : "function is not in function list"}'
		message['session'] = session
		message['redis'] = redis
		message['db'] = db
		return await fn(self, message)


	async def _create_family(self, data: dict) -> str:
		return json.dumps(await family.create(data['data']['unique_id'], **data))


FUNCTION_LIST = {
	'create_family': MessageHandler._create_family
}

