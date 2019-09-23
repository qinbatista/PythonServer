'''
account.py

Contains functions related to administrative account activies such as logging in, and
binding email addresses.
'''
import re
import asyncio

from module import common

PW_RE = re.compile(r'\A[\w!@#$%^&*()_+|`~=\-\\\[\]:;\'\"{}/?,.<>]{6,30}\Z')
AC_RE = re.compile(r'^[A-Za-z]\w{5,24}$')


async def login_unique(uid, **kwargs):
	exists, bound = await asyncio.gather(common.exists('info', 'unique_id', uid, db = 'accountdb', **kwargs), _account_bound(uid, **kwargs))
	if not exists:
		await _create_new_user(uid, **kwargs)
		status, message, prev_token = 1, 'new account created', ''
	elif bound:
		return common.mt(2, 'account already bound')
	else:
		status, message, prev_token = 0, 'success', await _get_prev_token('unique_id', uid, **kwargs)
	token = await _request_new_token(uid, prev_token, **kwargs)
	await _record_token(uid, token['token'], **kwargs)
	return common.mt(status, message, token)


async def login(identifier, value, password, **kwargs):
	pass

async def bind_account(uid, account, password):
	pass

async def bind_email(uid, email, **kwargs):
	pass

async def verify_email_code():
	pass

#######################################################################

async def _account_bound(uid, **kwargs):
	data = await common.execute(f'SELECT account FROM info WHERE unique_id = "{uid}";', kwargs['accountdb'])
	return not (data == () or (None,) in data or ('',) in data)

async def _create_new_user(uid, **kwargs):
	await common.execute(f'INSERT INTO info (unique_id) VALUES("{uid}");', kwargs['accountdb'])

async def _get_prev_token(identifier, value, **kwargs):
	data = await common.execute(f'SELECT token FROM info WHERE {identifier} = "{value}";', kwargs['accountdb'])
	return data[0][0]

async def _request_new_token(uid, prev_token = '', **kwargs):
	async with kwargs['session'].post(kwargs['tokenserverbaseurl'] + '/issue_token', data = {'unique_id' : uid, 'prev_token' : prev_token}) as resp:
		return await resp.json(content_type = 'text/json')

async def _record_token(uid, token, **kwargs):
	await common.execute(f'UPDATE info SET token = "{token}" WHERE unique_id = "{uid}";', kwargs['accountdb'])
