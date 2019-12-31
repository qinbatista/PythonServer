import os
cmd = {
	'nt': 'python',
	'posix': 'python3'
}
os.system(f'{cmd[os.name]} world_creator.py --addr rm-bp15dx5784333c2hdwo.mysql.rds.aliyuncs.com --pwrd lukseun1!')
os.system(f'{cmd[os.name]} user_creator.py --addr rm-bp15dx5784333c2hdwo.mysql.rds.aliyuncs.com --pwrd lukseun1!')
