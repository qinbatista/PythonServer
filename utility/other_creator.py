import sys
import pymysql
import argparse
import contextlib
from world_structure import MALL, EXCHANGE


def create(addr, user, pwrd, port):
    conn = pymysql.connect(host=addr, user=user, password=pwrd, port=port, charset='utf8mb4', autocommit=True)
    # mall table
    with contextlib.suppress(pymysql.err.ProgrammingError):
        conn.cursor().execute(f'CREATE DATABASE `mall`;')
    conn.select_db('mall')
    with contextlib.suppress(pymysql.err.InternalError):
        conn.cursor().execute(MALL)
    # exchange table
    with contextlib.suppress(pymysql.err.ProgrammingError):
        conn.cursor().execute(f'CREATE DATABASE `exchange`;')
    conn.select_db('exchange')
    with contextlib.suppress(pymysql.err.InternalError):
        conn.cursor().execute(EXCHANGE)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--addr', type=str, default='192.168.1.143')
    parser.add_argument('--user', type=str, default='root')
    parser.add_argument('--pwrd', type=str, default='lukseun')
    parser.add_argument('--port', type=int, default=3306)
    args = parser.parse_args()
    create(args.addr, args.user, args.pwrd, args.port)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.argv.extend(['--addr', '192.168.1.143', '--port', '3307'])
    main()

