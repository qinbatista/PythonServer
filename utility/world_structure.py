'''
world_structure.py

Contains the CREATE statements necessary to create the lukseun database structure.
Also includes necessary triggers.
'''

STAGES = \
"""
CREATE TABLE `stages` (
	 `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户唯一id',
	 `sid` SMALLINT UNSIGNED NOT NULL COMMENT '关卡类型id',
	 `stage` INT UNSIGNED NOT NULL COMMENT '关卡最高等级',
	 `btm` VARCHAR(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '进入时间',
	 PRIMARY KEY (`uid`, `sid`),
	 CONSTRAINT `stage_player_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

SUMMON = \
"""
CREATE TABLE `summon` (
	 `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户唯一id',
	 `cid` SMALLINT UNSIGNED NOT NULL COMMENT '消耗品id',
	 `pid` SMALLINT UNSIGNED NOT NULL COMMENT '位置id',
	 `mid` VARCHAR(16) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '商品eg=0:1:1',
	 `wgt` SMALLINT UNSIGNED NOT NULL DEFAULT 1 COMMENT '商品权重weight，只能为正整数',
	 `isb` SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '0：未购买，1：已购买',
	 PRIMARY KEY (`uid`, `cid`, `pid`),
	 CONSTRAINT `summon_player_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

ACHIEVEMENT = \
"""
CREATE TABLE `achievement` (
	 `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户唯一id',
	 `aid` SMALLINT UNSIGNED NOT NULL COMMENT '成就唯一id',
	 `value` SMALLINT UNSIGNED DEFAULT 0 COMMENT '成就完成的次数',
	 `reward` SMALLINT UNSIGNED DEFAULT 0 COMMENT '完成成就领奖的次数',
	 PRIMARY KEY (`uid`,`aid`),
	 CONSTRAINT `achievement_player_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

ARMOR = \
"""
CREATE TABLE `armor` (
	  `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户唯一id',
	  `aid` SMALLINT UNSIGNED NOT NULL COMMENT '盔甲id1-40种盔甲',
	  `level` SMALLINT UNSIGNED NOT NULL COMMENT '盔甲等级1-11级',
	  `quantity` INT UNSIGNED DEFAULT 0 COMMENT '盔甲数量',
	  PRIMARY KEY (`uid`, `aid`, `level`),
	  CONSTRAINT `armor_player_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

CHECKIN = \
"""
CREATE TABLE `check_in` (
	 `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户唯一id',
	 `date` VARCHAR(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '签到日期',
	 `reward` SMALLINT UNSIGNED DEFAULT 1 COMMENT '0：未领奖，1：已领奖',
	 PRIMARY KEY (`uid`, `date`),
	 CONSTRAINT `checkin_player_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""
FACTORY = \
"""
CREATE TABLE `factory` (
	  `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户唯一id',
	  `fid` SMALLINT NOT NULL COMMENT '工厂id',
	  `level` SMALLINT UNSIGNED NOT NULL DEFAULT 1 COMMENT '工厂等级',
	  `workers` SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '工厂工人',
	  `storage` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '工厂仓库',
	  PRIMARY KEY (`uid`,`fid`),
	  CONSTRAINT `factory_player_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

FAMILY = \
"""
CREATE TABLE `family` (
	  `name` VARCHAR(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '家族id(名字)',
	  `icon` SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '家族图标',
	  `exp` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '家族经验',
	  `notice` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '家族公告',
	  `board` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '家族黑板',
	  `rmtimes` SMALLINT UNSIGNED NOT NULL DEFAULT 5 COMMENT '可移除家族成员的剩余次数',
	  `rmtimer` VARCHAR(64) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '移除家族成员的日期，用于重置移除成员次数',
	  PRIMARY KEY (`name`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

FAMILYHISTORY = \
"""
CREATE TABLE `familyhistory` (
	  `hid` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '家族历史id',
	  `name` VARCHAR(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '家族id(名字)',
	  `date` VARCHAR(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '家族历史操作发生时间',
	  `msg` VARCHAR(256) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '家族历史操作信息',
	  PRIMARY KEY (`hid`, `name`),
	  CONSTRAINT `familyhistory_family_1` FOREIGN KEY (`name`) REFERENCES `family` (`name`) ON DELETE CASCADE ON UPDATE CASCADE
	) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

FAMILYROLE = \
"""
CREATE TABLE `familyrole` (
	  `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户唯一id',
	  `name` VARCHAR(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '家族id(名字)',
	  `role` SMALLINT UNSIGNED NOT NULL COMMENT '家族成员等级',
	  PRIMARY KEY (`uid`,`name`),
	  CONSTRAINT `familyrole_player_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE,
	  CONSTRAINT `familyrole_family_1` FOREIGN KEY (`name`) REFERENCES `family` (`name`) ON DELETE CASCADE ON UPDATE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

FRIEND = \
"""
CREATE TABLE `friend` (
	  `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户唯一id',
	  `fid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '朋友唯一id',
	  `recover` VARCHAR(64) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '发生礼物当天日期',
	  `since` VARCHAR(64) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '成为好友的当天日期',
	  PRIMARY KEY (`uid`,`fid`),
	  CONSTRAINT `friend_player_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

ITEM = \
"""
CREATE TABLE `item` (
	  `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户唯一id',
	  `iid` INT UNSIGNED NOT NULL COMMENT '物品id',
	  `value` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '物品数量',
	  PRIMARY KEY (`uid`,`iid`),
	  CONSTRAINT `item_player_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

LIMITS = \
"""
CREATE TABLE `limits` (
	  `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家id',
	  `lid` SMALLINT UNSIGNED NOT NULL COMMENT '次数限制id',
	  `value` INT UNSIGNED DEFAULT 0 COMMENT '次数',
	  PRIMARY KEY (`uid`, `lid`),
	  CONSTRAINT `limits_player_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

PLAYER = \
"""
CREATE TABLE `player` (
	  `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家id',
	  `gn` VARCHAR(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家游戏名',
	  `fid` VARCHAR(32) COLLATE utf8mb4_unicode_ci COMMENT '家族id(名字)',
	  `intro` VARCHAR(64) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '玩家自我介绍',
	  PRIMARY KEY (`uid`),
	  UNIQUE KEY `u_gn` (`gn`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""
# CONSTRAINT `clear_fid` FOREIGN KEY (`fid`) REFERENCES `family` (`name`) ON DELETE SET ''
# ALTER TABLE player ADD CONSTRAINT `clear_fid`
# FOREIGN KEY(`fid`) REFERENCES `family` (`name`) ON DELETE SET NULL;

PROGRESS = \
"""
CREATE TABLE `progress` (
	  `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家id',
	  `energy` SMALLINT UNSIGNED DEFAULT 120 COMMENT '玩家体力值',
	  `exp` INT UNSIGNED DEFAULT 0 COMMENT '玩家经验',
	  `vipexp` INT UNSIGNED DEFAULT 0 COMMENT 'vip经验',
	  `role` SMALLINT UNSIGNED DEFAULT 0 COMMENT '正在使用的角色',
	  `weapon` SMALLINT UNSIGNED DEFAULT 0 COMMENT '正在使用的武器',
	  `stage` SMALLINT UNSIGNED DEFAULT 0 COMMENT '当前正在进行的关卡',
	  PRIMARY KEY (`uid`),
	  CONSTRAINT `progress_player_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

ROLE = \
"""
CREATE TABLE `role` (
	  `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家id',
	  `rid` SMALLINT UNSIGNED NOT NULL COMMENT '角色id',
	  `star` SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '角色星数',
	  `level` SMALLINT UNSIGNED NOT NULL DEFAULT 1 COMMENT '角色等级',
	  `skillpoint` SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '角色技能剩余点数',
	  `segment` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '碎片数',
	  PRIMARY KEY (`uid`,`rid`),
	  CONSTRAINT `role_player_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

ROLEPASSIVE = \
"""
CREATE TABLE `rolepassive` (
	  `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家id',
	  `rid` SMALLINT UNSIGNED NOT NULL COMMENT '角色id',
	  `pid` SMALLINT UNSIGNED NOT NULL COMMENT '角色技能id',
	  `level` SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '技能等级',
	  PRIMARY KEY (`uid`,`rid`,`pid`),
	  CONSTRAINT `rolepassive_player_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

SKILL = \
"""
CREATE TABLE `skill` (
	  `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家id',
	  `sid` SMALLINT UNSIGNED NOT NULL COMMENT '玩家技能id',
	  `level` SMALLINT UNSIGNED NOT NULL DEFAULT 1 COMMENT '玩家技能等级',
	  PRIMARY KEY (`uid`,`sid`),
	  CONSTRAINT `skill_player_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

TASK = \
"""
CREATE TABLE `task` (
	  `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家id',
	  `tid` SMALLINT UNSIGNED NOT NULL COMMENT '任务id',
	  `value` SMALLINT UNSIGNED DEFAULT 0 COMMENT '表示任务是否完成0:false,1:true',
	  `reward` SMALLINT UNSIGNED DEFAULT 0 COMMENT '表示奖励是否已经领取0:false,1:true',
	  `timer` VARCHAR(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '完成时间',
	  PRIMARY KEY (`uid`,`tid`),
	  CONSTRAINT `task_player_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

TIMER = \
"""
CREATE TABLE `timer` (
	  `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家id',
	  `tid` SMALLINT UNSIGNED NOT NULL COMMENT '时间id',
	  `time` VARCHAR(64) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '时间',
	  PRIMARY KEY (`uid`,`tid`),
	  CONSTRAINT `timer_player_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

WEAPON = \
"""
CREATE TABLE `weapon` (
	  `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家id',
	  `wid` SMALLINT UNSIGNED NOT NULL COMMENT '武器id',
	  `star` SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '星数',
	  `level` SMALLINT UNSIGNED NOT NULL DEFAULT 1 COMMENT '武器等级',
	  `skillpoint` SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '武器剩余技能点数',
	  `segment` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '碎片',
	  PRIMARY KEY (`uid`,`wid`),
	  CONSTRAINT `weapon_player_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

WEAPONPASSIVE = \
"""
CREATE TABLE `weaponpassive` (
	  `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家id',
	  `wid` SMALLINT UNSIGNED NOT NULL COMMENT '武器id',
	  `pid` SMALLINT UNSIGNED NOT NULL COMMENT '武器技能id',
	  `level` SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '武器技能等级',
	  PRIMARY KEY (`uid`,`wid`,`pid`),
	  CONSTRAINT `weaponpassive_player_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

DARKMARKET = \
	"""
	CREATE TABLE `darkmarket` (
	  `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家id',
	  `pid` SMALLINT UNSIGNED NOT NULL COMMENT '位置id',
	  `gid` SMALLINT UNSIGNED NOT NULL COMMENT '组id',
	  `mid` SMALLINT UNSIGNED NOT NULL COMMENT '商品id',
	  `qty` SMALLINT UNSIGNED NOT NULL COMMENT '商品数量',
	  `cid` SMALLINT UNSIGNED NOT NULL COMMENT '消耗品id',
	  `amt` SMALLINT NOT NULL COMMENT '消耗品数量',
	  PRIMARY KEY (`uid`, `pid`),
	  CONSTRAINT `darkmarket_player_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
	"""

LEADERBOARD = \
"""
CREATE TABLE `leaderboard` (
	  `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家id',
	  `lid` SMALLINT UNSIGNED NOT NULL COMMENT '排行id',
	  `value` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '伤害',
	  PRIMARY KEY (`uid`,`lid`),
	  CONSTRAINT `leaderboard_player_1` FOREIGN KEY (`uid`) REFERENCES `player` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

MALL = \
"""
CREATE TABLE `mall` (
	  `oid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '订单号',
	  `world` VARCHAR(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户所在的世界',
	  `uid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家id',
	  `username` VARCHAR(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户游戏名',
	  `currency` VARCHAR(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '购买币种',
	  `cqty` SMALLINT UNSIGNED NOT NULL COMMENT '购买金额',
	  `mid` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '商品id',
	  `mqty` INT UNSIGNED NOT NULL COMMENT '商品数量',
	  `channel` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '渠道名字',
	  `time` VARCHAR(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '购买时间',
	  `repeatable` VARCHAR(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '是否为永久性物品',
	  `receive` SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '道具是否已领取道具',
	  PRIMARY KEY (`oid`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

EXCHANGE = \
"""
CREATE TABLE `exchange` (
	  `gid`   VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '游戏id',
	  `eid`   VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '兑换码',
	  `pid`   VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '物品id',
	  `etime` VARCHAR(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '兑换码结束时间',
	  `receive` SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '道具可领取次数，非0为可兑换',
	  PRIMARY KEY (`gid`, `eid`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

CONSTRAINT = \
"""
	ALTER TABLE player ADD CONSTRAINT `player_family_1`
	FOREIGN KEY(`fid`) REFERENCES `family` (`name`) ON DELETE SET NULL ON UPDATE CASCADE;
"""

TRIGGER1 = \
"""
CREATE TRIGGER `player_AFTER_INSERT1` AFTER INSERT ON `player` FOR EACH ROW
BEGIN
	INSERT INTO progress(uid) VALUES (new.uid);
END;
"""

TRIGGER2 = \
"""
CREATE TRIGGER `player_BEFORE_INSERT1` BEFORE UPDATE ON `player` FOR EACH ROW
BEGIN
	IF (old.fid IS NULL) AND (new.fid IS NOT NULL)
	THEN
		INSERT INTO familyrole(uid, name, role) VALUES (new.uid, new.fid, 0);
	END IF;
END;
"""

TABLES = [PLAYER, SUMMON, ACHIEVEMENT, ARMOR, CHECKIN, DARKMARKET,
		FACTORY, FAMILY, FAMILYHISTORY, FAMILYROLE, FRIEND, ITEM, LEADERBOARD, LIMITS,
		PROGRESS, ROLE, ROLEPASSIVE, SKILL, TASK, TIMER, WEAPON, WEAPONPASSIVE,
		CONSTRAINT]

TRIGGERS = [TRIGGER1, TRIGGER2]

