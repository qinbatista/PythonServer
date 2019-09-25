import json

from utility import config_reader

from module import mail
from module import enums
from module import family
from module import common
from module import account
from module import lottery
from module import summoning

CFG = config_reader.wait_config()

TOKEN_BASE_URL = CFG['token_server']['addr'] + ':' + CFG['token_server']['port']
MAIL_BASE_URL = CFG['mail_server']['addr'] + ':' + CFG['mail_server']['port']

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
		message['mailserverbaseurl'] = MAIL_BASE_URL
		message['world'] = '0'
		return json.dumps(await fn(self, message))


	###################### account.py ######################
	async def _login_unique(self, data: dict) -> str:
		return await account.login_unique(data['data']['unique_id'], **data)

	async def _login(self, data: dict) -> str:
		return await account.login(data['data']['identifier'], data['data']['value'], data['data']['password'], **data)

	async def _bind_account(self, data: dict) -> str:
		return await account.bind_account(data['data']['unique_id'], data['data']['account'], data['data']['password'], **data)

	async def _bind_email(self, data: dict) -> str:
		return await account.bind_email(data['data']['unique_id'], data['data']['email'], **data)

	async def _verify_email_code(self, data: dict) -> str:
		return await account.verify_email_code(data['data']['unique_id'], data['data']['code'], **data)

	###################### family.py ######################
	async def _create_family(self, data: dict) -> str:
		return await family.create(data['data']['unique_id'], data['data']['name'], **data)

	async def _leave_family(self, data: dict) -> str:
		return await family.leave(data['data']['unique_id'], **data)

	async def _remove_user_family(self, data: dict) -> str:
		return await family.remove_user(data['data']['unique_id'], data['data']['gn_target'], **data)

	async def _invite_user_family(self, data: dict) -> str:
		return await family.invite_user(data['data']['unique_id'], data['data']['gn_target'], **data)

	async def _request_join_family(self, data: dict) -> str:
		return await family.request_join(data['data']['unique_id'], data['data']['name'], **data)

	async def _respond_family(self, data: dict) -> str:
		return await family.respond(data['data']['unique_id'], data['data']['nonce'], **data)

	###################### mail.py ######################
	async def _send_mail(self, data: dict) -> str:
		return await mail.send_mail(enums.MailType.SIMPLE, '4', '1', **data)

	async def _get_new_mail(self, data: dict) -> str:
		return await mail.get_new_mail(data['data']['unique_id'], **data)

	async def _delete_mail(self, data: dict) -> str:
		return await mail.delete_mail(data['data']['unique_id'], data['data']['key'], **data)

	###################### summoning.py ######################
	async def _basic_summon(self, data: dict) -> str:
		return await summoning.summon(data['data']['unique_id'], enums.Item(int(data['data']['item'])), enums.Tier.BASIC, enums.RewardGroup.WEAPON, **data)


	async def test(self, data: dict) -> str:
		return await common.exists('player', ('uid', '1'), ('gn', 'cuck'), **data)
##########################################################################################################
##########################################################################################################

FUNCTION_LIST = {
	'test' : MessageHandler.test,
	###################### account.py ######################
	'login_unique' : MessageHandler._login_unique,
	'login' : MessageHandler._login,
	'bind_account' : MessageHandler._bind_account,
	'bind_email' : MessageHandler._bind_email,
	'verify_email_code' : MessageHandler._verify_email_code,

	###################### family.py ######################
	'create_family': MessageHandler._create_family,
	'leave_family' : MessageHandler._leave_family,
	'remove_user_family' : MessageHandler._remove_user_family,
	'invite_user_family' : MessageHandler._invite_user_family,
	'request_join_family' : MessageHandler._request_join_family,
	'respond_family' : MessageHandler._request_join_family,

	###################### mail.py ######################
	'send_mail' : MessageHandler._send_mail,
	'get_new_mail' : MessageHandler._get_new_mail,
	'delete_mail' : MessageHandler._delete_mail,

	###################### summoning.py ######################
	'basic_summon' : MessageHandler._basic_summon
}

