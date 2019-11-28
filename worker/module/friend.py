'''
friend.py

CHECKED RETURN TYPES WITH LIANG
'''

import asyncio

from module import mail
from module import enums
from module import common
from module import task
from module import achievement
from module import family
from datetime import datetime, timezone


async def get_all(uid, **kwargs):
	info = await _get_friend_info(uid, **kwargs)
	return common.mt(0, 'got all friends', {'friends': [{'gn': i[0], 'exp': i[1], 'recover': i[2], 'since': i[3], 'fid': i[4], 'intro': i[5], 'icon': 0} for i in info]})


async def remove(uid, gn_target, **kwargs):
	uid_target = await common.get_uid(gn_target, **kwargs)
	if uid == uid_target: return common.mt(99, 'don\'t be an idiot')
	await common.execute(f'DELETE FROM friend WHERE (uid = "{uid}" AND fid = "{uid_target}") OR (uid = "{uid_target}" AND fid = "{uid}");', **kwargs)
	return common.mt(0, 'removed target', {'gn': gn_target})


async def request(uid, gn_target, **kwargs):
	if await _is_request_max(uid, **kwargs):
		return common.mt(96, '6 request for 1 day, try tommorrow')

	kwargs.update({"aid":enums.Achievement.FRIEND_REQUEST})
	await achievement.record_achievement(kwargs['data']['unique_id'],**kwargs)

	uid_target = await common.get_uid(gn_target, **kwargs)
	if uid_target == "": return common.mt(97, 'no such person')
	if uid == uid_target: return common.mt(99, 'do not be an idiot')
	friends, _, _ = await _are_friends(uid, uid_target, **kwargs)
	if friends: return common.mt(95, 'already friends')
	await common.execute(f'INSERT INTO friend (uid, fid) VALUES ("{uid}", "{uid_target}") ON DUPLICATE KEY UPDATE uid = uid;', **kwargs)
	sender = await common.get_gn(uid, **kwargs)
	if not await mail.send_mail(enums.MailType.FRIEND_REQUEST, uid_target, from_=sender, \
			uid_sender=uid, **kwargs):
		return common.mt(98, 'could not send mail')
	await common.execute(f'INSERT INTO limits(uid, lid, value) VALUES ("{uid}", {enums.Limits.REQUEST_FRIEND_LIMITS}, value+1) ON DUPLICATE KEY UPDATE value = value+1;', **kwargs)
	return common.mt(0, 'request sent', {'gn': gn_target})


async def respond(uid, nonce, **kwargs):
	uid_sender = await _lookup_nonce(nonce, **kwargs)
	if not uid_sender: return common.mt(99, 'invalid nonce')
	await _add_friend(uid, uid_sender, **kwargs)
	info = await _get_friend_info(uid_sender, **kwargs)
	await mail.delete_mail(uid, nonce, **kwargs)
	if info == ():
		return common.mt(98, 'this person has date exception')
	return common.mt(0, 'success', {'gn': info[0][0], 'exp': info[0][1]})


async def send_gift(uid, gn_target, **kwargs):
	# 发送朋友礼物
	kwargs.update({"task_id": enums.Task.SEND_FRIEND_GIFT})
	await task.record_task(uid,**kwargs)
	fid = await common.get_uid(gn_target, **kwargs)
	friends, recover, since = await _are_friends(uid, fid, **kwargs)
	if not friends or since == '': return common.mt(99, 'not friends')
	now = datetime.now(timezone.utc)
	if not _can_send_gift(now, recover): return common.mt(98, 'gift cooldown')
	kwargs['items'] = common.encode_item(enums.Group.ITEM, enums.Item.FRIEND_GIFT, 1)
	kwargs['from_'] = await common.get_gn(uid, **kwargs)
	sent = await mail.send_mail(enums.MailType.GIFT, fid, \
			subj = enums.MailTemplate.FRIEND_GIFT.name, body = '', **kwargs)
	if not sent: return common.mt(97, 'mailbox error')
	kwargs.update({"aid":enums.Achievement.FRIEND_GIFT})
	await achievement.record_achievement(kwargs['data']['unique_id'],**kwargs)
	await common.execute(f'UPDATE friend SET recover = "{now.strftime("%Y-%m-%d")}" WHERE uid = "{uid}" AND fid = "{fid}";', **kwargs)
	return common.mt(0, 'success')


async def send_gift_all(uid, **kwargs):
	info = await common.execute(f'SELECT player.gn FROM friend JOIN player ON player.uid = friend.fid WHERE friend.uid = "{uid}";', **kwargs)
	if info == (): return common.mt(99, 'no friend to send gift')
	message_dic = []
	for index, i in enumerate(info):
		result = await send_gift(uid, i[0], **kwargs)
		if result["status"] == 0: message_dic.append(i[0])
	return common.mt(0, 'you send all friend gift success', message_dic)


async def find_person(uid, gn_target, **kwargs):
	data = await _get_person_info(await common.get_uid(gn_target, **kwargs), **kwargs)
	uid_target = await common.get_uid(gn_target, **kwargs)
	if uid == uid_target: return common.mt(98, "can't add yourself")
	if data == (): return common.mt(99, 'no such person')
	isfriends, _, _ = await _are_friends(uid, uid_target, **kwargs)
	isfamily = await _are_family(uid, uid_target, **kwargs)
	return common.mt(0, 'find person success', {'gn': data[0][0], 'intro': data[0][1], 'fid': data[0][2], 'exp': data[0][3], 'stage': data[0][4], 'role': data[0][5], "isfriend": str(isfriends), "isfamily": str(isfamily)})


###########################################################################################################

def _can_send_gift(now, recover):
	if recover == '': return True
	delta_time = now - datetime.strptime(recover, '%Y-%m-%d').replace(tzinfo=timezone.utc)
	return delta_time.days >= 1


async def _is_request_max(uid, **kwargs):
	now = datetime.now(timezone.utc).strftime('%Y-%m-%d')
	data = await common.execute(
		f"SELECT limits.value, timer.time FROM limits JOIN timer ON limits.uid = timer.uid WHERE limits.uid='{uid}' and limits.lid={enums.Limits.REQUEST_FRIEND_LIMITS} and timer.tid={enums.Timer.REQUEST_FRIEND_TIME}",
		**kwargs)
	if data == ():
		await common.execute(
			f'INSERT INTO limits(uid, lid, value) VALUES ("{uid}", {enums.Limits.REQUEST_FRIEND_LIMITS}, 0) ON DUPLICATE KEY UPDATE value = 0;',
			**kwargs)
		await common.execute(
			f'INSERT INTO timer(uid, tid, time) VALUES ("{uid}", {enums.Timer.REQUEST_FRIEND_TIME}, "{now}") ON DUPLICATE KEY UPDATE time = "{now}";',
			**kwargs)
		count, record_time = 0, now
	else:
		count, record_time = data[0][0], data[0][1]
	delta_time = datetime.now(timezone.utc) - datetime.strptime(record_time, '%Y-%m-%d').replace(tzinfo=timezone.utc)
	if delta_time.days >= 1:
		await common.execute(
			f'INSERT INTO timer(uid, tid, time) VALUES ("{uid}", {enums.Timer.REQUEST_FRIEND_TIME}, "{now}") ON DUPLICATE KEY UPDATE time = "{now}";',
			**kwargs)
		await common.execute(
			f'INSERT INTO limits(uid, lid, value) VALUES ("{uid}", {enums.Limits.REQUEST_FRIEND_LIMITS}, 0) ON DUPLICATE KEY UPDATE value = 0;',
			**kwargs)
	if delta_time.days < 1 and count <= 5:
		return False
	if delta_time.days < 1 and count > 5:
		return True


async def _add_friend(uid, fid, **kwargs):
	now = datetime.now(timezone.utc).strftime('%Y-%m-%d')
	await asyncio.gather(common.execute(
		f'INSERT INTO friend(uid, fid, since) VALUES ("{uid}", "{fid}", "{now}") ON DUPLICATE KEY UPDATE since = "{now}";',
		**kwargs), common.execute(
		f'INSERT INTO friend(uid, fid, since) VALUES ("{fid}", "{uid}", "{now}") ON DUPLICATE KEY UPDATE since = "{now}";',
		**kwargs))


async def _are_friends(uid, fid, **kwargs):
	data = await common.execute(f'SELECT recover, since FROM friend WHERE uid = "{uid}" AND fid = "{fid}";', **kwargs)
	return (True, data[0][0], data[0][1]) if data != () else (False, None, None)


async def _are_family(uid, fid, **kwargs):
	data1 = await common.execute(f'SELECT fid FROM player WHERE uid = "{uid}"', **kwargs)
	data2 = await common.execute(f'SELECT fid FROM player WHERE uid = "{fid}"', **kwargs)
	if data1[0][0] == '' and data2[0][0] == '':
		return False
	else:
		if data1[0][0] == data2[0][0] and family._check_invite_permissions(await family._get_role(uid, data1[0][0], **kwargs))==True:
			return True
		else:
			return False
# return True if (False if data1[0][0] == '' or data2[0][0] != '' else True) and family._check_invite_permissions(await family._get_role(uid, data1[0][0], **kwargs)) else False


async def _get_friend_info(uid, **kwargs):
	info = await common.execute(
		f'SELECT player.gn, progress.exp, friend.recover, friend.since, player.fid, player.intro FROM friend JOIN progress ON progress.uid = friend.fid JOIN player ON player.uid = friend.fid WHERE friend.uid = "{uid}";',
		**kwargs)
	if info == ():
		return ()
	else:
		return info


async def _get_person_info(uid, **kwargs):
	info = await common.execute(
		f'SELECT player.gn, player.intro, player.fid, progress.exp, progress.stage, progress.role FROM progress JOIN player ON progress.uid = player.uid WHERE player.uid = "{uid}";',
		**kwargs)
	if info == ():
		return ()
	else:
		return info


async def _lookup_nonce(nonce, **kwargs):
	async with kwargs['session'].post(kwargs['tokenserverbaseurl'] + '/redeem_nonce',
									  json={'keys': [nonce]}) as resp:
		data = await resp.json()
		return None if data[nonce]['status'] != 0 else data[nonce]['uid_sender']
