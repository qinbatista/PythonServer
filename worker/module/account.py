'''
account.py

Contains functions related to administrative account activies such as logging in, and
binding email addresses.
'''

import re
import os
import time
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
# AC_RE = re.compile(r'^(?=.*[a-z])(?=.*[0-9])[_a-z0-9]{5,24}$')
AC_RE = re.compile(r'^[_a-z][_a-z0-9]{4,23}$')
EM_RE = re.compile(r'^s*([A-Za-z0-9_-]+(.\w+)*@(\w+.)+\w{2,5})s*$')
UID = "lukseun%sM%sP%s"
CID = "%s#%sr%s"


async def register(uid, account, password, **kwargs):
	"""携带uid、账号密码进行注册"""
	account = account.lower()
	if uid.find(' ') != -1: return common.mt(96, 'UID contains Spaces')
	if uid == '': uid = await yield_uid(**kwargs)
	if not _valid_account(account): return common.mt(99, 'invalid account name')
	if not _valid_password(password): return common.mt(98, 'invalid password')
	exists = await common.exists('info', ('account', account), account=True, **kwargs)
	if exists: return common.mt(97, 'The account name has been used')
	exists = await common.exists('info', ('unique_id', uid), account=True, **kwargs)
	if not exists:  # 不存在的情况下创建新用户
		await _create_new_user(uid, **kwargs)
		status, message = 1, 'new account created'
	else:
		status, message = 0, 'success'
	token = await _request_new_token(uid, **kwargs)  # 生成一个新的token或使用原来的token加长有效时限
	await _record_token(uid, token['token'], **kwargs)
	salt = str(secrets.randbits(256))
	if len(salt) % 2 != 0:
		salt = '0' + salt
	hashed_pw = hashlib.scrypt(password.encode(), salt=salt.encode(), n=N, r=R, p=P).hex()
	await _set_credentials(uid, account, hashed_pw, salt, **kwargs)
	token['account'] = account
	return common.mt(status, message, token)

async def login_unique(uid, **kwargs):
	if uid.find(' ') != -1: return common.mt(96, 'UID contains Spaces')
	if uid == '': return common.mt(99, 'unique id is empty')
	exists, bound = await asyncio.gather(common.exists('info', ('unique_id', uid), account=True, **kwargs), _account_bound(uid, **kwargs))
	if not exists:  # 不存在的情况下创建新用户
		await _create_new_user(uid, **kwargs)
		status, message = 1, 'new account created'
	elif bound:  # uid账号已经绑定，要求使用账号密码登录
		return common.mt(2, 'account already bound')
	else:
		status, message = 0, 'success'
	data = await _request_new_token(uid, **kwargs)  # 生成一个新的token
	await _record_token(uid, data['token'], **kwargs)
	return common.mt(status, message, data)

async def login(identifier, value, password, **kwargs):
	if not await _valid_credentials(identifier, value, password, **kwargs):
		return common.mt(1, 'invalid credentials')
	uid = await _get_unique_id(identifier, value, **kwargs)
	data = await _request_new_token(uid, **kwargs)
	_, aep = await asyncio.gather(_record_token(uid, data['token'], **kwargs), \
			_get_account_email_phone(uid, **kwargs))
	data['account'], data['email'], data['phone_number'] = aep
	return common.mt(0, 'success', data)

async def all_info(uid, **kwargs):
	account, email, phone_number = await _get_account_email_phone(uid, **kwargs)
	return common.mt(0, 'success', {'account': account, 'email': email, 'phone_number': phone_number})

async def bind_account(uid, account, password, **kwargs):
	account = account.lower()
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
	code = await _gen_email_code(uid, email, status=0, **kwargs)
	r = await direct_mail.send_verification(email, code, kwargs['session'])
	if r != 'OK': return common.mt(96, 'email could not be sent', {'message' : r})
	return common.mt(0, 'success')

async def unbind_email(uid, email, **kwargs):
	if not await _account_bound(uid, **kwargs): return common.mt(99, 'account is not bound')
	bound = await common.execute(f'SELECT email FROM info WHERE unique_id = "{uid}";', account=True, **kwargs)
	if bound[0][0] == '': return common.mt(98, '你未绑定邮箱')
	if bound[0][0] != email: return common.mt(97, 'email error')
	code = await _gen_email_code(uid, email, status=1, **kwargs)
	r = await direct_mail.send_verification(email, code, kwargs['session'], status=1)
	if r != 'OK': return common.mt(96, 'email could not be sent', {'message' : r})
	return common.mt(0, 'success')

async def bind_phone(uid, phone, **kwargs):
	if not await _account_bound(uid, **kwargs): return common.mt(99, 'account is not bound')
	bound, exists = await asyncio.gather(_phone_bound(uid, **kwargs), common.exists('info', ('phone_number', phone), account = True, **kwargs))
	if bound: return common.mt(98, 'phone has already been bound')
	if exists: return common.mt(97, 'phone already exists')

	# 次数限制代码
	lim = await common.get_limit(uid, enums.Limits.BIND_PHONE, **kwargs)
	tim = await common.get_timer(uid, enums.Timer.BIND_PHONE_END, '%Y-%m-%d', **kwargs)
	now = common.datetime.now(tz=common.TZ_SH)
	if lim is None or tim is None or now >= tim:
		lim, tim = 5, now + common.timedelta(days=1)
	if lim <= 0: return common.mt(95, '今天发送短信次数已用完')
	lim -= 1
	await common.set_limit(uid, enums.Limits.BIND_PHONE, lim, **kwargs)
	await common.set_timer(uid, enums.Timer.BIND_PHONE_END, tim, '%Y-%m-%d', **kwargs)

	code = await _gen_phone_code(uid, phone, status=0, **kwargs)
	r = verify_phone.send_verification(phone, code, common.datetime.now(tz=common.TZ_SH).strftime("%Y%m%d"))
	if r != 'OK': return common.mt(96, 'phone could not be sent', {'message' : r})
	return common.mt(0, 'success')

async def unbind_phone(uid, phone, **kwargs):
	if not await _account_bound(uid, **kwargs): return common.mt(99, 'account is not bound')
	bound = await common.execute(f'SELECT phone_number FROM info WHERE unique_id = "{uid}";', account=True, **kwargs)
	if bound[0][0] == '': return common.mt(98, '你未绑定手机号')
	if bound[0][0] != phone: return common.mt(97, '手机号错误')

	# 次数限制代码
	lim = await common.get_limit(uid, enums.Limits.BIND_PHONE, **kwargs)
	tim = await common.get_timer(uid, enums.Timer.BIND_PHONE_END, '%Y-%m-%d', **kwargs)
	now = common.datetime.now(tz=common.TZ_SH)
	if lim is None or tim is None or now >= tim:
		lim, tim = 5, now + common.timedelta(days=1)
	if lim <= 0: return common.mt(95, '今天发送短信次数已用完')
	lim -= 1
	await common.set_limit(uid, enums.Limits.BIND_PHONE, lim, **kwargs)
	await common.set_timer(uid, enums.Timer.BIND_PHONE_END, tim, '%Y-%m-%d', **kwargs)

	code = await _gen_phone_code(uid, phone, status=1, **kwargs)
	r = verify_phone.send_verification(phone, code, common.datetime.now(tz=common.TZ_SH).strftime("%Y%m%d"), index=1)
	if r != 'OK': return common.mt(96, 'phone could not be sent', {'message' : r})
	return common.mt(0, 'success')

async def verify_email_code(uid, code, status=0, **kwargs):
	email = await kwargs['redis'].get(f'nonce.verify.email.{uid}.{status}.{code}')
	if not email: return common.mt(99, 'invalid code')
	# email = email.decode()
	await kwargs['redis'].delete(f'nonce.verify.email.{uid}.{status}.{code}')
	if status == 0:
		bound, exists = await asyncio.gather(_email_bound(uid, **kwargs), common.exists('info', ('email', email), account = True, **kwargs))
		if bound: return common.mt(98, 'account already bound email')
		if exists: return common.mt(97, 'email already exists')
		await _set_email(uid, email, **kwargs)
		return common.mt(0, 'success, email verified', {'email' : email})
	elif status == 1:
		await _set_email(uid, '', **kwargs)
		return common.mt(1, 'unbind success, email verified', {'email' : email})
	else:
		return common.mt(90, '无效状态码')

async def verify_phone_code(uid, code, status=0, **kwargs):
	phone = await kwargs['redis'].get(f'nonce.verify.phone.{uid}.{status}.{code}')
	if not phone: return common.mt(99, 'invalid code')
	# phone = phone.decode()
	await kwargs['redis'].delete(f'nonce.verify.phone.{uid}.{status}.{code}')
	if status == 0:
		bound, exists = await asyncio.gather(_phone_bound(uid, **kwargs), common.exists('info', ('phone_number', phone), account = True, **kwargs))
		if bound: return common.mt(98, 'account already bound phone')
		if exists: return common.mt(97, 'phone already exists')
		await _set_phone(uid, phone, **kwargs)
		return common.mt(0, 'success, phone verified', {'phone' : phone})
	elif status == 1:
		await _set_phone(uid, '', **kwargs)
		return common.mt(1, 'unbind success, phone verified', {'phone' : phone})
	else:
		return common.mt(90, '无效状态码')

#######################################################################


async def yield_uid(**kwargs):
	num, now = 10, time.time()
	uid = UID % (int(now), int(now % 1 * 1e6), os.getpid())
	while await common.exists('info', ('unique_id', uid), account=True, **kwargs) and num > 0:
		num, now = num - 1, time.time()
		uid = UID % (int(now), int(now % 1 * 1e6), os.getpid())
	return uid


async def yield_cid(uid, **kwargs):
	num, now, r = 100, time.time(), secrets.randbits(64)
	cid = CID % (int(now), int(now % 1 * 1e6), r)
	while await common.exists('info', ('cuid', cid), account=True, **kwargs) and num > 0:
		num, now, r = num - 1, time.time(), secrets.randbits(64)
		cid = CID % (int(now), int(now % 1 * 1e6), r)
	return uid if num == 0 else cid


async def _account_bound(uid, **kwargs):
	data = await common.execute(f'SELECT account FROM info WHERE unique_id = "{uid}";', account=True, **kwargs)
	return not (data == () or (None,) in data or ('',) in data)

async def _create_new_user(uid, **kwargs):
	cid = await yield_cid(uid, **kwargs)
	await common.execute(f'INSERT INTO info (unique_id, cuid) VALUES("{uid}", "{cid}");', account = True, **kwargs)

async def _email_bound(uid, **kwargs):
	data = await common.execute(f'SELECT email FROM info WHERE unique_id = "{uid}";', \
			account = True, **kwargs)
	return not (data == () or (None,) in data or ('',) in data)

async def _phone_bound(uid, **kwargs):
	data = await common.execute(f'SELECT phone_number FROM info WHERE unique_id = "{uid}";', \
			account = True, **kwargs)
	return not (data == () or (None,) in data or ('',) in data)

async def _gen_email_code(uid, email, status=0, **kwargs):
	code = ''.join(random.choice(string.digits) for i in range(6))
	while await kwargs['redis'].setnx(f'nonce.verify.email.{uid}.{status}.{code}', email) == 0:
		code = ''.join(random.choice(string.digits) for i in range(6))
	await kwargs['redis'].expire(f'nonce.verify.email.{uid}.{status}.{code}', 300)
	return code

async def _gen_phone_code(uid, phone, status=0, **kwargs):
	"""status是状态码，0绑定，1解绑"""
	code = ''.join(random.choice(string.digits) for i in range(4))
	while await kwargs['redis'].setnx(f'nonce.verify.phone.{uid}.{status}.{code}', phone) == 0:
		code = ''.join(random.choice(string.digits) for i in range(4))
	await kwargs['redis'].expire(f'nonce.verify.phone.{uid}.{status}.{code}', 300)
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
	await common.execute(f'UPDATE info SET token = "{token}" WHERE unique_id = "{uid}";', account=True, **kwargs)

async def _request_new_token(uid, is_session='0', **kwargs):
	async with kwargs['session'].post(kwargs['tokenserverbaseurl'] + '/issue_token',
			data={'uid' : uid, 'is_session': is_session}) as resp:
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
		value = value.lower()
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



