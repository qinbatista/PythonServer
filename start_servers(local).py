import os
import time
import subprocess
import signal
import requests
from socket import *
udpClient = socket(AF_INET,SOCK_DGRAM) #创建客户端
def loc():
	return os.path.dirname(os.path.realpath(__file__))

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
		processes.append(subprocess.Popen(['python', loc() + '/configuration_manager.py']))
		time.sleep(1)
		#processes.append(subprocess.Popen(['python', loc() + '/mail_server.py']))
		#processes.append(subprocess.Popen(['python', loc() + '/token_server.py']))
#		processes.append(subprocess.Popen(['python', loc() + '/account_manager.py']))
		#processes.append(subprocess.Popen(['python', loc() + '/game_manager_qin.py']))
		# processes.append(subprocess.Popen(['python3', loc() + '/game_manager_houyao.py']))


		processes.append(subprocess.Popen(['python', loc() + '/worker.py',get_host_ip()]))
		processes.append(subprocess.Popen(['python', loc() + '/gate.py',get_host_ip()]))
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
