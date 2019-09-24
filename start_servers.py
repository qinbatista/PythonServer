import os
import time
import subprocess
import signal
import requests

def loc():
	return os.path.dirname(os.path.realpath(__file__))



def main():
	processes = []
	try:
		processes.append(subprocess.Popen(['python3', loc() + '/configuration_manager.py']))
		time.sleep(1)
		#processes.append(subprocess.Popen(['python', loc() + '/mail_server.py']))
		#processes.append(subprocess.Popen(['python', loc() + '/token_server.py']))
#		processes.append(subprocess.Popen(['python', loc() + '/account_manager.py']))
		#processes.append(subprocess.Popen(['python', loc() + '/game_manager_qin.py']))
		# processes.append(subprocess.Popen(['python3', loc() + '/game_manager_houyao.py']))


		processes.append(subprocess.Popen(['python3', loc() + '/worker.py']))
		processes.append(subprocess.Popen(['python3', loc() + '/gate.py']))
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
