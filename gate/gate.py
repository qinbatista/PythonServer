'''
gate.py

A gate acts as the interface between a client request and our internal network.
A client can connect to any gate to make any request. Requests made to the gates
can be distributed using a system such as NGINX.

A gate server has two TCP socket servers listening for connections simultaneously.
Each socket server operates using a different protocol.

The first socket server is the client facing server, and follows the client protocol.
The client protocol is responsible for first accepting a request from the client,
submitting the request to the job queue, and then waiting for the job to complete.

The second socket server is the backend facing server, and follows the worker protocol.
The worker protocol is responsible for first receiving completed jobs from various workers,
and then sending the completed job back to the correct client. Once a job has been returned to
a client, close the connection to the client.
'''

import uuid
import asyncio
import aioredis
import argparse
import contextlib
import nats.aio.client

class Gate:
	LINE_ENDING = b'\r\n'

	def __init__(self, args):
		self.args = args
		self.nats = nats.aio.client.Client()
		self.redis = None
		self.ws = None
		self.cs = None
		self.gid = None
		self.cwriters = {}


	async def init(self):
		await Gate.add_signal_handler(lambda: asyncio.create_task(self.shutdown()))

		await self.nats.connect(self.args.nats_addr, \
				ping_interval          = 5, \
				max_reconnect_attempts = 1, \
				closed_cb              = Gate.on_nats_closed, \
				reconnected_cb         = Gate.on_nats_reconnect, \
				disconnected_cb        = Gate.on_nats_disconnect)

		self.redis = await aioredis.create_redis(f'redis://{self.args.redis_addr}')
		await self.register_gate()

		self.ws = await asyncio.start_server(self.worker_protocol, port = self.args.wport)
		self.cs = await asyncio.start_server(self.client_protocol, port = self.args.cport, \
				ssl = Gate.init_ssl(self.args.certpath, self.args.keyfilepath, self.args.sslpw))

		asyncio.create_task(self.ws.serve_forever())
		asyncio.create_task(self.cs.serve_forever())



	async def start(self):
		try:
			await self.init()
			while self.running:
				await asyncio.sleep(1)
				await self.register_gate()
			await self.shutdown()
		except asyncio.CancelledError:
			pass
		except:
			await self.shutdown()


	async def shutdown(self):
		print(f'gate {self.gid}: SIGINT signal received, gracefully shutting down...')
		self.cs.sockets[0].close()
		print(f'gate {self.gid}: no longer accepting new connections')
		timeout = 4
		while self.cs._active_count > 0 and timeout > 0:
			print(f'gate {self.gid}: waiting on {self.cs._active_count} clients, \
					timing out in {timeout} seconds...')
			await asyncio.sleep(0.5)
			timeout -= 1

		if self.nats.is_connected:
			await self.nats.close()
			print(f'gate {self.gid}: nats closed')

		if not self.redis.closed:
			await self.redis.delete(f'gates.id.{self.gid}')
			self.redis.close()
			await self.redis.wait_closed()
			print(f'gate {self.gid}: redis closed')

		with contextlib.suppress(ValueError):
			self.ws.close()
		with contextlib.suppress(ValueError):
			self.cs.close()
		await self.ws.wait_closed()
		await self.cs.wait_closed()

		outstanding = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
		[task.cancel() for task in outstanding]
		print(f'gate {self.gid}: shutdown done.')


	async def client_protocol(self, reader, writer):
		try:
			await self.submit_job(await Gate.receive(reader), writer)
		except (asyncio.LimitOverrunError, asyncio.IncompleteReadError):
			writer.close()
		finally:
			with contextlib.suppress(ConnectionResetError):
				await writer.wait_closed()

	async def submit_job(self, job, writer):
		jid = uuid.uuid4().hex
		self.cwriters[jid] = writer
		await self.redis.set(jid, self.gid, expire = 10)
		await self.nats.publish(self.args.channel, f'{jid}~{job}'.encode())
		if self.args.debug: print(f'gate: submitted job {jid} {job}')

	async def worker_protocol(self, reader, writer):
		try:
			while self.running:
				asyncio.create_task(self.forward(await Gate.receive(reader)))
		except ValueError:
			pass
		except (asyncio.LimitOverrunError, asyncio.IncompleteReadError):
			pass
		finally:
			writer.close()
			await writer.wait_closed()

	async def forward(self, response):
		jid, resp = response.split('~', maxsplit = 1)
		cwriter = self.cwriters.pop(jid)
		cwriter.write(resp.encode() + Gate.LINE_ENDING)
		await cwriter.drain()
		cwriter.close()
		if self.args.debug: print(f'gate: forwarded {jid} {resp}')
		with contextlib.suppress(ConnectionResetError):
			await cwriter.wait_closed()

	async def register_gate(self):
		if self.gid is None:
			self.gid = 0
			ip = Gate.get_ip(self.args.hostname)
			while await self.redis.setnx(f'gates.id.{self.gid}', f'{ip}:{self.args.wport}') == 0:
				self.gid += 1
			if self.args.debug:
				print(f'gate {self.gid}: {ip}  client: {self.args.cport} worker: {self.args.wport}')
		await self.redis.expire(f'gates.id.{self.gid}', 10)
	
	@staticmethod
	async def receive(reader):
		raw = await reader.readuntil(Gate.LINE_ENDING)
		return raw.decode().strip()
	
	@staticmethod
	async def on_nats_disconnect():
		pass

	@staticmethod
	async def on_nats_reconnect():
		pass

	@staticmethod
	async def on_nats_closed():
		pass

	@staticmethod
	async def add_signal_handler(handler):
		import signal
		import platform
		if platform.system() != 'Windows':
			asyncio.get_running_loop().add_signal_handler(signal.SIGINT, handler)

	@staticmethod
	def init_ssl(certpath, keyfilepath, pw):
		import os
		import ssl
		context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
		bpath   = os.path.dirname(os.path.realpath(__file__))
		context.load_cert_chain(certfile = bpath + certpath, keyfile = bpath + keyfilepath, password = pw)
		return context

	@staticmethod
	def get_ip(hostname = False):
		import socket
		if hostname:
			return socket.gethostname()
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(('10.255.255.255', 1))
			return s.getsockname()[0]
		finally:
			s.close()

	@property
	def running(self):
		return not self.nats.is_closed




async def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--hostname', action = 'store_true')
	parser.add_argument('--debug', action = 'store_true')
	parser.add_argument('--channel', type = str, default = 'jobs')
	parser.add_argument('--cport', type = int, default = 8880)
	parser.add_argument('--wport', type = int, default = 8201)
	parser.add_argument('--nats-addr', type = str, default = '192.168.1.102:4221')
	parser.add_argument('--redis-addr', type = str, default = '192.168.1.102')
	parser.add_argument('--certpath' , type = str, default = '/cert/mycert.crt')
	parser.add_argument('--keyfilepath' , type = str, default = '/cert/rsa_private.key')
	parser.add_argument('--sslpw' , type = str, default = 'lukseun1')
	await Gate(parser.parse_args()).start()


if __name__ == '__main__':
	asyncio.run(main())
