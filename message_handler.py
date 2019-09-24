import json

from utility import config_reader

from module import family
from module import account
from module import common

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
	async def resolve(self, message: str, resource) -> str:
		'''
		Resolves the message included in the request. If required, ensures that a valid token is present.
		'''
		message = json.loads(message)
		try:
			fn = self._functions[message['function']]
		except KeyError:
			return '{"status" : 10, "message" : "function is not in function list"}'
		message['session'] = resource['session']
		message['redis'] = resource['redis']
		message['worlddb'] = resource['db']
		message['accountdb'] = resource['accountdb']
		message['tokenserverbaseurl'] = TOKEN_BASE_URL
		return await fn(self, message)



	# account.py
	async def _login_unique(self, data: dict) -> str:
		return json.dumps(await account.login_unique(data['data']['unique_id'], **data))

	async def _login(self, data: dict) -> str:
		return json.dumps(await account.login(data['data']['identifier'], data['data']['value'], data['data']['password'], **data))

	async def _bind_account(self, data: dict) -> str:
		return json.dumps(await account.bind_account(data['data']['unique_id'], data['data']['account'], data['data']['password'], **data))

	async def _bind_email(self, data: dict) -> str:
		return json.dumps(await account.bind_email(data['data']['unique_id'], data['data']['email'], **data))
	async def _verify_email_code(self, data: dict) -> str:
		return json.dumps(await account.verify_email_code(data['data']['unique_id'], data['data']['code'], **data))

	# family.py
	async def _create_family(self, data: dict) -> str:
		return json.dumps(await family.create(data['data']['unique_id'], data['data']['name'], **data))

	async def _leave_family(self, data: dict) -> str:
		return json.dumps(await family.leave(data['data']['unique_id'], **data))


FUNCTION_LIST = {
	# account.py
	'login_unique' : MessageHandler._login_unique,
	'login' : MessageHandler._login,
	'bind_account' : MessageHandler._bind_account,
	'bind_email' : MessageHandler._bind_email,
	'verify_email_code' : MessageHandler._verify_email_code,

	# family.py
	'create_family': MessageHandler._create_family,
	'leave_family' : MessageHandler._leave_family
}

