'''
armor.py
'''

from module import enums
from module import common


async def upgrade(uid, aid, level, **kwargs):
	if level < 1 or level > 9: return common.mt(99, 'invalid level')
	return common.mt(0, 'success')
