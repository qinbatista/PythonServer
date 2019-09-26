'''
friend.py
'''

import datetime

from module import mail
from module import enums
from module import common
from module import family


async def get_all(uid, **kwargs):
	return common.mt(0, 'got all friends')

async def remove(uid, gn_target, **kwargs):
	uid_target = await family._get_uid(gn_target, **kwargs)
	if uid == uid_target: return common.mt(99, 'do not be an idiot')
	await common.execute(f'DELETE FROM friend WHERE (uid = "{uid}" AND fid = "{uid_target}") OR (uid = "{uid_target}" AND fid = "{uid}");', **kwargs)
	return common.mt(0, 'removed target')

async def request(uid, gn_target, **kwargs):
	uid_target = await family._get_uid(gn_target, **kwargs)
	if uid == uid_target: return common.mt(99, 'do not be an idiot')
	await common.execute(f'INSERT INTO friend (uid, fid) VALUES ("{uid}", "{uid_target}") ON DUPLICATE KEY UPDATE uid = uid;', **kwargs)
	sender = await family._get_gn(uid, **kwargs)
	if not await mail.send_mail(enums.MailType.FRIEND_REQUEST, uid_target, from_ = sender, sender = sender, uid_sender = uid, **kwargs):
		return common.mt(98, 'could not send mail')
	return common.mt(0, 'request sent', {'uid_target' : uid_target})

async def respond(uid, nonce, **kwargs):
	return common.mt(0, 'success')


##########################################################################################################

async def _get_friend_info(uid, **kwargs):
	info = await common.execute(f'SELECT player.gn, progress.exp FROM friend JOIN progress ON progress.uid = friend.fid JOIN player ON player.uid = friend.fid WHERE friend.uid = "{uid}";', **kwargs)
