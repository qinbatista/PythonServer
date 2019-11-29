'''
worker.py

A worker is responsible for handling client jobs published to the message queue.
Workers together form a work pool, across which many jobs can be distributed.
Workers can be added and removed dynamically depending upon the current server load.

The worker continually pulls job requests off the message queue.
Each job is then processed concurrently as a task.
Completed jobs are sent to the gate server which contains the requesting client.
'''

import sys
import json
import signal
import asyncio
import argparse
import message_handler
import nats.aio.client

from utility import worker_resources

import platform

class Worker:
	def __init__(self, args):
		self.args    = args
		self.mh      = message_handler.MessageHandler(token_addr = self.args.token_addr, \
				token_port = self.args.token_port, mail_addr = self.args.mail_addr, \
				mail_port  = self.args.mail_port)
		self.gates   = {}
		self.ujobs   = 0
		self.debug   = False
		self.running = False

		self.configs = worker_resources.ModuleConfigurations()
		self.resource= worker_resources.WorkerResources(self.args.redis_addr, self.args.db_addr, \
				self.args.db_user, self.args.db_pw)
		self.sid     = None
		self.nats    = None

	'''
	Starts the worker. Should only be called once.
	'''
	async def start(self, *, debug = False):
		self.debug = debug
		await self.init()
		print(f'this worker is operating on channel: {self.args.channel}')
		self.sid = await self.nats.subscribe(self.args.channel, 'workers', self.process_job)
		while self.running:
			await asyncio.sleep(1)
			await self.nats.flush()

	'''
	Processes the job request. Splits the message into cid, work parts.
	Submits the work to the message handler, and looks up correct gate with the cid.
	'''
	async def process_job(self, job):
		self.ujobs += 1
		cid, work = job.data.decode().split('~', maxsplit = 1)
		if self.debug: print(f'worker: received new job {work} with id {cid}')
		try:
			if self.debug: print(f'worker: calling messagehandler with args: {work}')
			resp = await asyncio.wait_for(self.mh.resolve(json.loads(work), self.resource, self.configs), 3)
		except asyncio.TimeoutError:
			if self.debug: print(f'worker: message handler call with args: {work} timed out...')
			resp = '{"status" : -2, "message" : "request timed out"}'
		except Exception as e:
			print(f'worker: message handler call with args: {work} had an error...')
			print(e)
			resp = '{"status" : -1, "message" : "programming error, this should not happen"}'
		if self.debug: print(f'worker: returning response {cid} back to correct gate...')
		await self._return_response(cid, resp, await self._get_gid(cid))
		if self.debug: print(f'worker: returned {cid} back to correct gate!')
		self.ujobs -= 1

	'''
	Establishes pre-requisite connections to other network services such as redis and nats.
	'''
	async def init(self):
		self.running = True
		self.nats = nats.aio.client.Client()
		await self.resource.init()
		await self.nats.connect(self.args.nats_addr, max_reconnect_attempts = 1)
		if platform.system() != 'Windows':
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
		timeout = 4
		while self.ujobs > 0 and timeout > 0:
			print(f'worker: there are {self.ujobs} outstanding jobs, timing out in {timeout} seconds...')
			await asyncio.sleep(1)
			timeout -= 1
		print('worker: closing gate connections')
		await self.resource.shutdown()
		for r,w in self.gates.values():
			w.close()
			await w.wait_closed()
		print('worker: mh shutting down') 
		await self.mh.shutdown()
		self.running = False
		print('worker: shutdown complete')



	'''
	Returns the gateid of the gate containing the requesting client.
	Opens a connection to the gate if it doesn't already exist.
	'''
	async def _get_gid(self, cid):
		gid = (await self.resource['redis'].get(cid)).decode()
		if gid not in self.gates or self.gates[gid][1].is_closing() or self.gates[gid][0].at_eof():
			if self.debug: print(f'adding a new gate connection for gate: {gid}')
			ip, port = (await self.resource['redis'].get('gates.id.' + gid)).decode().split(':')
			self.gates[gid] = await asyncio.open_connection(ip, int(port))
		return gid
	
	'''
	Sends the response back to the gate containing the requesting client
	'''
	async def _return_response(self, cid, response, gid):
		self.gates[gid][1].write((cid + '~' + response + '\r\n').encode())
		await self.gates[gid][1].drain()

async def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--channel'   , type = str, default = 'jobs')
	parser.add_argument('--nats-addr' , type = str, default = 'nats://nats')
	parser.add_argument('--redis-addr', type = str, default = 'redis://redis')
	parser.add_argument('--mail-addr' , type = str, default = 'http://mail')
	parser.add_argument('--token-addr', type = str, default = 'http://token')
	parser.add_argument('--mail-port' , type = int, default = 8020)
	parser.add_argument('--token-port', type = int, default = 8001)
	parser.add_argument('--db-addr'   , type = str, default = '192.168.1.102')
	parser.add_argument('--db-user'   , type = str, default = 'root')
	parser.add_argument('--db-pw'     , type = str, default = 'lukseun')
	await Worker(parser.parse_args()).start(debug=True)

if __name__ == '__main__':
	asyncio.run(main())
