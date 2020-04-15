import os
import subprocess
import argparse
#import start_servers as s
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

images = ['auth', 'config', 'edge', 'gate', 'mail', 'worker']
# images = ['config']


def login(username='qinbatista', password='lukseun1'):
	# subprocess.Popen(['docker', f'login --username={username} registry.cn-hangzhou.aliyuncs.com'])
	os.system(f'docker login --username={username} registry.cn-hangzhou.aliyuncs.com')


def docker(path):
	for image in images:
		#subprocess.Popen(['docker', 'build', '-t', f'{path}/{image}:latest', '-f', f'{s.loc()}/{image}/Dockerfile', f'{s.loc()}/{image}'])
		#subprocess.Popen(['docker', 'push',     f'{path}/{image}:latest'])
		print(f'starting build of {image}...')
		os.system(f'docker build -t {path}/{image}:latest -f {PATH}/{image}/Dockerfile {PATH}/{image}')
		print(f'build of image {image} done.')
		print(f'starting push of {image} to remote...')
		os.system(f'docker push {path}/{image}:latest')
		print(f'push of image {image} done.')


def k8s():
	for image in images:
		#subprocess.Popen(['kubectl', 'rollout', 'restart', 'deployment', image])
		os.system(f'kubectl rollout restart deployment {image}')


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', type=str)
	parser.add_argument('-p', type=str)
	args = parser.parse_args()
	# login(args.u, args.p)
	# docker('registry.cn-beijing.aliyuncs.com/lukseun')
	docker('registry.cn-hangzhou.aliyuncs.com/lukseun')
	k8s()


if __name__ == '__main__':
	main()
