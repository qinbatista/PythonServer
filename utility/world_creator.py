'''
world_creator.py
'''

import os
import json
import mailbox
import pymysql
import argparse

# imporant the create statements for each table
# statement names are imported to the local namespace, so be careful with name collisions
from world_structure import *  

TABLES = [PLAYER, SUMMON, ACHIEVEMENT, ARMOR, CHECKIN, DARKMARKET,
		FACTORY, FAMILY, FAMILYHISTORY, FAMILYROLE, FRIEND, ITEM, LEADERBOARD, LIMITS,
		PROGRESS, ROLE, ROLEPASSIVE, SKILL, TASK, TIMER, WEAPON, WEAPONPASSIVE,
		CONSTRAINT, TRIGGER1, TRIGGER2]



#########################################################################################

def database_exists(db, mysql_addr, mysql_user, mysql_pw):
	try:
		pymysql.connect(host = mysql_addr, user = mysql_user, password = mysql_pw,
				charset = 'utf8mb4', db = db)
	except pymysql.err.InternalError as e:
		if e.args[0] == 1049: return False
	return True

def create_db(world, mysql_addr, mysql_user, mysql_pw):
	if not database_exists(world, mysql_addr, mysql_user, mysql_pw):
		connection = pymysql.connect(host = mysql_addr, user = mysql_user,
				password = mysql_pw, charset = 'utf8mb4', autocommit = True)
		connection.cursor().execute(f'CREATE DATABASE `{world}`;')
		connection.select_db(world)
		# connection.cursor().execute(MALL)
		for table in TABLES:
			connection.cursor().execute(table)
		print(f'created new database for world {world}..')
	else:
		print(f'database for world {world} already exists, skipping..')
		connection = pymysql.connect(host = mysql_addr, user = mysql_user,
				password = mysql_pw, charset = 'utf8mb4', autocommit = True)
		connection.select_db(world)
		for table in TABLES:
			try:
				connection.cursor().execute(table)
			except:
				print("error")
		print(f'created new database for world {world}..')


def create_mailbox(world):
	path = os.path.dirname(os.path.realpath(__file__)) + '/../box'
	box  = mailbox.Maildir(path)
	try:
		worldbox = box.get_folder(str(world))
		print(f'mailbox for world {world} already exists, skipping..')
	except mailbox.NoSuchMailboxError:
		box.add_folder(str(world))
		print(f'added mailbox for world {world}..')

def create_world(world, mysql_addr, mysql_user, mysql_pw):
	create_db(world, mysql_addr, mysql_user, mysql_pw)
	create_mailbox(world)
	# TODO update path / make this compatible with aliyun mounted NAS


def loc():
	return os.path.dirname(os.path.realpath(__file__))


def save_world_config(world, path):
	data = json.load(open(path, encoding='utf-8'))
	data['worlds'].append({
		"status" : 0,
		"id"     : world,
		"name"   : f"world {world}"
	})
	with open(path, 'w', encoding='utf-8') as f:
		f.write(json.dumps(data))



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--addr', type = str, default = '192.168.1.102')
	parser.add_argument('--pwrd', type = str, default = 'lukseun')
	parser.add_argument('--user', type = str, default = 'root')
	args = parser.parse_args()

	path = os.path.join(loc(), '../config/configuration/1.0/server/world.json')
	for i in range(0, 10):
		world = f's{i}'
		create_world(world, args.addr, args.user, args.pwrd)
		save_world_config(world, path)


def test(world, mysql_addr, mysql_user, mysql_pw):
	connection = pymysql.connect(host=mysql_addr, user=mysql_user, password=mysql_pw, charset='utf8mb4', autocommit=True)
	connection.cursor().execute(f'CREATE DATABASE `{world}`;')
	connection.select_db(world)

	for table in TABLES:
		connection.cursor().execute(table)
	"""
	cursor = connection.cursor()
	cursor.execute(f"SELECT * FROM player;")
	data = cursor.fetchall()
	for d in data:
		if d[2] is None:
			print(f'{d} is None')
		else:
			print(f'{d}')
	"""


if __name__ == '__main__':
	main()
	# test("s6", "192.168.1.102", "root", "lukseun")
