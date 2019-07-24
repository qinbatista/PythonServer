

import sys
sys.path.insert(0, '..')

import pymysql
import asyncio
import unittest
import lukseun_client


class TestGameManager(unittest.TestCase):
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



if __name__ == '__main__':
	unittest.main(verbosity = 2)
