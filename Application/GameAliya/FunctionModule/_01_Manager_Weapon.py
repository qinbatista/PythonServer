#
# WeaponManager.py
#
###############################################################################


import json
import os
import random
import tormysql
import configparser
from aiohttp import web
from aiohttp import ClientSession


CONFIG = configparser.ConfigParser()
CONFIG.read('../../Configuration/server/1.0/server.conf')
MANAGER_PLAYER_BASE_URL = CONFIG['_04_Manager_Game']['address'] + ":" + CONFIG['_04_Manager_Game']['port']


class WeaponUpgradeError(Exception):
	def __init__(self, code: int, message: str = ''):
		self.code = code
		self.message = message


class WeaponManager:
	def __init__(self, standard_iron_count=20, standard_segment_count=30, standard_reset_weapon_skill_coin_count=100):
		self._standard_iron_count = standard_iron_count
		self._standard_segment_count = standard_segment_count
		# Reset the amount of gold coins consumed by weapon skills
		self._standard_reset_weapon_skill_coin_count = standard_reset_weapon_skill_coin_count

		self._valid_passive_skills = ['passive_skill_1_level', 'passive_skill_2_level', 'passive_skill_3_level', 'passive_skill_4_level']

		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive.
		# TODO verify that this is true :D
		self._pool = tormysql.ConnectionPool(max_connections=10, host='192.168.1.102', user='root', passwd='lukseun', db='aliya', charset='utf8')

	# levels up a particular weapon. costs iron.
	# returns the data payload
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
	def message_typesetting(self, status: int, message: str, data: dict = {}) -> dict:
		return {"status": status, "message": message, "random": random.randint(-1000, 1000), "data": data}








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
	async def _execute_statement(self, statement: str) -> tuple:
		'''
		Executes the given statement and returns the result.
		执行给定的语句并返回结果。
		'''
		async with await self._pool.Connection() as conn:
			async with conn.cursor() as cursor:
				await cursor.execute(statement)
				data = cursor.fetchall()
				return data

	async def _execute_statement_update(self, statement: str) -> int:
		'''
		Execute the update or set statement and return the result.
		执行update或set语句并返回结果。
		'''
		async with await self._pool.Connection() as conn:
			async with conn.cursor() as cursor:
				return await cursor.execute(statement)


# Part (2 / 2)
MANAGER = WeaponManager()  # we want to define a single instance of the class
ROUTES = web.RouteTableDef()


# Call this method whenever you return from any of the following functions.
# This makes it very easy to construct a json response back to the caller.
def _json_response(body: dict = '', **kwargs) -> web.Response:
	'''
	A simple wrapper for aiohttp.web.Response return value.
	'''
	kwargs['body'] = json.dumps(body or kwargs['kwargs']).encode('utf-8')
	kwargs['content_type'] = 'text/json'
	return web.Response(**kwargs)


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


def run(port):
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port=port)


if __name__ == '__main__':
	run(8001)
