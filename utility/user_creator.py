# world_creator.py

import pymysql


def create_table_info(cursor):
	statement = \
	"""
	CREATE TABLE `info` (
	  `unique_id` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `token` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
	  `password` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
	  `account` varchar(24) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
	  `email` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
	  `phone_number` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
	  `salt` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
	  PRIMARY KEY (`unique_id`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
	"""
	cursor.execute(statement)



def create_user():
	c = pymysql.connect(host = '192.168.1.102', user = 'root', password = 'lukseun', charset = 'utf8mb4', autocommit=True)
	cursor = c.cursor()
	cursor.execute(f'CREATE DATABASE `user`;')
	c.select_db('user')
	cursor = c.cursor()
	create_table_info(cursor)

def already_exists():
	try:
		pymysql.connect(host = '192.168.1.102', user = 'root', password = 'lukseun', charset = 'utf8mb4', db = 'user')
	except pymysql.err.InternalError as e:
		code, msg = e.args
		if code == 1049: return False
	return True

if __name__ == '__main__':
	if not already_exists():
		create_user()
	else:
		print('User table already exists')
