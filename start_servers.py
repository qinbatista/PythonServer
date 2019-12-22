import os
import time
import subprocess
import signal
import requests
from socket import *

udpClient = socket(AF_INET, SOCK_DGRAM)  # 创建客户端


def loc():
	return os.path.dirname(os.path.realpath(__file__))


PythonVersion = ""


def GetPythonCommand():
	global PythonVersion
	if PythonVersion != "":
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


def get_host_ip():
	try:
		s = socket(AF_INET, SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		ip = s.getsockname()[0]
	finally:
		s.close()
	return ip


def main():
	processes = []
	try:
		processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/config/configuration_manager.py'], shell=False))
		time.sleep(1)
		processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/worker/worker.py', \
				'--channel', get_host_ip(), '--redis-addr', '192.168.1.102', \
				'--nats-addr', '192.168.1.102', '--token-addr', '192.168.1.165', \
				'--mail-addr', '192.168.1.165'], shell=False))
		processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/gate/gate.py', \
				'--channel', get_host_ip(), '--redis-addr', '192.168.1.102', \
				'--nats-addr', '192.168.1.102', '--debug'], shell=False))
		time.sleep(0.2)
		print('Done spawning servers...')
		while len(processes) > 0:
			time.sleep(5)
	except KeyboardInterrupt:
		pass
	finally:
		for process in processes:
			process.send_signal(signal.SIGINT)
			process.wait()


if __name__ == '__main__':
	main()
