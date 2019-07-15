#
# WeaponManager.py
#
###############################################################################


import json
import random

import tormysql
from aiohttp import web
from aiohttp import ClientSession

BAG_MANAGER_BASE_URL = 'http://localhost:8082'


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
	async def level_up_weapon(self, unique_id: str, weapon: str, iron: int) -> str:
		async with ClientSession() as session:
			star = await self._get_weapon_star(unique_id, weapon)
			if star == 0:
				return await self.message_typesetting(1, "user does not have that weapon")

			row = await self._get_row_by_id(weapon, unique_id)

			if row[1] == 100:
				return await self.message_typesetting(3, "weapon has reached max level")  # 9 --> 3

			async with session.post(BAG_MANAGER_BASE_URL + '/get_iron', data={'unique_id': unique_id}) as resp:
				resp = await resp.json(content_type='text/json')
				current_iron = resp['iron']

			skill_upgrade_number = int(iron) // self._standard_iron_count
			if skill_upgrade_number == 0 or (current_iron // self._standard_iron_count) < skill_upgrade_number:
				return await self.message_typesetting(2, "insufficient materials, upgrade failed")

			# calculate resulting levels and used iron
			if (row[1] + skill_upgrade_number) > 100:
				skill_upgrade_number = 100 - row[1]
			row[1] += skill_upgrade_number
			row[6] += skill_upgrade_number

			# remove the iron from the account
			async with session.post(BAG_MANAGER_BASE_URL + '/remove_iron', data={'unique_id': unique_id, 'amount': self._standard_iron_count * skill_upgrade_number}) as resp:
				resp = await resp.json(content_type='text/json')
				remaining_iron = resp['remaining']

			# update the weapon level on the account
			await self.__set_weapon_level_up_data(unique_id, weapon, row[1], row[6])
			return await self.message_typesetting(0, "success", data={'weapon_bag1': row, 'item1': ['iron', remaining_iron]})

	# levels up a particular passive skill. costs skill points.
	# 提升特定的被动技能。 增加技能点。
	async def level_up_passive(self, unique_id: str, weapon: str, passive_skill: str) -> str:
		weapon_star = await self.__get_weapon_star(unique_id, weapon)
		if weapon_star == 0:
			return await self.message_typesetting(1, "user does not have that weapon")

		if passive_skill not in self._valid_passive_skills:
			return await self.message_typesetting(9, "passive skill does not exist")

		row = await self._get_row_by_id(weapon, unique_id)
		if row[6] == 0:
			return await self.message_typesetting(2, "insufficient skill points, upgrade failed")
		row[6] -= 1
		row[2 + self._valid_passive_skills.index(passive_skill)] += 1
		await self._set_passive_skill_level_up_data(unique_id, weapon, passive_skill, row[2 + self._valid_passive_skills.index(passive_skill)], row[6])
		row[0] = weapon
		return await self.message_typesetting(0, "success", data={"weapon_bag1": row})

	# resets all weapon passive skill points. refunds all skill points back. costs coins.
	async def reset_weapon_skill_point(self, unique_id: str, weapon: str) -> str:
		async with ClientSession() as session:
			# get the coin from the account
			async with session.post(BAG_MANAGER_BASE_URL + '/get_coin', data={"unique_id": unique_id}) as resp:
				resp = await resp.json(content_type='text/json')
				bag_coin = resp["coins"]
			info_list = await self._get_row_by_id(weapon, unique_id)
			if self.__get_weapon_star(unique_id=unique_id, weapon=weapon) == 0:
				return await self.message_typesetting(1, "no weapon!")
			elif bag_coin < self._standard_reset_weapon_skill_coin_count:
				return await self.message_typesetting(4, "there is not enough gold coins to reset!")  # 9 --> 4
			else:
				info_list[6] = info_list[0]
				info_list[2] = info_list[3] = info_list[4] = info_list[5] = 0
				bag_coin -= self._standard_reset_weapon_skill_coin_count
				coin_result = await self.__set_coin(bag_coin)
				weapon_result = await self.__set_skill_point(unique_id, weapon, skill_point=info_list[6])
				if coin_result == 0 or weapon_result == 0:
					return await self.message_typesetting(3, "abnormal data!")
				info_list[0] = weapon
				return await self.message_typesetting(0, weapon + " reset skill point success!", data={"weapon_bag1": info_list, "item1": ["coin", bag_coin]})

	# levels up the weapon star. costs segments.
	async def level_up_weapon_star(self, unique_id: str, weapon: str):
		pass

	async def __get_weapon_info(self, unique_id, weapon) -> list:
		data = await self._execute_statement("select weapon_level, passive_skill_1_level, passive_skill_2_level, passive_skill_3_level, passive_skill_4_level, skill_point, segment from " + weapon + " where unique_id='" + unique_id + "';")
		return list(data[0])

	async def __set_skill_point(self, unique_id, weapon_kind, skill_point) -> int:
		return await self._execute_statement_update("UPDATE " + weapon_kind + " SET passive_skill_1_level=0, passive_skill_2_level=0, passive_skill_3_level=0, passive_skill_4_level=0, skill_point=" + str(skill_point) + " where unique_id='" + unique_id + "'")

	async def __set_coin(self, coin) -> int:
		return await self._execute_statement_update("UPDATE bag SET coin=" + str(coin) + " where unique_id='" + self.unique_id + "'")

	async def __get_weapon_star(self, unique_id: str, weapon: str) -> int:
		data = await self._execute_statement("SELECT " + weapon + " FROM weapon_bag WHERE unique_id='" + str(unique_id) + "'")
		return data[0][0]

	async def __set_weapon_level_up_data(self, unique_id: str, weapon: str, weapon_level: int, skill_point: int):
		await self._execute_statement(
			"UPDATE `" + str(weapon) + "` SET weapon_level='" + str(weapon_level) + "', skill_point='" + str(
				skill_point) + "' WHERE unique_id='" + str(unique_id) + "';")

	async def _set_passive_skill_level_up_data(self, unique_id: str, weapon: str, passive_skill: str, skill_level: int, skill_points: int):
		await self._execute_statement(
			"UPDATE `" + str(weapon) + "` SET " + passive_skill + "='" + str(skill_level) + "', skill_point='" + str(
				skill_points) + "' WHERE unique_id='" + str(unique_id) + "';")

	async def _get_row_by_id(self, table_name: str, unique_id: str) -> list:
		data = await self._execute_statement("SELECT * FROM `" + str(table_name) + "` WHERE unique_id='" + str(unique_id) + "';")
		return list(data[0])

	# Format the information
	async def message_typesetting(self, status: int, message: str, data: dict=None) -> str:
		result = '{"status":"%s","message":"%s","random":"%s","data":{}}' % (
		status, message, str(random.randint(-1000, 1000)))
		# 分段保存字符串
		if data: result = result.replace("{}", json.dumps(data))
		return result

	# It is helpful to define a private method that you can simply pass
	# an SQL command as a string and it will execute. Call this method
	# whenever you issue an SQL statement.
	async def _execute_statement(self, statement: str) -> tuple:
		'''
		Executes the given statement and returns the result.
		'''
		async with await self._pool.Connection() as conn:
			async with conn.cursor() as cursor:
				await cursor.execute(statement)
				data = cursor.fetchall()
				return data

	async def _execute_statement_update(self, statement: str) -> int:
		'''
		Executes the given statement and returns the result.
		'''
		async with await self._pool.Connection() as conn:
			async with conn.cursor() as cursor:
				data = await cursor.execute(statement)
				return data

# Part (2 / 2)
MANAGER = WeaponManager()  # we want to define a single instance of the class
ROUTES = web.RouteTableDef()


# Call this method whenever you return from any of the following functions.
# This makes it very easy to construct a json response back to the caller.
def _json_response(body: str = '', **kwargs) -> web.Response:
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


def run(port):
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port)


if __name__ == '__main__':
	run(8001)
