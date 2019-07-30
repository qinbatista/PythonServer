


import pymysql
import asyncio
import unittest
import requests
import lukseun_client

db = pymysql.connect('192.168.1.102', 'root', 'lukseun', 'user')
cursor = db.cursor()
cursor.execute('DELETE FROM info WHERE unique_id = "bindme";')
db.commit()

resp = requests.post('http://localhost:8005/login_unique', data = {'unique_id' : 'bindme'})
TOKEN = resp.json()['data']['token']




class TestAccountManager(unittest.TestCase):
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
		self.cursor.execute('DELETE FROM info WHERE unique_id = "testtest";')
		self.cursor.execute('DELETE FROM info WHERE account = "keepokappa";')
		self.cursor.execute('DELETE FROM info WHERE email = "email@domain.com";')
		self.cursor.execute('DELETE FROM info WHERE phone_number = "18186691566";')
		self.cursor.execute('INSERT INTO info (unique_id) VALUES ("testtest");')
		self.db.commit()
		r = requests.post('http://localhost:8005/bind_account', data = {'unique_id' : 'testtest', 'account' : 'keepokappa', 'password' : 'secretpass', 'email' : '', 'phone_number' :''})
		msg = {'function' : 'login', 'data' : {'identifier' : 'account', 'value' : 'keepokappa', 'password' : 'secretpass'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)

	def test_login_email(self):
		self.cursor.execute('DELETE FROM info WHERE unique_id = "testtest";')
		self.cursor.execute('DELETE FROM info WHERE account = "keepokappa";')
		self.cursor.execute('DELETE FROM info WHERE email = "email@domain.com";')
		self.cursor.execute('DELETE FROM info WHERE phone_number = "18186691566";')
		self.cursor.execute('INSERT INTO info (unique_id) VALUES ("testtest");')
		self.db.commit()
		r = requests.post('http://localhost:8005/bind_account', data = {'unique_id' : 'testtest', 'account' : 'keepokappa', 'password' : 'secretpass', 'email' : 'email@domain.com', 'phone_number' :''})
		msg = {'function' : 'login', 'data' : {'identifier' : 'email', 'value' : 'email@domain.com', 'password' : 'secretpass'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)

	def test_login_phone_number(self):
		self.cursor.execute('DELETE FROM info WHERE unique_id = "testtest";')
		self.cursor.execute('DELETE FROM info WHERE account = "keepokappa";')
		self.cursor.execute('DELETE FROM info WHERE email = "email@domain.com";')
		self.cursor.execute('DELETE FROM info WHERE phone_number = "18186691566";')
		self.cursor.execute('INSERT INTO info (unique_id) VALUES ("testtest");')
		self.db.commit()
		r = requests.post('http://localhost:8005/bind_account', data = {'unique_id' : 'testtest', 'account' : 'keepokappa', 'password' : 'secretpass', 'email' : '', 'phone_number' :'18186691566'})
		msg = {'function' : 'login', 'data' : {'identifier' : 'phone_number', 'value' : '18186691566', 'password' : 'secretpass'}}

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

	def test_cannot_login_null(self):
		msg = {'function' : 'login', 'data' : {'identifier' : 'account', 'value' : '', 'password' : ''}}
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

	def test_can_bind_account(self):
		self.cursor.execute('DELETE FROM info WHERE account = "alreadyexists";')
		self.cursor.execute('DELETE FROM info WHERE email = "alreadyexists";')
		self.cursor.execute('DELETE FROM info WHERE phone_number = "18186691566";')
		self.cursor.execute('UPDATE info SET account = "", password = "", email = "", phone_number = "" WHERE unique_id = "bindme";')
		self.db.commit()
		msg = {'function' : 'bind_account', 'data' : {'token' : TOKEN, 'password' : 'passpass', 'account' : 'alreadyexists', 'email' : 'email@domain.com', 'phone_number' : '18186691566'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)

	def test_cannot_bind_account_already_exist(self):
		self.cursor.execute('DELETE FROM info WHERE email = "email" AND unique_id != "bindme";')
		self.cursor.execute('DELETE FROM info WHERE phone_number = "888" AND unique_id != "bindme";')
		self.cursor.execute('INSERT INTO info (unique_id, account) VALUES ("dummy", "alreadyexists");')
		self.cursor.execute('UPDATE info SET account = "", password = "", email = "", phone_number = "" WHERE unique_id = "bindme";')
		self.db.commit()
		msg = {'function' : 'bind_account', 'data' : {'token' : TOKEN, 'password' : 'passpass', 'account' : 'alreadyexists', 'email' : 'email@domain.com', 'phone_number' : '888'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.cursor.execute('DELETE FROM info WHERE unique_id = "dummy";')
		self.db.commit()
		self.assertEqual(response['status'], 5)

	def test_cannot_bind_email_already_exists(self):
		self.cursor.execute('DELETE FROM info WHERE account = "alreadyexists" AND unique_id != "bindme";')
		self.cursor.execute('DELETE FROM info WHERE email = "alreadyexists" AND unique_id != "bindme";')
		self.cursor.execute('DELETE FROM info WHERE phone_number = "888" AND unique_id != "bindme";')
		self.cursor.execute('UPDATE info SET account = "", password = "", email = "alreadyexists@domain.com", phone_number = "" WHERE unique_id = "bindme";')
		self.db.commit()
		msg = {'function' : 'bind_account', 'data' : {'token' : TOKEN, 'password' : 'passpass', 'account' : 'alreadyexists', 'email' : 'alreadyexists@domain.com', 'phone_number' : '888'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 6)


	def test_cannot_bind_phone_number_already_exists(self):
		self.cursor.execute('DELETE FROM info WHERE account = "alreadyexists" AND unique_id != "bindme";')
		self.cursor.execute('DELETE FROM info WHERE email = "alreadyexists" AND unique_id != "bindme";')
		self.cursor.execute('DELETE FROM info WHERE phone_number = "888" AND unique_id != "bindme";')
		self.cursor.execute('UPDATE info SET account = "", password = "", email = "", phone_number = "888" WHERE unique_id = "bindme";')
		self.db.commit()
		msg = {'function' : 'bind_account', 'data' : {'token' : TOKEN, 'password' : 'passpass', 'account' : 'alreadyexists', 'email' : 'email@domain.com', 'phone_number' : '888'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 7)





if __name__ == '__main__':
	unittest.main(verbosity = 2)
