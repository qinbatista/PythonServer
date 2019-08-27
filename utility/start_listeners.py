import os
import sys
import time
import subprocess
import signal
import requests

def loc():
	return os.path.dirname(os.path.realpath(__file__))

def main(listeners):
	processes = []
	try:
		for listener in range(int(listeners)):
			processes.append(subprocess.Popen(['python', loc() + '/listener.py', str(listener)]))
			time.sleep(0.2)
		print('Done spawning listener...')
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
		print('missing required argument: number of listeners')
	else:
		main(sys.argv[1])
