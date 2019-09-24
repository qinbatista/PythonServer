'''
common.py

Contains definitions of global enums as well as commonly used generic functions.
When desinging a function, try to make it as general as possible to allow the reuse of code.
'''

import enum

class Item(enum.IntEnum):
	COIN = 1
	IRON = 2
	FOOD = 3
	CRYSTAL = 4
	DIAMOND = 5
	SKILL_SCROLL_10 = 6
	SKILL_SCROLL_30 = 7
	SKILL_SCROLL_100 = 8
	EXPERIENCE_POTION = 9
	ENERGY_POTION_S = 10
	SUMMON_SCROLL_BASIC = 11
	SUMMON_SCROLL_PRO = 12
	SUMMON_SCROLL_PROPHET = 13
	FORTUNE_WHEEL_BASIC = 14
	FORTUNE_WHEEL_PRO = 15

##############################################################################

'''
try_item provides a single interface to query, and modify any player item.
it has three modes: check, add, remove
check:	access this mode by setting value parameter to 0
		returns a tuple containing True and the current value of that item

add:	access this mode by setting value parameter to a positive number
		returns a tuple containing True and the resulting value after adding value to it

remove:	access this mode by setting value parameter to a negative number
'''
async def try_item(uid, item, value, **kwargs):
	pass

async def exists(table, identifier, value, *, db = 'worlddb', **kwargs):
	data = await execute(f'SELECT EXISTS (SELECT 1 FROM {table} WHERE {identifier} = "{value}");', kwargs[db])
	if data == () or () in data: return False
	return data[0][0] != 0

async def execute(statement, pool):
	async with pool.acquire() as conn:
		async with conn.cursor() as cursor:
			await cursor.execute(statement)
			return await cursor.fetchall()

def mt(status, message, data = {}):
	return {'status' : status, 'message' : message, 'data' : data}
