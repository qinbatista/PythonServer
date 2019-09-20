'''
family.py
'''

import enum
from module import game
from module import common


class Role(enum.IntEnum):
	OWNER = 0,
	ADMIN = 1,
	ELITE = 2,
	BASIC = 3

async def create(pid, name, **kwargs):
	if not await game.try_coin(pid, -200, **kwargs):
		return mt(99, 'not enough coins!!!!')
	if await common.exists('family', 'name', name, **kwargs):
		return mt(98, 'that family name already exists!')
	await common.execute(f'INSERT INTO family VALUES("{name}", 0);', kwargs['db'])
	print(type(Role.OWNER.value))
	await common.execute(f'INSERT INTO familyrole(name, pid, role) VALUES("{name}", "{pid}", "{Role.OWNER.value}");', kwargs['db'])
	await common.execute(f'UPDATE player SET fid = "{name}" WHERE pid = "{pid}";', kwargs['db'])
	return mt(0, 'success!!')

async def leave():
	pass

async def kick_member():
	pass

def mt(status, message):
	return {'status' : status, 'message' : message}
