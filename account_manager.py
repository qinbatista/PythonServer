#
# account manager
#
###############################################################################


import re
import time
import json
import random
import asyncio
import hashlib
import secrets
import aiomysql

from aiohttp import web
from aiohttp import ClientSession
from utility import config_reader
from utility import direct_mail

CFG = config_reader.wait_config()

TOKEN_SERVER_BASE_URL = CFG['token_server']['addr'] + ':' + CFG['token_server']['port']

# Part (1 / 2)
class AccountManager:
	def __init__(self):
		self._pool = None
		self._password_re = re.compile(r'\A[\w!@#$%^&*()_+|`~=\-\\\[\]:;\'\"{}/?,.<>]{6,30}\Z')
		self._account_re = re.compile(r'^[A-Za-z]\w{5,24}$')
		self._email_re = re.compile(r'^s*([A-Za-z0-9_-]+(.\w+)*@(\w+.)+\w{2,5})s*$')
		self._phone_re = re.compile(r'\A[0-9]{10,15}\Z')
		self._n = 2**10
		self._r = 8
		self._p = 1

	async def login_unique(self, unique_id: str) -> dict:
		retvals = await asyncio.gather(self._check_exists('unique_id', unique_id), self._account_is_bound(unique_id))
		if not retvals[0]:
			await self._create_new_user(unique_id)
			status, message, prev_token = 1, 'new account created', ''
		elif retvals[1]:
			return self.message_typesetting(2, 'account already bound')
		else:
			status, message, prev_token = 0, 'success', await self._get_prev_token('unique_id', unique_id)
		resp = await self._request_new_token(unique_id, prev_token)
		await self._register_token(unique_id, resp['token'])
		return self.message_typesetting(status, message, resp)

	async def login(self, identifier: str, value: str, password: str) -> dict:
		valid = await self._valid_credentials(identifier, value, password)
		if not valid:
			return self.message_typesetting(1, 'Invalid credentials')
		unique_id = await self._get_unique_id(identifier, value)
		resp = await self._request_new_token(unique_id, await self._get_prev_token(identifier, value))
		retvals = await asyncio.gather(self._register_token(unique_id, resp['token']), self._get_account_email_phone(unique_id))
		account_email_phone = retvals[1]
		resp['account'] = account_email_phone[0]
		resp['email'] = account_email_phone[1]
		resp['phone_number'] = account_email_phone[2]
		return self.message_typesetting(0, 'success', resp)

	async def bind_account(self, unique_id: str, account: str, password: str) -> dict:
		if not self._is_valid_account(account):
			return self.message_typesetting(99, 'invalid account name')
		if not self._is_valid_password(password):
			return self.message_typesetting(98, 'invalid password')
		if await self._check_exists('account', account):
			return self.message_typesetting(97, 'invalid account name')

		random_salt = str(secrets.randbits(256))
		if len(random_salt) % 2 != 0:
			random_salt = '0' + random_salt
		hashed_password = hashlib.scrypt(password.encode(), salt=random_salt.encode(), n = self._n, r = self._r, p = self._p).hex()
		await self._execute_statement('UPDATE info SET account = "' + account + '", password = "' + hashed_password + '", salt = "' + random_salt + '" WHERE unique_id = "' + unique_id + '";')
		return self.message_typesetting(0, 'success', {'account' : account})

	async def bind_email(self, unique_id: str, email: str, redis, session):
		if not await self._account_is_bound(unique_id):
			return self.message_typesetting(99, 'account must be bound to bind email')
		retvals = await asyncio.gather(self._email_is_bound(unique_id), self._check_exists('email', email))
		if retvals[0]: return self.message_typesetting(98, 'email has already been bound')
		if retvals[1]: return self.message_typesetting(97, 'email already exists')
		code = str(secrets.randbits(6))
		while await redis.setnx('nonce.verify.email.' + code, email) == 0:
			code = str(secrets.randbits(6))
		print(f'account manager: created nonce code {code}')
		await redis.expire('nonce.verify.email.' + code, 300)
		r = await direct_mail.send_verification(email, code, session)
		if r != 'OK':
			print(f'account_manager: email could not be sent: {r}')
			return self.message_typesetting(96, 'email could not be sent', {'message' : r})
		print('account manager: message was sent')
		return self.message_typesetting(0, 'success, email sent. code valid for 5 minutes.')

	async def verify_email_code(self, unique_id: str, code, redis, session):
		email = await redis.get('nonce.verify.email.' + code)
		if not email: return self.message_typesetting(99, 'code invalid')
		email = email.decode()
		await redis.delete('nonce.verify.email.' + code)
		retvals = await asyncio.gather(self._email_is_bound(unique_id), self._check_exists('email', email))
		if retvals[0]: return self.message_typesetting(98, 'account already bound email')
		if retvals[1]: return self.message_typesetting(97, 'email already exists')
		await self._execute_statement(f'UPDATE info SET email = "{email}" WHERE unique_id = "{unique_id}";')
		return self.message_typesetting(0, 'success, email verified', {'email' : email})



			####################################
			#          P R I V A T E		   #
			####################################

	async def _get_account_email_phone(self, unique_id: str) -> tuple:
		data = await self._execute_statement('SELECT account, email, phone_number FROM info WHERE unique_id = "' + unique_id + '";')
		return data[0]

	async def _email_is_bound(self, unique_id: str) -> bool:
		data = await self._execute_statement('SELECT email FROM info WHERE unique_id = "' + unique_id + '";')
		if ('',) in data or () == data or (None,) in data:
			return False
		return True

	async def _phone_is_bound(self, unique_id: str) -> bool:
		data = await self._execute_statement('SELECT phone_number FROM info WHERE unique_id = "' + unique_id + '";')
		if ('',) in data or () == data or (None,) in data:
			return False
		return True

	#TODO return success or failure
	async def _bind_account(self, unique_id: str, password: str, account: str, email: str, phone: str):
		await self._execute_statement('UPDATE `info` SET password = "' + password + '", account = "' + account + '", email = "' + email + '", phone_number = "' + phone + '" WHERE unique_id = "' + unique_id + '";')

	#TODO return success or failure
	async def _create_new_user(self, unique_id: str):
		await self._execute_statement('INSERT INTO info (unique_id) VALUES ("' + unique_id + '");')

	async def _check_exists(self, identifier: str, value: str) -> bool:
		if value == '':
			return True
		data = await self._execute_statement('SELECT * FROM info WHERE `' + identifier + '` = "' + value + '";')
		if () == data:
			return False
		return True

	async def _account_is_bound(self, unique_id: str) -> bool:
		data = await self._execute_statement('SELECT account FROM info WHERE unique_id = "' + unique_id + '";')
		if ('',) in data or () == data or (None,) in data:
			return False
		return True

	async def _register_token(self, unique_id: str, token: str) -> None:
		await self._execute_statement('UPDATE info SET token = "' + token + '" WHERE unique_id = "' + unique_id + '";')

	async def _get_prev_token(self, identifier: str, value: str) -> str:
		data = await self._execute_statement('SELECT token FROM info WHERE `' + identifier + '` = "' + value + '";')
		return data[0][0]

	def _is_valid_password(self, password: str) -> bool:
		return bool(self._password_re.match(password))

	def _is_valid_account(self, account: str) -> bool:
		return bool(self._account_re.match(account))

	def _is_valid_email(self, email: str) -> bool:
		return bool(self._email_re.match(email))

	def _is_valid_phone(self, phone: str) -> bool:
		return bool(self._phone_re.match(phone))

	async def _valid_credentials(self, identifier: str, value: str, password: str) -> bool:
		if not self._is_valid_password(password): return False
		if identifier == 'account':
			if not self._is_valid_account(value): return False
		elif identifier == 'email':
			if not self._is_valid_email(value): return False
		p = await self._execute_statement('SELECT password, salt FROM info WHERE `' + identifier + '` = "' + value + '";')
		if p == (): return False
		hashed_password, salt = p[0]
		input_hash = hashlib.scrypt(password.encode(), salt = salt.encode(), n = self._n, r = self._r, p = self._p).hex()
		return hashed_password == input_hash

	async def _request_new_token(self, unique_id: str, prev_token: str = ''):
		async with ClientSession() as session:
			async with session.post(TOKEN_SERVER_BASE_URL + '/issue_token', data = {'unique_id' : unique_id, 'prev_token' : prev_token}) as resp:
				return await resp.json(content_type = 'text/json')


	async def _get_unique_id(self, identifier: str, value: str) -> str:
		'''
		Returns unique_id associated with the identifier. None if identifier invalid.
		'''
		data = await self._execute_statement('SELECT unique_id FROM info WHERE `' + identifier + '` = "' + value + '";')
		if data == () or (None,) in data or ('',) in data:
			return ""
		return data[0][0]

	async def _connect_sql(self):
		self._pool = await aiomysql.create_pool(
				maxsize = 5,
				host = '192.168.1.102',
				user = 'root',
				password = 'lukseun',
				charset = 'utf8',
				db = 'user',
				autocommit = True)

	async def _execute_statement(self, statement: str) -> tuple:
		'''
		Executes the given statement and returns the result.
		'''
		if self._pool is None: await self._connect_sql()
		async with self._pool.acquire() as conn:
			async with conn.cursor() as cursor:
				await cursor.execute(statement)
				return await cursor.fetchall()

	def message_typesetting(self, status: int, message: str, data: dict={}) -> dict:
		return {'status' : status, 'message' : message, 'random' : random.randint(-1000, 1000), 'data' : data}

