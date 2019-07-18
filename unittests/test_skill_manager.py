

import pymysql
import unittest
import subprocess


class TestSkillManager(unittest.TestCase):
	def setUp(self):
		self.db = pymysql.connect('192.168.1.102', 'root', 'lukseun', 'aliya')
		self.cursor = self.db.cursor()

	def test_can_level_up_skill(self):
		self.cursor.execute('UPDATE player SET skill_scroll_100 = 10 WHERE unique_id = "4";')
		self.db.commit()
		resp = subprocess.Popen("curl -d 'unique_id=4&skill_id=m1_level&scroll_id=skill_scroll_100' -X POST localhost:8010/level_up_skill", shell=True, stdout=subprocess.PIPE).stdout
		d = eval(resp.read().decode())
		self.assertEqual(d['status'], 0)
		self.assertEqual(d['data']['upgrade'], 0)
		self.assertEqual(d['data']['item1'][0], 'skill_scroll_100')
		self.assertEqual(d['data']['item1'][1], 9)

	def test_can_not_level_up_skill_do_not_have(self):
		self.cursor.execute('UPDATE skill SET m131_level = 0 WHERE unique_id = "4";')
		self.db.commit()
		resp = subprocess.Popen("curl -d 'unique_id=4&skill_id=m131_level&scroll_id=skill_scroll_100' -X POST localhost:8010/level_up_skill", shell=True, stdout=subprocess.PIPE).stdout
		d = eval(resp.read().decode())
		self.assertEqual(d['status'], 1)

	def test_can_not_level_up_skill_without_scroll(self):
		self.cursor.execute('UPDATE skill SET m131_level = 1 WHERE unique_id = "4";')
		self.cursor.execute('UPDATE player SET skill_scroll_30 = 0 WHERE unique_id = "4";')
		self.db.commit()
		resp = subprocess.Popen("curl -d 'unique_id=4&skill_id=m131_level&scroll_id=skill_scroll_30' -X POST localhost:8010/level_up_skill", shell=True, stdout=subprocess.PIPE).stdout
		d = eval(resp.read().decode())
		self.assertEqual(d['status'], 4)

	def test_can_not_level_up_skill_at_max_level(self):
		self.cursor.execute('UPDATE skill SET m131_level = 10 WHERE unique_id = "4";')
		self.cursor.execute('UPDATE player SET skill_scroll_30 = 1 WHERE unique_id = "4";')
		self.db.commit()
		resp = subprocess.Popen("curl -d 'unique_id=4&skill_id=m131_level&scroll_id=skill_scroll_30' -X POST localhost:8010/level_up_skill", shell=True, stdout=subprocess.PIPE).stdout
		d = eval(resp.read().decode())
		self.assertEqual(d['status'], 9)

	def test_can_get_all_skill(self):
		resp = subprocess.Popen("curl -d 'unique_id=4' -X POST localhost:8010/get_all_skill_level", shell=True, stdout=subprocess.PIPE).stdout
		d = eval(resp.read().decode())
		self.assertEqual(d['status'], 0)
		self.assertEqual(len(d['data']), 39)

	def test_can_get_skill(self):
		resp = subprocess.Popen("curl -d 'unique_id=4&skill_id=m1_level' -X POST localhost:8010/get_skill", shell=True, stdout=subprocess.PIPE).stdout
		d = eval(resp.read().decode())
		self.assertEqual(d['status'], 0)
		self.assertEqual(d['data']['skill1'][0], 'm1_level')


	def test_can_not_get_skill_invalid_skill_id(self):
		resp = subprocess.Popen("curl -d 'unique_id=4&skill_id=m1_lskfljlsdevel' -X POST localhost:8010/get_skill", shell=True, stdout=subprocess.PIPE).stdout
		d = eval(resp.read().decode())
		self.assertEqual(d['status'], 1)




if __name__ == '__main__':
	unittest.main(verbosity = 2)
