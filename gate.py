
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
import signal
import asyncio
import aioredis
import contextlib
import nats.aio.client

import platform

from utility import config_reader

CFG = config_reader.wait_config()

class Gate:
	def __init__(self, cport = 8880, wport = 8201):
		self.ip       = self._read_ip()
		self.cport    = cport
		self.wport    = wport
		self.cwriters = {}

		self.cs       = None
		self.ws       = None
		self.gid      = None
		self.nats     = None
		self.redis    = None
		self.running  = False


	'''
	Starts the gate server. Should only be called once.
	'''
	async def start(self):
		try:
			await self.init()
			asyncio.create_task(self.cs.serve_forever())
			asyncio.create_task(self.ws.serve_forever())
			while self.running:
				await asyncio.sleep(300)
				await self.redis.expire('gates.id.' + self.gid, 600)
				print(f'gate {self.gid}: updating expiration time for redis registry')
		except:
			await self.shutdown()
	
	'''
	Gracefully shuts down the gate.
	Stop accepting incomming client connections and wait for all
	previously connected client sessions to complete.
	Then, cancel all remaining tasks and shutdown the server.
	'''
	async def shutdown(self):
		if self.running:
			print(f'gate {self.gid}: shutdown signal received, gracefully shutting down...')
			self.running = False
			self.cs.sockets[0].close()
			print(f'gate {self.gid}: closing listening socket. not accepting new connections.')
			timeout = 4
			while self.cs._active_count > 0 and timeout > 0:
				print(f'gate {self.gid}: waiting on {self.cs._active_count}, timing out in {timeout} seconds...')
				await asyncio.sleep(0.5)
				timeout -= 1
			if self.nats.is_connected:
				await self.nats.close()
				print(f'gate {self.gid}: nats closed')
			if not self.redis.closed:
				await self.redis.delete('gates.id.' + self.gid)
				self.redis.close()
				await self.redis.wait_closed()
				print(f'gate {self.gid}: redis closed')
			with contextlib.suppress(ValueError):
				self.ws.close()
			with contextlib.suppress(ValueError):
				self.cs.close()
			# cancel remaining tasks
			await self.ws.wait_closed()
			await self.cs.wait_closed()
			tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
			[task.cancel() for task in tasks]
		else:
			print(f'gate {self.gid}: done.')

	'''
	Establishes pre-requisite connections to other network services such as redis and nats.
	Advertises the port and address of the backend server to be used by workers submitting responses.
	Starts both socket servers.
	'''
	async def init(self):
		if platform.system() != 'Windows':
			asyncio.get_running_loop().add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(self.shutdown()))
		self.nats = nats.aio.client.Client()
		self.redis = await aioredis.create_redis(CFG['redis']['addr'])
		await self.nats.connect(CFG['nats']['addr'], max_reconnect_attempts = 1)
		await self._next_avail_gid()
		await self.redis.set('gates.id.' + self.gid, self.ip + ':' + str(self.wport), expire = 600)
		self.ws = await asyncio.start_server(self.worker_protocol, port = self.wport)
		self.cs = await asyncio.start_server(self.client_protocol, port = self.cport)
		print(f'gate {self.gid}: find me at {self.ip} on ports client: {self.cport}  worker: {self.wport}')
		self.running = True

	'''
	Reads the client's job request and then submits it to the work queue.
	The client's writer socket will get closed once the work server receives
	the response to the client.
	'''
	async def client_protocol(self, reader, writer):
		try:
			await self._submit_job(await self._receive(reader), writer)
		except (asyncio.LimitOverrunError, asyncio.IncompleteReadError):
			writer.close()
		finally:
			await writer.wait_closed()

	'''
	Listens for completed jobs from a worker. Once a completed job has been received,
	launches a task to return that response back to the client.
	'''
	async def worker_protocol(self, reader, writer):
		try:
			while self.running:
				asyncio.create_task(self._relay_response(await self._receive(reader)))
		except ValueError:
			print(f'gate {self.gid}: Missing \'~\' delimiter in message. Closing backend connection.')
		except (asyncio.LimitOverrunError, asyncio.IncompleteReadError):
			print(f'gate {self.gid}: Backend connection did not follow protocol, closing connection.')
		finally:
			writer.close()
			await writer.wait_closed()

	'''
	Parses the worker message to find the cid of the original request.
	Uses the cid to discover which client to return the response to.
	Closes the client's writer socket after sending the response.
	'''
	async def _relay_response(self, r):
		cid, response = r.split('~', maxsplit = 1)
		cwriter = self.cwriters.pop(cid)
		cwriter.write((response + '\r\n').encode())
		await cwriter.drain()
		cwriter.close()
		await cwriter.wait_closed()

	'''
	Generates a unique job id, registers the client and gate to redis, and
	submits the job to the work queue.
	'''
	async def _submit_job(self, job, writer):
		cid = uuid.uuid4().hex
		self.cwriters[cid] = writer
		await self.redis.set(cid, self.gid, expire = 10)
		await self.nats.publish('jobs', (cid + '~' + job).encode())
		print(f'gate: submitted new job with id {cid} and args {job}')
		print(f'gate: waiting for job {cid} to complete')

	async def _receive(self, reader):
		raw = await reader.readuntil(b'\r\n')
		return raw.decode().strip()

	async def _next_avail_gid(self):
		gid = 1
		while await self.redis.exists('gates.id.' + str(gid)):
			gid += 1
		self.gid = str(gid)

	# reads the ip address of the machine
	# TODO possibly move to another module
	def _read_ip(self):
		import socket
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(('10.255.255.255', 1))
			return s.getsockname()[0]
		finally:
			s.close()

if __name__ == '__main__':
	asyncio.run(Gate().start())
