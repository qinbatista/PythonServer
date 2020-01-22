'''
world_merge.py

READ EVERYTHING BEFORE USING

A basic tool to help with merging worlds.
Migrates all players in the source world into the destination world.

There are some important things to know about this process:

First, the target world must not be a normal world that players can connect to directly.
It should have a private name, known only to us.
Additionally, the tables cannot have any triggers associated with it when performing the merge.
This is to ensure there is no duplicate data created, and ensure Key Constraints are not wrongly broken.
Remember, this world should not be listed to the client. And as such, new accounts can not be created in
this world directly.

This process is mildley destructive on the source world. Unique IDs, game names, and family names are all
modified by appending an '_' (underscore) character followed by the world name.
Running the world_merge tool on the same source world consecutively will result in unreachable player
entries to be inserted into the target world.

Any constraint errors that are encountered in the merge will not be handled gracefully.
It is both possible and highly likely that a constraint error will leave the target world in an
incomplete state, containing only a subset of players from the source world. Restoring from this
scenario would be incredibly difficult, as there is no easy way to check which players got successfully
merged.

As such, the most important rule is: MAKE BACKUPS BEFORE USE.
'''
import os
import pymysql
import argparse

# import the create statements for each table
# statement names are imported directly to the local namespace, so be careful with name collisions
from world_structure import *


def create_connection(addr, user, pw, db = None):
	c = pymysql.connect(host = addr, user = user, password = pw, charset = 'utf8mb4', autocommit = True)
	if db: c.select_db(db)
	return c

def database_exists(db, addr, user, pw):
	try:
		create_connection(addr, user, pw, db = db)
	except pymysql.err.InternalError as e:
		if e.args[0] == 1049:
			return False
	return True

def create_target(name, addr, user, pw):
	conn = create_connection(addr, user, pw)
	conn.cursor().execute(f'CREATE DATABASE `{name}`;')
	conn.select_db(name)
	for table in TABLES:
		conn.cursor().execute(table)

def enable_triggers(name, addr, user, pw):
	conn = create_connection(addr, user, pw, db = name)
	for trigger in TRIGGERS:
		conn.cursor().execute(trigger)

def disable_triggers(name, addr, user, pw):
	conn = create_connection(addr, user, pw, db = name)
	cursor = conn.cursor()
	cursor.execute('SHOW TRIGGERS;')
	data = cursor.fetchall()
	for trigger in data:
		cursor.execute(f'DROP TRIGGER {trigger[0]};')

def translate(src, addr, user, pw):
	conn = create_connection(addr, user, pw, db = src)
	cursor = conn.cursor()

	# translate uids and gamenames
	cursor.execute('SELECT `uid`, `gn` FROM `player`;')
	data = cursor.fetchall()
	for player in data:
		cursor.execute(f'UPDATE `player` SET `uid` = "{player[0]}_{src}", `gn` = "{player[1]}_{src}" \
				WHERE `uid` = "{player[0]}";')
	
	# translate family names
	cursor.execute('SELECT `name` FROM `family`;')
	data = cursor.fetchall()
	for family in data:
		cursor.execute(f'UPDATE `family` SET `name` = "{family[0]}_{src}" WHERE `name` = "{family[0]}";')

def dump_db(filename, db, addr, user, pw):
	os.system(f'mysqldump -h {addr} -u {user} -p{pw} --no-create-info --skip-triggers \
			--single-transaction {db} > {filename}')

def import_db(filename, db, addr, user, pw):
	os.system(f'mysql -h {addr} -u {user} -p{pw} {db} < {filename}')

def merge(args):
	if not database_exists(args.dest, args.addr, args.user, args.pwrd):
		create_target(args.dest, args.addr, args.user, args.pwrd)
	translate(args.src, args.addr, args.user, args.pwrd)
	dump_db('translated.sql', args.src, args.addr, args.user, args.pwrd)
	disable_triggers(args.dest, args.addr, args.user, args.pwrd)
	import_db('translated.sql', args.dest, args.addr, args.user, args.pwrd)
	enable_triggers(args.dest, args.addr, args.user, args.pwrd)

def yes_or_no(question, default = 'yes'):
	valid = {'y' : True, 'ye' : True, 'yes' : True,
			'n' : False, 'no' : False}
	if default is None:
		prompt = ' [y/n] '
	elif default == 'yes':
		prompt = ' [Y/n] '
	elif default == 'no':
		prompt = ' [y/N] '
	
	while True:
		choice = input(f'{question}{prompt}').lower()
		if default is not None and choice == '':
			return valid[default]
		elif choice in valid:
			return valid[choice]
		else:
			print('Invalid input')

def show_prompt():
	return (yes_or_no('Did you read the documentation?', default = 'no') and \
		yes_or_no('Did you make a database backup?', default = 'no'))

def main(args):
	if show_prompt():
		merge(args)
		print(f'Merge complete. Be sure to add "merge" : "{args.dest}" to world {args.src} in world.json.')
	print('Exiting.')



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('src'   , type = str, help = 'name of the source database')
	parser.add_argument('dest'  , type = str, help = 'name of the destination database')
	parser.add_argument('--addr', type = str, default = '192.168.1.102', help = 'database address')
	parser.add_argument('--pwrd', type = str, default = 'lukseun'      , help = 'database password')
	parser.add_argument('--user', type = str, default = 'root'         , help = 'database user')
	main(parser.parse_args())
