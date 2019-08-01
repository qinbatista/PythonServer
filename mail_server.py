#
# A simple mail server
#
######################################################################

import os
import json
import random
import mailbox
import requests


from aiohttp import web
from datetime import datetime


#TODO read port number from configuration manager

DIRNAME = os.path.dirname(os.path.realpath(__file__)) + '/box'

class MailServer:
	def __init__(self):
		self._box = mailbox.Maildir(DIRNAME)
	
	# TODO refactor code
	def send_mail(self, world: int, uid_to: str, **kwargs):
		# 0 - successfully sent mail
		# 60 - invalid request format
		# 61 - invalid message type
		if kwargs['type'] not in {'simple', 'gift'}:
			return self._message_typesetting(61, 'invalid message type')
		try:
			msg = self._construct_message(**kwargs)
			recipient_folder = self._box.get_folder(str(world)).get_folder(uid_to)
		except KeyError:
			return self._message_typesetting(60, 'invalid request format')
		except mailbox.NoSuchMailboxError:
			recipient_folder = self._box.get_folder(str(world)).add_folder(uid_to)
		recipient_folder.add(msg)
		return self._message_typesetting(0, 'success')


	def broadcast_mail(self):
		pass

	def get_new_mail(self, world: int, uid: str):
		try:
			folder = self._box.get_folder(str(world)).get_folder(uid)
		except mailbox.NoSuchMailboxError:
			return self._message_typesetting(1, 'user has no new mail')
		messages = []
		for mid, msg in folder.iteritems():
			if msg.get_subdir() == 'new':
				msg['nonce'] = self._request_nonce(msg)
				print(f'this is msg[nonce] : {msg["nonce"]}')
				messages.append(self._message_to_dict(msg))
				msg.set_subdir('cur')
				folder[mid] = msg
		if not messages:
			return self._message_typesetting(1, 'user has no new mail')
		return self._message_typesetting(0, 'got new mail', {'mail' : messages})


	def get_all_mail(self, world:int, uid: str):
		try:
			folder = self._box.get_folder(str(world)).get_folder(uid)
		except mailbox.NoSuchMailboxError:
			return self._message_typesetting(1, 'user has no mail')
		messages = []
		for mid, msg in folder.iteritems():
			if msg.get_subdir() == 'new':
				msg['nonce'] = self._request_nonce(msg)
				msg.set_subdir('cur')
				folder[mid] = msg
			messages.append(self._message_to_dict(msg))
		if not messages:
			return self._message_typesetting(1, 'user has no mail')
		return self._message_typesetting(0, 'got all mail', {'mail' : messages})

	def delete_mail(self):
		pass

	def delete_mail(self, world: int, unique_id: str, nonce: str) -> dict:
		try:
			folder = self._box.get_folder(str(world)).get_folder(unique_id)
			for mid, message in folder.iteritems():
				if message['nonce'] == nonce:
					folder.discard(mid)
		except mailbox.NoSuchMailboxError:
			pass
		return self._message_typesetting(0, 'successfully deleted message')


	def delete_all_mail(self, world:int, uid: str):
		try:
			folder = self._box.get_folder(str(world)).get_folder(uid)
		except mailbox.NoSuchMailboxError:
			return self._message_typesetting(0, 'deleted all mail')
		folder.clear()
		return self._message_typesetting(0, 'deleted all mail')

	def _request_nonce(self, msg: mailbox.MaildirMessage):
		if msg['type'] == 'gift':
			r = requests.post('http://localhost:8001/generate_nonce', json = {'type' : 'gift', 'items' : msg['items'], 'quantities' : msg['quantities']})
			return r.json()['data']['nonce']

	def _construct_message(self, **kwargs):
		msg = mailbox.MaildirMessage()
		msg['time']    = datetime.now().strftime('%Y/%m/%d, %H:%M:%S')
		msg['from']    = kwargs['from']
		msg['type']    = kwargs['type']
		msg['subject'] = kwargs['subject']
		msg.set_payload(kwargs['body'])
		if msg['type'] == 'gift':
			msg['items'] = kwargs['items']
			msg['quantities'] = kwargs['quantities']
		return msg

	def _message_to_dict(self, msg: mailbox.MaildirMessage, **kwargs) -> dict:
		d = {}
		d['subject'] = msg['subject']
		d['time'] = msg['time']
		d['from'] = msg['from']
		d['body'] = msg.get_payload()
		d['type'] = msg['type']
		d['data'] = {}
		d['data']['nonce'] = msg['nonce']
		return d


	def _message_typesetting(self, status: int, message: str, data: dict = {}) -> dict:
		return {'status' : status, 'message' : message, 'random' : random.randint(-1000, 1000), 'data' : data}


def _json_response(body: dict = '', **kwargs) -> web.Response:
	kwargs['body'] = json.dumps(body or kwargs['kwargs']).encode('utf-8')
	kwargs['content_type'] = 'text/json'
	return web.Response(**kwargs)

ROUTES = web.RouteTableDef()
@ROUTES.post('/send_mail')
async def __send_mail(request: web.Request) -> web.Response:
	post = await request.json() # notice we are awaiting a json type due to nested dictionary
	data = (request.app['MANAGER']).send_mail(post['world'], post['uid_to'], **post['kwargs'])
	return _json_response(data)

@ROUTES.post('/get_new_mail')
async def __get_new_mail(request: web.Request) -> web.Response:
	post = await request.post()
	data = (request.app['MANAGER']).get_new_mail(post['world'], post['unique_id'])
	return _json_response(data)

@ROUTES.post('/get_all_mail')
async def __get_all_mail(request: web.Request) -> web.Response:
	post = await request.post()
	data = (request.app['MANAGER']).get_all_mail(post['world'], post['unique_id'])
	return _json_response(data)

@ROUTES.post('/delete_all_mail')
async def __delete_all_mail(request: web.Request) -> web.Response:
	post = await request.post()
	data = (request.app['MANAGER']).delete_all_mail(post['world'], post['unique_id'])
	return _json_response(data)

@ROUTES.post('/delete_mail_gift')
async def __delete_mail_gift(request: web.Request) -> web.Response:
	post = await request.post()
	data = (request.app['MANAGER']).delete_mail_gift(post['world'], post['unique_id'], post['nonce'])
	return _json_response(data)

def run():
	app = web.Application()
	app.add_routes(ROUTES)
	app['MANAGER'] = MailServer()
	web.run_app(app, port = 8020)




if __name__ == '__main__':
	run()
