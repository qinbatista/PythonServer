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
	def __init__(self, path = 'world.{world}.gamemanager.{fn}', *, host = '192.168.1.102', port = 2004, **kwargs):
		self.graphite = socket.create_connection((host, port))
		self.inqueue = queue.Queue()
		self.submitter = threading.Thread(target = self._submit, daemon = True)
		self.submitter.start()
		self.path = path
		self.kwargs = kwargs

	def collect_async(self, fn):
		async def wrapper(*args, **kwargs):
			start = timeit.default_timer()
			retval = await fn(*args, **kwargs)
			end = timeit.default_timer()
			if len(args) > 1:
				self.inqueue.put((args[1], fn.__name__.lstrip('_'), time.time(), end - start))
			else:
				self.inqueue.put((kwargs['world'], fn.__name__.lstrip('_'), time.time(), end - start))
			return retval
		return wrapper
	
	def collect(self, fn):
		def wrapper(*args, **kwargs):
			start = timeit.default_timer()
			retval = fn(*args, **kwargs)
			end = timeit.default_timer()
			if len(args) > 1:
				self.inqueue.put((args[1], fn.__name__.lstrip('_'), time.time(), end - start))
			else:
				self.inqueue.put((kwargs['world'], fn.__name__.lstrip('_'), time.time(), end - start))
			return retval
		return wrapper

	def _submit(self):
		to_send = []
		while True:
			world, fn_name, timestamp, elapsedtime = self.inqueue.get()
			to_send.append((self._path(fn = fn_name, world = world), (timestamp, elapsedtime)))
			if len(to_send) > 10:
				payload = pickle.dumps(to_send, protocol = 2)
				header = struct.pack("!L", len(payload))
				message = header + payload
				self.graphite.sendall(message)
				to_send.clear()
	
	def _path(self, **kwargs):
		return self.path.format(**self.kwargs, **kwargs)

