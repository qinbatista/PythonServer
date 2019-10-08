'''
friend.py

CHECKED RETURN TYPES WITH LIANG
'''

import asyncio

from module import mail
from module import enums
from module import common
from datetime import datetime, timezone


async def get_all(uid, **kwargs):
	info = await _get_friend_info(uid, **kwargs)
	return common.mt(0, 'got all friends', {'friends' : [{'gn' : i[0], 'exp' : i[1], 'recover' : i[2], 'since' : i[3], 'icon' : 0} for i in info]})

async def remove(uid, gn_target, **kwargs):
	uid_target = await common.get_uid(gn_target, **kwargs)
	if uid == uid_target: return common.mt(99, 'don\'t be an idiot')
	await common.execute(f'DELETE FROM friend WHERE (uid = "{uid}" AND fid = "{uid_target}") OR (uid = "{uid_target}" AND fid = "{uid}");', **kwargs)
	return common.mt(0, 'removed target', {'gn' : gn_target})

async def request(uid, gn_target, **kwargs):
	uid_target = await common.get_uid(gn_target, **kwargs)
	if uid == uid_target: return common.mt(99, 'do not be an idiot')
	await common.execute(f'INSERT INTO friend (uid, fid) VALUES ("{uid}", "{uid_target}") ON DUPLICATE KEY UPDATE uid = uid;', **kwargs)
	sender = await common.get_gn(uid, **kwargs)
	if not await mail.send_mail(enums.MailType.FRIEND_REQUEST, uid_target, from_ = sender, sender = sender, uid_sender = uid, **kwargs):
		return common.mt(98, 'could not send mail')
	return common.mt(0, 'request sent', {'gn' : gn_target})

async def respond(uid, nonce, **kwargs):
	uid_sender = await _lookup_nonce(nonce, **kwargs)
	if not uid_sender: return common.mt(99, 'invalid nonce')
	await _add_friend(uid, uid_sender, **kwargs)
	info = await _get_friend_info(uid_sender, **kwargs)
	await mail.delete_mail(uid, nonce, **kwargs)
	# {'gn' : new friend, 'exp' : new friend, 'icon' : 0 new friend, 'recover' : NF, 'since' : since new friend}
	return common.mt(0, 'success', {'gn' : info[0], 'exp' : info[1]})

async def send_gift(uid, gn_target, **kwargs):
	fid = await common.get_uid(gn_target, **kwargs)
	friends, recover, since = await _are_friends(uid, fid, **kwargs)
	if not friends or since == '': return common.mt(99, 'not friends')
	now = datetime.now(timezone.utc)
	if not _can_send_gift(now, recover): return common.mt(98, 'gift cooldown')
	kwargs['data']['items'] = common.encode_item(enums.Group.ITEM, enums.Item.FRIEND_GIFT, 1)
	sent = await mail.send_mail(enums.MailType.GIFT, fid, **kwargs)
	if not sent: return common.mt(97, 'mailbox error')
	await common.execute(f'UPDATE friend SET recover = "{now.strftime("%Y-%m-%d")}" WHERE uid = "{uid}" AND fid = "{fid}";', **kwargs)
	# {'gn' : gn, 'recover' : rt}
	return common.mt(0, 'success')

async def send_gift_all(uid, **kwargs):
	pass



##########################################################################################################

def _can_send_gift(now, recover):
	if recover == '': return True
	delta_time = now - datetime.strptime(recover, '%Y-%m-%d').replace(tzinfo = timezone.utc)
	return delta_time.days >= 1

async def _add_friend(uid, fid, **kwargs):
	now = datetime.now(timezone.utc).strftime('%Y-%m-%d')
	await asyncio.gather(common.execute(f'INSERT INTO friend(uid, fid, since) VALUES ("{uid}", "{fid}", "{now}") ON DUPLICATE KEY UPDATE since = "{now}";', **kwargs), common.execute(f'INSERT INTO friend(uid, fid, since) VALUES ("{fid}", "{uid}", "{now}") ON DUPLICATE KEY UPDATE since = "{now}";', **kwargs))

async def _are_friends(uid, fid, **kwargs):
	data = await common.execute(f'SELECT recover, since FROM friend WHERE uid = "{uid}" AND fid = "{fid}";', **kwargs)
	return (True, data[0][0], data[0][1]) if data != () else (False, None, None)

async def _get_friend_info(uid, **kwargs):
	info = await common.execute(f'SELECT player.gn, progress.exp, friend.recover, friend.since FROM friend JOIN progress ON progress.uid = friend.fid JOIN player ON player.uid = friend.fid WHERE friend.uid = "{uid}";', **kwargs)
	return info

async def _lookup_nonce(nonce, **kwargs):
	async with kwargs['session'].post(kwargs['tokenserverbaseurl'] + '/redeem_nonce_new', json = {'nonce' : [nonce]}) as resp:
		data = await resp.json(content_type = 'text/json')
		return None if data[nonce]['status'] != 0 else data[nonce]['uid_sender']




