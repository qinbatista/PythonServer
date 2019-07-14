

import sys
sys.path.insert(0, '..')

import pymysql
import asyncio
import unittest
import lukseun_client


class TestLoginMethods(unittest.TestCase):
	def setUp(self):
		self.c = lukseun_client.LukseunClient('aliya', '127.0.0.1', port = 8880)


	def test_login_unique(self):
		msg = {'function' : 'login_unique', 'data' : {'unique_id' : 'mac'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)

	def test_login_unique_already_bound(self):
		msg = {'function' : 'login_unique', 'data' : {'unique_id' : '1'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 2)

	def test_login_unique_new_account(self):
		db = pymysql.connect('192.168.1.102', 'root', 'lukseun', 'aliya')
		cursor = db.cursor()
		cursor.execute('DELETE FROM userinfo WHERE unique_id = "new_user";')
		db.commit()
		msg = {'function' : 'login_unique', 'data' : {'unique_id' : 'new_user'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_login_account(self):
		msg = {'function' : 'login', 'data' : {'identifier' : 'account', 'value' : 'childrensucks', 'password' : 'keepo'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)

	def test_login_email(self):
		msg = {'function' : 'login', 'data' : {'identifier' : 'email', 'value' : 'matt@gmail.com', 'password' : 'keepo'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)

	def test_login_phone_number(self):
		msg = {'function' : 'login', 'data' : {'identifier' : 'phone_number', 'value' : '222', 'password' : 'keepo'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)

	def test_login_invalid_account(self):
		msg = {'function' : 'login', 'data' : {'identifier' : 'account', 'value' : 'doesntexist', 'password' : 'keepo'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_login_invalid_email(self):
		msg = {'function' : 'login', 'data' : {'identifier' : 'email', 'value' : 'doesntexist', 'password' : 'keepo'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_login_invalid_phone_number(self):
		msg = {'function' : 'login', 'data' : {'identifier' : 'phone_number', 'value' : 'doesntexist', 'password' : 'keepo'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_login_invalid_password_account(self):
		msg = {'function' : 'login', 'data' : {'identifier' : 'account', 'value' : 'childrensucks', 'password' : 'muahaha'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_login_invalid_password_email(self):
		msg = {'function' : 'login', 'data' : {'identifier' : 'email', 'value' : 'matt@gmail.com', 'password' : 'muahaha'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_login_invalid_password_phone_number(self):
		msg = {'function' : 'login', 'data' : {'identifier' : 'phone_number', 'value' : '222', 'password' : 'muahaha'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)



if __name__ == '__main__':
	unittest.main(verbosity = 2)
