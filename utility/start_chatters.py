import os
import sys
import time
import subprocess
import signal
import requests

def loc():
	return os.path.dirname(os.path.realpath(__file__))

def main(chatters):
	processes = []
	try:
		for chatter in range(int(chatters)):
			processes.append(subprocess.Popen(['python', loc() + '/chatter.py', str(chatter)]))
			time.sleep(0.5)
		print('Done spawning chatters...')
		while (len(processes) > 0):
			time.sleep(5)
	except KeyboardInterrupt:
		pass
	finally:
		for process in processes:
			process.send_signal(signal.SIGINT)
			process.wait()

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('missing required argument: number of chatters')
	else:
		main(sys.argv[1])
