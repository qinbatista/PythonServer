'''
simulator.py

Simulates users playing our game.
Able to make intelligent decisions such as inviting other simulated users to become friends.
Records timing metrics for all messages sent.
'''

import os
import ssl
import json
import time
import uuid
import queue
import pickle
import random
import struct
import socket
import asyncio
import argparse
import threading
import contextlib
import statistics

from functions import FunctionList
from dataclasses import dataclass, field
from collections import defaultdict


'''
Fascilitates a method of sending timed requests to the server.
Loads the SSL context a single time.
All simulated users share the same client instance.
'''
class Client:
	def __init__(self, host, port, certpath):
		self.host = host
		self.port = port
		self.ending = b'\r\n'
		self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
		self.context.load_verify_locations(certpath)
		self.context.check_hostname = False

	async def send(self, function, token, session, world):
		try:
			reader, writer = await asyncio.open_connection(self.host, self.port, ssl = self.context)
			request = function.dump(token, session, world).encode() + self.ending
			writer.write(request)
			await writer.drain()
			start = time.time()
			raw_resp = await reader.readuntil(self.ending)
			finish = time.time()
			return Metric(function.name, start, finish, request, raw_resp)
		finally:
			if writer:
				writer.close()
				await writer.wait_closed()

'''
Represents the global state of the simulation.
The global state is shared amongst all of the User instances.
'''
@dataclass
class GlobalState:
	client: Client
	users: defaultdict(set) = field(default_factory = lambda: defaultdict(set))
	families: defaultdict(set) = field(default_factory = lambda: defaultdict(set))
	metrics: asyncio.Queue = field(default_factory = asyncio.Queue)
	switch: dict = None

	def add(self, group, world, value):
		self.resolve_group(group)[world].add(value)

	def remove(self, group, world, value):
		with contextlib.suppress(KeyError):
			self.resolve_group(group)[world].discard(value)

	def random(self, group, world, default = None):
		with contextlib.suppress(IndexError):
			return random.choice(tuple(self.resolve_group(group)[world]))
		return default
	
	def resolve_group(self, group):
		if self.switch == None:
			self.switch = {'users' : self.users, 'families' : self.families}
		return self.switch[group]


'''
Represents the current state of a user.
The state is passed to each function call, allowing server response data to be stored.
This enables the simulated user to make intelligent function calls to the server.

For example, a call to "get_all_mail" will return a list containing the mail stored on the server.
These mails can then be saved in the user state.
After, a call to "delete_mail" can look in the user state for a valid mail key to send in the request.
'''
@dataclass
class UserState:
	functions: queue.Queue = queue.Queue()
	friendlist: set = field(default_factory = set)
	familylist: set = field(default_factory = set)
	mail: list = field(default_factory = list)
	token: str = ''
	session: str = ''
	world: str = ''
	uid: str = field(default_factory = lambda: uuid.uuid4().hex)
	gn: str = ''
	fn: str = ''
	switch: dict = None

	def random(self, group, default = None):
		with contextlib.suppress(IndexError):
			return random.choice(tuple(self.resolve_group(group)))
		return default

	def resolve_group(self, group):
		if self.switch == None:
			self.switch = {'familylist' : self.familylist, 'friendlist' : self.friendlist, \
					'mail' : self.mail}
		return self.switch[group]



'''
Contains information regarding a completed request and response to the server.
'''
@dataclass
class Metric:
	name: str
	start: float
	finish: float
	request: bytes
	raw_resp: bytes
	decoded: dict = None

	@property
	def resp(self):
		if self.decoded == None:
			self.decoded = json.loads(self.raw_resp.decode().strip())
		return self.decoded


'''
Represents a simulated user.

Each user maintains a current state, which contains information such as friends, family status, and mails.
The user tries to make intelligent function calls to the server, based on information in the user state.

Metrics are pushed to the global metric queue to be consumed elsewhere.
'''
class User:
	def __init__(self, global_state, argv):
		self.argv = argv
		self.state = UserState()
		self.global_state = global_state
	
	async def run(self):
		try:
			await self.call(FunctionList.get('login_unique'))
			while self.running:
				if self.state.functions.empty():
					self.state.functions.put(FunctionList.get(self.argv.fn))
				await self.global_state.metrics.put(await self.call(self.state.functions.get()))
				await asyncio.sleep(random.random() * self.argv.delay)
		except asyncio.CancelledError:
			pass
		except Exception as e:
			print(f'User {self.state.gn} encountered exception: {e}')
		finally:
			self.global_state.remove('users', self.state.world, self.state.gn)
			self.global_state.remove('families', self.state.world, self.state.fn)
	
	async def call(self, function):
		function.before_call(self.global_state, self.state)
		metric = await self.global_state.client.send(function, self.state.token, \
				self.state.session, self.state.world)
		function.after_call(self.global_state, self.state, metric)
		return metric

	def running(self):
		return True

'''
Pickles metrics collected from the metrics queue and publishes them to the graphite server.
The graphite server is then queried from the Graphana platform to create real-time graphs.
'''
class Submitter:
	def __init__(self, args, metrics):
		self.args    = args
		self.metrics = metrics
		self.pending = []
		self.last_sent = time.time()
		self.last_band = self.last_sent
		self.bandwidth = 0
	
	async def start(self):
		try:
			reader, writer = await asyncio.open_connection(self.args.graphite_addr, self.args.graphite_port)
			while True:
				m = await self.metrics.get()
				self.pending.append((f'simulator.functions.{m.name}', (m.start, m.finish - m.start)))
				self.pending.append(('simulator.bandwidth', (m.start, len(m.request) + len(m.raw_resp))))
				self.bandwidth += len(m.request) + len(m.raw_resp)
				if self.should_send():
					await self.send(writer)
					self.pending.clear()
					self.last_sent = time.time()
		except asyncio.CancelledError:
			pass
		finally:
			if writer:
				writer.close()
				await writer.wait_closed()
	
	async def send(self, writer):
		payload = pickle.dumps(self.pending, protocol = 2)
		payload = struct.pack('!L', len(payload)) + payload
		writer.write(payload)
		await writer.drain()
	
	def should_send(self):
		t = time.time()
		if t - self.last_band > 1:
			print(f'{self.bandwidth / (t - self.last_band)} bytes / second')
			self.last_band = t
			self.bandwidth = 0
		if len(self.pending) >= 200:
			return True
		if t - self.last_sent > 5:
			return True
		return False


'''
Orchestrates the creation and running of simulated users.
Simulated users make semi-intelligent requests to the server.
All metrics collected by users are pushed into the global metric queue.
This queue is fed into the Submitter class, who's job is to collect and submit metric data to a graphite 
server.
'''
class Simulator:
	def __init__(self, argv):
		self.argv = argv

		self.users = []
		self.state = None
		self.submitter = None
	
	async def init(self):
		self.state = GlobalState(Client(self.argv.host, self.argv.port, self.argv.certpath))
		self.submitter = Submitter(self.argv, self.state.metrics)
		asyncio.create_task(self.submitter.start())

	async def start(self):
		try:
			await self.init()
			while self.running:
				self.scale_users()
				await asyncio.sleep(1)
		except Exception as e:
			print(f'Simulator encountered and error: {e}')
		finally:
			pass
	
	def scale_users(self):
		self.users = [u for u in self.users if u.done() == False]
		if len(self.users) != self.argv.n:
			print(f'{self.argv.n - len(self.users)} users failed, replacing them with new ones...')
		self.users.extend([asyncio.create_task(User(self.state, self.argv).run()) \
				for _ in range(self.argv.n - len(self.users))])
	
	@property
	def running(self):
		return True



async def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('host'           , type = str, help = 'lukseun server address')
	parser.add_argument('-d', '--delay'  , type = int, default = 5, help = 'max delay between requests')
	parser.add_argument('-n'             , type = int, default = 50, help = 'number of concurrent users')
	parser.add_argument('-fn'            , type = str, default = None, help = 'force send only this fn')
	parser.add_argument('--port'         , type = int, default = 8880, help = 'lukseun server port')
	parser.add_argument('--graphite-port', type = int, default = 2004, help = 'graphite port')
	parser.add_argument('--graphite-addr', type = str, default = '192.168.1.102', help = 'graphite address')
	parser.add_argument('--certpath'     , type = str, default = '../gate/cert/mycert.crt', \
			help = 'path to ssl cert')
	await Simulator(parser.parse_args()).start()


if __name__ == '__main__':
	asyncio.run(main())
