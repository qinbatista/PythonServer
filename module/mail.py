'''
mail.py
'''

from module import common
from module import family
from module import enums


SWITCH = {}


'''
Possible valid kwargs:
	from_, body, subject, items, sender, uid_sender, name, target

Required Kwargs By MailType:
	SIMPLE: No kwargs required
	GIFT: items
	FRIEND_REQUEST: sender, uid_sender
	FAMILY_REQUEST: name, target
'''
async def send_mail(mailtype, *args, **kwargs):
	try:
		for uid in args:
			await (SWITCH[mailtype])(uid, **kwargs)
		return True
	except KeyError as e:
		print(e)
		return False

async def get_new_mail(uid, **kwargs):
	async with kwargs['session'].post(kwargs['mailserverbaseurl'] + '/new', data = {'world' : kwargs['world'], 'uid' : uid}) as resp:
		return await resp.json(content_type = 'text/json')

async def get_all_mail(uid, **kwargs):
	async with kwargs['session'].post(kwargs['mailserverbaseurl'] + '/all', data = {'world' : kwargs['world'], 'uid' : uid}) as resp:
		return await resp.json(content_type = 'text/json')

async def delete_mail(uid, key, **kwargs):
	async with kwargs['session'].post(kwargs['mailserverbaseurl'] + '/delete', data = {'world' : kwargs['world'], 'uid' : uid, 'key' : key}) as resp:
		return await resp.json(content_type = 'text/json')

async def mark_read(uid, key, **kwargs):
	async with kwargs['session'].post(kwargs['mailserverbaseurl'] + '/mark_read', data = {'world' : kwargs['world'], 'uid' : uid, 'key' : key}) as resp:
		return await resp.json(content_type = 'text/json')

async def delete_read(uid, **kwargs):
	async with kwargs['session'].post(kwargs['mailserverbaseurl'] + '/delete_read', data = {'world' : kwargs['world'], 'uid' : uid}) as resp:
		return await resp.json(content_type = 'text/json')


#################################################################################################

async def _send_mail(mail, **kwargs):
	async with kwargs['session'].post(kwargs['mailserverbaseurl'] + '/send', json = mail) as resp:
		result = await resp.json(content_type = 'text/json')
		return result['status'] == 0

async def _send_mail_simple(uid, **kwargs):
	mail = {'world' : kwargs['world'], 'uid' : uid, 'kwargs' : {'from' : kwargs['data'].get('from_', await family._get_gn(uid, **kwargs)), 'body' : kwargs['data'].get('body', 'This is a test message'), 'subj' : kwargs['data'].get('subj', 'Test Message'), 'type' : enums.MailType.SIMPLE.value}}
	return await _send_mail(mail, **kwargs)

async def _send_mail_gift(uid, **kwargs):
	mail = {'world' : kwargs['world'], 'uid' : uid, 'kwargs' : {'from' : kwargs.get('from_', await family._get_gn(uid, **kwargs)), 'body' : kwargs.get('body', 'Your gift is waiting!'), 'subj' : kwargs.get('subj', 'You have a gift!'), 'type' : enums.MailType.GIFT.value, 'items' : kwargs['data']['items']}}
	return await _send_mail(mail, **kwargs)

async def _send_mail_friend_request(uid, **kwargs):
	print(f'MAIL: this is kwargs: {kwargs}')
	mail = {'world' : kwargs['world'], 'uid' : uid, 'kwargs' : {'from' : kwargs['data']['sender'], 'body' : kwargs.get('body', 'Friend request'), 'subj' : kwargs.get('subj', 'You Have A Friend Request!'), 'type' : enums.MailType.FRIEND_REQUEST.value, 'uid_sender' : kwargs['data']['uid_sender']}}
	return await _send_mail(mail, **kwargs)

async def _send_mail_family_request(uid, **kwargs):
	mail = {'world' : kwargs['world'], 'uid' : uid, 'kwargs' : {'from' : kwargs.get('from_', 'server'), 'body' : kwargs.get('body', 'Family request'), 'subj' : kwargs.get('subj', 'Family Request'), 'type' : enums.MailType.FAMILY_REQUEST.value, 'name' : kwargs['data']['name'], 'target' : kwargs['data']['target']}}
	return await _send_mail(mail, **kwargs)

SWITCH[enums.MailType.SIMPLE] = _send_mail_simple
SWITCH[enums.MailType.GIFT] = _send_mail_gift
SWITCH[enums.MailType.FRIEND_REQUEST] = _send_mail_friend_request
SWITCH[enums.MailType.FAMILY_REQUEST] = _send_mail_family_request
