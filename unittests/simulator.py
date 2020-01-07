'''
simulator.py
'''
import os
import ssl
import time
import json
import uuid
import random
import string
import asyncio
import argparse
import statistics
import collections

import functions

class WorldList:
	@staticmethod
	def get_random():
		#		return random.choice(['s0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9'])
		return random.choice(['s0'])

class Client:
	LINE_ENDING = b'\r\n'
	def __init__(self, ip, certpath = os.path.dirname(os.path.realpath(__file__)) \
			+ '/../gate/cert/mycert.crt'): 
		self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
		self.context.load_verify_locations(certpath)
		self.context.check_hostname = False
		self.server_ip = ip
		self.server_port = 8880
	
	async def send(self, msg):
		r, w = await asyncio.open_connection(self.server_ip, self.server_port, ssl = self.context)

		w.write(msg.encode() + Client.LINE_ENDING)
		await w.drain()

		start = time.time()
		raw = await r.readuntil(Client.LINE_ENDING)
		finish = time.time()

		w.close()
		await w.wait_closed()
		return (start, finish, raw)


class User:
	def __init__(self, uid, queue, client, gamenames, familynames, maxdelay = 1, fn = None):
		self.fn       = fn
		self.uid      = uid
		self.queue    = queue
		self.client   = client
		self.maxdelay = maxdelay

		self.state    = {'token' : None, 'world' : None, 'gn' : '', 'fn' : '', 'gamenames' : gamenames, \
				'familynames' : familynames, 'uid' : self.uid, 'friendlist' : set(), 'mail' : []}
	
	async def run(self):
		try:
			await self.login()
			await self.join(WorldList.get_random())
			while True:
				stats = await self.call(self.fn)
				await self.queue.put(stats)
				if random.random() > 0.99:
					await self.join(WorldList.get_random())
				await asyncio.sleep(self.maxdelay * random.random())
		except Exception as e:
			print(e)
		finally:
			self.state['gamenames'][self.state['world']].discard(self.state['gn'])
			self.state['familynames'][self.state['world']].discard(self.state['fn'])

	async def login(self):
		_, _, raw = await self.call('login_unique')
		self.state['token'] = (json.loads(raw.decode().strip()))['data']['token']

	async def join(self, world):
		if self.state['world'] == world:
			return world
		self.state['gamenames'][self.state['world']].discard(self.state['gn'])
		self.state['familynames'][self.state['world']].discard(self.state['fn'])
		self.state['world'] = world
		_, _, raw = await self.call('enter_world')
		if (json.loads(raw.decode().strip()))['status'] != 0:
			_, _, raw = await self.call('create_player')
			if (json.loads(raw.decode().strip()))['status'] != 0:
				raise Exception('GN already taken')
		_, _, _ = await self.call('get_info_player')
		return world

	async def call(self, fn = None):
		f = (functions.FunctionList.get(fn))()
		f.before_call(self.state)
		stats = await self.client.send(f.dump(self.state['token'], self.state['world']))
		f.after_call(self.state, stats[2])
		return stats

	@staticmethod
	def random_name():
		return 'sim_' + ''.join(random.choice(string.digits) for i in range(15))

class Simulator:
	def __init__(self, server_ip, target_users, maxdelay, refresh):
		self.users = set()
		self.queue = asyncio.Queue()
		self.gamenames = collections.defaultdict(set)
		self.familynames = collections.defaultdict(set)

		self.refresh = refresh
		self.maxdelay = maxdelay
		self.server_ip = server_ip
		self.target_users = target_users
	
	async def start(self):
		try:
			simulation = asyncio.create_task(self.simulate())
			times = []
			while self.target_users < 500:
				times.clear()
				await asyncio.wait({self.collect_stats(times)}, timeout = self.refresh)
				self.analyze(self.refresh, times)
		except Exception as e:
			print(e)
		finally:
			pass
	
	async def collect_stats(self, times):
		try:
			while True:
				stats = await self.queue.get()
				times.append(stats[1] - stats[0])
		except asyncio.CancelledError:
			pass
	
	async def simulate(self):
		pending = set()
		while True:
			if len(self.users) > 0:
				_, pending = await asyncio.wait(self.users, timeout = 0.5)
			self.users     = self.update_users(pending)
	
	def analyze(self, interval, times):
		print('Summary     Time Unit: seconds')
		print('==============================')
		print(f'Number of Requests   : {len(times)}')
		print(f'Requests per Second  : {int(len(times) / interval)}')
		print(f'Minimum              : {min(times):.4}')
		print(f'Average              : {statistics.mean(times):.4}')
		print(f'Median               : {statistics.median(times):.4}')
		print(f'Maximum              : {max(times):.4}')
		print(f'Standard Deviation   : {statistics.pstdev(times):.4}', end = '\n\n\n')
	
	def target(self, n):
		self.target_users = n
	
	def update_users(self, pending):
		if len(pending) < self.target_users:
			print(f'Scaling up to {self.target_users} users...')
			for _ in range(self.target_users - len(pending)):
				pending.add(User(uuid.uuid4().hex, self.queue, Client(self.server_ip), \
						self.gamenames, self.familynames, maxdelay = self.maxdelay).run())
		elif len(pending) > self.target_users:
			print(f'Scaling down to {self.target_users} users...')
			for _ in range(len(pending) - self.target_users):
				pending.pop().cancel()
		return pending



async def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('host',            type = str)
	parser.add_argument('-fn',             type = str, default = None)
	parser.add_argument('-n',              type = int, default = 50)
	parser.add_argument('-d', '--delay',   type = int, default = 10)
	parser.add_argument('-r', '--refresh', type = int, default = 5)
	args = parser.parse_args()
	simulator = Simulator(args.host, args.n, args.delay, args.refresh)
	await simulator.start()


if __name__ == '__main__':
	asyncio.run(main())
