'''
family.py
'''
import asyncio
import pymysql

from module import mail
from module import enums
from module import common
from module import task
from module import achievement
from module import stage

from datetime import datetime, timezone, timedelta


async def create(uid, name, icon, **kwargs):
	"""icon必须为整型或者数字字符串"""
	exp_info = await stage.increase_exp(uid, 0, **kwargs)
	if exp_info["level"] < kwargs['config']['family']['general']['player_level']: return common.mt(95, "玩家等级未满开启等级")
	if not _valid_family_name(name): return common.mt(99, 'invalid family name')
	in_family, _ = await _in_family(uid, **kwargs)
	if in_family: return common.mt(98, 'already in a family')
	_, iid, cost = (common.decode_items(kwargs['config']['family']['general']['costs']['create']))[0]
	enough, remaining = await common.try_item(uid, iid, -cost, **kwargs)
	if not enough: return common.mt(97, 'insufficient materials')
	if await common.exists('family', ('name', name), **kwargs): return common.mt(96, 'name already exists!')
	await asyncio.gather(common.execute(f'INSERT INTO family(name, icon) VALUES("{name}", {icon});', **kwargs),
						common.execute(f'INSERT INTO familyrole(uid, name, role) VALUES("{uid}", "{name}", "{enums.FamilyRole.OWNER.value}");', **kwargs),
						common.execute(f'UPDATE player SET fid = "{name}" WHERE uid = "{uid}";', **kwargs))
	return common.mt(0, 'created family', {'name' : name, 'icon': icon, 'iid' : iid.value, 'value' : remaining})

async def leave(uid, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in a family')
	role = await _get_role(uid, name, **kwargs)
	if role == enums.FamilyRole.OWNER: return common.mt(98, 'owner can not leave family')
	days = kwargs['config']['family']['general']['leave_days']
	await common.execute(f'INSERT INTO timer (uid, tid, time) VALUES ("{uid}", {enums.Timer.FAMILY_JOIN_END.value}, "{(datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")}");', **kwargs)
	await _remove_from_family(uid, name, **kwargs)
	gn = await common.get_gn(uid, **kwargs)
	await _record_family_change(name, f'{gn} has left.', **kwargs)
	return common.mt(0, 'left family', {"cd_time": days * 24 * 3600})

async def remove_user(uid, gn_target, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in a family')
	role = await _get_role(uid, name, **kwargs)
	uid_target = await common.get_uid(gn_target, **kwargs)
	if uid == uid_target: return common.mt(96, "You can't remove yourself")
	_, name_target = await _in_family(uid_target, **kwargs)
	if name_target != name: return common.mt(98, 'target is not in your family')
	role_target = await _get_role(uid_target, name, **kwargs)
	if not _check_remove_permissions(role, role_target): return common.mt(97, 'insufficient permissions')
	await _remove_from_family(uid_target, name, **kwargs)
	gn = await common.get_gn(uid, **kwargs)
	await _record_family_change(name, f'{gn_target} was removed by {gn}.', **kwargs)
	return common.mt(0, 'removed user', {'gn' : gn_target})

async def invite_user(uid, gn_target, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in a family')
	role = await _get_role(uid, name, **kwargs)
	if not _check_invite_permissions(role): return common.mt(98, 'insufficient permissions')
	uid_target = await common.get_uid(gn_target, **kwargs)
	sent = await mail.send_mail(enums.MailType.FAMILY_REQUEST, uid_target, \
			subj = enums.MailTemplate.FAMILY_INVITATION.name, \
			name = name, uid_target = uid_target, **kwargs)
	return common.mt(0, 'invited user', {'gn' : gn_target}) if sent else common.mt(97, 'mail could not be sent')

async def request_join(uid, name, **kwargs):
	in_family, _ = await _in_family(uid, **kwargs)
	if in_family: return common.mt(99, 'already in a family')
	gn = await common.get_gn(uid, **kwargs)
	officials = await _get_uid_officials(name, **kwargs)
	if not officials: return common.mt(98, 'invalid family')
	sent = await mail.send_mail(enums.MailType.FAMILY_REQUEST, *officials, \
			subj = enums.MailTemplate.FAMILY_REQUEST.name, name = name, uid_target = uid, **kwargs)
	return common.mt(0, 'requested join', {'name' : name}) if sent else common.mt(97, 'mail could not be sent')

async def respond(uid, nonce, **kwargs):
	name, uid_target = await _lookup_nonce(nonce, **kwargs)
	if not name: return common.mt(99, 'invalid nonce')
	in_family, _ = await _in_family(uid_target, **kwargs)
	if in_family: return common.mt(98, 'already in a family')
	exists, info = await _get_family_info(name, 'icon', 'exp', 'notice', 'board', **kwargs)
	if not exists: return common.mt(97, 'family no longer exists')
	member_count = await _count_members(name, **kwargs)
	if member_count >= kwargs['config']['family']['general']['members']['max']: return common.mt(96, 'family is full')
	await _add_to_family(uid_target, name, **kwargs)
	gn_target = await common.get_gn(uid_target, **kwargs)
	await _record_family_change(name, f'{gn_target} has joined.', **kwargs)
	return common.mt(0, 'success', {'name' : name, 'icon' : info[0], 'exp' : info[1], 'notice' : info[2], 'board' : info[3]})

async def get_all(uid, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in a family')
	timer = await _get_disband_timer(name, **kwargs)
	if timer is not None and datetime.now(timezone.utc) > timer:
		await _delete_family(name, **kwargs)
		return common.mt(99, 'not in a family')
	_, info = await _get_family_info(name, 'icon', 'exp', 'notice', 'board', **kwargs)
	members = await _get_member_info(name, **kwargs)
	news = await _get_family_changes(name, **kwargs)
	return common.mt(0, 'success', {'name' : name, 'icon' : info[0], 'exp' : info[1], 'notice' : info[2], 'board' : info[3], 'members' : members, 'news' : news, 'timer' : -1 if timer is None else int((timer-datetime.now(timezone.utc)).total_seconds())})

async def get_store(**kwargs):
	return common.mt(0, 'success', {'merchandise' : [{'item' : k, 'cost' : v} for k,v in kwargs['config']['family']['store']['items'].items()]})

async def purchase(uid, item, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in a family')
	if item not in kwargs['config']['family']['store']['items']:
		return common.mt(98, 'invalid item')
	i, c = common.decode_items(','.join([item, kwargs['config']['family']['store']['items'][item]]))
	can_pay, cost_remaining = await common.try_item(uid, c[1], -1 * c[2], **kwargs)
	if not can_pay: return common.mt(97, 'insufficient funds')
	_, item_remaining = await common.try_item(uid, i[1], i[2], **kwargs)
	gn = await common.get_gn(uid, **kwargs)
	await _record_family_change(name, f'{gn} purchased {item}.', **kwargs)
	return common.mt(0, 'success', { enums.Group.ITEM.value : [ {'iid' : i[1], 'value' : item_remaining}, {'iid' : c[1], 'value' : cost_remaining}]})

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
	if role not in enums.FamilyRole._value2member_map_.keys(): return common.mt(95, 'role type error')
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
	gn = await common.get_gn(uid, **kwargs)
	await _record_family_change(name, f'{gn} set {gn_target} role to {new_role.name}.', **kwargs)
	return common.mt(0, 'success', {'gn' : gn_target, 'role' : new_role.value})

async def change_name(uid, new_name, **kwargs):
	if not _valid_family_name(new_name): return common.mt(99, 'invalid family name')
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(98, 'not in family')
	role = await _get_role(uid, name, **kwargs)
	if not _check_change_name_permissions(role): return common.mt(97, 'insufficient permissions')
	_, iid, cost = (common.decode_items(kwargs['config']['family']['general']['costs']['change_name']))[0]
	can_pay, remaining = await common.try_item(uid, iid, -cost, **kwargs)
	if not can_pay: return common.mt(96, 'insufficient funds')
	try:
		await common.execute(f'UPDATE family SET name = "{new_name}" WHERE name = "{name}";', **kwargs)
	except pymysql.err.IntegrityError:
		await common.try_item(uid, iid, cost, **kwargs)
		return common.mt(95, 'family name already exists')
	await common.execute(f'UPDATE player SET fid = "{new_name}" WHERE fid = "{name}";', **kwargs)
	await common.execute(f'UPDATE familyrole SET name = "{new_name}" WHERE name = "{name}";', **kwargs)
	await common.execute(f'UPDATE familyhistory SET name = "{new_name}" WHERE name = "{name}";', **kwargs)
	await _record_family_change(new_name, f'{await common.get_gn(uid, **kwargs)} changed family name to: {new_name}.', **kwargs)
	return common.mt(0, 'success', {'name' : new_name, 'iid' : iid.value, 'value' : remaining})

async def disband(uid, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in family')
	role = await _get_role(uid, name, **kwargs)
	if not _check_disband_permissions(role): return common.mt(98, 'insufficient permissions')
	timer = await _get_disband_timer(name, **kwargs)
	if timer is not None: return common.mt(97, 'family already disbanded')
	timer = await _set_disband_timer(name, **kwargs)
	await _record_family_change(name, f'{await common.get_gn(uid, **kwargs)} disbanded family.', **kwargs)
	return common.mt(0, 'success', {'timer' : timer})

async def cancel_disband(uid, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in family')
	role = await _get_role(uid, name, **kwargs)
	if not _check_disband_permissions(role): return common.mt(98, 'insufficient permissions')
	timer = await _get_disband_timer(name, **kwargs)
	if timer is None: return common.mt(97, 'family is not disbanded')
	await _delete_disband_timer(name, **kwargs)
	await _record_family_change(name, f'{await common.get_gn(uid, **kwargs)} canceled family disband.', **kwargs)
	return common.mt(0, 'success')

async def check_in(uid, **kwargs):
	kwargs.update({"task_id":enums.Task.FAMILY_CHECK_IN})
	await task.record_task(uid,**kwargs)

	kwargs.update({"aid":enums.Achievement.CHECK_IN_FAMILY})
	await achievement.record_achievement(kwargs['data']['unique_id'],**kwargs)

	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in family')
	timer = await _get_check_in_timer(uid, **kwargs)
	now = datetime.now(timezone.utc)
	if timer is not None and now < timer: return common.mt(98, 'already checked in today')
	time = (now + timedelta(days = 1)).strftime('%Y-%m-%d')
	await common.execute(f'INSERT INTO timer VALUES ("{uid}", {enums.Timer.FAMILY_CHECK_IN.value}, "{time}") ON DUPLICATE KEY UPDATE `time` = "{time}";', **kwargs)
	await common.execute(f'UPDATE family SET exp = exp + 1 WHERE name = "{name}";', **kwargs)
	_, iid, cost = (common.decode_items(kwargs['config']['family']['general']['rewards']['check_in']))[0]
	_, remaining = await common.try_item(uid, iid, cost, **kwargs)
	return common.mt(0, 'success', {'iid' : iid.value, 'value' : remaining})

async def gift_package(uid, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in family')
	data = await common.execute(f'SELECT uid FROM `familyrole` WHERE `name` = "{name}";', **kwargs)
	members = [m[0] for m in data]
	for member in members:
		for item in kwargs['config']['family']['store']['gift']:
			_, iid, cost = (common.decode_items(item))[0]
			await common.try_item(member, iid, cost, **kwargs)
	await _record_family_change(name, f'{await common.get_gn(uid, **kwargs)} purchased family gift package.', **kwargs)
	return common.mt(0, 'success')

async def get_random(**kwargs):
	data = await common.execute(f'SELECT `name`, `icon`, `exp`, `notice` FROM `family` ORDER BY RAND() LIMIT 10;', **kwargs)
	return common.mt(0, 'success', {'families' : [{'name' : f[0], 'icon' : f[1], 'exp' : f[2], 'notice' : f[3]} for f in data]})

async def config(**kwargs):
	return common.mt(0, 'success', data={'config': kwargs['config']['family']})


########################################################################
SET_ROLE_PERMISSIONS = {\
		enums.FamilyRole.OWNER : {'target' : {enums.FamilyRole.ADMIN, enums.FamilyRole.ELITE, enums.FamilyRole.BASIC}, 'new' : {enums.FamilyRole.ADMIN, enums.FamilyRole.ELITE, enums.FamilyRole.BASIC}},
		enums.FamilyRole.ADMIN : {'target' : {enums.FamilyRole.ELITE, enums.FamilyRole.BASIC}, 'new' : {enums.FamilyRole.ELITE, enums.FamilyRole.BASIC}}
		}

def _valid_family_name(name):
	return bool(name)

def _check_disband_permissions(check):
	return check >= enums.FamilyRole.ADMIN

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

async def _get_check_in_timer(uid, **kwargs):
	timer = await common.execute(f'SELECT time FROM `timer` WHERE uid = "{uid}" AND tid = {enums.Timer.FAMILY_CHECK_IN.value};', **kwargs)
	return None if timer == () else datetime.strptime(timer[0][0], '%Y-%m-%d').replace(tzinfo = timezone.utc)

# TODO parallelize with asyncio.gather and asyncio tasks
async def _delete_family(name, **kwargs):
	await _delete_disband_timer(name, **kwargs)
	data = await common.execute(f'SELECT uid FROM `familyrole` WHERE `name` = "{name}";', **kwargs)
	members = [m[0] for m in data]
	for member in members:
		await common.execute(f'UPDATE `player` SET fid = "" WHERE uid = "{member}";', **kwargs)
	await common.execute(f'DELETE FROM `familyrole` WHERE `name` = "{name}";', **kwargs)
	await common.execute(f'DELETE FROM `familyhistory` WHERE `name` = "{name}";', **kwargs)
	await common.execute(f'DELETE FROM `family` WHERE `name` = "{name}";', **kwargs)

async def _get_disband_timer(name, **kwargs):
	owner_uid = await common.execute(f'SELECT uid FROM `familyrole` WHERE `name` = "{name}" AND `role` = {enums.FamilyRole.OWNER};', **kwargs)
	timer = await common.execute(f'SELECT time FROM `timer` WHERE uid = "{owner_uid[0][0]}" AND tid = {enums.Timer.FAMILY_DISBAND.value};', **kwargs)
	return None if timer == () else datetime.strptime(timer[0][0], '%Y-%m-%d %H:%M:%S').replace(tzinfo = timezone.utc)

async def _set_disband_timer(name, **kwargs):
	owner_uid = await common.execute(f'SELECT uid FROM `familyrole` WHERE `name` = "{name}" AND `role` = {enums.FamilyRole.OWNER};', **kwargs)
	seconds = 3600 * 24
	time = (datetime.now(timezone.utc) + timedelta(seconds=seconds)).strftime('%Y-%m-%d %H:%M:%S')
	await common.execute(f'INSERT INTO `timer` VALUES ("{owner_uid[0][0]}", {enums.Timer.FAMILY_DISBAND.value}, "{time}");', **kwargs)
	return seconds

async def _delete_disband_timer(name, **kwargs):
	owner_uid = await common.execute(f'SELECT uid FROM `familyrole` WHERE `name` = "{name}" AND `role` = {enums.FamilyRole.OWNER};', **kwargs)
	await common.execute(f'DELETE FROM `timer` WHERE uid = "{owner_uid[0][0]}" AND tid = {enums.Timer.FAMILY_DISBAND.value};', **kwargs)

async def _count_members(name, **kwargs):
	count = await common.execute(f'SELECT COUNT(*) FROM familyrole WHERE `name` = "{name}";', **kwargs)
	return count[0][0]

async def _get_family_changes(name, **kwargs):
	data = await common.execute(f'SELECT `date`, `msg` FROM familyhistory WHERE `name` = "{name}" ORDER BY `hid` LIMIT 30;', **kwargs)
	return data

async def _record_family_change(name, msg, **kwargs):
	await common.execute(f'INSERT INTO familyhistory(name, date, msg) VALUES("{name}", "{datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}", "{msg}");', **kwargs)

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
	if data == () or ('',) in data: return False, ''
	return True, data[0][0]

async def _get_role(uid, name, **kwargs):
	data = await common.execute(f'SELECT role FROM familyrole WHERE uid = "{uid}" AND `name` = "{name}";', **kwargs)
	return enums.FamilyRole(data[0][0])


async def _get_uid_officials(name, **kwargs):
	data = await common.execute(f'SELECT uid FROM familyrole WHERE `name` = "{name}" AND `role` >= {enums.FamilyRole.ADMIN.value};', **kwargs)
	return None if data == () else [u[0] for u in data]

async def _lookup_nonce(nonce, **kwargs):
	async with kwargs['session'].post(kwargs['tokenserverbaseurl'] + '/redeem_nonce_new', json = {'nonce' : [nonce]}) as resp:
		data = await resp.json(content_type = 'text/json')
		return (None, None) if data[nonce]['status'] != 0 else (data[nonce]['name'], data[nonce]['uid_target'])

async def _remove_from_family(uid, name, **kwargs):
	await asyncio.gather(common.execute(f'UPDATE player SET fid = "" WHERE uid = "{uid}";', **kwargs),
			common.execute(f'DELETE FROM familyrole WHERE uid = "{uid}" AND name = "{name}";', **kwargs))
