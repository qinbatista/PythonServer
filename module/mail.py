'''
mail.py
'''

from module import common


async def _send_mail_simple(uid_to, **kwargs):
	mail = {'world' : kwargs['world'], 'uid_to' : uid_to, 'kwargs' : {'from' : kwargs.get('from_', 'server'), 'body' : kwargs.get('body', 'This is a test message'), 'subject' : kwargs.get('subject', 'Test Message'), 'type' : (common.MailType.SIMPLE.name).lower()}}
	return await _send_mail(mail, **kwargs)

async def _send_mail_gift(uid_to, **kwargs):
	return True

async def _send_mail_friend_request(uid_to, **kwargs):
	return True

async def _send_mail_family_invite(uid_to, **kwargs):
	return True

SWITCH = \
{
	common.MailType.SIMPLE : _send_mail_simple,
	common.MailType.GIFT : _send_mail_gift,
	common.MailType.FRIEND_REQUEST : _send_mail_friend_request,
	common.MailType.FAMILY_INVITE : _send_mail_family_invite
}

'''
Possible valid kwargs:
	from_, body, subject, items, quantities
'''
async def send_mail(mailtype, uid_to, **kwargs):
	try:
		return await (SWITCH[mailtype])(uid_to, **kwargs)
	except KeyError: return False


async def _send_mail(mail, **kwargs):
	async with kwargs['session'].post(kwargs['mailserverbaseurl'] + '/send_mail', json = mail) as resp:
		result = await resp.json(content_type = 'text/json')
		return result['status'] == 0

