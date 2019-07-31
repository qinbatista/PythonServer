#
# A simple mail server
#
######################################################################

import os
import json
import random
import mailbox

from aiohttp import web


#TODO read port number from configuration manager

DIRNAME = os.path.dirname(os.path.realpath(__file__)) + '/box'

class MailServer:
	def __init__(self):
		self._box = mailbox.Maildir(DIRNAME)
	
	def send_mail(self, world: int, uid_to: str, **kwargs):
		msg = self._construct_message(**kwargs)
		try:
			recipient_folder = self._box.get_folder(str(world)).get_folder(uid_to)
		except mailbox.NoSuchMailboxError:
			recipient_folder = self._box.get_folder(str(world)).add_folder(uid_to)
		finally:
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
			messages.append(self._message_to_dict(msg))
			if msg.get_subdir() == 'new':
				msg.set_subdir('cur')
				folder[mid] = msg
		if not messages:
			return self._message_typesetting(1, 'user has no mail')
		return self._message_typesetting(0, 'got all mail', {'mail' : messages})

	def delete_mail(self):
		pass

	def delete_all_mail(self, world:int, uid: str):
		try:
			folder = self._box.get_folder(str(world)).get_folder(uid)
		except mailbox.NoSuchMailboxError:
			return self._message_typesetting(0, 'deleted all mail')
		folder.clear()
		return self._message_typesetting(0, 'deleted all mail')

	#TODO add the time to the message
	def _construct_message(self, **kwargs):
		msg = mailbox.MaildirMessage()
		msg['from']    = kwargs['from']
		msg['type']    = kwargs['type']
		msg['subject'] = kwargs['subject']
		msg.set_payload(kwargs['body'])
		return msg

	def _message_to_dict(self, msg: mailbox.MaildirMessage, **kwargs) -> dict:
		d = {}
		d['subject'] = msg['subject']
		d['time'] = msg['time']
		d['from'] = msg['from']
		d['body'] = msg.get_payload()
		d['type'] = msg['type']
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
	post = await request.post()
	print(f'this is post: {post}')
	print(f'this is len: {len(post)}')
	print(post.keys())
	data = (request.app['MANAGER']).send_mail(post['world'], post['uid_to'], **post['kwargs'])
	return _json_response(data)

@ROUTES.post('/get_new_mail')
async def __get_new_mail(request: web.Request) -> web.Response:
	post = await request.post()
	data = (request.app['MANAGER']).get_new_mail(post['world'], post['unique_id'])
	return _json_response(data)

def run():
	app = web.Application()
	app.add_routes(ROUTES)
	app['MANAGER'] = MailServer()
	web.run_app(app, port = 8020)




if __name__ == '__main__':
	run()
