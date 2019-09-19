'''
family.py
'''

import enum
from module import game


class Role(enum.Enum):
	OWNER = 0,
	ADMIN = 1,
	ELITE = 2,
	BASIC = 3

async def create(pid, **kwargs):
	if not await game.try_coin(pid, -200, **kwargs):
		return mt(99, 'not enough coins!!!!')
	return mt(0, 'success!!')

async def leave():
	pass

async def kick_member():
	pass

def mt(status, message):
	return {'status' : status, 'message' : message}
