#!/usr/bin/env python3

# TODO REWRITE EVERYTHING, it sucks right now

import time
import asyncio
import tormysql
import requests
import contextlib
import configparser

from collections import defaultdict


MAXSIZE = 250

class ChatProtocolError(Exception):
	pass

class ChatServer:
	def __init__(self):
		self.users = defaultdict(dict)
		self.fchats = defaultdict(set)
		self.pool = tormysql.ConnectionPool(max_connections = 10, host = '192.168.1.102', user = 'root', passwd = 'lukseun', db = 'aliya', charset = 'utf8')
		self.commands = {'PUBLIC', 'FAMILY', 'PRIVATE', 'EXIT', 'UPDATE'}

	async def run(self):
		config = get_config()
		port = config.getint('chat_server', 'port')
		async with await asyncio.start_server(self.on_connect, '127.0.0.1', port) as s:
			print(f'starting chat server on port {port}...')
			await s.serve_forever()
	
	async def on_connect(self, reader, writer):
		name = ''
		try:
			name = await self._client_handshake(reader, writer)
			print(f'hello, {name}...')
			while True:
				command, payload = await self._receive(reader)
				if command == 'PUBLIC':
					await self._forward_public(name, payload)
				elif command == 'FAMILY':
					await self._forward_family(name, payload)
				elif command == 'PRIVATE':
					await self._forward_private(name, payload)
				elif command == 'UPDATE':
					await self._update(name)
				elif command == 'EXIT':
					break
				else:
					raise ChatProtocolError
			print(f'Received exit signal from {name}, closing connection.')

		except (ChatProtocolError, asyncio.IncompleteReadError, ValueError):
			print(f'ChatProtocolError encountered for user {name}, closing connection.')
		finally:
			with contextlib.suppress(KeyError):
				self.fchats[self.users[name]['fid']].remove(name)
				del self.users[name]
			writer.close()
			await writer.wait_closed()
	


	async def _update(self, name):
		if 'fid' in self.users[name]:
			fid = self.users[name]['fid']
			family = await self._get_users_with_fid(fid)
			if family:
				for u in self.fchats[fid].union(family):
					await self._update_fid(u)
			else:
				for u in self.fchats[fid]:
					await self._update_fid(u)
				self.fchats.pop(fid, None)
		else:
			await self._update_fid(name)



	async def _get_users_with_fid(self, fid):
		async with await self.pool.Connection() as conn:
			async with conn.cursor() as cursor:
				await cursor.execute(f'SELECT game_name FROM player WHERE familyid = "{fid}";')
				data = cursor.fetchall()
				return None if data == () else {v[0] for v in data}


	async def _forward_family(self, name, message):
		if 'fid' in self.users[name] and len(self.fchats[self.users[name]['fid']]) == 1:
			self.users[name]['w'].write(self._make_message('ERROR','All of your family is offline'))
			await self.users[name]['w'].drain()
		elif 'fid' in self.users[name]:
			writers = []
			to_remove = set()
			for user in self.fchats[self.users[name]['fid']]:
				try:
					if not self.users[user]['w'].is_closing():
						self.users[user]['w'].write(self._make_message('FAMILY', f'{name} : {message}'))
						writers.append(self.users[user]['w'].drain())
				except KeyError:
					to_remove.add(user)
			for u in to_remove:
				self.fchats[self.users[name]['fid']].remove(u)
				self.users.pop(u, None)
			await asyncio.gather(*writers)
		else:
			self.users[name]['w'].write(self._make_message('ERROR','You do not belong to a family chat'))
			await self.users[name]['w'].drain()

	async def _forward_private(self, name, payload):
		target, message = payload.split(':', maxsplit = 1)
		if target == name:
			self.users[name]['w'].write(self._make_message('ERROR', 'You can not send a message to yourself'))
			await self.users[name]['w'].drain()
		elif target in self.users:
			writers = []
			self.users[name]['w'].write(self._make_message('PRIVATE', f'{name} : {message}'))
			self.users[target]['w'].write(self._make_message('PRIVATE', f'{name} : {message}'))
			writers.append(self.users[name]['w'].drain())
			writers.append(self.users[target]['w'].drain())
			await asyncio.gather(*writers)
		else:
			self.users[name]['w'].write(self._make_message('ERROR', 'User is not online'))
			await self.users[name]['w'].drain()


	async def _forward_public(self, name, message):
		writers = []
		for user, info in self.users.items():
			if not info['w'].is_closing():
				info['w'].write(self._make_message('PUBLIC', f'{name} : {message}'))
				writers.append(info['w'].drain())
		await asyncio.gather(*writers)
	
	async def _client_handshake(self, reader, writer):
		command, name = await self._receive(reader)
		if command != 'REGISTER' or not self._valid_name(name): raise ChatProtocolError
		if name in self.users:
			if 'fid' in self.users[name]:
				self.fchats[self.users[name]['fid']].remove(name)
				self.users[name].pop('fid', None)
			if 'w' in self.users[name]:
				w = self.users[name].pop('w')
				w.close()
				await w.wait_closed()
			self.users.pop(name, None)
		self.users[name]['w'] = writer
		await self._update_fid(name)
		return name

	async def _update_fid(self, name):
		if 'fid' in self.users[name]:
			self.fchats[self.users[name]['fid']].remove(name)
			del self.users[name]['fid']
		fid = await self._lookup_family_id(name)
		if fid != None:
			self.users[name]['fid'] = fid
			self.fchats[fid].add(name)

	async def _receive(self, reader):
		raw = await reader.read(MAXSIZE)
		if raw == b'':
			raise ChatProtocolError
		decoded = raw.decode().strip()
		return decoded[:10].lstrip('0'), decoded[10:]

	async def _lookup_family_id(self, name):
		async with await self.pool.Connection() as conn:
			async with conn.cursor() as cursor:
				await cursor.execute(f'SELECT familyid FROM player WHERE game_name = "{name}";')
				data = cursor.fetchall()
				if data == () or ('',) in data:
					return None
				return data[0][0]

	def _make_message(self, command, message = ''):
		return (command.zfill(10) + message).encode()

	def _valid_name(self, name):
		return len(name) > 0


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






if __name__ == '__main__':
	s = ChatServer()
	asyncio.run(s.run())
