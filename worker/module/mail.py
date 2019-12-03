'''
mail.py
'''

from module import common
from module import enums

from datetime import datetime


SWITCH = {}

DAILY_SEND_LIMIT = 10


'''
Possible valid kwargs:
	from_, body, subject, items, sender, uid_sender, name, target

Required Kwargs By MailType:
	SIMPLE: No kwargs required
	GIFT: items
	FRIEND_REQUEST: sender, uid_sender
	FAMILY_REQUEST: name, uid_target
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
	async with kwargs['session'].post(kwargs['mailserverbaseurl'] + '/new', \
			data = {'world' : kwargs['world'], 'uid' : uid}) as resp:
		return common.mt(0, 'success', await resp.json())

async def get_all_mail(uid, **kwargs):
	async with kwargs['session'].post(kwargs['mailserverbaseurl'] + '/all', \
			data = {'world' : kwargs['world'], 'uid' : uid}) as resp:
		return common.mt(0, 'success', await resp.json())

async def delete_mail(uid, key, **kwargs):
	async with kwargs['session'].post(kwargs['mailserverbaseurl'] + '/delete', \
			data = {'world' : kwargs['world'], 'uid' : uid, 'key' : key}) as resp:
		return common.mt(0, 'success', await resp.json())

async def mark_read(uid, key, **kwargs):
	async with kwargs['session'].post(kwargs['mailserverbaseurl'] + '/mark_read', \
			data = {'world' : kwargs['world'], 'uid' : uid, 'key' : key}) as resp:
		return common.mt(0, 'success', await resp.json())

async def delete_read(uid, **kwargs):
	async with kwargs['session'].post(kwargs['mailserverbaseurl'] + '/delete_read', \
			data = {'world' : kwargs['world'], 'uid' : uid}) as resp:
		return common.mt(0, 'success', await resp.json())

async def send_mail_public(uid, gn_target, **kwargs):
	now          = datetime.now(tz=common.TZ_SH)
	limit, timer = await get_daily_send_limit(uid, **kwargs)
	if timer is not None and timer.date() == now.date():
		if limit >= DAILY_SEND_LIMIT:
			return common.mt(99, 'exceeded daily send limit')
	else: limit = 0
	res = await send_mail(enums.MailType.SIMPLE, await common.get_uid(gn_target, **kwargs), \
			from_ = await common.get_gn(uid, **kwargs), **kwargs)
	if res: await set_daily_send_limit(uid, limit + 1, now, **kwargs)
	return common.mt(0 if res else 98, 'success' if res else 'error', \
			{'sent' : limit + 1} if res else {'sent' : limit})


#################################################################################################

async def set_daily_send_limit(uid, limit, now, **kwargs):
	await common.set_timer(uid, enums.Timer.MAIL_LAST_SENT, now, **kwargs)
	await common.set_limit(uid, enums.Limits.MAIL_DAILY_SEND, limit, **kwargs)

async def get_daily_send_limit(uid, **kwargs):
	limit = await common.get_limit(uid, enums.Limits.MAIL_DAILY_SEND, **kwargs)
	timer = await common.get_timer(uid, enums.Timer.MAIL_LAST_SENT,   **kwargs)
	return (limit, timer) if limit is not None else (0, timer)


async def _send_mail(mail, **kwargs):
	async with kwargs['session'].post(kwargs['mailserverbaseurl'] + '/send', json = mail) as resp:
		return (await resp.json())['key']

async def _send_mail_simple(uid, **kwargs):
	mail = {'world' : kwargs['world'], 'uid' : uid, \
			'mail'  : { \
				'type' : enums.MailType.SIMPLE.value, \
				'from' : kwargs['data'].get('from_', kwargs['from_']), \
				'subj' : kwargs['data'].get('subj'), \
				'body' : kwargs['data'].get('body')}
			}
	return await _send_mail(mail, **kwargs)

async def _send_mail_gift(uid, **kwargs):
	mail = {'world' : kwargs['world'], 'uid' : uid, \
			'mail'  : { \
				'type' : enums.MailType.GIFT.value, \
				'from' : kwargs.get('from_', await common.get_gn(uid, **kwargs)), \
				'subj' : kwargs.get('subj', enums.MailTemplate.SYSTEM_REWARD.name), \
				'body' : kwargs.get('body', enums.MailTemplate.GIFT_1.name), \
				'items': kwargs['items']}}
	key = await _send_mail(mail, **kwargs)
	registered = await register_nonce(key, \
			{'type' : enums.MailType.GIFT.value, 'items' : kwargs['items']}, **kwargs)
	if not registered:
		await delete_mail(uid, key, **kwargs)
		return ''
	return key

async def _send_mail_friend_request(uid, **kwargs):
	mail = {'world' : kwargs['world'], 'uid' : uid, \
			'mail'  : { \
				'type' : enums.MailType.FRIEND_REQUEST.value, \
				'from' : kwargs.get('from_', 'server'), \
				'subj' : '',
				'body' : ''}}
	key = await _send_mail(mail, **kwargs)
	registered = await register_nonce(key, {'type' : enums.MailType.FRIEND_REQUEST.value, \
			'uid_sender' : kwargs['uid_sender']}, **kwargs)
	if not registered:
		await delete_mail(uid, key, **kwargs)
		return ''
	return key

async def _send_mail_family_request(uid, **kwargs):
	mail = {'world' : kwargs['world'], 'uid' : uid, \
			'mail'  : { \
				'type' : enums.MailType.FAMILY_REQUEST.value, \
				'from' : kwargs['name'], \
				'subj' : kwargs['subj'], \
				'body' : ''}}
	
	key = await _send_mail(mail, **kwargs)
	registered = await register_nonce(key, {'type' : enums.MailType.FAMILY_REQUEST.value, \
			'uid_target' : kwargs['uid_target'], 'name' : kwargs['name']}, **kwargs)
	if not registered:
		await delete_mail(uid, key, **kwargs)
		return ''
	return key

async def register_nonce(nonce, payload, **kwargs):
	async with kwargs['session'].post(kwargs['tokenserverbaseurl'] + '/register_nonce', \
			json = {'nonce' : nonce, 'payload' : payload}) as resp:
		return (await resp.json())['status'] == 0

SWITCH[enums.MailType.SIMPLE] = _send_mail_simple
SWITCH[enums.MailType.GIFT] = _send_mail_gift
SWITCH[enums.MailType.FRIEND_REQUEST] = _send_mail_friend_request
SWITCH[enums.MailType.FAMILY_REQUEST] = _send_mail_family_request
