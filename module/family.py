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
	return mt(0, 'success')

async def leave():
	pass

async def kick_member():
	pass

def mt(status, message):
	return {'status' : status, 'message' : message}
