'''
mail_server.py
'''

import os
import json
import mailbox
import datetime
import urllib.parse

from module import enums
from module import common
from aiohttp import web

import requests

DIRNAME = os.path.dirname(os.path.realpath(__file__)) + '/box'
TOKEN = 'http://192.168.1.165:8001'

class MailServer:
	def __init__(self):
		self.box = mailbox.Maildir(DIRNAME)
	
	async def send_mail(self, world, uid, **kwargs):
		try:
			mailtype = enums.MailType(int(kwargs['type']))
			message = self._construct_message(mailtype, **kwargs)
			folder = self._open_mail_folder(world, uid)
			self._deliver_message(folder, message)
		except (ValueError, KeyError): return common.mt(99, 'invalid parameters')
		return common.mt(0, 'success')

	async def delete(self, world, uid, key):
		folder = self._open_mail_folder(world, uid)
		for mid, msg in folder.iteritems():
			if mid == key:
				folder.discard(mid)
				return common.mt(0, 'deleted')
		return common.mt(-1, 'no match')

	async def delete_read(self, world, uid):
		deleted = []
		folder = self._open_mail_folder(world, uid)
		for mid, msg in folder.iteritems():
			if 'S' in msg.get_flags():
				folder.discard(mid)
				deleted.append(mid)
		return common.mt(0, 'success', {'keys' : deleted})

	async def mark_read(self, world, uid, key):
		folder = self._open_mail_folder(world, uid)
		for mid, msg in folder.iteritems():
			if mid == key:
				msg.add_flag('S')
				folder[mid] = msg
				return common.mt(0, 'marked')
		return common.mt(-1, 'no match')

	async def all_mail(self, world, uid):
		folder = self._open_mail_folder(world, uid)
		return common.mt(0, 'got all mail', {'mail' : self._read_subfolders(folder, {'new', 'cur'})})

	async def new_mail(self, world, uid):
		folder = self._open_mail_folder(world, uid)
		return common.mt(0, 'got new mail', {'mail' : self._read_subfolders(folder, {'new'})})

	############################################################

	def _attach_extra_information(self, msg, mailtype, **kwargs):
		if mailtype == enums.MailType.GIFT:
			msg['items'] = kwargs['items']
		elif mailtype == enums.MailType.FRIEND_REQUEST:
			msg['uid_sender'] = kwargs['uid_sender']
		elif mailtype == enums.MailType.FAMILY_REQUEST:
			msg['name'] = kwargs['name']
			msg['uid_target'] = kwargs['uid_target']
		return msg

	def _construct_message(self, mailtype, **kwargs):
		msg = mailbox.MaildirMessage()
		msg['time'] = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
		msg['type'] = str(mailtype.value)
		msg['from'] = urllib.parse.quote(kwargs['from'], safe = '')
		msg['subj'] = kwargs['subj']
		msg.set_payload(kwargs['body'])
		msg = self._attach_extra_information(msg, mailtype, **kwargs)
		return msg

	def _deliver_message(self, folder, message):
		key = folder.add(message)
		msg = folder[key]
		msg['key']  = key
		folder[key] = msg
	
	def _dump_message(self, msg):
		dump = {k : v for k, v in msg.items() if k not in {'uid_sender', 'name', 'uid_target'}}
		dump['body'] = msg.get_payload()
		dump['read'] = 0 if 'S' not in msg.get_flags() else 1
		return dump

	def _open_mail_folder(self, world, uid):
		try:
			folder = self.box.get_folder(str(world)).get_folder(uid)
		except mailbox.NoSuchMailboxError:
			folder = self.box.get_folder(str(world)).add_folder(uid)
		return folder

	def _read_subfolders(self, folder, subfolders):
		messages = []
		for mid, msg in folder.iteritems():
			if msg.get_subdir() in subfolders:
				msg = self._register_nonce(msg)
				msg.set_subdir('cur')
				folder[mid] = msg
				messages.append(self._dump_message(msg))
		return messages

	def _register_nonce(self, msg):
		if enums.MailType(int(msg['type'])) != enums.MailType.SIMPLE and 'F' not in msg.get_flags():
			if enums.MailType(int(msg['type'])) == enums.MailType.GIFT:
				r = requests.post(TOKEN + '/register_nonce', json = {'nonce' : msg['key'], 'type' : msg['type'], 'items' : msg['items']})
			elif enums.MailType(int(msg['type'])) == enums.MailType.FRIEND_REQUEST:
				r = requests.post(TOKEN + '/register_nonce', json = {'nonce' : msg['key'], 'type' : msg['type'], 'uid_sender' : msg['uid_sender']})
			elif enums.MailType(int(msg['type'])) == enums.MailType.FAMILY_REQUEST:
				r = requests.post(TOKEN + '/register_nonce', json = {'nonce' : msg['key'], 'type' : msg['type'], 'uid_target' : msg['uid_target'], 'name' : msg['name']})
			if r.json()['status'] == 0: msg.add_flag('F')
		return msg


def _json_response(b = '', **kwargs):
	kwargs['body'] = json.dumps(b or kwargs['kwargs']).encode('utf-8')
	kwargs['content_type'] = 'text/json'
	return web.Response(**kwargs)

ROUTES = web.RouteTableDef()

@ROUTES.post('/send')
async def __send_mail(request: web.Request) -> web.Response:
	post = await request.json() # notice we are awaiting a json type due to nested dictionary
	data = await (request.app['MANAGER']).send_mail(post['world'], post['uid'], **post['kwargs'])
	return _json_response(data)

@ROUTES.post('/new')
async def __get_new_mail(request: web.Request) -> web.Response:
	post = await request.post()
	data = await (request.app['MANAGER']).new_mail(post['world'], post['uid'])
	return _json_response(data)

@ROUTES.post('/all')
async def __get_all_mail(request: web.Request) -> web.Response:
	post = await request.post()
	data = await (request.app['MANAGER']).all_mail(post['world'], post['uid'])
	return _json_response(data)

@ROUTES.post('/mark_read')
async def __mark_read(request: web.Request) -> web.Response:
	post = await request.post()
	data = await (request.app['MANAGER']).mark_read(post['world'], post['uid'], post['key'])
	return _json_response(data)

@ROUTES.post('/delete_read')
async def __delete_read(request: web.Request) -> web.Response:
	post = await request.post()
	data = await (request.app['MANAGER']).delete_read(post['world'], post['uid'])
	return _json_response(data)

@ROUTES.post('/delete')
async def __delete(request: web.Request) -> web.Response:
	post = await request.post()
	data = await (request.app['MANAGER']).delete(post['world'], post['uid'], post['key'])
	return _json_response(data)

def run():
	app = web.Application(client_max_size = 10000000) # accept client requests up to 10 MB
	app.add_routes(ROUTES)
	app['MANAGER'] = MailServer()
	web.run_app(app, port = 8020)


if __name__ == '__main__':
	run()
