#
#
###############################################################################

import os
import time
import json
import random
import tormysql
import requests
import threading
import configparser
from aiohttp import web
from datetime import datetime, timedelta



class GameManager:
	def __init__(self):
		self._pools = [tormysql.ConnectionPool(max_connections = 10, host = '192.168.1.102', user = 'root', passwd = 'lukseun', db = 'aliya', charset = 'utf8')]
		self._refresh_configuration()
		self._start_timer(600)



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

	# TODO rename function - it is private and only called by pass_stage function
	async def try_pass_stage(self, world: int, unique_id: str, stage: int) -> dict:
		stage_data = self._stage_reward["stage"]
		sql_stage = await self._get_material(world, unique_id, "stage")
		if stage <= 0 or sql_stage + 1 < stage:
			return self._internal_format(status=9, remaining=0)  # abnormal data!
		material_dict = {}
		for key, value in stage_data[str(stage)].items():
			material_dict.update({key: value})
		if sql_stage + 1 == stage:  # 通过新关卡
			material_dict.update({"stage": 1})
		update_str, select_str = self._sql_str_operating(unique_id, material_dict)
		data = 1 - await self._execute_statement_update(world, update_str)  # 0, 1反转
		remaining = list(await self._execute_statement(world, select_str))  # 数据库设置后的值
		# 通过新关卡有关卡数据的返回，老关卡没有关卡数据的返回
		return self._internal_format(status=data, remaining=[material_dict, remaining[0]])  # 0 成功， 1 失败

	async def try_energy(self, world: int, unique_id: str, amount: int) -> dict:
		# amount > 0 硬增加能量
		# amount == 0 自动恢复能量
		# amount < 0 消耗能量
		# success ===> 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7
		# - 0 - 购买能量成功 === Purchase energy successfully
		# - 1 - 购买能量成功，能量未恢复满 === Purchase energy successfully, energy is not fully restored
		# - 2 - 获取能量成功 === Get energy successfully
		# - 3 - 能量已消耗，能量值及恢复时间更新成功 === Energy has been consumed, energy value and recovery time updated successfully
		# - 4 - 能量已完全恢复，能量更新成功 === Energy has been fully restored, successful energy update
		# - 5 - 能量尚未完全恢复，能量更新成功 === Energy has not fully recovered, successful energy update
		# - 6 - 能量刷新后已消耗，能量值及恢复时间更新成功 === After refreshing the energy, the energy value and recovery time are successfully updated.
		# - 7 - 能量已刷新，未恢复满，已消耗能量，能量值及恢复时间更新成功 === Energy has been refreshed, not fully recovered, energy has been consumed, energy value and recovery time updated successfully
		# - 8 - 参数错误 === Parameter error
		# - 9 - 无足够能量消耗 === Not enough energy consumption
		# - 10 - 数据库操作错误 === Database operation error
		full_energy=self._player["energy"]["max_energy"]
		if amount > 0:
			data = (await self._decrease_energy(world, unique_id, 0))["data"]
			json_data = await self._try_material(world, unique_id, "energy", amount)
			if int(json_data["status"]) == 1:
				return self._message_typesetting(10, "Database operation error")
			elif int(json_data["remaining"] >= full_energy):
				sql_str = "UPDATE player SET recover_time = '' WHERE unique_id = '%s';" % unique_id
				await self._execute_statement_update(world, sql_str)
				for i in range(len(data["keys"])):
					if data["keys"][i] == "energy":
						data["values"][i] = json_data["remaining"]
					if data["keys"][i] == "recover_time":
						data["values"][i] = ""
					if data["keys"][i] == "cooling_time":
						data["values"][i] = -1
				return self._message_typesetting(0, "Purchase energy successfully", data)
			else:
				for i in range(len(data["keys"])):
					if data["keys"][i] == "energy":
						data["values"][i] = json_data["remaining"]
				return self._message_typesetting(1, "Purchase energy successfully, energy is not fully restored", data)
		elif full_energy + amount < 0:
			return self._message_typesetting(8, "Parameter error")
		else:
			return await self._decrease_energy(world, unique_id, abs(amount))

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
		elif scroll_id not in self._skill_scroll_functions:
			return self._message_typesetting(3, 'Invalid scroll id')
		resp = await eval('self.try_' + scroll_id + '(world, unique_id, -1)')
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
		# - 9 - Passive skill does not exist
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
		# - 2 - insufficient segment, upgrade failed
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

	
	# TODO INTERNAL USE only?????
	async def try_unlock_weapon(self, world: int, unique_id: str, weapon: str) -> dict:
		# - 0 - Unlocked new weapon!   ===> {"keys": ["weapon"], "values": [weapon]}
		# - 1 - Weapon already unlocked, got free segment   ===>  {"keys": ['weapon', 'segment'], "values": [weapon, segment]}
		# - 2 - no weapon!
		try:
			star = await self._get_weapon_star(world, unique_id, weapon)
			if star != 0:
				segment = await self._get_segment(world, unique_id, weapon) + 30
				await self._set_segment_by_id(world, unique_id, weapon, segment)
				return self._message_typesetting(1, 'Weapon already unlocked, got free segment!', {"keys": ['weapon', 'star', 'segment'], "values": [weapon, star, segment]})
			await self._set_weapon_star(world, unique_id, weapon, 1)
			return self._message_typesetting(0, 'Unlocked new weapon!', {"keys": ["weapon", 'star', 'segment'], "values": [weapon, 1, 0]})
		except:
			return self._message_typesetting(2, 'no weapon!')

	async def try_unlock_role(self, world: int, unique_id: str, role: str) -> dict:
		# - 0 - Unlocked new role!   ===> {"keys": ["role"], "values": [role]}
		# - 1 - Role already unlocked, got free segment   ===>  {"keys": ['role', 'segment'], "values": [role, segment]}
		# - 2 - no role!
		star = await self._get_role_star(world, unique_id, role)
		if star != 0:
			segment = await self._get_role_segment(world, unique_id, role) + 30
			await self._set_role_segment_by_id(world, unique_id, role, segment)
			return self._message_typesetting(1, 'Role already unlocked, got free segment', {'keys' : ['role', 'star', 'segment'], 'values' : [role, star, segment]})
		await self._set_role_star(world, unique_id, role, 1)
		return self._message_typesetting(0, 'Unlocked new role!', {'keys' : ['role', 'star', 'segment'], 'values' : [role, 1, 0]})

	async def disintegrate_weapon(self, world: int, unique_id: str, weapon: str) -> dict:
		# 0 - successful weapon decomposition
		# 1 - User does not have that weapon
		# 2 - insufficient diamond
		# 3 - self._player is not updated
		# 4 - database operation error
		cost = self._player["disintegrate_weapon"]["cost"]  # cost is dict
		reward = self._player["disintegrate_weapon"]["reward"]  # dict
		weapon_tier = [
			self._player["disintegrate_weapon"]["weapontier1"],
			self._player["disintegrate_weapon"]["weapontier2"],
			self._player["disintegrate_weapon"]["weapontier3"],
			self._player["disintegrate_weapon"]["weapontier4"]
		]  # list
		star = await self._get_weapon_star(world=world, unique_id=unique_id, weapon=weapon)
		if star == 0:
			return self._message_typesetting(status=1, message="User does not have this weapon")
		#  能分解武器的情况下再扣钻石
		diamond_data = await self.try_diamond(world=world, unique_id=unique_id, value=-1*int(cost["diamond"]))
		if int(diamond_data["status"]) == 1:
			return self._message_typesetting(status=2, message="Insufficient diamond")
		reward_weapon_name = weapon
		for i in range(len(weapon_tier)):
			if weapon in weapon_tier[i]:
				key = random.randint(0, len(weapon_tier[i]) - 1)
				print("weapon: %s, weapon_tier[i][key]: %s" % (weapon, weapon_tier[i][key]))
				while weapon == weapon_tier[i][key]:
					key = random.randint(0, len(weapon_tier[i]) - 1)
				reward_weapon_name = weapon_tier[i][key]  # 增加武器碎片的武器
				break
		if weapon == reward_weapon_name:
			return self._message_typesetting(status=3, message="self._player not updated")
		#  数据库操作
		star_code = await self._set_weapon_star(world=world, unique_id=unique_id, weapon=weapon, star=0)  # 武器星数至0

		reward_weapon_segment = star * int(reward["segment"])  # 计算奖励武器的碎片数量
		#  构造更新语句和查询语句
		update_str = "update %s set segment=segment+%s where unique_id='%s'" % (reward_weapon_name, reward_weapon_segment, unique_id)
		select_str = "select segment from %s where unique_id='%s'" % (reward_weapon_name, unique_id)
		update_code = await self._execute_statement_update(world=world, statement=update_str)

		select_result = await self._execute_statement(world=world, statement=select_str)  # 获取含有碎片的查询的结果
		coin_data = await self.try_coin(world=world, unique_id=unique_id, value=int(reward["coin"])) # 获取添加金币之后的金币数量
		if star_code == 0 or update_code == 0 or int(coin_data["status"]) == 1:
			return self._message_typesetting(status=4, message="database operating error ==> update_code: %s, star_code: %s, json_status: %s" % (update_code, star_code, coin_data["status"]))
		data = {
			"remaing": {
				"cost_weapon_name": weapon,  # 武器分解的名字
				"cost_weapon_star": 0,  # 武器分解之后的星数
				"coin": coin_data["remaining"],  # player表中金币的剩余数量
				"diamond": diamond_data["remaining"],  # player表中钻石的剩余数量
				"reward_weapon_name": reward_weapon_name,  # 奖励碎片的武器名字
				"reward_weapon_segment": select_result[0][0]  # 碎片的剩余数量
			},
			"reward": {
				"coin": reward["coin"],  # 分解武器奖励的金币
				"reward_weapon_name": reward_weapon_name,  # 奖励碎片的武器名字
				"reward_weapon_segment": reward_weapon_segment  # 奖励碎片的数量
			}
		}
		return self._message_typesetting(status=0, message="Successful weapon decomposition", data=data)




#############################################################################
#						End Weapon Module Functions							#
#############################################################################








#############################################################################
#						Stage Module Functions								#
#############################################################################

	# TODO CHECK SPEED IMPROVEMENTS
	async def enter_stage(self, world: int, unique_id: str, stage: int) -> dict:
		# 0 - success
		# 97 - database operation error
		# 98 - key insufficient
		# 99 - parameter error
		enter_stage_data = self._entry_consumables["stage"]
		if stage <= 0 or stage > int(await self._get_material(world,  unique_id, "stage")):
			return self._message_typesetting(99, "Parameter error")
		keys = list(enter_stage_data[str(stage)].keys())
		values = [-v for v in list(enter_stage_data[str(stage)].values())]
		material_dict = {}
		for i in range(len(keys)):
			material_dict.update({keys[i]: values[i]})

		update_str, select_str = self._sql_str_operating(unique_id, material_dict)
		select_values = (await self._execute_statement(world, select_str))[0]
		for i in range(len(select_values)):
			values[i] = int(values[i]) + int(select_values[i])
			if values[i] < 0:
				return self._message_typesetting(98, "%s insufficient" % keys[i])

		if await self._execute_statement_update(world, update_str) == 0:
			return self._message_typesetting(status=97, message="database operating error")
		return self._message_typesetting(0, "success", {"keys": keys, "values": values})

	async def pass_stage(self, world: int, unique_id: str, stage: int, customs_clearance_time: str) -> dict:
		# success ===> 0
		# 0 : passed customs ===> success
		# 1 : database operation error
		# 9 : abnormal data!
		json_data = await self.try_pass_stage(world, unique_id, stage)
		status = int(json_data["status"])
		if status == 9:
			return self._message_typesetting(9, "abnormal data!")
		elif status == 1:
			return self._message_typesetting(1, "database operation error")
		else:
			material_dict = json_data["remaining"][0]
			data = {"keys": list(material_dict.keys()), "values": json_data["remaining"][1], "rewards": list(material_dict.values())}
			return self._message_typesetting(0, "passed customs!", data)


	async def start_hang_up(self, world: int, unique_id: str, stage: int) -> dict:
		"""
		success ===> 0 , 1
		# 0 - hang up success
		# 1 - Repeated hang up successfully
		# 2 - database operating error
		# 9 - Parameter error
		1分钟奖励有可能奖励1颗钻石，30颗金币，10个铁
		minute = 1 ==> reward 0 or 1 diamond and 30 coin and 10 iron
		minute = 2 ==> reward 0 or 1 or 2 diamond and 60 coin and 20 iron
		"""
		if stage <= 0 or stage > int(await self._get_material(world=world,  unique_id=unique_id, material="stage")):
			return self._message_typesetting(status=9, message="Parameter error")
		sql_str = "SELECT hang_up_time,hang_stage FROM player WHERE unique_id='%s'" % unique_id
		key_list = await self._execute_statement(world=world, statement=sql_str)
		hang_up_time, hang_stage = key_list[0]
		current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		# 此时的material_dict字典的值是给奖励列表的，
		# 所以hang_stage是奖励之前的关卡，
		# hang_up_time是之前挂起的开始时间
		material_dict = {}
		for key, value in self._hang_reward_list[str(hang_stage)].items():
			material_dict.update({key: value})
		material_dict.update({"hang_stage": hang_stage})
		material_dict.update({"hang_up_time": hang_up_time})
		key_word = ["hang_stage", "hang_up_time"]
		if hang_up_time == "":
			# 下面的功能是将奖励拿出来，并且将数据库剩余的值发送给客户端
			keys = list(material_dict.keys())
			update_str, select_str = self._sql_str_operating(unique_id=unique_id, material_dict=material_dict, key_word=key_word)
			if await self._execute_statement_update(world=world, statement=update_str) == 0:
				return self._message_typesetting(status=2, message="database operating error")
			data = await self._execute_statement(world=world, statement=select_str)
			values = list(data[0])
			return self._message_typesetting(status=0, message="hang up success", data={"keys": keys, "values": values})
		else:
			delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(hang_up_time, '%Y-%m-%d %H:%M:%S')
			minute = int(delta_time.total_seconds()) // 60
			hang_up_time = (datetime.strptime(hang_up_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=minute)).strftime("%Y-%m-%d %H:%M:%S")

			for key in material_dict.keys():
				if key not in key_word:
					material_dict[key] = int(material_dict[key]) * minute
			keys, hang_rewards = list(material_dict.keys()), list(material_dict.values())

			# 此时的material_dict中的数据是用于数据库操作的数据
			material_dict.update({"hang_stage": stage})
			material_dict.update({"hang_up_time": hang_up_time})

			update_str, select_str = self._sql_str_operating(unique_id=unique_id, material_dict=material_dict, key_word=key_word)
			await self._execute_statement_update(world=world, statement=update_str)
			data = await self._execute_statement(world=world, statement=select_str)
			values = list(data[0])
			return self._message_typesetting(status=1, message="Repeated hang up successfully", data={"keys": keys, "values": values, "hang_rewards": hang_rewards})

	async def get_hang_up_reward(self, world: int, unique_id: str) -> dict:
		"""
		success ===> 0
		# 0 - Settlement reward success
		# 1 - Temporarily no on-hook record
		"""
		sql_str = "SELECT hang_up_time,hang_stage FROM player WHERE unique_id='%s'" % unique_id
		key_list = await self._execute_statement(world=world, statement=sql_str)
		hang_up_time, hang_stage = key_list[0]
		current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		if hang_up_time == "" or int(hang_stage) == 0:
			return self._message_typesetting(status=1, message="Temporarily no on-hook record")
		else:
			# 此时的material_dict字典的值是给奖励列表的，
			# 所以hang_stage是奖励之前的关卡，
			# hang_up_time是之前挂起的开始时间
			material_dict = {}
			for key, value in self._hang_reward_list[str(hang_stage)].items():
				material_dict.update({key: value})
			material_dict.update({"hang_stage": hang_stage})
			material_dict.update({"hang_up_time": hang_up_time})
			key_word = ["hang_stage", "hang_up_time"]

			delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(hang_up_time, '%Y-%m-%d %H:%M:%S')
			minute = int(delta_time.total_seconds()) // 60
			hang_up_time = (datetime.strptime(hang_up_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=minute)).strftime("%Y-%m-%d %H:%M:%S")

			for key in material_dict.keys():
				if key not in key_word:
					material_dict[key] = int(material_dict[key]) * minute
			keys, hang_rewards = list(material_dict.keys()), list(material_dict.values())

			# 此时的material_dict中的数据是用于数据库操作的数据
			material_dict.update({"hang_up_time": hang_up_time})

			update_str, select_str = self._sql_str_operating(unique_id=unique_id, material_dict=material_dict, key_word=key_word)
			await self._execute_statement_update(world=world, statement=update_str)
			data = await self._execute_statement(world=world, statement=select_str)
			values = list(data[0])

			return self._message_typesetting(status=0, message="Settlement reward success", data={"keys": keys, "values": values, "hang_rewards": hang_rewards})




#############################################################################
#						End Stage Module Functions							#
#############################################################################




#############################################################################
#						Lottery Module Functions							#
#############################################################################

	async def random_gift_skill(self, world: int, unique_id: str, kind: str) -> dict:
		# success ===> 0 and 1
		# 0 - unlocked new skill            {"skill_id": skill_id, "value": value}
		# 1 - you received a free scroll    {"skill_scroll_id": skill_scroll_id, "value": value}
		# 2 - invalid skill name
		# 3 - database operation error
		tier_choice = (random.choices(self._lottery['skills']['names'], self._lottery['skills']['weights'][kind]))[0]
		gift_skill  = (random.choices(self._lottery['skills']['items'][tier_choice]))[0]
		data = await self.try_unlock_skill(world, unique_id, gift_skill)
		status = int(data['status'])
		if status == 0:
			return self._message_typesetting(0, 'unlocked new skill', {'keys' : [gift_skill], 'values': [1]})
		elif status == 1:  # skill already unlocked
			if tier_choice == 'skilltier1':
				skill_scroll_id = 'skill_scroll_10'
				data = await self.try_skill_scroll_10(world, unique_id, 1)
			elif tier_choice == 'skilltier2':
				skill_scroll_id = 'skill_scroll_30'
				data = await self.try_skill_scroll_30(world, unique_id, 1)
			else:
				skill_scroll_id = 'skill_scroll_100'
				data = await self.try_skill_scroll_100(world, unique_id, 1)
			if data['status'] != 0:
				return self._message_typesetting(3, 'Database operation error')
			return self._message_typesetting(1, 'You received a free scroll', {'keys' : [skill_scroll_id], 'values' : [data['remaining']]})
		else:
			return self._message_typesetting(2, 'Invalid skill name')


	async def random_gift_segment(self, world: int, unique_id: str, kind: str) -> dict:
		# success ===> 0 and 1
		# - 0 - Unlocked new weapon!   ===> {"keys": ["weapon"], "values": [weapon]}
		# - 1 - Weapon already unlocked, got free segment   ===>  {"keys": ['weapon', 'segment'], "values": [weapon, segment]}
		# - 2 - no weapon!
		tier_choice = (random.choices(self._lottery['weapons']['names'], self._lottery['weapons']['weights'][kind]))[0]
		gift_weapon = (random.choices(self._lottery['weapons']['items'][tier_choice]))[0]
		return await self.try_unlock_weapon(world, unique_id, gift_weapon)

	async def random_gift_role(self, world: int, unique_id: str, kind: str) -> dict:
		# success ===> 0 and 1
		# - 0 - Unlocked new weapon!   ===> {"keys": ["weapon"], "values": [weapon]}
		# - 1 - Weapon already unlocked, got free segment   ===>  {"keys": ['weapon', 'segment'], "values": [weapon, segment]}
		# - 2 - no weapon!
		tier_choice = (random.choices(self._lottery['roles']['names'], self._lottery['roles']['weights'][kind]))[0]
		gift_role = (random.choices(self._lottery['roles']['items'][tier_choice]))[0]
		return await self.try_unlock_role(world, unique_id, gift_role)


	async def basic_summon(self, world: int, unique_id: str, cost_item: str, summon_kind: str) -> dict:
		# 0 - unlocked new skill or weapon
		# 1 - you received free scroll or segments
		# 2 - invalid skill name
		# 3 - database operation error
		# 4 - insufficient material
		# 5 - cost_item error
		return await self._default_summon(world, unique_id, cost_item, 'basic', summon_kind)

	async def pro_summon(self, world: int, unique_id: str, cost_item: str, summon_kind: str) -> dict:
		# 0 - unlocked new skill or weapon
		# 1 - you received free scroll or segments
		# 2 - invalid skill name
		# 3 - database operation error
		# 4 - insufficient material
		# 5 - cost_item error
		return await self._default_summon(world, unique_id, cost_item, 'pro', summon_kind)


	async def friend_summon(self, world: int, unique_id: str, cost_item: str, summon_kind: str) -> dict:
		# 0 - unlocked new skill or weapon
		# 1 - you received free scroll or segments
		# 2 - invalid skill name
		# 3 - database operation error
		# 4 - insufficient material
		# 5 - cost_item error
		return await self._default_summon(world, unique_id, cost_item, 'friend', summon_kind)

	async def prophet_summon(self, world: int, unique_id: str, cost_item: str, summon_kind: str) -> dict:
		return await self._default_summon(world, unique_id, cost_item, 'prophe', summon_kind)

	async def fortune_wheel_basic(self, world: int, unique_id: str, cost_item: str) -> dict:
		return await self._default_fortune_wheel(world, unique_id, cost_item, 'basic')

	async def fortune_wheel_pro(self, world: int, unique_id: str, cost_item: str) -> dict:
		return await self._default_fortune_wheel(world, unique_id, cost_item, 'pro')



#############################################################################
#						End Lottery Module Functions						#
#############################################################################





#############################################################################
#							Private Functions								#
#############################################################################

	async def _set_role_segment_by_id(self, world: int, unique_id: str, role: str, segment: int):
		return await self._execute_statement_update(world, 'UPDATE `' + role + '` SET segment = "' + str(segment) + '" WHERE unique_id = "' + unique_id + '";')

	async def _get_role_segment(self, world: int, unique_id: str, role: str) -> int:
		data = await self._execute_statement(world, 'SELECT segment FROM `' + role + '` WHERE unique_id = "' + unique_id + '";')
		return int(data[0][0])

	async def _get_role_star(self, world: int, unique_id: str, role: str) -> dict:
		data = await self._execute_statement(world, 'SELECT ' + role + ' FROM role_bag WHERE unique_id = "' + unique_id + '";')
		return int(data[0][0])

	async def _set_role_star(self, world: int, unique_id: str, weapon: str, star: int):
		return await self._execute_statement_update(world, 'UPDATE role_bag SET ' + weapon + ' = "' + str(star) + '" WHERE unique_id = "' + unique_id + '";')

	async def _default_fortune_wheel(self, world: int, uid: str, cost_item: str, tier: str):
		# 0 - get item success
		# 1 - get weapon item success
		# 2 - get skill item success
		# 96 - item name error
		# 97 - skill operation error
		# 98 - insufficient material
		# 99 - cost_item error
		if cost_item == 'diamond':
			result = await self.try_diamond(world, uid, -int(self._lottery['fortune_wheel']['cost'][cost_item]))
		elif cost_item == 'coin':
			result = await self.try_coin(world, uid, -int(self._lottery['fortune_wheel']['cost'][cost_item]))
		elif cost_item == 'fortune_wheel_ticket_basic':
			result = await self.try_fortune_wheel_ticket_basic(world, uid, -int(self._lottery['fortune_wheel']['cost'][cost_item]))
		elif cost_item == 'fortune_wheel_ticket_pro':
			result = await self.try_fortune_wheel_ticket_pro(world, uid, -int(self._lottery['fortune_wheel']['cost'][cost_item]))
		elif cost_item == 'basic_summon_scroll':
			result = await self.try_basic_summon_scroll(world, uid, -int(self._lottery['fortune_wheel']['cost'][cost_item]))
		elif cost_item == 'pro_summon_scroll':
			result = await self.try_pro_summon_scroll(world, uid, -int(self._lottery['fortune_wheel']['cost'][cost_item]))
		else:
			return self._message_typesetting(99, 'cost_item error')
		if result['status'] != 0:
			return self._message_typesetting(98, 'insufficient materials')
		tier_choice = (random.choices(self._lottery['fortune_wheel']['names'], self._lottery['fortune_wheel']['weights'][tier]))[0]
		random_item = (random.choices(self._lottery['fortune_wheel']['items'][tier_choice]))[0]
		try_result = await self.try_diamond(world, uid, 0)

		# TODO THIS SHIT NEEDS TO BE REFACTORED
		if random_item == 'coin':
			try_result = await self.try_coin(world, uid, int(self._lottery['fortune_wheel']['reward'][tier][random_item]))
		elif random_item == 'energy':
			try_result = await self.try_energy(world, uid, int(self._lottery['fortune_wheel']['reward'][tier][random_item]))
			return self._message_typesetting(0, 'get item success', {'remaining' : {'keys' : try_result['data']['keys'], 'values' : try_result['data']['values']}, 'reward' : {'keys' : [random_item], 'values' : [self._lottery['fortune_wheel']['reward'][tier][random_item]]}})
		elif random_item == 'diamond':
			try_result = await self.try_diamond(world, uid, int(self._lottery['fortune_wheel']['reward'][tier][random_item]))
		elif random_item == 'skill_scroll_10':
			try_result = await self.try_skill_scroll_10(world, uid, int(self._lottery['fortune_wheel']['reward'][tier][random_item]))
		elif random_item == 'skill_scroll_30':
			try_result = await self.try_skill_scroll_30(world, uid, int(self._lottery['fortune_wheel']['reward'][tier][random_item]))
		elif random_item == 'skill_scroll_100':
			try_result = await self.try_skill_scroll_100(world, uid, int(self._lottery['fortune_wheel']['reward'][tier][random_item]))
		elif random_item == 'weapon':
			try_result = await self.random_gift_segment(world, uid, tier)
			if try_result['status'] == 0 or try_result['status'] == 1:
				message_dic = {
					"remaining" :
					{
						"weapon" : try_result['data']['values'][0],
						'star' : try_result['data']['values'][1],
						'segment' : try_result['data']['values'][2]
					},
					'reward':
					{
						'weapon' : try_result['data']['values'][0],
						'segment' : self._standard_segment_count
					}
				}
				return self._message_typesetting(1, 'get weapon item success', message_dic)
			else:
				return self._message_typesetting(97, 'skill operation error')
		elif random_item == 'skill':
			try_result = await self.random_gift_skill(world, uid, tier)
			if try_result['status'] == 0 or try_result['status'] == 1:
				if try_result['status'] == 0:
					message_dic = {
						"remaining":
						{
							"skill_id" : try_result['data']['keys'][0],
							'skill_level' : try_result['data']['values'][0]
						},
						'reward':
						{
							'skill_id' : try_result['data']['keys'][0],
							'skill_level' : try_result['data']['values'][0]
						}
					}
				else:
					message_dic = {
						'remaining' :
						{
							'scroll_id' : try_result['data']['keys'][0],
							'scroll_quantity' : try_result['data']['values'][0]
						},
						'reward' :
						{
							'scroll_id' : try_result['data']['values'][0],
							'scroll_quantity' : 1
						}
					}
				return self._message_typesetting(2, 'get skill item success', message_dic)
			else:
				return self._message_typesetting(97, 'skill operation error')
		else:
			return self._message_typesetting(96, 'item name error')
		return self._message_typesetting(3, 'get item success', {'remaining' : {'keys' : [random_item], 'values' : [try_result['remaining']]}, 'reward' : {'keys' : [random_item], 'values' : [self._lottery['fortune_wheel']['reward'][tier][random_item]]}})




	async def _get_energy_information(self, world: int, unique_id: str) -> (int, str):
		data = await self._execute_statement(world, 'SELECT energy, recover_time, FROM player WHERE unique_id = "' + unique_id + '";')
		return int(data[0][0]), data[0][1]

	async def _decrease_energy(self, world:int, unique_id: str, amount: int) -> dict:
		current_energy, recover_time = await self._get_energy_information(world, unique_id)
		current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		full_energy=self._player["energy"]["max_energy"]
		_cooling_time=self._player["energy"]["cooling_time"]
		if recover_time == '':  # 此时 current_energy == self._full_energy 成立
			if amount == 0:  # 成功1：如果没有恢复时间且是获取能量值，则直接拿取数据库的值给客户端
				return self._message_typesetting(2, 'Get energy successfully', {"keys": ['energy', 'recover_time', 'cooling_time'], "values": [current_energy, recover_time, -1]})
			current_energy -= amount
			# 成功2：如果没有恢复时间且是消耗能量值，则直接用数据库的值减去消耗的能量值，
			# 然后存入消耗之后的能量值，以及将当前的时间存入 恢复时间项
			if current_energy >= full_energy: current_time = ""  # 能量超出满能力状态时，不计算恢复时间
			cooling_time = _cooling_time * 60
			await self._execute_statement_update(world, 'UPDATE player SET energy = ' + str(current_energy) + ', recover_time = "' + current_time + '" WHERE unique_id = "' + unique_id + '";')
			return self._message_typesetting(3, 'Energy has been consumed, energy value and recovery time updated successfully', {"keys": ['energy', 'recover_time', 'cooling_time'], "values": [current_energy, current_time, cooling_time]})
		else:
			delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S')
			recovered_energy = delta_time.seconds // 60 // _cooling_time
			if amount == 0:
				# 成功3：如果有恢复时间且是获取能量值，则加上获取的能量值，并判断能量值是否满足上限
				# 满足上限的情况：直接将满能量值和空字符串分别存入能量值项和恢复时间项
				if current_energy + recovered_energy >= full_energy:
					recover_time, current_energy, cooling_time = "", full_energy, -1
					await self._execute_statement_update(world=world,statement='UPDATE player SET energy = ' + str(current_energy) + ', recover_time = "' + recover_time + '" WHERE unique_id = "' + unique_id + '";')
					return self._message_typesetting(status=4, message='Energy has been fully restored, successful energy update', data={"keys": ['energy', 'recover_time', 'cooling_time'], "values": [current_energy, recover_time, cooling_time]})
				# 成功4：如果有恢复时间且是获取能量值，则加上获取的能量值，并判断能量值是否满足上限
				# 不满足上限的情况：将能恢复的能量值计算出来，并且计算恢复后的能量值current_energy
				# 和恢复时间与恢复能量消耗的时间相减的恢复时间值
				else:
					recover_time, current_energy = (datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=recovered_energy * _cooling_time)).strftime("%Y-%m-%d %H:%M:%S"), current_energy + recovered_energy
					delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S')
					cooling_time = 60 * _cooling_time - delta_time.seconds
					await self._execute_statement_update(world=world, statement='UPDATE player SET energy = ' + str(current_energy) + ', recover_time = "' + recover_time + '" WHERE unique_id = "' + unique_id + '";')
					return self._message_typesetting(status=5, message='Energy has not fully recovered, successful energy update', data={"keys": ['energy', 'recover_time', 'cooling_time'], "values": [current_energy, recover_time, cooling_time]})

				# recover_time, current_energy = ("", self._full_energy) if (current_energy + recovered_energy >= self._full_energy) else ((datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=recovered_energy * self._cooling_time)).strftime("%Y-%m-%d %H:%M:%S"), current_energy + recovered_energy)
				# await self._execute_statement('UPDATE player SET energy = ' + str(current_energy) + ', recover_time = "' + recover_time + '" WHERE unique_id = "' + unique_id + '";')
				# return self.message_typesetting(status=0, message='Energy has been recovered and energy is successfully acquired', data={"keys": ['energy', 'recover_time'], "values": [current_energy, recover_time]})
			if recovered_energy + current_energy >= full_energy:
				# 成功5：如果有恢复时间且是消耗能量
				# 满足上限的情况是用上限能量值减去要消耗的能量值，然后设置减去之后的能量值和当前的时间分别存入能量值项和恢复时间项
				current_energy = full_energy - amount
				cooling_time = _cooling_time * 60
				await self._execute_statement_update(world=world,statement='UPDATE player SET energy = ' + str(current_energy) + ', recover_time = "' + current_time + '" WHERE unique_id = "' + unique_id + '";')
				return self._message_typesetting(6, 'After refreshing the energy, the energy value and recovery time are successfully updated.', {"keys": ['energy', 'recover_time', 'cooling_time'], "values": [current_energy, recover_time, cooling_time]})
			elif recovered_energy + current_energy - amount >= 0:
				# 成功6：如果有恢复时间且是消耗能量
				# 不满足上限的情况是用当前数据库的能量值和当前恢复的能量值相加然后减去消耗的能量值为要存入数据库的能量值项
				# 数据库中的恢复时间与恢复能量消耗的时间相减的恢复时间值存入到数据库的恢复时间项
				current_energy = recovered_energy + current_energy - amount
				recover_time = (datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=recovered_energy * _cooling_time)).strftime("%Y-%m-%d %H:%M:%S")
				delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S')
				cooling_time = 60 * _cooling_time - delta_time.seconds
				await self._execute_statement_update(world=world,statement='UPDATE player SET energy = ' + str(current_energy) + ', recover_time = "' + recover_time + '" WHERE unique_id = "' + unique_id + '";')
				return self._message_typesetting(7, 'Energy has been refreshed, not fully recovered, energy has been consumed, energy value and recovery time updated successfully', {"keys": ['energy', 'recover_time', 'cooling_time'], "values": [current_energy, recover_time, cooling_time]})
			else:  # 发生的情况是当前能量值和恢复能量值相加比需要消耗的能量值少
				return self._message_typesetting(status=9, message="Not enough energy consumption")







	async def _default_summon(self, world: int, unique_id: str, cost_item: str, tier: str, summon_item: str):
		if cost_item == 'diamond':
			result = await self.try_diamond(world, unique_id, -1 * int(self._lottery[summon_item]['cost'][cost_item]))
		elif cost_item == 'coin':
			result = await self.try_coin(world, unique_id, -1 * int(self._lottery[summon_item]['cost'][cost_item]))
		elif cost_item == 'basic_summon_scroll':
			result = await self.try_basic_summon_scroll(world, unique_id, -1 * int(self._lottery[summon_item]['cost'][cost_item]))
		elif cost_item == 'pro_summon_scroll':
			result = await self.try_pro_summon_scroll(world, unique_id, -int(self._lottery[summon_item]['cost'][cost_item]))
		elif cost_item == 'friend_gift':
			result = await self.try_friend_gift(world, unique_id, -int(self._lottery[summon_item]['cost'][cost_item]))
		elif cost_item == 'prophet_summon_scroll':
			result = await self.try_prophet_summon_scroll(world, unique_id, -int(self._lottery[summon_item]['cost'][cost_item]))
		else:
			return self._message_typesetting(4, 'wrong item name')
		if result['remaining'] < 0:
			return self._message_typesetting(97, 'insufficient materials')
		if summon_item == 'skills':
			try_result = await self.random_gift_skill(world, unique_id, tier)
			if try_result['status'] == 0 or try_result['status'] == 1:
				if try_result['status'] == 0:
					message_dic = {
						'remaining':
						{
							'skill_id' : try_result['data']['keys'][0],
							'skill_level' : try_result['data']['values'][0]
						},
						'reward':
						{
							'skill_id' : try_result['data']['keys'][0],
							'skill_level' : try_result['data']['values'][0]
						}
					}
				else:
					message_dic = {
						'remaining':
						{
							'scroll_id' : try_result['data']['keys'][0],
							'scroll_quantity' : try_result['data']['values'][0]
						},
						'reward':
						{
							'scroll_id' : try_result['data']['keys'][0],
							'scroll_quantity' : 1
						}
					}
				return self._message_typesetting(2, 'get skill item success', message_dic)
			else:
				return self._message_typesetting(97, 'skill operation error')
		elif summon_item == 'weapons':
			try_result = await self.random_gift_segment(world, unique_id, tier)
			if try_result['status'] == 0 or try_result['status'] == 1:
				message_dic = {
					'remaining' :
					{
						'weapon' : try_result['data']['values'][0],
						'star' : try_result['data']['values'][1],
						'segment' : try_result['data']['values'][2]
					},
					'reward':
					{
						'weapon' : try_result['data']['values'][0],
						'segment' : self._standard_segment_count
					}
				}
				return self._message_typsetting(1, 'get weapon item success', message_dic)
			else:
				return self._message_typesetting(97, 'operation error')

	async def _get_energy_information(self, world: int, unique_id: str) -> (int, str):
		data = await self._execute_statement(world, 'SELECT energy, recover_time FROM player WHERE unique_id = "' + unique_id + '";')
		return int(data[0][0]), data[0][1]


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

	async def _get_segment(self, world: int, unique_id: str, weapon: str) -> int:
		data = await self._execute_statement(world, 'SELECT segment FROM `' + weapon + '` WHERE unique_id = "' + unique_id + '";')
		return int(data[0][0])

	async def _set_segment_by_id(self, world: int, unique_id: str, weapon: str, segment: int):
		return await self._execute_statement_update(world, 'UPDATE `' + weapon + '` SET segment = "' + str(segment) + '" WHERE unique_id = "' + unique_id + '";')

	async def _get_weapon_star(self, world: int, unique_id: str, weapon: str) -> int:
		data = await self._execute_statement(world, 'SELECT ' + weapon + ' FROM weapon_bag WHERE unique_id = "' + unique_id + '";')
		return int(data[0][0])

	async def _get_row_by_id(self, world: int, weapon: str, unique_id: str) -> list:
		data = await self._execute_statement(world, 'SELECT * FROM `' + weapon + '` WHERE unique_id = "' + unique_id + '";')
		return list(data[0])

	async def _set_passive_skill_level_up_data(self, world: int, unique_id: str, weapon: str, passive: str, skill_level: int, skill_point: int) -> dict:
		return await self._execute_statement_update(world, 'UPDATE `' + weapon + '` SET ' + passive + ' = "' + str(skill_level) + '", skill_point = "' + str(skill_point) + '" WHERE unique_id = "' + unique_id + '";')

	async def _set_weapon_level_up_data(self, world: int, unique_id: str, weapon: str, weapon_level: int, skill_point: int) -> dict:
		return await self._execute_statement_update(world, 'UPDATE `' + weapon + '` SET weapon_level = "' + str(weapon_level) + '", skill_point = "' + str(skill_point) + '" WHERE unique_id = "' + unique_id + '";')


	async def _get_skill_level(self, world: int, unique_id: str, skill_id: str) -> int:
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


	def _sql_str_operating(self, unique_id: str, material_dict: dict, key_word: list = []) -> (str, str):
		update_str = "UPDATE player SET "
		update_end_str = " where unique_id='%s'" % unique_id
		select_str = "SELECT "
		select_end_str = " FROM player WHERE unique_id='%s'" % unique_id
		for key in material_dict.keys():
			if key in key_word:
				update_str += "%s='%s', " % (key, material_dict[key])
			else:
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


	def _refresh_configuration(self):
		r = requests.get('http://localhost:8000/get_game_manager_config')
		d = r.json()
		self._stage_reward = d['reward']
		self._skill_scroll_functions = set(d['skill']['skill_scroll_functions'])
		self._upgrade_chance = d['skill']['upgrade_chance']
		self._standard_iron_count = d['weapon']['standard_iron_count']
		self._standard_segment_count = d['weapon']['standard_segment_count']
		self._standard_reset_weapon_skill_coin_count = d['weapon']['standard_reset_weapon_skill_coin_count']
		self._valid_passive_skills = d['weapon']['valid_passive_skills']
		self._lottery = d['lottery']
		self._player = d['player']
		self._hang_reward_list = d['hang_reward']
		self._entry_consumables = d['entry_consumables']

	def _start_timer(self, seconds: int):
		t = threading.Timer(seconds, self._refresh_configuration)
		t.daemon = True
		t.start()



#############################################################################
#
#
#
#
#############################################################################

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
	result = await (request.app['MANAGER']).get_all_head(int(post['world']), post['table'])
	return _json_response(result)

@ROUTES.post('/get_all_material')
async def __get_all_material(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).get_all_material(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/get_all_supplies')
async def __get_all_supplies(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).get_all_supplies(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/add_supplies')
async def __add_supplies(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).add_supplies(int(post['world']), post['unique_id'], post['supply'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/level_up_scroll')
async def __level_up_scroll(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).level_up_scroll(int(post['world']), post['unique_id'], post['scroll_id'])
	return _json_response(result)

@ROUTES.post('/try_all_material')
async def __try_all_material(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_all_material(int(post['world']), post['unique_id'], int(post['stage']))
	return _json_response(result)

@ROUTES.post('/try_energy')
async def __try_energy(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_energy(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_coin')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_coin(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_iron')
async def __try_iron(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_iron(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_diamond')
async def __try_diamond(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_diamond(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_experience')
async def __try_experience(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_experience(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_level')
async def __try_level(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_level(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_role')
async def __try_role(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_role(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_stage')
async def __try_stage(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_stage(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_skill_scroll_10')
async def __try_skill_scroll_10(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_skill_scroll_10(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_skill_scroll_30')
async def __try_skill_scroll_30(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_skill_scroll_30(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_skill_scroll_100')
async def __try_skill_scroll_100(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_skill_scroll_100(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_experience_potion')
async def __try_experience_potion(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_experience_potion(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_small_energy_potion')
async def __try_small_energy_potion(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_small_energy_potion(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/level_up_skill')
async def __level_up_skill(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).level_up_skill(int(post['world']), post['unique_id'], post['skill_id'], post['scroll_id'])
	return _json_response(result)

@ROUTES.post('/get_all_skill_level')
async def __get_all_skill_level(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).get_all_skill_level(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/get_skill')
async def __get_skill(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).get_skill(int(post['world']), post['unique_id'], post['skill_id'])
	return _json_response(result)

@ROUTES.post('/try_unlock_skill')
async def __try_unlock_skill(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_unlock_skill(int(post['world']), post['unique_id'], post['skill_id'])
	return _json_response(result)

@ROUTES.post('/level_up_weapon')
async def __level_up_weapon(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).level_up_weapon(int(post['world']), post['unique_id'], post['weapon'], int(post['iron']))
	return _json_response(result)

@ROUTES.post('/level_up_passive')
async def __level_up_passive(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).level_up_passive(int(post['world']), post['unique_id'], post['weapon'], post['passive'])
	return _json_response(result)


@ROUTES.post('/level_up_weapon_star')
async def __level_up_weapon_star(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).level_up_weapon_star(int(post['world']), post['unique_id'], post['weapon'])
	return _json_response(result)

@ROUTES.post('/reset_weapon_skill_point')
async def __reset_weapon_skill_point(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).reset_weapon_skill_point(int(post['world']), post['unique_id'], post['weapon'])
	return _json_response(result)

@ROUTES.post('/get_all_weapon')
async def __get_all_weapon(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).get_all_weapon(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/try_unlock_weapon')
async def __try_unlock_weapon(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_unlock_weapon(int(post['world']), post['unique_id'], post['weapon'])
	return _json_response(result)

@ROUTES.post('/pass_stage')
async def __pass_stage(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).pass_stage(int(post['world']), post['unique_id'], int(post['stage']), post['clear_time'])
	return _json_response(result)


@ROUTES.post('/basic_summon')
async def __basic_summon(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(json.loads(requests.post('http://localhost:8006' + '/basic_summon', data = {'world': post['world'], "unique_id": post['unique_id'],"cost_item":post['cost_item']}).text))

@ROUTES.post('/pro_summon')
async def __pro_summon(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(json.loads(requests.post('http://localhost:8006' + '/pro_summon', data = {'world': post['world'], "unique_id": post['unique_id'],"cost_item":post['cost_item']}).text))

@ROUTES.post('/friend_summon')
async def __friend_summon(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(json.loads(requests.post('http://localhost:8006' + '/friend_summon', data = {'world': post['world'], "unique_id": post['unique_id'],"cost_item":post['cost_item']}).text))

@ROUTES.post('/prophet_summon')
async def __prophet_summon(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(json.loads(requests.post('http://localhost:8006' + '/prophet_summon', data = {'world': post['world'], "unique_id": post['unique_id'],"cost_item":post['cost_item']}).text))

@ROUTES.post('/basic_summon_skill')
async def __basic_summon(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(json.loads(requests.post('http://localhost:8006' + '/basic_summon_skill', data = {'world': post['world'], "unique_id": post['unique_id'],"cost_item":post['cost_item']}).text))

@ROUTES.post('/pro_summon_skill')
async def __pro_summon(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(json.loads(requests.post('http://localhost:8006' + '/pro_summon_skill', data = {'world': post['world'], "unique_id": post['unique_id'],"cost_item":post['cost_item']}).text))

@ROUTES.post('/friend_summon_skill')
async def __pro_summon(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(json.loads(requests.post('http://localhost:8006' + '/friend_summon_skill', data = {'world': post['world'], "unique_id": post['unique_id'],"cost_item":post['cost_item']}).text))

@ROUTES.post('/basic_summon_roles')
async def __basic_summon(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(json.loads(requests.post('http://localhost:8006' + '/basic_summon_roles', data = {'world': post['world'], "unique_id": post['unique_id'],"cost_item":post['cost_item']}).text))

@ROUTES.post('/pro_summon_roles')
async def __pro_summon(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(json.loads(requests.post('http://localhost:8006' + '/pro_summon_roles', data = {'world': post['world'], "unique_id": post['unique_id'],"cost_item":post['cost_item']}).text))

@ROUTES.post('/friend_summon_roles')
async def __pro_summon(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(json.loads(requests.post('http://localhost:8006' + '/friend_summon_roles', data = {'world': post['world'], "unique_id": post['unique_id'],"cost_item":post['cost_item']}).text))

@ROUTES.post('/fortune_wheel_basic')
async def __pro_summon(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(json.loads(requests.post('http://localhost:8006' + '/fortune_wheel_basic', data = {'world': post['world'], "unique_id": post['unique_id'],"cost_item":post['cost_item']}).text))

@ROUTES.post('/fortune_wheel_pro')
async def __pro_summon(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(json.loads(requests.post('http://localhost:8006' + '/fortune_wheel_pro', data = {'world': post['world'], "unique_id": post['unique_id'],"cost_item":post['cost_item']}).text))

@ROUTES.post('/automatically_refresh_store')
async def __automatically_refresh_store(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(json.loads(requests.post('http://localhost:8007' + '/automatically_refresh_store', data = {'world': post['world'], "unique_id": post['unique_id']}).text))

@ROUTES.post('/manually_refresh_store')
async def __manually_refresh_store(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(json.loads(requests.post('http://localhost:8007' + '/manually_refresh_store', data = {'world': post['world'], "unique_id": post['unique_id']}).text))

@ROUTES.post('/diamond_refresh_store')
async def __diamond_refresh_store(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(json.loads(requests.post('http://localhost:8007' + '/diamond_refresh_store', data = {'world': post['world'], "unique_id": post['unique_id']}).text))

@ROUTES.post('/black_market_transaction')
async def __black_market_transaction(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(json.loads(requests.post('http://localhost:8007' + '/black_market_transaction', data = {'world': post['world'], "unique_id": post['unique_id'], "code": post['code']}).text))

@ROUTES.post('/send_friend_gift')
async def _send_friend_gift(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(json.loads(requests.post('http://localhost:8006' + '/send_friend_gift', data = {'world': post['world'], "unique_id": post['unique_id'], "friend_id": post['friend_id']}).text))

@ROUTES.post('/send_all_friend_gift')
async def _send_all_friend_gift(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(json.loads(requests.post('http://localhost:8006' + '/send_all_friend_gift', data = {'world': post['world'], "unique_id": post['unique_id']}).text))

@ROUTES.post('/get_all_friend_info')
async def _get_all_friend_info(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(json.loads(requests.post('http://localhost:8006' + '/get_all_friend_info', data = {'world': post['world'], "unique_id": post['unique_id']}).text))

@ROUTES.post('/start_hang_up')
async def __start_hang_up(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).start_hang_up(int(post['world']), post['unique_id'], int(post['stage']))
	return _json_response(result)

@ROUTES.post('/get_hang_up_reward')
async def __get_hang_up_reward(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).get_hang_up_reward(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/fortune_wheel_pro')
async def __fortune_wheel_pro(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).fortune_wheel_pro(int(post['world']), post['unique_id'], post['cost_item'])
	return _json_response(result)

@ROUTES.post('/enter_stage')
async def __enter_stage(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).enter_stage(int(post['world']), post['unique_id'], int(post['stage']))
	return _json_response(result)




def get_config() -> configparser.ConfigParser:
	'''
	Fetches the server's configuration file from the config server.
	Waits until the configuration server is online.
	'''
	while True:
		try:
			r = requests.get('http://localhost:8000/get_server_config_location')
			parser = configparser.ConfigParser()
			parser.read(r.json()['file'])
			return parser
		except requests.exceptions.ConnectionError:
			print('Could not find configuration server, retrying in 5 seconds...')
			time.sleep(5)



def run():
	app = web.Application()
	app.add_routes(ROUTES)
	config = get_config()
	app['MANAGER'] = GameManager()
	web.run_app(app, port=config.getint('game_manager', 'port'))


if __name__ == '__main__':
	run()
