'''
worker.py

A worker is responsible for handling client jobs published to the message queue.
Workers together form a work pool, across which many jobs can be distributed.
Workers can be added and removed dynamically depending upon the current server load.

The worker continually pulls job requests off the message queue.
Each job is then processed concurrently as a task.
Completed jobs are sent to the gate server which contains the requesting client.
'''

import json
import asyncio
import argparse
import message_handler
import nats.aio.client

from utility import worker_resources

class Worker:
	LINE_ENDING = b'\r\n'

	def __init__(self, args):
		self.sid = None
		self.ujobs = 0
		self.gates = {}
		self.args = args
		self.nats = nats.aio.client.Client()

		self.mh = message_handler.MessageHandler(token_addr = self.args.token_addr, \
				token_port = self.args.token_port, mail_addr = self.args.mail_addr, \
				mail_port = self.args.mail_port)
		self.configs = worker_resources.ModuleConfigurations(self.args.config_addr, self.args.config_port)
		self.resource = worker_resources.WorkerResources(self.args.redis_addr, self.args.db_addr,
				self.args.db_user, self.args.db_pw, self.args.db_port)

	async def start(self):
		try:
			await self.init()
			print(f'this worker is operating on channel: {self.args.channel}')
			self.sid = await self.nats.subscribe(self.args.channel, 'workers', self.process_job)
			while self.running:
				await asyncio.sleep(1)
				await self.nats.flush()
			await self.shutdown()
		except asyncio.CancelledError:
			pass
		except:
			await self.shutdown()

	async def init(self):
		await Worker.add_signal_handler(lambda: asyncio.create_task(self.shutdown()))

		await self.nats.connect(self.args.nats_addr, \
				ping_interval          = 5, \
				max_reconnect_attempts = 1, \
				closed_cb              = Worker.on_nats_closed, \
				reconnected_cb         = Worker.on_nats_reconnect, \
				disconnected_cb        = Worker.on_nats_disconnect)

		await self.resource.init()
	
	async def process_job(self, job):
		self.ujobs += 1
		jid, work = job.data.decode().split('~', maxsplit = 1)
		if self.args.debug: print(f'worker: received {jid}')

		try:
			if self.args.debug: print(f'worker: calling messagehandler with args: {work}')
			resp = await asyncio.wait_for(self.mh.resolve(json.loads(work), self.resource, self.configs), 10)
		except asyncio.TimeoutError:
			if self.args.debug: print(f'worker: job {jid} : {work} timed out...')
			resp = '{"status" : -2, "message" : "request timed out"}'
		except Exception as e:
			print(f'worker: message handler with args {work} had an error..')
			print(e)
			resp = '{"status" : -1, "message" : "programming error, this should not happen"}'
		if self.args.debug: print(f'worker: returning {jid} to gate..', end = '')
		await self.return_response(jid, resp)
		if self.args.debug: print('done')
		self.ujobs -= 1
	
	async def return_response(self, jid, resp):
		gid = await self.get_gate(jid)
		self.gates[gid][1].write(f'{jid}~{resp}'.encode() + Worker.LINE_ENDING)
		await self.gates[gid][1].drain()

	async def get_gate(self, jid):
		gid = await self.resource['redis'].get(jid)
		if gid not in self.gates or self.gates[gid][1].is_closing() or self.gates[gid][0].at_eof():
			if self.args.debug: print(f'worker: adding new gate connection to gate {gid}')
			ip, port = (await self.resource['redis'].get(f'gates.id.{gid}')).split(':')
			self.gates[gid] = await asyncio.open_connection(ip, int(port))
		return gid


	async def shutdown(self):
		print('worker: SIGINT received, gracefully shutting down...')
		await self.nats._unsubscribe(self.sid)
		await self.nats.flush()
		print('worker: unsubscribed from job queue. not accepting new jobs')
		
		timeout = 4
		while self.ujobs > 0 and timeout > 0:
			print(f'worker: there are {self.ujobs} outstanding jobs..')
			await asyncio.sleep(1)
			timeout -= 1

		print('worker: closing gate connections.')
		await self.resource.shutdown()
		for r, w in self.gates.values():
			w.close()
			await w.wait_closed()
		print('worker: mh shutting down..')
		await self.mh.shutdown()

		outstanding = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
		[task.cancel() for task in outstanding]

		print('worker: shutdown complete')


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

	@property
	def running(self):
		return not self.nats.is_closed


async def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--debug'      , action = 'store_true')
	parser.add_argument('--db-pw'      , type = str, default = 'lukseun')
	parser.add_argument('--db-user'    , type = str, default = 'root')
	parser.add_argument('--db-addr'    , type = str, default = '192.168.1.143')
	parser.add_argument('--db_port'    , type = int, default = 3306)
	parser.add_argument('--channel'    , type = str, default = 'jobs')
	parser.add_argument('--config-port', type = int, default = 8000) 
	parser.add_argument('--config-addr', type = str, default = 'localhost')
	parser.add_argument('--token-addr' , type = str, default = 'token')
	parser.add_argument('--token-port' , type = int, default = 8001)
	parser.add_argument('--mail-addr'  , type = str, default = 'mail')
	parser.add_argument('--mail-port'  , type = int, default = 8020)
	parser.add_argument('--nats-addr'  , type = str, default = 'nats')
	parser.add_argument('--redis-addr' , type = str, default = 'redis')
	await Worker(parser.parse_args()).start()


if __name__ == '__main__':
	asyncio.run(main())
