'''
mail.py

A simple on disk mail server using the standardized Maildir format.
'''

import asyncio
import mailbox
import argparse
import urllib.parse
import concurrent.futures

from aiohttp  import web
from datetime import datetime
from dateutil import tz
TZ_SH = tz.gettz('Asia/Shanghai')

class MailServer:
	def __init__(self, path):
		self.mailbox  = mailbox.Maildir(path)
		self.executor = concurrent.futures.ThreadPoolExecutor()

	async def init(self, aiohttp_app):
		aiohttp_app.router.add_post('/mark_read'  , self.mark)
		aiohttp_app.router.add_post('/send'       , self.send)
		aiohttp_app.router.add_post('/delete'     , self.delete)
		aiohttp_app.router.add_post('/all'        , self.get_all)
		aiohttp_app.router.add_post('/new'        , self.get_new)
		aiohttp_app.router.add_post('/delete_read', self.delete_read)
		return aiohttp_app

	async def send(self, request):
		post = await request.json()
		try:
			key  = await asyncio.wrap_future(self.executor.submit(MailServer.send_mail, self.mailbox, \
							post['world'], post['uid'], post['mail']))
		except KeyError:
			key = ''
		return web.json_response({'key' : key})

	async def delete(self, request):
		post = await request.post()
		deleted = await asyncio.wrap_future(self.executor.submit(MailServer.delete_mail, self.mailbox, post['world'], post['uid'], lambda mid, m: mid == post['key']))
		return web.json_response({'keys' : deleted})

	async def delete_read(self, request):
		post = await request.post()
		deleted = await asyncio.wrap_future(self.executor.submit(MailServer.delete_mail, self.mailbox, post['world'], post['uid'], lambda mid, m: 'S' in m.get_flags()))
		return web.json_response({'keys' : deleted})

	async def mark(self, request):
		post   = await request.post()
		marked = await asyncio.wrap_future(self.executor.submit(MailServer.mark_mail, self.mailbox, \
				post['world'], post['uid'], post['key'], 'S'))
		return web.json_response({'key' : post['key'] if marked else ''})

	async def get_all(self, request):
		post = await request.post()
		mail = await asyncio.wrap_future(self.executor.submit(MailServer.get_mail, self.mailbox, \
				post['world'], post['uid'], ['new', 'cur']))
		return web.json_response({'mail' : mail})

	async def get_new(self, request):
		post = await request.post()
		mail = await asyncio.wrap_future(self.executor.submit(MailServer.get_mail, self.mailbox, \
				post['world'], post['uid'], ['new']))
		return web.json_response({'mail' : mail})

	@staticmethod
	def send_mail(mbox, world, uid, mail_dict):
		return MailServer.deliver_mail(MailServer.get_mail_folder(mbox, world, uid), \
				MailServer.construct_mail(mail_dict))

	@staticmethod
	def construct_mail(mail_dict):
		mail         = mailbox.MaildirMessage()
		mail['time'] = datetime.now(tz=TZ_SH).strftime('%Y-%m-%d %H:%M:%S')
		mail.set_payload(urllib.parse.quote(mail_dict.pop('body', ''), safe = ''))
		for k, v in mail_dict.items():
			mail[k] = urllib.parse.quote(str(v), safe = '') if k in {'from', 'subj'} else str(v)
		return mail

	@staticmethod
	def dump_mail(mail):
		dump = {'read' : 0 if 'S' not in mail.get_flags() else 1, \
				'body' : urllib.parse.unquote(mail.get_payload())}
		for k, v in mail.items():
			dump[k] = urllib.parse.unquote(v) if k in {'from', 'subj'} else v
		return dump

	@staticmethod
	def deliver_mail(folder, mail):
		key = folder.add(mail)
		msg = folder[key]
		msg['key']  = key
		folder[key] = msg
		return key

	@staticmethod
	def get_mail_folder(mbox, world, uid):
		try:
			return mbox.get_folder(str(world)).get_folder(uid)
		except mailbox.NoSuchMailboxError:
			return mbox.get_folder(str(world)).add_folder(uid)

	@staticmethod
	def read_subfolders(root, subfolders):
		mail = []
		for mid, m in root.iteritems():
			if m.get_subdir() in subfolders:
				mail.append(MailServer.dump_mail(m))
				m.set_subdir('cur')
				root[mid] = m
		return mail

	@staticmethod
	def mark_mail(mbox, world, uid, key, flags):
		folder = MailServer.get_mail_folder(mbox, world, uid)
		for mid, m in folder.iteritems():
			if mid == key:
				m.add_flag(flags)
				folder[mid] = m
				return True
		return False

	@staticmethod
	def delete_mail(mbox, world, uid, condition):
		deleted = []
		folder  = MailServer.get_mail_folder(mbox, world, uid)
		for mid, m in folder.iteritems():
			if condition(mid, m):
				folder.discard(mid)
				deleted.append(mid)
		return deleted

	@staticmethod
	def get_mail(mbox, world, uid, subfolders):
		return MailServer.read_subfolders(MailServer.get_mail_folder(mbox, world, uid), subfolders)



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('path'       , type = str)
	parser.add_argument('-p','--port', type = int, default = 8020)
	args = parser.parse_args()
	web.run_app(MailServer(args.path).init(web.Application()), port = args.port)



if __name__ == '__main__':
	main()
