# metrics.py
#
#

import time
import queue
import pickle
import socket
import struct
import timeit
import threading

class Collector:
	send_buffer = 1
	def __init__(self, *, path = 'world.{world}.function.{fn}', \
			host = '192.168.1.165', port = 2004):
		self.host      = host
		self.path      = path
		self.port      = port
		self.inqueue   = queue.Queue()
		self.graphite  = socket.create_connection((host, port))
		self.submitter = threading.Thread(target = self.submit, daemon = True)
		self.submitter.start()

	def collect_async(self, fn):
		async def wrapper(*args, **kwargs):
			start = timeit.default_timer()
			retval = await fn(*args, **kwargs)
			end = timeit.default_timer()
			self.inqueue.put((args[1].get('world', 'None'), args[1]['function'], time.time(), end - start))
			return retval
		return wrapper
	
	def submit(self):
		unsent = []
		with socket.create_connection((self.host, self.port)) as conn:
			while True:
				world, fn, timestamp, elapsed = self.inqueue.get()
				unsent.append((self.path.format(world = world, fn = fn), (timestamp, elapsed)))
				if len(unsent) > Collector.send_buffer:
					payload = pickle.dumps(unsent, protocol = 2)
					conn.sendall(struct.pack('!L', len(payload)) + payload)
					unsent.clear()
