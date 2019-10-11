'''
family.py
'''
import asyncio
import pymysql

from module import mail
from module import enums
from module import common

CHANGE_NAME_DIAMOND = 100

MERCHANDISE = { '3:6:1' : '3:1:80' }

async def create(uid, name, **kwargs):
	if not _valid_family_name(name): return common.mt(99, 'invalid family name')
	in_family, _ = await _in_family(uid, **kwargs)
	if in_family: return common.mt(98, 'already in a family')
	enough, _ = await common.try_item(uid, enums.Item.COIN, -200, **kwargs)
	if not enough: return common.mt(97, 'need coins')
	if await common.exists('family', ('name', name), **kwargs): return common.mt(96, 'name already exists!')
	await asyncio.gather(common.execute(f'INSERT INTO family(name) VALUES("{name}");', **kwargs),
						common.execute(f'INSERT INTO familyrole(uid, name, role) VALUES("{uid}", "{name}", "{enums.FamilyRole.OWNER.value}");', **kwargs),
						common.execute(f'UPDATE player SET fid = "{name}" WHERE uid = "{uid}";', **kwargs))
	return common.mt(0, 'created family', {'name' : name})

async def leave(uid, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in a family')
	role = await _get_role(uid, name, **kwargs)
	if role == enums.FamilyRole.OWNER: return common.mt(98, 'owner can not leave family')
	await _remove_from_family(uid, name, **kwargs)
	return common.mt(0, 'left family')

async def remove_user(uid, gn_target, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in a family')
	role = await _get_role(uid, name, **kwargs)
	uid_target = await common.get_uid(gn_target, **kwargs)
	_, name_target = await _in_family(uid_target, **kwargs)
	if name_target != name: return common.mt(98, 'target is not in your family')
	role_target = await _get_role(uid_target, name, **kwargs)
	if not _check_remove_permissions(role, role_target): return common.mt(97, 'insufficient permissions')
	await _remove_from_family(uid_target, name, **kwargs)
	return common.mt(0, 'removed user', {'gn' : gn_target})

async def invite_user(uid, gn_target, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in a family')
	role = await _get_role(uid, name, **kwargs)
	if not _check_invite_permissions(role): return common.mt(98, 'insufficient permissions')
	uid_target = await common.get_uid(gn_target, **kwargs)
	sent = await mail.send_mail(enums.MailType.FAMILY_REQUEST, uid_target, subj = 'Family Invitation', body = f'You have been invited to join: {name}', name = name, uid_target = uid_target, **kwargs)
	return common.mt(0, 'invited user', {'gn' : gn_target}) if sent else common.mt(97, 'mail could not be sent')

async def request_join(uid, name, **kwargs):
	in_family, _ = await _in_family(uid, **kwargs)
	if in_family: return common.mt(99, 'already in a family')
	gn = await common.get_gn(uid, **kwargs)
	officials = await _get_uid_officials(name, **kwargs)
	if not officials: return common.mt(98, 'invalid family')
	sent = await mail.send_mail(enums.MailType.FAMILY_REQUEST, *officials, subj = 'Family Request', body = f'{gn} requests to join your family.', name = name, uid_target = uid, **kwargs)
	return common.mt(0, 'requested join', {'name' : name}) if sent else common.mt(97, 'mail could not be sent')

async def respond(uid, nonce, **kwargs):
	name, uid_target = await _lookup_nonce(nonce, **kwargs)
	if not name: return common.mt(99, 'invalid nonce')
	in_family, _ = await _in_family(uid_target, **kwargs)
	if in_family: return common.mt(98, 'already in a family')
	exists, info = await _get_family_info(name, 'icon', 'exp', 'notice', 'board', **kwargs)
	if not exists: return common.mt(97, 'family no longer exists')
	await _add_to_family(uid_target, name, **kwargs)
	return common.mt(0, 'success', {'name' : name, 'icon' : info[0], 'exp' : info[1], 'notice' : info[2], 'board' : info[3]})

async def get_all(uid, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in a family')
	_, info = await _get_family_info(name, 'icon', 'exp', 'notice', 'board', **kwargs)
	members = await _get_member_info(name, **kwargs)
	return common.mt(0, 'success', {'name' : name, 'icon' : info[0], 'exp' : info[1], 'notice' : info[2], 'board' : info[3], 'members' : members})

async def get_store(**kwargs):
	return common.mt(0, 'success', {'merchandise' : [{'item' : k, 'cost' : v} for k,v in MERCHANDISE.items()]})

async def purchase(uid, item, **kwargs):
	gid, iid, value = (common.decode_items(item))[0]
	return common.mt(0, 'success')

async def set_notice(uid, msg, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in family')
	role = await _get_role(uid, name, **kwargs)
	if not _check_notice_permissions(role): return common.mt(98,'insufficient permissions')
	await common.execute(f'UPDATE family SET notice = "{msg}" WHERE `name` = "{name}";', **kwargs)
	return common.mt(0, 'success', {'notice' : msg})

async def set_blackboard(uid, msg, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in family')
	role = await _get_role(uid, name, **kwargs)
	if not _check_blackboard_permissions(role): return common.mt(98, 'insufficient permissions')
	await common.execute(f'UPDATE family SET board = "{msg}" WHERE `name` = "{name}";', **kwargs)
	return common.mt(0, 'success', {'board' : msg})

async def set_role(uid, gn_target, role, **kwargs):
	new_role = enums.FamilyRole(role)
	uid_target = await common.get_uid(gn_target, **kwargs)
	if uid == uid_target: return common.mt(99, 'can not modify self')
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(98, 'not in family')
	target_in_family, target_name = await _in_family(uid_target, **kwargs)
	if not target_in_family or target_name != name: return common.mt(97, 'target not in your family')
	actors_role = await _get_role(uid, name, **kwargs)
	targets_role = await _get_role(uid_target, name, **kwargs)
	if not _check_set_role_permissions(actors_role, targets_role, new_role): return common.mt(96, 'insufficient permissions')
	await common.execute(f'UPDATE familyrole SET role = {new_role.value} WHERE uid = "{uid_target}" AND `name` = "{name}";', **kwargs)
	return common.mt(0, 'success', {'gn' : gn_target, 'role' : new_role.value})

async def change_name(uid, new_name, **kwargs):
	if not _valid_family_name(new_name): return common.mt(99, 'invalid family name')
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(98, 'not in family')
	role = await _get_role(uid, name, **kwargs)
	if not _check_change_name_permissions(role): return common.mt(97, 'insufficient permissions')
	can_pay, remaining = await common.try_item(uid, enums.Item.DIAMOND, -CHANGE_NAME_DIAMOND, **kwargs)
	if not can_pay: return common.mt(96, 'insufficient funds')
	try:
		await common.execute(f'UPDATE family SET name = "{new_name}" WHERE name = "{name}";', **kwargs)
	except pymysql.err.IntegrityError:
		await common.try_item(uid, enums.Item.DIAMOND, CHANGE_NAME_DIAMOND, **kwargs)
		return common.mt(95, 'family name already exists')
	await common.execute(f'UPDATE player SET fid = "{new_name}" WHERE fid = "{name}";', **kwargs)
	await common.execute(f'UPDATE familyrole SET name = "{new_name}" WHERE name = "{name}";', **kwargs)
	return common.mt(0, 'success', {'name' : new_name, 'iid' : enums.Item.DIAMOND.value, 'value' : remaining})



########################################################################
SET_ROLE_PERMISSIONS = {\
		enums.FamilyRole.OWNER : {'target' : {enums.FamilyRole.ADMIN, enums.FamilyRole.ELITE, enums.FamilyRole.BASIC}, 'new' : {enums.FamilyRole.ADMIN, enums.FamilyRole.ELITE, enums.FamilyRole.BASIC}},
		enums.FamilyRole.ADMIN : {'target' : {enums.FamilyRole.ELITE, enums.FamilyRole.BASIC}, 'new' : {enums.FamilyRole.ELITE, enums.FamilyRole.BASIC}}
		}

def _valid_family_name(name):
	return bool(name)

def _check_change_name_permissions(check):
	return check >= enums.FamilyRole.ADMIN

def _check_set_role_permissions(actors_role, targets_role, new_role):
	try:
		return targets_role in SET_ROLE_PERMISSIONS[actors_role]['target'] and new_role in SET_ROLE_PERMISSIONS[actors_role]['new']
	except KeyError:
		pass
	return False

def _check_notice_permissions(check):
	return check >= enums.FamilyRole.ADMIN

def _check_blackboard_permissions(check):
	return check >= enums.FamilyRole.ADMIN

def _check_remove_permissions(remover, to_remove):
	if remover == enums.FamilyRole.OWNER: return True
	elif remover == enums.FamilyRole.ADMIN and to_remove < enums.FamilyRole.ADMIN: return True
	return False

def _check_invite_permissions(inviter):
	return inviter >= enums.FamilyRole.ADMIN

async def _get_member_info(name, **kwargs):
	data = await common.execute(f'SELECT player.gn, familyrole.role, progress.exp FROM familyrole JOIN player ON player.uid = familyrole.uid JOIN progress ON progress.uid = familyrole.uid WHERE familyrole.name = "{name}";', **kwargs)
	return [{'gn' : m[0], 'role' : m[1], 'exp' : m[2], 'icon' : 0} for m in data]

async def _get_family_info(name, *args, **kwargs):
	data = await common.execute(f'SELECT {",".join(args)} FROM family WHERE name = "{name}";', **kwargs)
	return (True, data[0]) if data != () else (False, ())

async def _add_to_family(uid, name, **kwargs):
	await asyncio.gather(common.execute(f'UPDATE player SET fid = "{name}" WHERE uid = "{uid}";', **kwargs),
			common.execute(f'INSERT INTO familyrole VALUES("{uid}", "{name}", {enums.FamilyRole.BASIC.value});', **kwargs))

async def _in_family(uid, **kwargs):
	data = await common.execute(f'SELECT fid FROM player WHERE uid = "{uid}";', **kwargs)
	if data == () or ('',) in data: return (False, '')
	return (True, data[0][0])

async def _get_role(uid, name, **kwargs):
	data = await common.execute(f'SELECT role FROM familyrole WHERE uid = "{uid}" AND `name` = "{name}";', **kwargs)
	return enums.FamilyRole(data[0][0])


async def _get_uid_officials(name, **kwargs):
	print(f'querying: SELECT uid FROM familyrole WHERE `name` = "{name}" AND `role` >= {enums.FamilyRole.ADMIN.value};')
	data = await common.execute(f'SELECT uid FROM familyrole WHERE `name` = "{name}" AND `role` >= {enums.FamilyRole.ADMIN.value};', **kwargs)
	return None if data == () else [u[0] for u in data]

async def _lookup_nonce(nonce, **kwargs):
	async with kwargs['session'].post(kwargs['tokenserverbaseurl'] + '/redeem_nonce_new', json = {'nonce' : [nonce]}) as resp:
		data = await resp.json(content_type = 'text/json')
		return (None, None) if data[nonce]['status'] != 0 else (data[nonce]['name'], data[nonce]['uid_target'])

async def _remove_from_family(uid, name, **kwargs):
	await asyncio.gather(common.execute(f'UPDATE player SET fid = "" WHERE uid = "{uid}";', **kwargs),
			common.execute(f'DELETE FROM familyrole WHERE uid = "{uid}" AND name = "{name}";', **kwargs))
