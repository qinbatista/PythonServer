#
#
###############################################################################

import os
import time
import json
import random
import tormysql
import configparser
from aiohttp import web
from datetime import datetime, timedelta

CONFIG = configparser.ConfigParser()
CONFIG.read('./Configuration/server/1.0/server.conf')

JSON_NAME = './Configuration/client/1.0/stage_reward_config.json'



SKILL_ID_LIST = ["m1_level", "p1_level", "g1_level", "m11_level", "m12_level", "m13_level", "p11_level", "p12_level", "p13_level", "g11_level", "g12_level", "g13_level", "m111_level", "m112_level", "m113_level", "m121_level", "m122_level", "m123_level", "m131_level", "m132_level", "m133_level", "p111_level", "p112_level", "p113_level", "p121_level", "p122_level", "p123_level", "p131_level", "p132_level", "p133_level", "g111_level", "g112_level", "g113_level", "g121_level", "g122_level", "g123_level", "g131_level", "g132_level", "g133_level"]


format_sql = {
	"smallint": "%s",
	"varchar": "'%s'",
	"char": "'%s'"
}

class GameManager:
	def __init__(self):
		self._pools = [tormysql.ConnectionPool(max_connections = 10, host = '192.168.1.102', user = 'root', passwd = 'lukseun', db = 'aliya', charset = 'utf8')]

		self._reward_list = self._read_json_data()
		self._skill_scroll_functions = {'skill_scroll_10' : self.try_skill_scroll_10, 'skill_scroll_30' : self.try_skill_scroll_30, 'skill_scroll_100' : self.try_skill_scroll_100}
		self._upgrade_chance = {'skill_scroll_10' : 0.10, 'skill_scroll_30' : 0.30, 'skill_scroll_100' : 1}

		self._standard_iron_count = 20
		self._standard_segment_count = 30
		self._standard_reset_weapon_skill_coin_count = 100

		self._valid_passive_skills = {'passive_skill_1_level', 'passive_skill_2_level', 'passive_skill_3_level', 'passive_skill_4_level'}


#############################################################################
#						 Bag Module Functions								#
#############################################################################
	async def get_all_head(self, world: int, table: str) -> dict:
		"""
		Used to get information such as the title of the database
		用于获取数据库的标题等信息
		:return:返回所有数据库的标题等信息，json数据
		"""
		data = list(await self._execute_statement(world, "desc %s;" % table))
		return self._internal_format(0, data)

	async def get_all_material(self, world: int, unique_id: str) -> dict:
		"""
		Used to get all numeric or string information
		用于获取所有的数字或字符串信息
		:param unique_id: 用户的唯一标识
		:return:返回所有材料名对应的值，json数据
		"""
		data = await self._execute_statement(world, "SELECT * FROM player WHERE unique_id='" + str(unique_id) + "'")
		return self._internal_format(0, data[0])

	async def get_all_supplies(self, world: int, unique_id: str) -> dict:
		# success ===> 0
		data_tuple = (await self.get_all_head(world, table="player"))["remaining"]
		heads = []
		for col in data_tuple:
				heads.append(col[0])
		content = list((await self.get_all_material(world, unique_id=unique_id))["remaining"])
		heads.pop(0)
		content.pop(0)
		return self._message_typesetting(0, "get supplies success", {"keys": heads, "values": content})

	async def add_supplies(self, world: int, unique_id: str, supply: str, value: int):
		# success ===> 0
		if value <= 0: return self._message_typesetting(9, "not a positive number")
		data = await self._try_material(world, unique_id, supply, value)
		if data["status"] == 0:
				return self._message_typesetting(0, "success", {"keys": [supply], "values": [data["remaining"]]})
		return self._message_typesetting(1, "failure")

	async def level_up_scroll(self, world: int, unique_id: str, scroll_id: str) -> dict:
		# 0 success
		# 1 advanced reels are not upgradeable
		# 2 insufficient scroll
		# 3 unexpected parameter
		# 4 parameter error
		# 9 database operation error
		if scroll_id == "skill_scroll_100": return self._message_typesetting(1, "advanced reels are not upgradeable!")
		try:
			scroll_id_count = await self._get_material(world, unique_id, scroll_id)
			if int(scroll_id_count) < 3:
				return self._message_typesetting(2, "Insufficient scroll")
			elif scroll_id == "skill_scroll_10":
				dict1 = await self.try_skill_scroll_10(world, unique_id, -3)
				dict2 = await self.try_skill_scroll_30(world, unique_id, 1)
				if dict1["status"] == 1 or dict2["status"] == 1:
					return self._message_typesetting(9, "database operation error!")
				return self._message_typesetting(0, "level up scroll success!", {"keys": ["skill_scroll_10", "skill_scroll_30"], "values": [dict1["remaining"], dict2["remaining"]]})
			elif scroll_id == "skill_scroll_30":
				dict1 = await self.try_skill_scroll_30(world, unique_id, -3)
				dict2 = await self.try_skill_scroll_100(world, unique_id, 1)
				if dict1["status"] == 1 or dict2["status"] == 1:
					return self._message_typesetting(9, "database operation error!")
				return self._message_typesetting(0, "level up scroll success!", {"keys": ["skill_scroll_30", "skill_scroll_100"], "values": [dict1["remaining"], dict2["remaining"]]})
			else:
				return self._message_typesetting(3, message="unexpected parameter --> " + scroll_id)
		except:
			return self._message_typesetting(4, 'parameter error!')

	async def try_all_material(self, world: int, unique_id: str, stage: int) -> dict:
		sql_stage = await self._get_material(world, unique_id, "stage")
		if stage <= 0 or sql_stage + 1 < stage:
			return self._internal_format(status=9, remaining=0)  # abnormal data!
		material_dict = dict(self._reward_list[stage])
		if sql_stage + 1 == stage:  # 通过新关卡
			material_dict.update({"stage": 1})
		update_str, select_str = self._sql_str_operating(unique_id, material_dict)
		data = 1 - await self._execute_statement_update(world, update_str)  # 0, 1反转
		remaining = list(await self._execute_statement(world, select_str))  # 数据库设置后的值
		# 通过新关卡有关卡数据的返回，老关卡没有关卡数据的返回
		return self._internal_format(status=data, remaining=[material_dict, remaining[0]])  # 0 成功， 1 失败

	async def try_coin(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'coin', value)

	async def try_iron(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'iron', value)

	async def try_diamond(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'diamond', value)

	async def try_experience(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'experience', value)

	async def try_level(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'level', value)

	async def try_role(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'role', value)

	async def try_stage(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'stage', value)

	async def try_skill_scroll_10(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'skill_scroll_10', value)

	async def try_skill_scroll_30(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'skill_scroll_30', value)

	async def try_skill_scroll_100(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'skill_scroll_100', value)

	async def try_experience_potion(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'experience_potion', value)

	async def try_small_energy_potion(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'small_energy_potion', value)

#############################################################################
#						End Bag Module Functions							#
#############################################################################



#############################################################################
#						 Skill Module Functions								#
#############################################################################

	# TODO ensure SQL UPDATE statement succeeds
	# TODO error checking for valid skill_id?
	async def level_up_skill(self, world: int, unique_id: str, skill_id: str, scroll_id: str):
		# success ===> 0 and 1
		# 0 - upgrade success
		# 1 - upgrade unsuccessful
		# 2 - User does not have that skill
		# 3 - Invalid scroll id
		# 4 - User does not have enough scrolls
		# 9 - Skill already at max level
		skill_level = await self._get_skill_level(world, unique_id, skill_id)
		if skill_level == 0:
			return self._message_typesetting(2, 'User does not have that skill')
		elif skill_level >= 10:
			return self._message_typesetting(9, 'Skill already max level')
		elif scroll_id not in self._skill_scroll_functions.keys():
			return self._message_typesetting(3, 'Invalid scroll id')
		resp = await self._skill_scroll_functions[scroll_id](world, unique_id, -1)
		if resp['status'] == 1:
			return self._message_typesetting(4, 'User does not have enough scrolls')
		if not self._roll_for_upgrade(scroll_id):
			return self._message_typesetting(1, 'upgrade unsuccessful', {'keys' : [skill_id, scroll_id], 'values' : [skill_level, resp['remaining']]})
		await self._execute_statement(world, 'UPDATE skill SET `' + skill_id + '` = ' + str(skill_level + 1) + ' WHERE unique_id = "' + unique_id + '";')
		return self._message_typesetting(0, 'upgrade success', {'keys' : [skill_id, scroll_id], 'values' : [skill_level + 1, resp['remaining']]})



	async def get_all_skill_level(self, world: int, unique_id: str) -> dict:
		# success ===> 0
		# 0 - Success
		names = await self._execute_statement(world, 'DESCRIBE skill;')
		values = await self._execute_statement(world, 'SELECT * from skill WHERE unique_id = "' + str(unique_id) + '";')
		key_list = []
		value_list = []
		for num, val in enumerate(zip(names[1:], values[0][1:])):
			key_list.append(val[0][0])
			value_list.append(val[1])
		return self._message_typesetting(0, 'success', {"keys": key_list, "values": value_list})


	async def get_skill(self, world: int, unique_id: str, skill_id: str) -> dict:
		# success ===> 0
		# 0 - Success
		# 1 - invalid skill name
		try:
			level = await self._get_skill_level(world, unique_id, skill_id)
			return self._message_typesetting(0, 'success', {'keys': [skill_id], 'values': [level]})
		except:
			return self._message_typesetting(1, 'invalid skill name')

	async def try_unlock_skill(self, world: int, unique_id: str, skill_id: str) -> dict:
		# success ===> 0 and 1
		# 0 - success unlocked new skill
		# 1 - skill already unlocked
		# 2 - invalid skill name
		# json ===> {"status": status, "remaining": remaining} ===> status 0、1、2、3
		try:  # 0、1、2
			level = await self._get_skill_level(world, unique_id, skill_id)
			if level == 0 and await self._execute_statement_update(world, 'UPDATE skill SET `' + skill_id + '` = 1 WHERE unique_id = "' + unique_id + '";') == 1:
				return self._internal_format(0, 'success, new skill unlocked')
			return self._internal_format(1, 'Skill already unlocked')
		except:
			return self._internal_format(2, 'Invalid skill name')


#############################################################################
#						End Skill Module Functions							#
#############################################################################


#############################################################################
#						Weapon Module Functions								#
#############################################################################


	async def level_up_weapon(self, world: int, unique_id: str, weapon: str, iron: int) -> dict:
		# - 0 - Success
		# - 1 - User does not have that weapon
		# - 2 - Incoming materials are not upgraded enough
		# - 3 - Insufficient materials, upgrade failed
		# - 4 - Database operation error
		# - 9 - Weapon already max level
		if await self._get_weapon_star(world, unique_id, weapon) == 0:
			return self._message_typesetting(1, 'User does not have that weapon')
		row = await self._get_row_by_id(world, weapon, unique_id)
		if row[1] == 100:
			return self._message_typesetting(9, 'Weapon already max level')
		skill_upgrade_number = iron // self._standard_iron_count
		data_tuple = (await self.get_all_head(world, weapon))['remaining']
		head = [x[0] for x in data_tuple]
		level_count = head.index('weapon_level')
		point_count = head.index('skill_point')
		if (row[level_count] + skill_upgrade_number) > 100:
			skill_upgrade_number = 100 - row[level_count]
		row[level_count] += skill_upgrade_number
		row[point_count] += skill_upgrade_number

		if skill_upgrade_number == 0:
			return self._message_typesetting(2, 'Incoming materials are not upgraded enough')
		data = await self.try_iron(world, unique_id, -1 * skill_upgrade_number * self._standard_iron_count)
		if int(data['status']) == 1:
			return self._message_typesetting(3, 'Insufficient materials, upgrade failed')
		if await self._set_weapon_level_up_data(world, unique_id, weapon, row[level_count], row[point_count]) == 0:
			return self._message_typesetting(3, 'Database operation error')
		head[0] = 'weapon'
		row[0] = weapon
		head.append('iron')
		row.append(data['remaining'])
		return self._message_typesetting(0, 'success', {'keys' : head, 'values' : row })


	async def level_up_passive(self, world: int, unique_id: str, weapon: str, passive: str):
		# - 0 - Success
		# - 1 - User does not have that weapon
		# - 2 - Insufficient skill points, upgrade failed
		# - 3 - Database operation error
		# - 9 - Weapon already max level
		if await self._get_weapon_star(world, unique_id, weapon) == 0:
			return self._message_typesetting(1, "User does not have that weapon")
		if passive not in self._valid_passive_skills:
			return self._message_typesetting(9, "Passive skill does not exist")
		data_tuple = (await self.get_all_head(world, weapon))["remaining"]
		head = [x[0] for x in data_tuple]
		row = await self._get_row_by_id(world, weapon, unique_id)
		point_count = head.index("skill_point")
		passive_count = head.index(passive)
		if row[point_count] == 0:
			return self._message_typesetting(2, "Insufficient skill points, upgrade failed")
		row[point_count] -= 1
		row[passive_count] += 1
		if await self._set_passive_skill_level_up_data(world, unique_id, weapon, passive, row[passive_count], row[point_count]) == 0:
			return self._message_typesetting(3, "Database operation error")
		head[0] = "weapon"
		row[0] = weapon
		return self._message_typesetting(0, "success", {"keys": head, "values": row})

	async def level_up_weapon_star(self, world: int, unique_id: str, weapon: str) -> dict:
		# - 0 - Weapon upgrade success
		# - 2 - insufficient gold coins, upgrade failed
		# - 3 - database operation error!
		data_tuple = (await self.get_all_head(world, weapon))["remaining"]
		head = [x[0] for x in data_tuple]
		row = await self._get_row_by_id(world, weapon, unique_id)
		weapon_star = await self._get_weapon_star(world, unique_id, weapon)
		segment_count = self._standard_segment_count * (1 + weapon_star)  # 根据武器星数增加碎片的消耗数量

		if int(row[head.index("segment")]) < segment_count:
			return self._message_typesetting(2, "Insufficient segments, upgrade failed!")

		row[head.index("segment")] = int(row[head.index("segment")]) - segment_count
		weapon_star += 1
		code1 = await self._set_segment_by_id(world, unique_id, weapon, row[head.index("segment")])
		code2 = await self._set_weapon_star(world, unique_id, weapon, weapon_star)
		if code1 == 0 or code2 == 0:
			return self._message_typesetting(3, "Database operation error!")
		head[0] = "weapon"
		row[0] = weapon
		head.append("star")
		row.append(weapon_star)
		return self._message_typesetting(0, weapon + " upgrade success!", {"keys": head, "values": row})

	async def reset_weapon_skill_point(self, world: int, unique_id: str, weapon: str) -> dict:
		# - 0 - Success
		# - 1 - no weapon
		# - 2 - insufficient gold coins, upgrade failed
		# - 3 - database operation error!
		# - 9 - Weapon reset skill point success

		if await self._get_weapon_star(world, unique_id, weapon) == 0:
			return self._message_typesetting(1, "no weapon!")
		data = await self.try_coin(world, unique_id, -1 * self._standard_reset_weapon_skill_coin_count)
		if int(data["status"]) == 1:
			return self._message_typesetting(2, "Insufficient gold coins, upgrade failed")

		data_tuple = (await self.get_all_head(world, weapon))["remaining"]
		head = [x[0] for x in data_tuple]

		row = await self._get_row_by_id(world, weapon, unique_id)

		row[head.index("skill_point")] = row[head.index("weapon_level")]
		row[head.index("passive_skill_1_level")] = row[head.index("passive_skill_2_level")] = row[head.index("passive_skill_3_level")] = row[head.index("passive_skill_4_level")] = 0
		if await self._reset_skill_point(world, unique_id, weapon, row[head.index("skill_point")]) == 0:
			return self._message_typesetting(3, "Database operation error!")

		head[0] = "weapon"
		row[0] = weapon
		head.append("coin")
		row.append(data["remaining"])
		return self._message_typesetting(0, weapon + " reset skill point success!", {"keys": head, "values": row})

	# TODO CHECK FOR SPEED IMPROVEMENTS
	async def get_all_weapon(self, world: int, unique_id: str):
		# - 0 - gain success
		data_tuple = (await self.get_all_head(world, "weapon_bag"))["remaining"]
		col_name_list = [x[0] for x in data_tuple]
		weapons_stars_list = await self._get_weapon_bag(world, unique_id)
		# The 0 position stores the UNIQUE_ID, so the column header does not traverse the 0 position.
		# The 0 position obtained by the __get_weapon_attributes method below is also UNIQUE_ID.
		# So it will be replaced by the number of weapons stars.
		# 0位置存储unique_id，因此列标题不会遍历0位置。下面的__get_weapon_attributes方法获得的0位置也是unique_id，
		# 因此它将被武器星数替换。
		keys = []
		values = []
		for i in range(1, len(col_name_list)):
			attribute_list = await self._get_weapon_attributes(world, unique_id, col_name_list[i])
			keys.append(col_name_list[i])
			attribute_list[0] = weapons_stars_list[i]
			values.append(attribute_list)
		return self._message_typesetting(0, "gain success", {"keys": keys, "values": values})






#############################################################################
#						End Weapon Module Functions							#
#############################################################################










			####################################
			#          P R I V A T E		   #
			####################################

	async def _get_weapon_bag(self, world: int, unique_id: str):
		data = await self._execute_statement(world, 'SELECT * FROM weapon_bag WHERE unique_id = "' + unique_id + '";')
		return list(data[0])

	async def _get_weapon_attributes(self, world: int, unique_id: str, weapon: str):
		data = await self._execute_statement(world, 'SELECT * FROM `' + weapon + '` WHERE unique_id = "' + unique_id + '";')
		return list(data[0])

	async def _reset_skill_point(self, world: int, unique_id: str, weapon: str, skill_point: int):
		return await self._execute_statement_update(world, 'UPDATE `' + weapon + '` SET passive_skill_1_level=0, passive_skill_2_level=0, passive_skill_3_level=0, passive_skill_4_level=0, skill_point = "' + str(skill_point) + '" WHERE unique_id = "' + unique_id + '";')

	async def _set_weapon_star(self, world: int, unique_id: str, weapon: str, star: int):
		return await self._execute_statement_update(world, 'UPDATE weapon_bag SET ' + weapon + ' = "' + str(star) + '" WHERE unique_id = "' + unique_id + '";') 

	async def _set_segment_by_id(self, world: int, unique_id: str, weapon: str, segment: int):
		return await self._execute_statement_update(world, 'UPDATE `' + weapon + '` SET segment = "' + str(segment) + '" WHERE unique_id = "' + unique_id + '";')

	async def _get_weapon_star(self, world: int, unique_id: str, weapon: str) -> dict:
		data = await self._execute_statement(world, 'SELECT ' + weapon + ' FROM weapon_bag WHERE unique_id = "' + unique_id + '";')
		return int(data[0][0])

	async def _get_row_by_id(self, world: int, weapon: str, unique_id: str) -> dict:
		data = await self._execute_statement(world, 'SELECT * FROM `' + weapon + '` WHERE unique_id = "' + unique_id + '";')
		return list(data[0])

	async def _set_passive_skill_level_up_data(self, world: int, unique_id: str, weapon: str, passive: str, skill_level: int, skill_point: int) -> dict:
		return await self._execute_statement_update(world, 'UPDATE `' + weapon + '` SET ' + passive + ' = "' + str(skill_level) + '", skill_point = "' + str(skill_point) + '" WHERE unique_id = "' + unique_id + '";')

	async def _set_weapon_level_up_data(self, world: int, unique_id: str, weapon: str, weapon_level: int, skill_point: int) -> dict:
		return await self._execute_statement_update(world, 'UPDATE `' + weapon + '` SET weapon_level = "' + str(weapon_level) + '", skill_point = "' + str(skill_point) + '" WHERE unique_id = "' + unique_id + '";')


	async def _get_skill_level(self, world: int, unique_id: str, skill_id: str) -> dict:
		data = await self._execute_statement(world, 'SELECT ' + skill_id + ' FROM skill WHERE unique_id = "' + unique_id + '";')
		return int(data[0][0])


	def _roll_for_upgrade(self, scroll_id: str) -> bool:
		return random.random() < self._upgrade_chance[scroll_id]

	async def _try_material(self, world: int, unique_id: str, material: str, value: int) -> dict:
		"""
		Try to change the database information
		A status of 0 is a success and a 1 is a failure.
		Return json data format
		尝试更改数据库信息
		状态为0表示成功，1表示失败。
		返回json数据格式
		:param unique_id:用户唯一识别码
		:param key:材料名
		:param value: 改变的材料值，正数是加运算，负数是减运算，0是给值
		:return:返回数据格式为 {"status": status, "remaining": remaining}
		"""
		num = await self._get_material(world, unique_id, material)
		if value == 0: return self._internal_format(0, num)
		num += value
		if num < 0: return self._internal_format(1, num)
		if await self._update_material(world, unique_id, material, num) == 0:
			return self._internal_format(1, num)
		return self._internal_format(status=0, remaining=num)

	async def _get_material(self, world: int, unique_id: str, material: str) -> int or str:
		"""
		Used to get numeric or string information
		用于获取数字或字符串信息
		:param unique_id: 用户的唯一标识
		:param material:材料名
		:return:返回材料名对应的值
		"""
		data = await self._execute_statement(world, 'SELECT ' + material + ' FROM player WHERE unique_id="' + str(unique_id) + '";')
		return data[0][0]

	async def _update_material(self, world: int, unique_id: str, material: str, value: int) -> int:
		"""
		Used to set information such as numeric values
		用于设置数值等信息
		:param unique_id:用户唯一识别码
		:param material:材料名
		:param material_value:要设置的材料对应的值
		:return:返回是否更新成功的标识，1为成功，0为失败
		"""
		return await self._execute_statement_update(world, 'UPDATE player SET ' + material + '=' + str(value) + ' where unique_id="' + unique_id + '";')


	def _sql_str_operating(self, unique_id: str, material_dict: dict) -> (str, str):
		update_str = "UPDATE player SET "
		update_end_str = " where unique_id='%s'" % unique_id
		select_str = "SELECT "
		select_end_str = " FROM player WHERE unique_id='%s'" % unique_id
		for key in material_dict.keys():
			update_str += "%s=%s+%s, " % (key, key, material_dict[key])
			select_str += "%s, " % key
		update_str = update_str[: len(update_str) - 2] + update_end_str
		select_str = select_str[: len(select_str) - 2] + select_end_str
		return update_str, select_str

	async def _execute_statement(self, world: int, statement: str) -> tuple:
		"""
		Executes the given statement and returns the result.
		执行给定的语句并返回结果。
		:param statement: Mysql执行的语句
		:return: 返回执行后的二维元组表
		"""
		async with await self._pools[world].Connection() as conn:
			async with conn.cursor() as cursor:
				await cursor.execute(statement)
				data = cursor.fetchall()
				return data

	async def _execute_statement_update(self, world: int, statement: str) -> int:
		"""
		Execute the update or set statement and return the result.
		执行update或set语句并返回结果。
		:param statement: Mysql执行的语句
		:return: 返回update或者是set执行的结果
		"""
		async with await self._pools[world].Connection() as conn:
			async with conn.cursor() as cursor:
				return await cursor.execute(statement)


	def _internal_format(self, status: int, remaining: int or tuple or list) -> dict:
		"""
		Internal json formatted information
		内部json格式化信息
		:param status:状态标识0：成功，1：失败
		:param remaining:改变后的结果
		:return:json格式：{"status": status, "remaining": remaining}
		"""
		return {"status": status, "remaining": remaining}

	def _message_typesetting(self, status: int, message: str, data: dict = {}) -> dict:
		"""
		Format the information
		:param message:说明语句
		:param data:json数据
		:return:返回客户端需要的json数据
		"""
		return {"status": status, "message": message, "random": random.randint(-1000, 1000), "data": data}

	def _read_json_data(self) -> list:
		if os.path.exists(JSON_NAME):
			data_dict = json.load(open(JSON_NAME, encoding = 'utf-8'))
			return [v for v in data_dict.values()]
		return []



#############################################################################
#
#
#
#
#############################################################################

MANAGER = GameManager()  # we want to define a single instance of the class
ROUTES = web.RouteTableDef()


def _json_response(body: dict = "", **kwargs) -> web.Response:
	'''
	A simple wrapper for aiohttp.web.Response return value.
	'''
	kwargs['body'] = json.dumps(body or kwargs['kwargs']).encode('utf-8')
	kwargs['content_type'] = 'text/json'
	return web.Response(**kwargs)


@ROUTES.post('/get_all_head')
async def __get_all_head(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.get_all_head(int(post['world']), post['table'])
	return _json_response(result)

@ROUTES.post('/get_all_material')
async def __get_all_material(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.get_all_material(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/get_all_supplies')
async def __get_all_supplies(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.get_all_supplies(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/add_supplies')
async def __add_supplies(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.add_supplies(int(post['world']), post['unique_id'], post['supply'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/level_up_scroll')
async def __level_up_scroll(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.level_up_scroll(int(post['world']), post['unique_id'], post['scroll_id'])
	return _json_response(result)

@ROUTES.post('/try_all_material')
async def __try_all_material(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_all_material(int(post['world']), post['unique_id'], int(post['stage']))
	return _json_response(result)

@ROUTES.post('/try_coin')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_coin(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_iron')
async def __try_iron(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_iron(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_diamond')
async def __try_diamond(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_diamond(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_experience')
async def __try_experience(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_experience(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_level')
async def __try_level(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_level(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_role')
async def __try_role(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_role(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_stage')
async def __try_stage(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_stage(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_skill_scroll_10')
async def __try_skill_scroll_10(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_skill_scroll_10(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_skill_scroll_30')
async def __try_skill_scroll_30(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_skill_scroll_30(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_skill_scroll_100')
async def __try_skill_scroll_100(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_skill_scroll_100(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_experience_potion')
async def __try_experience_potion(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_experience_potion(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_small_energy_potion')
async def __try_small_energy_potion(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_small_energy_potion(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/level_up_skill')
async def __level_up_skill(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.level_up_skill(int(post['world']), post['unique_id'], post['skill_id'], post['scroll_id'])
	return _json_response(result)

@ROUTES.post('/get_all_skill_level')
async def __get_all_skill_level(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.get_all_skill_level(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/get_skill')
async def __get_skill(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.get_skill(int(post['world']), post['unique_id'], post['skill_id'])
	return _json_response(result)

@ROUTES.post('/try_unlock_skill')
async def __try_unlock_skill(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_unlock_skill(int(post['world']), post['unique_id'], post['skill_id'])
	return _json_response(result)

@ROUTES.post('/level_up_weapon')
async def __level_up_weapon(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.level_up_weapon(int(post['world']), post['unique_id'], post['weapon'], int(post['iron']))
	return _json_response(result)

@ROUTES.post('/level_up_passive')
async def __level_up_passive(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.level_up_passive(int(post['world']), post['unique_id'], post['weapon'], post['passive'])
	return _json_response(result)


@ROUTES.post('/level_up_weapon_star')
async def __level_up_weapon_star(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.level_up_weapon_star(int(post['world']), post['unique_id'], post['weapon'])
	return _json_response(result)

@ROUTES.post('/reset_weapon_skill_point')
async def __reset_weapon_skill_point(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.reset_weapon_skill_point(int(post['world']), post['unique_id'], post['weapon'])
	return _json_response(result)

@ROUTES.post('/get_all_weapon')
async def __get_all_weapon(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.get_all_weapon(int(post['world']), post['unique_id'])
	return _json_response(result)



def run():
	print('REMINDER: NEED TO READ PORT FROM CONFIG FILE')
	print('REMINDER: NEED TO READ WEAPON_COST_INFO FROM CONFIG FILE')
	print('REMINDER: NEED TO READ VALID PASSIVE SKILLS FROM CONFIG FILE')
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port=8004)


if __name__ == '__main__':
	run()
