'''
chat.py
'''

import secrets
from module import enums
from module import common

async def get_login_token(uid, **kwargs):
	data = await common.execute(f'SELECT `gn`, `fid` FROM `player` WHERE `uid` = "{uid}";', **kwargs)
	gn, fn = data[0][0], data[0][1]
	token = str(secrets.randbits(128))
	await kwargs['redis'].hmset_dict(f'chat.logintokens.{token}', \
			{'world' : kwargs['world'], 'gn' : gn, 'fn' : fn})
	await kwargs['redis'].expire(f'chat.logintokens.{token}', 120)
	return common.mt(0, 'success', {'token' : token})
