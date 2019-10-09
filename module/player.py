'''
player.py
'''

from module import mail
from module import enums
from module import common

async def create(uid, gn, **kwargs):
	added, _ = await common.execute_update(f'INSERT INTO player(uid, gn) VALUES ("{uid}", "{gn}") ON DUPLICATE KEY UPDATE gn = gn;', **kwargs)
	return common.mt(0, 'success', {'gn' : gn}) if added != 0 else common.mt(99, 'gamename or uid already exists')

async def enter_world(uid, **kwargs):
	existing_player = await common.exists('player', ('uid', uid), **kwargs)
	if not existing_player: return common.mt(98, 'have not been in this world before')
	return common.mt(0, 'success')

async def get_account_world_info(uid, **kwargs):
	worlds = [{'server_status' : 0, 'world' : '1', 'world_name' : 'experimental_test1', 'gn' : '', 'exp' : ''},{'server_status' : 0, 'world' : '2', 'world_name' : 'experimental_test2', 'gn' : '', 'exp' : ''}]
	exp = await common.execute(f'SELECT exp FROM progress WHERE uid = "{uid}";', **kwargs)
	if exp != ():
		world = {'server_status' : 0, 'world' : '0', 'world_name' : 'experimental', 'gn' : await common.get_gn(uid, **kwargs), 'exp' : exp[0][0]}
		worlds.append(world)
	else:
		world = {'server_status' : 0, 'world' : '0', 'world_name' : 'experimental', 'gn' : '', 'exp' : ''}
		worlds.append(world)
	return common.mt(0, 'success', {'worlds' : worlds})

async def accept_gift(uid, nonce, **kwargs):
	gift = await _lookup_nonce(nonce, **kwargs)
	if not gift: return common.mt(99, 'invalid nonce')
	item = common.decode_items(gift)
	_, remaining = await common.try_item(uid, item[1], item[2], **kwargs)
	await mail.delete_mail(uid, nonce, **kwargs)
	return common.mt(0, 'success', item[0] : {'iid' : item[1], 'value' : remaining})

async def change_name(uid, name, **kwargs):
	pass

async def get_info(uid, **kwargs):
	pass

async def get_all_resource(uid, **kwargs):
	item = await common.execute(f'SELECT iid, value FROM item WHERE uid = "{uid}";', **kwargs)
	return common.mt(0, 'success', {'items': [{'iid': i[0], 'value': i[1]} for i in item]})

async def get_player_info(uid, **kwargs):
	player = await common.execute(f'SELECT gn, fid FROM player WHERE uid = "{uid}";', **kwargs)
	# 根据朋友id查朋友的游戏名字
	return common.mt(0, 'success', {'player_info': [{'gn': 'cc', 'fgn': 'fcc'}]})

#########################################################################################

async def _lookup_nonce(nonce, **kwargs):
	async with kwargs['session'].post(kwargs['tokenserverbaseurl'] + '/redeem_nonce_new', json = {'nonce' : [nonce]}) as resp:
		data = await resp.json(content_type = 'text/json')
		return None if data['status'] != 0 else data['nonce']['items']









