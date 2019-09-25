'''
common.py

Contains definitions of commonly used generic functions.
When desinging a function, try to make it as general as possible to allow the reuse of code.
'''


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

async def get_db(**kwargs):
	return kwargs['worlddb']

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

def mt(status, message, data = {}):
	return {'status' : status, 'message' : message, 'data' : data}
