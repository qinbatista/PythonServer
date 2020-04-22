import os
cmd = {
	'nt': 'python',
	'posix': 'python3'
}
os.system(f'{cmd[os.name]} world_creator.py --addr rm-bp15dx5784333c2hdwo.mysql.rds.aliyuncs.com --pwrd lukseun1!')
os.system(f'{cmd[os.name]} user_creator.py --addr rm-bp15dx5784333c2hdwo.mysql.rds.aliyuncs.com --pwrd lukseun1!')
os.system(f'{cmd[os.name]} other_creator.py --addr rm-bp15dx5784333c2hdwo.mysql.rds.aliyuncs.com --pwrd lukseun1!')
# os.system(f'{cmd[os.name]} world_creator.py --addr rm-2ze8n54298l950823ro.mysql.rds.aliyuncs.com --user lukseun --pwrd lukseun1!')
# os.system(f'{cmd[os.name]} user_creator.py --addr rm-2ze8n54298l950823ro.mysql.rds.aliyuncs.com --user lukseun --pwrd lukseun1!')
# os.system(f'{cmd[os.name]} other_creator.py --addr rm-2ze8n54298l950823ro.mysql.rds.aliyuncs.com --user lukseun --pwrd lukseun1!')
