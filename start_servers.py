import os
import time
import subprocess

def loc():
	return os.path.dirname(os.path.realpath(__file__))



def main():
	processes = []
	try:
		processes.append(subprocess.Popen(['python', loc() + '/configuration_manager.py']))
		time.sleep(1)
		processes.append(subprocess.Popen(['python', loc() + '/chat_server.py']))
		processes.append(subprocess.Popen(['python', loc() + '/mail_server.py']))
		processes.append(subprocess.Popen(['python', loc() + '/token_server.py']))
		processes.append(subprocess.Popen(['python', loc() + '/account_manager.py']))
		processes.append(subprocess.Popen(['python', loc() + '/game_manager.py']))
		processes.append(subprocess.Popen(['python', loc() + '/game_manager_qin.py']))
		processes.append(subprocess.Popen(['python', loc() + '/game_manager_houyao.py']))
		processes.append(subprocess.Popen(['python', loc() + '/lukseun_server.py']))
		while (len(processes) > 0):
			time.sleep(5)
	except KeyboardInterrupt:
		pass
	finally:
		for process in processes:
			subprocess.Popen.terminate(process)





if __name__ == '__main__':
	main()
