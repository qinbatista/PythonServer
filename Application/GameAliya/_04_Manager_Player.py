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
import configparser
import tormysql
from aiohttp import web

CONFIG = configparser.ConfigParser()
CONFIG.read('./Configuration/server/1.0/server.conf')


import json
import random
import tormysql
import configparser
from aiohttp import web
from aiohttp import ClientSession

CONFIG = configparser.ConfigParser()
CONFIG.read('./Configuration/server/1.0/server.conf')

BAG_BASE_URL = CONFIG['_04_Manager_Player']['address'] + ':' + CONFIG['_04_Manager_Player']['port']
SKILL_BASE_URL = CONFIG['skill_manager']['address'] + ':' + CONFIG['skill_manager']['port']
WEAPON_BASE_URL = CONFIG['_01_Manager_Weapon']['address'] + ':' + CONFIG['_01_Manager_Weapon']['port']

SKILL_ID_LIST = ["m1_level", "p1_level", "g1_level", "m11_level", "m12_level", "m13_level", "p11_level", "p12_level", "p13_level", "g11_level", "g12_level", "g13_level", "m111_level", "m112_level", "m113_level", "m121_level", "m122_level", "m123_level", "m131_level", "m132_level", "m133_level", "p111_level", "p112_level", "p113_level", "p121_level", "p122_level", "p123_level", "p131_level", "p132_level", "p133_level", "g111_level", "g112_level", "g113_level", "g121_level", "g122_level", "g123_level", "g131_level", "g132_level", "g133_level"]

# Part (1 / 2)
import time
from datetime import datetime
import json
import random
import tormysql
import configparser
from aiohttp import web
from aiohttp import ClientSession

CONFIG = configparser.ConfigParser()
CONFIG.read('./Configuration/server/1.0/server.conf')

BAG_BASE_URL = CONFIG['_04_Manager_Player']['address'] + CONFIG['_04_Manager_Player']['port']


# Part (1 / 2)
import json
import random
import tormysql
import configparser
from aiohttp import web
from aiohttp import ClientSession

CONFIG = configparser.ConfigParser()
CONFIG.read('./Configuration/server/1.0/server.conf')

BAG_BASE_URL = CONFIG['_04_Manager_Player']['address'] + ':' + CONFIG['_04_Manager_Player']['port']


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
MANAGER_BAG_BASE_URL = CONFIG['_04_Manager_Player']['address'] + ":" + CONFIG['_04_Manager_Player']['port']
JSON_NAME = "./Configuration/client/1.0/stage_reward_config.json"


import json
import tormysql
import random
from aiohttp import web
from aiohttp import ClientSession


# Part (1 / 2)
class PlayerManager:
	async def get_all_head(self) -> dict:
		"""
		Used to get information such as the title of the database
		用于获取数据库的标题等信息
		:return:返回所有数据库的标题等信息，json数据
		"""
		data = await self._execute_statement("desc player;")
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
	async def set_all_material(self, statement: str) -> dict:
		"""
		Perform all material update operations
		执行所有材料的更新操作
		:param statement:mysql执行语句
		:return:返回json数据， status：0成功，1失败
		"""
		if ",unique_id=" in statement.replace(" ", "").lower() or "setunique_id=" in statement.replace(" ", "").lower():
			print("[set_all_material] -> mysql注入语句：" + statement)
			return self.__internal_format(status=1, remaining=statement)
		data = await self._execute_statement_update(statement=statement)
		data = 1 - data  # 0, 1反转
		return self.__internal_format(status=data, remaining=data)
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
		return self.__internal_format(0, num)
	async def try_coin(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="coin", value=value)
	async def try_iron(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="iron", value=value)
	async def try_diamond(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="diamond", value=value)
	async def try_energy(self, unique_id: str, value: int) -> dict:
		return await self.__try_material(unique_id=unique_id, key="energy", value=value)
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
	def __internal_format(self, status: int, remaining: int or tuple) -> dict:
		"""
		Internal json formatted information
		内部json格式化信息
		:param status:状态标识0：成功，1：失败
		:param remaining:改变后的结果
		:return:json格式：{"status": status, "remaining": remaining}
		"""
		return {"status": status, "remaining": remaining}
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
			status = data["status"]
			if data['status'] == 1:  # skill already unlocked
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
					return self.message_typesetting(status=0, message='you received a free scroll', data={'skill_scroll_id': skill_scroll_id, 'value': data["remaining"]})
				return self.message_typesetting(status=3, message='database operation error')
			elif status == 0:  # success
				return self.message_typesetting(status=status, message=data['remaining'][status], data={"skill_id": gift_skill, "value": 1})
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
						return self.message_typesetting(status=0, message='you received a free scroll', data={'skill_scroll_id': skill_scroll_id, 'value': json_data["remaining"]})
					return self.message_typesetting(status=3, message='database operation error')
				elif status == 0:  # success
					return self.message_typesetting(status=status, message=data['remaining'][status], data={"skill_id": gift_skill, "value": 1})
				else:  # 2
					return self.message_typesetting(status=status, message=data['remaining'][status])
	async def random_gift_segment(self, unique_id: str) -> dict:
		tier_choice = (random.choices(self._weapon_tier_names, self._weapon_tier_weights))[0]
		gift_weapon = (random.choices(self._weapon_items[tier_choice]))[0]
		async with ClientSession() as session:
			async with session.post(WEAPON_BASE_URL + '/try_unlock_weapon', data = {'unique_id' : unique_id, 'weapon' : gift_weapon}) as resp:
				return await resp.json(content_type = 'text/json')
			####################################
			#          P R I V A T E		   #
			####################################
		
	def _read_lottery_configuration(self, conf: str = './Configuration/server/1.0/lottery.conf'):
		config = configparser.ConfigParser()
		config.read(conf)
		self._skill_tier_names = eval(config['skills']['names'])
		self._skill_tier_weights = eval(config['skills']['weights'])
		self._skill_items = eval(config['skills']['items'])
		self._weapon_tier_names = eval(config['weapons']['names'])
		self._weapon_tier_weights = eval(config['weapons']['weights'])
		self._weapon_items = eval(config['weapons']['items'])
			
		
	# It is helpful to define a private method that you can simply pass
	# an SQL command as a string and it will execute. Call this method
	# whenever you issue an SQL statement.
	async def try_energy(self, unique_id: str, amount: int) -> dict:
		if amount > 0:
			return await self._decrease_energy(unique_id, -1 * amount)
		elif amount < 0:
			return await self._decrease_energy(unique_id, amount)
		else:
			energy, last_time = await self._get_energy_information(unique_id)
			return self.message_typesetting(0, 'success', {'energy' : energy, 'recover_time' : last_time})
			####################################
			#          P R I V A T E		   #
			####################################
	async def _decrease_energy(self, unique_id: str, amount: int) -> dict:
		current_energy, recover_time = await self._get_energy_information(unique_id)
		if recover_time == '':
			if current_energy - amount > self._full_energy:
				await self._execute_statement('UPDATE player SET energy = "' + str(current_energy - amount) + '", recover_time = "" WHERE unique_id = "' + unique_id + '";')
				return self.message_typesetting(0, 'decrease success, remaining energy is over full energy, removed recover time', {'energy' : current_energy - amount})
			elif current_energy - amount == self._full_energy:
				await self._execute_statement('UPDATE player SET energy = "' + str(current_energy - amount) + '", recover_time = "' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '" WHERE unique_id = "' + unique_id + '";')
				return self.message_typesetting(0, 'decrease success, remaining energy full, recovering energy', {'energy' : current_energy - amount})
			else:
				await self._execute_statement('UPDATE player SET energy = "' + str(current_energy - amount) + '", recover_time = "' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '" WHERE unique_id = "' + unique_id + '";')
				return self.message_typesetting(0, 'decrease success, start recovering energy', {'energy' : current_energy - amount})
		else:
			delta_time = datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), '%Y-%m-%d %H:%M:%S') - datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S')
			recovered_energy = int(delta_time.seconds / 60 / 20)
			if recovered_energy + current_energy - amount >= 0:
				if recovered_energy + current_energy - amount > 10:
					await self._execute_statement('UPDATE player SET energy = "' + str(10 - amount) + '", recover_time = "" WHERE unique_id = "' + unique_id + '";')
					return self.message_typesetting(0, 'energy over full energy, remove record time', {'energy' : 10 - amount})
				else:
					await self._execute_statement('UPDATE player SET energy = "' + str(recovered_energy + current_energy - amount) + '", recover_time = "' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '" WHERE unique_id = "' + unique_id + '";')
					return self.message_typesetting(0, 'success, recovering energy', {'energy' : recovered_energy + current_energy - amount})
		return self.message_typesetting(1, 'energy error')
	async def _get_energy_information(self, unique_id: str) -> tuple:
		data = await self._execute_statement('SELECT energy, recover_time FROM player WHERE unique_id = "' + unique_id + '";')
		return (data[0][0], data[0][1])
		
		
	# It is helpful to define a private method that you can simply pass
	# an SQL command as a string and it will execute. Call this method
	# whenever you issue an SQL statement.
	async def level_up_skill(self, unique_id: str, skill_id: str, scroll_id: str) -> dict:
		# 0 - Success
		# 1 - User does not have that skill
		# 4 - User does not have enough scrolls
		# 9 - Skill already at max level
		skill_level = await self._get_skill_level(unique_id, skill_id)
		if skill_level == 0:
			return self.message_typesetting(1, 'User does not have that skill')
		if skill_level >= 10:
			return self.message_typesetting(9, 'Skill already max level')
		if self.__class__.__name__ == 'PlayerManager':
			fn = {'skill_scroll_10' : self.try_skill_scroll_10, 'skill_scroll_30' : self.try_skill_scroll_30, 'skill_scroll_100' : self.try_skill_scroll_100}
			f = fn[scroll_id]
			resp = await f(unique_id, -1)
			scroll_quantity = resp['remaining']
		else:
			async with ClientSession() as session:
				async with session.post(BAG_BASE_URL + '/try_'+scroll_id, data = {'unique_id' : unique_id, 'value' : -1}) as resp:
					resp = await resp.json(content_type='text/json')
					if resp['status'] == 1:
						return self.message_typesetting(4, 'User does not have enough scrolls')
					scroll_quantity = resp['remaining']
			
		if not await self._roll_for_upgrade(scroll_id):
			return self.message_typesetting(0, 'success', {'skill1' : [skill_id, skill_level], 'item1' : [scroll_id, scroll_quantity], 'upgrade' : '1'})
		await self._execute_statement('UPDATE skill SET `' + skill_id + '` = ' + str(skill_level + 1) + ' WHERE unique_id = "' + unique_id + '";')
		return self.message_typesetting(0, 'success', {'skill1' : [skill_id, skill_level + 1], 'item1' : [scroll_id, scroll_quantity], 'upgrade' : '0'})
			
	async def get_all_skill_level(self, unique_id: str) -> dict:
		# 0 - Success
		names = await self._execute_statement('DESCRIBE skill;')
		values = await self._execute_statement('SELECT * from skill WHERE unique_id = "' + str(unique_id) + '";')
		data = {}
		for num, val in enumerate(zip(names[1:], values[0][1:])):
			data['skill' + str(num + 1)] = [ val[0][0] , val[1] ]
		return self.message_typesetting(0, 'success', data)
	async def get_skill(self, unique_id: str, skill_id: str) -> dict:
		# 0 - Success
		# 1 - invalid skill name
		try:
			level = await self._get_skill_level(unique_id, skill_id)
			return self.message_typesetting(0, 'success', {'skill': skill_id, 'value': level})
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
			if level == 0 and await self._execute_statement_update('UPDATE skill SET `' + skill_id + '` = 1 WHERE unique_id = "' + unique_id + '";') == 0:
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
	def __internal_format(self, status: int, remaining: int or tuple) -> dict:
		"""
		Internal json formatted information
		内部json格式化信息
		:param status:状态标识0：成功，1：失败
		:param remaining:改变后的结果
		:return:json格式：{"status": status, "remaining": remaining}
		"""
		return {"status": status, "remaining": remaining}
	async def pass_stage(self, unique_id: str, stage_client: int) -> dict:
		reward_list = self.__read_json_data()
		print("reward_list:" + str(reward_list))
		async with ClientSession() as session:
			if self.__class__.__name__ == "StageSystemClass":
				async with session.post(MANAGER_BAG_BASE_URL + '/get_all_head') as resp:
					data_head_tuple = json.loads(await resp.text())["remaining"]
				async with session.post(MANAGER_BAG_BASE_URL + '/get_all_material', data={'unique_id': unique_id}) as resp:
					content_tuple = json.loads(await resp.text())["remaining"]
			else:
				data_head_tuple = (await self.get_all_head())["remaining"]
				content_tuple = (await self.get_all_material(unique_id=unique_id))["remaining"]
			head_list, format_list = self.__get_head_list(data_head_tuple=data_head_tuple)
			item_dict = self.__structure_item_dict(head_list, content_tuple)
			if stage_client <= 0 or (item_dict["stage"] + 1) < stage_client:
				return self.message_typesetting(9, "abnormal data!")
			# 改变所有该变的变量
			if item_dict["stage"] + 1 == stage_client:  # 通过新关卡
				item_dict["stage"] = stage_client
			reward_data = reward_list[stage_client]  # 获得奖励
			reward_data_len = len(reward_data.keys()) + 1
			data = self.__structure_data(reward_data=reward_data, item_dict=item_dict, reward_data_len=reward_data_len)
			sql_str = self.__sql_str_operating(unique_id=unique_id, table_name="player", head_list=head_list, format_list=format_list, item_dict=item_dict)
			if self.__class__.__name__ == "StageSystemClass":
				async with session.post(MANAGER_BAG_BASE_URL + '/set_all_material', data={"statement": sql_str}) as resp:
					sql_result = json.loads(await resp.text())
			else:
				sql_result = await self.set_all_material(statement=sql_str)
			if int(sql_result["status"]) == 1:
				return self.message_typesetting(1, "abnormal data!")
			return self.message_typesetting(0, "passed customs!", data=data)
	def __read_json_data(self) -> list:
		data = []
		if os.path.exists(JSON_NAME):
			data_dict = json.load(open(JSON_NAME, encoding="utf-8"))
			for key in data_dict.keys():
				data.append(data_dict[key])
		print("[stage_module.py][read_json_data] -> data:" + str(data))
		return data
	def __get_head_list(self, data_head_tuple: tuple) -> (list, list):
		"""
		获取到列标题列表
		获取构造mysql语句的单字符
		:param data_head_tuple:二维元组
		:return:列标题列表，格式列表
		"""
		head_list = []
		format_list = []
		for col in data_head_tuple:
			head_list.append(col[0])
			format_list.append(format_sql[col[1][:col[1].find("(")]])  # 将smallint(6)截取出smallint，然后用标准转换成字符，用于后面替换成sql的替换
		return head_list, format_list
	def __structure_data(self, reward_data: dict, item_dict: dict, reward_data_len: int) -> dict:
		"""
		构造一个返回给客户端的通关奖励与设置字典，包含奖励与设置项
		:param reward_data:奖励的字典
		:param item_dict:所有的字段对应的字典
		:param reward_data_len:奖励的字典的长度
		:return:返回的是一个字典，包含奖励与设置
		"""
		temp_list = []
		data = {}
		for key in reward_data.keys():
			temp_list.append(reward_data[key])  # [key, value]
		for i in range(1, reward_data_len):
			reward = "reward" + str(i)
			data.update({reward: temp_list[i - 1]})
		for i in range(1, reward_data_len):
			reward = "reward" + str(i)
			key = data[reward][0]
			item_dict[key] += data[reward][1]
			data.update({"item" + str(i): [key, item_dict[key]]})
		data.update({"item" + str(reward_data_len): ["stage", item_dict["stage"]]})
		return data
	def __structure_item_dict(self, head_list, content_tuple) -> dict:
		item_dict = {}
		for i in range(len(head_list)):
			item_dict.update({head_list[i]: content_tuple[i]})
		return item_dict
	def __sql_str_operating(self, unique_id: str, table_name: str, head_list: list, format_list: list, item_dict: dict) -> str:
		heard_str = "UPDATE %s SET " % table_name
		end_str = " where unique_id='%s'" % unique_id
		result_str = ""
		temp_list = []
		for i in range(len(head_list)):
			if head_list[i] != "unique_id":
				temp_list.append(item_dict[head_list[i]])
				if i != len(head_list) - 1:
					result_str += head_list[i] + "=%s, " % format_list[i]
				else:
					result_str += head_list[i] + "=%s" % format_list[i]
		result_str = heard_str + result_str + end_str
		print("[StageSystemClass][__sql_str_operating] -> result_str:" + result_str)
		print("[StageSystemClass][__sql_str_operating] -> temp_list:" + str(temp_list))
		return result_str % tuple(temp_list)
	def __init__(self):
		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive.
		self._pool = tormysql.ConnectionPool(max_connections = 10, host = '192.168.1.102', user = 'root', passwd = 'lukseun', db = 'aliya', charset = 'utf8')
		self._skill_tier_names = []
		self._skill_tier_weights = []
		self._skill_items = {}
		self._weapon_tier_names = []
		self._weapon_tier_weights = []
		self._weapon_items = {}
		self._read_lottery_configuration()
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

	def __internal_format(self, status: int, remaining: int or tuple) -> dict:
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
@ROUTES.post('/try_energy')
async def __try_coin(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.try_energy(unique_id=post['unique_id'], value=int(post['value']))
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
@ROUTES.post('/get_all_head')
async def __get_all_head(request: web.Request) -> web.Response:
	result = await MANAGER.get_all_head()
	return _json_response(result)
@ROUTES.post('/get_all_material')
async def __get_all_material(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.get_all_material(unique_id=post['unique_id'])
	return _json_response(result)
@ROUTES.post('/set_all_material')
async def __set_all_material(request: web.Request) -> web.Response:
	post = await request.post()
	result = await MANAGER.set_all_material(statement=post['statement'])
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
	result = await MANAGER.pass_stage(unique_id=post['unique_id'], stage_client=int(post['stage']))
	return _json_response(result)
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
