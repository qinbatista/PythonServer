'''
player.py
'''

from module import mail
from module import enums
from module import common

async def create(uid, gn, **kwargs):
	added, _ = await common.execute_update(f'INSERT INTO player(uid, gn) VALUES ("{uid}", "{gn}") ON DUPLICATE KEY UPDATE gn = gn;', **kwargs)
	await common.execute(f'INSERT INTO `factory` (`uid`, `fid`, `workers`, `storage`) VALUES \
			("{uid}", {enums.Factory.UNASSIGNED.value}, 5, 5);', **kwargs)
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
	_, remaining = await common.try_item(uid, item[0][1], item[0][2], **kwargs)
	await mail.mark_read(uid, nonce, **kwargs)
	return common.mt(0, 'success', {'items' : [{'iid' : item[0][1].value, 'value' : remaining}]})

async def change_name(uid, name, **kwargs):
	pass

async def get_info(uid, player_experience, **kwargs):
	# data包含玩家名字和家庭名字，info包含玩家进程信息
	data = await common.execute(f'SELECT gn, fid FROM player WHERE uid = "{uid}";', **kwargs)
	info = await common.execute(f'SELECT energy, exp, stage, towerstage, hangstage FROM progress WHERE uid = "{uid}";', **kwargs)
	if info == ():
		await common.execute(f'INSERT INTO progress (uid) VALUE ("{uid}");', **kwargs)
		info = await common.execute(f'SELECT energy, exp, stage, towerstage, hangstage FROM progress WHERE uid = "{uid}";', **kwargs)
	return common.mt(0, 'success', {'gn': data[0][0], 'family_name': data[0][1], 'energy': info[0][0], 'exp': info[0][1], 'stage': info[0][2], 'towerstage': info[0][3], 'hangstage': info[0][4], 'player_experience': player_experience})

async def get_all_resource(uid, **kwargs):
	item = await common.execute(f'SELECT iid, value FROM item WHERE uid = "{uid}";', **kwargs)
	return common.mt(0, 'success', {'items': [{'iid': i[0], 'value': i[1]} for i in item]})


#########################################################################################

async def _lookup_nonce(nonce, **kwargs):
	async with kwargs['session'].post(kwargs['tokenserverbaseurl'] + '/redeem_nonce_new', json = {'nonce' : [nonce]}) as resp:
		data = await resp.json(content_type = 'text/json')
		return None if data[nonce]['status'] != 0 else data[nonce]['items']









