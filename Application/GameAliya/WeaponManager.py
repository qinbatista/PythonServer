#
# WeaponManager.py
#
###############################################################################


import json
import tormysql
from aiohttp import web
from aiohttp import ClientSession

BAG_MANAGER_BASE_URL = 'http://localhost:8082'



class WeaponUpgradeError(Exception):
	def __init__(self, code: int, message: str = ''):
		self.code = code
		self.message = message


class WeaponManager:
	def __init__(self, standard_iron_count = 20, standard_segment_count = 30):
		self._standard_iron_count = standard_iron_count
		self._standard_segment_count = standard_segment_count

		self._valid_passive_skills = ['passive_skill_1_level', 'passive_skill_2_level', 'passive_skill_3_level', 'passive_skill_4_level']

		# This is the connection pool to the SQL server. These connections stay open
		# for as long as this class is alive. 
		# TODO verify that this is true :D
		self._pool = tormysql.ConnectionPool(max_connections = 10, host = '127.0.0.1', user = 'root', passwd = 'lukseun', db = 'aliya', charset = 'utf8')


	# levels up a particular weapon. costs iron.
	# returns the data payload
	async def level_up_weapon(self, unique_id: str, weapon: str, iron: int) -> dict:
		async with ClientSession() as session:
			star = await self._get_weapon_star(unique_id, weapon)
			if star == 0:
				return {'status' : 1, 'message' : 'user does not have that weapon', 'data' : {}}

			row = await self._get_row_by_id(weapon, unique_id)

			if row[1] == 100:
				return {'status' : 9, 'message' : 'weapon has reached max level', 'data' : {}}

			async with session.post(BAG_MANAGER_BASE_URL + '/get_iron', data = {'unique_id' : unique_id}) as resp:
				resp = await resp.json(content_type='text/json')
				current_iron = resp['iron']
			skill_upgrade_number = int(iron) // self._standard_iron_count
			if skill_upgrade_number == 0 or (current_iron // self._standard_iron_count) < skill_upgrade_number:
				return {'status' : 2, 'message' : 'insufficient materials, upgrade failed', 'data' : {}}

			# calculate resulting levels and used iron
			if (row[1] + skill_upgrade_number) > 100:
				skill_upgrade_number = 100 - row[1]
			row[1] += skill_upgrade_number
			row[6] += skill_upgrade_number

			# remove the iron from the account
			async with session.post(BAG_MANAGER_BASE_URL + '/remove_iron', data = {'unique_id' : unique_id, 'amount' : self._standard_iron_count * skill_upgrade_number}) as resp:
				resp = await resp.json(content_type='text/json')
				remaining_iron = resp['remaining']

			# update the weapon level on the account
			await self._set_weapon_level_up_data(unique_id, weapon, row[1], row[6])
			return {'status' : 0, 'message' : 'success', 'data' : {'weapon_bag1' : row, 'item1' : ['iron', remaining_iron]}}


	# levels up a particular passive skill. costs skill points.
	async def level_up_passive(self, unique_id: str, weapon: str, passive_skill: str) -> dict:
		weapon_star = await self._get_weapon_star(unique_id, weapon)
		if weapon_star == 0:
			return {'status' : 1, 'message' : 'user does not have that weapon', 'data' : {}}

		if passive_skill not in self._valid_passive_skills:
			return {'status' : 9, 'message' : 'passive skill does not exist', 'data' : {}}

		row = await self._get_row_by_id(weapon, unique_id)

		if row[6] <= 0:
			return {'status' : 2, 'message' : 'insufficient skill points, upgrade failed', 'data' : {}}
		row[6] -= 1
		row[2 + self._valid_passive_skills.index(passive_skill)] += 1

		await self._set_passive_skill_level_up_data(unique_id, weapon, passive_skill, row[2 + self._valid_passive_skills.index(passive_skill)], row[6])
		return {'status' : 0, 'message' : 'success', 'data' : {'weapon_bag1' : row}}


	# resets all weapon passive skill points. refunds all skill points back. costs coins.
	async def reset_weapon_skill_points(self, unique_id: str, weapon: str):
		pass

	# levels up the weapon star. costs segments.
	async def level_up_weapon_star(self, unique_id: str, weapon: str):
		pass







	async def _get_weapon_star(self, unique_id: str, weapon: str) -> int:
		data = await self._execute_statement("SELECT `" + str(weapon) + "` FROM weapon_bag WHERE unique_id='" + str(unique_id) + "';")
		if () in data or data == None:
			return 0
		return data[0][0]

	async def _set_weapon_level_up_data(self, unique_id: str, weapon: str, weapon_level: int, skill_point: int):
		await self._execute_statement("UPDATE `" + str(weapon) + "` SET weapon_level='" + str(weapon_level) + "', skill_point='" + str(skill_point) + "' WHERE unique_id='" + str(unique_id) + "';")


	async def _set_passive_skill_level_up_data(self, unique_id: str, weapon: str, passive_skill: str, skill_level: int, skill_points: int):
		await self._execute_statement("UPDATE `" + str(weapon) + "` SET " + passive_skill + "='" + str(skill_level) + "', skill_point='" + str(skill_points) + "' WHERE unique_id='" + str(unique_id) + "';")

	async def _get_row_by_id(self, table_name: str, unique_id: str) -> list:
		data = await self._execute_statement("SELECT * FROM `" + str(table_name) + "` WHERE unique_id='" + str(unique_id) + "';")
		if () in data: # this should never happen
			return None
		return list(data[0])



	

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



# Part (2 / 2)
MANAGER = WeaponManager() # we want to define a single instance of the class
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
	data = await MANAGER.level_up_weapon(post['unique_id'], post['weapon'], post['iron'])
	return _json_response(data)


@ROUTES.post('/level_up_passive')
async def __level_up_passive(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.level_up_passive(post['unique_id'], post['weapon'], post['passive'])
	return _json_response(data)




def run(port: int):
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port = port)


if __name__ == '__main__':
	run(8083)
