

import sys
sys.path.insert(0, '..')

import pymysql
import asyncio
import unittest
import lukseun_client



# This function runs upon importing this module. It fetches a token to be used for all requests made here
msg = {'function' : 'login_unique', 'data' : {'unique_id' : '4'}}
response = asyncio.get_event_loop().run_until_complete(lukseun_client.LukseunClient('aliya', '127.0.0.1', port = 8880).send_message(str(msg).replace("'", "\"")))
TOKEN = response['data']['token']

class TestPlayerStateMethods(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		super(TestWeaponMethods, cls).setUpClass()
		cls.db = pymysql.connect('192.168.1.102', 'root', 'lukseun', 'aliya')
		cls.c = lukseun_client.LukseunClient('aliya', '127.0.0.1', port = 8880)
		cls.token = TOKEN



	def test_can_level_up_skill(self):
		pass

	def test_can_not_level_up_skill_invalid_skill_id(self):
		msg = {'function' : 'skill_level_up', 'data' : {'token' : self.token, 'skill_id' : 'invalid skill id', 'scroll_id' : 'scroll_skill_10'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_can_not_level_up_skill_doesnt_have(self):
		cursor = self.db.cursor()
		cursor.execute('UPDATE skill SET m12_level = "0" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'function' : 'skill_level_up', 'data' : {'token' : self.token, 'skill_id' : 'm12_level', 'scroll_id' : 'scroll_skill_10'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_can_not_level_up_skill_invalid_scroll_id(self):
		msg = {'function' : 'skill_level_up', 'data' : {'token' : self.token, 'skill_id' : 'm12_level', 'scroll_id' : 'invalid scroll id'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 2)


	def test_can_not_level_up_skill_must_have_enough_scrolls(self):
		pass

	def test_can_not_level_up_skill_already_max(self):
		pass

	def test_can_get_all_skill_level(self):
		msg = {'function' : 'get_all_skill_level', 'data' : {'token' : self.token}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)
		self.assertEqual(len(response['data']), 39)


	def test_can_get_single_skill(self):
		cursor = self.db.cursor()
		cursor.execute('UPDATE skill SET m1_level = "3" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'function' : 'get_skill', 'data' : {'token' : self.token, 'skill_id' : 'm1_level'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)
		self.assertEqual(response['data']['skill1'][0], 3)


	def test_can_not_get_single_skill_that_doesnt_exist(self):
		msg = {'function' : 'get_skill', 'data' : {'token' : self.token, 'skill_id' : 'invalid skill id'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)


	def test_can_level_up_scroll(self):
		pass

	def test_must_have_enough_scrolls(self):
		pass

	def test_can_get_all_supplies(self):
		pass




if __name__ == '__main__':
	unittest.main(verbosity = 2)
