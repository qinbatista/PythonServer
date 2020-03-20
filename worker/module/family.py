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

from datetime import datetime, timedelta


async def create(uid, name, icon, **kwargs):
	"""icon必须为整型或者数字字符串"""
	exp_info = await stage.increase_exp(uid, 0, **kwargs)
	if exp_info["level"] < kwargs['config']['family']['general']['player_level']: return common.mt(95, "you must over level 18")
	if not _valid_family_name(name): return common.mt(99, 'invalid family name')
	in_family, _ = await _in_family(uid, **kwargs)
	if in_family: return common.mt(98, 'already in a family')
	_, iid, cost = (common.decode_items(kwargs['config']['family']['general']['costs']['create']))[0]
	if await common.exists('family', ('name', name), **kwargs): return common.mt(96, 'name already exists!')
	enough, remaining = await common.try_item(uid, iid, -cost, **kwargs)
	if not enough: return common.mt(97, 'insufficient materials')
	# 以下语句必须顺序执行
	await common.execute(f'INSERT INTO family(name, icon) VALUES("{name}", {icon});', **kwargs)
	await common.execute(f'UPDATE player SET fid = "{name}" WHERE uid = "{uid}";', **kwargs)
	await common.execute(f'UPDATE familyrole SET role = "{enums.FamilyRole.OWNER.value}" WHERE uid = "{uid}" AND name = "{name}";', **kwargs)
	return common.mt(0, 'created family', {'name' : name, 'icon': icon, 'iid' : iid.value, 'value' : remaining})

async def leave(uid, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in a family')
	role = await _get_role(uid, name, **kwargs)
	if role == enums.FamilyRole.OWNER: return common.mt(98, 'owner can not leave family')
	days = kwargs['config']['family']['general']['leave_days']
	await common.execute(f'INSERT INTO item (uid, iid, value) VALUES ("{uid}", "{enums.Item.FAMILY_COIN_RECORD.value}", 0) ON DUPLICATE KEY UPDATE `value`= 0', **kwargs)
	await common.execute(f'INSERT INTO timer (uid, tid, time) VALUES ("{uid}", {enums.Timer.FAMILY_JOIN_END.value}, "{(datetime.now(tz=common.TZ_SH) + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")}") ON DUPLICATE KEY UPDATE `time`= "{(datetime.now(tz=common.TZ_SH) + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")}";', **kwargs)
	await _remove_from_family(uid, name, **kwargs)
	gn = await common.get_gn(uid, **kwargs)
	await _record_family_change(name, f'{enums.FamilyHistoryKeys.LEAVE.value}:{gn}', **kwargs)
	return common.mt(0, 'left family', {"cd_time": days * 24 * 3600})

async def remove_user(uid, gn_target, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in a family')
	role = await _get_role(uid, name, **kwargs)
	uid_target = await common.get_uid(gn_target, **kwargs)
	if uid == uid_target: return common.mt(96, "You can't remove yourself")
	rmtimes, rmtimer = await _rmtimes_timer(name, **kwargs)
	if rmtimes == 0: return common.mt(94, "We have run out of members to remove today", {"cd_time": common.remaining_cd()})
	rmtimes -= 1
	in_family, name_target = await _in_family(uid_target, **kwargs)
	if not in_family: return common.mt(95, "target doesn't have a family")
	if name_target != name: return common.mt(98, 'target is not in your family')
	role_target = await _get_role(uid_target, name, **kwargs)
	if not _check_remove_permissions(role, role_target): return common.mt(97, 'insufficient permissions')
	await _remove_from_family(uid_target, name, **kwargs)
	await common.execute(f'UPDATE family SET rmtimes={rmtimes} WHERE name = "{name}";', **kwargs)
	gn = await common.get_gn(uid, **kwargs)
	await _record_family_change(name, f'{enums.FamilyHistoryKeys.REMOVE.value}:{gn},{gn_target}', **kwargs)
	return common.mt(0, 'removed user', {'gn' : gn_target, 'rmtimes': rmtimes, "cd_time": common.remaining_cd()})

async def invite_user(uid, gn_target, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in a family')
	role = await _get_role(uid, name, **kwargs)
	if not _check_invite_permissions(role): return common.mt(98, 'insufficient permissions')
	uid_target = await common.get_uid(gn_target, **kwargs)
	if uid_target == "": return common.mt(93, 'The invited user does not exist')
	join_data = await common.execute(f'SELECT time FROM timer WHERE uid="{uid_target}" AND tid="{enums.Timer.FAMILY_JOIN_END.value}";', **kwargs)
	if join_data != () and datetime.strptime(join_data[0][0], "%Y-%m-%d %H:%M:%S").replace(tzinfo=common.TZ_SH) > datetime.now(tz=common.TZ_SH):
		seconds = int((datetime.strptime(join_data[0][0], "%Y-%m-%d %H:%M:%S").replace(tzinfo=common.TZ_SH) - datetime.now(tz=common.TZ_SH)).total_seconds())
		return common.mt(96, 'The invitation to the object to leave the family cooldown has not ended', {'seconds': seconds})
	exp_info = await stage.increase_exp(uid_target, 0, **kwargs)
	if exp_info["level"] < kwargs['config']['family']['general']['player_level']: return common.mt(95, "邀请对象等级不满18级")
	in_family_target, _ = await _in_family(uid_target, **kwargs)
	if in_family_target: return common.mt(94, 'The invitee has already joined the family')
	# 以下是邀请成员限制的代码
	owner_data = await common.execute(f'SELECT limits.value, timer.time FROM familyrole JOIN (limits, timer) ON (familyrole.uid=limits.uid AND limits.lid={enums.Limits.FAMILY_INVITE} AND familyrole.uid=timer.uid AND timer.tid={enums.Timer.FAMILY_INVITE_END}) WHERE familyrole.name="{name}" AND familyrole.role={enums.FamilyRole.OWNER};', **kwargs)
	limit, itime = owner_data[0] if owner_data != () else (kwargs["config"]["family"]["general"]["itimes"], (datetime.now(tz=common.TZ_SH) + timedelta(days=1)).strftime("%Y-%m-%d"))
	if datetime.strptime(itime, "%Y-%m-%d").replace(tzinfo=common.TZ_SH) <= datetime.now(tz=common.TZ_SH):
		limit = kwargs["config"]["family"]["general"]["itimes"] - 1
		itime = (datetime.now(tz=common.TZ_SH) + timedelta(days=1)).strftime("%Y-%m-%d")
	elif limit == 0:
		return common.mt(91, "We've run out of invitations today")
	else:
		limit -= 1
	sent = await mail.send_mail({'type' : enums.MailType.FAMILY_REQUEST.value, 'from' : name, \
			'subj' : enums.MailTemplate.FAMILY_INVITATION.name, 'body' : '', 'uid_target' : uid_target, \
			'name' : name}, uid_target, **kwargs)
	if sent[uid_target]['status'] == 1:
		return common.mt(92, 'target mailbox full')
	if sent[uid_target]['status'] != 0:
		return common.mt(97, 'internal mail error')
	await asyncio.gather(
		common.execute(f'INSERT INTO limits (uid, lid, value) SELECT familyrole.uid, {enums.Limits.FAMILY_INVITE}, {limit} FROM familyrole WHERE familyrole.`name` = "{name}" AND familyrole.`role` = {enums.FamilyRole.OWNER} ON DUPLICATE KEY UPDATE limits.value={limit};', **kwargs),
		common.execute(f'INSERT INTO timer (uid, tid, time) SELECT familyrole.uid, {enums.Timer.FAMILY_INVITE_END}, "{itime}" FROM familyrole WHERE familyrole.`name` = "{name}" AND familyrole.`role` = {enums.FamilyRole.OWNER} ON DUPLICATE KEY UPDATE timer.time = "{itime}";', **kwargs)
	)
	gn = await common.get_gn(uid, **kwargs)
	await _record_family_change(name, f'{enums.FamilyHistoryKeys.INVITE.value}:{gn},{gn_target}', **kwargs)
	return common.mt(0, 'invited user', {'gn' : gn_target, 'times': limit})

async def request_join(uid, name, **kwargs):
	in_family, _ = await _in_family(uid, **kwargs)
	if in_family: return common.mt(99, 'already in a family')
	gn = await common.get_gn(uid, **kwargs)
	officials = await _get_uid_officials(name, **kwargs)
	if officials is None: return common.mt(98, 'invalid family')
	join_data = await common.execute(f'SELECT time FROM timer WHERE uid="{uid}" AND tid="{enums.Timer.FAMILY_JOIN_END}";', **kwargs)
	if join_data != () and datetime.strptime(join_data[0][0], "%Y-%m-%d %H:%M:%S").replace(tzinfo=common.TZ_SH) > datetime.now(tz=common.TZ_SH):
		seconds = int((datetime.strptime(join_data[0][0], "%Y-%m-%d %H:%M:%S").replace(tzinfo=common.TZ_SH) - datetime.now(tz=common.TZ_SH)).total_seconds())
		return common.mt(96, 'Leaving the family cooldown is not over', {'seconds': seconds})
	exp_info = await stage.increase_exp(uid, 0, **kwargs)
	if exp_info["level"] < kwargs['config']['family']['general']['player_level']: return common.mt(95, "Your rating is below 18", {'exp_info': exp_info})
	# 以下是申请加入家族次数的限制代码
	now = datetime.now(tz=common.TZ_SH)
	lim, tim = await asyncio.gather(common.get_limit(uid, enums.Limits.FAMILY_JOIN, **kwargs), common.get_timer(uid, enums.Timer.FAMILY_JOIN, timeformat='%Y-%m-%d', **kwargs))
	lim, tim = (kwargs["config"]["family"]["general"]["jtimes"] - 1, now + timedelta(days=1)) if tim is None or tim < now else (lim - 1, tim)
	if lim < 0: return common.mt(94, "You haven't applied enough to join the family today")
	await asyncio.gather(common.set_timer(uid, enums.Timer.FAMILY_JOIN, tim, timeformat='%Y-%m-%d', **kwargs), common.set_limit(uid, enums.Limits.FAMILY_JOIN, lim, **kwargs))

	sent = await mail.send_mail({'type' : enums.MailType.FAMILY_REQUEST.value, 'from' : gn, \
			'subj' : enums.MailTemplate.FAMILY_REQUEST.name, 'body' : '', 'uid_target' : uid, \
			'name' : name}, *officials, **kwargs)
	for s in sent.values():
		if s['status'] == 0:
			return common.mt(0, 'requested join', {'name': name, 'lim': lim, 'cooling': common.remaining_cd()})
	return common.mt(97, 'request could not be sent')

async def respond(uid, nonce, **kwargs):
	name, uid_target = await _lookup_nonce(nonce, **kwargs)
	if not name: return common.mt(99, 'invalid nonce')
	await mail.delete_mail(uid, nonce, **kwargs)
	in_family, _ = await _in_family(uid_target, **kwargs)
	if in_family: return common.mt(98, 'target user is already in family')
	exists, info = await _get_family_info(name, 'icon', 'exp', 'notice', 'board', **kwargs)
	if not exists: return common.mt(97, 'family no longer exists')
	member_count = await _count_members(name, **kwargs)
	if member_count >= kwargs['config']['family']['general']['members']['max']: return common.mt(96, 'family is full')
	await _add_to_family(uid_target, name, **kwargs)
	gn_target = await common.get_gn(uid_target, **kwargs)
	gn = await common.get_gn(uid, **kwargs)
	await _record_family_change(name, f'{enums.FamilyHistoryKeys.RESPOND.value}:{gn},{gn_target}', **kwargs)
	return common.mt(0, 'success', {'name' : name, 'icon' : info[0], 'exp' : info[1], 'notice' : info[2], 'board' : info[3]})

async def get_all(uid, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in a family')
	timer = await _get_disband_timer(name, **kwargs)
	if await _check_delete_family(timer, name, **kwargs): return common.mt(99, 'not in a family')
	_, info = await _get_family_info(name, 'icon', 'exp', 'notice', 'board', **kwargs)
	members = await _get_member_info(name, **kwargs)
	news = await _get_family_changes(name, **kwargs)
	checkin_data = await common.execute(f'SELECT time FROM timer WHERE uid="{uid}" AND tid="{enums.Timer.FAMILY_CHECK_IN}";', **kwargs)
	is_checkin = 0 if checkin_data == () else (0 if datetime.strptime(checkin_data[0][0], "%Y-%m-%d").replace(tzinfo=common.TZ_SH) < datetime.now(tz=common.TZ_SH) else 1)
	return common.mt(0, 'success', {'name' : name, 'icon' : info[0], 'exp' : info[1], 'notice' : info[2], 'board' : info[3], 'members' : members, 'news' : news, 'timer' : -1 if timer is None else int((timer-datetime.now(tz=common.TZ_SH)).total_seconds()), 'is_checkin': is_checkin})

async def get_store(**kwargs):
	return common.mt(0, 'success', {'merchandise' : [{'item' : k, 'cost' : v} for k, v in kwargs['config']['family']['store']['items'].items()]})

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
	await _record_family_change(name, f'{enums.FamilyHistoryKeys.PURCHASE.value}:{gn}', **kwargs)
	return common.mt(0, 'success', { enums.Group.ITEM.value : [ {'iid' : i[1], 'value' : item_remaining}, {'iid' : c[1], 'value' : cost_remaining}]})

async def set_notice(uid, msg, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in family')
	role = await _get_role(uid, name, **kwargs)
	if not _check_notice_permissions(role): return common.mt(98, 'insufficient permissions')
	# 以下是公告次数限制的代码
	owner_data = await common.execute(f'SELECT limits.value, timer.time FROM familyrole JOIN (limits, timer) ON (familyrole.uid=limits.uid AND limits.lid={enums.Limits.FAMILY_NOTICE} AND familyrole.uid=timer.uid AND timer.tid={enums.Timer.FAMILY_NOTICE_END}) WHERE familyrole.name="{name}" AND familyrole.role={enums.FamilyRole.OWNER};', **kwargs)
	now = datetime.now(tz=common.TZ_SH)
	limit, ntime = (kwargs["config"]["family"]["general"]["ntimes"], (now + timedelta(days=1)).strftime("%Y-%m-%d")) if owner_data == () else owner_data[0]
	if datetime.strptime(ntime, "%Y-%m-%d").replace(tzinfo=common.TZ_SH) <= now:
		limit, ntime = kwargs["config"]["family"]["general"]["ntimes"] - 1, (now + timedelta(days=1)).strftime("%Y-%m-%d")
	elif limit == 0:
		return common.mt(97, 'The number of announcements today has been used up')
	else:
		limit -= 1
	await asyncio.gather(
		common.execute(f'INSERT INTO limits (uid, lid, value) SELECT familyrole.uid, {enums.Limits.FAMILY_NOTICE}, {limit} FROM familyrole WHERE familyrole.`name` = "{name}" AND familyrole.`role` = {enums.FamilyRole.OWNER} ON DUPLICATE KEY UPDATE limits.value={limit};', **kwargs),
		common.execute(f'INSERT INTO timer (uid, tid, time) SELECT familyrole.uid, {enums.Timer.FAMILY_NOTICE_END}, "{ntime}" FROM familyrole WHERE familyrole.`name` = "{name}" AND familyrole.`role` = {enums.FamilyRole.OWNER} ON DUPLICATE KEY UPDATE timer.time = "{ntime}";', **kwargs)
	)
	#  ##############################
	await common.execute(f'UPDATE family SET notice = "{msg}" WHERE `name` = "{name}";', **kwargs)
	return common.mt(0, 'success', {'notice' : msg, 'limit': limit, 'seconds': common.remaining_cd()})

async def set_blackboard(uid, msg, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in family')
	role = await _get_role(uid, name, **kwargs)
	if not _check_blackboard_permissions(role): return common.mt(98, 'insufficient permissions')
	await common.execute(f'UPDATE family SET board = "{msg}" WHERE `name` = "{name}";', **kwargs)
	return common.mt(0, 'success', {'board' : msg})

async def set_icon(uid, icon, **kwargs):
	if icon < 0: return common.mt(99, 'Wrong icon number')
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(98, "You don't have a family.")
	role = await _get_role(uid, name, **kwargs)
	if not _check_blackboard_permissions(role): return common.mt(97, 'You have no access.')
	_, ic = await _get_family_info(name, 'icon', **kwargs)
	if ic[0] == icon: return common.mt(96, 'Cannot be set to the original icon')
	await common.execute(f'UPDATE family SET icon={icon} WHERE name="{name}";', **kwargs)
	gn = await common.get_gn(uid, **kwargs)
	await _record_family_change(name, f'{enums.FamilyHistoryKeys.ICON.value}:{gn}', **kwargs)
	return common.mt(0, 'success', {'icon': icon})

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
	if targets_role == new_role: return common.mt(94, 'Membership has always been this identity')
	if not _check_set_role_permissions(actors_role, targets_role, new_role): return common.mt(96, 'insufficient permissions')
	await common.execute(f'UPDATE familyrole SET role = {new_role.value} WHERE uid = "{uid_target}" AND `name` = "{name}";', **kwargs)
	gn = await common.get_gn(uid, **kwargs)
	await _record_family_change(name, f'{enums.FamilyHistoryKeys.ROLE.value}:{gn},{gn_target}', **kwargs)
	return common.mt(0, 'success', {'gn' : gn_target, 'role' : new_role.value})

async def change_name(uid, new_name, **kwargs):
	if not _valid_family_name(new_name): return common.mt(99, 'invalid family name')
	can_change, _ = await _get_family_info(new_name, 'icon', **kwargs)
	if can_change: return common.mt(95, 'Family names have been used')
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(98, 'not in family')
	role = await _get_role(uid, name, **kwargs)
	if not _check_change_name_permissions(role): return common.mt(97, 'insufficient permissions')
	_, iid, cost = (common.decode_items(kwargs['config']['family']['general']['costs']['change_name']))[0]
	can_pay, remaining = await common.try_item(uid, iid, -cost, **kwargs)
	if not can_pay: return common.mt(96, 'insufficient funds')
	await common.execute(f'UPDATE family SET name = "{new_name}" WHERE name = "{name}";', **kwargs)
	gn = await common.get_gn(uid, **kwargs)
	await _record_family_change(new_name, f'{enums.FamilyHistoryKeys.CHANGE_NAME.value}:{gn}', **kwargs)
	return common.mt(0, 'success', {'name' : new_name, 'iid' : iid.value, 'value' : remaining})

async def disband(uid, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in family')
	role = await _get_role(uid, name, **kwargs)
	if not _check_disband_permissions(role): return common.mt(98, 'insufficient permissions')
	timer = await _get_disband_timer(name, **kwargs)
	if timer is not None: return common.mt(97, 'family already disbanded')
	timer = await _set_disband_timer(name, **kwargs)
	gn = await common.get_gn(uid, **kwargs)
	await _record_family_change(name, f'{enums.FamilyHistoryKeys.DISBAND.value}:{gn}', **kwargs)
	return common.mt(0, 'success', {'timer' : timer})

async def cancel_disband(uid, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in family')
	role = await _get_role(uid, name, **kwargs)
	if not _check_disband_permissions(role): return common.mt(98, 'insufficient permissions')
	timer = await _get_disband_timer(name, **kwargs)
	if timer is None: return common.mt(97, 'family is not disbanded')
	await _delete_disband_timer(name, **kwargs)
	gn = await common.get_gn(uid, **kwargs)
	await _record_family_change(name, f'{enums.FamilyHistoryKeys.CANCEL_DISBAND.value}:{gn}', **kwargs)
	return common.mt(0, 'success')

async def check_in(uid, **kwargs):
	kwargs.update({"task_id":enums.Task.FAMILY_CHECK_IN})
	await task.record_task(uid,**kwargs)

	kwargs.update({"aid":enums.Achievement.CHECK_IN_FAMILY})
	await achievement.record_achievement(kwargs['data']['unique_id'],**kwargs)

	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in family')
	timer = await _get_check_in_timer(uid, **kwargs)
	now = datetime.now(tz=common.TZ_SH)
	if timer is not None and now < timer: return common.mt(98, 'already checked in today')
	time = (now + timedelta(days=1)).strftime('%Y-%m-%d')

	await common.execute(f'INSERT INTO timer VALUES ("{uid}", {enums.Timer.FAMILY_CHECK_IN}, "{time}") ON DUPLICATE KEY UPDATE `time` = "{time}";', **kwargs)
	exp_data = await increase_exp(name, 1, **kwargs)
	# 增加家族金币和记录金币
	_, iid_fc, cost_fc = (common.decode_items(kwargs['config']['family']['general']['rewards']['family_coin']))[0]
	_, remain_fc  = await common.try_item(uid, iid_fc, cost_fc, **kwargs)
	_, remain_fcr = await common.try_item(uid, enums.Item.FAMILY_COIN_RECORD, cost_fc, **kwargs)
	data = {'remaining': [{"iid": iid_fc.value, "value": remain_fc}, {"iid": enums.Item.FAMILY_COIN_RECORD.value, "value": remain_fcr}],
			'reward':    [{"iid": iid_fc.value, "value": cost_fc},   {"iid": enums.Item.FAMILY_COIN_RECORD.value, "value": cost_fc}],
			'exp_data':  exp_data}
	items = common.decode_items(','.join(kwargs['config']['family']['general']['rewards']['special']))
	for _, iid, cost in items:
		_, remain = await common.try_item(uid, iid, cost, **kwargs)
		data['remaining'].append({"iid": iid.value, "value": remain})
		data['reward'].append({"iid": iid.value, "value": cost})
	return common.mt(0, 'success', data)

async def abdicate(uid, target, **kwargs):
	"""族长让位给族员"""
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, "You don't have a family.")
	target_uid = await common.get_uid(target, **kwargs)
	if target_uid == "": return common.mt(98, "The target object does not exist")
	in_family, target_name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(97, 'Objects have no family')
	if name != target_name: return common.mt(96, 'You and your partner are not in the same family')
	actors_role = await _get_role(uid, name, **kwargs)
	if actors_role != enums.FamilyRole.OWNER: return common.mt(95, 'You are not a patriarch.')
	gn = await common.get_gn(uid, **kwargs)
	await asyncio.gather(
		_delete_disband_timer(name, **kwargs),
		common.execute(f'INSERT INTO limits (uid, lid, value) SELECT "{target_uid}", {enums.Limits.FAMILY_INVITE}, (@v:=limits.value) FROM limits WHERE uid="{uid}" AND lid={enums.Limits.FAMILY_INVITE} ON DUPLICATE KEY UPDATE value=@v;', **kwargs),
		common.execute(f'INSERT INTO limits (uid, lid, value) SELECT "{target_uid}", {enums.Limits.FAMILY_NOTICE}, (@v:=limits.value) FROM limits WHERE uid="{uid}" AND lid={enums.Limits.FAMILY_NOTICE} ON DUPLICATE KEY UPDATE value=@v;', **kwargs),
		common.execute(f'INSERT INTO timer (uid, tid, time) SELECT "{target_uid}", {enums.Timer.FAMILY_INVITE_END}, (@t:=timer.time) FROM timer WHERE uid="{uid}" AND tid={enums.Timer.FAMILY_INVITE_END} ON DUPLICATE KEY UPDATE time=@t;', **kwargs),
		common.execute(f'INSERT INTO timer (uid, tid, time) SELECT "{target_uid}", {enums.Timer.FAMILY_NOTICE_END}, (@t:=timer.time) FROM timer WHERE uid="{uid}" AND tid={enums.Timer.FAMILY_NOTICE_END} ON DUPLICATE KEY UPDATE time=@t;', **kwargs)
	)
	await common.execute(f'UPDATE familyrole SET role = {enums.FamilyRole.BASIC} WHERE uid = "{uid}" AND `name` = "{name}";', **kwargs)
	await common.execute(f'UPDATE familyrole SET role = {enums.FamilyRole.OWNER} WHERE uid = "{target_uid}" AND `name` = "{name}";', **kwargs)
	await _record_family_change(name, f'{enums.FamilyHistoryKeys.ABDICATE.value}:{gn},{target}', **kwargs)
	return common.mt(0, 'success', {gn: enums.FamilyRole.BASIC.value, target: enums.FamilyRole.OWNER.value})

# TODO 内部方法
async def welfare(uid, **kwargs):
	in_family, name = await _in_family(uid, **kwargs)
	if not in_family: return common.mt(99, 'not in family')
	data = await common.execute(f'SELECT uid FROM `familyrole` WHERE `name` = "{name}";', **kwargs)
	members = [m[0] for m in data]
	del data
	data = {'remaining': [], 'reward': []}
	for member in members:
		for item in kwargs['config']['family']['store']['gift']:
			_, iid, cost = (common.decode_items(item))[0]
			_, qty = await common.try_item(member, iid, cost, **kwargs)
			data['remaining'].append({'iid': iid.value, 'qty': qty})
			data['reward'].append({'iid': iid.value, 'qty': cost})
	await _record_family_change(name, f'{enums.FamilyHistoryKeys.PURCHASE.value}:{await common.get_gn(uid, **kwargs)}', **kwargs)
	return common.mt(0, 'success', data)

async def search(name, **kwargs):
	can, info = await _get_family_info(name, 'icon', 'exp', 'notice', 'board', **kwargs)
	if not can: return common.mt(99, f'There is no <{name}> family')
	people = (await common.execute(f'SELECT COUNT(*) FROM player WHERE fid="{name}";', **kwargs))[0][0]
	return common.mt(0, 'success', {'info': {'name': name, 'icon': info[0], 'exp': info[1], 'notice': info[2], 'board': info[3], 'people': people}})

async def get_random(number=5, **kwargs):
	data = await common.execute(f'SELECT `name`, `icon`, `exp`, `notice`, `board` FROM `family` ORDER BY RAND() LIMIT {number};', **kwargs)
	return common.mt(0, 'success', {'families': [{'name': f[0], 'icon': f[1], 'exp': f[2], 'notice': f[3], 'board': f[4],
			'people': (await common.execute(f'SELECT COUNT(*) FROM player WHERE fid="{f[0]}";', **kwargs))[0][0]} for f in data]})

async def config(**kwargs):
	return common.mt(0, 'success', data={'config': kwargs['config']['family']})


########################################################################
SET_ROLE_PERMISSIONS = {
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
	return None if timer == () else datetime.strptime(timer[0][0], '%Y-%m-%d').replace(tzinfo=common.TZ_SH)

async def _check_delete_family(timer, name, **kwargs):
	if timer is not None and datetime.now(tz=common.TZ_SH) > timer:
		await _delete_disband_timer(name, **kwargs)
		await common.execute(f'DELETE FROM `family` WHERE `name` = "{name}";', **kwargs)
		return True
	return False

async def _get_disband_timer(name, **kwargs):
	owner_uid = await common.execute(f'SELECT uid FROM `familyrole` WHERE `name` = "{name}" AND `role` = {enums.FamilyRole.OWNER};', **kwargs)
	timer = await common.execute(f'SELECT time FROM `timer` WHERE uid = "{owner_uid[0][0]}" AND tid = {enums.Timer.FAMILY_DISBAND};', **kwargs)
	return None if timer == () else datetime.strptime(timer[0][0], '%Y-%m-%d %H:%M:%S').replace(tzinfo=common.TZ_SH)

async def _set_disband_timer(name, **kwargs):
	owner_uid = await common.execute(f'SELECT uid FROM `familyrole` WHERE `name` = "{name}" AND `role` = {enums.FamilyRole.OWNER};', **kwargs)
	seconds = int(3600 * kwargs['config']['family']['general']['disband_hours'])
	time = (datetime.now(tz=common.TZ_SH) + timedelta(seconds=seconds)).strftime('%Y-%m-%d %H:%M:%S')
	await common.execute(f'INSERT INTO `timer` VALUES ("{owner_uid[0][0]}", {enums.Timer.FAMILY_DISBAND.value}, "{time}");', **kwargs)
	return seconds

async def _delete_disband_timer(name, **kwargs):
	owner_uid = await common.execute(f'SELECT uid FROM `familyrole` WHERE `name` = "{name}" AND `role` = {enums.FamilyRole.OWNER};', **kwargs)
	await common.execute(f'DELETE FROM `timer` WHERE uid = "{owner_uid[0][0]}" AND tid = {enums.Timer.FAMILY_DISBAND};', **kwargs)

async def _count_members(name, **kwargs):
	count = await common.execute(f'SELECT COUNT(*) FROM familyrole WHERE `name` = "{name}";', **kwargs)
	return count[0][0]

async def _get_family_changes(name, **kwargs):
	data = await common.execute(f'SELECT `date`, `msg` FROM familyhistory WHERE `name` = "{name}" ORDER BY `hid` LIMIT 30;', **kwargs)
	return data

async def _record_family_change(name, msg, **kwargs):
	await common.execute(f'INSERT INTO familyhistory(name, date, msg) VALUES("{name}", "{datetime.now(tz=common.TZ_SH).strftime("%Y-%m-%d %H:%M:%S")}", "{msg}");', **kwargs)

async def _get_member_info(name, **kwargs):
	# await __insert(name, **kwargs)
	data = await common.execute(f'SELECT player.gn, progress.role, familyrole.role, progress.exp, timer.time, item.value, i2.value FROM familyrole JOIN player ON player.uid = familyrole.uid JOIN progress ON progress.uid = familyrole.uid join timer on timer.uid = familyrole.uid and timer.tid={enums.Timer.LOGIN_TIME} join item on item.uid = familyrole.uid and item.iid ={enums.Item.FAMILY_COIN} join item as i2 on i2.uid = familyrole.uid and i2.iid ={enums.Item.FAMILY_COIN_RECORD} WHERE familyrole.name = "{name}";', **kwargs)
	return [{'gn' : m[0], 'player_role' : m[1], 'family_role' : m[2], 'exp' : m[3], 'last_login' : m[4], 'family_coin' : m[5], 'family_coin_record' : m[6]} for m in data]

async def _get_family_info(name, *args, **kwargs):
	data = await common.execute(f'SELECT {",".join(args)} FROM family WHERE name = "{name}";', **kwargs)
	return (True, data[0]) if data != () else (False, ())

async def _add_to_family(uid, name, **kwargs):
	await common.execute(f'UPDATE player SET fid = "{name}" WHERE uid = "{uid}";', **kwargs)

async def _in_family(uid, **kwargs):
	data = await common.execute(f'SELECT fid FROM player WHERE uid = "{uid}";', **kwargs)
	if data == () or (None,) in data: return False, None
	return True, data[0][0]

async def _get_role(uid, name, **kwargs):
	data = await common.execute(f'SELECT role FROM familyrole WHERE uid = "{uid}" AND `name` = "{name}";', **kwargs)
	return enums.FamilyRole(data[0][0])


async def _get_uid_officials(name, **kwargs):
	data = await common.execute(f'SELECT uid FROM familyrole WHERE `name` = "{name}" AND `role` >= {enums.FamilyRole.ADMIN.value};', **kwargs)
	return None if data == () else [u[0] for u in data]

async def _lookup_nonce(nonce, **kwargs):
	async with kwargs['session'].post(kwargs['tokenserverbaseurl'] + '/redeem_nonce', \
			json = {'keys' : [nonce]}) as resp:
		data = await resp.json()
		return (None, None) if data[nonce]['status'] != 0 else (data[nonce]['name'], data[nonce]['uid_target'])

async def _remove_from_family(uid, name, **kwargs):
	await asyncio.gather(common.execute(f'UPDATE player SET fid = NULL WHERE uid = "{uid}";', **kwargs),
			common.execute(f'DELETE FROM familyrole WHERE uid = "{uid}" AND name = "{name}";', **kwargs))

async def _rmtimes_timer(name, **kwargs):
	data = await common.execute(f'SELECT rmtimes, rmtimer FROM family WHERE name = "{name}";', **kwargs)
	rmtimes, rmtimer = data[0]
	if rmtimer == '' or rmtimer != datetime.now(tz=common.TZ_SH).strftime("%Y-%m-%d"):
		await common.execute(f'UPDATE family SET rmtimes={kwargs["config"]["family"]["general"]["rmtimes"]}, rmtimer="{datetime.now(tz=common.TZ_SH).strftime("%Y-%m-%d")}" WHERE name = "{name}";', **kwargs)
		data = await common.execute(f'SELECT rmtimes, rmtimer FROM family WHERE name = "{name}";', **kwargs)
		rmtimes, rmtimer = data[0]
	return rmtimes, rmtimer

async def increase_exp(name, exp, **kwargs):
	"""增加家族经验
	exp为0则获得经验，反之取绝对值增加经验，
	并返回总经验和等级，升到下一级需要的经验
	"""
	# TODO 取配置和数据
	exp_config = kwargs['config']['family']['level']['exp']
	_, fds = await _get_family_info(name, 'exp', **kwargs)
	sql_exp = fds[0]
	# TODO 计算等级和需要的经验
	level, need = common.__calculate(exp_config, sql_exp)
	if exp == 0: return {'exp': sql_exp, 'level': level, 'need': need, 'reward': exp}
	# TODO 重新计算等级和需要的经验
	sql_exp += exp
	level, need = common.__calculate(exp_config, sql_exp)
	await common.update_famliy(name, 'exp', sql_exp, **kwargs)
	# TODO 返回总经验、等级、需要经验
	return {'exp': sql_exp, 'level': level, 'need': need, 'reward': exp}

async def __insert(name, **kwargs):
	"""没有这个登录时间和贡献记录，返回的数据不全数据"""
	await asyncio.gather(
		common.execute(f'INSERT INTO timer (uid, tid, time) SELECT familyrole.uid, {enums.Timer.LOGIN_TIME}, "{datetime.now(tz=common.TZ_SH).strftime("%Y-%m-%d")}" FROM familyrole WHERE name="{name}" ON DUPLICATE KEY UPDATE timer.tid=`tid`;', **kwargs),
		common.execute(f'INSERT INTO item (uid, iid) SELECT familyrole.uid, {enums.Item.FAMILY_COIN} FROM familyrole WHERE name="{name}" ON DUPLICATE KEY UPDATE iid=`iid`;', **kwargs),
		common.execute(f'INSERT INTO item (uid, iid) SELECT familyrole.uid, {enums.Item.FAMILY_COIN_RECORD} FROM familyrole WHERE name="{name}" ON DUPLICATE KEY UPDATE iid=`iid`;', **kwargs)
	)
