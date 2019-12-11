import subprocess
import argparse
import start_servers as s


images = []


def login(username, password):
	subprocess.Popen(['docker', f'login --username=hou@1442248065720316 registry.cn-hangzhou.aliyuncs.com'])
	subprocess.Popen([s.GetPythonCommand(), s.loc() + '/config/configuration_manager.py'])


def docker():
	subprocess.Popen([s.GetPythonCommand(), s.loc() + '/config/configuration_manager.py'])


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', type=str)
	parser.add_argument('-p', type=str)
	args = parser.parse_args()
	login(args.u, args.p)


if __name__ == '__main__':
	main()
