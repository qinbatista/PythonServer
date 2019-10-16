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
	  PRIMARY KEY (`uid`,`name`)
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

TABLES = [ACHIEVEMENT, ARMOR, CHECKIN, DARKMARKETITEMS, FACTORY, FAMILY, \
		FAMILYHISTORY, FAMILYROLE, FRIEND, ITEM, LIMITS, PLAYER, PROGRESS, \
		ROLE, ROLEPASSIVE, SKILL, TASK, TIMER, WEAPON, WEAPONPASSIVE]

#########################################################################################

def database_exists(db):
	try:
		pymysql.connect(host = '192.168.1.102', user = 'root', password = 'lukseun',
				charset = 'utf8mb4', db = db)
	except pymysql.err.InternalError as e:
		if e.args[0] == 1049: return False
	return True

def create_world(world):
	if not database_exists(world):
		connection = pymysql.connect(host = '192.168.1.102', user = 'root',
				password = 'lukseun', charset = 'utf8mb4', autocommit = True)
		connection.cursor().execute(f'CREATE DATABASE `{world}`;')
		for table in TABLES:
			connection.cursor().execute(table)




if __name__ == '__main__':
	create_world(input('Enter world name: '))


