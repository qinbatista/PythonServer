'''
world_creator.py
'''

import pymysql


ACHIEVEMENT = \
"""
CREATE TABLE `achievement` (
	 `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户唯一id',
	 `aid` int(11) NOT NULL COMMENT '成就唯一id',
	 `value` int(11) DEFAULT 0 COMMENT '成就完成的次数',
	 `reward` int(11) DEFAULT 0 COMMENT '完成成就领奖的次数',
	 PRIMARY KEY (`uid`,`aid`),
	 CONSTRAINT `achievement_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

ARMOR = \
"""
CREATE TABLE `armor` (
	  `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户唯一id',
	  `aid` int(11) NOT NULL COMMENT '盔甲唯一id标识1-40种盔甲',
	  `level` int(11) NOT NULL COMMENT '盔甲等级唯一id标识1-10级',
	  `quantity` int(11) DEFAULT 0 COMMENT '完成成就领奖的次数',
	  PRIMARY KEY (`uid`, `aid`, `level`),
	  CONSTRAINT `armor_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

CHECKIN = \
"""
CREATE TABLE `check_in` (
	 `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家唯一标识',
	 `date` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '签到日期',
	 `reward` smallint(6) DEFAULT 0 COMMENT '0：未领奖，1：已领奖',
	 PRIMARY KEY (`uid`, `date`),
	 CONSTRAINT `checkin_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

DARKMARKETITEMS = \
"""
CREATE TABLE `darkmarketitems` (
	  `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `mid` int(11) NOT NULL,
	  `gid` int(11) NOT NULL,
	  `qty` int(11) NOT NULL DEFAULT 0,
	  `cid` int(11) NOT NULL,
	  `amt` int(11) NOT NULL,
	  PRIMARY KEY (`uid`,`mid`),
	  CONSTRAINT `darkmarketitems_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

FACTORY = \
"""
CREATE TABLE `factory` (
	  `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `fid` int(11) NOT NULL,
	  `level` int(11) NOT NULL DEFAULT 0,
	  `workers` int(11) NOT NULL DEFAULT 0,
	  `storage` int(11) NOT NULL DEFAULT 0,
	  `timer` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
	  PRIMARY KEY (`uid`,`fid`),
	  CONSTRAINT `factory_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

FAMILY = \
"""
CREATE TABLE `family` (
	  `name` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `icon` int(11) NOT NULL DEFAULT 0,
	  `exp` int(11) NOT NULL DEFAULT 0,
	  `notice` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
	  `board` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
	  PRIMARY KEY (`name`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

FAMILYHISTORY = \
"""
CREATE TABLE `familyhistory` (
	  `hid` int(11) NOT NULL AUTO_INCREMENT,
	  `name` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `date` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `msg` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
	  PRIMARY KEY (`hid`)
	) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

FAMILYROLE = \
"""
CREATE TABLE `familyrole` (
	  `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `name` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `role` int(11) NOT NULL,
	  PRIMARY KEY (`uid`,`name`),
	  CONSTRAINT `familyrole_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

FRIEND = \
"""
CREATE TABLE `friend` (
	  `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `fid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `recover` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
	  `since` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
	  PRIMARY KEY (`uid`,`fid`),
	  CONSTRAINT `friend_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

ITEM = \
"""
CREATE TABLE `item` (
	  `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `iid` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `value` int(11) NOT NULL DEFAULT 0,
	  PRIMARY KEY (`uid`,`iid`),
	  CONSTRAINT `item_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

LIMITS = \
"""
CREATE TABLE `limits` (
	  `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家唯一id',
	  `lid` smallint(6) NOT NULL COMMENT '任务唯一id',
	  `value` smallint(6) DEFAULT 0 COMMENT '表示记录的次数',
	  PRIMARY KEY (`uid`,`lid`),
	  CONSTRAINT `limits_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

PLAYER = \
"""
CREATE TABLE `player` (
	  `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `gn` varchar(65) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `fid` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
	  PRIMARY KEY (`uid`),
	  UNIQUE KEY `u_gn` (`gn`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

PROGRESS = \
"""
CREATE TABLE `progress` (
	  `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家唯一id',
	  `energy` smallint(6) DEFAULT 10 COMMENT '玩家体力值，默认10',
	  `exp` smallint(6) DEFAULT 0 COMMENT '玩家经验值',
	  `role` smallint(6) DEFAULT 0 COMMENT '拥有的角色数',
	  `weapon` smallint(6) DEFAULT 0 COMMENT '拥有的武器数',
	  `stage` smallint(6) DEFAULT 0 COMMENT '最高普通关卡',
	  `towerstage` smallint(6) DEFAULT 0 COMMENT '冲塔最高关卡',
	  `hangstage` smallint(6) DEFAULT 0 COMMENT '当前挂机的关卡',
	  `videxp` smallint(6) DEFAULT 0 COMMENT 'vip经验',
	  PRIMARY KEY (`uid`),
	  CONSTRAINT `fk_progress_t1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

<<<<<<< .merge_file_5NtewO
ROLE = \
"""
CREATE TABLE `role` (
	  `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `rid` int(11) NOT NULL,
	  `star` int(11) NOT NULL DEFAULT 1,
	  `level` int(11) NOT NULL DEFAULT 0,
	  `skillpoint` int(11) NOT NULL DEFAULT 0,
	  `segment` int(11) NOT NULL DEFAULT 0,
	  PRIMARY KEY (`uid`,`rid`),
	  CONSTRAINT `role_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

ROLEPASSIVE = \
"""
CREATE TABLE `rolepassive` (
	  `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `rid` int(11) NOT NULL,
	  `pid` int(11) NOT NULL,
	  `level` int(11) NOT NULL DEFAULT 0,
	  PRIMARY KEY (`uid`,`rid`,`pid`),
	  CONSTRAINT `rolepassive_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

SKILL = \
"""
CREATE TABLE `skill` (
	  `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `sid` int(11) NOT NULL,
	  `level` int(11) NOT NULL DEFAULT 1,
	  PRIMARY KEY (`uid`,`sid`),
	  CONSTRAINT `skill_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

TASK = \
"""
CREATE TABLE `task` (
	  `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家唯一id',
	  `tid` smallint(6) NOT NULL COMMENT '任务唯一id',
	  `value` smallint(6) DEFAULT 0 COMMENT '表示任务是否完成0:false,1:true',
	  `reward` smallint(6) DEFAULT 0 COMMENT '表示奖励是否已经领取0:false,1:true',
	  `timer` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '完成时间',
	  PRIMARY KEY (`uid`,`tid`),
	  CONSTRAINT `task_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""
=======

def creat_darkmarket(cursor):
	statement = \
	"""
	CREATE TABLE `darkmarket` (
	  `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家id',
	  `pid` smallint(6) NOT NULL COMMENT 'position id',
	  `gid` smallint(6) NOT NULL COMMENT '组id',
	  `mid` smallint(6) NOT NULL COMMENT '商品id',
	  `qty` smallint(6) NOT NULL COMMENT '商品数量',
	  `cid` smallint(6) NOT NULL COMMENT '消耗品id',
	  `amt` smallint(6) NOT NULL COMMENT '消耗品数量',
	  PRIMARY KEY (`uid`, `pid`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
	"""
	cursor.execute(statement)

def create_world(world):
	c = pymysql.connect(host = '192.168.1.102', user = 'root', password = 'lukseun', charset = 'utf8mb4', autocommit=True)
	cursor = c.cursor()
	cursor.execute(f'CREATE DATABASE `{world}`;')
	c.select_db(world)
	cursor = c.cursor()
	create_table_armor(cursor)
	create_table_dark_market(cursor)
	create_table_union_store(cursor)
	create_table_factory(cursor)
	create_table_families(cursor)
	create_table_friend(cursor)
	create_table_leader_board(cursor)
	create_table_player(cursor)
	create_table_role(cursor)
	create_table_skill(cursor)
	create_table_weapon(cursor)
	creat_table_task(cursor)
	create_achievement(cursor)
	create_triggers_player(cursor)

def create_mailbox(world):
	boxlocation = os.path.dirname(os.path.realpath(__file__)) + '/../box'
	box = mailbox.Maildir(boxlocation)
	try:
		wbox = box.get_folder(str(world))
		print('mailbox already exists, skipping...')
	except mailbox.NoSuchMailboxError:
		box.add_folder(str(world))
		print('added mailbox...')
>>>>>>> .merge_file_1AzpG5

TIMER = \
"""
CREATE TABLE `timer` (
	  `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `tid` int(11) NOT NULL,
	  `time` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
	  PRIMARY KEY (`uid`,`tid`),
	  CONSTRAINT `timer_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

WEAPON = \
"""
CREATE TABLE `weapon` (
	  `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `wid` int(11) NOT NULL,
	  `star` int(11) NOT NULL DEFAULT 1,
	  `level` int(11) NOT NULL DEFAULT 0,
	  `skillpoint` int(11) NOT NULL DEFAULT 0,
	  `segment` int(11) NOT NULL DEFAULT 0,
	  PRIMARY KEY (`uid`,`wid`),
	  CONSTRAINT `weapon_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

WEAPONPASSIVE = \
"""
CREATE TABLE `weaponpassive` (
	  `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `wid` int(11) NOT NULL,
	  `pid` int(11) NOT NULL,
	  `level` int(11) NOT NULL DEFAULT 0,
	  PRIMARY KEY (`uid`,`wid`,`pid`),
	  CONSTRAINT `weaponpassive_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

TABLES = [PLAYER, ACHIEVEMENT, ARMOR, CHECKIN, DARKMARKETITEMS, FACTORY, FAMILY, \
		FAMILYHISTORY, FAMILYROLE, FRIEND, ITEM, LIMITS, PROGRESS, \
		ROLE, ROLEPASSIVE, SKILL, TASK, TIMER, WEAPON, WEAPONPASSIVE]

#########################################################################################

def database_exists(db):
	try:
		pymysql.connect(host = '192.168.1.102', user = 'root', password = 'lukseun',
				charset = 'utf8mb4', db = db)
	except pymysql.err.InternalError as e:
		if e.args[0] == 1049: return False
	return True

<<<<<<< .merge_file_5NtewO
def create_world(world):
	if not database_exists(world):
		connection = pymysql.connect(host = '192.168.1.102', user = 'root',
				password = 'lukseun', charset = 'utf8mb4', autocommit = True)
		connection.cursor().execute(f'CREATE DATABASE `{world}`;')
		connection.select_db(world)
		for table in TABLES:
			connection.cursor().execute(table)


=======
def operating_test():
	c = pymysql.connect(host='127.0.0.1', user='root', password='lukseun', charset='utf8mb4', autocommit=True)
	c.select_db("experimental")
	cursor = c.cursor()
	# creat_table_task(cursor)
	# create_table_armor(cursor)
	# create_achievement(cursor)
	# create_table_union_store(cursor)
	# create_check_in(cursor)
	# create_table_player(cursor)
	# create_table_families(cursor)
	# creat_limits(cursor)

	# cursor.execute(f'DROP TABLE progress')
	creat_darkmarket(cursor)
	# creat_progress(cursor)
	# cursor.execute(f'insert into progress (uid, exp) value ("1", 0)')
	# code = cursor.execute(f'insert into timer (uid, tid) value ("1", 11)')
	# cursor.execute('select iid from item where uid = "1";')
	# print(cursor.fetchall())
	# code = cursor.execute(f'insert into item (uid, iid) value ("1", 10)')
	# print(code)
	# for i in range(1, 100):
	# 	cursor.execute(f'insert into progress (uid, exp) values ("{i}", 0)')
>>>>>>> .merge_file_1AzpG5


if __name__ == '__main__':
	create_world(input('Enter world name: '))


