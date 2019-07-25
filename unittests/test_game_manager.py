

import sys
sys.path.insert(0, '..')

import pymysql
import asyncio
import unittest
import requests
import lukseun_client

resp = requests.post('http://localhost:8005/login_unique', data = {'unique_id' : '4'})
TOKEN = resp.json()['data']['token']

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



	
	def test_can_get_all_head(self):
		pass

	def test_can_get_all_material(self):
		pass

	def test_can_get_all_supplies(self):
		pass

	def test_can_add_supplies(self):
		pass

	def test_cannot_add_negative_supplies(self):
		# status 9
		pass

	def test_can_level_up_scroll(self):
		pass

	def test_cannot_level_up_scroll_without_scroll(self):
		# status 2
		pass

	def test_cannot_level_up_scroll_advanced_scroll(self):
		# status 1
		pass

	def test_cannot_level_up_scroll_invalid_scroll_name(self):
		# status 4
		pass

	def test_can_try_all_material(self):
		pass

	def test_cannot_try_all_material_invalid_stage(self):
		# status 9
		pass

# TODO should be duplicated for all material types
	def test_can_try_coin_check(self):
		pass

# TODO should be duplicated for all material types
	def test_can_try_coin_add(self):
		pass

# TODO should be duplicated for all material types
	def test_can_try_coin_subtract(self):
		pass

# TODO should be duplicated for all material types
	def test_cannot_try_coin_subtract_insufficient(self):
		# status 1
		pass

	def test_can_level_up_skill(self):
		pass

	def test_cannot_level_up_skill_without_having_skill(self):
		# status 2
		pass

	def test_cannot_level_up_skill_invalid_scroll_id(self):
		#status 3
		pass

	def test_cannot_level_up_skill_not_enough_scrolls(self):
		# status 4
		pass

	def test_cannot_level_up_skill_already_max_level(self):
		# status 9
		pass

	def test_can_get_all_skill_level(self):
		pass

	def test_can_get_skill(self):
		pass

	def test_cannot_get_skill_invalid_skill_name(self):
		#status 1
		pass

	def test_can_try_unlock_skill(self):
		pass

	def test_can_try_unlock_skill_already_unlocked(self):
		#status 1
		pass

	def test_cannot_try_unlock_skill_invalid_name(self):
		#status 2
		pass
	
	def test_can_level_up_weapon(self):
		pass

	def test_cannot_level_up_weapon_without_having(self):
		#status 1
		pass

	def test_cannot_level_up_weapon_incoming_material_too_low(self):
		# status 2
		pass

	def test_cannot_level_up_weapon_insufficient_materials(self):
		#status 3
		pass

	def test_cannot_level_up_weapon_already_max_level(self):
		#status 9
		pass

	def test_can_level_up_passive(self):
		pass

	def test_cannot_level_up_passive_without_having_weapon(self):
		# status 1
		pass

	def test_cannot_level_up_passive_insufficient_skill_point(self):
		# status 2
		pass

	def test_cannot_level_up_passive_skill_doesnt_exist(self):
		# status 9
		pass

	def test_can_level_up_weapon_star(self):
		pass

	def test_cannot_level_up_weapon_star_insufficient_material(self):
		# status 2
		pass

	def test_can_reset_weapon_skill_point(self):
		pass

	def test_cannot_reset_weapon_skill_point_for_weapon_dont_have(self):
		# status 1
		pass

	def test_cannot_reset_weapon_skill_point_insufficient_material(self):
		# status 2
		pass

	def test_can_get_all_weapon(self):
		pass

	def test_can_try_unlock_weapon(self):
		pass

	def test_can_try_unlock_weapon_already_exists(self):
		# status 1
		pass

	def test_cannot_try_unlock_weapon_dont_have(self):
		# status 2
		pass

	def test_can_pass_stage(self):
		pass

	def test_cannot_pass_stage_abnormal_data(self):
		# status 9
		pass

	def test_can_random_gift_skill(self):
		pass

	def test_cannot_random_gift_skill_invalid_skill_name(self):
		# status 2
		pass

	def test_can_random_gift_segment(self):
		pass

	def test_cannot_random_gift_segment_weapon_dont_have(self):
		# status 2
		pass










if __name__ == '__main__':
	unittest.main(verbosity = 2)
