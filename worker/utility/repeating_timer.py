# repeating_timer.py

import time
import threading

class RepeatingTimer(threading.Thread):
	def __init__(self, repeat_time, fn, *args, **kwargs):
		super().__init__(daemon = True)
		self.repeat_time = repeat_time
		self.fn = fn
		self.args = args
		self.kwargs = kwargs
	
	def run(self):
		while True:
			self.fn(*self.args, **self.kwargs)
			time.sleep(self.repeat_time)
