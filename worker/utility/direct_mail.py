'''
direct_mail.py

A simple client for Aliyun's direct mail client.
Allows the sending of verification emails to the specified clients.

Requires the caller to supply an aiohttp.ClientSession instance.
'''

import os
import hmac
import base64
import secrets
import datetime
import urllib.parse

ALIYUN_DIRECT_MAIL_API = 'https://dm.aliyuncs.com/'

ACCESS_KEY_ID = 'LTAI4FqKe1CFpUJUSwrVxTSN'
SECRET_KEY    = 'YQgBAPiYvycnTdQ0T7auxjMQGsXVdN'
ACCOUNT_NAME  = 'verify@mail.lukseun.com'


BASE_REQUEST = \
{
	'AccessKeyId' : ACCESS_KEY_ID,
	'AccountName' : ACCOUNT_NAME,
	'Action' : 'SingleSendMail',
	'AddressType' : 0,
	'Format' : 'json',
	'RegionId' : 'cn-hangzhou',
	'ReplyToAddress' : 'False',
	'SignatureMethod' : 'HMAC-SHA1',
	'SignatureVersion' : '1.0',
	'Subject' : '陆逊互娱账户注册验证码',
	'Version' : '2015-11-23'
}

with open(os.path.dirname(os.path.realpath(__file__)) + '/verify_email_template_zh.html', 'r', encoding='utf-8') as html:
	VERIFY_TEMPLATE = html.read()

def percent_encode(item):
	return urllib.parse.quote(str(item), safe = '')

def canonicalized_query_string(**kwargs):
	return '&'.join([percent_encode(k) + '=' + percent_encode(v) for k, v in sorted(kwargs.items())])

def sign(cqs, http_method = 'POST'):
	sts = http_method + '&%2F&' + percent_encode(cqs)
	return base64.b64encode(hmac.digest((SECRET_KEY + '&').encode(), sts.encode(), 'sha1')).decode()

def merge_kwargs(**kwargs):
	return kwargs

'''
Returns 'OK' on successful send, an error message otherwise.
'''
async def send_verification(to, nonce, session):
	html = VERIFY_TEMPLATE.replace('~NONCE~', nonce)
	snonce = str(secrets.randbits(65))
	tstamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
	cqs  = canonicalized_query_string(**BASE_REQUEST, HtmlBody = html, SignatureNonce = snonce, Timestamp = tstamp, ToAddress = to)
	signature = sign(cqs)
	async with session.post(ALIYUN_DIRECT_MAIL_API, params = merge_kwargs(**BASE_REQUEST, HtmlBody = html, SignatureNonce = snonce, Timestamp = tstamp, ToAddress = to, Signature = signature)) as r:
		if r.status != 200:
			return await r.text()
		return 'OK'

