import os
import time
import subprocess
import signal
import requests
from socket import *
udpClient = socket(AF_INET,SOCK_DGRAM) #创建客户端
def loc():
	return os.path.dirname(os.path.realpath(__file__))
PythonVersion=""
def GetPythonCommand():
	global PythonVersion
	if PythonVersion!="":
		return PythonVersion

	try:
		version1 = os.popen("python3.7 --version")
		if version1.read()!="":
			PythonVersion="python3.7"
	except:
		pass

	try:
		version2 = os.popen("python.exe --version")
		if version2.read()!="":
			PythonVersion="python.exe"
	except:
		pass

	try:
		version3 = os.popen("python3 --version")
		if version3.read()!="":
			PythonVersion="python3"
	except:
		pass

	try:
		version4 = os.popen("python --version")
		if version4.read()!="":
			PythonVersion="python"
	except:
		pass
	# print("Version:"+version1.read())
	# print("show:"+version2.read())
	# print("show:"+version3.read())
	
	if version2.read()!="":
		PythonVersion="python"
	if version3.read()!="":
		PythonVersion="python.exe"
	if version4.read()!="":
		PythonVersion="python"
	print("Your are using python command:"+PythonVersion)
	return PythonVersion

def get_host_ip():
    try:
        s = socket(AF_INET,SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def main():
	processes = []
	try:
		processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/configuration_manager.py']))
		time.sleep(1)
		#processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/mail_server.py']))
		#processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/token_server.py']))
		#processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/account_manager.py']))
		#processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/game_manager_qin.py']))
		#processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/game_manager_houyao.py']))
		processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/worker.py',get_host_ip()]))
		processes.append(subprocess.Popen([GetPythonCommand(), loc() + '/gate.py',get_host_ip()]))
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
