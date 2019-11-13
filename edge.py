'''
edge.py
'''

import enum
import signal
import asyncio
import aioredis
import contextlib
import nats.aio.client

from utility     import config_reader
from collections import defaultdict

LINE_ENDING        = '\r\n'
LINE_ENDING_B      = LINE_ENDING.encode()
COMMAND_MAX_LENGTH = 10

class ChatProtocolError(Exception):
	pass

class Command(enum.Enum):
	FAMILY   = 'FAMILY'
	PUBLIC   = 'PUBLIC'
	REGISTER = 'REGISTER'
	EXIT     = 'EXIT'
	OK       = 'OK'

class User:
	def __init__(self, writer, world, gn, fn = ''):
		self.gn     = gn
		self.fn     = fn if fn != '' else None
		self.world  = world
		self.writer = writer

class Userlist:
	def __init__(self):
		self.public = defaultdict(set)
		self.family = defaultdict(lambda: defaultdict(set))
	
	def add(self, user):
		self.public[user.world].add(user.writer)
		if user.fn is not None:
			self.family[user.world][user.fn].add(user.writer)

	def remove(self, user):
		if user is not None:
			with contextlib.suppress(KeyError):
				self.public[user.world].remove(user.writer)
			if user.fn is not None:
				with contextlib.suppress(KeyError):
					self.family[user.world][user.fn].remove(user.writer)

	def get_public(self, world):
		with contextlib.suppress(KeyError):
			return self.public[world]
		return set()

	def get_family(self, world, fn):
		with contextlib.suppress(KeyError):
			return self.family[world][fn]
		return set()

class Edge:
	def __init__(self, port = 9000):
		self.port       = port
		self.pubsub     = nats.aio.client.Client()
		self.channels   = set()
		self.userlist   = Userlist()
		self.drain_lock = asyncio.Lock()

		self.redis      = None
		self.server     = None
		self.running    = False

	async def start(self):
		try:
			await self.init()
			asyncio.create_task(self.server.serve_forever())
			print(f'Starting edge server on port {self.port}')
			while self.running:
				await asyncio.sleep(300)
		except:
			await self.shutdown()

	async def init(self):
		asyncio.get_running_loop().add_signal_handler(signal.SIGINT, \
				lambda: asyncio.create_task(self.shutdown()))
		await self.pubsub.connect('nats://192.168.1.102', max_reconnect_attempts = 1)
		self.redis   = await aioredis.create_redis('redis://192.168.1.102', encoding = 'utf-8')
		self.server  = await asyncio.start_server(self.client_protocol, port = self.port)
		self.running = True
	
	async def shutdown(self):
		if self.running:
			self.running = False
			self.server.close()
			await self.server.wait_closed()
			if not self.pubsub.is_connected:
				await self.pubsub.close()
			if not self.redis.closed:
				self.redis.close()
				await self.redis.wait_closed()
			tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
			[task.cancel() for task in tasks]

	async def client_protocol(self, reader, writer):
		user = None
		try:
			user = await self.client_handshake(reader, writer)
			print(f'User {user.gn} has joined world {user.world}')
			while True:
				cmd, payload = await self.receive(reader)
				if cmd == Command.PUBLIC:
					await self.pubsub.publish(self.encode_channel_public(user.world), \
							f'{user.gn}:{payload}'.encode())
				elif cmd == Command.FAMILY and user.fn is not None:
					await self.pubsub.publish(self.encode_channel_family(user.world, user.fn), \
							f'{user.gn}:{payload}'.encode())
				else:
					break
		except (ValueError, ChatProtocolError, ConnectionResetError, \
				asyncio.streams.IncompleteReadError):
			pass
		finally:
			self.userlist.remove(user)
			writer.close()
			await writer.wait_closed()
			if user != None: print(f'User {user.gn} has left world {user.world}')

	# receives messages from pubsub server and distributes them to the interested connected clients
	# unsubscribes from pubsub channels when there are no longer any interested clients
	async def server_protocol(self, message):
		world, family = self.decode_channel(message.subject)
		users = self.userlist.get_public(world) if not family \
				else self.userlist.get_family(world, family)
		if len(users) != 0:
			await self.send(self.make_message(Command.PUBLIC if not family else Command.FAMILY, \
					message.data), *users)
		else:
			await self.pubsub.unsubscribe(message.subject)
			print(f'Unsubscribing to channel: {message.subject}')
	
	# performs initial client handshake. requires client to provide a valid login token.
	# raises ChatProtocolError if protocol is not followed, or an invalid login token was provided.
	async def client_handshake(self, reader, writer):
		print('new client_handshake')
		cmd, nonce = await self.receive(reader)
		if cmd == Command.REGISTER:
			user = await self.validate_login_token(writer, nonce)
			if user is not None:
				await self.register_user(user)
				await self.send(self.make_message(Command.OK), writer)
				return user
		raise ChatProtocolError

	# registers the user with the chat server.
	# subscribes the chat server to the channels required by the client if not already subscribed.
	async def register_user(self, user):
		self.userlist.add(user)
		public_channel = self.encode_channel_public(user.world)
		await self.subscribe_once(public_channel)
		if user.fn is not None:
			family_channel = self.encode_channel_family(user.world, user.fn)
			await self.subscribe_once(family_channel)

	# checks if the login token provided by the client is valid.
	# returns a User object on valid token, None otherwise.
	async def validate_login_token(self, writer, nonce):
		token = await self.redis.hgetall(f'chat.logintokens.{nonce}')
		if len(token) == 0:
			return None
		await self.redis.delete(f'chat.logintokens.{nonce}')
		return User(writer, token['world'], token['gn'], token['fn'])

	# returns (command enum, message) if connection is alive.
	# raises ConnectionResetError otherwise
	async def receive(self, reader):
		raw = await reader.readuntil(LINE_ENDING_B)
		if raw == b'':
			raise ConnectionResetError
		decoded = raw.decode().strip()
		return (Command(decoded[:COMMAND_MAX_LENGTH].lstrip('0')), decoded[COMMAND_MAX_LENGTH:])

	# sends the message to all given client writers
	async def send(self, msg, *writers):
		for writer in writers:
			if not writer.is_closing():
				writer.write(msg)
				async with self.drain_lock:
					await writer.drain()

	async def subscribe_once(self, channel):
		if channel not in self.channels:
			print(f'Subscribing to channel: {channel}')
			self.channels.add(channel)
			await self.pubsub.subscribe(channel, cb = self.server_protocol)

	# returns encoded message formatted to protocol specifications
	def make_message(self, cmd, encodedmsg = b''):
		return cmd.value.zfill(COMMAND_MAX_LENGTH).encode() + encodedmsg + LINE_ENDING_B

	def encode_channel_public(self, world):
		return f'chat~{world}~public'

	def encode_channel_family(self, world, fn):
		return f'chat~{world}~family~{fn}'

	def decode_channel(self, channel):
		decoded = channel.split('~')
		return (decoded[1], None) if len(decoded) < 4 else (decoded[1], decoded[3])


	



######################################################################################################
async def main():
	await Edge().start()

if __name__ == '__main__':
	asyncio.run(main())
