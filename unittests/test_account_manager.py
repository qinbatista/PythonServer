

import sys
sys.path.insert(0, '..')

import pymysql
import asyncio
import unittest
import lukseun_client


class TestLoginMethods(unittest.TestCase):
	def setUp(self):
		self.c = lukseun_client.LukseunClient('aliya', '127.0.0.1', port = 8880)
		self.db = pymysql.connect('192.168.1.102', 'root', 'lukseun', 'user')
		self.cursor = self.db.cursor()


	def test_login_unique_new_account(self):
		self.cursor.execute('DELETE FROM info WHERE unique_id = "new_user";')
		self.db.commit()
		msg = {'function' : 'login_unique', 'data' : {'unique_id' : 'new_user'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_login_existing_unique(self):
		self.cursor.execute('DELETE FROM info WHERE unique_id = "existing";')
		self.cursor.execute('INSERT INTO info (unique_id) VALUES ("existing");')
		self.db.commit()
		msg = {'function' : 'login_unique', 'data' : {'unique_id' : 'existing'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)

	def test_cannot_login_unique_already_bound(self):
		self.cursor.execute('DELETE FROM info WHERE unique_id = "alreadybound";')
		self.cursor.execute('INSERT INTO info (unique_id, account) VALUES ("alreadybound", "accountname");')
		self.db.commit()
		msg = {'function' : 'login_unique', 'data' : {'unique_id' : 'alreadybound'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 2)

	def test_login_account(self):
		self.cursor.execute('DELETE FROM info WHERE unique_id = "test";')
		self.cursor.execute('INSERT INTO info (unique_id, password, account) VALUES ("test", "pass", "test");')
		self.db.commit()
		msg = {'function' : 'login', 'data' : {'identifier' : 'account', 'value' : 'test', 'password' : 'pass'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)

	def test_login_email(self):
		self.cursor.execute('DELETE FROM info WHERE unique_id = "test";')
		self.cursor.execute('INSERT INTO info (unique_id, password, email) VALUES ("test", "pass", "email");')
		self.db.commit()
		msg = {'function' : 'login', 'data' : {'identifier' : 'email', 'value' : 'email', 'password' : 'pass'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)

	def test_login_phone_number(self):
		self.cursor.execute('DELETE FROM info WHERE unique_id = "test";')
		self.cursor.execute('INSERT INTO info (unique_id, password, phone_number) VALUES ("test", "pass", "888");')
		self.db.commit()
		msg = {'function' : 'login', 'data' : {'identifier' : 'phone_number', 'value' : '888', 'password' : 'pass'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)

	def test_cannot_login_invalid_account(self):
		self.cursor.execute('DELETE FROM info WHERE account = "doesntexist";')
		self.db.commit()
		msg = {'function' : 'login', 'data' : {'identifier' : 'account', 'value' : 'doesntexist', 'password' : 'pass'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_cannot_login_invalid_email(self):
		self.cursor.execute('DELETE FROM info WHERE email = "doesntexist";')
		self.db.commit()
		msg = {'function' : 'login', 'data' : {'identifier' : 'email', 'value' : 'doesntexist', 'password' : 'keepo'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_cannot_login_invalid_phone_number(self):
		self.cursor.execute('DELETE FROM info WHERE phone_number = "doesntexist";')
		self.db.commit()
		msg = {'function' : 'login', 'data' : {'identifier' : 'phone_number', 'value' : 'doesntexist', 'password' : 'keepo'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_cannot_login_invalid_password_account(self):
		self.cursor.execute('DELETE FROM info WHERE unique_id = "test";')
		self.cursor.execute('INSERT INTO info (unique_id, password, account) VALUES ("test", "pass", "test");')
		self.db.commit()
		msg = {'function' : 'login', 'data' : {'identifier' : 'account', 'value' : 'test', 'password' : 'wrongpassword'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_cannot_login_invalid_password_email(self):
		self.cursor.execute('DELETE FROM info WHERE unique_id = "test";')
		self.cursor.execute('INSERT INTO info (unique_id, password, email) VALUES ("test", "pass", "email");')
		self.db.commit()
		msg = {'function' : 'login', 'data' : {'identifier' : 'email', 'value' : 'email', 'password' : 'wrongpassword'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_cannot_login_invalid_password_phone_number(self):
		self.cursor.execute('DELETE FROM info WHERE unique_id = "test";')
		self.cursor.execute('INSERT INTO info (unique_id, password, phone_number) VALUES ("test", "pass", "888");')
		self.db.commit()
		msg = {'function' : 'login', 'data' : {'identifier' : 'phone_number', 'value' : '888', 'password' : 'wrongpassword'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)



if __name__ == '__main__':
	unittest.main(verbosity = 2)
