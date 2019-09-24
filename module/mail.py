'''
mail.py
'''

from module import common


SWITCH = {}


'''
Possible valid kwargs:
	from_, body, subject, items, quantities, sender, uid_sender, name, target

Required Kwargs By MailType:
	SIMPLE: No kwargs required
	GIFT: quantities, items
	FRIEND_REQUEST: from_, sender, uid_sender
	FAMILY_REQUEST: name, target
'''
async def send_mail(mailtype, uid_to, **kwargs):
	try:
		return await (SWITCH[mailtype])(uid_to, **kwargs)
	except KeyError: return False

async def get_new_mail(uid, **kwargs):
	async with kwargs['session'].post(kwargs['mailserverbaseurl'] + '/get_new_mail', data = {'world' : kwargs['world'], 'unique_id' : uid}) as resp:
		return await resp.json(content_type = 'text/json')

#################################################################################################

async def _send_mail(mail, **kwargs):
	async with kwargs['session'].post(kwargs['mailserverbaseurl'] + '/send_mail', json = mail) as resp:
		result = await resp.json(content_type = 'text/json')
		return result['status'] == 0

async def _send_mail_simple(uid_to, **kwargs):
	mail = {'world' : kwargs['world'], 'uid_to' : uid_to, 'kwargs' : {'from' : kwargs.get('from_', 'server'), 'body' : kwargs.get('body', 'This is a test message'), 'subject' : kwargs.get('subject', 'Test Message'), 'type' : (common.MailType.SIMPLE.name).lower()}}
	return await _send_mail(mail, **kwargs)

async def _send_mail_gift(uid_to, **kwargs):
	mail = {'world' : kwargs['world'], 'uid_to' : uid_to, 'kwargs' : {'from' : kwargs.get('from_', 'server'), 'body' : kwargs.get('body', 'Your gift is waiting!'), 'subject' : kwargs.get('subject', 'You have a gift!'), 'type' : (common.MailType.GIFT.name).lower(), 'quantities' : kwargs['quantities'], 'items' : kwargs['items']}}
	return await _send_mail(mail, **kwargs)

async def _send_mail_friend_request(uid_to, **kwargs):
	mail = {'world' : kwargs['world'], 'uid_to' : uid_to, 'kwargs' : {'from' : kwargs['from_'], 'body' : kwargs.get('body', 'Friend request'), 'subject' : kwargs.get('subject', 'You Have A Friend Request!'), 'type' : (common.MailType.FRIEND_REQUEST.name).lower(), 'sender' : kwargs['sender'], 'uid_sender' : kwargs['uid_sender']}}
	return await _send_mail(mail, **kwargs)

async def _send_mail_family_request(uid_to, **kwargs):
	mail = {'world' : kwargs['world'], 'uid_to' : uid_to, 'kwargs' : {'from' : kwargs.get('from_', 'server'), 'body' : kwargs.get('body', 'Family request'), 'subject' : kwargs.get('subject', 'Family Request'), 'type' : (common.MailType.FAMILY_REQUEST.name).lower(), 'name' : kwargs['name'], 'target' : kwargs['target']}}
	return await _send_mail(mail, **kwargs)

SWITCH[common.MailType.SIMPLE] = _send_mail_simple
SWITCH[common.MailType.GIFT] = _send_mail_gift
SWITCH[common.MailType.FRIEND_REQUEST] = _send_mail_friend_request
SWITCH[common.MailType.FAMILY_REQUEST] = _send_mail_family_request
