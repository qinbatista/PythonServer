'''
mail.py

A simple on disk mail server using the standardized Maildir format.
'''

import asyncio
import mailbox
import argparse
import contextlib
import urllib.parse
import concurrent.futures

from aiohttp  import web
from datetime import datetime
from dateutil import tz

class MailServer:
	MAILBOX_LIMIT = 50

	class MailboxFullError(Exception):
		pass

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
			key = await asyncio.wrap_future(self.executor.submit(MailServer.send_mail, self.mailbox, \
							post['world'], post['uid'], post['mail']))
		except KeyError:
			return web.json_response({'status' : -1, 'uid' : post['uid'], 'key' : ''})
		except MailServer.MailboxFullError:
			return web.json_response({'status' :  1, 'uid' : post['uid'], 'key' : ''})
		return web.json_response({    'status' :  0, 'uid' : post['uid'], 'key' : key})

	async def delete(self, request):
		"""删除指定邮件"""
		post = await request.post()
		deleted = await asyncio.wrap_future(self.executor.submit(MailServer.delete_mail, self.mailbox, \
				post['world'], post['uid'], lambda mid, m: mid == post['key']))
		return web.json_response({'keys' : deleted})

	async def delete_read(self, request):
		"""删除已读的所有邮件"""
		post = await request.post()
		deleted = await asyncio.wrap_future(self.executor.submit(MailServer.delete_mail, self.mailbox, \
				post['world'], post['uid'], lambda mid, m: 'S' in m.get_flags()))
		return web.json_response({'keys' : deleted})

	async def mark(self, request):
		"""设置邮件为已读，标记邮件标识"""
		post   = await request.post()
		marked = await asyncio.wrap_future(self.executor.submit(MailServer.mark_mail, self.mailbox, \
				post['world'], post['uid'], post['key'], 'S'))
		return web.json_response({'key' : post['key'] if marked else ''})

	async def get_all(self, request):
		"""返回所有的邮件，包括新邮件和已读邮件
		cur：当前所有邮件的数量
		max：邮箱最大限制的数量"""
		post = await request.post()
		mail = await asyncio.wrap_future(self.executor.submit(MailServer.get_mail, self.mailbox, \
				post['world'], post['uid'], ['new', 'cur']))
		return web.json_response({'mail' : mail, 'count' : \
				{'cur' : len(MailServer.get_mail_folder(self.mailbox, post['world'], post['uid'])), \
				'max' : MailServer.MAILBOX_LIMIT}})

	async def get_new(self, request):
		"""返回所有的新邮件
		cur：当前所有邮件的数量
		max：邮箱最大限制的数量"""
		post = await request.post()
		mail = await asyncio.wrap_future(self.executor.submit(MailServer.get_mail, self.mailbox, \
				post['world'], post['uid'], ['new']))
		return web.json_response({'mail' : mail, 'count' : \
				{'cur' : len(MailServer.get_mail_folder(self.mailbox, post['world'], post['uid'])), \
				'max' : MailServer.MAILBOX_LIMIT}})

	@staticmethod
	def send_mail(mbox, world, uid, mail_dict):
		"""发送邮件
		mbox：mailbox.Maildir对象
		world：接收者所在世界
		uid：接收者的uid
		mail_dict: 邮件信息（字典）"""
		return MailServer.deliver_mail(MailServer.get_mail_folder(mbox, world, uid), \
				MailServer.construct_mail(mail_dict))

	@staticmethod
	def construct_mail(mail_dict):
		"""构造邮件
		time：构造时间
		from：发送者的uid
		subj：邮件主题
		其他信息以键值对存放进邮件
		set_payload设置邮件内容
		"""
		mail         = mailbox.MaildirMessage()
		mail['time'] = datetime.now(tz = tz.gettz('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
		mail.set_payload(urllib.parse.quote(mail_dict.pop('body', ''), safe = ''))
		for k, v in mail_dict.items():
			mail[k] = urllib.parse.quote(str(v), safe = '') if k in {'from', 'subj'} else str(v)
		return mail

	@staticmethod
	def dump_mail(mail):
		"""解析每一封邮件，dump包含字段解析
		read：0未读，1已读
		body：get_payload读取邮件内容
		from：发送者的uid
		subj：邮件主题
		其他信息以键值对返回
		"""
		dump = {'read' : 0 if 'S' not in mail.get_flags() else 1, \
				'body' : urllib.parse.unquote(mail.get_payload())}
		for k, v in mail.items():
			dump[k] = urllib.parse.unquote(v) if k in {'from', 'subj'} else v
		return dump

	@staticmethod
	def deliver_mail(folder, mail):
		"""存放邮件到指定的文件夹下"""
		mail_count = 0
		with contextlib.suppress(FileNotFoundError):
			# this can fail in the case where the folder was recently created
			mail_count = len(folder) 
		if mail_count >= MailServer.MAILBOX_LIMIT:
			raise MailServer.MailboxFullError
		# 获取key并将key添加到邮件中
		key = folder.add(mail)
		msg = folder[key]
		msg['key']  = key
		folder[key] = msg
		return key

	@staticmethod
	def get_mail_folder(mbox, world, uid):
		"""创建或指定邮件存放需要的路径，返回邮箱地址对象"""
		return mbox.add_folder(str(world)).add_folder(uid)

	@staticmethod
	def read_subfolders(root, subfolders):
		"""读取邮件信息，读取之后将邮件从new文件夹移到cur文件夹"""
		mail = []
		for mid, m in root.iteritems():
			if m.get_subdir() in subfolders:
				mail.append(MailServer.dump_mail(m))
				m.set_subdir('cur')
				root[mid] = m
		return mail

	@staticmethod
	def mark_mail(mbox, world, uid, key, flags):
		"""添加标志"""
		folder = MailServer.get_mail_folder(mbox, world, uid)
		for mid, m in folder.iteritems():
			if mid == key:
				m.add_flag(flags)
				folder[mid] = m
				return True
		return False

	@staticmethod
	def delete_mail(mbox, world, uid, condition):
		"""删除满足条件的邮件
		condition：匿名方法"""
		deleted = []
		folder  = MailServer.get_mail_folder(mbox, world, uid)
		for mid, m in folder.iteritems():
			if condition(mid, m):
				folder.discard(mid)
				deleted.append(mid)
		return deleted

	@staticmethod
	def get_mail(mbox, world, uid, subfolders):
		""" 获取邮件
		mbox: mailbox.Maildir对象
		world: 获取的邮件所在世界
		uid: 获取的邮件所在用户uid
		subfolders: 子文件夹列表
		return: 返回邮件信息列表
		"""
		return MailServer.read_subfolders(MailServer.get_mail_folder(mbox, world, uid), subfolders)



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('path'       , type = str)
	parser.add_argument('-p','--port', type = int, default = 8020)
	args = parser.parse_args()
	web.run_app(MailServer(args.path).init(web.Application()), port = args.port)



if __name__ == '__main__':
	main()
