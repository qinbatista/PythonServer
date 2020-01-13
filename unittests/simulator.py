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
import random
import asyncio
import argparse
import threading
import contextlib
import statistics

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

from functions import FunctionList
from dataclasses import dataclass, field
from collections import defaultdict


'''
Fascilitates a method of sending timed requests to the server.
'''
class Client:
	def __init__(self, host, port, certpath):
		self.host = host
		self.port = port
		self.ending = b'\r\n'
		self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
		self.context.load_verify_locations(certpath)
		self.context.check_hostname = False

	async def send(self, function, token, world):
		try:
			reader, writer = await asyncio.open_connection(self.host, self.port, ssl = self.context)
			request = function.dump(token, world).encode() + self.ending
			writer.write(request)
			await writer.drain()
			start = time.time()
			raw_resp = await reader.readuntil(self.ending)
			finish = time.time()
			return Metric(function.name, start, finish, request, raw_resp)
		finally:
			writer.close()
			await writer.wait_closed()

'''
Represents the global state of the simulation.
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
Contains an aggregation of all the data collected through the entire run time of the simulation.
'''
@dataclass
class Statistics:
	data: defaultdict(list) = field(default_factory = lambda: defaultdict(list))
	latest: defaultdict(list) = field(default_factory = lambda: defaultdict(list))

	def add(self, metric):
		self.data[metric.name].append((metric.finish - metric.start, metric.start, metric.finish))
		self.latest[metric.name].append((metric.finish - metric.start, metric.start, metric.finish))
	
	def print(self):
		os.system('cls') if os.name == 'nt' else os.system('clear')
		title = f'{"Function":<35}|{"N":^8}|{"Min":^8}|{"Avg":^8}|{"Med":^8}|{"Max":^8}|{"Std":^8}|'
		print(f'{title}\n{"=" * len(title)}')
		for function in sorted(self.data):
			times = [t[0] for t in self.data[function]]
			num_req = len(self.data[function])
			min_req = min(times)
			avg_req = statistics.mean(times)
			med_req = statistics.median(times)
			max_req = max(times)
			std_dev = statistics.pstdev(times)
			print(f'{function:<35}|{num_req:<8}|{min_req:<8.4}|{avg_req:<8.4}|{med_req:<8.4}|{max_req:<8.4}|{std_dev:<8.4}|')
		self.latest.clear()


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
		metric = await self.global_state.client.send(function, self.state.token, self.state.world)
		function.after_call(self.global_state, self.state, metric)
		return metric

	def running(self):
		return True

class GUI(threading.Thread):
	def __init__(self, args, stats):
		threading.Thread.__init__(self)
		self.args = args
		self.stats = stats

		plt.rc('font', size = 6)
		plt.rc('axes', labelsize = 6)
		plt.rc('axes', labelsize = 6)
		plt.rc('xtick', labelsize = 6)
		plt.rc('ytick', labelsize = 6)

		self.fig = plt.figure(figsize = (10, 10), dpi = 150)
		self.histogram = self.fig.add_subplot(2, 2, 1)

		self.average = self.fig.add_subplot(2, 2, 2)
		self.average_x, self.average_y = [], []

		self.piechart = self.fig.add_subplot(2, 2, 3)

	
	def run(self):
		ani_average = ani.FuncAnimation(self.fig, self.update_average, \
				interval=self.args.refresh*1000)
		ani_piechart = ani.FuncAnimation(self.fig, self.update_piechart, \
				interval=self.args.refresh*1000)
		ani_histogram = ani.FuncAnimation(self.fig, self.update_histogram, \
				interval=self.args.refresh*1000)
		plt.show()
	
	def update_histogram(self, i):
		functions = tuple(sorted(self.stats.data, reverse = True))
		y_pos = np.arange(len(functions))
		count = [len(self.stats.data[fn]) for fn in functions]

		self.histogram.clear()
		self.histogram.set_title('Function Calls')
		self.histogram.set_xlabel('Number of Calls')
		self.histogram.barh(y_pos, count, align = 'center', alpha = 0.5)
		self.histogram.set_yticks(y_pos)
		self.histogram.set_yticklabels(functions)
	
	def update_piechart(self, i):
		functions = tuple(sorted(self.stats.data, reverse = True))
		count = [len(self.stats.data[fn]) for fn in functions]
		self.piechart.clear()
		self.piechart.axis('equal')
		self.piechart.pie(count, labels = functions, rotatelabels = True)
	
	def update_average(self, i):
		self.average.clear()
		self.average.set_title('Average Response')
		self.average.set_ylabel('Response Time (ms)')
		self.average.get_xaxis().set_visible(False)
		num, tot = 0, 0
		for times in self.stats.data.values():
			tot += sum(t[0] for t in times)
			num += len(times)
		if num != 0:
			self.average_x.append(time.time())
			self.average_y.append((tot / num) * 1000)
			self.average_x = self.average_x[-20:]
			self.average_y = self.average_y[-20:]
		self.average.plot(self.average_x, self.average_y)



class Simulator:
	def __init__(self, argv):
		self.argv = argv
		self.stats = Statistics()
		self.gui = GUI(self.argv, self.stats)

		self.users = []
		self.global_state = None

	async def start(self):
		try:
			self.gui.start()
			self.global_state = GlobalState(Client(self.argv.host, self.argv.port, self.argv.certpath))
			#users=[asyncio.create_task(User(self.global_state, self.argv).run())for _ in range(self.argv.n)]
			while self.running:
				self.scale_users()
				await asyncio.wait({self.gather_metrics()}, timeout = self.argv.refresh)
				self.stats.print()
		except Exception as e:
			print(f'Simulator encountered and error: {e}')
		finally:
			self.gui.join()
	
	async def gather_metrics(self):
		while True:
			self.stats.add(await self.global_state.metrics.get())
	
	def scale_users(self):
		self.users = [u for u in self.users if u.done() == False]
		self.users.extend([asyncio.create_task(User(self.global_state, self.argv).run()) \
				for _ in range(self.argv.n - len(self.users))])
	
	@property
	def running(self):
		return True



async def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('host', type = str)
	parser.add_argument('--port', type = int, default = 8880)
	parser.add_argument('-n', type = int, default = 50)
	parser.add_argument('-d', '--delay', type = int, default = 5)
	parser.add_argument('-r', '--refresh', type = int, default = 2)
	parser.add_argument('-v', '--verbose', action = 'store_true')
	parser.add_argument('-fn', type = str, default = None)
	parser.add_argument('--certpath', type = str, default = '../gate/cert/mycert.crt')
	await Simulator(parser.parse_args()).start()


if __name__ == '__main__':
	asyncio.run(main())
