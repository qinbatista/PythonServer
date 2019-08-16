#
# A simple mail server
#
######################################################################

import os
import json
import time
import random
import mailbox
import requests
import configparser


from aiohttp import web
from datetime import datetime

DIRNAME = os.path.dirname(os.path.realpath(__file__)) + '/box'

class MailServer:
	def __init__(self):
		self._box = mailbox.Maildir(DIRNAME)
	
	# TODO refactor code
	def send_mail(self, world: int, uid_to: str, **kwargs):
		# 0 - successfully sent mail
		# 60 - invalid request format
		# 61 - invalid message type
		if kwargs['type'] not in {'simple', 'gift', 'friend_request', 'family_request'}:
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



	def get_new_mail(self, world: int, uid: str):
		# 0 - successfully got new mail
		# 62 - mailbox empty
		try:
			folder = self._box.get_folder(str(world)).get_folder(uid)
		except mailbox.NoSuchMailboxError:
			return self._message_typesetting(62, 'mailbox empty')
		messages = []
		for mid, msg in folder.iteritems():
			if msg.get_subdir() == 'new':
				msg['nonce'] = self._request_nonce(msg)
				messages.append(self._message_to_dict(msg))
				msg.set_subdir('cur')
				folder[mid] = msg
		if not messages:
			return self._message_typesetting(62, 'mailbox empty')
		return self._message_typesetting(0, 'got new mail', {'mail' : messages})


	def get_all_mail(self, world:int, uid: str):
		# 0 - successfully got all mail
		# 62 - mailbox empty
		try:
			folder = self._box.get_folder(str(world)).get_folder(uid)
		except mailbox.NoSuchMailboxError:
			return self._message_typesetting(62, 'mailbox empty')
		messages = []
		for mid, msg in folder.iteritems():
			if msg.get_subdir() == 'new':
				msg['nonce'] = self._request_nonce(msg)
				msg.set_subdir('cur')
				folder[mid] = msg
			messages.append(self._message_to_dict(msg))
		if not messages:
			return self._message_typesetting(62, 'mailbox empty')
		return self._message_typesetting(0, 'got all mail', {'mail' : messages})

	def delete_mail(self, world: int, unique_id: str, nonce: str) -> dict:
		# 0 - successfully deleted mail
		try:
			folder = self._box.get_folder(str(world)).get_folder(unique_id)
			for mid, message in folder.iteritems():
				if message['nonce'] == nonce:
					folder.discard(mid)
		except mailbox.NoSuchMailboxError:
			pass
		return self._message_typesetting(status=0, message='successfully deleted message', data={"nonce": nonce})


	def delete_all_mail(self, world: int, uid: str):
		# 0 - successfully deleted all mail
		try:
			folder = self._box.get_folder(str(world)).get_folder(uid)
		except mailbox.NoSuchMailboxError:
			return self._message_typesetting(0, 'deleted all mail')
		for mid, msg in folder.iteritems():
			if msg.get_subdir() == 'cur':
				folder.discard(mid)
		return self._message_typesetting(0, 'deleted all mail')

	# TODO map for loop to run concurrently
	def broadcast_mail(self, world: int, users: [str], **kwargs) -> dict:
		# 0 - successfully sent mail
		# 60 - invalid request format
		# 61 - invalid message type
		if kwargs['type'] not in {'simple', 'gift', 'friend_request'}:
			return self._message_typesetting(61, 'invalid message type')
		try:
			msg = self._construct_message(**kwargs)
		except KeyError:
			return self._message_typesetting(60, 'invalid request format')
		for user in users:
			try:
				folder = self._box.get_folder(str(world)).get_folder(user)
			except mailbox.NoSuchMailboxError:
				folder = self._box.get_folder(str(world)).add_folder(user)
			folder.add(msg)
		return self._message_typesetting(0, 'success')

	def _request_nonce(self, msg: mailbox.MaildirMessage):
		if msg['type'] == 'gift':
			r = requests.post('http://localhost:8001/generate_nonce', json = {'type' : 'gift', 'items' : msg['items'], 'quantities' : msg['quantities']})
			return r.json()['data']['nonce']
		elif msg['type'] == 'friend_request':
			r = requests.post('http://localhost:8001/generate_nonce', json = {'type' : 'friend_request', 'uid_sender' : msg['uid_sender'], 'sender' : msg['sender']})
			return r.json()['data']['nonce']
		elif msg['type'] == 'family_request':
			r = requests.post('http://localhost:8001/generate_nonce', json = {'type' : 'family_request', 'fid' : msg['fid'], 'target' : msg['target']})
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
		elif msg['type'] == 'friend_request':
			msg['sender'] = kwargs['sender']
			msg['uid_sender'] = kwargs['uid_sender']
		elif msg['type'] == 'family_request':
			msg['fid'] = kwargs['fid']
			msg['fname'] = kwargs['fname']
			msg['target'] = kwargs['target']
		return msg

	def _message_to_dict(self, msg: mailbox.MaildirMessage, **kwargs) -> dict:
		d = {}
		d['subject'] = msg['subject']
		d['time'] = msg['time']
		d['from'] = msg['from']
		d['body'] = msg.get_payload()
		d['type'] = msg['type']
		d['data'] = {}
		if msg['type'] == 'gift':
			d['data']['nonce'] = msg['nonce']
		elif msg['type'] == 'friend_request':
			d['data']['nonce'] = msg['nonce']
			d['data']['sender'] = msg['sender']
		elif msg['type'] == 'family_request':
			d['data']['nonce'] = msg['nonce']
			d['data']['fname'] = msg['fname']
			d['data']['target'] = msg['target']

		return d


	def _message_typesetting(self, status: int, message: str, data: dict = {}) -> dict:
		return {'status' : status, 'message' : message, 'random' : random.randint(-1000, 1000), 'data' : data}

def get_config():
	while True:
		try:
			r = requests.get('http://localhost:8000/get_server_config_location')
			parser = configparser.ConfigParser()
			parser.read(r.json()['file'])
			return parser
		except requests.exceptions.ConnectionError:
			print('Could not find configuration server, retrying in 5 seconds...')
			time.sleep(5)

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

@ROUTES.post('/delete_mail')
async def __delete_mail(request: web.Request) -> web.Response:
	post = await request.post()
	data = (request.app['MANAGER']).delete_mail(post['world'], post['unique_id'], post['nonce'])
	return _json_response(data)

@ROUTES.post('/broadcast_mail')
async def __broadcast_mail(request: web.Request) -> web.Response:
	post = await request.json() # notice we are awaiting a json type due to nested dictionary
	data = (request.app['MANAGER']).broadcast_mail(post['world'], post['users'], **post['mail'])
	return _json_response(data)

def run():
	app = web.Application(client_max_size = 10000000) # accept client requests up to 10 MB
	app.add_routes(ROUTES)
	app['MANAGER'] = MailServer()
	config = get_config()
	web.run_app(app, port = config.getint('mail_server', 'port'))




if __name__ == '__main__':
	run()
