'''
mail.py

Fascilitates the sending and receiving of in-game mail.

The construction, storage, and retrieval of in-game mail happens on a different server.
The module handles all required HTTP requests to the mail server.
Additionally, will register nonces for certain types of mail.

The send_mail method handles the sending of all types of mail.
The "mail" parameter is a dictionary whose contents change depending upon the type of mail being sent.
All mail types MUST have the following keys in the mail parameter:
	- type - A number repesenting the enums.MailType value
	- from - A string denoting who the mail is from
	- subj - The subject line of the mail
	- body - The main body of the mail

Depending on the mail's type, additional parameters in the mail dictionary may be required as declared here:
	SIMPLE:
		
	GIFT:
		- items - An encoded string of items to be sent as a gift
	
	FRIEND_REQUEST:
		- uid_sender - The unique id of the sender

	FAMILY_REQUEST:
		- uid_target - The unique id of the player who might be added to the family
		- name - The name of the family who might accept the new player
'''

import asyncio

from module import enums
from module import common
from datetime import datetime

SWITCH = {}
DAILY_SEND_LIMIT = 10


async def send_mail(mail, *uids, **kwargs):
	sent = await asyncio.gather(*[_send_mail(mail, uid, **kwargs) for uid in uids])
	return {s.pop('uid') : s for s in sent}

async def send_mail_public(uid, gn_target, **kwargs):
	now   = datetime.now(tz = common.TZ_SH)
	limit = await common.get_limit(uid, enums.Limits.MAIL_DAILY_SEND, **kwargs)
	limit = limit if limit is not None else 0
	timer = await common.get_timer(uid, enums.Timer.MAIL_LAST_SENT,   **kwargs)

	if timer is not None and timer.date() == now.date():
		if limit >= DAILY_SEND_LIMIT:
			return common.mt(99, 'exceeded daily send limit')
	else: limit = 0

	uid_t = await common.get_uid(gn_target, **kwargs)
	sent  = await send_mail({'type' : enums.MailType.SIMPLE.value, \
			'from' : await common.get_gn(uid, **kwargs), 'subj' : kwargs['data']['subj'], \
			'body' : kwargs['data']['body']}, uid_t, **kwargs)
	if sent[uid_t]['status'] != 0:
		return common.mt(98, 'error', {'sent' : limit})

	await common.set_timer(uid, enums.Timer.MAIL_LAST_SENT  , now      , **kwargs)
	await common.set_limit(uid, enums.Limits.MAIL_DAILY_SEND, limit + 1, **kwargs)
	return common.mt(0, 'success', {'sent' : limit + 1})

async def get_new_mail(uid, **kwargs):
	async with kwargs['session'].post(kwargs['mailserverbaseurl'] + '/new', \
			data = {'world' : kwargs['world'], 'uid' : uid}) as resp:
		return common.mt(0, 'success', await resp.json())

async def get_all_mail(uid, **kwargs):
	async with kwargs['session'].post(kwargs['mailserverbaseurl'] + '/all', \
			data = {'world' : kwargs['world'], 'uid' : uid}) as resp:
		return common.mt(0, 'success', await resp.json())

async def delete_mail(uid, key, **kwargs):
	if key != '':
		async with kwargs['session'].post(kwargs['mailserverbaseurl'] + '/delete', \
				data = {'world' : kwargs['world'], 'uid' : uid, 'key' : key}) as resp:
			return common.mt(0, 'success', await resp.json())
	return common.mt(99, 'key不能为空')

async def mark_read(uid, key, **kwargs):
	if key != '':
		async with kwargs['session'].post(kwargs['mailserverbaseurl'] + '/mark_read', \
				data = {'world' : kwargs['world'], 'uid' : uid, 'key' : key}) as resp:
			return common.mt(0, 'success', await resp.json())
	return common.mt(99, 'key不能为空')

async def delete_read(uid, **kwargs):
	async with kwargs['session'].post(kwargs['mailserverbaseurl'] + '/delete_read', \
			data = {'world' : kwargs['world'], 'uid' : uid}) as resp:
		return common.mt(0, 'success', await resp.json())

#########################################################################################
async def _send(payload, **kwargs):
	async with kwargs['session'].post(kwargs['mailserverbaseurl'] + '/send', json = payload) as resp:
		return await resp.json()

async def _send_mail(mail, recipient, **kwargs):
	try:
		return await (SWITCH[enums.MailType(mail['type'])])(mail, recipient, **kwargs)
	except KeyError:
		return {'status' : -1, 'uid' : recipient, 'key' : ''}

async def _send_mail_simple(mail, uid, **kwargs):
	return await _send({'world' : kwargs['world'], 'uid' : uid, 'mail' : \
			{k : mail[k] for k in {'type', 'from', 'subj', 'body'}}}, **kwargs)

async def _send_mail_gift(mail, uid, **kwargs):
	resp = await _send({'world' : kwargs['world'], 'uid' : uid, 'mail' : \
			{k : mail[k] for k in {'type', 'from', 'subj', 'body', 'items'}}}, **kwargs)
	if resp['status'] == 0:
		await _safe_register(uid, resp['key'], mail, {'type', 'items'}, **kwargs)
	return resp

async def _send_mail_friend_request(mail, uid, **kwargs):
	resp = await _send({'world' : kwargs['world'], 'uid' : uid, 'mail' : \
			{k : mail[k] for k in {'type', 'from', 'subj', 'body'}}}, **kwargs)
	if resp['status'] == 0:
		await _safe_register(uid, resp['key'], mail, {'type', 'uid_sender'}, **kwargs)
	return resp

async def _send_mail_family_request(mail, uid, **kwargs):
	resp = await _send({'world' : kwargs['world'], 'uid' : uid, 'mail' : \
			{k : mail[k] for k in {'type', 'from', 'subj', 'body'}}}, **kwargs)
	if resp['status'] == 0:
		await _safe_register(uid, resp['key'], mail, {'type', 'uid_target', 'name'}, **kwargs)
	return resp

async def _safe_register(uid, key, mail, payload_keys, **kwargs):
	try:
		async with kwargs['session'].post(kwargs['tokenserverbaseurl'] + '/register_nonce', \
				json = {'nonce' : key, 'payload' : {k : mail[k] for k in payload_keys}}) as resp:
			if (await resp.json())['status'] != 0:
				raise KeyError
	except KeyError:
		await delete_mail(uid, key, **kwargs)
		raise KeyError





SWITCH[enums.MailType.GIFT]           = _send_mail_gift
SWITCH[enums.MailType.SIMPLE]         = _send_mail_simple
SWITCH[enums.MailType.FRIEND_REQUEST] = _send_mail_friend_request
SWITCH[enums.MailType.FAMILY_REQUEST] = _send_mail_family_request
