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


class FamilyRole(enum.IntEnum):
	BASIC = 0
	ELITE = 4
	ADMIN = 8
	OWNER = 10

class MailType(enum.IntEnum):
	SIMPLE = 0
	GIFT = 1
	FRIEND_REQUEST = 2
	FAMILY_REQUEST = 3


##############################################################################

async def try_item(uid, item, value, **kwargs):
	async with (await get_db(**kwargs)).acquire() as conn:
		# await conn.select_db()
		async with conn.cursor() as cursor:
			await cursor.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = "{item.value}" FOR UPDATE;')
			quantity = await cursor.fetchall()
			if value >= 0 or quantity[0][0] + value >= 0:
				await cursor.execute(f'UPDATE item SET value = value + {value} WHERE uid = "{uid}" AND iid = "{item.value}";')
				return (True, quantity[0][0] + value)
			return (False, quantity[0][0] + value)


async def exists(table, identifier, value, *, account = False, **kwargs):
	data = await execute(f'SELECT EXISTS (SELECT 1 FROM {table} WHERE {identifier} = "{value}");', account, **kwargs)
	if data == () or () in data: return False
	return data[0][0] != 0

async def execute(statement, account = False, **kwargs):
	async with ((await get_db(**kwargs)).acquire() if not account else kwargs['accountdb'].acquire()) as conn:
		# await conn.select_db()
		async with conn.cursor() as cursor:
			await cursor.execute(statement)
			return await cursor.fetchall()

async def get_db(**kwargs):
	return kwargs['worlddb']

def mt(status, message, data = {}):
	return {'status' : status, 'message' : message, 'data' : data}
