'''
account.py

Contains functions related to administrative account activies such as logging in, and
binding email addresses.
'''

import re
import string
import random
import asyncio
import hashlib
import secrets
from module import common
from module import enums
from utility import direct_mail
from utility import verify_phone
from module import achievement
N = 2**10
R = 8
P = 1

PW_RE = re.compile(r'\A[\w!@#$%^&*()_+|`~=\-\\\[\]:;\'\"{}/?,.<>]{6,30}\Z')
AC_RE = re.compile(r'^[A-Za-z]\w{5,24}$')
EM_RE = re.compile(r'^s*([A-Za-z0-9_-]+(.\w+)*@(\w+.)+\w{2,5})s*$')


async def login_unique(uid, **kwargs):
	exists, bound = await asyncio.gather(common.exists('info', ('unique_id', uid), \
			account = True, **kwargs), _account_bound(uid, **kwargs))
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
	if not await _valid_credentials(identifier, value, password, **kwargs):
		return common.mt(1, 'invalid credentials')
	uid = await _get_unique_id(identifier, value, **kwargs)
	data = await _request_new_token(uid, await _get_prev_token(identifier, value, **kwargs), **kwargs)
	_, aep = await asyncio.gather(_record_token(uid, data['token'], **kwargs), \
			_get_account_email_phone(uid, **kwargs))
	data['account'], data['email'], data['phone_number'] = aep
	return common.mt(0, 'success', data)

async def bind_account(uid, account, password, **kwargs):
	if await _account_bound(uid, **kwargs): return common.mt(96, 'account already bound')
	if not _valid_account(account): return common.mt(99, 'invalid account name')
	if not _valid_password(password): return common.mt(98, 'invalid password')
	if await common.exists('info', ('account', account), account = True, **kwargs):
		return common.mt(97, 'invalid account name')
	salt = str(secrets.randbits(256))
	if len(salt) % 2 != 0:
		salt = '0' + salt
	hashed_pw = hashlib.scrypt(password.encode(), salt = salt.encode(), n = N, r = R, p = P).hex()
	await _set_credentials(uid, account, hashed_pw, salt, **kwargs)
	return common.mt(0, 'success', {'account' : account})

async def bind_email(uid, email, **kwargs):
	if not await _account_bound(uid, **kwargs): return common.mt(99, 'account is not bound')
	bound, exists = await asyncio.gather(_email_bound(uid, **kwargs), common.exists('info', ('email', email), account = True, **kwargs))
	if bound: return common.mt(98, 'email has already been bound')
	if exists: return common.mt(97, 'email already exists')
	code = await _gen_email_code(email, **kwargs)
	r = await direct_mail.send_verification(email, code, kwargs['session'])
	if r != 'OK': return common.mt(96, 'email could not be sent', {'message' : r})
	return common.mt(0, 'success')

async def bind_phone(uid, phone, **kwargs):
	if not await _account_bound(uid, **kwargs): return common.mt(99, 'account is not bound')
	bound, exists = await asyncio.gather(_phone_bound(uid, **kwargs), common.exists('info', ('phone_number', phone), account = True, **kwargs))
	if bound: return common.mt(98, 'phone has already been bound')
	if exists: return common.mt(97, 'phone already exists')
	code = await _gen_phone_code(phone, **kwargs)
	r = verify_phone.send_verification(phone, code)
	if r != 'OK': return common.mt(96, 'phone could not be sent', {'message' : r})
	return common.mt(0, 'success')

async def verify_email_code(uid, code, **kwargs):
	email = await kwargs['redis'].get('nonce.verify.email.' + code)
	if not email: return common.mt(99, 'invalid code')
	email = email.decode()
	await kwargs['redis'].delete('nonce.verify.email.' + code)
	bound, exists = await asyncio.gather(_email_bound(uid, **kwargs), common.exists('info', ('email', email), account = True, **kwargs))
	if bound: return common.mt(98, 'account already bound email')
	if exists: return common.mt(97, 'email already exists')
	await _set_email(uid, email, **kwargs)
	return common.mt(0, 'success, email verified', {'email' : email})

async def verify_phone_code(uid, code, **kwargs):
	phone = await kwargs['redis'].get('nonce.verify.phone.' + code)
	if not phone: return common.mt(99, 'invalid code')
	phone = phone.decode()
	await kwargs['redis'].delete('nonce.verify.phone.' + code)
	bound, exists = await asyncio.gather(_phone_bound(uid, **kwargs), common.exists('info', ('phone_number', phone), account = True, **kwargs))
	if bound: return common.mt(98, 'account already bound phone')
	if exists: return common.mt(97, 'phone already exists')
	await _set_phone(uid, phone, **kwargs)
	return common.mt(0, 'success, phone verified', {'phone' : phone})

#######################################################################

async def _account_bound(uid, **kwargs):
	data = await common.execute(f'SELECT account FROM info WHERE unique_id = "{uid}";', \
			account = True, **kwargs)
	return not (data == () or (None,) in data or ('',) in data)

async def _create_new_user(uid, **kwargs):
	await common.execute(f'INSERT INTO info (unique_id) VALUES("{uid}");', account = True, **kwargs)

async def _email_bound(uid, **kwargs):
	data = await common.execute(f'SELECT email FROM info WHERE unique_id = "{uid}";', \
			account = True, **kwargs)
	return not (data == () or (None,) in data or ('',) in data)

async def _phone_bound(uid, **kwargs):
	data = await common.execute(f'SELECT phone_number FROM info WHERE unique_id = "{uid}";', \
			account = True, **kwargs)
	return not (data == () or (None,) in data or ('',) in data)

async def _gen_email_code(email, **kwargs):
	code = ''.join(random.choice(string.digits) for i in range(6))
	while await kwargs['redis'].setnx('nonce.verify.email.' + code, email) == 0:
		code = ''.join(random.choice(string.digits) for i in range(6))
	await kwargs['redis'].expire('nonce.verify.email.' + code, 300)
	return code

async def _gen_phone_code(phone, **kwargs):
	code = ''.join(random.choice(string.digits) for i in range(4))
	while await kwargs['redis'].setnx('nonce.verify.phone.' + code, phone) == 0:
		code = ''.join(random.choice(string.digits) for i in range(4))
	await kwargs['redis'].expire('nonce.verify.phone.' + code, 300)
	return code

async def _get_account_email_phone(uid, **kwargs):
	data = await common.execute(f'SELECT account, email, phone_number FROM info WHERE unique_id = "{uid}";', account = True, **kwargs)
	return data[0]

async def _get_hash_and_salt(identifier, value, **kwargs):
	data = await common.execute(f'SELECT password, salt FROM info WHERE `{identifier}` = "{value}";', account = True, **kwargs)
	return (None, None) if data == () else data[0]

async def _get_prev_token(identifier, value, **kwargs):
	data = await common.execute(f'SELECT token FROM info WHERE {identifier} = "{value}";', account = True, **kwargs)
	return data[0][0]

async def _get_unique_id(identifier, value, **kwargs):
	data = await common.execute(f'SELECT unique_id FROM info WHERE `{identifier}` = "{value}";', account = True, **kwargs)
	if data == () or (None,) in data or ('',) in data:
		return ''
	return data[0][0]

async def _record_token(uid, token, **kwargs):
	await common.execute(f'UPDATE info SET token = "{token}" WHERE unique_id = "{uid}";', account = True, **kwargs)

async def _request_new_token(uid, prev_token = '', **kwargs):
	async with kwargs['session'].post(kwargs['tokenserverbaseurl'] + '/issue_token', \
			data = {'uid' : uid, 'prev_token' : prev_token}) as resp:
		return await resp.json()

async def _set_credentials(uid, account, hashed_pw, salt, **kwargs):
	await common.execute(f'UPDATE info SET account = "{account}", password = "{hashed_pw}", salt = "{salt}" WHERE unique_id = "{uid}";', account = True, **kwargs)

async def _set_email(uid, email, **kwargs):
	await common.execute(f'UPDATE info SET email = "{email}" WHERE unique_id = "{uid}";', account = True, **kwargs)

async def _set_phone(uid, phone, **kwargs):
	await common.execute(f'UPDATE info SET phone_number = "{phone}" WHERE unique_id = "{uid}";', account = True, **kwargs)

async def _valid_credentials(identifier, value, password, **kwargs):
	if not _valid_password(password): return False
	if identifier == 'account':
		if not _valid_account(value): return False
	elif identifier == 'email':
		if not _valid_email(value): return False
	hashed_pw, salt = await _get_hash_and_salt(identifier, value, **kwargs)
	print(f'this is HPW: {hashed_pw} and this is SALT: {salt}')
	if not hashed_pw: return False
	input_hash = hashlib.scrypt(password.encode(), salt = salt.encode(), n = N, r = R, p = P).hex()
	return input_hash == hashed_pw

def _valid_account(account):
	return bool(AC_RE.match(account))

def _valid_email(email):
	return bool(EM_RE.match(email))

def _valid_password(password):
	return bool(PW_RE.match(password))



