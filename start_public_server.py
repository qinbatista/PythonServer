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

	try:
		version1 = os.popen("python3.7 --version")
		if version1.read()!="":
			PythonVersion="python3.7"
			print("Your are using python command:"+PythonVersion)
			return PythonVersion
	except Exception as e:
		print(str(e))

	try:
		version2 = os.popen("python.exe --version")
		if version2.read()!="":
			PythonVersion="python.exe"
			print("Your are using python command:"+PythonVersion)
			return PythonVersion
	except Exception as e:
		print(str(e))

	try:
		version3 = os.popen("python3 --version")
		if version3.read()!="":
			PythonVersion="python3"
			print("Your are using python command:"+PythonVersion)
			return PythonVersion
	except Exception as e:
		print(str(e))

	try:
		version4 = os.popen("python --version")
		if version4.read()!="":
			PythonVersion="python"
			print("Your are using python command:"+PythonVersion)
			return PythonVersion
	except Exception as e:
		print(str(e))
	# print("Version:"+version1.read())
	# print("show:"+version2.read())
	# print("show:"+version3.read())


def main():
	processes = []
	try:
		processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/config/configuration_manager.py']))
		time.sleep(1)
		processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/mail_server.py']))
		processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/token_server.py']))
		processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/edge/edge.py', \
				'--redis-addr', 'redis://192.168.1.102', '--nats-addr', 'nats://192.168.1.102']))
		processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/worker/worker.py', \
				'--channel', get_host_ip(), '--redis-addr', 'redis://192.168.1.102', \
				'--nats-addr', 'nats://192.168.1.102', '--token-addr', 'http://localhost', \
				'--mail-addr', 'http://localhost']))
		processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/gate/gate.py', \
				'--channel' , get_host_ip(), '--redis-addr', 'redis://192.168.1.102', \
				'--nats-addr', 'nats://192.168.1.102', '--testing']))
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
