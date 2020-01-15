'''
user_creator.py
'''

import pymysql
import argparse


def create_table_info(cursor):
	statement = \
	"""
	CREATE TABLE `info` (
	  `unique_id` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `cuid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '提供客户端的uid',
	  `token` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '玩家游戏token',
	  `password` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '玩家加密后的密码',
	  `account` varchar(24) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '玩家账号',
	  `email` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '绑定的邮箱',
	  `phone_number` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '绑定的手机号',
	  `salt` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
	  `birth` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '玩家的生日',
	  `sex` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '玩家的性别',
	  PRIMARY KEY (`unique_id`),
	  UNIQUE KEY `c_uid` (`cuid`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
	"""
	cursor.execute(statement)

def create_user(mysql_addr, mysql_user, mysql_pw):
	c = pymysql.connect(host = mysql_addr, user = mysql_user, password = mysql_pw, \
			charset = 'utf8mb4', autocommit=True)
	cursor = c.cursor()
	cursor.execute(f'CREATE DATABASE `user`;')
	c.select_db('user')
	cursor = c.cursor()
	create_table_info(cursor)

def already_exists(mysql_addr, mysql_user, mysql_pw):
	try:
		pymysql.connect(host = mysql_addr, user = mysql_user, password = mysql_pw, \
				charset = 'utf8mb4', db = 'user')
	except pymysql.err.InternalError as e:
		code, msg = e.args
		if code == 1049: return False
	return True

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--addr', type = str, default = '192.168.1.102')
	parser.add_argument('--pwrd', type = str, default = 'lukseun')
	parser.add_argument('--user', type = str, default = 'root')
	args = parser.parse_args()

	if not already_exists(args.addr, args.user, args.pwrd):
		create_user(args.addr, args.user, args.pwrd)
	else:
		print('User table already exists')


if __name__ == '__main__':
	main()
