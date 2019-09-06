'''
worker.py

A worker is responsible for handling client jobs published to the message queue.
Workers together form a work pool, across which many jobs can be distributed.
Workers can be added and removed dynamically depending upon the current server load.

The worker continually pulls job requests off the message queue.
Each job is then processed concurrently as a task.
Completed jobs are sent to the gate server which contains the requesting client.
'''

import signal
import asyncio
import aiohttp
import aioredis
import message_handler
import nats.aio.client

class Worker:
	def __init__(self):
		self.mh      = message_handler.MessageHandler()
		self.gates   = {}
		self.ujobs   = 0
		self.running = False

		self.sid     = None
		self.nats    = None
		self.redis   = None
		self.session = None

	'''
	Starts the worker. Should only be called once.
	'''
	async def start(self):
		try:
			await self.init()
			self.sid = await self.nats.subscribe('jobs', 'workers', self.process_job)
			subbed = True
			while self.running:
				await asyncio.sleep(1)
		finally:
			await self.session.close()

	'''
	Processes the job request. Splits the message into cid, work parts.
	Submits the work to the message handler, and looks up correct gate with the cid.
	'''
	async def process_job(self, job):
		self.ujobs += 1
		cid, work = job.data.decode().split('~', maxsplit = 1)
		response  = await self.mh.resolve(work, self.session)
		await self._return_response(cid, response, await self._get_gid(cid))
		self.ujobs -= 1

	'''
	Establishes pre-requisite connections to other network services such as redis and nats.
	'''
	async def init(self):
		self.running = True
		self.nats = nats.aio.client.Client()
		self.session = aiohttp.ClientSession()
		self.redis = await aioredis.create_redis('redis://192.168.1.102')
		await self.nats.connect('nats://192.168.1.102/', max_reconnect_attempts = 1)
		asyncio.get_running_loop().add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(self.shutdown()))

	'''
	Gracefully shuts down the worker. Drains outstanding messages from the message queue,
	and closes nats connection. Waits for uncompleted client jobs to finish.
	'''
	async def shutdown(self):
		print('worker: SIGINT received, gracefully shutting down...')
		await self.nats._unsubscribe(self.sid)
		await self.nats.flush()
		print('worker: unsubscribed from job queue. not accepting new jobs')
		while self.ujobs > 0:
			print(f'worker: there are {self.ujobs} outstanding jobs')
			await asyncio.sleep(1)
		print('worker: closing gate connections')
		for r,w in self.gates.values():
			w.close()
			await w.wait_closed()
		self.running = False
		print('worker: shutdown complete')



	'''
	Returns the gateid of the gate containing the requesting client.
	Opens a connection to the gate if it doesn't already exist.
	'''
	async def _get_gid(self, cid):
		gid = (await self.redis.get(cid)).decode()
		if gid not in self.gates or self.gates[gid][1].is_closing() or self.gates[gid][0].at_eof():
			print(f'adding a new gate connection for gate: {gid}')
			ip, port = (await self.redis.get('gates.id.' + gid)).decode().split(':')
			self.gates[gid] = await asyncio.open_connection(ip, int(port))
		return gid
	
	'''
	Sends the response back to the gate containing the requesting client
	'''
	async def _return_response(self, cid, response, gid):
		self.gates[gid][1].write((cid + '~' + response + '\r\n').encode())
		await self.gates[gid][1].drain()


if __name__ == '__main__':
	worker = Worker()
	asyncio.run(worker.start())
