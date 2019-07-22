#
# An example for an SQL manager server using asyncio programming methods.
# We will use aiohttp library to network these API calls so that they can be
# accessed from different physical devices on the network.
# Additionally, we will be using tormysql library to manage the SQL server pool
# of connections.
#
# All functions that connect to the database should be async. The more async code
# we use, the faster the entire server becomes.
#
#
# The file has two parts:
#	- The DefaultManager class
#	- The aiohttp server bindings for the class methods
#
###############################################################################


# Some safe default includes. Feel free to add more if you need.
import random
import json
import os
import configparser
import tormysql
from aiohttp import web

CONFIG = configparser.ConfigParser()
CONFIG.read('./Configuration/server/1.0/server.conf')
JSON_NAME = "./Configuration/client/1.0/stage_reward_config.json"


import json
import random
import tormysql
import configparser
from aiohttp import web
from aiohttp import ClientSession

CONFIG = configparser.ConfigParser()
CONFIG.read('./Configuration/server/1.0/server.conf')
LOTTERY = configparser.ConfigParser()
LOTTERY.read('./Configuration/server/1.0/lottery.conf')
BAG_BASE_URL = CONFIG['_04_Manager_Game']['address'] + ':' + CONFIG['_04_Manager_Game']['port']
SKILL_BASE_URL = CONFIG['skill_manager']['address'] + ':' + CONFIG['skill_manager']['port']
WEAPON_BASE_URL = CONFIG['_01_Manager_Weapon']['address'] + ':' + CONFIG['_01_Manager_Weapon']['port']

SKILL_ID_LIST = ["m1_level", "p1_level", "g1_level", "m11_level", "m12_level", "m13_level", "p11_level", "p12_level", "p13_level", "g11_level", "g12_level", "g13_level", "m111_level", "m112_level", "m113_level", "m121_level", "m122_level", "m123_level", "m131_level", "m132_level", "m133_level", "p111_level", "p112_level", "p113_level", "p121_level", "p122_level", "p123_level", "p131_level", "p132_level", "p133_level", "g111_level", "g112_level", "g113_level", "g121_level", "g122_level", "g123_level", "g131_level", "g132_level", "g133_level"]


# Part (1 / 2)
import time
from datetime import datetime, timedelta
import json
import random
import tormysql
import configparser
from aiohttp import web
from aiohttp import ClientSession

CONFIG = configparser.ConfigParser()
CONFIG.read('./Configuration/server/1.0/server.conf')

BAG_BASE_URL = CONFIG['_04_Manager_Game']['address'] + CONFIG['_04_Manager_Game']['port']


# Part (1 / 2)
import json
import random
import tormysql
import configparser
from aiohttp import web
from aiohttp import ClientSession

CONFIG = configparser.ConfigParser()
CONFIG.read('./Configuration/server/1.0/server.conf')

BAG_BASE_URL = CONFIG['_04_Manager_Game']['address'] + ':' + CONFIG['_04_Manager_Game']['port']


# Part (1 / 2)
import json
import tormysql
import os
import configparser
import random
from aiohttp import web
from aiohttp import ClientSession


format_sql = {
	"smallint": "%s",
	"varchar": "'%s'",
	"char": "'%s'"
}
CONFIG = configparser.ConfigParser()
CONFIG.read('./Configuration/server/1.0/server.conf')
MANAGER_BAG_BASE_URL = CONFIG['_04_Manager_Game']['address'] + ":" + CONFIG['_04_Manager_Game']['port']


import json
import os
import random
import tormysql
import configparser
from aiohttp import web
from aiohttp import ClientSession


CONFIG = configparser.ConfigParser()
CONFIG.read('./Configuration/server/1.0/server.conf')
MANAGER_PLAYER_BASE_URL = CONFIG['_04_Manager_Game']['address'] + ":" + CONFIG['_04_Manager_Game']['port']


import json
import tormysql
import random
from aiohttp import web
from aiohttp import ClientSession


# Part (1 / 2)
class PlayerManager:
	async def get_all_head(self, table: str) -> dict:
		"""
		Used to get information such as the title of the database
		用于获取数据库的标题等信息
		:return:返回所有数据库的标题等信息，json数据
		"""
		data = list(await self._execute_statement("desc %s;" % table))
		return self.__internal_format(status=0, remaining=data)
	async def get_all_material(self, unique_id: str) -> dict:
		"""
		Used to get all numeric or string information
		用于获取所有的数字或字符串信息
		:param unique_id: 用户的唯一标识
		:return:返回所有材料名对应的值，json数据
		"""
		data = await self._execute_statement("SELECT * FROM player WHERE unique_id='" + str(unique_id) + "'")
		return self.__internal_format(status=0, remaining=data[0])
	async def get_all_supplies(self, unique_id: str) -> dict:
		data_tuple = (await self.get_all_head(table="player"))["remaining"]
		heads = []
		for col in data_tuple:
			heads.append(col[0])
		content = list((await self.get_all_material(unique_id=unique_id))["remaining"])
		heads.pop(0)
		content.pop(0)
		return self.message_typesetting(status=0, message="get supplies success", data={"keys": heads, "values": content})
	async def add_supplies(self, unique_id: str, key: str, value: int):
		if value <= 0: return self.message_typesetting(status=9, message="not a positive number")
		json_data = await self.__try_material(unique_id=unique_id, key=key, value=value)
		if json_data["status"] == 0:
			return self.message_typesetting(status=0, message="success", data={"keys": [key], "values": [json_data["remaining"]]})
		return self.message_typesetting(status=1, message="failure")
	async def level_up_scroll(self, unique_id: str, scroll_id: str) -> dict:
		# 0 success
		# 1 advanced reels are not upgradeable
		# 2 insufficient scroll
		# 3 unexpected parameter
		# 4 parameter error
		# 9 database operation error
		print("scroll_id：" + scroll_id)
		if scroll_id == "skill_scroll_100": return self.message_typesetting(status=1, message="advanced reels are not upgradeable!")
		try:
			scroll_id_count = await self.__get_material(unique_id=unique_id, material=scroll_id)
			if scroll_id_count < 3:
				return self.message_typesetting(status=2, message="Insufficient scroll")
			elif scroll_id == "skill_scroll_10":
				dict1 = await self.try_skill_scroll_10(unique_id=unique_id, value=-3)
				dict2 = await self.try_skill_scroll_30(unique_id=unique_id, value=1)
				if dict1["status"] == 1 or dict2["status"] == 1:
					return self.message_typesetting(status=9, message="database operation error!")
				return self.message_typesetting(status=0, message="level up scroll success!", data={"keys": ["skill_scroll_10", "skill_scroll_30"], "values": [dict1["remaining"], dict2["remaining"]]})
			elif scroll_id == "skill_scroll_30":
				dict1 = await self.try_skill_scroll_30(unique_id=unique_id, value=-3)
				dict2 = await self.try_skill_scroll_100(unique_id=unique_id, value=1)
				if dict1["status"] == 1 or dict2["status"] == 1:
					return self.message_typesetting(status=9, message="database operation error!")
				return self.message_typesetting(status=0, message="level up scroll success!", data={"keys":["skill_scroll_30", "skill_scroll_100"], "values": [dict1["remaining"], dict2["remaining"]]})
			else:
				return self.message_typesetting(status=3, message="unexpected parameter --> " + scroll_id)
		except:
			return self.message_typesetting(status=9, message="parameter error!")
	async def try_all_material(self, unique_id: str, stage: int) -> dict:
		sql_stage = await self.__get_material(unique_id=unique_id, material="stage")
		if stage <= 0 or sql_stage + 1 < stage:
			print("[try_all_material] -> stage:" + str(stage))
			return self.__internal_format(status=9, remaining=0)  # abnormal data!
		if sql_stage + 1 == stage:  # 通过新关卡
			material_dict = dict(self.reward_list[stage])
			material_dict.update({"stage": 1})
		else:  # 老关卡
			material_dict = dict(self.reward_list[sql_stage])
		update_str, select_str = self.__sql_str_operating(unique_id=unique_id, material_dict=material_dict)
		data = 1 - await self._execute_statement_update(statement=update_str)  # 0, 1反转
		remaining = list(await self._execute_statement(statement=select_str))  # 数据库设置后的值
		# 通过新关卡有关卡数据的返回，老关卡没有关卡数据的返回
		return self.__internal_format(status=data, remaining=[material_dict, remaining[0]])  # 0 成功， 1 失败
	async def __update_material(self, unique_id: str, material: str, material_value: int) -> int:
		"""
		Used to set information such as numeric values
		用于设置数值等信息
		:param unique_id:用户唯一识别码
		:param material:材料名
		:param material_value:要设置的材料对应的值
		:return:返回是否更新成功的标识，1为成功，0为失败
		"""
		return await self._execute_statement_update("UPDATE player SET " + material + "=" + str(material_value) + " where unique_id='" + unique_id + "'")
	async def __get_material(self, unique_id: str, material: str) -> int or str:
		"""
		Used to get numeric or string information
		用于获取数字或字符串信息
		:param unique_id: 用户的唯一标识
		:param material:材料名
		:return:返回材料名对应的值
		"""
		data = await self._execute_statement("SELECT " + material + " FROM player WHERE unique_id='" + str(unique_id) + "'")
		return data[0][0]
	async def __set_material(self, unique_id: str, material: str, material_value: str) -> int:
		"""
		Used to set string information such as user name
		用于设置用户名等字符串信息
		:param unique_id:用户的唯一标识
		:param material:材料名
		:param material_value:要存入数据库的值
		:return:update的状态返回量，1：成功，0：失败（未改变数据统一返回0）
		"""
		return await self._execute_statement_update("UPDATE player SET " + material + "='" + str(material_value) + "' where unique_id='" + unique_id + "'")
	async def __try_material(self, unique_id: str, key: str, value: int) -> dict:
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
		num = await self.__get_material(unique_id=unique_id, material=key)
		if value == 0: return self.__internal_format(0, num)
		num += value
		if num < 0: return self.__internal_format(1, num)
		if await self.__update_material(unique_id=unique_id, material=key, material_value=num) == 0:
			return self.__internal_format(1, num)
		return self.__internal_format(status=0, remaining=num)
	async def try_coin(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="coin", value=value)
	async def try_iron(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="iron", value=value)
	async def try_diamond(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="diamond", value=value)
	async def try_experience(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="experience", value=value)
	async def try_level(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="level", value=value)
	async def try_role(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="role", value=value)
	async def try_stage(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="stage", value=value)
	async def try_skill_scroll_10(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="skill_scroll_10", value=value)
	async def try_skill_scroll_30(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="skill_scroll_30", value=value)
	async def try_skill_scroll_100(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="skill_scroll_100", value=value)
	async def try_experience_potion(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="experience_potion", value=value)
	async def try_small_energy_potion(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="small_energy_potion", value=value)
	def __read_json_data(self) -> list:
		data = []
		if os.path.exists(JSON_NAME):
			data_dict = json.load(open(JSON_NAME, encoding="utf-8"))
			for key in data_dict.keys():
				data.append(data_dict[key])
		print("[__read_json_data] -> data:" + str(data))
		return data
	def __sql_str_operating(self, unique_id: str, material_dict: dict) -> (str, str):
		update_str = "UPDATE player SET "
		update_end_str = " where unique_id='%s'" % unique_id
		select_str = "SELECT "
		select_end_str = " FROM player WHERE unique_id='%s'" % unique_id
		for key in material_dict.keys():
			update_str += "%s=%s+%s, " % (key, key, material_dict[key])
			select_str += "%s, " % key
		update_str = update_str[: len(update_str) - 2] + update_end_str
		select_str = select_str[: len(select_str) - 2] + select_end_str
		print("[__sql_str_operating] -> update_str:" + update_str)
		print("[__sql_str_operating] -> select_str:" + select_str)
		return update_str, select_str
	async def random_gift_skill(self, unique_id: str) -> dict:
		# 0 - skill ======== success, unlocked new skill 或 skill scroll ======== you received a free scroll
		# {"skill_id": skill_id, "value": value} 或 {"skill_scroll_id": skill_scroll_id, "value": value}
		# 2 - invalid skill name
		# 3 - database operation error
		tier_choice = (random.choices(self._skill_tier_names, self._skill_tier_weights))[0]
		gift_skill = (random.choices(self._skill_items[tier_choice]))[0]
		print("gift_skill:" + str(gift_skill))
		if self.__class__.__name__ == 'PlayerManager':
			data = await self.try_unlock_skill(unique_id, gift_skill)
			status = int(data["status"])
			if status == 1:  # skill already unlocked
				if tier_choice == 'skilltier1':
					skill_scroll_id = "skill_scroll_10"
					data = await self.try_skill_scroll_10(unique_id, 1)
				elif tier_choice == 'skilltier2':
					skill_scroll_id = "skill_scroll_30"
					data = await self.try_skill_scroll_30(unique_id, 1)
				else:
					skill_scroll_id = "skill_scroll_100"
					data = await self.try_skill_scroll_100(unique_id, 1)
				if data["status"] == 0:
					return self.message_typesetting(status=0, message='you received a free scroll', data={"keys": [skill_scroll_id], "values": [data["remaining"]]})
				return self.message_typesetting(status=3, message='database operation error')
			elif status == 0:  # success
				return self.message_typesetting(status=status, message=data['remaining'][status], data={"keys": [gift_skill], "values": [1]})
			else:  # 2
				return self.message_typesetting(status=status, message=data['remaining'][status])
		else:
			async with ClientSession() as session:
				async with session.post(SKILL_BASE_URL + '/try_unlock_skill', data = {'unique_id' : unique_id, 'skill_id' : gift_skill}) as resp:
					data = await resp.json(content_type = 'text/json')
				status = int(data['status'])
				if status == 1:
					if tier_choice == 'skilltier1':
						skill_scroll_id = "skill_scroll_10"
						async with session.post(BAG_BASE_URL + '/try_skill_scroll_10', data={'unique_id': unique_id, 'value': 1}) as resp:
							json_data = await resp.json(content_type='text/json')
					elif tier_choice == 'skilltier2':
						skill_scroll_id = "skill_scroll_30"
						async with session.post(BAG_BASE_URL + '/try_skill_scroll_30', data={'unique_id': unique_id, 'value': 1}) as resp:
							json_data = await resp.json(content_type='text/json')
					else:
						skill_scroll_id = "skill_scroll_100"
						async with session.post(BAG_BASE_URL + '/try_skill_scroll_100', data={'unique_id': unique_id, 'value': 1}) as resp:
							json_data = await resp.json(content_type='text/json')
					if json_data["status"] == 0:
						return self.message_typesetting(status=0, message='you received a free scroll', data={"keys": [skill_scroll_id], "values": [data["remaining"]]})
					return self.message_typesetting(status=3, message='database operation error')
				elif status == 0:  # success
					return self.message_typesetting(status=status, message=data['remaining'][status], data={"keys": [gift_skill], "values": [1]})
				else:  # 2
					return self.message_typesetting(status=status, message=data['remaining'][status])
	async def random_gift_segment(self, unique_id: str) -> dict:
		# - 0 - Unlocked new weapon!   ===> {"keys": ["weapon"], "values": [weapon]}
		# - 0 - Weapon already unlocked, got free segment   ===>  {"keys": ['weapon', 'segment'], "values": [weapon, segment]}
		# - 1 - no weapon!
		tier_choice = (random.choices(self._weapon_tier_names, self._weapon_tier_weights))[0]
		gift_weapon = (random.choices(self._weapon_items[tier_choice]))[0]
		async with ClientSession() as session:
			async with session.post(WEAPON_BASE_URL + '/try_unlock_weapon', data = {'unique_id' : unique_id, 'weapon' : gift_weapon}) as resp:
				return await resp.json(content_type = 'text/json')
			####################################
			#          P R I V A T E		   #
			####################################
		
	def _read_lottery_configuration(self):
		self._skill_tier_names = eval(LOTTERY['skills']['names'])
		self._skill_tier_weights = eval(LOTTERY['skills']['weights'])
		self._skill_items = eval(LOTTERY['skills']['items'])
		self._weapon_tier_names = eval(LOTTERY['weapons']['names'])
		self._weapon_tier_weights = eval(LOTTERY['weapons']['weights'])
		self._weapon_items = eval(LOTTERY['weapons']['items'])
	# It is helpful to define a private method that you can simply pass
	# an SQL command as a string and it will execute. Call this method
	# whenever you issue an SQL statement.
	async def try_energy(self, unique_id: str, amount: int) -> dict:  # amount > 0
		# - 0 - 获取能量成功 === Get energy successfully
		# - 0 - 能量已消耗，能量值及恢复时间更新成功 === Energy has been consumed, energy value and recovery time updated successfully
		# - 0 - 能量已恢复，获取能量成功 === Energy has been recovered and energy is successfully acquired
		# - 0 - 能量刷新后已消耗，能量值及恢复时间更新成功 === After refreshing the energy, the energy value and recovery time are successfully updated.
		# - 0 - 能量已刷新，未恢复满，已消耗能量，能量值及恢复时间更新成功 === Energy has been refreshed, not fully recovered, energy has been consumed, energy value and recovery time updated successfully
		# - 1 - 参数错误 === Parameter error
		# - 2 - 无足够能量消耗 === Not enough energy consumption
		if amount < 0 or amount > self._full_energy:
			return self.message_typesetting(status=1, message="Parameter error")
		return await self._decrease_energy(unique_id=unique_id, amount=amount)
			####################################
			#          P R I V A T E		   #
			####################################
	async def _decrease_energy(self, unique_id: str, amount: int) -> dict:
		current_energy, recover_time = await self._get_energy_information(unique_id)
		current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		if recover_time == '':  # 此时 current_energy == self._full_energy 成立
			if amount == 0:  # 成功1：如果没有恢复时间且是获取能量值，则直接拿取数据库的值给客户端
				return self.message_typesetting(status=0, message='Get energy successfully', data={"keys": ['energy', 'recover_time'], "values": [current_energy, recover_time]})
			current_energy -= amount
			# 成功2：如果没有恢复时间且是消耗能量值，则直接用数据库的值减去消耗的能量值，
			# 然后存入消耗之后的能量值，以及将当前的时间存入 恢复时间项
			await self._execute_statement('UPDATE player SET energy = ' + str(current_energy) + ', recover_time = "' + current_time + '" WHERE unique_id = "' + unique_id + '";')
			return self.message_typesetting(0, 'Energy has been consumed, energy value and recovery time updated successfully', {"keys": ['energy', 'recover_time'], "values": [current_energy, current_time]})
		else:
			delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S')
			recovered_energy = delta_time.seconds // 60 // self._recover_time
			if amount == 0:
				# 成功3：如果有恢复时间且是获取能量值，则加上获取的能量值，并判断能量值是否满足上限
				# - 1 - 满足上限的情况：直接将满能量值和空字符串分别存入能量值项和恢复时间项
				# - 2 - 不满足上限的情况：将能恢复的能量值计算出来，并且计算恢复后的能量值current_energy
				#       和恢复时间与恢复能量消耗的时间相减的恢复时间值
				recover_time, current_energy = ("", self._full_energy) if (current_energy + recovered_energy >= self._full_energy) else ((datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=recovered_energy * self._recover_time)).strftime("%Y-%m-%d %H:%M:%S"), current_energy + recovered_energy)
				await self._execute_statement('UPDATE player SET energy = ' + str(current_energy) + ', recover_time = "' + recover_time + '" WHERE unique_id = "' + unique_id + '";')
				return self.message_typesetting(status=0, message='Energy has been recovered and energy is successfully acquired', data={"keys": ['energy', 'recover_time'], "values": [current_energy, recover_time]})
			if recovered_energy + current_energy >= self._full_energy:
				# 成功4：如果有恢复时间且是消耗能量
				# 满足上限的情况是用上限能量值减去要消耗的能量值，然后设置减去之后的能量值和当前的时间分别存入能量值项和恢复时间项
				current_energy = self._full_energy - amount
				await self._execute_statement('UPDATE player SET energy = ' + str(current_energy) + ', recover_time = "' + current_time + '" WHERE unique_id = "' + unique_id + '";')
				return self.message_typesetting(0, 'After refreshing the energy, the energy value and recovery time are successfully updated.', {"keys": ['energy', 'recover_time'], "values": [current_energy, current_time]})
			elif recovered_energy + current_energy - amount >= 0:
				# 成功5：如果有恢复时间且是消耗能量
				# 不满足上限的情况是用当前数据库的能量值和当前恢复的能量值相加然后减去消耗的能量值为要存入数据库的能量值项
				# 数据库中的恢复时间与恢复能量消耗的时间相减的恢复时间值存入到数据库的恢复时间项
				current_energy = recovered_energy + current_energy - amount
				recover_time = (datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=recovered_energy * self._recover_time)).strftime("%Y-%m-%d %H:%M:%S")
				await self._execute_statement('UPDATE player SET energy = ' + str(current_energy) + ', recover_time = "' + recover_time + '" WHERE unique_id = "' + unique_id + '";')
				return self.message_typesetting(0, 'Energy has been refreshed, not fully recovered, energy has been consumed, energy value and recovery time updated successfully', {"keys": ['energy', 'recover_time'], "values": [current_energy, recover_time]})
			else:  # 发生的情况是当前能量值和恢复能量值相加比需要消耗的能量值少
				return self.message_typesetting(status=2, message="Not enough energy consumption")
	async def _get_energy_information(self, unique_id: str) -> (int, str):
		data = await self._execute_statement('SELECT energy, recover_time FROM player WHERE unique_id = "' + unique_id + '";')
		return int(data[0][0]), data[0][1]
	# It is helpful to define a private method that you can simply pass
	# an SQL command as a string and it will execute. Call this method
	# whenever you issue an SQL statement.
	async def level_up_skill(self, unique_id: str, skill_id: str, scroll_id: str) -> dict:
		# 0 - Success upgrade=0 升级成功， upgrade=1升级失败
		# 1 - User does not have that skill
		# 2 - Invalid scroll id
		# 4 - User does not have enough scrolls
		# 9 - Skill already at max level
		skill_level = await self._get_skill_level(unique_id, skill_id)
		if skill_level == 0:
			return self.message_typesetting(1, 'User does not have that skill')
		if skill_level >= 10:
			return self.message_typesetting(9, 'Skill already max level')
		fn = {'skill_scroll_10': self.try_skill_scroll_10, 'skill_scroll_30': self.try_skill_scroll_30, 'skill_scroll_100': self.try_skill_scroll_100}
		if self.__class__.__name__ == 'PlayerManager':
			if scroll_id not in fn.keys():
				return self.message_typesetting(status=2, message="Invalid scroll id")
			f = fn[scroll_id]
			resp = await f(unique_id, -1)
			if resp['status'] == 1:
				return self.message_typesetting(4, 'User does not have enough scrolls')
			scroll_quantity = resp['remaining']
		else:
			if scroll_id not in fn.keys():
				return self.message_typesetting(status=2, message="Invalid scroll id")
			async with ClientSession() as session:
				async with session.post(BAG_BASE_URL + '/try_'+scroll_id, data = {'unique_id' : unique_id, 'value' : -1}) as resp:
					resp = await resp.json(content_type='text/json')
					if resp['status'] == 1:
						return self.message_typesetting(4, 'User does not have enough scrolls')
					scroll_quantity = resp['remaining']
			
		if not await self._roll_for_upgrade(scroll_id):
			return self.message_typesetting(0, 'success', {'keys': [skill_id, scroll_id], 'values': [skill_level, scroll_quantity], 'upgrade': 1})
		await self._execute_statement('UPDATE skill SET `' + skill_id + '` = ' + str(skill_level + 1) + ' WHERE unique_id = "' + unique_id + '";')
		return self.message_typesetting(0, 'success', {'keys': [skill_id, scroll_id], 'values': [skill_level + 1, scroll_quantity], 'upgrade': 0})
	async def get_all_skill_level(self, unique_id: str) -> dict:
		# 0 - Success
		names = await self._execute_statement('DESCRIBE skill;')
		values = await self._execute_statement('SELECT * from skill WHERE unique_id = "' + str(unique_id) + '";')
		key_list = []
		value_list = []
		for num, val in enumerate(zip(names[1:], values[0][1:])):
			key_list.append(val[0][0])
			value_list.append(val[1])
		return self.message_typesetting(0, 'success', data={"keys": key_list, "values": value_list})
	async def get_skill(self, unique_id: str, skill_id: str) -> dict:
		# 0 - Success
		# 1 - invalid skill name
		try:
			level = await self._get_skill_level(unique_id, skill_id)
			return self.message_typesetting(0, 'success', {'keys': [skill_id], 'values': [level]})
		except:
			return self.message_typesetting(1, 'invalid skill name')
	async def try_unlock_skill(self, unique_id: str, skill_id: str) -> dict:
		# 0 - success, unlocked new skill
		# 1 - skill already unlocked
		# 2 - invalid skill name
		# json ===> {"status": status, "remaining": remaining} ===> status 0、1、2、3
		table_tuple = ("success, unlocked new skill", "skill already unlocked", "invalid skill name")
		try:  # 0、1、2
			level = await self._get_skill_level(unique_id, skill_id)
			if level == 0 and await self._execute_statement_update('UPDATE skill SET `' + skill_id + '` = 1 WHERE unique_id = "' + unique_id + '";') == 1:
				return self.__internal_format(status=0, remaining=table_tuple)  # success, unlocked new skill
			return self.__internal_format(status=1, remaining=table_tuple)  # skill already unlocked
		except:
			return self.__internal_format(status=2, remaining=table_tuple)  # invalid skill name
			####################################
			#          P R I V A T E		   #
			####################################
		
		
	async def _get_skill_level(self, unique_id: str, skill_id: str) -> int:
		data = await self._execute_statement('SELECT ' + skill_id + ' FROM skill WHERE unique_id = "' + unique_id + '";')
		return int(data[0][0])
	async def _roll_for_upgrade(self, scroll_id: str) -> bool:
		UPGRADE = { 'skill_scroll_10' : 0.10, 'skill_scroll_30' : 0.30, 'skill_scroll_100' : 1 }
		try:
			roll = random.random()
			return roll < UPGRADE[scroll_id]
		except KeyError:
			return False
	# It is helpful to define a private method that you can simply pass
	# an SQL command as a string and it will execute. Call this method
	# whenever you issue an SQL statement.
	async def pass_stage(self, unique_id: str, stage: int) -> dict:
		# 0 : passed customs ===> success
		# 1 : database operation error
		# 9 : abnormal data!
		if self.__class__.__name__ == "PlayerManager":
			json_data = await self.try_all_material(unique_id=unique_id, stage=stage)
		else:
			async with ClientSession() as session:
				async with session.post(MANAGER_BAG_BASE_URL + '/try_all_material', data = {'unique_id' : unique_id, 'stage': stage}) as resp:
					json_data = json.loads(await resp.text())
		status = int(json_data["status"])
		if status == 9:
			return self.message_typesetting(status=9, message="abnormal data!")
		elif status == 1:
			return self.message_typesetting(status=1, message="database operation error")
		else:
			material_dict = json_data["remaining"][0]
			data = {"keys": list(material_dict.keys()), "values": json_data["remaining"][1], "rewards": list(material_dict.values())}
			return self.message_typesetting(status=0, message="passed customs!", data=data)
	async def level_up_weapon(self, unique_id: str, weapon: str, iron: int) -> dict:
		# - 0 - Success
		# - 1 - User does not have that weapon
		# - 2 - Insufficient materials, upgrade failed
		# - 3 - Database operation error
		# - 9 - Weapon already max level
		async with ClientSession() as session:
			if await self.__get_weapon_star(unique_id, weapon) == 0:
				return self.message_typesetting(status=1, message="user does not have that weapon")
			head = []
			if self.__class__.__name__ == "PlayerManager":
				data_tuple = (await self.get_all_head(table=weapon))["remaining"]
			else:
				async with session.post(MANAGER_PLAYER_BASE_URL + '/get_all_head', data={'table': weapon}) as resp:
					data_tuple = json.loads(await resp.text())['remaining']
			for col in data_tuple:
				head.append(col[0])
			row = await self.__get_row_by_id(weapon, unique_id)
			if row[1] == 100:
				return self.message_typesetting(status=9, message="weapon has reached max level")
			skill_upgrade_number = int(iron) // self._standard_iron_count
			level_count = head.index("weapon_level")
			point_count = head.index("skill_point")
			# calculate resulting levels and used iron
			if (row[level_count] + skill_upgrade_number) > 100:
				skill_upgrade_number = 100 - row[level_count]
			row[level_count] += skill_upgrade_number
			row[point_count] += skill_upgrade_number
			if skill_upgrade_number == 0:
				return self.message_typesetting(status=2, message="insufficient materials, upgrade failed")
			if self.__class__.__name__ == "PlayerManager":
				json_data = await self.try_iron(unique_id=unique_id, value=-skill_upgrade_number * self._standard_iron_count)
			else:
				async with session.post(MANAGER_PLAYER_BASE_URL + '/try_iron', data={"unique_id": unique_id, "value": -skill_upgrade_number * self._standard_iron_count}) as resp:
					json_data = json.loads(await resp.text())
			if int(json_data["status"]) == 1:
				return self.message_typesetting(status=2, message="insufficient materials, upgrade failed")
			remaining_iron = int(json_data["remaining"])
			# update the weapon level on the account
			if await self.__set_weapon_level_up_data(unique_id=unique_id, weapon=weapon, weapon_level=row[level_count], skill_point=row[point_count]) == 0:
				return self.message_typesetting(status=3, message="database operation error")
			head[0] = "weapon"
			row[0] = weapon
			head.append("iron")
			row.append(remaining_iron)
			return self.message_typesetting(status=0, message="success", data={'keys': head, 'values': row})
	# levels up a particular passive skill. costs skill points.
	# 提升特定的被动技能。 增加技能点。
	async def level_up_passive(self, unique_id: str, weapon: str, passive_skill: str) -> dict:
		# - 0 - Success
		# - 1 - User does not have that weapon
		# - 2 - Insufficient skill points, upgrade failed
		# - 3 - Database operation error
		# - 9 - Weapon already max level
		async with ClientSession() as session:
			if await self.__get_weapon_star(unique_id, weapon) == 0:
				return self.message_typesetting(status=1, message="user does not have that weapon")
			if passive_skill not in self._valid_passive_skills:
				return self.message_typesetting(status=9, message="passive skill does not exist")
			head = []
			if self.__class__.__name__ == "PlayerManager":
				data_tuple = (await self.get_all_head(table=weapon))["remaining"]
			else:
				async with session.post(MANAGER_PLAYER_BASE_URL + '/get_all_head', data={'table': weapon}) as resp:
					data_tuple = json.loads(await resp.text())['remaining']
			for col in data_tuple:
				head.append(col[0])
			row = await self.__get_row_by_id(weapon, unique_id)
			point_count = head.index("skill_point")
			passive_count = head.index(passive_skill)
			if row[point_count] == 0:
				return self.message_typesetting(status=2, message="Insufficient skill points, upgrade failed")
			row[point_count] -= 1
			row[passive_count] += 1
			if await self.__set_passive_skill_level_up_data(unique_id=unique_id, weapon=weapon, passive_skill=passive_skill, skill_level=row[passive_count], skill_points=row[point_count]) == 0:
				return self.message_typesetting(status=3, message="database operation error")
			head[0] = "weapon"
			row[0] = weapon
			return self.message_typesetting(status=0, message="success", data={"keys": head, "values": row})
	# resets all weapon passive skill points. refunds all skill points back. costs coins.
	async def reset_weapon_skill_point(self, unique_id: str, weapon: str) -> dict:
		# - 0 - Success
		# - 1 - no weapon
		# - 2 - insufficient gold coins, upgrade failed
		# - 3 - database operation error!
		# - 9 - Weapon reset skill point success
		async with ClientSession() as session:
			# get the coin from the account
			if await self.__get_weapon_star(unique_id=unique_id, weapon=weapon) == 0:
				return self.message_typesetting(status=1, message="no weapon!")
			if self.__class__.__name__ == "PlayerManager":
				json_data = await self.try_coin(unique_id=unique_id, value=-self._standard_reset_weapon_skill_coin_count)
				data_tuple = (await self.get_all_head(table=weapon))["remaining"]
			else:
				async with session.post(MANAGER_PLAYER_BASE_URL + '/try_coin', data={"unique_id": unique_id, "value": -self._standard_reset_weapon_skill_coin_count}) as resp:
					json_data = json.loads(await resp.text())
				async with session.post(MANAGER_PLAYER_BASE_URL + '/get_all_head', data={'table': weapon}) as resp:
					data_tuple = json.loads(await resp.text())['remaining']
			if int(json_data["status"]) == 1:
				return self.message_typesetting(status=2, message="insufficient gold coins, upgrade failed")
			head = []
			for col in data_tuple:
				head.append(col[0])
			row = await self.__get_row_by_id(table_name=weapon, unique_id=unique_id)
			row[head.index("skill_point")] = row[head.index("weapon_level")]
			row[head.index("passive_skill_1_level")] = row[head.index("passive_skill_2_level")] = row[head.index("passive_skill_3_level")] = row[head.index("passive_skill_4_level")] = 0
			if await self.__set_skill_point(unique_id=unique_id, weapon=weapon, skill_point=str(row[head.index("skill_point")])) == 0:
				return self.message_typesetting(status=3, message="database operation error!")
			head[0] = "weapon"
			row[0] = weapon
			head.append("coin")
			row.append(json_data["remaining"])
			return self.message_typesetting(status=0, message=weapon + " reset skill point success!", data={"keys": head, "values": row})
	# levels up the weapon star. costs segments.
	# 升级武器星数。 成本是碎片。
	async def level_up_weapon_star(self, unique_id: str, weapon: str) -> dict:
		# - 0 - Weapon upgrade success
		# - 2 - insufficient gold coins, upgrade failed
		# - 3 - database operation error!
		async with ClientSession() as session:
			if self.__class__.__name__ == "PlayerManager":
				data_tuple = (await self.get_all_head(table=weapon))["remaining"]
			else:
				async with session.post(MANAGER_PLAYER_BASE_URL + '/get_all_head', data={'table': weapon}) as resp:
					data_tuple = json.loads(await resp.text())['remaining']
			head = []
			for col in data_tuple:
				head.append(col[0])
			row = await self.__get_row_by_id(table_name=weapon, unique_id=unique_id)
			weapon_star = await self.__get_weapon_star(unique_id=unique_id, weapon=weapon)
			segment_count = self._standard_segment_count * (1 + weapon_star)  # 根据武器星数增加碎片的消耗数量
			if row[head.index("segment")] < segment_count:
				return self.message_typesetting(status=2, message="insufficient segments, upgrade failed!")
			else:
				row[head.index("segment")] -= segment_count
				weapon_star += 1
				code1 = await self.__set_segment_by_id(unique_id=unique_id, weapon=weapon, segment=row[head.index("segment")])
				code2 = await self.__set_weapon_star(unique_id=unique_id, weapon=weapon, star=weapon_star)
				if code1 == 0 or code2 == 0:
					return self.message_typesetting(status=3, message="database operation error!")
				head[0] = "weapon"
				row[0] = weapon
				head.append("star")
				row.append(weapon_star)
				return self.message_typesetting(status=0, message=weapon + " upgrade success!", data={"keys": head, "values": row})
	# Get details of all weapons
	# Currently operating the database to get the weapon details, will not give a failure
	# 获取所有武器的详细信息
	# 目前操作数据库获取武器详细信息，不会给定失败的情况
	async def get_all_weapon(self, unique_id: str):
		# - 0 - gain success
		async with ClientSession() as session:
			if self.__class__.__name__ == "PlayerManager":
				data_tuple = (await self.get_all_head(table="weapon_bag"))["remaining"]
			else:
				async with session.post(MANAGER_PLAYER_BASE_URL + '/get_all_head', data={'table': "weapon_bag"}) as resp:
					data_tuple = json.loads(await resp.text())['remaining']
			col_name_list = []
			for col in data_tuple:
				col_name_list.append(col[0])
			print("col_name_list:" + str(col_name_list))
			weapons_stars_list = await self.__get_weapon_bag(unique_id=unique_id)
			# The 0 position stores the UNIQUE_ID, so the column header does not traverse the 0 position.
			# The 0 position obtained by the __get_weapon_attributes method below is also UNIQUE_ID.
			# So it will be replaced by the number of weapons stars.
			# 0位置存储unique_id，因此列标题不会遍历0位置。下面的__get_weapon_attributes方法获得的0位置也是unique_id，
			# 因此它将被武器星数替换。
			keys = []
			values = []
			for i in range(1, len(col_name_list)):
				# await self.__check_table(unique_id=unique_id, table=col_name_list[i])
				attribute_list = await self.__get_weapon_attributes(unique_id=unique_id, weapon=col_name_list[i])
				keys.append(col_name_list[i])
				attribute_list[0] = weapons_stars_list[i]
				values.append(attribute_list)
			return self.message_typesetting(status=0, message="gain success", data={"keys": keys, "values": values})
	async def try_unlock_weapon(self, unique_id: str, weapon: str) -> dict:
		# - 0 - Unlocked new weapon!   ===> {"keys": ["weapon"], "values": [weapon]}
		# - 0 - Weapon already unlocked, got free segment   ===>  {"keys": ['weapon', 'segment'], "values": [weapon, segment]}
		# - 1 - no weapon!
		try:
			star = await self.__get_weapon_star(unique_id, weapon)
			if star != 0:
				segment = await self.__get_segment(unique_id, weapon) + 30
				await self.__set_segment_by_id(unique_id, weapon, segment)
				return self.message_typesetting(status=0, message='Weapon already unlocked, got free segment!', data={"keys": ['weapon', 'segment'], "values": [weapon, segment]})
			await self.__set_weapon_star(unique_id, weapon, 1)
			return self.message_typesetting(status=0, message='Unlocked new weapon!', data={"keys": ["weapon"], "values": [weapon]})
		except:
			return self.message_typesetting(status=1, message='no weapon!')
	# Format the information
	# Get table properties, column headers
	# 获取表属性，列标题
	async def __get_col_name_list(self, table) -> list:
		sql_result = await self._execute_statement("desc " + table + ";")
		col_list = []
		for col in sql_result:
			col_list.append(col[0])
		return col_list
	# Get the content corresponding to the unique_id in the weapon backpack table.
	# This content is the star number of the weapon.
	# 获取武器背包表中unique_id对应的内容。
	# 这个内容是武器的星数。
	async def __get_weapon_bag(self, unique_id) -> list:
		sql_result = await self._execute_statement("select * from weapon_bag where unique_id='" + unique_id + "'")
		return list(sql_result[0])
	# Get the content corresponding to unique_id in the weapon table
	# This content is part of the weapon details
	# 获取武器表中unique_id对应的内容，此内容是武器的部分详细信息
	async def __get_weapon_attributes(self, unique_id, weapon) -> list:
		sql_result = await self._execute_statement("select * from " + weapon + " where unique_id='" + unique_id + "'")
		return list(sql_result[0])
	async def __get_weapon_info(self, unique_id, weapon) -> list:
		data = await self._execute_statement("select weapon_level, passive_skill_1_level, passive_skill_2_level, passive_skill_3_level, passive_skill_4_level, skill_point, segment from " + weapon + " where unique_id='" + unique_id + "';")
		return list(data[0])
	async def __set_skill_point(self, unique_id: str, weapon: str, skill_point: str) -> int:
		return await self._execute_statement_update("UPDATE " + weapon + " SET passive_skill_1_level=0, passive_skill_2_level=0, passive_skill_3_level=0, passive_skill_4_level=0, skill_point=" + skill_point + " where unique_id='" + unique_id + "'")
	async def __set_weapon_star(self, unique_id: str, weapon: str, star: int) -> int:
		return await self._execute_statement_update("UPDATE weapon_bag SET " + weapon + "=" + str(star) + " where unique_id='" + unique_id + "'")
	async def __get_weapon_star(self, unique_id: str, weapon: str) -> int:
		data = await self._execute_statement("SELECT " + weapon + " FROM weapon_bag WHERE unique_id='" + str(unique_id) + "'")
		return data[0][0]
	async def __set_material(self, unique_id: str, material: str, material_value: int) -> int:
		return await self._execute_statement_update("UPDATE player SET " + material + "=" + str(material_value) + " where unique_id='" + unique_id + "'")
	async def __get_material(self, unique_id: str, material: str) -> int:
		data = await self._execute_statement("SELECT " + material + " FROM player WHERE unique_id='" + str(unique_id) + "'")
		return data[0][0]
	async def __set_weapon_level_up_data(self, unique_id: str, weapon: str, weapon_level: int, skill_point: int):
		await self._execute_statement(
			"UPDATE `" + str(weapon) + "` SET weapon_level='" + str(weapon_level) + "', skill_point='" + str(
				skill_point) + "' WHERE unique_id='" + str(unique_id) + "';")
	async def __set_passive_skill_level_up_data(self, unique_id: str, weapon: str, passive_skill: str, skill_level: int, skill_points: int):
		await self._execute_statement(
			"UPDATE `" + str(weapon) + "` SET " + passive_skill + "='" + str(skill_level) + "', skill_point='" + str(
				skill_points) + "' WHERE unique_id='" + str(unique_id) + "';")
	async def __get_segment(self, unique_id: str, weapon: str) -> int:
		data = await self._execute_statement('SELECT segment FROM `' + weapon + '` WHERE unique_id = "' + unique_id + '";')
		return int(data[0][0])
	async def __set_segment_by_id(self, unique_id: str, weapon: str, segment: int):
		return await self._execute_statement_update(
			"UPDATE `" + str(weapon) + '` SET segment="' + str(segment) + '" WHERE unique_id="' + str(unique_id) + '";')
	async def __get_row_by_id(self, table_name: str, unique_id: str) -> list:
		data = await self._execute_statement("SELECT * FROM `" + str(table_name) + "` WHERE unique_id='" + str(unique_id) + "';")
		return list(data[0])
	# Used to check user records, create if they don't exist
	# 用于检查用户记录，如果不存在则创建
	async def __check_table(self, unique_id: str, table: str) -> None:
		if len(await self._execute_statement("select * from " + table + " where unique_id='" + unique_id + "'")) == 0:
			await self._execute_statement_update("INSERT INTO " + table + "(unique_id) VALUES ('" + unique_id + "')")
	# It is helpful to define a private method that you can simply pass
	# an SQL command as a string and it will execute. Call this method
	# whenever you issue an SQL statement.
	def __init__(self):
		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive.
		# 这是SQL服务器的连接池。 只要这个类还活着，这些连接就会保持打开状态。
		# TODO verify that this is true :D
		self.reward_list = self.__read_json_data()

		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive. 
		self._skill_tier_names = []
		self._skill_tier_weights = []
		self._skill_items = {}
		self._weapon_tier_names = []
		self._weapon_tier_weights = []
		self._weapon_items = {}
		self._read_lottery_configuration()
	

		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive. 
		self._recover_time = 10  # 10分钟恢复一点体力
		self._full_energy = 10

		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive. 
	
		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive.
		# 这是SQL服务器的连接池。 只要这个类还活着，这些连接就会保持打开状态。
		# TODO verify that this is true :D


		self._standard_iron_count = CONFIG['_01_Manager_Weapon']['standard_iron_count']
		self._standard_segment_count = CONFIG['_01_Manager_Weapon']['standard_segment_count']
		# Reset the amount of gold coins consumed by weapon skills
		self._standard_reset_weapon_skill_coin_count = CONFIG['_01_Manager_Weapon']['standard_reset_weapon_skill_coin_count']
		self._valid_passive_skills = CONFIG['_01_Manager_Weapon']['_valid_passive_skills']

		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive.
		# TODO verify that this is true :D

	# levels up a particular weapon. costs iron.
	# returns the data payload
		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive.
		self._pool = tormysql.ConnectionPool(max_connections = 10, host = '192.168.1.102', user = 'root', passwd = 'lukseun', db = 'aliya', charset = 'utf8')

	async def public_method(self) -> None:
		# Something interesting
		# await self._execute_statement('STATEMENT')
		pass

	async def _execute_statement(self, statement: str) -> tuple:
		"""
		Executes the given statement and returns the result.
		执行给定的语句并返回结果。
		:param statement: Mysql执行的语句
		:return: 返回执行后的二维元组表
		"""
		async with await self._pool.Connection() as conn:
			async with conn.cursor() as cursor:
				await cursor.execute(statement)
				data = cursor.fetchall()
				return data

	async def _execute_statement_update(self, statement: str) -> int:
		"""
		Execute the update or set statement and return the result.
		执行update或set语句并返回结果。
		:param statement: Mysql执行的语句
		:return: 返回update或者是set执行的结果
		"""
		async with await self._pool.Connection() as conn:
			async with conn.cursor() as cursor:
				return await cursor.execute(statement)

	def __internal_format(self, status: int, remaining: int or tuple or list) -> dict:
		"""
		Internal json formatted information
		内部json格式化信息
		:param status:状态标识0：成功，1：失败
		:param remaining:改变后的结果
		:return:json格式：{"status": status, "remaining": remaining}
		"""
		return {"status": status, "remaining": remaining}

	def message_typesetting(self, status: int, message: str, data: dict = {}) -> dict:
		"""
		Format the information
		:param message:说明语句
		:param data:json数据
		:return:返回客户端需要的json数据
		"""
		return {"status": status, "message": message, "random": random.randint(-1000, 1000), "data": data}



# Part (2 / 2)
MANAGER = PlayerManager()  # we want to define a single instance of the class
ROUTES = web.RouteTableDef()


# Call this method whenever you return from any of the following functions.
# This makes it very easy to construct a json response back to the caller.
def _json_response(body: dict = "", **kwargs) -> web.Response:
	'''
	A simple wrapper for aiohttp.web.Response return value.
	'''
	kwargs['body'] = json.dumps(body or kwargs['kwargs']).encode('utf-8')
	kwargs['content_type'] = 'text/json'
	return web.Response(**kwargs)


# Defines a function decorator that will require a valid token to be
# presented in the Authorization headers. To make a public facing API call
# required a valid token, put @login_required above the name of the function.
def login_required(fn):
	async def wrapper(request):
		async with ClientSession() as session:
			async with session.get('http://localhost:8080/validate', headers = {'authorization' : str(request.headers.get('authorization'))}) as resp:
				if resp.status == 200:
					return await fn(request)
		return _json_response({'message' : 'You need to be logged in to access this resource'}, status = 401)
	return wrapper


# Try running the server and then visiting http://localhost:[PORT]/public_method
@ROUTES.post('/try_coin')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_coin(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)
@ROUTES.post('/try_iron')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_iron(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)
@ROUTES.post('/try_diamond')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_diamond(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)
@ROUTES.post('/try_experience')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_experience(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)
@ROUTES.post('/try_level')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_level(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)
@ROUTES.post('/try_role')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_role(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)
@ROUTES.post('/try_stage')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_stage(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)
@ROUTES.post('/try_skill_scroll_10')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_skill_scroll_10(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)
@ROUTES.post('/try_skill_scroll_30')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_skill_scroll_30(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)
@ROUTES.post('/try_skill_scroll_100')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_skill_scroll_100(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)
@ROUTES.post('/try_experience_potion')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_experience_potion(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)
@ROUTES.post('/try_small_energy_potion')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_small_energy_potion(unique_id=post['unique_id'], value=int(post['value']))
	return _json_response(result)
@ROUTES.post('/try_all_material')
async def __try_all_material(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_all_material(unique_id=post['unique_id'], stage=int(post['stage']))
	return _json_response(result)
@ROUTES.post('/get_all_head')
async def __get_all_head(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.get_all_head(table=post["table"])
	return _json_response(result)
@ROUTES.post('/get_all_material')
async def __get_all_material(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.get_all_material(unique_id=post['unique_id'])
	return _json_response(result)
@ROUTES.post('/get_all_supplies')
async def __get_all_supplies(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.get_all_supplies(unique_id=post['unique_id'])
	return _json_response(result)
@ROUTES.post('/level_up_scroll')
async def __level_up_scroll(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.level_up_scroll(unique_id=post['unique_id'], scroll_id=post["scroll_id"])
	return _json_response(result)
@ROUTES.post('/add_supplies')
async def __add_supplies(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.add_supplies(unique_id=post['unique_id'], key=post["key"], value=int(post["value"]))
	return _json_response(result)
@ROUTES.post('/random_gift_skill')
async def __random_gift_skill(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.random_gift_skill(post['unique_id'])
	return _json_response(data)
@ROUTES.post('/random_gift_segment')
async def __random_gift_segment(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.random_gift_segment(post['unique_id'])
	return _json_response(data)
@ROUTES.post('/try_energy')
async def __decrease_energy(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.try_energy(post['unique_id'], int(post['amount']))
	return _json_response(data)
@ROUTES.post('/level_up_skill')
async def __get_all_skill_level(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.level_up_skill(post['unique_id'], post['skill_id'], post['scroll_id'])
	return _json_response(data)
@ROUTES.post('/get_all_skill_level')
async def __get_all_skill_level(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.get_all_skill_level(post['unique_id'])
	return _json_response(data)
@ROUTES.post('/get_skill')
async def __get_skill(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.get_skill(post['unique_id'], post['skill_id'])
	return _json_response(data)
@ROUTES.post('/try_unlock_skill')
async def __try_unlock_skill(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.try_unlock_skill(post['unique_id'], post['skill_id'])
	return _json_response(data)
@ROUTES.post('/pass_stage')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.pass_stage(unique_id=post['unique_id'], stage=int(post['stage']))
	return _json_response(result)
@ROUTES.post('/level_up_weapon')
async def __level_up_weapon(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.level_up_weapon(post['unique_id'], post['weapon'], int(post['iron']))
	return _json_response(data)
@ROUTES.post('/level_up_passive')
async def __level_up_passive(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.level_up_passive(post['unique_id'], post['weapon'], post['passive'])
	return _json_response(data)
@ROUTES.post('/reset_weapon_skill_point')
async def __reset_weapon_skill_point(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.reset_weapon_skill_point(post['unique_id'], post['weapon'])
	return _json_response(data)
@ROUTES.post('/level_up_weapon_star')
async def __level_up_weapon_star(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.level_up_weapon_star(post['unique_id'], post['weapon'])
	return _json_response(data)
@ROUTES.post('/get_all_weapon')
async def __get_all_weapon(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.get_all_weapon(post['unique_id'])
	return _json_response(data)
@ROUTES.post('/try_unlock_weapon')
async def __try_unlock_weapon(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.try_unlock_weapon(post['unique_id'], post['weapon'])
	return _json_response(data)
@ROUTES.get('/public_method')
async def __public_method(request: web.Request) -> web.Response:
	await MANAGER.public_method()
	return _json_response({'message' : 'asyncio code is awesome!'}, status = 200)


@ROUTES.get('/protected_method')
@login_required
async def __protected_method(request: web.Request) -> web.Response:
	return _json_response({'message' : 'if you can see this, you are logged in!!'})


def run(port):
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port=port)


if __name__ == '__main__':
	run(8004)
