import time
import requests
import configparser

import os
import sys
import queue
import signal
import asyncio
import tormysql
import threading
import contextlib

from datetime import datetime
from collections import defaultdict


MAXSIZE = 250


class ChatProtocolError(Exception):
	pass

class SignalHandler:
	def __init__(self, stopper, worker):
		self.stopper = stopper
		self.worker = worker
	
	def __call__(self, signum, frame):
		self.stopper.set()
		self.worker.join()
		sys.exit(0)

# runs in a separate thread, logs all chat messages recieved through the queue
def chat_logger(world, in_queue, stopper):
	while not stopper.is_set():
		today = datetime.today().strftime('%Y/%m/%d')
		os.makedirs(f'chatlogs/{today}/', exist_ok = True)
		with open(f'chatlogs/{today}/{world}.log', 'a') as log:
			while not stopper.is_set() and today == datetime.today().strftime('%Y/%m/%d'):
				try:
					wait = 0
					name, command, payload = in_queue.get(block = False)
					log.write(f'{time.time()}~{name}~{command}~{payload}\n')
				except queue.Empty:
					time.sleep(wait)
					wait = min(wait + 0.1, 2)

class ChatServer:
	def __init__(self, world = ''):
		self.world = world
		self.users = defaultdict(dict)
		self.families = defaultdict(lambda: defaultdict(set))
		self.pool = tormysql.ConnectionPool(max_connections = 10, host = '192.168.1.102', user = 'root', passwd = 'lukseun', db = self.world if self.world != 0 else 'aliya', charset = 'utf8')
		self.stopper = threading.Event()
		self.in_queue = queue.Queue()
		self.logger = threading.Thread(target = chat_logger, args = (self.world, self.in_queue, self.stopper))
		signal.signal(signal.SIGINT, SignalHandler(self.stopper, self.logger))

	async def run(self, port):
		async with await asyncio.start_server(self.handle_client, None, port) as s:
			print(f'starting chat server for world "{self.world}" on port {port}...')
			self.logger.start()
			await s.serve_forever()
	
	# the main protocol loop. if chat protocol is not followed, close connection immediately
	async def handle_client(self, reader, writer):
		name = ''
		try:
			name = await self.client_handshake(reader, writer)
			print(f'hello, {name}...')
			while True:
				command, payload = await self._receive(reader)
				self.in_queue.put((name, command, payload))
				if command == 'PUBLIC':
					await self.send_public(name, payload)
				elif command == 'FAMILY':
					await self.send_family(name, payload)
				elif command == 'PRIVATE':
					await self.send_private(name, payload)
				elif command == 'UPDATE':
					await self.update(name)
				elif command == 'EXIT':
					break
				else: raise ChatProtocolError
		except (ChatProtocolError):
			print(f'ChatProtocolError raised for user {name}...')
		except ConnectionResetError:
			print(f'ConnectionReset for user {name}...')
		except KeyError as e:
			print(e)
			print(f'KeyError for user {name}...')
		finally:
			await self._cleanup(name, writer)
			print(f'connection closed for {name}')

	# propagates database updates to all applicable users within the calling user's circle
	async def update(self, name):
		if 'fid' not in self.users[name]:
			await self._update_fid(name)
		if 'fid' in self.users[name]:
			fid = self.users[name]['fid']
			oldmembers = self.families[fid]['members']
			fname, members = await self._update_families_cache(fid)
			for changed in oldmembers ^ members:
				await self._update_fid(changed)
			if not fname:
				del self.families[fid]

	# forwards the message to all users in family chat
	async def send_family(self, name, message):
		if 'fid' not in self.users[name]:
			await self._send(self._make_message('ERROR', '81:You have no family'), self.users[name]['w'])
		elif len(self.families[self.users[name]['fid']]['members']) == 1:
			await self._send(self._make_message('ERROR', '80:Your family is offline'), self.users[name]['w'])
		else:
			await self._send(self._make_message('FAMILY', f'{name}:{message}'), *[self.users[u]['w'] for u in self.families[self.users[name]['fid']]['members']])


	# sends message directly to user specified in payload
	async def send_private(self, name, payload):
		target, message = payload.split(':', maxsplit = 1)
		if target == name:
			await self._send(self._make_message('ERROR', '91:Don\'t be an idiot'), self.users[name]['w'])
		elif target not in self.users:
			await self._send(self._make_message('ERROR', '90:User not online'), self.users[name]['w'])
		else:
			await self._send(self._make_message('PRIVATE', f'{name}:{target}:{message}'), self.users[name]['w'], self.users[target]['w'])

	# forwards the message to all users in public chat
	async def send_public(self, name, message):
		await self._send(self._make_message('PUBLIC', f'{name}:{message}'), *[v['w'] for v in self.users.values()])

	# performs handshake with client on newly established connection. throws ChatProtocolError
	async def client_handshake(self, reader, writer):
		command, name = await self._receive(reader)
		if command != 'REGISTER' or not self._valid_name(name): raise ChatProtocolError
		if name in self.users:
			await self._handle_name_collision(name)
		self.users[name]['w'] = writer
		await self._update_fid(name)
		return name

	# fetches the latest family information from the database and updates the cached version
	async def _update_families_cache(self, fid):
		fname, members = await self._get_family_information(fid)
		if fname:
			self.families[fid]['fname'] = fname
			self.families[fid]['members'] = {m for m in members if m in self.users}
		return (None, {}) if not fname else (fname, {m for m in members if m in self.users})

	# cleans up old fid and group membership, and updates with new fid and group membership
	# does not fetch family_name from database
	async def _update_fid(self, name):
		fid = await self._get_familyid(name)
		if 'fid' in self.users[name]:
			self.families[self.users[name]['fid']]['members'].discard(name)
			del self.users[name]['fid']
		if fid:
			self.users[name]['fid'] = fid
			self.families[fid]['members'].add(name)
	
	# in the event of name collision, close old connection and remove name from family group
	async def _handle_name_collision(self, name):
		if 'fid' in self.users[name]:
			self.families[self.users[name]['fid']]['members'].remove(name)
		if 'w' in self.users[name]:
			await self._close_connection(self.users[name]['w'])
		del self.users[name]

	# returns (command, arguments) if connection is alive, raises ChatProtocolError otherwise
	async def _receive(self, reader):
		raw = await reader.read(MAXSIZE)
		if raw == b'': raise ChatProtocolError
		decoded = raw.decode().strip()
		return decoded[:10].lstrip('0'), decoded[10:]

	# sends a message to the given writers
	async def _send(self, message, *args):
		writers = []
		for writer in args:
			if not writer.is_closing():
				writer.write(message)
				writers.append(writer.drain())
		await asyncio.gather(*writers)
	
	# returns familyid if user is part of a family, None otherwise
	async def _get_familyid(self, name):
		async with await self.pool.Connection() as conn:
			async with conn.cursor() as cursor:
				await cursor.execute(f'SELECT familyid FROM player WHERE game_name = "{name}";')
				data = cursor.fetchall()
				return None if data == () else data[0][0]

	# returns (familyname, {set of users}) if family exists, None otherwise
	async def _get_family_information(self, fid):
		async with await self.pool.Connection() as conn:
			async with conn.cursor() as cursor:
				await cursor.execute(f'SELECT * FROM families WHERE familyid = "{fid}";')
				data = cursor.fetchall()
				return (None, {}) if data == () else (data[0][1], {u for u in data[0][2:] if u != ''})

	async def _cleanup(self, name, writer):
		with contextlib.suppress(KeyError):
			self.families[self.users[name]['fid']]['members'].remove(name)
			del self.users[name]
		await self._close_connection(writer)

	async def _close_connection(self, writer):
		writer.close()
		await writer.wait_closed()

	def _make_message(self, command, message = ''):
		return (command.zfill(10) + message).encode()

	def _valid_name(self, name):
		return len(name) > 0

def get_config():
	while True:
		try:
			r = requests.get('http://localhost:8000/register_chat_server')
			return r.json()
		except requests.exceptions.ConnectionError:
			print('Could not find configuration server, retrying in 5 seconds...')
			time.sleep(5)

if __name__ == '__main__':
	config = get_config()
	server = ChatServer(config['world'])
	asyncio.run(server.run(config['port']))
