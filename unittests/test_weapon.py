

import sys
sys.path.insert(0, '..')

import pymysql
import asyncio
import unittest
import lukseun_client


class TestWeaponMethods(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		super(TestWeaponMethods, cls).setUpClass()
		cls.db = pymysql.connect('192.168.1.102', 'root', 'lukseun', 'aliya')
		cls.c = lukseun_client.LukseunClient('aliya', '127.0.0.1', port = 8880)
		msg = {'function' : 'login_unique', 'data' : {'unique_id' : '4'}}

		response = asyncio.get_event_loop().run_until_complete(cls.c.send_message(str(msg).replace("'", "\"")))
		cls.token = response['data']['token']


	def test_must_be_logged_in(self):
		msg = {'function' : 'level_up_weapon', 'data' : {'token' : 'muahaah', 'weapon' : 'weapon1', 'iron' : '20'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 11)
		self.assertEqual(response['data']['bad_token'], 'muahaah')

	def test_must_have_valid_message_format(self):
		msg = {'function' : 'level_up_weapon', 'data' : {'weapon' : 'weapon1', 'iron' : '20'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 10)


	def test_can_level_up_weapon_once(self):
		cursor = self.db.cursor()
		cursor.execute('UPDATE weapon1 SET weapon_level = "5" WHERE unique_id = "4";')
		cursor.execute('UPDATE bag SET iron = "1000" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'function' : 'level_up_weapon', 'data' : {'token' : self.token, 'weapon' : 'weapon1', 'iron' : '20'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)
		self.assertEqual(response['data']['weapon_bag1'][1], 6)
		self.assertEqual(response['data']['item1'][1], 980)


	def test_can_level_up_weapon_multiple_times(self):
		cursor = self.db.cursor()
		cursor.execute('UPDATE weapon1 SET weapon_level = "5" WHERE unique_id = "4";')
		cursor.execute('UPDATE bag SET iron = "1000" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'function' : 'level_up_weapon', 'data' : {'token' : self.token, 'weapon' : 'weapon1', 'iron' : '200'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)
		self.assertEqual(response['data']['weapon_bag1'][1], 15)
		self.assertEqual(response['data']['item1'][1], 800)
	
	def test_can_level_up_to_max(self):
		cursor = self.db.cursor()
		cursor.execute('UPDATE weapon1 SET weapon_level = "1" WHERE unique_id = "4";')
		cursor.execute('UPDATE bag SET iron = "3000" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'function' : 'level_up_weapon', 'data' : {'token' : self.token, 'weapon' : 'weapon1', 'iron' : '3000'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)
		self.assertEqual(response['data']['weapon_bag1'][1], 100)
		self.assertEqual(response['data']['item1'][1], 1020)



	def test_must_have_weapon(self):
		msg = {'function' : 'level_up_weapon', 'data' : {'token' : self.token, 'weapon' : 'weapon2', 'iron' : '20'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_cannot_level_up_past_max(self):
		cursor = self.db.cursor()
		cursor.execute('UPDATE weapon1 SET weapon_level = "100" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'function' : 'level_up_weapon', 'data' : {'token' : self.token, 'weapon' : 'weapon1', 'iron' : '20'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 9)


	def test_must_have_upgrade_materials(self):
		cursor = self.db.cursor()
		cursor.execute('UPDATE weapon1 SET weapon_level = "10" WHERE unique_id = "4";')
		cursor.execute('UPDATE bag SET iron = "19" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'function' : 'level_up_weapon', 'data' : {'token' : self.token, 'weapon' : 'weapon1', 'iron' : '20'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 2)

	
	def test_can_not_level_up_passive_of_weapon_dont_own(self):
		msg = {'function' : 'level_up_passive', 'data' : {'token' : self.token, 'weapon' : 'weapon2', 'passive' : 'passive_skill_1_level'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	
	def test_can_level_up_passive(self):
		cursor = self.db.cursor()
		cursor.execute('UPDATE weapon1 SET passive_skill_1_level = "3" WHERE unique_id = "4";')
		cursor.execute('UPDATE weapon1 SET skill_point = "300" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'function' : 'level_up_passive', 'data' : {'token' : self.token, 'weapon' : 'weapon1', 'passive' : 'passive_skill_1_level'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)
		self.assertEqual(response['data']['weapon_bag1'][2], 4)
		self.assertEqual(response['data']['weapon_bag1'][6], 299)
	
	def test_can_not_level_up_passive_without_skill_point(self):
		cursor = self.db.cursor()
		cursor.execute('UPDATE weapon1 SET skill_point = "0" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'function' : 'level_up_passive', 'data' : {'token' : self.token, 'weapon' : 'weapon1', 'passive' : 'passive_skill_1_level'}}

		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 2)












if __name__ == '__main__':
	unittest.main(verbosity = 2)
