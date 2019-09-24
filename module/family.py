'''
family.py
'''
import asyncio

from module import common


async def create(uid, name, **kwargs):
	if not _valid_family_name(name): return common.mt(99, 'invalid family name')
	in_family, _ = await _in_family(uid, **kwargs)
	if in_family: return common.mt(97, 'already in a family')
	enough, _ = await common.try_item(uid, common.Item.COIN, -200, **kwargs)
	if not enough: return common.mt(99, 'need coins')
	if await common.exists('family', 'name', name, **kwargs): return common.mt(98, 'name already exists!')
	await asyncio.gather(common.execute(f'INSERT INTO family(name) VALUES("{name}");', **kwargs),
						common.execute(f'INSERT INTO familyrole(uid, name, role) VALUES("{uid}", "{name}", "{common.FamilyRole.OWNER.value}");', **kwargs),
						common.execute(f'UPDATE player SET fid = "{name}" WHERE uid = "{uid}";', **kwargs))
	return common.mt(0, 'success!!')

async def leave(uid, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in a family')
	role = await _get_role(uid, name, **kwargs)
	if role == common.FamilyRole.OWNER: return common.mt(98, 'owner can not leave family')
	await _remove_from_family(uid, name, **kwargs)
	return common.mt(0, 'success')

async def remove_user(uid, gn_target, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in a family')
	role = await _get_role(uid, name, **kwargs)
	uid_target = await _get_uid(gn_target, **kwargs)
	_, name_target = await _in_family(uid_target, **kwargs)
	if name_target != name: return common.mt(98, 'target is not in your family')
	role_target = await _get_role(uid_target, name, **kwargs)
	if not _check_remove_permissions(role, role_target): return common.mt(97, 'insufficient permissions')
	await _remove_from_family(uid_target, name, **kwargs)
	return common.mt(0, 'success')

async def invite_user():
	pass

async def request_join():
	pass

async def respond_nonce():
	pass


########################################################################
def _valid_family_name(name):
	return bool(name)

def _check_remove_permissions(remover, to_remove):
	if remover == common.FamilyRole.OWNER: return True
	elif remove == common.FamilyRole.ADMIN and to_remove < common.FamilyRole.ADMIN: return True
	return False

async def _in_family(uid, **kwargs):
	data = await common.execute(f'SELECT fid FROM player WHERE uid = "{uid}";', **kwargs)
	if data == () or ('',) in data: return (False, '')
	return (True, data[0][0])

async def _get_role(uid, name, **kwargs):
	data = await common.execute(f'SELECT role FROM familyrole WHERE uid = "{uid}" AND `name` = "{name}";', **kwargs)
	return common.FamilyRole(data[0][0])

async def _get_uid(gn, **kwargs):
	data = await common.execute(f'SELECT uid FROM player WHERE gn = "{gn}";', **kwargs)
	return data[0][0]

async def _remove_from_family(uid, name, **kwargs):
	await asyncio.gather(common.execute(f'UPDATE player SET fid = "" WHERE uid = "{uid}";', **kwargs),
			common.execute(f'DELETE FROM familyrole WHERE uid = "{uid}" AND name = "{name}";', **kwargs))
