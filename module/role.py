'''
role.py
'''

from modules import enums
from modules import common


async def get_all(uid, **kwargs):
	roles = []
	return common.mt(0, 'success', {'roles' : roles)
