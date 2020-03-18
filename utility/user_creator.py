'''
user_creator.py
'''

import pymysql
import argparse
import sys
import contextlib


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


def create_user(mysql_addr, mysql_user, mysql_pw, port):
    c = pymysql.connect(host=mysql_addr, user=mysql_user, password=mysql_pw,
                        port=port,
                        charset='utf8mb4', autocommit=True)
    cursor = c.cursor()
    with contextlib.suppress(pymysql.err.ProgrammingError):
        cursor.execute(f'CREATE DATABASE `user`;')
    c.select_db('user')
    cursor = c.cursor()
    with contextlib.suppress(pymysql.err.InternalError):
        create_table_info(cursor)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--addr', type=str, default='192.168.1.143')
    parser.add_argument('--pwrd', type=str, default='lukseun')
    parser.add_argument('--user', type=str, default='root')
    parser.add_argument('--port', type=int, default=3306)
    args = parser.parse_args()
    create_user(args.addr, args.user, args.pwrd, args.port)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.argv.extend(['--addr', '192.168.1.143', '--port', '3307'])
    main()
