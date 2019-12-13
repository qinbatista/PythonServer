import os
import time
import subprocess
import signal
import requests
from socket import *
PythonVersion=""
def loc():
	return os.path.dirname(os.path.realpath(__file__))

def get_host_ip():
	try:
		s = socket(AF_INET, SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		ip = s.getsockname()[0]
	finally:
		s.close()
	return ip

def GetPythonCommand():
	global PythonVersion
	if PythonVersion!="":
		return PythonVersion
	for cmd in ['python3.7', 'python.exe', 'python3']:
		try:
			version = os.popen(f'{cmd} --version')
			if version.read() != '':
				PythonVersion = cmd
				print(f'You are using python command: {cmd}')
				return PythonVersion
		except Exception as e:
			print(e)

def main():
	processes = []
	try:
		processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/config/configuration_manager.py']))
		time.sleep(1)
		processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/mail/mail.py', \
				loc() + '/mail/box']))
		processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/auth/auth.py', \
				'lukseunsecret', '--redis-addr', '192.168.1.102']))
		processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/edge/edge.py', \
				'--redis-addr', '192.168.1.102', '--nats-addr', '192.168.1.102']))
		processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/worker/worker.py', \
				'--channel', get_host_ip(), '--redis-addr', '192.168.1.102', \
				'--nats-addr', '192.168.1.102', '--token-addr', 'localhost', \
				'--mail-addr', 'localhost']))
		processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/gate/gate.py', \
				'--channel' , get_host_ip(), '--redis-addr', '192.168.1.102', \
				'--nats-addr', '192.168.1.102']))
		time.sleep(0.2)
		print('Done spawning servers...')
		while (len(processes) > 0):
			time.sleep(5)
	except KeyboardInterrupt:
		pass
	finally:
		for process in processes:
			process.send_signal(signal.SIGINT)
			process.wait()





if __name__ == '__main__':
	main()
