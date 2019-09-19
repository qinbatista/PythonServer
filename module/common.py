'''
common.py
'''
async def execute(statement, pool):
	async with pool.acquire() as conn:
		async with conn.cursor() as cursor:
			await cursor.execute(statement)
			return await cursor.fetchall()

