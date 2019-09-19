'''
game.py
'''

import enum


class Item(enum.Enum):
	COIN = 0

class Game:
	def __init__(self):
		pass

	async def try_coin(self, pid, value, **kwargs):
		coins = await self._get_material(pid, Item.COIN, kwargs)
		return (coins + value) >= 0

	async def _get_material(self, pid, mid, **kwargs):
		data = await self._execute_statement(f'SELECT value FROM item WHERE pid = "{pid}" AND iid = "{mid}";')
		return int(data[0][0])

	async def _execute_statement(self, statement, pool):
		async with pool.acquire() as conn:
			async with conn.cursor() as cursor:
				await cursor.execute(statement)
				return await cursor.fetchall()
	
