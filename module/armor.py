'''
armor.py
'''

from module import enums
from module import common


async def upgrade(uid, aid, level, **kwargs):
	if level < 1 or level > 9: return common.mt(99, 'invalid level')
	return common.mt(0, 'success')


async def get_all_armor(uid, **kwargs):
	armor = await common.execute(f'SELECT aid, level, quantity FROM armor WHERE uid = "{uid}";', **kwargs)
	return common.mt(0, 'success', {'armors': [{'aid': a[0], 'level': a[1], 'quantity': a[2]} for a in armor]})