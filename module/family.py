'''
family.py
'''
from module import common


async def create(uid, name, **kwargs):
	if not _valid_family_name(name): return common.mt(99, 'invalid family name')
	in_family, _ = await _in_family(uid, **kwargs)
	if in_family: return common.mt(97, 'already in a family')
	enough, _ = await common.try_item(uid, common.Item.COIN, -200, **kwargs)
	if not enough: return common.mt(99, 'need coins')
	if await common.exists('family', 'name', name, **kwargs): return common.mt(98, 'name already exists!')
	await asyncio.gather(common.execute(f'INSERT INTO family(name) VALUES("{name}");', kwargs['worlddb']),
						common.execute(f'INSERT INTO familyrole(uid, name, role) VALUES("{uid}", "{name}", "{common.FamilyRole.OWNER.value}");', kwargs['worlddb']),
						common.execute(f'UPDATE player SET fid = "{name}" WHERE uid = "{uid}";', kwargs['worlddb']))
	return common.mt(0, 'success!!')

async def leave(uid, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in a family')
	role = await _get_role(uid, name, **kwargs)
	if role == common.FamilyRole.OWNER: return common.mt(98, 'owner can not leave family')
	await common.execute(f'UPDATE player SET fid = "" WHERE uid = "{uid}";', kwargs['worlddb'])
	await common.execute(f'DELETE FROM familyrole WHERE uid = "{uid}" AND name = "{name}";', kwargs['worlddb'])
	return common.mt(0, 'success')



async def invite_user():
	pass

async def request_join():
	pass

async def respond_nonce():
	pass

async def kick_member():
	pass

########################################################################
def _valid_family_name(name):
	return bool(name)

async def _in_family(uid, **kwargs):
	data = await common.execute(f'SELECT fid FROM player WHERE uid = "{uid}";', kwargs['worlddb'])
	if data == () or ('',) in data: return (False, '')
	return (True, data[0][0])

async def _get_role(uid, name, **kwargs):
	data = await common.execute(f'SELECT role FROM familyrole WHERE uid = "{uid}" AND `name` = "{name}";', kwargs['worlddb'])
	return common.FamilyRole(data[0][0])
