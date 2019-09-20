'''
game.py
'''

import enum

from module import common


class Item(enum.IntEnum):
	COIN = 0

async def try_coin(pid, value, **kwargs):
	coins = await _get_material(pid, Item.COIN, **kwargs)
	return (coins + value) >= 0

async def _get_material(pid, mid, **kwargs):
	data = await common.execute(f'SELECT value FROM item WHERE pid = "{pid}" AND iid = "{mid.value}";', kwargs['db'])
	return int(data[0][0])

