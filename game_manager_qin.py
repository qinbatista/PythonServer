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


	async def try_all_material(self, world: int, unique_id: str, stage: int) -> dict:
		sql_stage = await self._get_material(world, unique_id, "stage")
		if stage <= 0 or sql_stage + 1 < stage:
			return self._internal_format(status=9, remaining=0)  # abnormal data!
		material_dict = dict(self._reward[stage])
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

	async def try_fortune_wheel_ticket_basic(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'fortune_wheel_ticket_basic', value)

	async def try_fortune_wheel_ticket_pro(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'fortune_wheel_ticket_pro', value)

	async def try_basic_summon_scroll(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'basic_summon_scroll', value)

	async def try_pro_summon_scroll(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'pro_summon_scroll', value)

	async def try_friend_gift(self, world: int, unique_id: str, value: int) -> dict:
		return await self._try_material(world, unique_id, 'friend_gift', value)
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
				return self._message_typesetting(1, 'Weapon already unlocked, got free segment!', {"keys": ['weapon','star','segment'], "values": [weapon,star,segment]})
			await self._set_weapon_star(world, unique_id, weapon, 1)
			return self._message_typesetting(0, 'Unlocked new weapon!', {"keys": ["weapon","star","segment"], "values": [weapon,1,0]})
		except:
			return self._message_typesetting(2, 'no weapon!')

	async def try_unlock_role(self, world: int, unique_id: str, role: str) -> dict:
		# - 0 - Unlocked new role!   ===> {"keys": ["role"], "values": [role]}
		# - 1 - role already unlocked, got free segment   ===>  {"keys": ['role', 'segment'], "values": [role, segment]}
		# - 2 - no role!
		# try:
		star = await self._get_role_star(world, unique_id, role)
		if star != 0:
			segment = await self._get_role_segment(world, unique_id, role) + 30
			await self._set_role_segment_by_id(world, unique_id, role, segment)
			return self._message_typesetting(1, 'role already unlocked, got free segment!', {"keys": ['role','star','segment'], "values": [role,star,segment]})
		await self._set_role_star(world, unique_id, role, 1)
		return self._message_typesetting(0, 'Unlocked new role!', {"keys": ["role","star","segment"], "values": [role,1,0]})
		# except:
		# 	return self._message_typesetting(2, 'no role!')




#############################################################################
#						End Stage Module Functions							#
#############################################################################




#############################################################################
#						Lottery Module Functions							#
#############################################################################

#qin
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

#qin
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
		# - 0 - Unlocked new role!   ===> {"keys": ["weapon"], "values": [weapon]}
		# - 1 - role already unlocked, got free segment   ===>  {"keys": ['weapon', 'segment'], "values": [weapon, segment]}
		# - 2 - no weapon!
		tier_choice = (random.choices(self._lottery['roles']['names'], self._lottery['roles']['weights'][kind]))[0]
		gift_role = (random.choices(self._lottery['roles']['items'][tier_choice]))[0]
		return await self.try_unlock_role(world, unique_id, gift_role)

	async def basic_summon(self, world: int, unique_id: str, cost_item: str, summon_kind:str) -> dict:
		# 0 - unlocked new skill or weapon
		# 1 - you received free scroll or segments
		# 2 - invalid skill name
		# 3 - database operation error
		# 4 - insufficient material
		# 5 - cost_item error
		return await self._default_summon(world, unique_id, cost_item, 'basic',summon_kind)

	async def pro_summon(self, world: int, unique_id: str, cost_item: str,summon_kind:str) -> dict:
		# 0 - unlocked new skill or weapon
		# 1 - you received free scroll or segments
		# 2 - invalid skill name
		# 3 - database operation error
		# 4 - insufficient material
		# 5 - cost_item error
		return await self._default_summon(world, unique_id, cost_item, 'pro',summon_kind)

	async def friend_summon(self, world: int, unique_id: str, cost_item: str,summon_kind:str) -> dict:
		# 0 - unlocked new skill or weapon
		# 1 - you received free scroll or segments
		# 2 - invalid skill name
		# 3 - database operation error
		# 4 - insufficient material
		# 5 - cost_item error
		return await self._default_summon(world, unique_id, cost_item, 'friend_gitf',summon_kind)

	async def prophet_summon(self, world: int, unique_id: str, cost_item: str,summon_kind:str) -> dict:
		# 0 - unlocked new skill or weapon
		# 1 - you received free scroll or segments
		# 2 - invalid skill name
		# 3 - database operation error
		# 4 - insufficient material
		# 5 - cost_item error
		return await self._default_summon(world, unique_id, cost_item, 'prophet',summon_kind)

	async def basic_summon_10_times(self, world: int, unique_id: str, cost_item: str, summon_kind:str) -> dict:
		# 0 - unlocked new skill or weapon
		# 1 - you received free scroll or segments
		# 2 - invalid skill name
		# 3 - database operation error
		# 4 - insufficient material
		# 5 - cost_item error
		result_list = []
		for _ in range(0,10):
			message_list=await self._default_summon(world, unique_id, cost_item, 'basic',summon_kind)
			result_list.append(message_list['data'])
		return self._message_typesetting(2, '10 times basic_summon',result_list)

	async def pro_summon_10_times(self, world: int, unique_id: str, cost_item: str,summon_kind:str) -> dict:
		# 0 - unlocked new skill or weapon
		# 1 - you received free scroll or segments
		# 2 - invalid skill name
		# 3 - database operation error
		# 4 - insufficient material
		# 5 - cost_item error
		result_list = []
		for _ in range(0,10):
			message_list=await self._default_summon(world, unique_id, cost_item, 'pro',summon_kind)
			result_list.append(message_list['data'])
		return self._message_typesetting(2, '10 times pro_summon',result_list)

	async def friend_summon_10_times(self, world: int, unique_id: str, cost_item: str,summon_kind:str) -> dict:
		# 0 - unlocked new skill or weapon
		# 1 - you received free scroll or segments
		# 2 - invalid skill name
		# 3 - database operation error
		# 4 - insufficient material
		# 5 - cost_item error
		result_list = []
		for _ in range(0,10):
			message_list=await self._default_summon(world, unique_id, cost_item, 'pro',summon_kind)
			result_list.append(message_list['data'])
		return self._message_typesetting(2, '10 times pro_summon',result_list)

	async def prophet_summon_10_times(self, world: int, unique_id: str, cost_item: str,summon_kind:str) -> dict:
		# 0 - unlocked new skill or weapon
		# 1 - you received free scroll or segments
		# 2 - invalid skill name
		# 3 - database operation error
		# 4 - insufficient material
		# 5 - cost_item error
		result_list = []
		for _ in range(0,10):
			message_list=await self._default_summon(world, unique_id, cost_item, 'prophet',summon_kind)
			result_list.append(message_list['data'])
		return self._message_typesetting(2, '10 times pro_summon',result_list)

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
#qin modify new callback message keyward
	async def _default_fortune_wheel(self, world: int, uid: str, cost_item: str, tier: str):
		# 0 - get energy success
		# 1 - get weapon item success
		# 2 - get skill item success
		# 3 - get resource success
		# 96 - item name error
		# 97 - database opeartion error
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
			result = await self.try_basic_summon_scroll(world, uid, -1 * int(self._lottery['fortune_wheel']['cost'][cost_item]))
		elif cost_item == 'pro_summon_scroll':
			result = await self.try_pro_summon_scroll(world, uid, -1 * int(self._lottery['fortune_wheel']['cost'][cost_item]))
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
		elif random_item == 'iron':
			try_result = await self.try_iron(world, uid, int(self._lottery['fortune_wheel']['reward'][tier][random_item]))
		elif random_item == 'skill_scroll_10':
			try_result = await self.try_skill_scroll_10(world, uid, int(self._lottery['fortune_wheel']['reward'][tier][random_item]))
		elif random_item == 'skill_scroll_30':
			try_result = await self.try_skill_scroll_30(world, uid, int(self._lottery['fortune_wheel']['reward'][tier][random_item]))
		elif random_item == 'skill_scroll_100':
			try_result = await self.try_skill_scroll_100(world, uid, int(self._lottery['fortune_wheel']['reward'][tier][random_item]))
		elif random_item == 'weapon':
			try_result = await self.random_gift_segment(world, uid, tier)
			if try_result["status"]==0  or try_result["status"]==1:
				message_dic={
					"remaining":
					{
						"weapon":try_result['data']["values"][0],
						"star":try_result['data']["values"][1],
						"segment":try_result['data']["values"][2]
					},
					"reward":
					{
						"weapon":try_result['data']["values"][0],
						"segment":self._standard_segment_count
					}
				}
				return self._message_typesetting(1, 'get weapon item success', message_dic)
			else:
				return self._message_typesetting(97, 'database opeartion error')
		elif random_item == 'skill':
			try_result = await self.random_gift_skill(world, uid, tier)
			if try_result["status"]==0 or try_result["status"]==1:
				if try_result["status"]==0:
					message_dic={
						"remaining":
						{
							"skill_id":try_result['data']["keys"][0],
							"skill_level":try_result['data']["values"][0]
						},
						"reward":
						{
							"skill_id":try_result['data']["keys"][0],
							"skill_level":try_result['data']["values"][0]
						}
					}
				else:
					message_dic={
						"remaining":
						{
							"scroll_id":try_result['data']["keys"][0],
							"scroll_quantity":try_result['data']["values"][0]
						},
						"reward":
						{
							"scroll_id":try_result['data']["values"][0],
							"scroll_quantity":1
						}
					}
				return self._message_typesetting(2, 'get skill item success', message_dic)
			else:
				return self._message_typesetting(97, 'database opeartion error')
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






#qin modify callback message
	async def _default_summon(self, world: int, unique_id: str, cost_item: str, tier: str, summon_item:str)->str:
		if cost_item == 'diamond':
			result = await self.try_diamond(world, unique_id, -1 * int(self._lottery[summon_item]['cost']['diamond']))
		elif cost_item == 'coin':
			result = await self.try_coin(world, unique_id, -1 * int(self._lottery[summon_item]['cost']['diamond']))
		elif cost_item == 'basic_summon_scroll':
			result = await self.try_basic_summon_scroll(world, unique_id, -1 * int(self._lottery[summon_item]['cost']['basic_summon_scroll']))
		elif cost_item == 'pro_summon_scroll':
			result = await self.try_pro_summon_scroll(world, unique_id, -1 * int(self._lottery[summon_item]['cost']['pro_summon_scroll']))
		elif cost_item == 'friend_gift':
			result = await self.try_friend_gift(world, unique_id, -1 * int(self._lottery[summon_item]['cost']['friend_gift']))
		else:
			return self._message_typesetting(4, 'wrong item name')
		if result["remaining"]<0:
			return self._message_typesetting(97, 'insufficient materials')
		# print("result="+str(result)+" cost_item = "+cost_item+ " coin="+(self._lottery[summon_item]['cost']['diamond']))
		if summon_item == 'skills':
			try_result = await self.random_gift_skill(world, unique_id, tier)
			if try_result["status"]==0 or try_result["status"]==1:
				if try_result["status"]==0:
					message_dic={
						"remaining":
						{
							"skill_id":try_result['data']["keys"][0],
							"skill_level":try_result['data']["values"][0]
						},
						"reward":
						{
							"skill_id":try_result['data']["keys"][0],
							"skill_level":try_result['data']["values"][0]
						}
					}
				else:
					message_dic={
						"remaining":
						{
							"scroll_id":try_result['data']["keys"][0],
							"scroll_quantity":try_result['data']["values"][0]+1
						},
						"reward":
						{
							"scroll_id":try_result['data']["keys"][0],
							"scroll_quantity":1
						}
					}
				return self._message_typesetting(2, 'get skill item success', message_dic)
			else:
				return self._message_typesetting(97, 'skill opeartion error')
		elif summon_item == 'weapons':
			try_result = await self.random_gift_segment(world, unique_id, tier)
			if try_result["status"]==0  or try_result["status"]==1:
				message_dic={
					"remaining":
					{
						"weapon":try_result['data']["values"][0],
						"star":try_result['data']["values"][1],
						"segment":try_result['data']["values"][2]+self._standard_segment_count
					},
					"reward":
					{
						"weapon":try_result['data']["values"][0],
						"segment":self._standard_segment_count
					}
				}
				if try_result["status"]==0:
					return self._message_typesetting(0, 'get weapon success', message_dic)
				else:
					return self._message_typesetting(1, 'get weapon segment success', message_dic)
			else:
				return self._message_typesetting(96, 'weapons opeartion error')
		elif summon_item == 'roles':
			try_result = await self.random_gift_role(world, unique_id, tier)
			if try_result["status"]==0  or try_result["status"]==1:
				message_dic={
					"remaining":
					{
						"role":try_result['data']["values"][0],
						"star":try_result['data']["values"][1],
						"segment":try_result['data']["values"][2]+self._standard_segment_count
					},
					"reward":
					{
						"role":try_result['data']["values"][0],
						"segment":self._standard_segment_count
					}
				}
				return self._message_typesetting(1, 'get role item success', message_dic)
			else:
				return self._message_typesetting(97, 'opeartion error')
	async def _send_friend_gift(self, world: int, unique_id: str, friend_id: str)->str:
		# 0 - send friend gift success because of f_recovering_time is empty
		# 1 - send friend gift success because time is over 1 day
		# 99 - send friend gift failed, because not cooldown time is not finished
		#return value
		# {
		# 	 {"f_id": "5", "f_name": "\u4faf\u5c27", "f_level": 0}
		# }
		# f_id friend id
		# f_name friend name
		# f_level friend level
		data = await self._execute_statement(world, 'SELECT * FROM friend_list WHERE unique_id = "' + unique_id + '";')
		mylist = list(data[0])
		my_friend_id_index =  mylist.index(friend_id)
		f_id = mylist[(my_friend_id_index-1)*4+1]
		f_recovering_time = mylist[(my_friend_id_index-1)*4+4]
		sql_result = await self._execute_statement(world, 'SELECT game_name,level FROM player WHERE unique_id = "' + unique_id + '";')
		f_game_name = sql_result[0][0]
		f_level = sql_result[0][1]
		if f_recovering_time=="":
			current_time = time.strftime('%Y-%m-%d', time.localtime())
			data = await self._execute_statement_update(world, 'UPDATE friend_list SET recovery_time' + str(my_friend_id_index) + ' = "' + current_time + '" WHERE unique_id = "' + unique_id + '";')
			data={
				"remaining" :
				{
				"f_id":f_id,
				"f_name":f_game_name,
				"f_level":f_level,
				"current_time":current_time
				}
			}
			return self._message_typesetting(0, 'send friend gift success because of f_recovering_time is empty',data)
		else:
			current_time = time.strftime('%Y-%m-%d', time.localtime())
			delta_time = datetime.strptime(current_time, '%Y-%m-%d') - datetime.strptime(f_recovering_time, '%Y-%m-%d')
			if delta_time.days>=1:
				await self._execute_statement_update(world, "UPDATE friend_list SET recovery_time" + str(my_friend_id_index) + " = '" + current_time + "',friend_name"+str(my_friend_id_index) + "='" + str(f_game_name)+"'" + ",friend_level"+str(my_friend_id_index) + "=" + str(f_level) + " WHERE unique_id ='" +unique_id +"';")
				data={
					"remaining" :
					{
						"f_id":f_id,
						"f_name":f_game_name,
						"f_level":f_level,
						"current_time":current_time
					}
				}
				return self._message_typesetting(1, 'send friend gift success because time is over 1 day',data)
			else:
				data={
					"remaining" :
					{
						"f_id":f_id,
						"f_name":f_game_name,
						"f_level":f_level,
						"current_time":f_recovering_time
					}
				}
				return self._message_typesetting(99, 'send friend gift failed, because cooldown time is not finished',data)
	async def _send_all_friend_gift(self, world: int, unique_id: str):
		data = await self._execute_statement(world, 'SELECT * FROM friend_list WHERE unique_id = "' + unique_id + '";')
		mylist = list(data[0])
		f_id,f_name,f_level,f_recovery_time =[],[],[],[]
		for my_friend_id_index in range(1,int((len(mylist)-1)/4)+1):
			f_id_check = mylist[(my_friend_id_index-1)*4+1]
			f_game_name_check = mylist[(my_friend_id_index-1)*4+2]
			f_level_check = mylist[(my_friend_id_index-1)*4+3]
			if f_id_check =="":
				continue
			f_recovering_time = mylist[(my_friend_id_index-1)*4+4]
			if f_recovering_time=="":
				current_time = time.strftime('%Y-%m-%d', time.localtime())
				data = await self._execute_statement_update(world, 'UPDATE friend_list SET recovery_time' + str(my_friend_id_index) + ' = "' + current_time + '" WHERE unique_id = "' + unique_id + '";')
				mylist[(my_friend_id_index-1)*4+4]=current_time
				# print('send friend gift success because of f_recovering_time is empty')
			else:
				current_time = time.strftime('%Y-%m-%d', time.localtime())
				delta_time = datetime.strptime(current_time, '%Y-%m-%d') - datetime.strptime(f_recovering_time, '%Y-%m-%d')
				if delta_time.days>=1:
					# print("UPDATE friend_list SET recovery_time" + str(my_friend_id_index) + " = '" + current_time + "',friend_name"+str(my_friend_id_index) + "='" + str(f_game_name_check)+"'" + ",friend_level"+str(my_friend_id_index) + "=" + str(f_level_check) + " WHERE unique_id ='" +unique_id +"';")
					await self._execute_statement_update(world, "UPDATE friend_list SET recovery_time" + str(my_friend_id_index) + " = '" + current_time + "',friend_name"+str(my_friend_id_index) + "='" + str(f_game_name_check)+"'" + ",friend_level"+str(my_friend_id_index) + "=" + str(f_level_check) + " WHERE unique_id ='" +unique_id +"';")
					mylist[(my_friend_id_index-1)*4+4]=current_time
					# print('send friend gift success because time is over 1 day')
				else:
					pass
					# print('send friend gift failed, because not cooldown time is not finished')
			if mylist[(my_friend_id_index-1)*4+1+0]!='':
				f_id.append(mylist[(my_friend_id_index-1)*4+1])
				f_name.append(mylist[(my_friend_id_index-1)*4+2])
				f_level.append(mylist[(my_friend_id_index-1)*4+3])
				f_recovery_time.append(mylist[(my_friend_id_index-1)*4+4])
		data={
			"remaining":
			{
				"f_list_id":f_id,
				"f_name":f_name,
				"f_level":f_level,
				"f_recovery_time":f_recovery_time
			}
		}
		return self._message_typesetting(0, 'send all friends gift',data)
	async def _get_all_resource_info(self, world: int, unique_id: str):
		data = await self._execute_statement(world, 'SELECT * FROM player WHERE unique_id = "' + unique_id + '";')
		mylist = list(data[0])
		data = {
			"remaining":{
				"game_name": mylist[1],
				"coin": mylist[2],
				"iron": mylist[3],
				"diamond": mylist[4],
				"energy": mylist[5],
				"experience": mylist[6],
				"level": mylist[7],
				"role": mylist[8],
				"stage": mylist[9],
				"tower_stage": mylist[10],
				"skill_scroll_10":mylist[11],
				"skill_scroll_30": mylist[12],
				"skill_scroll_100": mylist[13],
				"experience_potion": mylist[14],
				"small_energy_potion": mylist[15],
				"recover_time": mylist[16],
				"hang_stage": mylist[17],
				"hang_up_time": mylist[18],
				"basic_summon_scroll": mylist[19],
				"pro_summon_scroll": mylist[20],
				"friend_gift": mylist[21],
				"prophet_summon_scroll": mylist[22],
				"fortune_wheel_ticket_basic": mylist[23],
				"fortune_wheel_ticket_pro": mylist[24]
			}
		}
		return self._message_typesetting(0, 'got all friends info',data)

	async def _get_all_tower_info(self, world: int, unique_id: str):
		if self._entry_consumables!="":
			return self._message_typesetting(1, 'configration is empty')
		data = {
			"remaining":{
				"entry_consumables":self._entry_consumables
			}
		}
		return self._message_typesetting(0, 'got all tower info',data)

	async def _get_all_armor_info(self, world: int, unique_id: str):
		armor1 = await self._execute_statement(world, 'SELECT * FROM armor1 WHERE unique_id = "' + unique_id + '";')
		armor2 = await self._execute_statement(world, 'SELECT * FROM armor2 WHERE unique_id = "' + unique_id + '";')
		armor3 = await self._execute_statement(world, 'SELECT * FROM armor3 WHERE unique_id = "' + unique_id + '";')
		armor4 = await self._execute_statement(world, 'SELECT * FROM armor4 WHERE unique_id = "' + unique_id + '";')
		data = {}
		for i in range(1,5):
			data.update({"armor"+str(i):{}})
			for j in range(1,11):
				data["armor"+str(i)].update({"armor_level"+str(j):str(eval("armor%s"%i)[0][j])})
		return self._message_typesetting(0, 'got all armor info',data)

	async def _level_enemy_layouts_config(self, world: int, unique_id: str):
		if self._level_enemy_layouts_config_json=="":
			return self._message_typesetting(1, 'configration is empty')
		data = {"remaining":{"level_enemy_layouts_config":self._level_enemy_layouts_config_json}}
		return self._message_typesetting(0, 'got all level enemy layouts config info',data)

	async def _monster_config(self, world: int, unique_id: str):
		if self._monster_config_json=="":
			return self._message_typesetting(1, 'configration is empty')
		data = {"remaining":{"monster_config":self._monster_config_json}}
		return self._message_typesetting(0, 'got all monster config info',data)

	async def _get_lottery_config_info(self, world: int, unique_id: str):
		if self._lottery=="":
			return self._message_typesetting(1, 'configration is empty')
		data = {"remaining":{"skills":self._lottery["skills"]["cost"],"weapons":self._lottery["weapons"]["cost"],"roles":self._lottery["roles"]["cost"],"fortune_wheel":self._lottery["fortune_wheel"]["cost"]}}
		return self._message_typesetting(0, 'got all lottery config info',data)

	async def _get_stage_reward_config(self, world: int, unique_id: str):
		if self._get_stage_reward_config_json=="":
			return self._message_typesetting(1, 'configration is empty')
		data = {"remaining":{"stage_reward_config":self._get_stage_reward_config_json}}
		return self._message_typesetting(0, 'got all stage reward config info',data)

	async def _get_all_friend_info(self, world: int, unique_id: str):
		#0 got all friends info
		# return message:{"f_list_id":f_id, "f_name":f_name,"f_level":f_level,"f_recovery_time":f_recovery_time}
		#return all friends info which friend id is not empty
		data = await self._execute_statement(world, 'SELECT * FROM friend_list WHERE unique_id = "' + unique_id + '";')
		mylist = list(data[0])
		f_id,f_name,f_level,f_recovery_time =[],[],[],[]
		for i in range(0,int((len(mylist)-1)/4)):
			if mylist[i*4+1+0]!="":
				f_id.append(mylist[i*4+1+0])
				f_name.append(mylist[i*4+1+1])
				f_level.append(mylist[i*4+1+2])
				f_recovery_time.append(mylist[i*4+1+3])
		data={
			"remaining":
			{
				"f_list_id":f_id,
				"f_name":f_name,
				"f_level":f_level,
				"f_recovery_time":f_recovery_time
			}
		}
		return self._message_typesetting(0, 'got all friends info',data)
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

	async def _set_role_star(self, world: int, unique_id: str, weapon: str, star: int):
		return await self._execute_statement_update(world, 'UPDATE role_bag SET ' + weapon + ' = "' + str(star) + '" WHERE unique_id = "' + unique_id + '";') 

	async def _get_segment(self, world: int, unique_id: str, weapon: str) -> int:
		data = await self._execute_statement(world, 'SELECT segment FROM `' + weapon + '` WHERE unique_id = "' + unique_id + '";')
		return int(data[0][0])

	async def _get_role_segment(self, world: int, unique_id: str, role: str) -> int:
		data = await self._execute_statement(world, 'SELECT segment FROM `' + role + '` WHERE unique_id = "' + unique_id + '";')
		return int(data[0][0])

	async def _set_segment_by_id(self, world: int, unique_id: str, weapon: str, segment: int):
		return await self._execute_statement_update(world, 'UPDATE `' + weapon + '` SET segment = "' + str(segment) + '" WHERE unique_id = "' + unique_id + '";')

	async def _set_role_segment_by_id(self, world: int, unique_id: str, role: str, segment: int):
		return await self._execute_statement_update(world, 'UPDATE `' + role + '` SET segment = "' + str(segment) + '" WHERE unique_id = "' + unique_id + '";')

	async def _get_weapon_star(self, world: int, unique_id: str, weapon: str) -> dict:
		data = await self._execute_statement(world, 'SELECT ' + weapon + ' FROM weapon_bag WHERE unique_id = "' + unique_id + '";')
		return int(data[0][0])

	async def _get_role_star(self, world: int, unique_id: str, role: str) -> dict:
		data = await self._execute_statement(world, 'SELECT ' + role + ' FROM role_bag WHERE unique_id = "' + unique_id + '";')
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
		self._reward = d['reward']
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

		result = requests.get('http://localhost:8000/get_level_enemy_layouts_config')
		self._level_enemy_layouts_config_json = result.json()

		result = requests.get('http://localhost:8000/get_monster_config')
		self._monster_config_json = result.json()

		result = requests.get('http://localhost:8000/get_stage_reward_config')
		self._get_stage_reward_config_json = result.json()

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

@ROUTES.post('/try_basic_summon_scroll')
async def __try_basic_summon_scroll(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_basic_summon_scroll(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_pro_summon_scroll')
async def __try_pro_summon_scroll(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_pro_summon_scroll(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_friend_gift')
async def __try_friend_gift(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_friend_gift(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_fprophet_summon_scroll')
async def __try_fprophet_summon_scroll(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_fprophet_summon_scroll(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_fortune_wheel_ticket_basic')
async def __try_fortune_wheel_ticket_basic(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_fortune_wheel_ticket_basic(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)

@ROUTES.post('/try_fortune_wheel_ticket_pro')
async def __try_fortune_wheel_ticket_pro(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_fortune_wheel_ticket_pro(int(post['world']), post['unique_id'], int(post['value']))
	return _json_response(result)
@ROUTES.post('/level_up_skill')
async def __level_up_skill(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).level_up_skill(int(post['world']), post['unique_id'], post['skill_id'], post['scroll_id'])
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

@ROUTES.post('/try_unlock_weapon')
async def __try_unlock_weapon(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).try_unlock_weapon(int(post['world']), post['unique_id'], post['weapon'])
	return _json_response(result)

@ROUTES.post('/basic_summon')
async def __basic_summon(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).basic_summon(int(post['world']), post['unique_id'], post['cost_item'],"weapons")
	return _json_response(result)

@ROUTES.post('/pro_summon')
async def __pro_summon(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).pro_summon(int(post['world']), post['unique_id'], post['cost_item'],"weapons")
	return _json_response(result)

@ROUTES.post('/friend_summon')
async def __friend_summon(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).friend_summon(int(post['world']), post['unique_id'], post['cost_item'],"weapons")
	return _json_response(result)

@ROUTES.post('/basic_summon_10_times')
async def __basic_summon_10_times(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).basic_summon_10_times(int(post['world']), post['unique_id'], post['cost_item'],"weapons")
	return _json_response(result)

@ROUTES.post('/pro_summon_10_times')
async def __pro_summon_10_times(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).pro_summon_10_times(int(post['world']), post['unique_id'], post['cost_item'],"weapons")
	return _json_response(result)

@ROUTES.post('/friend_summon_10_times')
async def __friend_summon_10_times(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).friend_summon_10_times(int(post['world']), post['unique_id'], post['cost_item'],"weapons")
	return _json_response(result)

@ROUTES.post('/prophet_summon_10_times')
async def __prophet_summon_10_times(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).prophet_summon_10_times(int(post['world']), post['unique_id'], post['cost_item'],"weapons")
	return _json_response(result)

@ROUTES.post('/basic_summon_skill')
async def basic_summon_skill(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).basic_summon(int(post['world']), post['unique_id'], post['cost_item'],"skills")
	return _json_response(result)

@ROUTES.post('/pro_summon_skill')
async def pro_summon_skill(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).pro_summon(int(post['world']), post['unique_id'], post['cost_item'],"skills")
	return _json_response(result)

@ROUTES.post('/friend_summon_skill')
async def friend_summon_skill(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).friend_summon(int(post['world']), post['unique_id'], post['cost_item'],"skills")
	return _json_response(result)


@ROUTES.post('/basic_summon_skill_10_times')
async def basic_summon_skill_10_times(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).basic_summon_10_times(int(post['world']), post['unique_id'], post['cost_item'],"skills")
	return _json_response(result)

@ROUTES.post('/pro_summon_skill_10_times')
async def pro_summon_skill_10_times(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).pro_summon_10_times(int(post['world']), post['unique_id'], post['cost_item'],"skills")
	return _json_response(result)

@ROUTES.post('/friend_summon_skill_10_times')
async def friend_summon_skill_10_times(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).friend_summon_10_times(int(post['world']), post['unique_id'], post['cost_item'],"skills")
	return _json_response(result)


@ROUTES.post('/basic_summon_roles')
async def basic_summon_roles(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).basic_summon(int(post['world']), post['unique_id'], post['cost_item'],"roles")
	return _json_response(result)

@ROUTES.post('/pro_summon_roles')
async def pro_summon_roles(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).pro_summon(int(post['world']), post['unique_id'], post['cost_item'],"roles")
	return _json_response(result)

@ROUTES.post('/friend_summon_roles')
async def friend_summon_roles(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).friend_summon(int(post['world']), post['unique_id'], post['cost_item'],"roles")
	return _json_response(result)


@ROUTES.post('/basic_summon_roles_10_times')
async def basic_summon_roles_10_times(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).basic_summon_10_times(int(post['world']), post['unique_id'], post['cost_item'],"roles")
	return _json_response(result)

@ROUTES.post('/pro_summon_roles_10_times')
async def pro_summon_roles_10_times(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).pro_summon_10_times(int(post['world']), post['unique_id'], post['cost_item'],"roles")
	return _json_response(result)

@ROUTES.post('/friend_summon_roles_10_times')
async def friend_summon_roles_10_times(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER']).friend_summon_10_times(int(post['world']), post['unique_id'], post['cost_item'],"roles")
	return _json_response(result)


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

@ROUTES.post('/send_friend_gift')
async def __fortune_wheel_pro(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER'])._send_friend_gift(int(post['world']), post['unique_id'], post['friend_id'])
	return _json_response(result)

@ROUTES.post('/send_all_friend_gift')
async def __fortune_wheel_pro(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER'])._send_all_friend_gift(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/get_all_friend_info')
async def __fortune_wheel_pro(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER'])._get_all_friend_info(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/get_all_resource_info')
async def __get_all_resource_info(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER'])._get_all_resource_info(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/get_all_tower_info')
async def __get_all_tower_info(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER'])._get_all_tower_info(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/get_all_armor_info')
async def get_all_armor_info(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER'])._get_all_armor_info(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/level_enemy_layouts_config')
async def _level_enemy_layouts_config(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER'])._level_enemy_layouts_config(int(post['world']), post['unique_id'])
	return _json_response(result)


@ROUTES.post('/monster_config')
async def _monster_config(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER'])._monster_config(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/get_lottery_config_info')
async def _get_lottery_config_info(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER'])._get_lottery_config_info(int(post['world']), post['unique_id'])
	return _json_response(result)

@ROUTES.post('/get_stage_reward_config')
async def _get_stage_reward_config(request: web.Request) -> web.Response:
	post = await request.post()
	result = await (request.app['MANAGER'])._get_stage_reward_config(int(post['world']), post['unique_id'])
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
	web.run_app(app, port=config.getint('game_manager_qin', 'port'))


if __name__ == '__main__':
	run()
