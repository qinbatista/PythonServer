'''
armor.py
'''

from module import enums
from module import common


async def upgrade(uid, aid, tier, **kwargs): 
	if tier < 1 or tier > 9: return common.mt(99, 'invalid tier')
	return common.mt(0, 'success')
