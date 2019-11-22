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

	try:
		version1 = os.popen("python3.7 --version")
		if version1.read() != "":
			PythonVersion = "python3.7"
			print("Your are using python command:" + PythonVersion)
			return PythonVersion
	except Exception as e:
		print(str(e))

	try:
		version2 = os.popen("python.exe --version")
		if version2.read() != "":
			PythonVersion = "python.exe"
			print("Your are using python command:" + PythonVersion)
			return PythonVersion
	except Exception as e:
		print(str(e))

	try:
		version3 = os.popen("python3 --version")
		if version3.read() != "":
			PythonVersion = "python3"
			print("Your are using python command:" + PythonVersion)
			return PythonVersion
	except Exception as e:
		print(str(e))

	try:
		version4 = os.popen("python --version")
		if version4.read() != "":
			PythonVersion = "python"
			print("Your are using python command:" + PythonVersion)
			return PythonVersion
	except Exception as e:
		print(str(e))

	print("Version1:" + version1.read())
	print("Version2:" + version2.read())
	print("Version3:" + version3.read())
	print("Version3:" + version4.read())


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
		processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/worker/worker.py', get_host_ip()], shell=False))
		processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/gate/gate.py', get_host_ip()], shell=False))
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
