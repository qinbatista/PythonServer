

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
		self.db = pymysql.connect('192.168.1.102', 'root', 'lukseun', 'aliya')
		self.cursor = self.db.cursor()

	
	def test_can_get_all_head(self):
		msg = {'world' : '0', 'function' : 'get_all_head', 'data' : {'token' : TOKEN, 'table' : 'player'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)

	def test_can_get_all_material(self):
		msg = {'world' : '0', 'function' : 'get_all_material', 'data' : {'token' : TOKEN}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)

	def test_can_get_all_supplies(self):
		msg = {'world' : '0', 'function' : 'get_all_supplies', 'data' : {'token' : TOKEN}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)

	def test_can_add_supplies(self):
		self.cursor.execute('UPDATE player SET iron = "0" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'add_supplies', 'data' : {'token' : TOKEN, 'supply' : 'iron', 'value' : '100'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)
		self.assertEqual(response['data']['keys'][0], 'iron')
		self.assertEqual(int(response['data']['values'][0]), 100)


	def test_cannot_add_negative_supplies(self):
		msg = {'world' : '0', 'function' : 'add_supplies', 'data' : {'token' : TOKEN, 'supply' : 'iron', 'value' : '-100'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 9)

	def test_can_level_up_scroll(self):
		self.cursor.execute('UPDATE player SET skill_scroll_10 = "40", skill_scroll_30 = "0" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'level_up_scroll', 'data' : {'token' : TOKEN, 'scroll_id' : 'skill_scroll_10'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)
		self.assertEqual(response['data']['keys'], ['skill_scroll_10', 'skill_scroll_30'])
		self.assertEqual(response['data']['values'], [37, 1])

	def test_cannot_level_up_scroll_without_scroll(self):
		self.cursor.execute('UPDATE player SET skill_scroll_10 = "0" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'level_up_scroll', 'data' : {'token' : TOKEN, 'scroll_id' : 'skill_scroll_10'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 2)

	def test_cannot_level_up_scroll_advanced_scroll(self):
		self.cursor.execute('UPDATE player SET skill_scroll_100 = "10" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'level_up_scroll', 'data' : {'token' : TOKEN, 'scroll_id' : 'skill_scroll_100'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_cannot_level_up_scroll_invalid_scroll_name(self):
		msg = {'world' : '0', 'function' : 'level_up_scroll', 'data' : {'token' : TOKEN, 'scroll_id' : 'invalid_scroll_name'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 4)

	def test_can_try_all_material(self):
		msg = {'world' : '0', 'function' : 'try_all_material', 'data' : {'token' : TOKEN, 'stage' : '4'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)

	def test_cannot_try_all_material_invalid_stage(self):
		msg = {'world' : '0', 'function' : 'try_all_material', 'data' : {'token' : TOKEN, 'stage' : '-4'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 9)

	def test_can_try_coin_check(self):
		self.cursor.execute('UPDATE player SET coin = "1000" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'try_coin', 'data' : {'token' : TOKEN, 'value' : '0'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)
		self.assertEqual(int(response['remaining']), 1000)

	def test_can_try_coin_add(self):
		self.cursor.execute('UPDATE player SET coin = "1000" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'try_coin', 'data' : {'token' : TOKEN, 'value' : '100'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)
		self.assertEqual(int(response['remaining']), 1100)

	def test_can_try_coin_subtract(self):
		self.cursor.execute('UPDATE player SET coin = "1000" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'try_coin', 'data' : {'token' : TOKEN, 'value' : '-100'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)
		self.assertEqual(int(response['remaining']), 900)

	def test_cannot_try_coin_subtract_insufficient(self):
		self.cursor.execute('UPDATE player SET coin = "1000" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'try_coin', 'data' : {'token' : TOKEN, 'value' : '-2000'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_can_level_up_skill(self):
		self.cursor.execute('UPDATE skill SET m1_level = "1" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE player SET skill_scroll_100 = "1" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'level_up_skill', 'data' : {'token' : TOKEN, 'skill_id' : 'm1_level', 'scroll_id' : 'skill_scroll_100'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)
		self.assertEqual(response['data']['keys'], ['m1_level', 'skill_scroll_100'])
		self.assertEqual(response['data']['values'], [2, 0])

	def test_cannot_level_up_skill_without_having_skill(self):
		self.cursor.execute('UPDATE skill SET m1_level = "0" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE player SET skill_scroll_100 = "1" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'level_up_skill', 'data' : {'token' : TOKEN, 'skill_id' : 'm1_level', 'scroll_id' : 'skill_scroll_100'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 2)

	def test_cannot_level_up_skill_invalid_scroll_id(self):
		self.cursor.execute('UPDATE skill SET m1_level = "1" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'level_up_skill', 'data' : {'token' : TOKEN, 'skill_id' : 'm1_level', 'scroll_id' : 'skill_scroll_1'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 3)

	def test_cannot_level_up_skill_not_enough_scrolls(self):
		self.cursor.execute('UPDATE skill SET m1_level = "1" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE player SET skill_scroll_100 = "0" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'level_up_skill', 'data' : {'token' : TOKEN, 'skill_id' : 'm1_level', 'scroll_id' : 'skill_scroll_100'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 4)

	def test_cannot_level_up_skill_already_max_level(self):
		self.cursor.execute('UPDATE skill SET m1_level = "10" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE player SET skill_scroll_100 = "1" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'level_up_skill', 'data' : {'token' : TOKEN, 'skill_id' : 'm1_level', 'scroll_id' : 'skill_scroll_100'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 9)

	def test_can_get_all_skill_level(self):
		msg = {'world' : '0', 'function' : 'get_all_skill_level', 'data' : {'token' : TOKEN}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)

	def test_can_get_skill(self):
		self.cursor.execute('UPDATE skill SET m1_level = "10" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'get_skill', 'data' : {'token' : TOKEN, 'skill_id' : 'm1_level'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)
		self.assertEqual(response['data']['keys'], ['m1_level'])
		self.assertEqual(response['data']['values'], [10])

	def test_cannot_get_skill_invalid_skill_name(self):
		msg = {'world' : '0', 'function' : 'get_skill', 'data' : {'token' : TOKEN, 'skill_id' : 'invalid skill name'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_can_try_unlock_skill(self):
		self.cursor.execute('UPDATE skill SET m1_level = "0" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'try_unlock_skill', 'data' : {'token' : TOKEN, 'skill_id' : 'm1_level'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)

	def test_can_try_unlock_skill_already_unlocked(self):
		self.cursor.execute('UPDATE skill SET m1_level = "1" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'try_unlock_skill', 'data' : {'token' : TOKEN, 'skill_id' : 'm1_level'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_cannot_try_unlock_skill_invalid_name(self):
		msg = {'world' : '0', 'function' : 'try_unlock_skill', 'data' : {'token' : TOKEN, 'skill_id' : 'invalid skill name here'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 2)
	
	def test_can_level_up_weapon(self):
		self.cursor.execute('UPDATE weapon_bag SET weapon1 = "1" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE player SET iron = "1000" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET weapon_level = "10" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'level_up_weapon', 'data' : {'token' : TOKEN, 'weapon' : 'weapon1', 'iron' : '60'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)
		self.assertEqual(response['data']['values'][0], 'weapon1')
		self.assertEqual(int(response['data']['values'][1]), 13)
		self.assertEqual(int(response['data']['values'][-1]), 940)

	def test_cannot_level_up_weapon_without_having(self):
		self.cursor.execute('UPDATE weapon_bag SET weapon1 = "0" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE player SET iron = "1000" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET weapon_level = "10" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'level_up_weapon', 'data' : {'token' : TOKEN, 'weapon' : 'weapon1', 'iron' : '60'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)


	def test_cannot_level_up_weapon_incoming_material_too_low(self):
		self.cursor.execute('UPDATE weapon_bag SET weapon1 = "1" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE player SET iron = "1000" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET weapon_level = "10" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'level_up_weapon', 'data' : {'token' : TOKEN, 'weapon' : 'weapon1', 'iron' : '0'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 2)

	def test_cannot_level_up_weapon_insufficient_materials(self):
		self.cursor.execute('UPDATE weapon_bag SET weapon1 = "1" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE player SET iron = "0" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET weapon_level = "10" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'level_up_weapon', 'data' : {'token' : TOKEN, 'weapon' : 'weapon1', 'iron' : '60'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 3)

	def test_cannot_level_up_weapon_already_max_level(self):
		self.cursor.execute('UPDATE weapon_bag SET weapon1 = "1" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE player SET iron = "1000" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET weapon_level = "100" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'level_up_weapon', 'data' : {'token' : TOKEN, 'weapon' : 'weapon1', 'iron' : '60'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 9)

	def test_can_level_up_passive(self):
		self.cursor.execute('UPDATE weapon_bag SET weapon1 = "1" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET skill_point = "10" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET passive_skill_1_level = "2" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'level_up_passive', 'data' : {'token' : TOKEN, 'weapon' : 'weapon1', 'passive' : 'passive_skill_1_level'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)
		self.assertEqual(response['data']['values'][0], 'weapon1')
		self.assertEqual(int(response['data']['values'][2]), 3)
		self.assertEqual(int(response['data']['values'][6]), 9)

	def test_cannot_level_up_passive_without_having_weapon(self):
		self.cursor.execute('UPDATE weapon_bag SET weapon1 = "0" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET skill_point = "10" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET passive_skill_1_level = "2" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'level_up_passive', 'data' : {'token' : TOKEN, 'weapon' : 'weapon1', 'passive' : 'passive_skill_1_level'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_cannot_level_up_passive_insufficient_skill_point(self):
		self.cursor.execute('UPDATE weapon_bag SET weapon1 = "1" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET skill_point = "0" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET passive_skill_1_level = "2" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'level_up_passive', 'data' : {'token' : TOKEN, 'weapon' : 'weapon1', 'passive' : 'passive_skill_1_level'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 2)

	def test_cannot_level_up_passive_skill_doesnt_exist(self):
		msg = {'world' : '0', 'function' : 'level_up_passive', 'data' : {'token' : TOKEN, 'weapon' : 'weapon1', 'passive' : 'doesnt exist passive skill'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 9)

	def test_can_level_up_weapon_star(self):
		self.cursor.execute('UPDATE weapon_bag SET weapon1 = "1" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET segment = "100" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'level_up_weapon_star', 'data' : {'token' : TOKEN, 'weapon' : 'weapon1'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)
		self.assertEqual(int(response['data']['values'][-1]), 2)
		self.assertEqual(int(response['data']['values'][7]), 40)

	def test_cannot_level_up_weapon_star_insufficient_material(self):
		self.cursor.execute('UPDATE weapon_bag SET weapon1 = "1" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET segment = "0" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'level_up_weapon_star', 'data' : {'token' : TOKEN, 'weapon' : 'weapon1'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 2)

	def test_can_reset_weapon_skill_point(self):
		self.cursor.execute('UPDATE weapon_bag SET weapon1 = "1" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET weapon_level = "10" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET passive_skill_1_level = "2" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET passive_skill_2_level = "2" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET passive_skill_3_level = "2" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET passive_skill_4_level = "2" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET skill_point = "2" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE player SET coin = "1000" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'reset_weapon_skill_point', 'data' : {'token' : TOKEN, 'weapon' : 'weapon1'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)
		self.assertEqual(int(response['data']['values'][-1]), 900)
		self.assertEqual(int(response['data']['values'][2]), 0)
		self.assertEqual(int(response['data']['values'][3]), 0)
		self.assertEqual(int(response['data']['values'][4]), 0)
		self.assertEqual(int(response['data']['values'][5]), 0)
		self.assertEqual(int(response['data']['values'][6]), 10)

	def test_cannot_reset_weapon_skill_point_for_weapon_dont_have(self):
		self.cursor.execute('UPDATE weapon_bag SET weapon1 = "0" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET skill_point = "10" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET passive_skill_1_level = "2" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET passive_skill_2_level = "2" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET passive_skill_3_level = "2" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET passive_skill_4_level = "2" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE player SET coin = "1000" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'reset_weapon_skill_point', 'data' : {'token' : TOKEN, 'weapon' : 'weapon1'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_cannot_reset_weapon_skill_point_insufficient_material(self):
		self.cursor.execute('UPDATE weapon_bag SET weapon1 = "1" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET skill_point = "10" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET passive_skill_1_level = "2" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET passive_skill_2_level = "2" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET passive_skill_3_level = "2" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE weapon1 SET passive_skill_4_level = "2" WHERE unique_id = "4";')
		self.cursor.execute('UPDATE player SET coin = "0" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'reset_weapon_skill_point', 'data' : {'token' : TOKEN, 'weapon' : 'weapon1'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 2)

	def test_can_get_all_weapon(self):
		msg = {'world' : '0', 'function' : 'get_all_weapon', 'data' : {'token' : TOKEN}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)

	def test_can_try_unlock_weapon(self):
		self.cursor.execute('UPDATE weapon_bag SET weapon2 = "0" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'try_unlock_weapon', 'data' : {'token' : TOKEN, 'weapon' : 'weapon2'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)

	def test_can_try_unlock_weapon_already_exists(self):
		self.cursor.execute('UPDATE weapon_bag SET weapon2 = "1" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'try_unlock_weapon', 'data' : {'token' : TOKEN, 'weapon' : 'weapon2'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 1)

	def test_cannot_try_unlock_invalid_weapon(self):
		msg = {'world' : '0', 'function' : 'try_unlock_weapon', 'data' : {'token' : TOKEN, 'weapon' : 'invalid weapon name'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 2)

	def test_can_pass_stage(self):
		self.cursor.execute('UPDATE player SET stage = "7" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'pass_stage', 'data' : {'token' : TOKEN, 'stage' : '5'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 0)

	def test_cannot_pass_stage_abnormal_data(self):
		msg = {'world' : '0', 'function' : 'pass_stage', 'data' : {'token' : TOKEN, 'stage' : '-5'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 9)

	def test_can_basic_summon(self):
		self.cursor.execute('UPDATE player SET diamond = "100" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'basic_summon', 'data' : {'token' : TOKEN, 'cost_item' : 'diamond'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertTrue(response['status'] == 0 or response['status'] == 1)

	def test_cannot_basic_summon_insufficient_material(self):
		self.cursor.execute('UPDATE player SET diamond = "0" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'basic_summon', 'data' : {'token' : TOKEN, 'cost_item' : 'diamond'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 4)

	def test_cannot_basic_summon_invalid_cost_item(self):
		self.cursor.execute('UPDATE player SET diamond = "100" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'basic_summon', 'data' : {'token' : TOKEN, 'cost_item' : 'invalid cost item'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 5)

	def test_can_pro_summon(self):
		self.cursor.execute('UPDATE player SET diamond = "100" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'pro_summon', 'data' : {'token' : TOKEN, 'cost_item' : 'diamond'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertTrue(response['status'] == 0 or response['status'] == 1)

	def test_cannot_pro_summon_insufficient_material(self):
		self.cursor.execute('UPDATE player SET diamond = "0" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'pro_summon', 'data' : {'token' : TOKEN, 'cost_item' : 'diamond'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 4)

	def test_cannot_pro_summon_invalid_cost_item(self):
		self.cursor.execute('UPDATE player SET diamond = "100" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'pro_summon', 'data' : {'token' : TOKEN, 'cost_item' : 'invalid cost item'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 5)

	def test_can_friend_summon(self):
		self.cursor.execute('UPDATE player SET diamond = "100" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'friend_summon', 'data' : {'token' : TOKEN, 'cost_item' : 'diamond'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertTrue(response['status'] == 0 or response['status'] == 1)

	def test_cannot_friend_summon_insufficient_material(self):
		self.cursor.execute('UPDATE player SET diamond = "0" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'friend_summon', 'data' : {'token' : TOKEN, 'cost_item' : 'diamond'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 4)

	def test_cannot_friend_summon_invalid_cost_item(self):
		self.cursor.execute('UPDATE player SET diamond = "100" WHERE unique_id = "4";')
		self.db.commit()
		msg = {'world' : '0', 'function' : 'friend_summon', 'data' : {'token' : TOKEN, 'cost_item' : 'invalid cost item'}}
		response = asyncio.get_event_loop().run_until_complete(self.c.send_message(str(msg).replace("'", "\"")))
		self.assertEqual(response['status'], 5)










if __name__ == '__main__':
	unittest.main(verbosity = 2)
