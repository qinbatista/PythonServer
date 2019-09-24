'''
family.py
'''
from module import common


async def create(uid, name, **kwargs):
	if not _valid_family_name(name): return common.mt(99, 'invalid family name')
	if await _in_family(uid, **kwargs): return common.mt(97, 'already in a family')
	enough, _ = await common.try_item(uid, common.Item.COIN, -200, **kwargs)
	if not enough: return common.mt(99, 'need coins')
	if await common.exists('family', 'name', name, **kwargs): return common.mt(98, 'name already exists!')
	await common.execute(f'INSERT INTO family(name) VALUES("{name}");', kwargs['worlddb'])
	await common.execute(f'INSERT INTO familyrole(uid, name, role) VALUES("{uid}", "{name}", "{common.FamilyRole.OWNER.value}");', kwargs['worlddb'])
	await common.execute(f'UPDATE player SET fid = "{name}" WHERE uid = "{uid}";', kwargs['worlddb'])
	return common.mt(0, 'success!!')

async def leave():
	pass

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
	return not (data == () or ('',) in data)
