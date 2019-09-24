'''
family.py
'''
import asyncio

from module import mail
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

async def invite_user(uid, gn_target, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in a family')
	role = await _get_role(uid, name, **kwargs)
	if not _check_invite_permissions(role): return common.mt(98, 'insufficient permissions')
	uid_target = await _get_uid(gn_target, **kwargs)
	sent = await mail.send_mail(common.MailType.FAMILY_REQUEST, uid_target, from_ = name, subject = 'Family Invitation', body = f'You have been invited to join:\n{name}', name = name, target = gn_target)
	return common.mt(0, 'success') if sent else common.mt(97, 'mail could not be sent')

async def request_join(uid, name, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if in_family: return common.mt(99, 'already in a family')
	gn = await _get_gn(uid, **kwargs)
	officials = await _get_uid_officials(name, **kwargs)
	if not officials: return common.mt(98, 'invalid family')
	sent = await mail.send_mail(common.MailType.FAMILY_REQUEST, *officials, from_ = name, subject = 'Family Request', body = f'{gn} requests to join your family.', name = name, target = gn)
	return common.mt(0, 'success') if sent else common.mt(97, 'mail could not be sent')

async def respond(uid, nonce, **kwargs):
	name, gn_target = await _lookup_nonce(nonce, **kwargs)
	uid_target = await _get_uid(gn_target, **kwargs)
	in_family, _ = await _in_family(uid_target, **kwargs)
	if in_family: return common.mt(99, 'already in a family')
	await _add_to_family(uid_target, name)
	return common.mt(0, 'success')


########################################################################
def _valid_family_name(name):
	return bool(name)

def _check_remove_permissions(remover, to_remove):
	if remover == common.FamilyRole.OWNER: return True
	elif remove == common.FamilyRole.ADMIN and to_remove < common.FamilyRole.ADMIN: return True
	return False

def _check_invite_permissions(inviter):
	return inviter >= common.FamilyRole.ADMIN

async def _add_to_family(uid, name, **kwargs):
	await asyncio.gather(common.execute(f'UPDATE player SET fid = "{name}" WHERE uid = "{uid}";', **kwargs),
			common.execute(f'INSERT INTO familyrole VALUES("{uid}", "{name}", {common.FamilyRole.BASIC.value});', **kwargs))

async def _in_family(uid, **kwargs):
	data = await common.execute(f'SELECT fid FROM player WHERE uid = "{uid}";', **kwargs)
	if data == () or ('',) in data: return (False, '')
	return (True, data[0][0])

async def _get_gn(uid, **kwargs):
	data = await common.execute(f'SELECT gn FROM player WHERE uid = "{uid}";', **kwargs)
	return data[0][0]

async def _get_role(uid, name, **kwargs):
	data = await common.execute(f'SELECT role FROM familyrole WHERE uid = "{uid}" AND `name` = "{name}";', **kwargs)
	return common.FamilyRole(data[0][0])

async def _get_uid(gn, **kwargs):
	data = await common.execute(f'SELECT uid FROM player WHERE gn = "{gn}";', **kwargs)
	return data[0][0]

async def _get_uid_officials(name, **kwargs):
	data = await common.execute(f'SELECT uid FROM familyrole WHERE `name` = "{name}" AND `role` >= {common.FamilyRole.ADMIN.value};', **kwargs)
	return None if data == () else [u[0] for u in data]

async def _lookup_nonce(nonce, **kwargs):
	async with kwargs['session'].post(kwargs['tokenserverbaseurl'] + '/redeem_nonce', data = {'nonce' : nonce}) as resp:
		pass
	return (None, None)

async def _remove_from_family(uid, name, **kwargs):
	await asyncio.gather(common.execute(f'UPDATE player SET fid = "" WHERE uid = "{uid}";', **kwargs),
			common.execute(f'DELETE FROM familyrole WHERE uid = "{uid}" AND name = "{name}";', **kwargs))
