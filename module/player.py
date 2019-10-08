'''
player.py
'''

from module import enums
from module import common

async def create(uid, gn, **kwargs):
	added, _ = await common.execute_update(f'INSERT INTO player(uid, gn) VALUES ("{uid}", "{gn}") ON DUPLICATE KEY UPDATE gn = gn;', **kwargs)
	return common.mt(0, 'success', {'gn' : gn}) if added != 0 else common.mt(99, 'gamename or uid already exists')

async def enter_world(uid, **kwargs):
	existing_player = await common.exists('player', ('uid', uid), **kwargs)
	if not existing_player: return common.mt(98, 'have not been in this world before')
	return common.mt(0, 'success')

async def accept_gift(uid, key, **kwargs):
	pass

async def change_name(uid, name, **kwargs):
	pass

async def get_info(uid, **kwargs):
	pass

async def get_all_resource(uid, **kwargs):
	item = await common.execute(f'SELECT iid, value FROM item WHERE uid = "{uid}";', **kwargs)
	return common.mt(0, 'success', {'items': [{'iid': i[0], 'value': i[1]} for i in item]})

