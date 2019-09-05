#
#
###############################################################################

import os
import sys
import time
import json
import random
import tormysql
import requests
import threading
import configparser
from aiohttp import web
from datetime import datetime, timedelta
from utility import repeating_timer
from utility import metrics


C = metrics.Collector()

class GameManager:
	def __init__(self, worlds = []):
		self._initialize_pools(worlds)
		self._is_first_start = True
		self.is_first_month = False
		self._boss_life=[]
		self._boss_life_remaining=[]
		self._refresh_configuration()
		self._timer = repeating_timer.RepeatingTimer(3, self._refresh_configuration)
		self._timer.start()

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

	@C.collect_async
	async def get_all_supplies(self, world: int, unique_id: str) -> dict:
		# success ===> 0
		data_tuple = (await self.get_all_head(world, table="player"))["remaining"]
		content = list((await self.get_all_material(world, unique_id=unique_id))["remaining"])
		remaining = {}
		for i in range(1, len(data_tuple)):
			remaining.update({data_tuple[i][0]: content[i]})
		return self._message_typesetting(0, "get supplies success", {"remaining": remaining})

	async def add_supplies(self, world: int, unique_id: str, supply: str, value: int):
		# success ===> 0
		if value <= 0: return self._message_typesetting(9, "not a positive number")
		data = await self._try_material(world, unique_id, supply, value)
		if data["status"] == 0:
			return self._message_typesetting(status=0, message="success", data={"remaining": {supply: data["remaining"]}})
		return self._message_typesetting(status=1, message="failure")

	@C.collect_async
	async def level_up_scroll(self, world: int, unique_id: str, scroll_id: str) -> dict:
		# 0 success
		# 95 advanced reels are not upgradeable
		# 96 insufficient scroll
		# 97 unexpected parameter --> scroll_id
		# 98 parameter error
		# 99 database operation error
		if scroll_id == "skill_scroll_100": return self._message_typesetting(status=95, message="advanced reels are not upgradeable!")
		try:
			scroll_id_count = await self._get_material(world, unique_id, scroll_id)
			if int(scroll_id_count) < 3:
				return self._message_typesetting(status=96, message="Insufficient scroll")
			elif scroll_id == "skill_scroll_10":
				dict1 = await self.try_skill_scroll_10(world, unique_id, -3)
				dict2 = await self.try_skill_scroll_30(world, unique_id, 1)
				if dict1["status"] == 1 or dict2["status"] == 1:
					return self._message_typesetting(status=99, message="database operation error!")
				return self._message_typesetting(status=0, message="level up scroll success!", data={"remaining": {"skill_scroll_10": dict1["remaining"], "skill_scroll_30": dict2["remaining"]}})
			elif scroll_id == "skill_scroll_30":
				dict1 = await self.try_skill_scroll_30(world, unique_id, -3)
				dict2 = await self.try_skill_scroll_100(world, unique_id, 1)
				if dict1["status"] == 1 or dict2["status"] == 1:
					return self._message_typesetting(status=99, message="database operation error!")
				return self._message_typesetting(status=0, message="level up scroll success!", data={"remaining": {"skill_scroll_30": dict1["remaining"], "skill_scroll_100": dict2["remaining"]}})
			else:
				return self._message_typesetting(status=97, message="unexpected parameter --> " + scroll_id)
		except:
			return self._message_typesetting(status=98, message='parameter error!')

	# TODO rename function - it is private and only called by pass_stage function
	async def try_pass_stage(self, world: int, unique_id: str, stage: int) -> dict:
		stage_data = self._stage_reward["stage"]
		sql_stage = await self._get_material(world, unique_id, "stage")
		if stage <= 0 or sql_stage + 1 < stage:
			return self._internal_format(status=9, remaining=0)  # abnormal data!
		material_dict = {"stage": 0}
		stages = [int(x) if str.isdigit(x) else 1 for x in stage_data.keys()]
		if stage not in stages: stage_reward = stage_data[str(max(stages))]
		else: stage_reward = stage_data[str(stage)]
		for key, value in stage_reward.items():
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
		# - 97 - 参数错误 === Parameter error
		# - 98 - 无足够能量消耗 === Not enough energy consumption
		# - 99 - 数据库操作错误 === Database operation error
		full_energy=self._player["energy"]["max_energy"]
		sql_energy = await self._get_material(world, unique_id, "energy")
		if sql_energy >= full_energy: await self._execute_statement_update(world, f"update player set recover_time='' where unique_id = '{unique_id}';")
		if amount > 0:
			data = (await self._decrease_energy(world, unique_id, 0))["data"]
			json_data = await self._try_material(world, unique_id, "energy", amount)
			if int(json_data["status"]) == 1:
				return self._message_typesetting(status=99, message="Database operation error")
			elif int(json_data["remaining"] >= full_energy):
				sql_str = f"UPDATE player SET recover_time = '' WHERE unique_id = '{unique_id}';"
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
			return self._message_typesetting(status=97, message="Parameter error")
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

	async def try_armor(self, world: int, unique_id: str, armor_id: str, armor_level: str, value: int) -> dict:
		select_str = f"select {armor_level} from armor where unique_id='{unique_id}' and armor_id='{armor_id}'"
		insert_str = f"insert into armor(unique_id, armor_id, {armor_level}) values('{unique_id}', '{armor_id}', {value})"
		update_str = f"update armor set {armor_level}={armor_level}+{value} where unique_id='{unique_id}' and armor_id='{armor_id}'"
		select_data = await self._execute_statement(world=world, statement=select_str)
		if select_data:
			if not value:
				return self._internal_format(status=0, remaining=select_data[0][0])
			remaining = select_data[0][0] + value
			if remaining < 0:
				return self._internal_format(status=1, remaining=remaining)
			status = await self._execute_statement_update(world=world, statement=update_str)
			return self._internal_format(status=1 - status, remaining=remaining)
		else:
			status = await self._execute_statement_update(world=world, statement=insert_str)
			return self._internal_format(status=1 - status, remaining=value)

#############################################################################
#						End Bag Module Functions							#
#############################################################################



#############################################################################
#						 Skill Module Functions								#
#############################################################################

	# TODO ensure SQL UPDATE statement succeeds
	# TODO error checking for valid skill_id?
	@C.collect_async
	async def level_up_skill(self, world: int, unique_id: str, skill_id: str, scroll_id: str):
		# success ===> 0 and 1
		# 0 - upgrade success
		# 1 - upgrade unsuccessful
		# 96 - User does not have that skill
		# 97 - Invalid scroll id
		# 98 - User does not have enough scrolls
		# 99 - Skill already at max level
		skill_level = await self._get_skill_level(world, unique_id, skill_id)
		if skill_level == 0:
			return self._message_typesetting(96, 'User does not have that skill')
		elif skill_level >= 10:
			return self._message_typesetting(99, 'Skill already max level')
		elif scroll_id not in self._skill_scroll_functions:
			return self._message_typesetting(97, 'Invalid scroll id')
		resp = await eval('self.try_' + scroll_id + '(world, unique_id, -1)')
		if resp['status'] == 1:
			return self._message_typesetting(98, 'User does not have enough scrolls')
		if not self._roll_for_upgrade(scroll_id):
			return self._message_typesetting(1, 'upgrade unsuccessful', {'remaining': {skill_id: skill_level, scroll_id: resp['remaining']}})
		await self._execute_statement(world, 'UPDATE skill SET `' + skill_id + '` = ' + str(skill_level + 1) + ' WHERE unique_id = "' + unique_id + '";')
		return self._message_typesetting(0, 'upgrade success', {'remaining': {skill_id: skill_level + 1, scroll_id: resp['remaining']}})

	@C.collect_async
	async def get_all_skill_level(self, world: int, unique_id: str) -> dict:
		# success ===> 0
		# 0 - Success
		names = await self._execute_statement(world, 'DESCRIBE skill;')
		values = await self._execute_statement(world, 'SELECT * from skill WHERE unique_id = "' + str(unique_id) + '";')
		remaining = {}
		for num, val in enumerate(zip(names[1:], values[0][1:])):
			remaining.update({val[0][0]: val[1]})
		return self._message_typesetting(0, 'success', {"remaining": remaining})

	def get_skill_level_up_config(self) -> dict:
		# success ===> 0
		# 0 - Success
		return self._message_typesetting(0, 'success', {"remaining": {"skill_scroll_functions": self._skill_scroll_functions, "upgrade_chance": self._upgrade_chance}})

	@C.collect_async
	async def get_skill(self, world: int, unique_id: str, skill_id: str) -> dict:
		# success ===> 0
		# 0 - Success
		# 99 - invalid skill name
		try:
			level = await self._get_skill_level(world, unique_id, skill_id)
			return self._message_typesetting(0, 'success', {'remaining': {skill_id: level}})
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

	@C.collect_async
	async def level_up_weapon(self, world: int, unique_id: str, weapon: str, iron: int) -> dict:
		# - 0 - Success
		# - 94 - Invalid weapon name
		# - 95 - User does not have that weapon
		# - 96 - Incoming materials are not upgraded enough
		# - 97 - Insufficient materials, upgrade failed
		# - 98 - Database operation error
		# - 99 - Weapon already max level
		if weapon not in self._weapon_config["weapons"]:
			return self._message_typesetting(status=94, message="Invalid weapon name")
		row = await self._get_row_by_id(world, weapon, unique_id)
		if row[2] == 0:
			return self._message_typesetting(95, 'User does not have that weapon')
		if row[3] == 100:
			return self._message_typesetting(status=99, message='Weapon already max level')

		standard_iron_count = self._weapon_config['standard_iron_count']
		skill_upgrade_number = iron // standard_iron_count
		data_tuple = (await self.get_all_head(world, 'weapon'))['remaining']
		head = [x[0] for x in data_tuple]
		level_count = head.index('weapon_level')
		point_count = head.index('skill_point')
		if (row[level_count] + skill_upgrade_number) > 100:
			skill_upgrade_number = 100 - row[level_count]
		row[level_count] += skill_upgrade_number
		row[point_count] += skill_upgrade_number

		if skill_upgrade_number == 0:
			return self._message_typesetting(status=96, message='Incoming materials are not upgraded enough')
		data = await self.try_iron(world, unique_id, -1 * skill_upgrade_number * standard_iron_count)
		if int(data['status']) == 1:
			return self._message_typesetting(97, 'Insufficient materials, upgrade failed')
		sql_str = 'UPDATE weapon SET '
		for i in range(len(head)):
			if head[i] != 'unique_id' and head[i] != 'weapon_name':
				sql_str += head[i] + '=' + str(row[i]) + ','
		sql_str = sql_str[:-1] + f' WHERE unique_id = "{unique_id}" AND weapon_name = "{weapon}"'
		if await self._execute_statement_update(world, sql_str) == 0:
			return self._message_typesetting(98, 'Database operation error')
		remaining = {'iron' : data['remaining']}
		for i in range(len(head)):
			remaining.update({head[i] : row[i]})
		remaining.pop('unique_id')
		return self._message_typesetting(status=0, message='success', data={'remaining': remaining})

	@C.collect_async
	async def level_up_passive(self, world: int, unique_id: str, weapon: str, passive: str) -> dict:
		# - 0 - Success
		# - 94 - Invalid weapon name
		# - 96 - User does not have that weapon
		# - 97 - Insufficient skill points, upgrade failed
		# - 98 - Database operation error
		# - 99 - Passive skill does not exist
		if weapon not in self._weapon_config["weapons"]:
			return self._message_typesetting(status=94, message="Invalid weapon name")
		row = await self._get_row_by_id(world, weapon, unique_id)
		if row[2] == 0:
			return self._message_typesetting(status=96, message="User does not have that weapon")
		valid_passive_skills = self._weapon_config["valid_passive_skills"]
		if passive not in valid_passive_skills:
			return self._message_typesetting(status=99, message="Passive skill does not exist")
		data_tuple = (await self.get_all_head(world, 'weapon'))["remaining"]
		head = [x[0] for x in data_tuple]
		row = await self._get_row_by_id(world, weapon, unique_id)
		point_count = head.index("skill_point")
		passive_count = head.index(passive)
		if row[point_count] == 0:
			return self._message_typesetting(status=97, message="Insufficient skill points, upgrade failed")
		row[point_count] -= 1
		row[passive_count] += 1
		sql_str = 'UPDATE weapon SET '
		for i in range(len(head)):
			if head[i] != 'unique_id' and head[i] != 'weapon_name':
				sql_str += head[i] + '=' + str(row[i]) + ','
		sql_str = sql_str[:-1] + f' WHERE unique_id = "{unique_id}" AND weapon_name = "{weapon}"'
		if await self._execute_statement_update(world, sql_str) == 0:
			return self._message_typesetting(98, 'Database operation error')
		remaining = {}
		for i in range(len(head)):
			remaining.update({head[i] : row[i]})
		remaining.pop('unique_id')
		return self._message_typesetting(status=0, message="success", data={"remaining": remaining})

	@C.collect_async
	async def level_up_weapon_star(self, world: int, unique_id: str, weapon: str) -> dict:
		# - 0 - Weapon upgrade success
		# - 98 - insufficient segment, upgrade failed
		# - 99 - Skill has been reset or database operation error!
		data_tuple = (await self.get_all_head(world, 'weapon'))["remaining"]
		head = [x[0] for x in data_tuple]
		row = await self._get_row_by_id(world, weapon, unique_id)

		star_count = head.index('weapon_star')
		segment_count = self._weapon_config["standard_segment_count"] * (1 + row[star_count])

		if int(row[head.index("segment")]) < segment_count:
			return self._message_typesetting(98, "Insufficient segments, upgrade failed!")

		row[head.index("segment")] = int(row[head.index("segment")]) - segment_count
		row[star_count] += 1
		sql_str = 'UPDATE weapon SET '
		for i in range(len(head)):
			if head[i] != 'unique_id' and head[i] != 'weapon_name':
				sql_str += head[i] + '=' + str(row[i]) + ','
		sql_str = sql_str[:-1] + f' WHERE unique_id = "{unique_id}" AND weapon_name = "{weapon}"'
		if await self._execute_statement_update(world, sql_str) == 0:
			return self._message_typesetting(99, 'Skill has been reset or database operation error!')
		remaining = {}
		for i in range(len(head)):
			remaining.update({head[i]: row[i]})
		remaining.pop('unique_id')
		return self._message_typesetting(0, weapon + " upgrade success!", {"remaining": remaining})

	@C.collect_async
	async def reset_weapon_skill_point(self, world: int, unique_id: str, weapon: str) -> dict:
		# - 0 - Success
		# - 94 - Invalid weapon name
		# - 97 - no weapon
		# - 98 - insufficient gold coins, upgrade failed
		# - 99 - database operation error!

		if weapon not in self._weapon_config["weapons"]:
			return self._message_typesetting(status=94, message="Invalid weapon name")
		row = await self._get_row_by_id(world, weapon, unique_id)
		if row[2] == 0:
			return self._message_typesetting(97, 'no weapon')
		data = await self.try_coin(world, unique_id, -1 * self._weapon_config["standard_reset_weapon_skill_coin_count"])
		if int(data["status"]) == 1:
			return self._message_typesetting(98, "Insufficient gold coins, upgrade failed")

		data_tuple = (await self.get_all_head(world, 'weapon'))["remaining"]
		head = [x[0] for x in data_tuple]

		row[head.index("skill_point")] = row[head.index("weapon_level")]
		row[head.index("passive_skill_1_level")] = row[head.index("passive_skill_2_level")] = row[head.index("passive_skill_3_level")] = row[head.index("passive_skill_4_level")] = 0

		sql_str = 'UPDATE weapon SET '
		for i in range(len(head)):
			if head[i] != 'unique_id' and head[i] != 'weapon_name':
				sql_str += head[i] + '=' + str(row[i]) + ','
		sql_str = sql_str[:-1] + f' WHERE unique_id = "{unique_id}" AND weapon_name = "{weapon}"'

		if await self._execute_statement_update(world, sql_str) == 0:
			return self._message_typesetting(99, 'Database operation error')

		remaining = {'coin' : data['remaining']}
		for i in range(len(head)):
			remaining.update({head[i]: row[i]})
		remaining.pop('unique_id')
		return self._message_typesetting(0, weapon + " reset skill point success!", {"remaining": remaining})

	# TODO CHECK FOR SPEED IMPROVEMENTS
	@C.collect_async
	async def get_all_weapon(self, world: int, unique_id: str) -> dict:
		# - 0 - gain success
		data_tuple = (await self.get_all_head(world, "weapon"))["remaining"]
		col_name_list = [x[0] for x in data_tuple]

		row = await self._execute_statement(world, f'SELECT * FROM weapon WHERE unique_id = "{unique_id}";')
		remaining = {}
		for i in range(0, len(row)):
			weapon = {}
			for j in range(2, len(row[i])):
				weapon.update({col_name_list[j] : row[i][j]})
			remaining.update({row[i][1] : weapon})
		return self._message_typesetting(0, "gain success", {"remaining": remaining})

	# TODO INTERNAL USE only?????
	async def try_unlock_weapon(self, world: int, unique_id: str, weapon: str) -> dict:
		# - 0 - Unlocked new weapon!   ===> {"keys": ['weapon', 'star', 'segment'], "values": [weapon, star, segment]}
		# - 1 - Weapon already unlocked, got free segment   ===>  {"keys": ['weapon', 'star', 'segment'], "values": [weapon, star, segment]}
		# - 99 - Invalid weapon name
		if weapon not in self._weapon_config["weapons"]:
			return self._message_typesetting(status=99, message="Invalid weapon name")
		row = await self._get_row_by_id(world=world, weapon=weapon, unique_id=unique_id)
		if row[2] != 0:  # weapon_star
			row[9] += self._weapon_config["standard_segment_count"]  # segment
			sql_str = f"update weapon set weapon_star={row[2]}, segment={row[9]} where unique_id='{unique_id}' and weapon_name='{weapon}'"
			await self._execute_statement_update(world=world, statement=sql_str)
			return self._message_typesetting(1, 'Weapon already unlocked, got free segment!', {"keys": ['weapon', 'star', 'segment'], "values": [weapon, row[2], row[9]]})
		else:
			row[2] += 1  # weapon_star
			sql_str = f"update weapon set weapon_star={row[2]}, segment={row[9]} where unique_id='{unique_id}' and weapon_name='{weapon}'"
			await self._execute_statement_update(world=world, statement=sql_str)
			return self._message_typesetting(0, 'Unlocked new weapon!', {"keys": ["weapon", 'star', 'segment'], "values": [weapon, row[2], row[9]]})

	async def try_unlock_role(self, world: int, unique_id: str, role: str) -> dict:
		# - 0 - Unlocked new role!   ===> {"keys": ['role', 'star', 'segment'], "values": [role, star, segment]}
		# - 1 - Role already unlocked, got free segment   ===>  {"keys": ['role', 'star', 'segment'], "values": [role, star, segment]}
		# - 99 - Invalid role name
		if role not in self._role_config["roles"]:
			return self._message_typesetting(status=99, message="Invalid role name")
		row = await self._get_role_row_by_id(world=world, role=role, unique_id=unique_id)
		if row[2] != 0:  # role_star
			row[9] += self._role_config["standard_segment_count"]  # segment
			sql_str = f"update role set role_star={row[2]}, segment={row[9]} where unique_id='{unique_id}' and role_name='{role}'"
			await self._execute_statement_update(world=world, statement=sql_str)
			return self._message_typesetting(1, 'Role already unlocked, got free segment', {'keys' : ['role', 'star', 'segment'], 'values' : [role, row[2], row[9]]})
		else:
			row[2] += 1  # role_star
			sql_str = f"update role set role_star={row[2]}, segment={row[9]} where unique_id='{unique_id}' and role_name='{role}'"
			await self._execute_statement_update(world=world, statement=sql_str)
			return self._message_typesetting(0, 'Unlocked new role!', {'keys' : ['role', 'star', 'segment'], 'values' : [role, row[2], row[9]]})

	@C.collect_async
	async def disintegrate_weapon(self, world: int, unique_id: str, weapon: str) -> dict:
		# 0 - successful weapon decomposition
		# 96 - User does not have that weapon
		# 97 - insufficient diamond
		# 98 - self._player is not updated
		# 99 - database operation error
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
			return self._message_typesetting(status=96, message="User does not have this weapon")
		#  能分解武器的情况下再扣钻石
		diamond_data = await self.try_diamond(world=world, unique_id=unique_id, value=-1*int(cost["diamond"]))
		if int(diamond_data["status"]) == 1:
			return self._message_typesetting(status=97, message="Insufficient diamond")
		reward_weapon_name = weapon
		for i in range(len(weapon_tier)):
			if weapon in weapon_tier[i]:
				key = random.randint(0, len(weapon_tier[i]) - 1)
				while weapon == weapon_tier[i][key]:
					key = random.randint(0, len(weapon_tier[i]) - 1)
				reward_weapon_name = weapon_tier[i][key]  # 增加武器碎片的武器
				break
		if weapon == reward_weapon_name:
			return self._message_typesetting(status=98, message="self._player not updated")
		#  数据库操作
		star_code = await self._set_weapon_star(world=world, unique_id=unique_id, weapon=weapon, star=0)  # 武器星数至0

		reward_weapon_segment = star * int(reward["segment"])  # 计算奖励武器的碎片数量
		#  构造更新语句和查询语句
		update_str = f"update weapon set segment=segment+{reward_weapon_segment} where unique_id='{unique_id}' and weapon_name='{reward_weapon_name}'"
		select_str = f"select segment from weapon where unique_id='{unique_id}' and weapon_name='{reward_weapon_name}'"
		update_code = await self._execute_statement_update(world=world, statement=update_str)

		select_result = await self._execute_statement(world=world, statement=select_str)  # 获取含有碎片的查询的结果
		coin_data = await self.try_coin(world=world, unique_id=unique_id, value=int(reward["coin"])) # 获取添加金币之后的金币数量
		if star_code == 0 or update_code == 0 or int(coin_data["status"]) == 1:
			return self._message_typesetting(status=99, message="database operating error ==> update_code: %s, star_code: %s, json_status: %s" % (update_code, star_code, coin_data["status"]))
		data = {
			"remaing": {
				"cost_weapon": weapon,  # 武器分解的名字
				"cost_star": 0,  # 武器分解之后的星数
				"coin": coin_data["remaining"],  # player表中金币的剩余数量
				"diamond": diamond_data["remaining"],  # player表中钻石的剩余数量
				"reward_weapon": reward_weapon_name,  # 奖励碎片的武器名字
				"reward_segment": select_result[0][0]  # 碎片的剩余数量
			},
			"reward": {
				"coin": reward["coin"],  # 分解武器奖励的金币
				"reward_weapon": reward_weapon_name,  # 奖励碎片的武器名字
				"reward_segment": reward_weapon_segment  # 奖励碎片的数量
			}
		}
		return self._message_typesetting(status=0, message="Successful weapon decomposition", data=data)

#############################################################################
#						End Weapon Module Functions							#
#############################################################################


#############################################################################
#						Start Role Module Functions							#
#############################################################################

	@C.collect_async
	async def upgrade_role_level(self, world: int, unique_id: str, role: str, experience_potion: int) -> dict:
		# - 0 - Success
		# - 94 - Invalid role name
		# - 95 - User does not have that role
		# - 96 - Incoming materials are not upgraded enough
		# - 97 - Insufficient materials, upgrade failed
		# - 98 - Database operation error
		# - 99 - role already max level
		if role not in self._role_config["roles"]:
			return self._message_typesetting(status=94, message="Invalid role name")
		row = await self._get_role_row_by_id(world, role, unique_id)
		if row[2] == 0:
			return self._message_typesetting(95, 'User does not have that role')
		if row[3] == 100:
			return self._message_typesetting(status=99, message='role already max level')

		standard_experience_potion_count = self._role_config['standard_experience_potion_count']
		skill_upgrade_number = experience_potion // standard_experience_potion_count
		data_tuple = (await self.get_all_head(world, 'role'))['remaining']
		head = [x[0] for x in data_tuple]
		level_count = head.index('role_level')
		point_count = head.index('skill_point')
		if (row[level_count] + skill_upgrade_number) > 100:
			skill_upgrade_number = 100 - row[level_count]
		row[level_count] += skill_upgrade_number
		row[point_count] += skill_upgrade_number

		if skill_upgrade_number == 0:
			return self._message_typesetting(status=96, message='Incoming materials are not upgraded enough')
		data = await self.try_experience_potion(world, unique_id, -1 * skill_upgrade_number * standard_experience_potion_count)
		if int(data['status']) == 1:
			return self._message_typesetting(97, 'Insufficient materials, upgrade failed')
		sql_str = 'UPDATE role SET '
		for i in range(len(head)):
			if head[i] != 'unique_id' and head[i] != 'role_name':
				sql_str += head[i] + '=' + str(row[i]) + ','
		sql_str = sql_str[:-1] + f' WHERE unique_id = "{unique_id}" AND role_name = "{role}"'
		if await self._execute_statement_update(world, sql_str) == 0:
			return self._message_typesetting(98, 'Database operation error')
		remaining = {'experience_potion' : data['remaining']}
		for i in range(len(head)):
			remaining.update({head[i] : row[i]})
		remaining.pop('unique_id')
		return self._message_typesetting(status=0, message='success', data={'remaining': remaining})

	@C.collect_async
	async def upgrade_role_star(self, world: int, unique_id: str, role: str) -> dict:
		# - 0 - role upgrade success
		# - 94 - Invalid role name
		# - 98 - insufficient segment, upgrade failed
		# - 99 - Skill has been reset or database operation error!
		if role not in self._role_config["roles"]:
			return self._message_typesetting(status=94, message="Invalid role name")
		data_tuple = (await self.get_all_head(world, 'role'))["remaining"]
		head = [x[0] for x in data_tuple]
		row = await self._get_role_row_by_id(world, role, unique_id)

		star_count = head.index('role_star')
		segment_count = self._role_config["standard_segment_count"] * (1 + row[star_count])

		if int(row[head.index("segment")]) < segment_count:
			return self._message_typesetting(98, "Insufficient segments, upgrade failed!")

		row[head.index("segment")] = int(row[head.index("segment")]) - segment_count
		row[star_count] += 1
		sql_str = 'UPDATE role SET '
		for i in range(len(head)):
			if head[i] != 'unique_id' and head[i] != 'role_name':
				sql_str += head[i] + '=' + str(row[i]) + ','
		sql_str = sql_str[:-1] + f' WHERE unique_id = "{unique_id}" AND role_name = "{role}"'
		if await self._execute_statement_update(world, sql_str) == 0:
			return self._message_typesetting(99, 'Skill has been reset or database operation error!')
		remaining = {}
		for i in range(len(head)):
			remaining.update({head[i]: row[i]})
		remaining.pop('unique_id')
		return self._message_typesetting(0, role + " upgrade success!", {"remaining": remaining})

	async def get_all_roles(self, world: int, unique_id: str) -> dict:
		# - 0 - Get all the role information
		data_tuple = (await self.get_all_head(world, 'role'))["remaining"]
		head = [x[0] for x in data_tuple]
		content = await self._execute_statement(world, f'SELECT * FROM role WHERE unique_id = "{unique_id}"')
		remaining = []
		for i in range(len(content)):
			role_info = {}
			for j in range(1, len(head)):
				role_info.update({head[j]: content[i][j]})
			remaining.append(role_info)
		return self._message_typesetting(0, "Get all the role information", {"remaining": remaining})

	def get_role_config(self) -> dict:
		# - 0 - Get role configuration information
		return self._message_typesetting(0, "Get role configuration information", {"remaining": {"role_config": self._role_config}})

#############################################################################
#						End Role Module Functions							#
#############################################################################

#############################################################################
#						Stage Module Functions								#
#############################################################################

	# TODO CHECK SPEED IMPROVEMENTS
	@C.collect_async
	async def enter_stage(self, world: int, unique_id: str, stage: int) -> dict:
		# 0 - success
		# 97 - Insufficient energy
		# 98 - key insufficient
		# 99 - parameter error
		enter_stage_data = self._entry_consumables["stage"]
		if stage <= 0 or stage > int(await self._get_material(world,  unique_id, "stage")) + 1:
			return self._message_typesetting(99, "Parameter error")
		stages = [int(x) for x in enter_stage_data.keys()]
		if stage not in stages: stage = max(stages)
		keys = list(enter_stage_data[str(stage)].keys())
		values = [-1*int(v) for v in list(enter_stage_data[str(stage)].values())]
		remaining = {}
		material_dict = {}
		for i in range(len(keys)):
			material_dict.update({keys[i]: values[i]})
		update_str, select_str = self._sql_str_operating(unique_id, material_dict)
		select_values = (await self._execute_statement(world, select_str))[0]
		for i in range(len(select_values)):
			values[i] = int(values[i]) + int(select_values[i])
			if values[i] < 0:
				return self._message_typesetting(98, "%s insufficient" % keys[i])
		if "energy" in keys:
			energy_data = await self.try_energy(world=world, unique_id=unique_id, amount=material_dict["energy"])
			if energy_data["status"] >= 97:
				return self._message_typesetting(status=97, message="Insufficient energy")
			values.pop(keys.index("energy"))
			keys.remove("energy")
			material_dict.pop("energy")
			for i in range(len(energy_data["data"]["keys"])):
				remaining.update({energy_data["data"]["keys"][i]: energy_data["data"]["values"][i]})

		if material_dict:
			update_str, select_str = self._sql_str_operating(unique_id, material_dict)
			await self._execute_statement_update(world, update_str)
		for i in range(len(keys)):
			remaining.update({keys[i]: values[i]})
		return self._message_typesetting(0, "success", {"remaining": remaining})

	@C.collect_async
	async def pass_stage(self, world: int, unique_id: str, stage: int, clear_time: str) -> dict:
		# success ===> 0
		# 0 : passed customs ===> success
		# 98 : database operation error
		# 99 : abnormal data!
		json_data = await self.try_pass_stage(world, unique_id, stage)
		status = int(json_data["status"])
		if status == 9:
			return self._message_typesetting(status=99, message="abnormal data!")
		elif status == 1:
			return self._message_typesetting(status=98, message="database operation error")
		else:
			reward = json_data["remaining"][0]
			keys = list(reward.keys())
			values = json_data["remaining"][1]
			remaining = {}
			for i in range(len(keys)):
				remaining.update({keys[i]: values[i]})
			reward.pop("stage")
			return self._message_typesetting(status=0, message="passed customs!", data={"remaining": remaining, "reward": reward})

	@C.collect_async
	async def enter_tower(self, world: int, unique_id: str, stage: int) -> dict:
		# 0 - success
		# 97 - Insufficient energy
		# 98 - key insufficient
		# 99 - parameter error
		enter_tower_data = self._entry_consumables["tower"]
		if stage <= 0 or stage > int(await self._get_material(world,  unique_id, "tower_stage")) + 1:
			return self._message_typesetting(99, "Parameter error")
		stages = [int(x) for x in enter_tower_data.keys()]
		if stage not in stages: stage = max(stages)
		keys = list(enter_tower_data[str(stage)].keys())
		values = [-1*int(v) for v in list(enter_tower_data[str(stage)].values())]
		remaining = {}
		material_dict = {}
		for i in range(len(keys)):
			material_dict.update({keys[i]: values[i]})
		update_str, select_str = self._sql_str_operating(unique_id, material_dict)
		select_values = (await self._execute_statement(world, select_str))[0]
		for i in range(len(select_values)):
			values[i] = int(values[i]) + int(select_values[i])
			if values[i] < 0:
				return self._message_typesetting(98, "%s insufficient" % keys[i])
		if "energy" in keys:
			energy_data = await self.try_energy(world=world, unique_id=unique_id, amount=material_dict["energy"])
			if energy_data["status"] >= 97:
				return self._message_typesetting(status=97, message="Insufficient energy")
			values.pop(keys.index("energy"))
			keys.remove("energy")
			material_dict.pop("energy")
			for i in range(len(energy_data["data"]["keys"])):
				remaining.update({energy_data["data"]["keys"][i]: energy_data["data"]["values"][i]})
		if material_dict:
			update_str, select_str = self._sql_str_operating(unique_id, material_dict)
			await self._execute_statement_update(world, update_str)
		for i in range(len(keys)):
			remaining.update({keys[i]: values[i]})
		return self._message_typesetting(0, "success", {"remaining": remaining})

	@C.collect_async
	async def pass_tower(self, world: int, unique_id: str, stage: int, clear_time: str) -> dict:
		# 0 - Earn rewards success
		# 1 - Successfully unlock new skills
		# 2 - Gain a scroll
		# 3 - Gain weapon fragments
		# 94 - weapon -> database operating error
		# 95 - skill -> database operating error
		# 96 - Accidental prize -> key
		# 97 - pass_tower_data -> database operation error
		# 99 - parameter error
		pass_tower_data = self._stage_reward["tower"]
		sql_stage = int(await self._get_material(world,  unique_id, "tower_stage"))
		if stage <= 0 or stage > sql_stage + 1:
			return self._message_typesetting(99, "Parameter error")

		stages = [int(x) if str.isdigit(x) else 1 for x in pass_tower_data.keys()]
		if stage not in stages:
			if stage % 10 != 0:
				while max(stages) % 10 == 0:
					stages.remove(max(stages))
			else:
				while max(stages) % 10 != 0:
					stages.remove(max(stages))
			tower_reward = pass_tower_data[str(max(stages))]
		else:
			tower_reward = pass_tower_data[str(stage)]
		if stage % 10 != 0:
			material_dict = {"tower_stage": 0}
			remaining = {}
			for key, value in tower_reward.items():
				if "energy" == key:
					energy_data = await self.try_energy(world=world, unique_id=unique_id, amount=value)
					keys, values = energy_data["data"]["keys"], energy_data["data"]["values"]
					for i in range(len(keys)):
						remaining.update({keys[i]: values[i]})
				else:
					material_dict.update({key: value})
			if sql_stage + 1 == stage:  # 通过新关卡
				material_dict.update({"tower_stage": 1})
			update_str, select_str = self._sql_str_operating(unique_id, material_dict)
			if await self._execute_statement_update(world, update_str) == 0:
				return self._message_typesetting(status=97, message="pass_tower_data -> database operating error")
			keys = list(material_dict.keys())
			values = list((await self._execute_statement(world=world, statement=select_str))[0])
			for i in range(len(keys)):
				remaining.update({keys[i]: values[i]})
			material_dict.pop("tower_stage")
			return self._message_typesetting(status=0, message="Earn rewards success", data={"remaining": remaining, "reward": material_dict})
		else:
			reward = random.choices(population=tower_reward)[0]
			if reward in pass_tower_data["skill"]:
				reward_data = await self.try_unlock_skill(world=world, unique_id=unique_id, skill_id=reward)
				if reward_data["status"] == 0:
					tower_stage = (await self._try_material(world=world, unique_id=unique_id, material="tower_stage", value=1 if sql_stage + 1 == stage else 0))["remaining"]
					return self._message_typesetting(status=1, message="Successfully unlock new skills", data={"remaining": {reward: 1, "tower_stage": tower_stage}, "reward": {reward: 1}})
				else:
					scroll = random.choices(population=pass_tower_data["skill_scroll"], weights=pass_tower_data["weights"])[0]
					scroll_data = await self._try_material(world=world, unique_id=unique_id, material=scroll, value=1)
					if scroll_data["status"] == 1:
						return self._message_typesetting(status=95, message="skill -> database operating error")
					tower_stage = (await self._try_material(world=world, unique_id=unique_id, material="tower_stage", value=1 if sql_stage + 1 == stage else 0))["remaining"]
					return self._message_typesetting(status=2, message="Gain a scroll", data={"remaining": {scroll: scroll_data["remaining"], "tower_stage": tower_stage}, "reward": {scroll: 1}})
			elif reward in pass_tower_data["weapon"]:  # weapon
				if len(pass_tower_data["segment"]) == 2:
					segment = random.randint(pass_tower_data["segment"][0], pass_tower_data["segment"][1])
				else:
					segment = pass_tower_data["segment"][0]
				sql_str = "update %s set segment=segment+%s where unique_id='%s'" % (reward, segment, unique_id)
				if await self._execute_statement_update(world=world, statement=sql_str) == 0:
					return self._message_typesetting(status=94, message="weapon -> database operating error")
				segment_result = await self._get_segment(world=world, unique_id=unique_id, weapon=reward)
				tower_stage = (await self._try_material(world=world, unique_id=unique_id, material="tower_stage", value=1 if sql_stage + 1 == stage else 0))["remaining"]
				return self._message_typesetting(status=3, message="Gain weapon fragments", data={"remaining": {"weapon": reward, "segment": segment_result, "tower_stage": tower_stage}, "reward": {"segment": segment}})
			else:
				return self._message_typesetting(status=96, message="Accidental prize -> " + reward)

	async def get_all_stage_info(self):
		# 0 - got all stage info
		# 99 - configration is empty
		if self._entry_consumables == "":
			return self._message_typesetting(99, 'configration is empty')
		return self._message_typesetting(0, 'got all stage info', data={"remaining": self._entry_consumables})

	@C.collect_async
	async def start_hang_up(self, world: int, unique_id: str, stage: int) -> dict:
		"""
		success ===> 0 , 1
		# 0 - hang up success
		# 1 - Repeated hang up successfully
		# 98 - database operating error
		# 99 - Parameter error
		1分钟奖励有可能奖励1颗钻石，30颗金币，10个铁
		minute = 1 ==> reward 0 or 1 diamond and 30 coin and 10 iron
		minute = 2 ==> reward 0 or 1 or 2 diamond and 60 coin and 20 iron
		"""
		if stage <= 0 or stage > int(await self._get_material(world=world,  unique_id=unique_id, material="stage")):
			return self._message_typesetting(status=99, message="Parameter error")
		sql_str = "SELECT hang_up_time,hang_stage FROM player WHERE unique_id='%s'" % unique_id
		key_list = await self._execute_statement(world=world, statement=sql_str)
		hang_up_time, hang_stage = key_list[0]
		current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		# 此时的material_dict字典的值是给奖励列表的，
		# 所以hang_stage是奖励之前的关卡，
		# hang_up_time是之前挂起的开始时间
		probability_reward = self._hang_reward["probability_reward"]
		material_dict = {}
		probability_dict = {}
		for key, value in self._hang_reward[str(hang_stage)].items():
			if key in probability_reward: probability_dict.update({key: value})
			else: material_dict.update({key: value})
		material_dict.update({"hang_stage": hang_stage})
		material_dict.update({"hang_up_time": hang_up_time})
		key_word = ["hang_stage", "hang_up_time"]
		if hang_up_time == "":
			material_dict.update({"hang_up_time": current_time})
			material_dict.update({"hang_stage": stage})
			# 下面的功能是将奖励拿出来，并且将数据库剩余的值发送给客户端
			keys = list(material_dict.keys())
			update_str, select_str = self._sql_str_operating(unique_id=unique_id, material_dict=material_dict, key_word=key_word)
			if await self._execute_statement_update(world=world, statement=update_str) == 0:
				return self._message_typesetting(status=98, message="database operating error")
			data = await self._execute_statement(world=world, statement=select_str)
			remaining = {"hang_up_time_seconds": 0}
			for i in range(len(keys)):
				remaining.update({keys[i]: data[0][i]})
			return self._message_typesetting(status=0, message="hang up success", data={"remaining": remaining})
		else:
			delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(hang_up_time, '%Y-%m-%d %H:%M:%S')
			minute = int(delta_time.total_seconds()) // 60
			current_time = (datetime.strptime(hang_up_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=minute)).strftime("%Y-%m-%d %H:%M:%S")

			for key in material_dict.keys():
				if key not in key_word:
					material_dict[key] = int(material_dict[key]) * minute

			for key, value in probability_dict.items():  # 完成minute次十万分之value[1]的概率抽到value[0]个特殊的key奖励
				material_dict.update({key: sum(random.choices(value[1]*[value[0]] + (100000 - value[1])*[0], k=minute))})
			keys = list(material_dict.keys())

			# 此时的material_dict中的数据是用于数据库操作的数据
			material_dict.update({"hang_stage": stage})
			material_dict.update({"hang_up_time": current_time})

			update_str, select_str = self._sql_str_operating(unique_id=unique_id, material_dict=material_dict, key_word=key_word)
			await self._execute_statement_update(world=world, statement=update_str)
			data = await self._execute_statement(world=world, statement=select_str)

			delta_time = datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), '%Y-%m-%d %H:%M:%S') - datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
			remaining = {"hang_up_time_seconds": int(delta_time.total_seconds())}
			for i in range(len(keys)):
				remaining.update({keys[i]: data[0][i]})
			material_dict.update({"hang_stage": hang_stage})
			material_dict.update({"hang_up_time": hang_up_time})
			return self._message_typesetting(status=1, message="Repeated hang up successfully", data={"remaining": remaining, "reward": material_dict})

	@C.collect_async
	async def get_hang_up_reward(self, world: int, unique_id: str) -> dict:
		"""
		success ===> 0
		# 0 - Settlement reward success
		# 99 - Temporarily no on-hook record
		"""
		sql_str = "SELECT hang_up_time,hang_stage FROM player WHERE unique_id='%s'" % unique_id
		key_list = await self._execute_statement(world=world, statement=sql_str)
		hang_up_time, hang_stage = key_list[0]
		current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		if hang_up_time == "" or int(hang_stage) == 0:
			return self._message_typesetting(status=99, message="Temporarily no on-hook record")
		else:
			# 此时的material_dict字典的值是给奖励列表的，
			# 所以hang_stage是奖励之前的关卡，
			# hang_up_time是之前挂起的开始时间
			probability_reward = self._hang_reward["probability_reward"]
			material_dict = {}
			probability_dict = {}
			for key, value in self._hang_reward[str(hang_stage)].items():
				if key in probability_reward: probability_dict.update({key: value})
				else: material_dict.update({key: value})
			material_dict.update({"hang_stage": hang_stage})
			material_dict.update({"hang_up_time": hang_up_time})
			key_word = ["hang_stage", "hang_up_time"]

			delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(hang_up_time, '%Y-%m-%d %H:%M:%S')
			minute = int(delta_time.total_seconds()) // 60
			current_time = (datetime.strptime(hang_up_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=minute)).strftime("%Y-%m-%d %H:%M:%S")

			for key in material_dict.keys():
				if key not in key_word:
					material_dict[key] = int(material_dict[key]) * minute

			for key, value in probability_dict.items():  # 完成minute次十万分之value[1]的概率抽到value[0]个特殊的key奖励
				material_dict.update({key: sum(random.choices(value[1]*[value[0]] + (100000 - value[1])*[0], k=minute))})
			keys = list(material_dict.keys())

			# 此时的material_dict中的数据是用于数据库操作的数据
			material_dict.update({"hang_up_time": current_time})

			update_str, select_str = self._sql_str_operating(unique_id=unique_id, material_dict=material_dict, key_word=key_word)
			await self._execute_statement_update(world=world, statement=update_str)
			data = await self._execute_statement(world=world, statement=select_str)

			delta_time = datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), '%Y-%m-%d %H:%M:%S') - datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
			remaining = {"hang_up_time_seconds": int(delta_time.total_seconds())}
			for i in range(len(keys)):
				remaining.update({keys[i]: data[0][i]})
			material_dict.update({"hang_up_time": hang_up_time})
			return self._message_typesetting(status=0, message="Settlement reward success", data={"remaining": remaining, "reward": material_dict})

	@C.collect_async
	async def get_hang_up_info(self, world: int, unique_id: str) -> dict:
		"""
		success ===> 0
		# 0 - get hang up info
		# 99 - This data does not exist in the database
		"""
		sql_str = "SELECT hang_up_time, hang_stage, stage, tower_stage FROM player WHERE unique_id='%s'" % unique_id
		data = await self._execute_statement(world=world, statement=sql_str)
		if not data: return self._message_typesetting(99, 'This data does not exist in the database')
		hang_up_time, hang_stage, stage, tower_stage = data[0]
		current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		if hang_up_time=="": hang_up_time = current_time
		delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(hang_up_time, '%Y-%m-%d %H:%M:%S')
		return self._message_typesetting(status=0, message="get hang up info", data={"remaining": {"tower_stage":tower_stage,"stage":stage,"hang_up_time": hang_up_time, "hang_stage": hang_stage, "hang_up_time_seconds": int(delta_time.total_seconds())}})

	def get_monster_info(self) -> dict:
		"""
		# 0 - Get all monster information to get success
		"""
		return self._message_typesetting(status=0, message="Get all monster information to get success", data={"remaining": {"monster_config": self._monster_config_json}})

	async def get_stage_info(self, world: int, unique_id: str) -> dict:
		"""
		# 0 - Successfully obtained level information
		# 1 - No information found for this user, successfully obtained general level configuration information
		"""
		server_config = {
			"entry_consumables": self._entry_consumables,
			"hang_reward": self._hang_reward,
			"stage_reward": self._stage_reward,
			"level_enemy_layouts": self._level_enemy_layouts_config_json,
			"world_boss": self._world_boss
		}
		remaining = {"server_config": server_config}
		data = await self._execute_statement(world, f"select stage, tower_stage, hang_stage, hang_up_time from player where unique_id='{unique_id}'")
		if data:
			stage, tower_stage, hang_stage, hang_up_time = data[0]
			sql_data = {"stage": stage, "tower_stage": tower_stage, "hang_stage": hang_stage, "hang_up_time": hang_up_time}
			remaining.update({"sql_data": sql_data})
			return self._message_typesetting(status=0, message="Successfully obtained level information", data={"remaining": remaining})
		return self._message_typesetting(status=1, message="No information found for this user, successfully obtained general level configuration information", data={"remaining": remaining})


	@C.collect_async
	async def show_energy(self, world: int, unique_id: str):
		data = await self.try_energy(world=world, unique_id=unique_id, amount=0)
		_data = data["data"]
		if "keys" in _data:
			keys = _data["keys"]
			values = _data["values"]
			data_dict = {}
			for i in range(len(keys)):
				data_dict.update({keys[i]: values[i]})
			data["data"] = {"remaining": data_dict}
		return data

	@C.collect_async
	async def upgrade_armor(self, world: int, unique_id: str, armor_id: str, level: int) -> dict:
		"""
		# success ===> 0
		# 0 - Successful synthesis
		# 97 - database operation error
		# 98 - Insufficient basic armor
		# 99 - parameter error
		:param armor_id: 盔甲种类，代表armor1、armor2、armor3   ......
		:param level: 盔甲种类下的等级，代表armor_level1、armor_level2、armor_level3   ......
		:return: dict
		"""
		if level < 1 or level > 9:
			return self._message_typesetting(status=99, message="Parameter error")
		armor1, armor2 = f"armor_level{level}", f"armor_level{level + 1}"
		armor = {"armor_id": armor_id, armor1: 0, armor2: 0}
		armor[armor1], armor[armor2] = await self._get_armor(world=world, unique_id=unique_id, armor_id=armor_id, armor1=armor1, armor2=armor2)
		if armor[armor1] < 3:
			return self._message_typesetting(status=98, message="Insufficient basic armor")
		else:
			armor[armor1] -= 3
			armor[armor2] += 1
			sql_str = f"update armor set {armor1}={armor[armor1]}, {armor2}={armor[armor2]} where unique_id='{unique_id}' and armor_id='{armor_id}'"
			if await self._execute_statement_update(world=world, statement=sql_str) == 0:
				return self._message_typesetting(status=97, message="database operating error")
			return self._message_typesetting(status=0, message="Successful synthesis", data={"remaining": armor})

	async def _get_armor(self, world: int, unique_id: str, armor_id: str, armor1: str, armor2: str) -> tuple:
		sql_str = f"select {armor1}, {armor2} from armor where unique_id='{unique_id}' and armor_id='{armor_id}'"
		data = await self._execute_statement(world=world, statement=sql_str)
		if data:
			return data[0]
		else:
			await self._execute_statement_update(world=world, statement=f"insert into armor(unique_id, armor_id) values ('{unique_id}','{armor_id}')")
			return (await self._execute_statement(world=world, statement=sql_str))[0]

	@C.collect_async
	async def get_all_armor_info(self, world: int, unique_id: str):
		# 0 - got all armor info
		result = await self._execute_statement(world, f"SELECT * FROM armor WHERE unique_id='{unique_id}';")
		remaining = {}
		for i in range(0,len(result)):
			remaining.update({result[i][1]:{}})
			for j in range(1,11):
				remaining[result[i][1]].update({"armor_level"+str(j):result[i][j+1]})
		# print("remaining="+str(remaining))
		return self._message_typesetting(0, 'got all armor info', data={"remaining": remaining})

	@C.collect_async
	async def automatically_refresh_store(self, world: int, unique_id: str) -> dict:
		"""
		success -> 0 and 1
		# 0 - First refresh market success
		# 1 - Refresh market success
		# 2 - Refresh time is not over yet, market information has been obtained
		# 98 - Unexpected element, please update the configuration table
		# 99 - database operation error
		"""
		dark_market_data = self._player['dark_market']
		merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity = await self._get_dark_market_material(world, unique_id, code = 1)

		remaining = {}
		if refresh_time == '':
			refreshable_quantity = 3
			refresh_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
			tier_choice = random.choices(dark_market_data['names'], dark_market_data['weights'], k = 8)
			key_list = [(random.choices(dark_market_data[tier], k = 1))[0] for tier in tier_choice]
			for i in range(len(key_list)):
				merchandise = key_list[i]
				code = i + 1
				if merchandise in dark_market_data['weapon']:
					currency_type = (random.choices(list(dark_market_data['segment'].keys()), k = 1))[0]
					merchandise_quantity = random.randint(int(dark_market_data['segment'][currency_type]['quantity_min']), int(dark_market_data['segment'][currency_type]['quantity_max']))
					currency_type_price = random.randint(int(dark_market_data['segment'][currency_type]['cost_range_min']), int(dark_market_data['segment'][currency_type]['cost_range_max']))
					if await self._set_dark_market_material(world, unique_id, code, merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity) == 0:
						return self._message_typesetting(99, 'database operation error')
				elif merchandise in dark_market_data['skill']:
					currency_type = (random.choices(list(dark_market_data['reward_skill'].keys()), k=1))[0]
					merchandise_quantity = 1
					currency_type_price = random.randint(int(dark_market_data['reward_skill'][currency_type]['cost_range_min']), int(dark_market_data['reward_skill'][currency_type]['cost_range_max']))
					if await self._set_dark_market_material(world, unique_id, code, merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity) == 0:
						return self._message_typesetting(99, 'database operation error')
				elif merchandise in dark_market_data['other'].keys():
					currency_type = (random.choices(list(dark_market_data['other'][merchandise].keys()), k=1))[0]
					merchandise_quantity = random.randint(int(dark_market_data['other'][merchandise][currency_type]['quantity_min']), int(dark_market_data['other'][merchandise][currency_type]['quantity_max']))
					if await self._set_dark_market_material(world, unique_id, code, merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity) == 0:
						return self._message_typesetting(99, 'database operating error')
				else:
					return self._message_typesetting(98, 'Unexpected element, please update the configuration table.')
				remaining.update({'merchandise%s' % code : merchandise, 'merchandise%s_quantity' % code : merchandise_quantity, 'currency_type%s' % code : currency_type, 'currency_type%s_price' % code : currency_type_price})
			remaining.update({'refresh_time' : refresh_time, 'refreshable_quantity' : int(refreshable_quantity)})
			return self._message_typesetting(0, 'First refresh market success', {'remaining' : remaining})
		else:
			current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
			delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(refresh_time, '%Y-%m-%d %H:%M:%S')
			if delta_time.total_seconds() // 3600 >= 3:
				frequency = delta_time.total_seconds() // 3600 // 3
				refreshable_quantity += frequency
				if refreshable_quantity > 3:
					refreshable_quantity = 3
				refresh_time = (datetime.strptime(refresh_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours = frequency*3)).strftime('%Y-%m-%d %H:%M:%S')

				tier_choice = random.choices(dark_market_data['names'], dark_market_data['weights'], k = 8)
				key_list = [(random.choices(dark_market_data[tier], k = 1))[0] for tier in tier_choice]
				for i in range(len(key_list)):
					merchandise = key_list[i]
					code = i + 1
					if merchandise in dark_market_data['weapon']:
						currency_type = (random.choices(list(dark_market_data['segment'].keys()), k = 1))[0]
						merchandise_quantity = random.randint(int(dark_market_data['segment'][currency_type]['quantity_min']), int(dark_market_data['segment'][currency_type]['quantity_max']))
						currency_type_price = random.randint(int(dark_market_data['segment'][currency_type]['cost_range_min']), int(dark_market_data['segment'][currency_type]['cost_range_max']))
						if await self._set_dark_market_material(world, unique_id, code, merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity) == 0:
							return self._message_typesetting(99, 'database operation error')
					elif merchandise in dark_market_data['skill']:
						currency_type = (random.choices(list(dark_market_data['reward_skill'].keys()), k=1))[0]
						merchandise_quantity = 1
						currency_type_price = random.randint(int(dark_market_data['reward_skill'][currency_type]['cost_range_min']), int(dark_market_data['reward_skill'][currency_type]['cost_range_max']))
						if await self._set_dark_market_material(world, unique_id, code, merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity) == 0:
							return self._message_typesetting(99, 'database operation error')
					elif merchandise in dark_market_data['other'].keys():
						currency_type = (random.choices(list(dark_market_data['other'][merchandise].keys()), k=1))[0]
						merchandise_quantity = random.randint(int(dark_market_data['other'][merchandise][currency_type]['quantity_min']), int(dark_market_data['other'][merchandise][currency_type]['quantity_max']))
						currency_type_price = random.randint(int(dark_market_data['other'][merchandise][currency_type]['cost_range_min']), int(dark_market_data['other'][merchandise][currency_type]['cost_range_max']))
						if await self._set_dark_market_material(world, unique_id, code, merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity) == 0:
							return self._message_typesetting(99, 'database operating error')
					else:
						return self._message_typesetting(98, 'Unexpected element, please update the configuration table.')
					remaining.update({'merchandise%s' % code : merchandise, 'merchandise%s_quantity' % code : merchandise_quantity, 'currency_type%s' % code : currency_type, 'currency_type%s_price' % code : currency_type_price})
				remaining.update({'refresh_time' : refresh_time, 'refreshable_quantity' : int(refreshable_quantity)})
				return self._message_typesetting(1, 'refresh market success', {'remaining' : remaining})
			else:
				headers = [x[0] for x in list(await self._execute_statement(world, 'desc dark_market;'))]
				content = (await self._execute_statement(world, f'SELECT * FROM dark_market WHERE unique_id = "{unique_id}";'))[0]
				for i in range(len(headers)):
					remaining.update({headers[i] : content[i]})
				remaining.pop('unique_id')
				return self._message_typesetting(2, 'Refresh time is not over yet, market information has been obtained', {'remaining' : remaining})

	@C.collect_async
	async def manually_refresh_store(self, world: int, unique_id: str) -> dict:
		"""
		# 0  - refresh market success
		# 97 - insufficient refreshable quantity
		# 98 - unexpected element, please update the configuration table
		# 99 - database operation error
		"""
		dark_market_data = self._player['dark_market']
		merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity = await self._get_dark_market_material(world, unique_id, code = 1)
		remaining = {}
		if refreshable_quantity > 0:
			if refreshable_quantity == 3:
				refresh_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
			refreshable_quantity -= 1
			tier_choice = random.choices(dark_market_data['names'], dark_market_data['weights'], k = 8)
			key_list = [(random.choices(dark_market_data[tier], k = 1))[0] for tier in tier_choice]
			for i in range(len(key_list)):
				merchandise = key_list[i]
				code = i + 1
				if merchandise in dark_market_data['weapon']:
					currency_type = (random.choices(list(dark_market_data['segment'].keys()), k = 1))[0]
					merchandise_quantity = random.randint(int(dark_market_data['segment'][currency_type]['quantity_min']), int(dark_market_data['segment'][currency_type]['quantity_max']))
					currency_type_price = random.randint(int(dark_market_data['segment'][currency_type]['cost_range_min']), int(dark_market_data['segment'][currency_type]['cost_range_max']))
					if await self._set_dark_market_material(world, unique_id, code, merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity) == 0:
						return self._message_typesetting(99, 'database operation error')
				elif merchandise in dark_market_data['skill']:
					currency_type = (random.choices(list(dark_market_data['reward_skill'].keys()), k=1))[0]
					merchandise_quantity = 1
					currency_type_price = random.randint(int(dark_market_data['reward_skill'][currency_type]['cost_range_min']), int(dark_market_data['reward_skill'][currency_type]['cost_range_max']))
					if await self._set_dark_market_material(world, unique_id, code, merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity) == 0:
						return self._message_typesetting(99, 'database operation error')
				elif merchandise in dark_market_data['other'].keys():
					currency_type = (random.choices(list(dark_market_data['other'][merchandise].keys()), k=1))[0]
					merchandise_quantity = random.randint(int(dark_market_data['other'][merchandise][currency_type]['quantity_min']), int(dark_market_data['other'][merchandise][currency_type]['quantity_max']))
					currency_type_price = random.randint(int(dark_market_data['other'][merchandise][currency_type]['cost_range_min']), int(dark_market_data['other'][merchandise][currency_type]['cost_range_max']))
					if await self._set_dark_market_material(world, unique_id, code, merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity) == 0:
						return self._message_typesetting(99, 'database operating error')
				else:
					return self._message_typesetting(98, 'Unexpected element, please update the configuration table.')
				remaining.update({'merchandise%s' % code : merchandise, 'merchandise%s_quantity' % code : merchandise_quantity, 'currency_type%s' % code : currency_type, 'currency_type%s_price' % code : currency_type_price})
			remaining.update({'refresh_time' : refresh_time, 'refreshable_quantity' : int(refreshable_quantity)})
			return self._message_typesetting(0, 'refresh market success', {'remaining' : remaining})
		else:
			return self._message_typesetting(97, 'insufficient refreshable quantity')

	@C.collect_async
	async def diamond_refresh_store(self, world: int, unique_id: str) -> dict:
		"""
		# 0  - refresh market success
		# 97 - insufficient diamond
		# 98 - unexpected element, please update the configuration table
		# 99 - database operation error
		"""
		dark_market_data = self._player['dark_market']
		merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity = await self._get_dark_market_material(world, unique_id, code = 1)
		diamond_data = await self.try_diamond(world, unique_id, -1 * int(dark_market_data['diamond_refresh_store']['diamond']))
		remaining = {'diamond' : diamond_data['remaining']}
		if diamond_data['status'] == 1:
			return self._message_typesetting(97, 'insufficient diamond')
		else:
			tier_choice = random.choices(dark_market_data['names'], dark_market_data['weights'], k = 8)
			key_list = [(random.choices(dark_market_data[tier], k = 1))[0] for tier in tier_choice]
			for i in range(len(key_list)):
				merchandise = key_list[i]
				code = i + 1
				if merchandise in dark_market_data['weapon']:
					currency_type = (random.choices(list(dark_market_data['segment'].keys()), k = 1))[0]
					merchandise_quantity = random.randint(int(dark_market_data['segment'][currency_type]['quantity_min']), int(dark_market_data['segment'][currency_type]['quantity_max']))
					currency_type_price = random.randint(int(dark_market_data['segment'][currency_type]['cost_range_min']), int(dark_market_data['segment'][currency_type]['cost_range_max']))
					if await self._set_dark_market_material(world, unique_id, code, merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity) == 0:
						return self._message_typesetting(99, 'database operation error')
				elif merchandise in dark_market_data['skill']:
					currency_type = (random.choices(list(dark_market_data['reward_skill'].keys()), k=1))[0]
					merchandise_quantity = 1
					currency_type_price = random.randint(int(dark_market_data['reward_skill'][currency_type]['cost_range_min']), int(dark_market_data['reward_skill'][currency_type]['cost_range_max']))
					if await self._set_dark_market_material(world, unique_id, code, merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity) == 0:
						return self._message_typesetting(99, 'database operation error')
				elif merchandise in dark_market_data['other'].keys():
					currency_type = (random.choices(list(dark_market_data['other'][merchandise].keys()), k=1))[0]
					merchandise_quantity = random.randint(int(dark_market_data['other'][merchandise][currency_type]['quantity_min']), int(dark_market_data['other'][merchandise][currency_type]['quantity_max']))
					currency_type_price = random.randint(int(dark_market_data['other'][merchandise][currency_type]['cost_range_min']), int(dark_market_data['other'][merchandise][currency_type]['cost_range_max']))
					if await self._set_dark_market_material(world, unique_id, code, merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity) == 0:
						return self._message_typesetting(99, 'database operating error')
				else:
					return self._message_typesetting(98, 'Unexpected element, please update the configuration table.')
				remaining.update({'merchandise%s' % code : merchandise, 'merchandise%s_quantity' % code : merchandise_quantity, 'currency_type%s' % code : currency_type, 'currency_type%s_price' % code : currency_type_price})
			remaining.update({'refresh_time' : refresh_time, 'refreshable_quantity' : int(refreshable_quantity)})
			return self._message_typesetting(0, 'refresh market success', {'remaining' : remaining})

	@C.collect_async
	async def black_market_transaction(self, world: int, unique_id: str, code: int) -> dict:
		# 0  : gain weapon fragments
		# 1  : gain new skills
		# 2  : gain a scroll
		# 3  : gain several materials
		# 93 : unexpected element, please update configuration table
		# 94 : other -> database operating error
		# 95 : skill -> database operating error
		# 96 : weapon -> database operating error
		# 97 : (diamond or coin) insufficient
		# 98 : merchandise has been sold
		# 99 : parameter error
		if code < 1 or code > 8:
			return self._message_typesetting(99, 'parameter error')
		merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity = await self._get_dark_market_material(world, unique_id, code)

		if merchandise == '':
			return self._message_typesetting(98, 'merchandise has been sold')
		dark_market_data = self._player['dark_market']
		remaining = {}
		if merchandise in dark_market_data['weapon']:
			currency_type_data = await self._try_material(world, unique_id, currency_type, -1 * currency_type_price)
			if currency_type_data['status'] == 1:
				return self._message_typesetting(97, currency_type + ' insufficient')
			sql_str = f"UPDATE weapon SET segment=segment+{merchandise_quantity} WHERE unique_id='{unique_id}' AND weapon_name='{merchandise}';"
			if await self._execute_statement_update(world, sql_str) == 0:
				return self._message_typesetting(96, 'weapon -> database operating error')
			segment = (await self._execute_statement(world, 'SELECT segment FROM weapon WHERE unique_id = "%s" AND weapon_name="%s";' % (unique_id, merchandise)))[0][0]
			remaining.update({'code' : code, 'weapon' : merchandise, 'segment' : segment, 'currency_type' : currency_type, 'cost_remaining' : currency_type_data['remaining']})
			if await self._set_dark_market_material(world, unique_id, code, '', 0, '', 0, refresh_time, refreshable_quantity) == 0:
				pass # only a print statement found in original code, maybe should return error?
			return self._message_typesetting(0, 'gain weapon fragments', {'remaining' : remaining})
		elif merchandise in dark_market_data['skill']:
			currency_type_data = await self._try_material(world, unique_id, currency_type, -1 * currency_type_price)
			if currency_type_data['status'] == 1:
				return self._message_typesetting(97, currency_type + ' insufficient')
			skill_data = await self.try_unlock_skill(world, unique_id, merchandise)
			if skill_data['status'] == 0:
				remaining.update({'code' : code, 'skill' : merchandise, 'level' : 1, 'currency_type' : currency_type, 'cost_remaining' : currency_type_data['remaining']})
				if await self._set_dark_market_material(world, unique_id, code, '', 0, '', 0, refresh_time, refreshable_quantity) == 0:
					pass # only a print statement found in original code
				return self._message_typesetting(1, 'gain new skills', {'remaining' : remaining})
			else:
				scroll = (random.choices(dark_market_data['skill_scroll'], cum_weights=[0.7, 0.9, 1]))[0]
				scroll_data = await self._try_material(world, unique_id, scroll, 1)
				if scroll_data['status'] == 1:
					return self._message_typesetting(95, 'skill -> database operating error')
				remaining.update({'code' : code, 'scroll' : scroll, 'quantity' : scroll_data['remaining'], 'currency_type' : currency_type, 'cost_remaining' : currency_type_data['remaining']})
				if await self._set_dark_market_material(world, unique_id, code, '', 0, '', 0, refresh_time, refreshable_quantity) == 0:
					pass # only a print statement found in original code
				return self._message_typesetting(2, 'gain a scroll', {'remaining' : remaining})
		elif merchandise in dark_market_data['other'].keys():
			currency_type_data = await self._try_material(world, unique_id, currency_type, -1 * currency_type_price)
			if currency_type_data['status'] == 1:
				return self._message_typesetting(97, currency_type + ' insufficient')
			other_data = await self._try_material(world, unique_id, merchandise, merchandise_quantity)
			if other_data['status'] == 1:
				return self._message_typesetting(94, 'other -> database operating error')
			remaining.update({'code' : code, 'merchandise' : merchandise, 'quantity' : other_data['remaining'], 'currency_type' : currency_type, 'cost_remaining' : currency_type_data['remaining']})
			if await self._set_dark_market_material(world, unique_id, code, '', 0, '', 0, refresh_time, refreshable_quantity) == 0:
				pass  # only a print statement found in original code
			return self._message_typesetting(3, 'gain several materials', {'remaining' : remaining})
		else:
			return self._message_typesetting(93, 'unexpected element, please update the configuration table.')

#############################################################################
#						End Stage Module Functions							#
#############################################################################




#############################################################################
#						Lottery Module Functions							#
#############################################################################

	@C.collect_async
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

	@C.collect_async
	async def random_gift_weapon(self, world: int, unique_id: str, kind: str) -> dict:
		# success ===> 0 and 1
		# - 0 - Unlocked new weapon!   ===> {"keys": ["weapon"], "values": [weapon]}
		# - 1 - Weapon already unlocked, got free segment   ===>  {"keys": ['weapon', 'segment'], "values": [weapon, segment]}
		# - 99 - Invalid weapon name
		tier_choice = (random.choices(self._lottery['weapons']['names'], self._lottery['weapons']['weights'][kind]))[0]
		gift_weapon = (random.choices(self._lottery['weapons']['items'][tier_choice]))[0]
		return await self.try_unlock_weapon(world, unique_id, gift_weapon)

	@C.collect_async
	async def random_gift_role(self, world: int, unique_id: str, kind: str) -> dict:
		# success ===> 0 and 1
		# - 0 - Unlocked new weapon!   ===> {"keys": ["weapon"], "values": [weapon]}
		# - 1 - Weapon already unlocked, got free segment   ===>  {"keys": ['role', 'segment'], "values": [weapon, segment]}
		# - 99 - Invalid role name
		tier_choice = (random.choices(self._lottery['roles']['names'], self._lottery['roles']['weights'][kind]))[0]
		gift_role = (random.choices(self._lottery['roles']['items'][tier_choice]))[0]
		return await self.try_unlock_role(world, unique_id, gift_role)

	@C.collect_async
	async def basic_summon(self, world: int, unique_id: str, cost_item: str, summon_kind: str) -> dict:
		# success -> 0 , 1 , 2 , 3 , 4 , 5
		# 0  - get skill item success
		# 1  - you already has skill, get scroll
		# 2  - get weapon success
		# 3  - get weapon segment success
		# 4  - get role item success
		# 5  - get role segment success
		# 95 - operation error
		# 96 - weapons operation error
		# 97 - skill operation error
		# 98 - insufficient materials
		# 99 - wrong item name
		return await self._default_summon(world, unique_id, cost_item, 'basic', summon_kind)

	@C.collect_async
	async def pro_summon(self, world: int, unique_id: str, cost_item: str, summon_kind: str) -> dict:
		# success -> 0 , 1 , 2 , 3 , 4 , 5
		# 0  - get skill item success
		# 1  - you already has skill, get scroll
		# 2  - get weapon success
		# 3  - get weapon segment success
		# 4  - get role item success
		# 5  - get role segment success
		# 95 - operation error
		# 96 - weapons operation error
		# 97 - skill operation error
		# 98 - insufficient materials
		# 99 - wrong item name
		return await self._default_summon(world, unique_id, cost_item, 'pro', summon_kind)

	@C.collect_async
	async def friend_summon(self, world: int, unique_id: str, cost_item: str, summon_kind: str) -> dict:
		# success -> 0 , 1 , 2 , 3 , 4 , 5
		# 0  - get skill item success
		# 1  - you already has skill, get scroll
		# 2  - get weapon success
		# 3  - get weapon segment success
		# 4  - get role item success
		# 5  - get role segment success
		# 95 - operation error
		# 96 - weapons operation error
		# 97 - skill operation error
		# 98 - insufficient materials
		# 99 - wrong item name
		return await self._default_summon(world, unique_id, cost_item, 'friend_gift', summon_kind)

	@C.collect_async
	async def prophet_summon(self, world: int, unique_id: str, cost_item: str, summon_kind: str) -> dict:
		# success -> 0 , 1 , 2 , 3 , 4 , 5
		# 0  - get skill item success
		# 1  - you already has skill, get scroll
		# 2  - get weapon success
		# 3  - get weapon segment success
		# 4  - get role item success
		# 5  - get role segment success
		# 95 - operation error
		# 96 - weapons operation error
		# 97 - skill operation error
		# 98 - insufficient materials
		# 99 - wrong item name
		return await self._default_summon(world, unique_id, cost_item, 'prophet', summon_kind)

	@C.collect_async
	async def basic_summon_10_times(self, world: int, unique_id: str, cost_item: str, summon_kind:str) -> dict:
		# 0  - 10 times basic_summon
		# 98 - insufficient materials
		# 99 - wrong item name
		if cost_item == 'diamond':
			result = await self.try_diamond(world, unique_id, -10 * int(self._lottery[summon_kind]['cost']['diamond']))
		elif cost_item == 'coin':
			result = await self.try_coin(world, unique_id, -10 * int(self._lottery[summon_kind]['cost']['diamond']))
		elif cost_item == 'basic_summon_scroll':
			result = await self.try_basic_summon_scroll(world, unique_id, -10 * int(self._lottery[summon_kind]['cost']['basic_summon_scroll']))
		elif cost_item == 'pro_summon_scroll':
			result = await self.try_pro_summon_scroll(world, unique_id, -10 * int(self._lottery[summon_kind]['cost']['pro_summon_scroll']))
		elif cost_item == 'friend_gift':
			result = await self.try_friend_gift(world, unique_id, -10 * int(self._lottery[summon_kind]['cost']['friend_gift']))
		else:
			return self._message_typesetting(status=99, message='wrong item name')
		if result["status"] != 0:
			return self._message_typesetting(status=98, message='insufficient materials')

		remaining_dict = {}
		reward_dict = {}
		for i in range(0, 10):
			message_dict = await self._default_summon(world, unique_id, "10_times", 'basic', summon_kind)
			message_dict["data"]["remaining"].update({"cost_item": cost_item, "cost_quantity": result["remaining"], "status": message_dict["status"]})
			message_dict["data"]["reward"].update({"status": message_dict["status"]})
			remaining_dict.update({str(i): message_dict["data"]["remaining"]})
			reward_dict.update({str(i): message_dict["data"]["reward"]})
		return self._message_typesetting(status=0, message='10 times basic_summon', data={"remaining": remaining_dict, "reward": reward_dict})

	@C.collect_async
	async def pro_summon_10_times(self, world: int, unique_id: str, cost_item: str,summon_kind:str) -> dict:
		# 0  - 10 times pro_summon
		# 98 - insufficient materials
		# 99 - wrong item name
		if cost_item == 'diamond':
			result = await self.try_diamond(world, unique_id, -10 * int(self._lottery[summon_kind]['cost']['diamond']))
		elif cost_item == 'coin':
			result = await self.try_coin(world, unique_id, -10 * int(self._lottery[summon_kind]['cost']['diamond']))
		elif cost_item == 'basic_summon_scroll':
			result = await self.try_basic_summon_scroll(world, unique_id, -10 * int(self._lottery[summon_kind]['cost']['basic_summon_scroll']))
		elif cost_item == 'pro_summon_scroll':
			result = await self.try_pro_summon_scroll(world, unique_id, -10 * int(self._lottery[summon_kind]['cost']['pro_summon_scroll']))
		elif cost_item == 'friend_gift':
			result = await self.try_friend_gift(world, unique_id, -10 * int(self._lottery[summon_kind]['cost']['friend_gift']))
		else:
			return self._message_typesetting(99, 'wrong item name')
		if result["status"] != 0:
			return self._message_typesetting(status=98, message='insufficient materials')

		remaining_dict = {}
		reward_dict = {}
		for i in range(0, 10):
			message_dict = await self._default_summon(world, unique_id, "10_times", 'pro', summon_kind)
			message_dict["data"]["remaining"].update({"cost_item": cost_item, "cost_quantity": result["remaining"], "status": message_dict["status"]})
			message_dict["data"]["reward"].update({"status": message_dict["status"]})
			remaining_dict.update({str(i): message_dict["data"]["remaining"]})
			reward_dict.update({str(i): message_dict["data"]["reward"]})
		return self._message_typesetting(status=0, message='10 times pro_summon', data={"remaining": remaining_dict, "reward": reward_dict})

	@C.collect_async
	async def friend_summon_10_times(self, world: int, unique_id: str, cost_item: str,summon_kind:str) -> dict:
		# 0  - 10 times friend_summon
		# 98 - insufficient materials
		# 99 - wrong item name
		if cost_item == 'diamond':
			result = await self.try_diamond(world, unique_id, -10 * int(self._lottery[summon_kind]['cost']['diamond']))
		elif cost_item == 'coin':
			result = await self.try_coin(world, unique_id, -10 * int(self._lottery[summon_kind]['cost']['diamond']))
		elif cost_item == 'basic_summon_scroll':
			result = await self.try_basic_summon_scroll(world, unique_id, -10 * int(self._lottery[summon_kind]['cost']['basic_summon_scroll']))
		elif cost_item == 'pro_summon_scroll':
			result = await self.try_pro_summon_scroll(world, unique_id, -10 * int(self._lottery[summon_kind]['cost']['pro_summon_scroll']))
		elif cost_item == 'friend_gift':
			result = await self.try_friend_gift(world, unique_id, -10 * int(self._lottery[summon_kind]['cost']['friend_gift']))
		else:
			return self._message_typesetting(99, 'wrong item name')
		if result["status"] != 0:
			return self._message_typesetting(status=98, message='insufficient materials')

		remaining_dict = {}
		reward_dict = {}
		for i in range(0, 10):
			message_dict = await self._default_summon(world, unique_id, "10_times", 'friend_gift', summon_kind)
			message_dict["data"]["remaining"].update({"cost_item": cost_item, "cost_quantity": result["remaining"], "status": message_dict["status"]})
			message_dict["data"]["reward"].update({"status": message_dict["status"]})
			remaining_dict.update({str(i): message_dict["data"]["remaining"]})
			reward_dict.update({str(i): message_dict["data"]["reward"]})
		return self._message_typesetting(status=0, message='10 times friend_summon', data={"remaining": remaining_dict, "reward": reward_dict})

	@C.collect_async
	async def prophet_summon_10_times(self, world: int, unique_id: str, cost_item: str,summon_kind:str) -> dict:
		# 0  - 10 times prophet_summon
		# 98 - insufficient materials
		# 99 - wrong item name
		if cost_item == 'diamond':
			result = await self.try_diamond(world, unique_id, -10 * int(self._lottery[summon_kind]['cost']['diamond']))
		elif cost_item == 'coin':
			result = await self.try_coin(world, unique_id, -10 * int(self._lottery[summon_kind]['cost']['diamond']))
		elif cost_item == 'basic_summon_scroll':
			result = await self.try_basic_summon_scroll(world, unique_id, -10 * int(self._lottery[summon_kind]['cost']['basic_summon_scroll']))
		elif cost_item == 'pro_summon_scroll':
			result = await self.try_pro_summon_scroll(world, unique_id, -10 * int(self._lottery[summon_kind]['cost']['pro_summon_scroll']))
		elif cost_item == 'friend_gift':
			result = await self.try_friend_gift(world, unique_id, -10 * int(self._lottery[summon_kind]['cost']['friend_gift']))
		else:
			return self._message_typesetting(99, 'wrong item name')
		if result["status"] != 0:
			return self._message_typesetting(status=98, message='insufficient materials')

		remaining_dict = {}
		reward_dict = {}
		for i in range(0, 10):
			message_dict = await self._default_summon(world, unique_id, "10_times", 'prophet', summon_kind)
			message_dict["data"]["remaining"].update({"cost_item": cost_item, "cost_quantity": result["remaining"], "status": message_dict["status"]})
			message_dict["data"]["reward"].update({"status": message_dict["status"]})
			remaining_dict.update({str(i): message_dict["data"]["remaining"]})
			reward_dict.update({str(i): message_dict["data"]["reward"]})
		return self._message_typesetting(status=0, message='10 times prophet_summon', data={"remaining": remaining_dict, "reward": reward_dict})

	@C.collect_async
	async def fortune_wheel_basic(self, world: int, unique_id: str, cost_item: str) -> dict:
		# 0  - get energy success
		# 1  - get weapon success
		# 2  - get weapon segment success
		# 3  - get skill success
		# 4  - already have skill, get scroll
		# 5  - get item success
		# 96 - item name error
		# 97 - database skill operation error
		# 98 - insufficient material
		# 99 - cost_item error
		return await self._default_fortune_wheel(world, unique_id, cost_item, 'basic')

	@C.collect_async
	async def fortune_wheel_pro(self, world: int, unique_id: str, cost_item: str) -> dict:
		# 0  - get energy success
		# 1  - get weapon success
		# 2  - get weapon segment success
		# 3  - get skill success
		# 4  - already have skill, get scroll
		# 5  - get item success
		# 96 - item name error
		# 97 - database skill operation error
		# 98 - insufficient material
		# 99 - cost_item error
		return await self._default_fortune_wheel(world, unique_id, cost_item, 'pro')

#############################################################################
#						End Lottery Module Functions						#
#############################################################################


#############################################################################
#						Start Friend Module Functions						#
#############################################################################

	@C.collect_async
	async def get_all_friend_info(self, world: int, unique_id: str) -> dict:
		# 0 - Got all friends info
		# 99 - You do not have any friends. FeelsBadMan.
		friends = await self._execute_statement(world, f'SELECT * FROM friend WHERE unique_id = "{unique_id}";')
		if len(friends) == 0:
			return self._message_typesetting(99, 'You do not have any friends. FeelsBadMan.')
		remaining = {'remaining' : {'f_name' : [], 'f_level' : [], 'f_recovery_time' : [], 'become_friend_time' : []}}
		for friend in friends:
			remaining['remaining']['f_name'].append(friend[2])
			remaining['remaining']['f_level'].append(friend[3])
			remaining['remaining']['f_recovery_time'].append(friend[4])
			remaining['remaining']['become_friend_time'].append(friend[5])
		return self._message_typesetting(0, 'Got all friends info', remaining)

	# TODO optimize the subroutine
	# TODO check to ensure function is working as expected
	@C.collect_async
	async def send_all_friend_gift(self, world: int, unique_id: str) -> dict:
		friends = await self._execute_statement(world, f'SELECT * FROM friend WHERE unique_id = "{unique_id}" and become_friend_time != "";')
		if len(friends) == 0:
			return self._message_typesetting(98, 'You have no friends. FeelsBadMan.')
		remaining = {'remaining' : {'f_name' : [], 'f_level' : [], 'f_recovery_time' : []}}
		for friend in friends:
			d = await self.send_friend_gift(world, unique_id, friend[2])
			if d["status"]==0:
				remaining['remaining']['f_name'].append(d['data']['remaining']['f_name'])
				remaining['remaining']['f_level'].append(d['data']['remaining']['f_level'])
				remaining['remaining']['f_recovery_time'].append(d['data']['remaining']['current_time'])
		if len(remaining['remaining']['f_name'])==0:
			return self._message_typesetting(1, 'sent all friends gifts, but all your friends are not exist', remaining)
		else:
			return self._message_typesetting(0, 'sent all friends gifts', remaining)

	@C.collect_async
	async def send_friend_gift(self, world: int, unique_id: str, friend_name: str) -> dict:
		# 0 - send friend gift success because of f_recovering_time is empty
		# 1 - send friend gift success because time is over 1 day
		# 95 - this person is not exist anymore
		# 96 - This person has not become your friend
		# 97 - Mailbox error
		# 98 - this person is not your friend anymore
		# 99 - send friend gift failed, because not cooldown time is not finished
		#
		# return value
		# {
		#	{'f_id' : str, 'f_name' : str, 'f_level': int}
		# }
		data = await self._execute_statement(world, f'SELECT unique_id FROM player WHERE game_name = "{friend_name}";')
		if len(data)==0:
			return self._message_typesetting(95, 'this person is not exist anymore')
		friend_id = (await self._execute_statement(world, f'SELECT unique_id FROM player WHERE game_name = "{friend_name}";'))[0][0]
		data = await self._execute_statement(world, f'SELECT * FROM friend WHERE unique_id = "{unique_id}" AND friend_id = "{friend_id}";')
		if len(data) == 0:
			return self._message_typesetting(98, 'this person is not your friend anymore')
		mylist = list(data[0])
		f_recovering_time = mylist[4]
		sql_result = await self._execute_statement(world, f'SELECT game_name, level FROM player WHERE unique_id = "{friend_id}";')
		f_game_name = sql_result[0][0]
		f_level = sql_result[0][1]
		if mylist[5] == '':
			return self._message_typesetting(status=96, message="This person has not become your friend")
		elif f_recovering_time == '':
			json_data = {
					'world' : world,
					'uid_to': friend_id,
					'kwargs': {
						'from' : 'server',
						'body' : 'Your gift is waiting.',
						'subject' : 'You have a gift!',
						'type' : 'gift',
						'items' : 'friend_gift',
						'quantities' : '1'
						}
					}
			result = requests.post('http://localhost:8020/send_mail', json = json_data).json()
			if result['status'] != 0:
				return self._message_typesetting(97, 'mailbox error')
			current_time = time.strftime('%Y-%m-%d', time.localtime())
			await self._execute_statement_update(world, f'UPDATE friend SET recovery_time = "{current_time}" WHERE unique_id = "{unique_id}" AND friend_id = "{friend_id}";')
			data = {
					'remaining' : {
							'f_name' : f_game_name,
							'f_level' : f_level,
							'current_time' : current_time
						}
					}
			return self._message_typesetting(0, 'send friend gift success because of f_recovering time is empty', data)
		else:
			current_time = time.strftime('%Y-%m-%d', time.localtime())
			delta_time = datetime.strptime(current_time, '%Y-%m-%d') - datetime.strptime(f_recovering_time, '%Y-%m-%d')
			if delta_time.days >= 1:
				json_data = {
						'world' : world,
						'uid_to': friend_id,
						'kwargs': {
							'from' : 'server',
							'body' : 'Your gift is waiting.',
							'subject' : 'You have a gift!',
							'type' : 'gift',
							'items' : 'friend_gift',
							'quantities' : '1'
							}
						}
				result = requests.post('http://localhost:8020/send_mail', json = json_data).json()
				if result['status'] != 0:
					return self._message_typesetting(97, 'Mailbox error')
				await self._execute_statement_update(world, f'UPDATE friend SET recovery_time = "{current_time}" WHERE unique_id = "{unique_id}" AND friend_id = "{friend_id}";')
				data = {
						'remaining' : {
								'f_name' : f_game_name,
								'f_level' : f_level,
								'current_time' : current_time
							}
						}
				return self._message_typesetting(1, 'send friend gift success because of f_recovering time is over 1 day', data)
			else:
				data = {
						'remaining' : {
								'f_name' : f_game_name,
								'f_level' : f_level,
								'current_time' : f_recovering_time
							}
						}
				return self._message_typesetting(99, 'send friend gift failed, because cooldown time is not finished', data)

	@C.collect_async
	async def delete_friend(self, world: int, unique_id: str, friend_name: str) -> dict:
		# 0 - request friend successfully
		# 98 - you don't have this friend
		# 99 - No such person
		friend_data = await self._execute_statement(world, f'SELECT unique_id FROM player WHERE game_name = "{friend_name}";')
		if len(friend_data) == 0:
			return self._message_typesetting(99, 'no such person')
		friend_id = friend_data[0][0]
		data = await self._execute_statement(world, f'SELECT * FROM friend WHERE unique_id = "{unique_id}" AND friend_id = "{friend_id}";')
		if len(data) != 0:
			await self._execute_statement(world, f'DELETE FROM friend WHERE unique_id = "{unique_id}" AND friend_id = "{friend_id}";')
			if data[0][5] != "":
				await self._execute_statement(world, f'DELETE FROM friend WHERE unique_id = "{friend_id}" AND friend_id = "{unique_id}";')
			return self._message_typesetting(0, 'delete friend success', data={"remaining": {"friend_name": friend_name}})
		else:
			return self._message_typesetting(98, 'you do not have this friend')

	@C.collect_async
	async def redeem_nonce(self, world: int, unique_id: str, nonce: str) -> dict:
		# 0 - successfully redeemed
		# 99 - database operation error
		response = requests.post('http://localhost:8001/redeem_nonce', json = {'type' : ['gift'], 'nonce' : [nonce]})
		requests.post('http://localhost:8020/delete_mail', data={"world": world, "unique_id": unique_id, "nonce": nonce})
		data = response.json()
		if data[nonce]['status'] != 0:
			return self._message_typesetting(98, 'nonce already redeemed')
		items = data[nonce]['items']
		quantities = data[nonce]['quantities']
		sql_str = f'UPDATE player SET {items}={items}+{quantities} WHERE unique_id = "{unique_id}";'
		if await self._execute_statement_update(world, sql_str) == 0:
			return self._message_typesetting(99, 'database operating error')
		sql_str = f'SELECT {items} FROM player WHERE unique_id = "{unique_id}";'
		quantities = (await self._execute_statement(world, sql_str))[0][0]
		return self._message_typesetting(0, 'successfully redeemed', {'remaining' : {"nonce": nonce, items : quantities}})

	@C.collect_async
	async def redeem_all_nonce(self, world: int, unique_id: str, type_list: [str], nonce_list: [str]) -> dict:
		# success -> 0
		# 0 - Add friends to success
		# 98 - database operating error
		# 99 - You already have this friend
		response = requests.post('http://localhost:8001/redeem_nonce', json = {'type' : type_list, 'nonce' : nonce_list})
		data = response.json()
		remaining = {"nonce_list": nonce_list, "expired_nonce": []}
		current_time = time.strftime('%Y-%m-%d', time.localtime())
		for i in range(len(type_list)):
			if data[nonce_list[i]]["status"] == 0:
				if type_list[i] == "gift":
					items = data[nonce_list[i]]["items"]
					quantities = data[nonce_list[i]]["quantities"]
					sql_str = f"update player set {items}={items}+{quantities} where unique_id='{unique_id}'"
					if await self._execute_statement_update(world=world, statement=sql_str) == 0:
						return self._message_typesetting(status=98, message="database operating error")
					sql_str = f"select {items} from player where unique_id='{unique_id}'"
					quantities = (await self._execute_statement(world=world, statement=sql_str))[0][0]
					remaining.update({items: quantities})
				elif type_list[i] == "simple":
					pass
				elif type_list[i] == "friend_request":
					friend_name = data[nonce_list[i]]["sender"]
					friend_id = data[nonce_list[i]]["uid_sender"]
					unique_data = await self._execute_statement(world=world, statement=f"SELECT * FROM friend WHERE unique_id='{friend_id}' and friend_id='{unique_id}'")
					if unique_data[0][5] == "":
						# friend_name = data[0][2]
						update_str = f"update friend set become_friend_time='{current_time}' where unique_id='{friend_id}' and friend_id='{unique_id}'"
						insert_str = f"replace into friend(unique_id, friend_id, friend_name, become_friend_time) values('{unique_id}', '{friend_id}', '{friend_name}', '{current_time}')"
						await self._execute_statement_update(world=world, statement=update_str)
						await self._execute_statement_update(world=world, statement=insert_str)
						remaining["nonce_list"].append(nonce_list[i])
				else:
					return self._message_typesetting(status=99, message="type_list error")
			else:
				remaining["expired_nonce"].append(nonce_list[i])
		return self._message_typesetting(status=0, message="successfully redeemed", data={"remaining": remaining})

	@C.collect_async
	async def request_friend(self, world: int, unique_id: str, friend_name: str) -> dict:
		# success -> 0
		# 0 - request friend successfully
		# 95 - database operating error
		# 96 - Mailbox error
		# 97 - You already have this friend
		# 98 - You have sent a friend request
		# 99 - No such person
		friend_data = await self._execute_statement(world=world, statement=f"SELECT unique_id FROM player WHERE game_name='{friend_name}' and unique_id != '{unique_id}'")
		if len(friend_data) == 0:
			return self._message_typesetting(status=99, message="No such person")
		friend_id = friend_data[0][0]

		data = await self._execute_statement(world=world, statement=f"SELECT * FROM friend WHERE unique_id='{unique_id}' and friend_id='{friend_id}'")
		if len(data) != 0:
			if data[0][5] == "":
				return self._message_typesetting(status=98, message="You have sent a friend request")
			return self._message_typesetting(status=97, message="You already have this friend")

		unique_name = (await self._execute_statement(world=world, statement=f"SELECT game_name FROM player WHERE unique_id='{unique_id}'"))[0][0]
		json_data = {
			"world": world,
			"uid_to": friend_id,
			"kwargs": {
				"from": "server",
				"subject": "You have a friend request!",
				"body": "Friend request",
				"type": "friend_request",
				"sender": unique_name,
				"uid_sender": unique_id
			}
		}
		result = requests.post('http://localhost:8020/send_mail', json=json_data).json()
		if result["status"] != 0:
			return self._message_typesetting(status=96, message='Mailbox error')

		if await self._execute_statement_update(world=world, statement=f"insert into friend (unique_id, friend_id, friend_name) values ('{unique_id}', '{friend_id}', '{friend_name}')") == 0:
			return self._message_typesetting(status=95, message="database operating error")
		return self._message_typesetting(status=0, message="request friend successfully")

	@C.collect_async
	async def response_friend(self, world: int, unique_id: str, nonce: str) -> dict:
		# success -> 0
		# 0 - Add friends to success
		# 97 - nonce error
		# 98 - The other has deleted the friend request
		# 99 - You already have this friend
		response = requests.post('http://localhost:8001/redeem_nonce', json = {'type' : ['friend_request'], 'nonce' : [nonce]})
		data = response.json()
		try:
			friend_name = data[nonce]["sender"]
			friend_id = data[nonce]["uid_sender"]
			requests.post('http://localhost:8020/delete_mail', data={"world": world, "unique_id": unique_id, "nonce": nonce})
		except:
			return self._message_typesetting(status=97, message="nonce error")

		data = await self._execute_statement(world=world, statement=f"SELECT * FROM friend WHERE unique_id='{friend_id}' and friend_id='{unique_id}'")
		if data[0][5] != "":
			return self._message_typesetting(status=99, message="You already have this friend")
		# friend_name = data[0][2]

		current_time = time.strftime('%Y-%m-%d', time.localtime())
		update_str = f"update friend set become_friend_time='{current_time}' where unique_id='{friend_id}' and friend_id='{unique_id}'"
		insert_str = f"replace into friend(unique_id, friend_id, friend_name, become_friend_time) values('{unique_id}', '{friend_id}', '{friend_name}', '{current_time}')"
		update_code = await self._execute_statement_update(world=world, statement=update_str)
		if update_code == 0:
			return self._message_typesetting(status=98, message="The other has deleted the friend request")
		await self._execute_statement_update(world=world, statement=insert_str)
		return self._message_typesetting(status=0, message="Add friends to success", data={"remaining": {"nonce": nonce}})

#############################################################################
#						End Friend Module Functions							#
#############################################################################

#############################################################################
#                     Start Mall Function Position                          #
#############################################################################
	@C.collect_async
	async def purchase_scroll_mall(self, world: int, unique_id: str, scroll_type: str, purchase_type: str, quantity: int):
		"""
		0 - Purchase success
		96 - Insufficient {mall_consume}
		97 - No such purchase type
		98 - This scroll cannot be purchased
		99 - The quantity purchased must be a positive integer
		"""
		scroll_config = self._mall_config["scroll"]
		if quantity <= 0:
			return self._message_typesetting(status=99, message="The quantity purchased must be a positive integer")
		mall_scroll_type = scroll_config["scroll_type"]
		if scroll_type not in mall_scroll_type:
			return self._message_typesetting(status=98, message="This scroll cannot be purchased")
		mall_purchase_type = scroll_config[scroll_type]["purchase_type"]
		if purchase_type not in mall_purchase_type:
			return self._message_typesetting(status=97, message="No such purchase type")
		mall_consume = scroll_config[scroll_type][purchase_type]["consume"]
		mall_quantity = -1 * scroll_config[scroll_type][purchase_type]["quantity"] * quantity
		mall_scroll_quantity = scroll_config[scroll_type][purchase_type]["scroll_quantity"] * quantity
		consume_data = await eval(f"self.try_{mall_consume}({world}, {unique_id}, {mall_quantity})")
		if consume_data["status"] == 1:
			return self._message_typesetting(status=96, message=f"Insufficient {mall_consume}")
		await self._execute_statement_update(world=world, statement=f"update player set {scroll_type}={scroll_type}+{mall_scroll_quantity} where unique_id='{unique_id}'")
		scroll_quantity = await self._get_material(world=world, unique_id=unique_id, material=scroll_type)
		return self._message_typesetting(status=0, message="Purchase success", data={"remaining": {mall_consume: consume_data["remaining"], scroll_type: scroll_quantity}, "reward": {scroll_type: mall_scroll_quantity}})
#############################################################################
#                     Start Mall Function Position                          #
#############################################################################


#############################################################################
#                     Start Temp Function Position                          #
#############################################################################

	async def get_lottery_config_info(self, world: int, unique_id: str):
		if self._lottery == "":
			return self._message_typesetting(1, 'configration is empty')
		data = {
			"remaining": {
				"skills": self._lottery["skills"]["cost"],
				"weapons": self._lottery["weapons"]["cost"],
				"roles": self._lottery["roles"]["cost"],
				"fortune_wheel": self._lottery["fortune_wheel"]["cost"]
			}
		}
		return self._message_typesetting(0, 'got all lottery config info', data)

	async def get_stage_reward_config(self, world: int, unique_id: str):
		if self._get_stage_reward_config_json == "":
			return self._message_typesetting(1, 'configration is empty')
		data = {"remaining": {"stage_reward_config": self._get_stage_reward_config_json}}
		return self._message_typesetting(0, 'got all stage reward config info', data)

	async def monster_config(self, world: int, unique_id: str):
		if self._monster_config_json == "":
			return self._message_typesetting(1, 'configration is empty')
		data = {"remaining": {"monster_config": self._monster_config_json}}
		return self._message_typesetting(0, 'got all monster config info', data)

	async def level_enemy_layouts_config(self, world: int, unique_id: str):
		if self._level_enemy_layouts_config_json == "":
			return self._message_typesetting(1, 'configration is empty')
		data = {"remaining": {"level_enemy_layouts_config": self._level_enemy_layouts_config_json}}
		return self._message_typesetting(0, 'got all level enemy layouts config info', data)

	async def get_account_world_info(self, unique_id: str):
		# 0 - Get all world information
		remaining = []
		for w in range(len(self._pools)):
			data = await self._execute_statement(w, f"select game_name,level from player where unique_id='{unique_id}'")
			if data:
				if w == 0:
					remaining.append({"server_status": 0, "world": w, "world_name": "aliya", "game_name": data[0][0], "level": data[0][1]})
				else:
					remaining.append({"server_status": 0, "world": w, "world_name": f"world{w}", "game_name": data[0][0], "level": data[0][1]})
			else:
				if w == 0:
					remaining.append({"server_status": 0, "world": w, "world_name": "aliya"})
				else:
					remaining.append({"server_status": 0, "world": w, "world_name": f"world{w}"})
		return self._message_typesetting(0, 'Get all world information', data={"remaining": remaining})

	async def choice_world(self, unique_id: str, target_world: int):
		# 0 - enter world success
		# 1 - enter world success, have role in world
		# 97 - enter world failed, the world is full
		# 98 - You have been in this world
		# 99 - No such world
		# world=0
		remaining = {}
		if target_world < 0 or target_world >= len(self._pools):
			return self._message_typesetting(99, "No such world")
		# if world == target_world:
		# 	return self._message_typesetting(98, "You have been in this world")
		server_status = 1  # 获取系统方法赋值 含世界参数target_world
		if server_status == -1:
			return self._message_typesetting(97, 'enter world failed, the world is full')
		data = await self._execute_statement(target_world, f"select game_name, level, role from player where unique_id='{unique_id}'")
		if data:
			# weapons = (await self.get_all_weapon(target_world, unique_id))["data"]
			# supplies = (await self.get_all_supplies(target_world, unique_id))["data"]
			# skills = (await self.get_all_skill_level(target_world, unique_id))["data"]
			# armors = (await self.get_all_armor_info(target_world, unique_id))["data"]
			# remaining.update({"world": target_world, "info": {"weapons": weapons, "supplies": supplies, "skills": skills, "armors": armors}})
			remaining.update({"world": target_world, "game_name": data[0][0], "level": data[0][1], "role": data[0][2]})
			return self._message_typesetting(1, 'enter world success, you have initialized all the information', data={"remaining": remaining})
		return self._message_typesetting(0, 'enter world success', data={"remaining": {"world": target_world}})

	async def create_player(self, world: int, unique_id: str, game_name: str):
		# 0 - You have successfully created a player in this world
		# 1 - Create failed, you have a player in this world
		# 98 - The player's name has been used
		# 99 - Player name cannot be a null character
		remaining = {}
		data_head = (await self.get_all_head(world, 'player'))['remaining']
		head = [x[0] for x in data_head]
		data = await self._execute_statement(world, f"select * from player where unique_id='{unique_id}'")
		if data:
			for i in range(len(head)):
				remaining.update({head[i]: data[0][i]})
			return self._message_typesetting(1, 'Create failed, you have a player in this world', data={"remaining": remaining})

		data_name = await self._execute_statement(world, f"select game_name from player")
		game_names = [x[0] for x in data_name]
		if game_name == "":
			return self._message_typesetting(99, "Player name cannot be a null character")
		if game_name in game_names:
			return self._message_typesetting(98, "The player's name has been used")

		await self._execute_statement_update(world, f"insert into player(unique_id, game_name) values('{unique_id}', '{game_name}')")
		data = await self._execute_statement(world, f"select * from player where unique_id='{unique_id}'")
		for i in range(len(head)):
			remaining.update({head[i]: data[0][i]})
		return self._message_typesetting(0, 'You have successfully created a player in this world', data={"remaining": remaining})

#############################################################################
#                       End Temp Function Position                          #
#############################################################################

#############################################################################
#						Start Family Functions								#
#############################################################################

	@C.collect_async
	async def remove_user_family(self, world: int, uid: str, gamename_target: str) -> dict:
		# announcement = "执行人:执行目标:执行方式:执行人的身份:执行目标的身份"
		# 0 - success, user removed
		# 91 - You don't have permission to delete the administrator
		# 92 - You can't remove the patriarch.
		# 93 - You have reached the upper limit of the number of union removals today.
		# 94 - No such union
		# 95 - you can not remove yourself using this function
		# 96 - user does not belong to your family
		# 97 - you must be family owner to remove a user
		# 98 - you do not belong to a family
		# 99 - He is not your family member
		game_name, fid, union_login, union_contribution = await self._get_familyid(world, unique_id = uid)
		if not fid: return self._message_typesetting(98, 'you are not in a family.')
		members = [gname[0] for gname in await self._execute_statement(world, f"select game_name from player where familyid='{fid}'")]
		if gamename_target not in members: return self._message_typesetting(99, 'He is not your family member')
		if game_name == gamename_target: return self._message_typesetting(95, 'you can not remove yourself using this function')
		family_info = await self._get_family_information(world, fid)
		if not family_info: return self._message_typesetting(94, 'No such union')
		remaining = {}
		family_info = list(family_info[0])
		remove_times = family_info[17]
		remove_start_time = family_info[16]
		news = family_info[6]
		president = family_info[7]
		admins = []
		members.remove(president)
		for admin in family_info[8: 11]:
			if admin:
				admins.append(admin)
				members.remove(admin)
		if president == gamename_target: return self._message_typesetting(92, "You can't remove the patriarch")
		# 获得当前时间用于比较开始删除的时间，并判断是否重置当前的次数
		current_time = datetime.now().strftime("%Y-%m-%d")
		if remove_start_time == "" or (datetime.strptime(remove_start_time, '%Y-%m-%d') - datetime.strptime(current_time, '%Y-%m-%d')).total_seconds() != 0:
			remove_start_time = current_time
			remove_times = 5
		if remove_times == 0: return self._message_typesetting(93, 'You have reached the upper limit of the number of union removals today.')
		else: remove_times -= 1
		if game_name != president and game_name not in admins: return self._message_typesetting(97, 'you are not family admin')
		try:
			announcement = ""
			if game_name == president:  # 会长权限
				for i in range(len(family_info[8: 11])):  # 管理员admin
					if gamename_target == family_info[i + 8]:
						announcement = f"{game_name}:{gamename_target}:1:president:admin"
						await self._execute_statement_update(world, f'UPDATE families SET admin{i + 1} = "" WHERE familyid = "{fid}";')
				if not announcement:
					for i in range(len(family_info[11: 16])):  # 精英elite
						if gamename_target == family_info[i + 11]:
							announcement = f"{game_name}:{gamename_target}:1:president:elite"
							await self._execute_statement_update(world, f'UPDATE families SET elite{i + 1} = "" WHERE familyid = "{fid}";')
				if not announcement:
					announcement = f"{game_name}:{gamename_target}:1:president:member"
			else:
				if gamename_target in admins: return self._message_typesetting(91, "You don't have permission to delete the administrator")
				for i in range(len(family_info[11: 16])):  # 精英elite
					if gamename_target == family_info[i + 11]:
						announcement = f"{game_name}:{gamename_target}:1:admin:elite"
						await self._execute_statement_update(world, f'UPDATE families SET elite{i + 1} = "" WHERE familyid = "{fid}";')
				if not announcement:
					announcement = f"{game_name}:{gamename_target}:1:admin:member"
			if news == "":
				news = {"1": announcement}
			else:
				content = list(json.loads(news.replace("'", "\""), encoding='utf-8').values())
				if len(content) >= 30: content.pop(0)
				content.append(announcement)
				news = {}
				for i, value in enumerate(content):
					news.update({str(i + 1): value})
			await self._execute_statement_update(world, f'UPDATE families SET remove_start_time="{remove_start_time}", remove_times={remove_times}, announcement="{announcement}", news="{str(news)}" WHERE familyid = "{fid}";')
			await self._execute_statement_update(world, f'UPDATE player SET familyid = "", cumulative_contribution=0 WHERE game_name = "{gamename_target}";')
			remaining.update({"announcement": announcement, "news": news, "remove_start_time": remove_start_time, "remove_times": remove_times})
		except ValueError:
			return self._message_typesetting(96, 'user is not in your family')
		return self._message_typesetting(0, 'success, user removed', data={"remaining": remaining})

	# TODO refactor code to run both sql statements with asyncio.gather
	# if the person leaving is the owner, disband the entire family
	@C.collect_async
	async def leave_family(self, world: int, uid: str) -> dict:
		# 0 - success, you have left your family
		# 98 - you do not belong to a family
		game_name, fid = await self._get_familyid(world, unique_id = uid)
		if fid is None or fid == '': return self._message_typesetting(98, 'you are not in a family.')
		owner, fname, members = await self._get_family_information(world, fid)
		if game_name == owner: # the owner is leaving, disband the entire family
			for member in members:
				if member != '':
					await self._execute_statement_update(world, f'UPDATE player SET familyid = "" WHERE game_name = "{member}";')
			await self._execute_statement(world, f'DELETE FROM families WHERE familyid = "{fid}";')
		else:
			await self._execute_statement_update(world, f'UPDATE player SET familyid = "" WHERE unique_id = "{uid}";')
			await self._execute_statement_update(world, f'UPDATE families SET member{members.index(game_name)} = "" WHERE familyid = "{fid}";')
		return self._message_typesetting(0, 'success, you have left your family.')

	@C.collect_async
	async def create_family(self, world: int, uid: str, fname: str) -> dict:
		# 0 - success, family created
		# 98 - you are already in a family
		# 97 - fname already taken
		# 99 - invalid fname
		if fname == '' or not fname: return self._message_typesetting(99, 'invalid fname');
		if await self._family_exists(world, fname):
			return self._message_typesetting(97, 'fname already taken')
		game_name, fid = await self._get_familyid(world, unique_id = uid)
		if fid is not None and fid != '': return self._message_typesetting(98, 'already in a family')
		await self._execute_statement_update(world, f'UPDATE player SET familyid = "{game_name}" WHERE unique_id = "{uid}";')
		await self._execute_statement(world, f'INSERT INTO families (familyid, familyname, member0) VALUES("{game_name}", "{fname}", "{game_name}");')

		return self._message_typesetting(0, 'success, family created')

	@C.collect_async
	async def request_join_family(self, world: int, uid: str, fname: str) -> dict:
		# 0 - success, join request message sent to family owner's mailbox
		# 98 - you already belong to a family
		# 99 - family does not exist
		game_name, fid = await self._get_familyid(world, unique_id = uid)
		if fid is not None and fid != '': return self._message_typesetting(98, 'already in a family')
		if not await self._family_exists(world, fname): return self._message_typesetting(99, 'family does not exist')
		data = await self._execute_statement(world, f'SELECT familyid FROM families WHERE familyname = "{fname}";')
		owner_uid = await self._execute_statement(world, f'SELECT unique_id FROM player WHERE game_name = "{data[0][0]}";')
		j = {'world' : 0, 'uid_to' : owner_uid[0][0], 'kwargs' : {'from' : 'server', 'subject' : 'New join family request', 'body' : f'new request to join family from {game_name}', 'type' : 'family_request', 'fid' : data[0][0], 'fname' : fname, 'target' : game_name, 'uid' : uid}}
		r = requests.post('http://localhost:8020/send_mail', json = j)
		return self._message_typesetting(0, 'success, join request sent to family owners mailbox')

	@C.collect_async
	async def invite_user_family(self, world: int, uid: str, target: str) -> dict:
		# 0 - success, join request message sent to family owner's mailbox
		# 95 - target does not exist
		# 96 - target is already in a family
		# 97 - you must be family owner
		# 98 - you do not belong to a family
		# 99 - invalid target
		game_name, fid = await self._get_familyid(world, unique_id = uid)
		if fid is None or fid == '': return self._message_typesetting(98, 'not in a family')
		owner, fname, members = await self._get_family_information(world, fid)
		if owner != game_name: return self._message_typesetting(97, 'you must be family owner')
		tgame_name, tfid = await self._get_familyid(world, game_name = target)
		if not tgame_name: return self._message_typesetting(95, 'target does not exist')
		if tfid is not None and tfid != '': return self._message_typesetting(96, 'target already in a family')
		targetuid = await self._execute_statement(world, f'SELECT unique_id FROM player WHERE game_name = "{target}";')
		j = {'world' : 0, 'uid_to' : targetuid[0][0], 'kwargs' : {'from' : game_name, 'subject' : 'New join family request', 'body' : f'{game_name} invites you to join their family!', 'type' : 'family_request', 'fid' : fid, 'fname' : fname, 'target' : tgame_name, 'uid' : targetuid[0][0]}}
		r = requests.post('http://localhost:8020/send_mail', json = j)
		return self._message_typesetting(0, 'success, request sent')

	@C.collect_async
	async def respond_family(self, world: int, uid: str, nonce: str) -> dict:
		# 0 - success
		# 96 - family does not exist
		# 97 - target is already in a family
		# 98 - family is full
		# 99 - invalid nonce
		r = requests.post('http://localhost:8001/redeem_nonce', json = {'type' : ['family_request'], 'nonce' : [nonce]}).json()
		if r[nonce]['status'] != 0 or r[nonce]['type'] != 'family_request':
			return self._message_typesetting(99, 'invalid nonce')
		game_name, fid = await self._get_familyid(world, unique_id = r[nonce]['uid'])
		if fid is not None and fid != '': return self._message_typesetting(97, 'target already in a family')
		owner, fname, members = await self._get_family_information(world, r[nonce]['fid'])
		if owner is None: return self._message_typesetting(96, 'family does not exist')
		try:
			next_open = members.index('')
		except ValueError:
			return self._message_typesetting(98, 'family is full')
		await self._execute_statement_update(world, f'UPDATE families SET member{next_open} = "{r[nonce]["target"]}" WHERE familyid = "{r[nonce]["fid"]}";')
		await self._execute_statement_update(world, f'UPDATE player SET familyid = "{r[nonce]["fid"]}" WHERE unique_id = "{r[nonce]["uid"]}";')
		return self._message_typesetting(0, 'success')

#############################################################################
#							End Family Functions							#
#############################################################################

#############################################################################
#							Start Factory Functions							#
#############################################################################

	@C.collect_async
	async def refresh_food_storage(self, world: int, unique_id: str) -> dict:
		# 0  - Food factory update success
		# 99 - Food factory did not start
		food_factory = self._factory_config["food_factory"]
		factory_data = await self._select_factory(world=world, unique_id=unique_id)
		# 配置文件中工厂等级下的最大容量
		food_storage_limit = food_factory["storage_limit"][str(factory_data[1])]
		# 数据库中存的工厂工作的开始时间
		food_start_time = factory_data[5]
		# 数据库中存的工人的数量
		food_factory_workers = factory_data[9]
		# 数据库中存的物资数量
		food_storage = factory_data[14]
		# 数据库中的加速时间
		acceleration_end_time = factory_data[20]
		acceleration_value = 1
		times = 1
		current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		if acceleration_end_time:  # 加速中 存在日期
			acceleration_value = 2  # 加速的倍数设置
			time_difference = datetime.strptime(acceleration_end_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
			if int(time_difference.total_seconds()) <= 0:  # 加速卡过期
				times = 2
				current_time = acceleration_end_time
				# eval(re.sub(r"\D", "", "2019-08-21 10:57:49"))
				await self._execute_statement_update(world=world, statement=f"update factory set acceleration_end_time='' where unique_id='{unique_id}'")
		remaining = {"food_factory_workers": food_factory_workers}
		reward = {"food_increment": 0}
		if food_start_time:
			for i in range(times):
				if times == 2 and i == 1:
					acceleration_value = 1
					current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
				time_difference = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(food_start_time, '%Y-%m-%d %H:%M:%S')
				food_increment = int(time_difference.total_seconds()) // food_factory["time_consuming"] * food_factory_workers * acceleration_value
				if food_increment < 0: continue
				if food_storage + food_increment > food_storage_limit:
					food_increment = food_storage_limit - food_storage
				food_storage += food_increment
				reward["food_increment"] += food_increment
				reward.update({"food_start_time": food_start_time})
				food_start_time = current_time
				remaining.update({"food_storage": food_storage})
				remaining.update({"food_start_time": food_start_time})
				sql_str = f"update factory set food_storage={food_storage}, food_factory_timer='{food_start_time}' where unique_id='{unique_id}'"
				await self._execute_statement_update(world=world, statement=sql_str)
			return self._message_typesetting(status=0, message="Food factory update success", data={"remaining": remaining, "reward": reward})
		else:
			return self._message_typesetting(status=99, message="Food factory did not start")

	@C.collect_async
	async def refresh_mine_storage(self, world: int, unique_id: str) -> dict:
		# 0  - Mine factory update success
		# 99 - Mine factory did not start
		mine_factory = self._factory_config["mine_factory"]
		factory_data = await self._select_factory(world=world, unique_id=unique_id)
		# 配置文件中工厂等级下的最大容量
		mine_storage_limit = mine_factory["storage_limit"][str(factory_data[2])]
		# 数据库中存的工厂工作的开始时间
		mine_start_time = factory_data[6]
		# 数据库中存的工人的数量
		mine_factory_workers = factory_data[10]
		# 数据库中存的物资数量
		food_storage = factory_data[14]
		iron_storage = factory_data[15]
		# 数据库中的加速时间
		acceleration_end_time = factory_data[20]
		acceleration_value = 1
		times = 1
		current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		if acceleration_end_time:  # 加速中 存在日期
			acceleration_value = 2  # 加速的倍数设置
			time_difference = datetime.strptime(acceleration_end_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
			if int(time_difference.total_seconds()) <= 0:  # 加速卡过期
				times = 2
				current_time = acceleration_end_time
				await self._execute_statement_update(world=world, statement=f"update factory set acceleration_end_time='' where unique_id='{unique_id}'")
		remaining = {"mine_factory_workers": mine_factory_workers}
		reward = {"iron_increment": 0}
		if mine_start_time:
			for i in range(times):
				if times == 2 and i == 1:
					acceleration_value = 1
					current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
				cost_food = mine_factory["cost"]["food"]
				time_difference = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(mine_start_time, '%Y-%m-%d %H:%M:%S')
				iron_increment = int(time_difference.total_seconds()) // mine_factory["time_consuming"] * mine_factory_workers * acceleration_value
				if iron_increment < 0: continue
				if iron_storage + iron_increment > mine_storage_limit:
					iron_increment = mine_storage_limit - iron_storage
				if food_storage // cost_food < iron_increment:  # 1工人生产1铁消耗3食物
					iron_increment = food_storage // cost_food
				food_storage -= cost_food * iron_increment
				iron_storage += iron_increment
				reward["iron_increment"] += iron_increment
				reward.update({"mine_start_time": mine_start_time})
				mine_start_time = current_time
				remaining.update({"food_storage": food_storage})
				remaining.update({"iron_storage": iron_storage})
				remaining.update({"mine_start_time": mine_start_time})
				sql_str = f"update factory set iron_storage={iron_storage}, mine_factory_timer='{mine_start_time}' where unique_id='{unique_id}'"
				await self._execute_statement_update(world=world, statement=sql_str)
			return self._message_typesetting(status=0, message="Mine factory update success", data={"remaining": remaining, "reward": reward})
		else:
			return self._message_typesetting(status=99, message="Mine factory did not start")

	@C.collect_async
	async def refresh_crystal_storage(self, world: int, unique_id: str) -> dict:
		# 0  - Crystal factory update success
		# 99 - Crystal factory did not start
		mine_factory = self._factory_config["mine_factory"]
		crystal_factory = self._factory_config["crystal_factory"]
		factory_data = await self._select_factory(world=world, unique_id=unique_id)
		# 配置文件中工厂等级下的最大容量
		crystal_storage_limit = crystal_factory["storage_limit"][str(factory_data[3])]
		# 数据库中存的工厂工作的开始时间
		crystal_start_time = factory_data[7]
		# 数据库中存的工人的数量
		crystal_factory_workers = factory_data[11]
		# 数据库中存的物资数量
		food_storage = factory_data[14]
		iron_storage = factory_data[15]
		crystal_storage = factory_data[16]
		# 数据库中的加速时间
		acceleration_end_time = factory_data[20]
		acceleration_value = 1
		times = 1
		current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		if acceleration_end_time:  # 加速中 存在日期
			acceleration_value = 2  # 加速的倍数设置
			time_difference = datetime.strptime(acceleration_end_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
			if int(time_difference.total_seconds()) <= 0:  # 加速卡过期
				times = 2
				current_time = acceleration_end_time
				await self._execute_statement_update(world=world, statement=f"update factory set acceleration_end_time='' where unique_id='{unique_id}'")
		remaining = {"crystal_factory_workers": crystal_factory_workers}
		reward = {"crystal_increment": 0}
		if crystal_start_time:
			for i in range(times):
				if times == 2 and i == 1:
					acceleration_value = 1
					current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
				cost_food = crystal_factory["cost"]["food"]
				cost_iron = crystal_factory["cost"]["iron"]
				time_difference = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(crystal_start_time, '%Y-%m-%d %H:%M:%S')
				crystal_increment = int(time_difference.total_seconds()) // crystal_factory["time_consuming"] * crystal_factory_workers * acceleration_value
				if crystal_increment < 0: continue
				# 配置文件下的仓库容量约束
				if crystal_storage + crystal_increment > crystal_storage_limit:
					crystal_increment = crystal_storage_limit - crystal_storage
				# 数据库下的原始材料数量的约束
				if food_storage // cost_food < iron_storage // cost_iron:
					if food_storage // cost_food < crystal_increment:
						crystal_increment = food_storage // cost_food
				else:  # food_storage // cost_food >= iron_storage // cost_iron
					if iron_storage // cost_iron < crystal_increment:
						crystal_increment = iron_storage // cost_iron
				food_storage -= cost_food * crystal_increment
				iron_storage -= cost_iron * crystal_increment
				crystal_storage += crystal_increment
				reward["crystal_increment"] += crystal_increment
				reward.update({"crystal_start_time": crystal_start_time})
				crystal_start_time = current_time
				remaining.update({"food_storage": food_storage})
				remaining.update({"iron_storage": iron_storage})
				remaining.update({"crystal_storage": crystal_storage})
				remaining.update({"crystal_start_time": crystal_start_time})
				sql_str = f"update factory set crystal_storage={crystal_storage}, crystal_factory_timer='{crystal_start_time}' where unique_id='{unique_id}'"
				await self._execute_statement_update(world=world, statement=sql_str)
			return self._message_typesetting(status=0, message="Crystal factory update success", data={"remaining": remaining, "reward": reward})
		else:
			return self._message_typesetting(status=99, message="Crystal factory did not start")

	@C.collect_async
	async def refresh_equipment_storage(self, world: int, unique_id: str) -> dict:
		"""
		0  - Equipment factory update success
		99 - Equipment factory did not start
		"""
		equipment_factory = self._factory_config["equipment_factory"]
		factory_data = await self._select_factory(world=world, unique_id=unique_id)
		# 数据库中存的工厂工作的开始时间
		equipment_start_time = factory_data[8]
		# 数据库中存的工人的数量
		equipment_factory_workers = factory_data[12]
		# 数据库中存的物资数量
		iron_storage = factory_data[15]
		equipment_storage = factory_data[17]
		# 数据库中的加速时间
		acceleration_end_time = factory_data[20]
		# 数据库中的制造的盔甲类型
		equipment_product_type = factory_data[22]
		acceleration_value = 1
		times = 1
		current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		if acceleration_end_time:  # 加速中 存在日期
			acceleration_value = 2  # 加速的倍数设置
			time_difference = datetime.strptime(acceleration_end_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
			if int(time_difference.total_seconds()) <= 0:  # 加速卡过期
				times = 2
				current_time = acceleration_end_time
				await self._execute_statement_update(world=world, statement=f"update factory set acceleration_end_time='' where unique_id='{unique_id}'")
		remaining = {"equipment_factory_workers": equipment_factory_workers}
		reward = {"equipment_increment": 0}
		if equipment_start_time:
			if not equipment_product_type:
				equipment_product_type = "armor1"
			for i in range(times):
				if times == 2 and i == 1:
					acceleration_value = 1
					current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
				cost_iron = equipment_factory[equipment_product_type]["cost"]["iron"]
				time_difference = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(equipment_start_time, '%Y-%m-%d %H:%M:%S')
				equipment_increment = int(time_difference.total_seconds()) // equipment_factory[equipment_product_type]["time_consuming"] * equipment_factory_workers * acceleration_value
				if equipment_increment < 0: continue
				if iron_storage // cost_iron < equipment_increment:
					equipment_increment = iron_storage // cost_iron
				iron_storage -= equipment_increment * cost_iron
				equipment_storage += equipment_increment
				reward["equipment_increment"] += equipment_increment
				reward.update({"equipment_start_time": equipment_start_time})
				equipment_start_time = current_time
				remaining.update({"iron_storage": iron_storage})
				remaining.update({"equipment_storage": equipment_storage})
				remaining.update({"equipment_start_time": equipment_start_time})
				sql_str = f"update factory set equipment_storage={equipment_storage}, equipment_factory_timer='{equipment_start_time}', equipment_product_type='{equipment_product_type}' where unique_id='{unique_id}'"
				await self._execute_statement_update(world=world, statement=sql_str)

			return self._message_typesetting(status=0, message="Equipment factory update success", data={"remaining": remaining, "reward": reward})
		else:
			return self._message_typesetting(status=99, message="Equipment factory did not start")

	@C.collect_async
	async def refresh_all_storage(self, world: int, unique_id: str) -> dict:
		"""
		0 -  update factory success
		99 - update factory failed, all factories are not initialized
		"""
		food_factory = self._factory_config["food_factory"]
		mine_factory = self._factory_config["mine_factory"]
		crystal_factory = self._factory_config["crystal_factory"]
		equipment_factory = self._factory_config["equipment_factory"]
		factory_data = await self._select_factory(world=world, unique_id=unique_id)
		# 配置文件中工厂等级下的最大容量
		food_storage_limit = food_factory["storage_limit"][str(factory_data[1])]
		mine_storage_limit = mine_factory["storage_limit"][str(factory_data[2])]
		crystal_storage_limit = crystal_factory["storage_limit"][str(factory_data[3])]
		# 数据库中存的工厂工作的开始时间
		food_start_time = factory_data[5]
		mine_start_time = factory_data[6]
		crystal_start_time = factory_data[7]
		equipment_start_time = factory_data[8]
		# 数据库中存的工人的数量
		food_factory_workers = factory_data[9]
		mine_factory_workers = factory_data[10]
		crystal_factory_workers = factory_data[11]
		equipment_factory_workers = factory_data[12]
		# 数据库中存的物资数量
		food_storage = factory_data[14]
		iron_storage = factory_data[15]
		crystal_storage = factory_data[16]
		equipment_storage = factory_data[17]
		# 数据库中的加速时间
		acceleration_end_time = factory_data[20]
		# 数据库中的制造的盔甲类型
		equipment_product_type = factory_data[22]

		remaining = {"food_factory_workers": food_factory_workers, "mine_factory_workers": mine_factory_workers, "crystal_factory_workers": crystal_factory_workers, "equipment_factory_workers": equipment_factory_workers}
		reward = {"food_increment": 0, "iron_increment": 0, "crystal_increment": 0, "equipment_increment": 0}

		acceleration_value = 1
		times = 1
		current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

		if acceleration_end_time:  # 加速中 存在日期
			acceleration_value = 2  # 加速的倍数设置
			time_difference = datetime.strptime(acceleration_end_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
			if int(time_difference.total_seconds()) <= 0:
				times = 2
				current_time = acceleration_end_time
				await self._execute_statement_update(world=world, statement=f"update factory set acceleration_end_time='' where unique_id='{unique_id}'")

		for i in range(times):
			if times == 2 and i == 1:
				acceleration_value = 1
				current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
			if food_start_time:  # food_start_time != ""
				time_difference = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(food_start_time, '%Y-%m-%d %H:%M:%S')
				food_increment = int(time_difference.total_seconds()) // food_factory["time_consuming"] * food_factory_workers * acceleration_value
				if food_storage + food_increment > food_storage_limit:
					food_increment = food_storage_limit - food_storage
				food_storage += food_increment
				reward["food_increment"] += food_increment
				reward.update({"food_start_time": food_start_time})
				food_start_time = current_time
				remaining.update({"food_storage": food_storage})
				remaining.update({"food_start_time": food_start_time})
			if mine_start_time:
				cost_food = mine_factory["cost"]["food"]
				time_difference = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(mine_start_time, '%Y-%m-%d %H:%M:%S')
				iron_increment = int(time_difference.total_seconds()) // mine_factory["time_consuming"] * mine_factory_workers * acceleration_value
				if iron_storage + iron_increment > mine_storage_limit:
					iron_increment = mine_storage_limit - iron_storage
				if food_storage // cost_food < iron_increment:  # 1工人生产1铁消耗3食物
					iron_increment = food_storage // cost_food
				food_storage -= cost_food * iron_increment
				iron_storage += iron_increment
				reward["iron_increment"] += iron_increment
				reward.update({"mine_start_time": mine_start_time})
				mine_start_time = current_time
				remaining.update({"food_storage": food_storage})
				remaining.update({"iron_storage": iron_storage})
				remaining.update({"mine_start_time": mine_start_time})
			if crystal_start_time:
				cost_food = crystal_factory["cost"]["food"]
				cost_iron = crystal_factory["cost"]["iron"]
				time_difference = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(crystal_start_time, '%Y-%m-%d %H:%M:%S')
				crystal_increment = int(time_difference.total_seconds()) // crystal_factory["time_consuming"] * crystal_factory_workers * acceleration_value
				# 配置文件下的仓库容量约束
				if crystal_storage + crystal_increment > crystal_storage_limit:
					crystal_increment = crystal_storage_limit - crystal_storage
				# 数据库下的原始材料数量的约束
				if food_storage // cost_food < iron_storage // cost_iron:
					if food_storage // cost_food < crystal_increment:
						crystal_increment = food_storage // cost_food
				else:  # food_storage // cost_food >= iron_storage // cost_iron
					if iron_storage // cost_iron < crystal_increment:
						crystal_increment = iron_storage // cost_iron
				food_storage -= cost_food * crystal_increment
				iron_storage -= cost_iron * crystal_increment
				crystal_storage += crystal_increment
				reward["crystal_increment"] += crystal_increment
				reward.update({"crystal_start_time": crystal_start_time})
				crystal_start_time = current_time
				remaining.update({"food_storage": food_storage})
				remaining.update({"iron_storage": iron_storage})
				remaining.update({"crystal_storage": crystal_storage})
				remaining.update({"crystal_start_time": crystal_start_time})
			if equipment_start_time:
				if not equipment_product_type:
					equipment_product_type = "armor1"
				cost_iron = equipment_factory[equipment_product_type]["cost"]["iron"]
				time_difference = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(equipment_start_time, '%Y-%m-%d %H:%M:%S')
				equipment_increment = int(time_difference.total_seconds()) // equipment_factory[equipment_product_type]["time_consuming"] * equipment_factory_workers * acceleration_value
				if iron_storage // cost_iron < equipment_increment:
					equipment_increment = iron_storage // cost_iron
				iron_storage -= equipment_increment * cost_iron
				equipment_storage += equipment_increment
				reward["equipment_increment"] += equipment_increment
				reward.update({"equipment_start_time": equipment_start_time})
				reward.update({"equipment_product_type": equipment_product_type})
				equipment_start_time = current_time
				remaining.update({"iron_storage": iron_storage})
				remaining.update({"equipment_storage": equipment_storage})
				remaining.update({"equipment_start_time": equipment_start_time})
				remaining.update({"equipment_product_type": equipment_product_type})

			sql_str = f"update factory set food_storage={food_storage}, iron_storage={iron_storage}, crystal_storage={crystal_storage}, equipment_storage={equipment_storage}, food_factory_timer='{food_start_time}', mine_factory_timer='{mine_start_time}', crystal_factory_timer='{crystal_start_time}', equipment_factory_timer='{equipment_start_time}', equipment_product_type='{equipment_product_type}' where unique_id='{unique_id}'"
			await self._execute_statement_update(world=world, statement=sql_str)
		if len(reward) > 4:
			return self._message_typesetting(status=0, message="update factory success", data={"remaining": remaining, "reward": reward})
		return self._message_typesetting(status=99, message="update factory failed, all factories are not initialized")

	@C.collect_async
	async def distribution_workers(self, world: int, unique_id: str, workers_quantity: int, factory_kind: str) -> dict:
		"""
		0  - Successful employee assignment, get factory work rewards
		1  - Successful employee assignment
		2  - Allocation is full
		97 - Insufficient distribution workers
		98 - Factory type error
		99 - The number of workers assigned is not a positive integer
		思路： 判断分配的工人数量workers_quantity是否为为正整数 The number of workers assigned is not a positive integer ==> 代号99，
		工厂类型factory_kind是否在数据库表中 Factory type error ==> 代号98，查询数据库表中是否存在unique_id的数据，
		不存在则创建，获取数据库中的所有工人的数量totally_workers和正在此工厂工作的工人数量factory_workers，
		先判断所有工人的数量是否大于等于工厂等级下限制的工人数量
		后判断所有工人的数量是否大于等于分配的工人数量
		如果小于则分配完所有的工人到指定的工厂下工作
		最终正确结果返回字典键值对包含以下：==> 代号0
			remaining：
				1.所有工人的数量：totally_workers
				2.指定的工厂下工作人员数量：factory_workers
				3.工厂开始工作时间：start_time
				4.工厂生产的所有物品数量：storage
			reward：
				5.工厂生产的所有物品增加的数量：increment
				6.工厂生产物品结算的开始时间：start_time
		问题：如果指定工厂之前存在工人在工作则结算后的工作时间是否统一成当前时间
		"""
		all_factory = self._factory_config["factory_kind"]
		if workers_quantity <= 0:
			return self._message_typesetting(status=99, message="The number of workers assigned is not a positive integer")

		if factory_kind not in all_factory:
			return self._message_typesetting(status=98, message="Factory type error")

		factory_mark = all_factory.index(factory_kind)
		remaining = {}
		reward = {}
		result = await self.refresh_all_storage(world, unique_id)
		if result["data"]:
			remaining = result["data"]["remaining"]
			reward = result["data"]["reward"]
		factory_data = await self._select_factory(world=world, unique_id=unique_id)
		factory_config = self._factory_config[f"{factory_kind}_factory"]
		factory_level = factory_data[1 + factory_mark]
		factory_workers = factory_data[9 + factory_mark]
		totally_workers = factory_data[13]
		current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		if factory_kind != "equipment":
			# 配置文件下的工作人员上限限制
			workers_number_limit = factory_config["workers_number_limit"][str(factory_level)]
			if factory_workers + workers_quantity > workers_number_limit:
				workers_quantity = workers_number_limit - factory_workers
		# 数据库可分配人员数量的限制
		if workers_quantity > totally_workers:
			workers_quantity = totally_workers
		totally_workers -= workers_quantity
		factory_workers += workers_quantity
		sql_str = f"update factory set totally_workers={totally_workers}, {factory_kind}_factory_workers={factory_workers}, {factory_kind}_factory_timer='{current_time}' where unique_id='{unique_id}'"
		await self._execute_statement_update(world=world, statement=sql_str)
		remaining.update({"totally_workers": totally_workers, f"{factory_kind}_factory_workers": factory_workers, f"{factory_kind}_start_time": current_time})
		if workers_quantity == 0:
			return self._message_typesetting(status=2, message="Allocation is full", data={"remaining": remaining, "reward": reward})
		if reward:
			return self._message_typesetting(status=0, message="Successful employee assignment, get factory work rewards", data={"remaining": remaining, "reward": reward})
		return self._message_typesetting(status=1, message="Successful employee assignment", data={"remaining": remaining})

	@C.collect_async
	async def equipment_manufacturing_armor(self, world: int, unique_id: str, armor_id: str) -> dict:
		"""
		0 - Successfully opened manufacturing armor
		1 - Armor table update failed, factory has been updated
		99 - No such armor type
		"""
		equipment_factory = self._factory_config["equipment_factory"]
		if armor_id not in equipment_factory["armor_id"]:
			return self._message_typesetting(status=99, message="No such armor type")
		remaining = {}
		reward = {}
		result = await self.refresh_all_storage(world, unique_id)
		if result["status"] == 0:
			remaining = result["data"]["remaining"]
			reward = result["data"]["reward"]
		factory_data = await self._select_factory(world, unique_id)
		sql_armor_quantity = factory_data[17]
		sql_armor_id = factory_data[22]
		if sql_armor_id and sql_armor_quantity:
			reward.update({"armor_id": sql_armor_id, "armor_quantity": sql_armor_quantity})
			armor_data = await self.try_armor(world, unique_id, armor_id, "armor_level1", sql_armor_quantity)
			if armor_data["status"]:
				return self._message_typesetting(status=1, message="Armor table update failed, factory has been updated", data={"remaining": remaining, "reward": reward})
			remaining.update({"armor_id": sql_armor_id, "armor_quantity": armor_data["remaining"]})
		update_str = f"update factory set equipment_storage=0, equipment_product_type='{armor_id}' where unique_id='{unique_id}'"
		await self._execute_statement_update(world, update_str)
		remaining.update({"finally_equipment_storage": 0, "finally_equipment_product_type": armor_id})
		return self._message_typesetting(status=0, message="Successfully opened manufacturing armor", data={"remaining": remaining, "reward": reward})

	@C.collect_async
	async def buy_workers(self, world: int, unique_id: str, workers_quantity: int) -> dict:
		"""
		0  - Buy workers success, storage has been refreshed
		1  - Buy workers success
		98 - Buy workers failed, insufficient food
		99 - The number of workers can only be a positive integer
		思路：查询所有工人的数量，读取配置文件下的工人数量购买限制，
		此时需不需要刷新食物工厂？
		判断购买的工人数量是否大于等于最大工人数限制，
		判断需要的食物数量是否足够
		"""
		if workers_quantity <= 0:
			return self._message_typesetting(status=99, message="The number of workers can only be a positive integer")
		remaining = {}
		reward = {}
		result = await self.refresh_all_storage(world,unique_id)
		if result["status"] == 0:
			remaining = result["data"]["remaining"]
			reward = result["data"]["reward"]
		workers_max = self._factory_config["buy_workers_max"]
		workers_max_food = self._factory_config["buy_workers_max_food"]
		workers_need_food = self._factory_config["buy_workers_need_food"]
		factory_data = await self._select_factory(world, unique_id)
		food_storage = factory_data[14]
		all_workers = sum(factory_data[9: 14], 1)  # 多加一人
		if all_workers >= workers_max:
			if workers_quantity * workers_max_food > food_storage:
				workers_quantity = food_storage // workers_max_food
			food_storage -= workers_quantity * workers_max_food
		else:
			for worker in range(workers_quantity):  # 0开始递增，刚好多减一人，与最初平等
				workers_next = all_workers + worker
				if workers_next >= workers_max:
					if workers_max_food > food_storage:
						workers_quantity = worker  # 此工人没有被购买
						break
					else:
						food_storage -= workers_max_food
				else:
					need_food = workers_need_food[str(workers_next)]
					if need_food > food_storage:
						workers_quantity = worker  # 此工人没有被购买
						break
					else:
						food_storage -= need_food
		if workers_quantity == 0:
			return self._message_typesetting(status=98, message="buy workers failed, insufficient food")
		all_workers += workers_quantity - 1  # 多减一人，与最初平等
		totally_workers = all_workers - sum(factory_data[9: 13])
		sql_str = f"update factory set totally_workers={totally_workers}, food_storage={food_storage} where unique_id='{unique_id}'"
		await self._execute_statement_update(world=world, statement=sql_str)
		remaining.update({"all_workers": all_workers, "totally_workers": totally_workers, "buy_workers_quantity": workers_quantity, "food_storage": food_storage})
		if reward:
			return self._message_typesetting(status=0, message="Buy workers success, storage has been refreshed", data={"remaining": remaining, "reward": reward})
		return self._message_typesetting(status=1, message="Buy workers success", data={"remaining": remaining})

	@C.collect_async
	async def upgrade_food_factory(self, world: int, unique_id: str, upgrade_level: int = 1) -> dict:
		"""
		0  - Upgrade food factory success
		1  - Upgrade food factory success, storage has been refreshed
		2  - Upgrade factory failed, Insufficient crystal, storage has been refreshed
		# 97 - Upgrade factory failed，Insufficient crystal
		98 - The factory has reached full level
		99 - Upgrade level can only be a positive integer
		思路：判断upgrade_level是否为正整数，查询数据库中的工厂等级是否达到满级
		读取配置文件下升级工厂需要的材料限制
		"""
		if upgrade_level <= 0:
			return self._message_typesetting(status=99, message="Upgrade level can only be a positive integer")
		storage_level_limit = self._factory_config["food_factory"]["storage_level_limit"]
		upgrade_need_crystals = self._factory_config["food_factory"]["upgrade_need_crystals_limit"]
		factory_data = await self._select_factory(world, unique_id)
		factory_level = factory_data[1]
		all_crystal = factory_data[16]
		remaining = {}
		reward = {}
		result = await self.refresh_all_storage(world, unique_id)
		if result["status"] == 0:
			remaining = result["data"]["remaining"]
			reward = result["data"]["reward"]
		if factory_level == storage_level_limit:
			return self._message_typesetting(status=98, message="The factory has reached full level")
		if factory_level + upgrade_level > storage_level_limit:
			upgrade_level = storage_level_limit - factory_level
		for upgrade in range(upgrade_level):
			need_crystal = upgrade_need_crystals[str(factory_level + upgrade + 1)]
			if need_crystal > all_crystal:
				upgrade_level = upgrade
				break
			else:
				all_crystal -= need_crystal
		if upgrade_level == 0:
			return self._message_typesetting(status=2, message="Upgrade factory failed, Insufficient crystal, storage has been refreshed", data={"remaining": remaining, "reward": reward})
			# return self._message_typesetting(status=97, message="Upgrade factory failed, Insufficient crystal")
		factory_level += upgrade_level
		remaining.update({"food_factory_level": factory_level, "crystal_storage": all_crystal, "upgrade_level": upgrade_level})
		sql_str = f"update factory set food_factory_level={factory_level}, crystal_storage={all_crystal} where unique_id='{unique_id}'"
		await self._execute_statement_update(world=world, statement=sql_str)
		if reward:
			return self._message_typesetting(status=1, message="Upgrade food factory success, storage has been refreshed", data={"remaining": remaining, "reward": reward})
		return self._message_typesetting(status=0, message="Upgrade food factory success", data={"remaining": remaining})

	@C.collect_async
	async def upgrade_mine_factory(self, world: int, unique_id: str) -> dict:
		"""
		0  - Upgrade mine factory success
		1  - Upgrade mine factory success, storage has been refreshed
		2  - Upgrade factory failed, Insufficient crystal, storage has been refreshed
		# 97 - Upgrade factory failed，Insufficient crystal
		98 - The factory has reached full level
		"""
		storage_level_limit = self._factory_config["mine_factory"]["storage_level_limit"]
		upgrade_need_crystals = self._factory_config["mine_factory"]["upgrade_need_crystals_limit"]
		factory_data = await self._select_factory(world, unique_id)
		factory_level = factory_data[2]
		all_crystal = factory_data[16]
		remaining = {}
		reward = {}
		result = await self.refresh_all_storage(world, unique_id)
		if result["status"] == 0:
			remaining = result["data"]["remaining"]
			reward = result["data"]["reward"]
		if factory_level == storage_level_limit:
			return self._message_typesetting(status=98, message="The factory has reached full level")
		factory_level += 1
		need_crystal = upgrade_need_crystals[str(factory_level)]
		if need_crystal > all_crystal:
			return self._message_typesetting(status=2, message="Upgrade factory failed, Insufficient crystal, storage has been refreshed", data={"remaining": remaining, "reward": reward})
			# return self._message_typesetting(status=97, message="Upgrade factory failed, Insufficient crystal")
		else:
			all_crystal -= need_crystal
		remaining.update({"mine_factory_level": factory_level, "crystal_storage": all_crystal, "upgrade_level": 1})
		sql_str = f"update factory set mine_factory_level={factory_level}, crystal_storage={all_crystal} where unique_id='{unique_id}'"
		await self._execute_statement_update(world=world, statement=sql_str)
		if reward:
			return self._message_typesetting(status=1, message="Upgrade mine factory success, storage has been refreshed", data={"remaining": remaining, "reward": reward})
		return self._message_typesetting(status=0, message="Upgrade mine factory success", data={"remaining": remaining})

	@C.collect_async
	async def upgrade_crystal_factory(self, world: int, unique_id: str) -> dict:
		"""
		0  - Upgrade crystal factory success
		1  - Upgrade crystal factory success, storage has been refreshed
		2  - Upgrade factory failed, Insufficient crystal, storage has been refreshed
		# 97 - Upgrade factory failed，Insufficient crystal
		98 - The factory has reached full level
		"""
		storage_level_limit = self._factory_config["crystal_factory"]["storage_level_limit"]
		upgrade_need_crystals = self._factory_config["crystal_factory"]["upgrade_need_crystals_limit"]
		factory_data = await self._select_factory(world, unique_id)
		factory_level = factory_data[3]
		all_crystal = factory_data[16]
		remaining = {}
		reward = {}
		result = await self.refresh_all_storage(world, unique_id)
		if result["status"] == 0:
			remaining = result["data"]["remaining"]
			reward = result["data"]["reward"]
		if factory_level == storage_level_limit:
			return self._message_typesetting(status=98, message="The factory has reached full level")
		factory_level += 1
		need_crystal = upgrade_need_crystals[str(factory_level)]
		if need_crystal > all_crystal:
			return self._message_typesetting(status=2, message="Upgrade factory failed, Insufficient crystal, storage has been refreshed", data={"remaining": remaining, "reward": reward})
			# return self._message_typesetting(status=97, message="Upgrade factory failed, Insufficient crystal")
		else:
			all_crystal -= need_crystal
		remaining.update({"crystal_factory_level": factory_level, "crystal_storage": all_crystal, "upgrade_level": 1})
		sql_str = f"update factory set crystal_factory_level={factory_level}, crystal_storage={all_crystal} where unique_id='{unique_id}'"
		await self._execute_statement_update(world=world, statement=sql_str)
		if reward:
			return self._message_typesetting(status=1, message="Upgrade crystal factory success, storage has been refreshed", data={"remaining": remaining, "reward": reward})
		return self._message_typesetting(status=0, message="Upgrade crystal factory success", data={"remaining": remaining})

	@C.collect_async
	async def upgrade_wishing_pool(self, world: int, unique_id: str) -> dict:
		"""
		0  - Upgrade wishing pool success
		1  - Upgrade wishing pool success, storage has been refreshed
		2  - Upgrade wishing pool failed, Insufficient crystal, storage has been refreshed
		# 97 - Upgrade wishing pool failed，Insufficient crystal
		98 - The wishing pool has reached full level
		"""
		storage_level_limit = self._factory_config["wishing_pool"]["storage_level_limit"]
		upgrade_need_crystals = self._factory_config["wishing_pool"]["upgrade_need_crystals_limit"]
		factory_data = await self._select_factory(world, unique_id)
		factory_level = factory_data[18]
		all_crystal = factory_data[16]
		remaining = {}
		reward = {}
		result = await self.refresh_all_storage(world, unique_id)
		if result["status"] == 0:
			remaining = result["data"]["remaining"]
			reward = result["data"]["reward"]
		if factory_level == storage_level_limit:
			return self._message_typesetting(status=98, message="The wishing pool has reached full level")
		factory_level += 1
		need_crystal = upgrade_need_crystals[str(factory_level)]
		if need_crystal > all_crystal:
			return self._message_typesetting(status=2, message="Upgrade wishing pool failed, Insufficient crystal, storage has been refreshed", data={"remaining": remaining, "reward": reward})
			# return self._message_typesetting(status=97, message="Upgrade factory failed, Insufficient crystal")
		else:
			all_crystal -= need_crystal
		remaining.update({"wishing_pool_level": factory_level, "crystal_storage": all_crystal, "upgrade_level": 1})
		sql_str = f"update factory set wishing_pool_level={factory_level}, crystal_storage={all_crystal} where unique_id='{unique_id}'"
		await self._execute_statement_update(world=world, statement=sql_str)
		if reward:
			return self._message_typesetting(status=1, message="Upgrade wishing pool success, storage has been refreshed", data={"remaining": remaining, "reward": reward})
		return self._message_typesetting(status=0, message="Upgrade wishing pool success", data={"remaining": remaining})

	@C.collect_async
	async def acceleration_technology(self, world: int, unique_id: str) -> dict:
		"""
		0  - Accelerate success
		1  - Accelerate failed, update factory success
		99 - update factory failed, all factories are not initialized, accelerate failed
		"""
		remaining = {}
		reward = {}
		result = await self.refresh_all_storage(world, unique_id)
		if result["status"] == 0:
			remaining = result["data"]["remaining"]
			reward = result["data"]["reward"]
			diamond_data = await self.try_diamond(world=world, unique_id=unique_id, value=-self._factory_config["acceleration_consuming_diamond"])
			if diamond_data["status"] == 1:
				return self._message_typesetting(status=1, message="Accelerate failed, update factory success", data={"remaining": remaining, "reward": reward})
			remaining.update({"diamond": diamond_data["remaining"]})
		else:
			return self._message_typesetting(status=99, message="update factory failed, all factories are not initialized, accelerate failed")
		acceleration_end_time = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
		await self._execute_statement_update(world=world, statement=f"update factory set acceleration_end_time='{acceleration_end_time}' where unique_id='{unique_id}'")
		remaining.update({"acceleration_end_time": acceleration_end_time})
		return self._message_typesetting(status=0, message="Accelerate success", data={"remaining": remaining, "reward": reward})

	@C.collect_async
	async def get_factory_info(self, world: int, unique_id: str) -> dict:
		"""
		0  - Successfully obtained configuration information
		"""
		remaining = {}
		sql_info = {}
		data_head = (await self.get_all_head(world, table="factory"))["remaining"]
		factory_data = await self._select_factory(world=world, unique_id=unique_id)
		for i in range(1, len(data_head)):
			sql_info.update({data_head[i][0]: factory_data[i]})
		remaining.update({"sql_info": sql_info})
		remaining.update({"server_config": self._factory_config})
		return self._message_typesetting(status=0, message="Successfully obtained configuration information", data={"remaining": remaining})

#############################################################################
#							End Factory Functions							#
#############################################################################



#############################################################################
#							Private Functions								#
#############################################################################

	async def _select_factory(self, world: int, unique_id) -> list:
		sql_str = f"select * from factory where unique_id={unique_id}"
		data = await self._execute_statement(world, sql_str)
		if data: return data[0]
		await self._execute_statement(world, f"INSERT INTO factory (unique_id) VALUES ('{unique_id}')")
		return list((await self._execute_statement(world, sql_str))[0])

	async def _family_exists(self, world: int, fname: str):
		return (0,) not in (await self._execute_statement(world, f'SELECT COUNT(1) FROM families WHERE familyname = "{fname}";'))

	async def _get_family_information(self, world: int, fid: str) -> tuple:
		return await self._execute_statement(world, f'SELECT * FROM families WHERE familyid = "{fid}";')

	async def _get_familyid(self, world: int, **kwargs):
		if 'unique_id' in kwargs:
			data = await self._execute_statement(world, f'SELECT game_name, familyid, union_login, union_contribution FROM player WHERE unique_id = "{kwargs["unique_id"]}";')
		else:
			data = await self._execute_statement(world, f'SELECT game_name, familyid, union_login, union_contribution FROM player WHERE game_name = "{kwargs["game_name"]}";')
		return data[0] if data else ('', '', '', 0)

	async def _get_dark_market_material(self, world: int, unique_id: str, code: int) -> tuple:
		sql_str = 'SELECT merchandise%s, merchandise%s_quantity, currency_type%s, currency_type%s_price, refresh_time, refreshable_quantity FROM dark_market WHERE unique_id = "%s";' % (code, code, code, code, unique_id)
		data = await self._execute_statement(world, sql_str)
		return data[0]

	async def _set_dark_market_material(self, world: int, unique_id: str, code: int, merchandise: str, merchandise_quantity: int, currency_type: str, currency_type_price: int, refresh_time: str, refreshable_quantity: int) -> int:
		sql_str = 'UPDATE dark_market SET merchandise%s="%s", merchandise%s_quantity="%s", currency_type%s="%s", currency_type%s_price="%s", refresh_time="%s", refreshable_quantity="%s" WHERE unique_id="%s";' % (code, merchandise, code, merchandise_quantity, code, currency_type, code, currency_type_price, refresh_time, refreshable_quantity, unique_id)
		return await self._execute_statement_update(world, sql_str)

	async def _default_fortune_wheel(self, world: int, uid: str, cost_item: str, tier: str):
		# 0  - get energy success
		# 1  - get weapon success
		# 2  - get weapon segment success
		# 3  - get skill success
		# 4  - already have skill, get scroll
		# 5  - get item success
		# 96 - item name error
		# 97 - database skill operation error
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

		# TODO THIS SHIT NEEDS TO BE REFACTORED
		if random_item == 'coin':
			try_result = await self.try_coin(world, uid, int(self._lottery['fortune_wheel']['reward'][tier][random_item]))
		elif random_item == 'energy':
			try_result = await self.try_energy(world, uid, int(self._lottery['fortune_wheel']['reward'][tier][random_item]))
			keys = try_result["keys"]
			values = try_result["values"]
			remaining = {"cost_item": cost_item, "cost_quantity": result["remaining"]}
			for i in range(len(keys)):
				remaining.update({keys[i]: values[i]})
			return self._message_typesetting(0, 'get energy success', {'remaining' : remaining, 'reward' : {random_item: self._lottery['fortune_wheel']['reward'][tier][random_item]}})
		elif random_item == 'diamond':
			try_result = await self.try_diamond(world, uid, int(self._lottery['fortune_wheel']['reward'][tier][random_item]))
		elif random_item == 'iron':
			try_result = await self.try_iron(world, uid, int(self._lottery['fortune_wheel']['reward'][tier][random_item]))
		elif random_item == 'skill_scroll_10':
			try_result = await self.try_skill_scroll_10(world, uid, int(self._lottery['fortune_wheel']['reward'][tier][random_item]))
		elif random_item == 'skill_scroll_30':
			try_result = await self.try_skill_scroll_30(world, uid, int(self._lottery['fortune_wheel']['reward'][tier][random_item]))
		elif random_item == 'skill_scroll_100':
			try_result = await self.try_skill_scroll_100(world, uid, int(self._lottery['fortune_wheel']['reward'][tier][random_item]))
		elif random_item == 'weapon':
			try_result = await self.random_gift_weapon(world, uid, tier)
			if try_result['status'] == 0:
				message_dic = {
					"remaining" :
					{
						"weapon" : try_result['data']['values'][0],
						'star' : try_result['data']['values'][1],
						'segment' : try_result['data']['values'][2],
						"cost_item": cost_item,
						"cost_quantity": result["remaining"]
					},
					'reward':
					{
						'weapon' : try_result['data']['values'][0],
						'star' : 1
					}
				}
				return self._message_typesetting(1, 'get weapon success', message_dic)
			elif try_result['status'] == 1:
				message_dic = {
					"remaining" :
					{
						"weapon" : try_result['data']['values'][0],
						'star' : try_result['data']['values'][1],
						'segment' : try_result['data']['values'][2],
						"cost_item": cost_item,
						"cost_quantity": result["remaining"]
					},
					'reward':
					{
						'weapon' : try_result['data']['values'][0],
						'segment' : self._role_config["standard_segment_count"]
					}
				}
				return self._message_typesetting(2, 'get weapon segment success', message_dic)
			else:
				return self._message_typesetting(97, 'database weapon operation error')
		elif random_item == 'skill':
			try_result = await self.random_gift_skill(world, uid, tier)
			if try_result['status'] == 0:
				message_dic = {
					"remaining":
					{
						"skill_id" : try_result['data']['keys'][0],
						'skill_level' : try_result['data']['values'][0],
						"cost_item": cost_item,
						"cost_quantity": result["remaining"]
					},
					'reward':
					{
						'skill_id' : try_result['data']['keys'][0],
						'skill_level' : 1
					}
				}
				return self._message_typesetting(3, 'get skill success', message_dic)
			elif try_result['status'] == 1:
				message_dic = {
					'remaining' :
					{
						'scroll_id' : try_result['data']['keys'][0],
						'scroll_quantity' : try_result['data']['values'][0],
						"cost_item": cost_item,
						"cost_quantity": result["remaining"]
					},
					'reward' :
					{
						'scroll_id' : try_result['data']['values'][0],
						'scroll_quantity' : 1
					}
				}
				return self._message_typesetting(4, 'already have skill, get scroll', message_dic)
			else:
				return self._message_typesetting(97, 'database skill operation error')
		else:
			return self._message_typesetting(96, 'item name error')
		return self._message_typesetting(5, 'get item success', {'remaining' : {"cost_item": cost_item, "cost_quantity": result["remaining"], "item_id": random_item, "item_quantity": try_result['remaining']}, 'reward' : {"item_id": random_item, "item_quantity": self._lottery['fortune_wheel']['reward'][tier][random_item]}})

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
			recovered_energy = int(delta_time.total_seconds()) // 60 // _cooling_time
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
					cooling_time = 60 * _cooling_time - int(delta_time.total_seconds())
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
				return self._message_typesetting(6, 'After refreshing the energy, the energy value and recovery time are successfully updated.', {"keys": ['energy', 'recover_time', 'cooling_time'], "values": [current_energy, current_time, cooling_time]})
			elif recovered_energy + current_energy - amount >= 0:
				# 成功6：如果有恢复时间且是消耗能量
				# 不满足上限的情况是用当前数据库的能量值和当前恢复的能量值相加然后减去消耗的能量值为要存入数据库的能量值项
				# 数据库中的恢复时间与恢复能量消耗的时间相减的恢复时间值存入到数据库的恢复时间项
				current_energy = recovered_energy + current_energy - amount
				recover_time = (datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=recovered_energy * _cooling_time)).strftime("%Y-%m-%d %H:%M:%S")
				delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S')
				cooling_time = 60 * _cooling_time - int(delta_time.total_seconds())
				await self._execute_statement_update(world=world,statement='UPDATE player SET energy = ' + str(current_energy) + ', recover_time = "' + recover_time + '" WHERE unique_id = "' + unique_id + '";')
				return self._message_typesetting(7, 'Energy has been refreshed, not fully recovered, energy has been consumed, energy value and recovery time updated successfully', {"keys": ['energy', 'recover_time', 'cooling_time'], "values": [current_energy, recover_time, cooling_time]})
			else:  # 发生的情况是当前能量值和恢复能量值相加比需要消耗的能量值少
				return self._message_typesetting(status=98, message="Not enough energy consumption")

	async def try_basic_summon_scroll(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'basic_summon_scroll', value)

	async def try_pro_summon_scroll(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'pro_summon_scroll', value)

	async def try_friend_gift(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'friend_gift', value)

	async def try_fortune_wheel_ticket_basic(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'fortune_wheel_ticket_basic', value)

	async def try_fortune_wheel_ticket_pro(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'fortune_wheel_ticket_pro', value)

	# TODO REFACTOR REFACTOR REFACTOR
	async def _default_summon(self, world: int, unique_id: str, cost_item: str, tier: str, summon_item: str):
		# success -> 0 , 1 , 2 , 3 , 4 , 5
		# 0  - get skill item success
		# 1  - you already has skill, get scroll
		# 2  - get weapon success
		# 3  - get weapon segment success
		# 4  - get role item success
		# 5  - get role segment success
		# 95 - operation error
		# 96 - weapons operation error
		# 97 - skill operation error
		# 98 - insufficient materials
		# 99 - wrong item name
		if cost_item == "10_times":
			result = {"remaining": 0}
		else:
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
			else:
				return self._message_typesetting(99, 'wrong item name')
			if result['remaining'] < 0:
				return self._message_typesetting(98, 'insufficient materials')
		if summon_item == 'skills':
			try_result = await self.random_gift_skill(world, unique_id, tier)
			if try_result['status'] == 0 or try_result['status'] == 1:
				if try_result['status'] == 0:
					message_dic = {
						'remaining': {
							"skill_id": try_result['data']["keys"][0],
							"skill_level": try_result['data']["values"][0],
							"cost_item": cost_item,
							"cost_quantity": result["remaining"]
						},
						'reward': {
							"skill_id": try_result['data']["keys"][0],
							"skill_level": try_result['data']["values"][0]
						}
					}
					return self._message_typesetting(0, 'get skill item success', message_dic)
				else:
					message_dic = {
						'remaining': {
							"scroll_id": try_result['data']["keys"][0],
							"scroll_quantity": try_result['data']["values"][0],
							"cost_item": cost_item,
							"cost_quantity": result["remaining"]
						},
						'reward': {
							"scroll_id": try_result['data']["keys"][0],
							"scroll_quantity": 1
						}
					}
					return self._message_typesetting(1, 'you already has skill, get scroll', message_dic)
			else:
				return self._message_typesetting(97, 'skill operation error')
		elif summon_item == 'weapons':
			try_result = await self.random_gift_weapon(world, unique_id, tier)
			if try_result['status'] == 0 :
				message_dic = {
					'remaining':
					{
						'weapon': try_result['data']['values'][0],
						'star': try_result['data']['values'][1],
						'segment': try_result['data']['values'][2],
						"cost_item": cost_item,
						"cost_quantity": result["remaining"]
					},
					'reward':
					{
						'weapon': try_result['data']['values'][0],
						'star': 1
					}
				}
				return self._message_typesetting(2, 'get weapon success', message_dic)
			elif try_result['status'] == 1 :
				message_dic = {
					'remaining':
					{
						'weapon': try_result['data']['values'][0],
						'star': try_result['data']['values'][1],
						'segment': try_result['data']['values'][2],
						"cost_item": cost_item,
						"cost_quantity": result["remaining"]
					},
					'reward':
					{
						'weapon': try_result['data']['values'][0],
						'segment': self._weapon_config["standard_segment_count"]
					}
				}
				return self._message_typesetting(3, 'get weapon segment success', message_dic)
			else:
				return self._message_typesetting(96, 'weapons operation error')
		elif summon_item == 'roles':
			try_result = await self.random_gift_role(world, unique_id, tier)
			if try_result['status'] == 0:
				message_dic = {
					'remaining' :
					{
						'role' : try_result['data']['values'][0],
						'star' : try_result['data']['values'][1],
						'segment' : try_result['data']['values'][2],
						"cost_item": cost_item,
						"cost_quantity": result["remaining"]
					},
					'reward':
					{
						'role' : try_result['data']['values'][0],
						'star' : 1
					}
				}
				return self._message_typesetting(4, 'get role success', message_dic)
			elif try_result['status'] == 1:
				message_dic = {
					'remaining' :
					{
						'role' : try_result['data']['values'][0],
						'star' : try_result['data']['values'][1],
						'segment' : try_result['data']['values'][2],
						"cost_item": cost_item,
						"cost_quantity": result["remaining"]
					},
					'reward':
					{
						'role' : try_result['data']['values'][0],
						'segment' : self._role_config["standard_segment_count"]
					}
				}
				return self._message_typesetting(5, 'get role segment success', message_dic)
			else:
				return self._message_typesetting(95, 'operation error')

	async def _enter_world_boss_stage(self, world: int, unique_id: str):
		#0 enter world success
		#1 enter world success and you had never enter before
		#98 boss all died
		#99 Insufficient enter ticket
		if self._boss_life_remaining[9]<=0:
			return self._message_typesetting(status=98, message="boss all died")
		data = await self._execute_statement(world,f'select world_boss_enter_time,world_boss_remaining_times from player where unique_id ="{unique_id}"')
		current_time1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		current_time2 = (datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")
		d1 = datetime.strptime(current_time1, '%Y-%m-%d %H:%M:%S')
		d2 = datetime.strptime(current_time2, '%Y-%m-%d %H:%M:%S')
		if data[0][0]=="":
			data = await self._execute_statement_update(world,f'UPDATE player SET world_boss_enter_time ="{current_time1}",world_boss_remaining_times ="{str(self._max_enter_time-1)}" WHERE unique_id = "{unique_id}"')
			message_dic={
				'remaining' :
				{
					"world_boss_enter_time":current_time1,
					'world_boss_remaining_times' : self._max_enter_time-1,
				},
				'reward':
				{
					"world_boss_enter_time": int((d2-d1).total_seconds()),
					'world_boss_remaining_times' : 1
				}
			}
			return self._message_typesetting(status=1, message="enter boss world success, it is first time to enter boss world", data=message_dic)
		else:
			delta_time = datetime.strptime(current_time1, '%Y-%m-%d %H:%M:%S') - datetime.strptime(data[0][0], '%Y-%m-%d %H:%M:%S')
			my_time = int(delta_time.total_seconds()/60/60/24)
			if my_time>=1:
				world_boss_remaining_times = self._max_enter_time
			else:
				world_boss_remaining_times = data[0][1]
			if world_boss_remaining_times-1>=0:
				data = await self._execute_statement_update(world,f'UPDATE player SET world_boss_enter_time ="{current_time1}",world_boss_remaining_times ="{str(int(world_boss_remaining_times)-1)}" WHERE unique_id = "{unique_id}"')
				message_dic={
					'remaining' :
					{
						"world_boss_enter_time":current_time1,
						'world_boss_remaining_times' : world_boss_remaining_times-1,
					},
					'reward':
					{
						"world_boss_enter_time": int((d2-d1).total_seconds()),
						'world_boss_remaining_times' : 1
					}
				}
				return self._message_typesetting(status=0, message="enter bass world success",data = message_dic)
			else:
				return self._message_typesetting(status=99, message="energy is not enough")

	async def _leave_world_boss_stage(self, world: int, unique_id: str, total_damage: int):
		# 0 challenge success
		if total_damage>=self._max_upload_damage:
			return self._message_typesetting(status=99, message="abnormal data")
		else:
			for i in range(0,10):
				if self._boss_life_remaining[i]>0:
					self._boss_life_remaining[i] = self._boss_life_remaining[i]-total_damage
					self._boss_life_remaining[i] = 0 if self._boss_life_remaining[i]<=0 else self._boss_life_remaining[i]
					data = await self._execute_statement(world,f'select * from leader_board where unique_id ="{unique_id}"')
					total_damage = data[0][2] if total_damage>data[0][2] else total_damage
					await self._execute_statement_update(world,f'UPDATE leader_board SET world_boss_damage ="{data[0][2]+total_damage}",once_top_damage ="{total_damage}" WHERE unique_id = "{unique_id}"')
					break
				else:
					self._boss_life_remaining[i] =0
					continue
		message_dic = {
			'remaining' :
			{
			'boss1' : "%.2f" %(self._boss_life_remaining[0]/self._boss_life[0]),
			'boss2' : "%.2f" %(self._boss_life_remaining[1]/self._boss_life[1]),
			'boss3' : "%.2f" %(self._boss_life_remaining[2]/self._boss_life[2]),
			"boss4" : "%.2f" %(self._boss_life_remaining[3]/self._boss_life[3]),
			"boss5" : "%.2f" %(self._boss_life_remaining[4]/self._boss_life[4]),
			'boss6' : "%.2f" %(self._boss_life_remaining[5]/self._boss_life[5]),
			'boss7' : "%.2f" %(self._boss_life_remaining[6]/self._boss_life[6]),
			'boss8' : "%.2f" %(self._boss_life_remaining[7]/self._boss_life[7]),
			"boss9" : "%.2f" %(self._boss_life_remaining[8]/self._boss_life[8]),
			"boss10": "%.2f" %(self._boss_life_remaining[9]/self._boss_life[9])
			}
		}
		return self._message_typesetting(status=0, message="challenge success",data=message_dic)

	async def _check_boss_status(self,world: int,unique_id: str):
		#0 return boss info success
		data = await self._execute_statement(world,f'select world_boss_enter_time,world_boss_remaining_times from player where unique_id ="{unique_id}"')
		if data[0][0]=="":
			current_time1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			data = await self._execute_statement_update(world,f'UPDATE player SET world_boss_enter_time ="{current_time1}",world_boss_remaining_times ="{str(self._max_enter_time)}" WHERE unique_id = "{unique_id}"')
		current_time1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		current_time2 = (datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")
		d1 = datetime.strptime(current_time1, '%Y-%m-%d %H:%M:%S')
		d2 = datetime.strptime(current_time2, '%Y-%m-%d %H:%M:%S')
		message_dic = {
					'remaining' :
					{
						'world_boss_enter_time':current_time1,
						'world_boss_remaining_times':int((d2-d1).total_seconds()),
						'boss1' : "%.2f" %(int(self._boss_life_remaining[0])/int(self._boss_life[0])),
						'boss2' : "%.2f" %(int(self._boss_life_remaining[1])/int(self._boss_life[1])),
						'boss3' : "%.2f" %(int(self._boss_life_remaining[2])/int(self._boss_life[2])),
						"boss4" : "%.2f" %(int(self._boss_life_remaining[3])/int(self._boss_life[3])),
						"boss5" : "%.2f" %(int(self._boss_life_remaining[4])/int(self._boss_life[4])),
						'boss6' : "%.2f" %(int(self._boss_life_remaining[5])/int(self._boss_life[5])),
						'boss7' : "%.2f" %(int(self._boss_life_remaining[6])/int(self._boss_life[6])),
						'boss8' : "%.2f" %(int(self._boss_life_remaining[7])/int(self._boss_life[7])),
						"boss9" : "%.2f" %(int(self._boss_life_remaining[8])/int(self._boss_life[8])),
						"boss10": "%.2f" %(int(self._boss_life_remaining[9])/int(self._boss_life[9]))
					}
				}
		return self._message_typesetting(status=0, message="you get all boss message",data= message_dic)

	async def _active_wishing_pool(self, world: int, unique_id: str, weapon_id: str):
		#0 免费抽获取碎片成功没有暴击
		#1 免费抽2倍暴击抽奖
		#2 免费抽3倍暴击抽奖
		#10 钻石抽获取碎片成功没有暴击
		#11 钻石抽2倍暴击抽奖
		#12 钻石抽3倍暴击抽奖
		#99 时间未到
		basic_segment = self._factory_config["wishing_pool"]["basic_segment"]
		basic_recover_time = self._factory_config["wishing_pool"]["basic_recover_time"]
		basic_diamond = self._factory_config["wishing_pool"]["basic_diamond"]
		return_value = 0
		random_number = random.randint(0, 100)
		if 0<=random_number < 10:
			basic_segment = basic_segment*3
			return_value=2
		elif 10<=random_number < 55:
			basic_segment = basic_segment*2
			return_value=1
		await self._set_segment_by_id(world, unique_id, weapon_id, basic_segment)
		current_time1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		data_json={
				"remaining":
				{
					"weapon_id": weapon_id,
					"weapon_segment": basic_segment,
					"wish_pool_timer": current_time1,
					"diamond":0
				},
				"reward":
				{
					"weapon_id": weapon_id,
					"weapon_segment": basic_segment,
					"wish_pool_timer": 0,
					"diamond":0
				}
			}
		data = await self._execute_statement(world, 'SELECT wishing_pool_level, wishing_pool_timer, wishing_pool_times FROM factory WHERE unique_id = "' + unique_id + '";')
		if data[0][1] =="":
			await self._execute_statement_update(world, f'UPDATE factory SET wishing_pool_timer="{current_time1}" WHERE unique_id = "{unique_id}"')
			data_json["reward"]["wish_pool_timer"] = basic_recover_time*3600-int(data[0][0])*1*3600
			return self._message_typesetting(return_value, 'you get segement',data_json)
		else:
			current_time1 = data[0][1]
			current_time2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			d1 = datetime.strptime(current_time1, '%Y-%m-%d %H:%M:%S')
			d2 = datetime.strptime(current_time2, '%Y-%m-%d %H:%M:%S')
			#print("玩家时间："+current_time1)
			#print("服务器时间:"+current_time2)
			#print("间隔时间:"+str(int((d2-d1).total_seconds())))
			#print("48小时秒钟："+str(basic_recover_time*3600))
			#print("等级减去秒钟："+str(int(data[0][0])*1*3600))
			#print("抽奖CD减时间:"+ str(basic_recover_time*3600-int(data[0][0])*1*3600-((d2-d1).total_seconds())))
			reward_time = basic_recover_time*3600-int(data[0][0])*1*3600-(int((d2-d1).total_seconds()))
			if reward_time<=0:
				await self._execute_statement_update(world, f'UPDATE factory SET wishing_pool_times="{0}" WHERE unique_id = "{unique_id}"')
				data_json["reward"]["wish_pool_timer"] = basic_recover_time*3600-int(data[0][0])*1*3600
			else:
				data_json["reward"]["wish_pool_timer"] = basic_recover_time*3600-int(data[0][0])*1*3600-(int((d2-d1).total_seconds()))
			if int((d2-d1).total_seconds()) <(basic_recover_time- int(data[0][0])*1)*3600:
				return_data = await self.try_diamond(world, unique_id,-data[0][2]*basic_diamond)
				#{"status": status, "remaining": remaining}
				if return_data["status"]==0:
					data_json["remaining"]["diamond"] = return_data["remaining"]
					data_json["reward"]["diamond"] = data[0][2]*basic_diamond
					await self._execute_statement_update(world, f'UPDATE factory SET wishing_pool_times="{data[0][2]+1}" WHERE unique_id = "{unique_id}"')
					return self._message_typesetting(int("1"+str(return_value)), 'you get segement by diamond',data_json)
				else:
					return self._message_typesetting(99, 'insufficient diamond',data_json)
			else:
				await self._execute_statement_update(world, f'UPDATE factory SET wishing_pool_timer="{current_time2}" WHERE unique_id = "{unique_id}"')
			return self._message_typesetting(return_value, 'you get segement',data_json)

	async def _get_top_damage(self, world: int, unique_id: int, range_number: int) -> (int, str):
		# 0 return 10 data successfully
		# 98 range number should over or equal 1
		# 99 no data
		if range_number<=0:
			return self._message_typesetting(status=98, message="range number should over or equal 1")
		data_leader_board = await self._execute_statement(world,f'SELECT * FROM leader_board ORDER BY world_boss_damage DESC LIMIT {10*(range_number-1)},{10}')
		if len(data_leader_board)==0:
			return self._message_typesetting(status=99, message="no data")
		data_users = await self._execute_statement(world,f'SELECT game_name FROM player where unique_id in {data_leader_board[0][0],data_leader_board[1][0],data_leader_board[2][0],data_leader_board[3][0],data_leader_board[4][0],data_leader_board[5][0],data_leader_board[6][0],data_leader_board[7][0],data_leader_board[8][0],data_leader_board[9][0]} ORDER BY FIELD(unique_id,{data_leader_board[0][0]},{data_leader_board[1][0]},{data_leader_board[2][0]},{data_leader_board[3][0]},{data_leader_board[4][0]},{data_leader_board[5][0]},{data_leader_board[6][0]},{data_leader_board[7][0]},{data_leader_board[8][0]},{data_leader_board[9][0]})')
		message_dic={"remaining":{}, "page" : range_number}
		for index in range(0,len(data_users)):
			message_dic["remaining"].update({index:{data_users[index][0]:data_leader_board[index][2]}})
		return self._message_typesetting(status=0, message="get top "+str(range_number*10)+" damage",data= message_dic)

	async def _get_energy_information(self, world: int, unique_id: str) -> (int, str):
		data = await self._execute_statement(world, f"SELECT energy, recover_time FROM player WHERE unique_id='{unique_id}';")
		return int(data[0][0]), data[0][1]

	async def _set_weapon_star(self, world: int, unique_id: str, weapon: str, star: int):
		return await self._execute_statement_update(world, 'UPDATE weapon SET weapon_star = "' + str(star) + '" WHERE unique_id = "' + unique_id + '" AND weapon_name = "' + weapon + '";') 

	async def _get_segment(self, world: int, unique_id: str, weapon: str) -> int:
		data = await self._execute_statement(world, 'SELECT segment FROM weapon WHERE unique_id = "' + unique_id + '" AND weapon_name = "' + weapon + '";')
		return int(data[0][0])

	async def _set_segment_by_id(self, world: int, unique_id: str, weapon: str, segment: int):
		return await self._execute_statement_update(world, 'UPDATE `weapon' + '` SET segment = "' + str(segment) + '" WHERE unique_id = "' + unique_id  + '" and weapon_name="'+weapon+'";')

	async def _get_weapon_star(self, world: int, unique_id: str, weapon: str) -> int:
		data = await self._execute_statement(world, 'SELECT weapon_star FROM weapon WHERE unique_id = "' + unique_id + '" AND weapon_name = "' + weapon + '";')
		return int(data[0][0])

	async def _get_row_by_id(self, world: int, weapon: str, unique_id: str) -> list:
		try:
			return list((await self._execute_statement(world, f'SELECT * FROM weapon WHERE unique_id = "{unique_id}" AND weapon_name = "{weapon}"'))[0])
		except:
			await self._execute_statement(world, f'INSERT INTO weapon (unique_id, weapon_name) VALUES ("{unique_id}", "{weapon}")')
			return list((await self._execute_statement(world, f'SELECT * FROM weapon WHERE unique_id = "{unique_id}" AND weapon_name = "{weapon}"'))[0])

	async def _get_role_row_by_id(self, world: int, role: str, unique_id: str) -> list:
		try:
			return list((await self._execute_statement(world, f'SELECT * FROM role WHERE unique_id = "{unique_id}" AND role_name = "{role}"'))[0])
		except:
			await self._execute_statement(world, f'INSERT INTO role (unique_id, role_name) VALUES ("{unique_id}", "{role}")')
			return list((await self._execute_statement(world, f'SELECT * FROM role WHERE unique_id = "{unique_id}" AND role_name = "{role}"'))[0])

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
		return await self._execute_statement_update(world, f"UPDATE player SET {material}={value} where unique_id='{unique_id}'")

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

	def firstDayOfMonth(self, dt):
		return (dt + timedelta(days= -dt.day + 1)).replace(hour=0, minute=0, second=0, microsecond=0)

	def _refresh_configuration(self):
		r = requests.get('http://localhost:8000/get_game_manager_config')
		d = r.json()
		self._mall_config = d['mall']
		self._factory_config = d['factory']
		self._stage_reward = d['reward']
		self._skill_scroll_functions = d['skill']['skill_scroll_functions']
		self._upgrade_chance = d['skill']['upgrade_chance']
		self._weapon_config = d['weapon']
		self._role_config = d['role']
		self._lottery = d['lottery']
		self._player = d['player']
		self._hang_reward = d['hang_reward']
		self._entry_consumables = d['entry_consumables']
		if self.firstDayOfMonth(datetime.today()).day == datetime.today().day and self.is_first_month==False:
			print("firstDayOfMonth")
			self._is_first_start = True
			self.is_first_month=True
		if self.firstDayOfMonth(datetime.today()).day != datetime.today().day and self.is_first_month==True:
			self.is_first_month=False
		if self._is_first_start:
			print("refresh")
			self._boss_life=[]
			self._boss_life_remaining=[]
			self._is_first_start = False
			self._world_boss = d['world_boss']
			self._max_enter_time = self._world_boss['max_enter_time']
			self._max_upload_damage = self._world_boss['max_upload_damage']
			for i in range(0,10):
				self._boss_life_remaining.append(self._world_boss["boss"+str(i+1)]["life_value"])
				self._boss_life.append(self._world_boss["boss"+str(i+1)]["life_value"])

		result = requests.get('http://localhost:8000/get_stage_reward_config')
		self._get_stage_reward_config_json = result.json()
		result = requests.get('http://localhost:8000/get_monster_config')
		self._monster_config_json = result.json()
		result = requests.get('http://localhost:8000/get_level_enemy_layouts_config')
		self._level_enemy_layouts_config_json = result.json()
	
	def _initialize_pools(self, worlds):
		self._pools = {}
		if len(worlds) == 0:
			self._pools[0] = tormysql.ConnectionPool(max_connections = 10, host = '192.168.1.102', user = 'root', passwd = 'lukseun', db = 'aliya', charset = 'utf8')
		else:
			for world in worlds:
				if world == 0:
					self._pools[0] = tormysql.ConnectionPool(max_connections = 10, host = '192.168.1.102', user = 'root', passwd = 'lukseun', db = 'aliya', charset = 'utf8')
				else:
					self._pools[world] = tormysql.ConnectionPool(max_connections = 10, host = '192.168.1.102', user = 'root', passwd = 'lukseun', db = f'world{world}', charset = 'utf8')

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


# SERVER PRIVATE
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

@ROUTES.post('/get_skill_level_up_config')
async def _get_skill_level_up_config(request: web.Request) -> web.Response:
	post = await request.post()
	result = (request.app['MANAGER']).get_skill_level_up_config()
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

@ROUTES.post('/disintegrate_weapon')
async def __disintegrate_weapon(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).disintegrate_weapon(int(post['world']), post['unique_id'], post['weapon'])
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

@ROUTES.post('/enter_tower')
async def __enter_tower(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).enter_tower(int(post['world']), post['unique_id'], int(post['stage']))
	return _json_response(result)

@ROUTES.post('/pass_tower')
async def __pass_tower(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).pass_tower(int(post['world']), post['unique_id'], int(post['stage']), post['clear_time'])
	return _json_response(result)

@ROUTES.post('/get_all_stage_info')
async def __get_all_stage_info(request: web.Request) -> web.Response:
	result = await (request.app['MANAGER']).get_all_stage_info()
	return _json_response(result)

######################################################
####################    role      ####################
######################################################

@ROUTES.post('/upgrade_role_level')
async def _upgrade_role_level(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).upgrade_role_level(int(post['world']), post['unique_id'], post['role'], int(post['experience_potion']))
	return _json_response(result)

@ROUTES.post('/upgrade_role_star')
async def _upgrade_role_star(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).upgrade_role_star(int(post['world']), post['unique_id'], post['role'])
	return _json_response(result)

@ROUTES.post('/get_all_roles')
async def _get_all_roles(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).get_all_roles(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/get_role_config')
async def _get_role_config(request: web.Request) -> web.Response:
	post = await request.post()
	result = (request.app['MANAGER']).get_role_config()
	return _json_response(result)

# ############################################################ #
# ######                  summon weapons                ###### #
# ############################################################ #
@ROUTES.post('/basic_summon')
async def __basic_summon(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).basic_summon(int(post['world']), post['unique_id'], post['cost_item'], "weapons")
	return _json_response(result)


@ROUTES.post('/pro_summon')
async def __pro_summon(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).pro_summon(int(post['world']), post['unique_id'], post['cost_item'], "weapons")
	return _json_response(result)


@ROUTES.post('/friend_summon')
async def __friend_summon(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).friend_summon(int(post['world']), post['unique_id'], post['cost_item'], "weapons")
	return _json_response(result)


#  weapons 10_times
@ROUTES.post('/basic_summon_10_times')
async def __basic_summon_10_times(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).basic_summon_10_times(int(post['world']), post['unique_id'], post['cost_item'], "weapons")
	return _json_response(result)


@ROUTES.post('/pro_summon_10_times')
async def __pro_summon_10_times(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).pro_summon_10_times(int(post['world']), post['unique_id'], post['cost_item'], "weapons")
	return _json_response(result)


@ROUTES.post('/friend_summon_10_times')
async def __friend_summon_10_times(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).friend_summon_10_times(int(post['world']), post['unique_id'], post['cost_item'], "weapons")
	return _json_response(result)


@ROUTES.post('/prophet_summon_10_times')
async def __prophet_summon_10_times(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).prophet_summon_10_times(int(post['world']), post['unique_id'], post['cost_item'], "weapons")
	return _json_response(result)


# ############################################################ #
# ######                  summon skills                 ###### #
# ############################################################ #
@ROUTES.post('/basic_summon_skill')
async def __basic_summon_skill(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).basic_summon(int(post['world']), post['unique_id'], post['cost_item'], "skills")
	return _json_response(result)


@ROUTES.post('/pro_summon_skill')
async def __pro_summon_skill(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).pro_summon(int(post['world']), post['unique_id'], post['cost_item'], "skills")
	return _json_response(result)


@ROUTES.post('/friend_summon_skill')
async def __friend_summon_skill(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).friend_summon(int(post['world']), post['unique_id'], post['cost_item'], "skills")
	return _json_response(result)


#  skills 10_times
@ROUTES.post('/basic_summon_skill_10_times')
async def __basic_summon_skill_10_times(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).basic_summon_10_times(int(post['world']), post['unique_id'], post['cost_item'], "skills")
	return _json_response(result)


@ROUTES.post('/pro_summon_skill_10_times')
async def __pro_summon_skill_10_times(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).pro_summon_10_times(int(post['world']), post['unique_id'], post['cost_item'], "skills")
	return _json_response(result)


@ROUTES.post('/friend_summon_skill_10_times')
async def __friend_summon_skill_10_times(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).friend_summon_10_times(int(post['world']), post['unique_id'], post['cost_item'], "skills")
	return _json_response(result)


# ############################################################ #
# ######                  summon roles                  ###### #
# ############################################################ #
@ROUTES.post('/basic_summon_roles')
async def __basic_summon(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).basic_summon(int(post['world']), post['unique_id'], post['cost_item'], "roles")
	return _json_response(result)


@ROUTES.post('/pro_summon_roles')
async def __pro_summon(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).pro_summon(int(post['world']), post['unique_id'], post['cost_item'], "roles")
	return _json_response(result)


@ROUTES.post('/friend_summon_roles')
async def __friend_summon(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).friend_summon(int(post['world']), post['unique_id'], post['cost_item'], "roles")
	return _json_response(result)


#  roles 10_times
@ROUTES.post('/basic_summon_roles_10_times')
async def __basic_summon_roles_10_times(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).basic_summon_10_times(int(post['world']), post['unique_id'], post['cost_item'], "roles")
	return _json_response(result)


@ROUTES.post('/pro_summon_roles_10_times')
async def __pro_summon_roles_10_times(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).pro_summon_10_times(int(post['world']), post['unique_id'], post['cost_item'], "roles")
	return _json_response(result)


@ROUTES.post('/friend_summon_roles_10_times')
async def __friend_summon_roles_10_times(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).friend_summon_10_times(int(post['world']), post['unique_id'], post['cost_item'], "roles")
	return _json_response(result)

# #####################################################
# #####################################################
# #####################################################

@ROUTES.post('/fortune_wheel_basic')
async def __fortune_wheel_basic(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).fortune_wheel_basic(int(post['world']), post['unique_id'], post['cost_item'])
	return _json_response(result)

@ROUTES.post('/fortune_wheel_pro')
async def __fortune_wheel_pro(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).fortune_wheel_pro(int(post['world']), post['unique_id'], post['cost_item'])
	return _json_response(result)

@ROUTES.post('/automatically_refresh_store')
async def __automatically_refresh_store(request: web.Request) -> web.Response:
	post = await request.post()
	data = await (request.app['MANAGER']).automatically_refresh_store(int(post['world']), post['unique_id'])
	return _json_response(data)

@ROUTES.post('/manually_refresh_store')
async def __manually_refresh_store(request: web.Request) -> web.Response:
	post = await request.post()
	data = await (request.app['MANAGER']).manually_refresh_store(int(post['world']), post['unique_id'])
	return _json_response(data)

@ROUTES.post('/diamond_refresh_store')
async def __diamond_refresh_store(request: web.Request) -> web.Response:
	post = await request.post()
	data = await (request.app['MANAGER']).diamond_refresh_store(int(post['world']), post['unique_id'])
	return _json_response(data)

@ROUTES.post('/black_market_transaction')
async def __black_market_transaction(request: web.Request) -> web.Response:
	post = await request.post()
	data = await (request.app['MANAGER']).black_market_transaction(int(post['world']), post['unique_id'], int(post['code']))
	return _json_response(data)

@ROUTES.post('/send_friend_gift')
async def _send_friend_gift(request: web.Request) -> web.Response:
	post = await request.post()
	data = await (request.app['MANAGER']).send_friend_gift(int(post['world']), post['unique_id'], post['friend_name'])
	return _json_response(data)

@ROUTES.post('/send_all_friend_gift')
async def _send_all_friend_gift(request: web.Request) -> web.Response:
	post = await request.post()
	data = await (request.app['MANAGER']).send_all_friend_gift(int(post['world']), post['unique_id'])
	return _json_response(data)

@ROUTES.post('/get_all_friend_info')
async def _get_all_friend_info(request: web.Request) -> web.Response:
	post = await request.post()
	data = await (request.app['MANAGER']).get_all_friend_info(int(post['world']), post['unique_id'])
	return _json_response(data)

@ROUTES.post('/delete_friend')
async def _delete_friend(request: web.Request) -> web.Response:
	post = await request.post()
	data = await (request.app['MANAGER']).delete_friend(int(post['world']), post['unique_id'], post['friend_name'])
	return _json_response(data)


@ROUTES.post('/request_friend')
async def _request_friend(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).request_friend(int(post['world']), post['unique_id'], post['friend_name'])
	return _json_response(result)


@ROUTES.post('/response_friend')
async def _response_friend(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).response_friend(int(post['world']), post['unique_id'], post['nonce'])
	return _json_response(result)


@ROUTES.post('/get_new_mail')
async def _get_new_mail(request: web.Request) -> web.Response:
	return _json_response(json.loads(requests.post('http://localhost:8020/get_new_mail', data=await request.post()).text))


@ROUTES.post('/get_all_mail')
async def _get_all_mail(request: web.Request) -> web.Response:
	return _json_response(json.loads(requests.post('http://localhost:8020/get_all_mail', data=await request.post()).text))


@ROUTES.post('/delete_mail')
async def _delete_mail(request: web.Request) -> web.Response:
	return _json_response(json.loads(requests.post('http://localhost:8020/delete_mail', data=await request.post()).text))


@ROUTES.post('/delete_all_mail')
async def _delete_all_mail(request: web.Request) -> web.Response:
	return _json_response(json.loads(requests.post('http://localhost:8020/delete_all_mail', data=await request.post()).text))


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

@ROUTES.post('/get_hang_up_info')
async def __get_hang_up_info(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).get_hang_up_info(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/get_monster_info')
async def _get_monster_info(request: web.Request) -> web.Response:
	result = (request.app['MANAGER']).get_monster_info()
	return _json_response(result)

@ROUTES.post('/get_stage_info')
async def _get_stage_info(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).get_stage_info(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/enter_stage')
async def __enter_stage(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).enter_stage(int(post['world']), post['unique_id'], int(post['stage']))
	return _json_response(result)

@ROUTES.post('/show_energy')
async def __show_energy(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).show_energy(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/upgrade_armor')
async def __upgrade_armor(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).upgrade_armor(int(post['world']), post['unique_id'], post["armor_id"], int(post['level']))
	return _json_response(result)

@ROUTES.post('/get_all_armor_info')
async def __get_all_armor_info(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).get_all_armor_info(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/redeem_nonce')
async def _redeem_nonce(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).redeem_nonce(int(post['world']), post['unique_id'], post['nonce'])
	return _json_response(result)

@ROUTES.post('/redeem_all_nonce')
async def _redeem_nonce(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).redeem_all_nonce(int(post['world']), post['unique_id'], post.getall('type_list'), post.getall('nonce_list'))
	return _json_response(result)

#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
@ROUTES.post('/leave_family')
async def _leave_family(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(await (request.app['MANAGER']).leave_family(int(post['world']), post['unique_id']))

@ROUTES.post('/create_family')
async def _create_family(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(await (request.app['MANAGER']).create_family(int(post['world']), post['unique_id'], post['fname']))

@ROUTES.post('/request_join_family')
async def _request_join_family(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(await (request.app['MANAGER']).request_join_family(int(post['world']), post['unique_id'], post['fname']))

@ROUTES.post('/invite_user_family')
async def _invite_user_family(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(await (request.app['MANAGER']).invite_user_family(int(post['world']), post['unique_id'], post['target']))

@ROUTES.post('/remove_user_family')
async def _remove_user_family(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(await (request.app['MANAGER']).remove_user_family(int(post['world']), post['unique_id'], post['user']))

@ROUTES.post('/respond_family')
async def _respond_family(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(await (request.app['MANAGER']).respond_family(int(post['world']), post['unique_id'], post['nonce']))
#  ################################################################################
#  ########################## start mall  #########################################
#  ################################################################################

@ROUTES.post('/purchase_scroll_mall')
async def _purchase_scroll_mall(request: web.Request) -> web.Response:
	post = await request.post()
	return _json_response(await (request.app['MANAGER']).purchase_scroll_mall(int(post['world']), post['unique_id'], post['scroll_type'], post["purchase_type"], int(post['quantity'])))

#  ################################################################################
#  ##########################   end mall  #########################################
#  ################################################################################
@ROUTES.post('/get_lottery_config_info')
async def _get_lottery_config_info(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).get_lottery_config_info(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/get_stage_reward_config')
async def _get_stage_reward_config(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).get_stage_reward_config(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/monster_config')
async def _monster_config(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).monster_config(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/level_enemy_layouts_config')
async def _level_enemy_layouts_config(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).level_enemy_layouts_config(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/check_boss_status')
async def _check_boss_status(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER'])._check_boss_status(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/enter_world_boss_stage')
async def _enter_world_boss_stage(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER'])._enter_world_boss_stage(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/leave_world_boss_stage')
async def _leave_world_boss_stage(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER'])._leave_world_boss_stage(int(post['world']), post['unique_id'],int(post['total_damage']))
	return _json_response(result)

@ROUTES.post('/get_top_damage')
async def _get_top_damage(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER'])._get_top_damage(int(post['world']), post['unique_id'],int(post['range_number']))
	return _json_response(result)

@ROUTES.post('/active_wishing_pool')
async def _active_wishing_pool(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER'])._active_wishing_pool(int(post['world']), post['unique_id'], post['weapon_id'])
	return _json_response(result)

@ROUTES.post('/refresh_all_storage')
async def _refresh_all_storage(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).refresh_all_storage(int(post['world']), post['unique_id'])
	return _json_response(result)


@ROUTES.post('/refresh_food_storage')
async def _refresh_food_storage(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).refresh_food_storage(int(post['world']), post['unique_id'])
	return _json_response(result)


@ROUTES.post('/refresh_mine_storage')
async def _refresh_mine_storage(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).refresh_mine_storage(int(post['world']), post['unique_id'])
	return _json_response(result)


@ROUTES.post('/refresh_crystal_storage')
async def _refresh_crystal_storage(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).refresh_crystal_storage(int(post['world']), post['unique_id'])
	return _json_response(result)


@ROUTES.post('/refresh_equipment_storage')
async def _refresh_equipment_storage(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).refresh_equipment_storage(int(post['world']), post['unique_id'])
	return _json_response(result)


@ROUTES.post('/distribution_workers')
async def _distribution_workers(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).distribution_workers(int(post['world']), post['unique_id'], int(post['workers_quantity']), post['factory_kind'])
	return _json_response(result)


@ROUTES.post('/equipment_manufacturing_armor')
async def _equipment_manufacturing_armor(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).equipment_manufacturing_armor(int(post['world']), post['unique_id'], post['armor_kind'])
	return _json_response(result)


@ROUTES.post('/buy_workers')
async def _buy_workers(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).buy_workers(int(post['world']), post['unique_id'], int(post['workers_quantity']))
	return _json_response(result)


@ROUTES.post('/upgrade_food_factory')
async def _upgrade_food_factory(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).upgrade_food_factory(int(post['world']), post['unique_id'])
	return _json_response(result)


@ROUTES.post('/upgrade_mine_factory')
async def _upgrade_mine_factory(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).upgrade_mine_factory(int(post['world']), post['unique_id'])
	return _json_response(result)


@ROUTES.post('/upgrade_crystal_factory')
async def _upgrade_crystal_factory(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).upgrade_crystal_factory(int(post['world']), post['unique_id'])
	return _json_response(result)


@ROUTES.post('/upgrade_wishing_pool')
async def _upgrade_wishing_pool(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).upgrade_wishing_pool(int(post['world']), post['unique_id'])
	return _json_response(result)


@ROUTES.post('/acceleration_technology')
async def _acceleration_technology(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).acceleration_technology(int(post['world']), post['unique_id'])
	return _json_response(result)


@ROUTES.post('/get_factory_info')
async def _get_factory_info(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).get_factory_info(int(post['world']), post['unique_id'])
	return _json_response(result)


@ROUTES.post('/get_account_world_info')
async def _get_account_world_info(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).get_account_world_info(post['unique_id'])
	return _json_response(result)


@ROUTES.post('/choice_world')
async def _choice_world(request: web.Request) -> web.Response:
	post = await request.post()
	print(str(post))
	result = await (request.app['MANAGER']).choice_world(post['unique_id'], int(post['target_world']))
	return _json_response(result)


@ROUTES.post('/create_player')
async def _create_player(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).create_player(int(post['world']), post['unique_id'], post['game_name'])
	return _json_response(result)


def get_config() -> configparser.ConfigParser:
	'''
	Fetches the server's configuration file from the config server.
	Waits until the configuration server is online.
	'''
	while True:
		try:
			r = requests.get('http://localhost:8000/register_game_manager')
			return r.json()
		except requests.exceptions.ConnectionError:
			print('Could not find configuration server, retrying in 5 seconds...')
			time.sleep(5)


def run():
	app = web.Application()
	app.add_routes(ROUTES)
	config = get_config()
	app['MANAGER'] = GameManager(config['worlds'])
	print(f'starting game manager for worlds {config["worlds"]} on port {config["port"]}...')
	web.run_app(app, port=config['port'])


if __name__ == '__main__':
	run()
