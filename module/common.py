'''
common.py
'''

def mt(status, message, data = {}):
	return {'status' : status, 'message' : message, 'data' : data}

async def exists(table, identifier, value, *, db = 'worlddb', **kwargs):
	data = await execute(f'SELECT EXISTS (SELECT 1 FROM {table} WHERE {identifier} = "{value}");', kwargs[db])
	if data == () or () in data: return False
	return data[0][0] != 0

async def execute(statement, pool):
	async with pool.acquire() as conn:
		async with conn.cursor() as cursor:
			await cursor.execute(statement)
			return await cursor.fetchall()

