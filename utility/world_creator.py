'''
world_creator.py
'''

import os
import mailbox
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
	  `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户id',
	  `aid` int(11) NOT NULL COMMENT '盔甲id1-40种盔甲',
	  `level` int(11) NOT NULL COMMENT '盔甲等级1-10级',
	  `quantity` int(11) DEFAULT 0 COMMENT '盔甲数量',
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
FACTORY = \
"""
CREATE TABLE `factory` (
	  `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `fid` int(11) NOT NULL,
	  `level` int(11) NOT NULL DEFAULT 1,
	  `workers` int(11) NOT NULL DEFAULT 0,
	  `storage` int(11) NOT NULL DEFAULT 0,
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
	  `intro` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
	  PRIMARY KEY (`uid`),
	  UNIQUE KEY `u_gn` (`gn`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

PLAYERAFTERINSERT = \
"""
CREATE TRIGGER `player_AFTER_INSERT` AFTER INSERT ON `player` FOR EACH ROW
BEGIN
INSERT INTO progress(uid) VALUES (new.uid);
END
"""

PROGRESS = \
"""
CREATE TABLE `progress` (
	  `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家唯一id',
	  `energy` smallint(6) DEFAULT 10 COMMENT '玩家体力值，默认10',
	  `exp` smallint(6) DEFAULT 0 COMMENT '玩家经验值',
	  `role` smallint(6) DEFAULT 1 COMMENT '拥有的角色数',
	  `weapon` smallint(6) DEFAULT 0 COMMENT '拥有的武器数',
	  `stage` smallint(6) DEFAULT 0 COMMENT '最高普通关卡',
	  `towerstage` smallint(6) DEFAULT 0 COMMENT '冲塔最高关卡',
	  `hangstage` smallint(6) DEFAULT 0 COMMENT '当前挂机的关卡',
	  `vipexp` smallint(6) DEFAULT 0 COMMENT 'vip经验',
	  PRIMARY KEY (`uid`),
	  CONSTRAINT `fk_progress_t1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

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

DARKMARKET = \
	"""
	CREATE TABLE `darkmarket` (
	  `uid` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家id',
	  `pid` smallint(6) NOT NULL COMMENT 'position id',
	  `gid` smallint(6) NOT NULL COMMENT '组id',
	  `mid` smallint(6) NOT NULL COMMENT '商品id',
	  `qty` smallint(6) NOT NULL COMMENT '商品数量',
	  `cid` smallint(6) NOT NULL COMMENT '消耗品id',
	  `amt` smallint(6) NOT NULL COMMENT '消耗品数量',
	  PRIMARY KEY (`uid`, `pid`),
	  CONSTRAINT `darkmarket_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
	"""

TABLES = [PLAYER, PLAYERAFTERINSERT, ACHIEVEMENT, ARMOR, CHECKIN, DARKMARKETITEMS, \
		FACTORY, FAMILY, FAMILYHISTORY, FAMILYROLE, FRIEND, ITEM, LIMITS, PROGRESS, \
		ROLE, ROLEPASSIVE, SKILL, TASK, TIMER, WEAPON, WEAPONPASSIVE,DARKMARKET]




#########################################################################################

def database_exists(db):
	try:
		pymysql.connect(host = '192.168.1.102', user = 'root', password = 'lukseun',
				charset = 'utf8mb4', db = db)
	except pymysql.err.InternalError as e:
		if e.args[0] == 1049: return False
	return True

def create_db(world):
	if not database_exists(world):
		connection = pymysql.connect(host = '192.168.1.102', user = 'root',
				password = 'lukseun', charset = 'utf8mb4', autocommit = True)
		connection.cursor().execute(f'CREATE DATABASE `{world}`;')
		connection.select_db(world)
		for table in TABLES:
			connection.cursor().execute(table)
		print(f'created new database for world {world}..')
	else:
		print(f'database for world {world} already exists, skipping..')
		connection = pymysql.connect(host = '192.168.1.102', user = 'root',
				password = 'lukseun', charset = 'utf8mb4', autocommit = True)
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

def create_world(world):
	create_db(world)
	create_mailbox(world)



if __name__ == '__main__':
	create_world(input('Enter world name: '))


