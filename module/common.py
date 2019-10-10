'''
common.py

Contains definitions of commonly used generic functions.
When desinging a function, try to make it as general as possible to allow the reuse of code.
'''
from module import enums


async def exists(table, *conditions, account = False, **kwargs):
	condition = ' AND '.join([f'`{cond[0]}` = "{cond[1]}"' for cond in conditions])
	data = await execute(f'SELECT EXISTS (SELECT 1 FROM {table} WHERE {condition});', account, **kwargs)
	if data == () or () in data: return False
	return data[0][0] != 0

async def execute(statement, account = False, **kwargs):
	async with ((await get_db(**kwargs)).acquire() if not account else kwargs['accountdb'].acquire()) as conn:
		# await conn.select_db()
		async with conn.cursor() as cursor:
			await cursor.execute(statement)
			return await cursor.fetchall()

async def execute_update(statement, account = False, **kwargs):
	async with ((await get_db(**kwargs)).acquire() if not account else kwargs['accountdb'].acquire()) as conn:
		# await conn.select_db()
		async with conn.cursor() as cursor:
			affected = await cursor.execute(statement)
			return (affected, await cursor.fetchall())

async def get_gn(uid, **kwargs):
	data = await execute(f'SELECT gn FROM player WHERE uid = "{uid}";', **kwargs)
	return data[0][0]

async def get_uid(gn, **kwargs):
	data = await execute(f'SELECT uid FROM player WHERE gn = "{gn}";', **kwargs)
	return data[0][0]

async def try_item(uid, item, value, **kwargs):
	async with (await get_db(**kwargs)).acquire() as conn:
		# await conn.select_db()
		async with conn.cursor() as cursor:
			await cursor.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = "{item.value}" FOR UPDATE;')
			quantity = await cursor.fetchall()
			if value >= 0 or (quantity != () and quantity[0][0] + value >= 0):
				await cursor.execute(f'INSERT INTO item (uid, iid, value) VALUES ("{uid}", {item.value}, value) ON DUPLICATE KEY UPDATE value = value + {value};')
				return (True, quantity[0][0] + value) if quantity != () else (True, value)
			return (False, quantity[0][0] + value) if quantity != () else (False, value)

async def get_db(**kwargs):
	return kwargs['worlddb']

def encode_item(gid, iid, value):
	return f'{gid.value}:{iid.value}:{value}'

def decode_items(items):
	decoded = []
	for item in items.split(','):
		gid, iid, value = item.split(':')
		gid = enums.Group(int(gid))
		if gid == enums.Group.ITEM:
			decoded.append((gid, enums.Item(int(iid)), int(value)))
		elif gid == enums.Group.WEAPON:
			decoded.append((gid, enums.Weapon(int(iid)), int(value)))
		elif gid == enums.Group.SKILL:
			decoded.append((gid, enums.Skill(int(iid)), int(value)))
		elif gid == enums.Group.ROLE:
			decoded.append((gid, enums.Role(int(iid)), int(value)))
		elif gid == enums.Group.ARMOR:
			decoded.append((gid, enums.Armor(int(iid)), int(value)))
	return decoded



def mt(status, message, data = {}):
	return {'status' : status, 'message' : message, 'data' : data}
