'''
world_creator.py
'''

import os
import sys
import json
import mailbox
import pymysql
import argparse
import contextlib

# imporant the create statements for each table
# statement names are imported to the local namespace, so be careful with name collisions
from world_structure import *

TABLES = [PLAYER, SCIENCES, ELEMENTS, STAGES, SUMMON, ACHIEVEMENT, ARMOR, CHECKIN,
          DARKMARKET, FACTORY, FAMILY, FAMILYHISTORY, FAMILYROLE, FRIEND,
          ITEM, LEADERBOARD, LIMITS, PROGRESS, ROLE, ROLEPASSIVE, SKILL,
          TASK, TIMER, WEAPON, WEAPONPASSIVE, CONSTRAINT, TRIGGER1, TRIGGER2]


#########################################################################################

def get_conn(mysql_addr, mysql_user, mysql_pw, port):
    return pymysql.connect(host=mysql_addr, user=mysql_user, password=mysql_pw,
                           charset='utf8mb4', port=port, autocommit=True)


def create_db(world, mysql_addr, mysql_user, mysql_pw, port):
    conn = get_conn(mysql_addr, mysql_user, mysql_pw, port)
    with contextlib.suppress(pymysql.err.ProgrammingError):
        conn.cursor().execute(f'CREATE DATABASE `{world}`;')
    conn.select_db(world)
    cursor = conn.cursor()
    for table in TABLES:
        with contextlib.suppress(pymysql.err.InternalError):
            cursor.execute(table)
    print(f'created new database for world {world}..')


def create_mailbox(world):
    path = os.path.dirname(os.path.realpath(__file__)) + '/../box'
    box = mailbox.Maildir(path)
    try:
        world_box = box.get_folder(str(world))
        print(f'mailbox for world {world} already exists, skipping..')
    except mailbox.NoSuchMailboxError:
        box.add_folder(str(world))
        print(f'added mailbox for world {world}..')


def create_world(world, mysql_addr, mysql_user, mysql_pw, port):
    create_db(world, mysql_addr, mysql_user, mysql_pw, port)
    create_mailbox(world)


# H update path / make this compatible with aliyun mounted NAS


def loc():
    return os.path.dirname(os.path.realpath(__file__))


def save_world_config(world, path):
    data = json.load(open(path, encoding='utf-8'))
    data['worlds'].append({
        "status": 0,
        "id": world,
        "name": f"world {world}",
        "merge": world
    })
    worlds = []
    for wd in data['worlds']:
        if wd not in worlds:
            worlds.append(wd)
    data['worlds'] = worlds
    with open(path, 'w', encoding='utf-8') as w:
        json.dump(data, w, ensure_ascii=False, indent=4)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--addr', type=str, default='192.168.1.143')
    parser.add_argument('--pwrd', type=str, default='lukseun')
    parser.add_argument('--user', type=str, default='root')
    parser.add_argument('--port', type=int, default=3306)
    args = parser.parse_args()

    path = os.path.join(loc(), '../config/configuration/1.0/server/world.json')
    for i in range(0, 10):
        world = f's{i}'
        create_world(world, args.addr, args.user, args.pwrd, args.port)
        save_world_config(world, path)


def test(world, mysql_addr, mysql_user, mysql_pw, port=3307):
    conn = get_conn(mysql_addr, mysql_user, mysql_pw, port)
    conn.cursor().execute(f'CREATE DATABASE `{world}`;')
    conn.select_db(world)
    for table in TABLES:
        conn.cursor().execute(table)
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
    if len(sys.argv) == 1:
        sys.argv.extend(['--addr', '192.168.1.143', '--port', '3307'])
    main()
    # test("s6", "192.168.1.143", "root", "lukseun")
