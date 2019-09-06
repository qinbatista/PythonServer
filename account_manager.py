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
import tormysql
import requests
import configparser
from aiohttp import web
from aiohttp import ClientSession


TOKEN_SERVER_BASE_URL = 'http://127.0.0.1:8001'

# Part (1 / 2)
class AccountManager:
	def __init__(self):
		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive.
		self._pool = tormysql.ConnectionPool(max_connections=10, host='192.168.1.102', user='root', passwd='lukseun', db='user', charset='utf8')
		self._password_re = re.compile(r'\A[\w!@#$%^&*()_+|`~=\-\\\[\]:;\'\"{}/?,.<>]{6,30}\Z')
		self._account_re = re.compile(r'^[A-Za-z]\w{5,24}$')
		self._email_re = re.compile(r'^s*([A-Za-z0-9_-]+(.\w+)*@(\w+.)+\w{2,5})s*$')
		self._phone_re = re.compile(r'\A[0-9]{10,15}\Z')
		self._n = 2**10
		self._r = 8
		self._p = 1


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

	# TODO run check_exists as a task
	# TODO refactor code for speed improvements
	async def bind_account(self, unique_id: str, password: str, account: str, email: str, phone: str) -> dict:
		if await self._account_is_bound(unique_id): # trying to bind additional items
			if email == '' and phone == '':
				return self.message_typesetting(9, 'could not bind additional items')
			if email != '':
				retvals = await asyncio.gather(self._email_is_bound(unique_id), self._check_exists('email', email))
				if retvals[0]:
					return self.message_typesetting(8, 'email already bound')
				if retvals[1]:
					return self.message_typesetting(6, 'email already exists')
				if not self._is_valid_email(email):
					return self.message_typesetting(2, 'invalid email')

			if phone != '':
				retvals = await asyncio.gather(self._phone_is_bound(unique_id), self._check_exists('phone_number', phone))
				if retvals[0]:
					return self.message_typesetting(9, 'phone already bound')
				if retvals[1]:
					return self.message_typesetting(4, 'phone already exists')
				if not self._is_valid_phone(phone):
					return self.message_typesetting(3, 'invalid phone')

			if email != '':
				await self._execute_statement('UPDATE info SET email = "' + email + '" WHERE unique_id = "' + unique_id + '";')
			if phone != '':
				await self._execute_statement('UPDATE info SET phone_number = "' + phone + '" WHERE unique_id = "' + unique_id + '";')

		else: # trying to bind for the first time
			retvals = await asyncio.gather(self._check_exists('account', account), self._check_exists('email', email), self._check_exists('phone_number', phone))
			if not self._is_valid_account(account):
				return self.message_typesetting(1, 'invalid account name')
			if retvals[0]:
				return self.message_typesetting(5, 'account already exists')
			if not self._is_valid_password(password):
				return self.message_typesetting(4, 'invalid password')
			
			if email != '':
				if retvals[1]:
					return self.message_typesetting(6, 'email already exists')
				if not self._is_valid_email(email):
					return self.message_typesetting(2, 'invalid email')

			if phone != '':
				if retvals[2]:
					return self.message_typesetting(7, 'phone already exists')
				if not self._is_valid_phone(phone):
					return self.message_typesetting(3, 'invalid phone')


			random_salt = str(secrets.randbits(256))
			if len(random_salt) % 2 != 0:
				random_salt = '0' + random_salt
			hashed_password = hashlib.scrypt(password.encode(), salt=random_salt.encode(), n = self._n, r = self._r, p = self._p).hex()
			await self._execute_statement('UPDATE info SET account = "' + account + '", password = "' + hashed_password + '", salt = "' + random_salt + '" WHERE unique_id = "' + unique_id + '";')

			if email != '':
				await self._execute_statement('UPDATE info SET email = "' + email + '" WHERE unique_id = "' + unique_id + '";')
			if phone != '':
				await self._execute_statement('UPDATE info SET phone_number = "' + phone + '" WHERE unique_id = "' + unique_id + '";')
		return self.message_typesetting(0, 'success')






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

	async def _execute_statement(self, statement: str) -> tuple:
		'''
		Executes the given statement and returns the result.
		'''
		async with await self._pool.Connection() as conn:
			async with conn.cursor() as cursor:
				await cursor.execute(statement)
				data = cursor.fetchall()
				return data

	def message_typesetting(self, status: int, message: str, data: dict={}) -> dict:
		return {'status' : status, 'message' : message, 'random' : random.randint(-1000, 1000), 'data' : data}

