'''
edge.py
'''

import enum
import signal
import asyncio
import aioredis
import nats.aio.client

LINE_ENDING    = '\r\n'
COMMAND_LENGTH = 10

class ChatProtocolError(Exception):
	pass

class Command(enum.Enum):
	EXIT     = 'EXIT'
	FAMILY   = 'FAMILY'
	PUBLIC   = 'PUBLIC'
	REGISTER = 'REGISTER'

class Edge:
	def __init__(self, port = 9000):
		self.port     = 9000
		self.pubsub   = nats.aio.client.Client()
		self.channels = set()

		self.redis   = None
		self.server  = None
		self.running = False

	async def start(self):
		try:
			await self.init()
			asyncio.create_task(self.server.serve_forever())
			while self.running:
				await asyncio.sleep(300)
		except:
			await self.shutdown()

	async def init(self):
		asyncio.get_running_loop().add_signal_handler(signal.SIGINT, \
				lambda: asyncio.create_task(self.shutdown()))
		await self.pubsub.connect('nats://192.168.1.102', max_reconnect_attempts = 1)
		self.redis   = await aioredis.create_redis('redis://192.168.1.102')
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
		try:
			while True:
				pass
		except:
			pass
		finally:
			pass

	async def server_protocol(self, message):
		message.data.decode()
	
	async def client_handshake(reader, writer):
		cmd, nonce = await receive(reader)
		if cmd == Command.REGISTER:
			world, gn, fn = await validate_nonce(nonce)
			if world is not None:
				return gn
		raise ChatProtocolError

	# checks if the login token provided by the client is valid. returns (None, None, None) if invalid.
	async def validate_nonce(nonce):
		return (None, None, None)

	# returns (command enum, message) if connection is alive, raises ConnectionResetError otherwise
	async def receive(self, reader):
		raw = await reader.readuntil(LINE_ENDING.encode())
		if raw == b'':
			raise ConnectionResetError
		decoded = raw.decode().strip()
		return enums.Command(decoded[:COMMAND_LENGTH].lstrip('0')), decoded[COMMAND_LENGTH:]

	# returns encoded message formatted to protocol specifications
	def make_message(self, cmd, msg = ''):
		return (cmd.value.zfill(COMMAND_LENGTH) + msg + LINE_ENDING).encode()

	



##################################################
async def main():
	edge = Edge()
	await edge.start()

if __name__ == '__main__':
	asyncio.run(main())
