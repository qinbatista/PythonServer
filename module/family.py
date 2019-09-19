'''
family.py
'''

import enum


class Role(enum.Enum):
	OWNER = 0,
	ADMIN = 1,
	ELITE = 2,
	BASIC = 3

class Family:
	def __init__(self):
		pass
	
	async def create(self, **kwargs):
		pass

	async def leave(self):
		pass

	async def kick_member(self):
		pass
