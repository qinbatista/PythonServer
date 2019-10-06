# world_creator.py

import os
import pymysql
import mailbox

def create_table_armor(cursor):
	statement = \
	"""
	CREATE TABLE `armor` (
	  `unique_id` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家唯一标识',
	  `armor_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '盔甲唯一标识',
	  `armor_level1` int(6) NOT NULL DEFAULT 0 COMMENT '盔甲的等级1',
	  `armor_level2` int(6) NOT NULL DEFAULT 0 COMMENT '盔甲的等级2',
	  `armor_level3` int(6) NOT NULL DEFAULT 0 COMMENT '盔甲的等级3',
	  `armor_level4` int(6) NOT NULL DEFAULT 0 COMMENT '盔甲的等级4',
	  `armor_level5` int(6) NOT NULL DEFAULT 0 COMMENT '盔甲的等级5',
	  `armor_level6` int(6) NOT NULL DEFAULT 0 COMMENT '盔甲的等级6',
	  `armor_level7` int(6) NOT NULL DEFAULT 0 COMMENT '盔甲的等级7',
	  `armor_level8` int(6) NOT NULL DEFAULT 0 COMMENT '盔甲的等级8',
	  `armor_level9` int(6) NOT NULL DEFAULT 0 COMMENT '盔甲的等级9',
	  `armor_level10` int(6) NOT NULL DEFAULT 0 COMMENT '盔甲的等级10',
	  PRIMARY KEY (`unique_id`,`armor_id`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
	"""
	cursor.execute(statement)

def create_table_dark_market(cursor):
	statement = \
	"""
	CREATE TABLE `dark_market` (
	  `unique_id` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家唯一标识',
	  `merchandise1` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '黑市中展示可以买的材料1',
	  `merchandise1_quantity` int(6) DEFAULT 0 COMMENT '黑市中展示可以买的材料1的数量',
	  `currency_type1` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '材料1的价值(金币或者钻石)',
	  `currency_type1_price` int(6) DEFAULT 0 COMMENT '材料1的价格',
	  `merchandise2` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '黑市中展示可以买的材料2',
	  `merchandise2_quantity` int(6) DEFAULT 0 COMMENT '黑市中展示可以买的材料2的数量',
	  `currency_type2` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '材料2的价值(金币或者钻石)',
	  `currency_type2_price` int(6) DEFAULT 0 COMMENT '材料2的价格',
	  `merchandise3` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '黑市中展示可以买的材料3',
	  `merchandise3_quantity` int(6) DEFAULT 0 COMMENT '黑市中展示可以买的材料3的数量',
	  `currency_type3` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '材料3的价值(金币或者钻石)',
	  `currency_type3_price` int(6) DEFAULT 0 COMMENT '材料3的价格',
	  `merchandise4` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '黑市中展示可以买的材料4',
	  `merchandise4_quantity` int(6) DEFAULT 0 COMMENT '黑市中展示可以买的材料4的数量',
	  `currency_type4` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '材料4的价值(金币或者钻石)',
	  `currency_type4_price` int(6) DEFAULT 0 COMMENT '材料4的价格',
	  `merchandise5` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '黑市中展示可以买的材料5',
	  `merchandise5_quantity` int(6) DEFAULT 0 COMMENT '黑市中展示可以买的材料5的数量',
	  `currency_type5` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '材料5的价值(金币或者钻石)',
	  `currency_type5_price` int(6) DEFAULT 0 COMMENT '材料5的价格',
	  `merchandise6` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '黑市中展示可以买的材料6',
	  `merchandise6_quantity` int(6) DEFAULT 0 COMMENT '黑市中展示可以买的材料6的数量',
	  `currency_type6` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '材料6的价值(金币或者钻石)',
	  `currency_type6_price` int(6) DEFAULT 0 COMMENT '材料6的价格',
	  `merchandise7` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '黑市中展示可以买的材料7',
	  `merchandise7_quantity` int(6) DEFAULT 0 COMMENT '黑市中展示可以买的材料7的数量',
	  `currency_type7` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '材料7的价值(金币或者钻石)',
	  `currency_type7_price` int(6) DEFAULT 0 COMMENT '材料7的价格',
	  `merchandise8` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '黑市中展示可以买的材料8',
	  `merchandise8_quantity` int(6) DEFAULT 0 COMMENT '黑市中展示可以买的材料8的数量',
	  `currency_type8` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '材料8的价值(金币或者钻石)',
	  `currency_type8_price` int(6) DEFAULT 0 COMMENT '材料8的价格',
	  `refresh_time` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '刷新所有材料的刷新时间',
	  `refreshable_quantity` int(6) DEFAULT 0 COMMENT '可以刷新所有材料的次数',
	  PRIMARY KEY (`unique_id`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
	"""
	cursor.execute(statement)

def create_table_union_store(cursor):
	statement = \
	"""
	CREATE TABLE `union_store` (
	  `unique_id` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家唯一标识',
	  `merchandise1` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '工会商店中展示可以买的材料1',
	  `merchandise1_quantity` int(6) DEFAULT 0 COMMENT '工会商店中展示可以买的材料1的数量',
	  `currency_type1` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '材料1的价值(金币或者钻石)',
	  `currency_type1_price` int(6) DEFAULT 0 COMMENT '材料1的价格',
	  `merchandise2` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '工会商店中展示可以买的材料2',
	  `merchandise2_quantity` int(6) DEFAULT 0 COMMENT '工会商店中展示可以买的材料2的数量',
	  `currency_type2` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '材料2的价值(金币或者钻石)',
	  `currency_type2_price` int(6) DEFAULT 0 COMMENT '材料2的价格',
	  `merchandise3` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '工会商店中展示可以买的材料3',
	  `merchandise3_quantity` int(6) DEFAULT 0 COMMENT '工会商店中展示可以买的材料3的数量',
	  `currency_type3` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '材料3的价值(金币或者钻石)',
	  `currency_type3_price` int(6) DEFAULT 0 COMMENT '材料3的价格',
	  `merchandise4` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '工会商店中展示可以买的材料4',
	  `merchandise4_quantity` int(6) DEFAULT 0 COMMENT '工会商店中展示可以买的材料4的数量',
	  `currency_type4` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '材料4的价值(金币或者钻石)',
	  `currency_type4_price` int(6) DEFAULT 0 COMMENT '材料4的价格',
	  `merchandise5` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '工会商店中展示可以买的材料5',
	  `merchandise5_quantity` int(6) DEFAULT 0 COMMENT '工会商店中展示可以买的材料5的数量',
	  `currency_type5` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '材料5的价值(金币或者钻石)',
	  `currency_type5_price` int(6) DEFAULT 0 COMMENT '材料5的价格',
	  `merchandise6` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '工会商店中展示可以买的材料6',
	  `merchandise6_quantity` int(6) DEFAULT 0 COMMENT '工会商店中展示可以买的材料6的数量',
	  `currency_type6` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '材料6的价值(金币或者钻石)',
	  `currency_type6_price` int(6) DEFAULT 0 COMMENT '材料6的价格',
	  `merchandise7` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '工会商店中展示可以买的材料7',
	  `merchandise7_quantity` int(6) DEFAULT 0 COMMENT '工会商店中展示可以买的材料7的数量',
	  `currency_type7` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '材料7的价值(金币或者钻石)',
	  `currency_type7_price` int(6) DEFAULT 0 COMMENT '材料7的价格',
	  `merchandise8` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '工会商店中展示可以买的材料8',
	  `merchandise8_quantity` int(6) DEFAULT 0 COMMENT '工会商店中展示可以买的材料8的数量',
	  `currency_type8` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '材料8的价值(金币或者钻石)',
	  `currency_type8_price` int(6) DEFAULT 0 COMMENT '材料8的价格',
	  `refresh_time` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '刷新所有材料的刷新时间',
	  `refreshable_quantity` int(6) DEFAULT 0 COMMENT '可以刷新所有材料的次数',
	  PRIMARY KEY (`unique_id`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
	"""
	cursor.execute(statement)

def create_table_factory(cursor):
	statement = \
	"""
	CREATE TABLE `factory` (
	  `unique_id` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家唯一标识',
	  `food_factory_level` int(11) unsigned DEFAULT 1 COMMENT '食品工厂的等级',
	  `mine_factory_level` int(11) unsigned DEFAULT 1 COMMENT '矿山工厂的等级',
	  `crystal_factory_level` int(11) unsigned DEFAULT 1 COMMENT '水晶工厂的等级',
	  `equipment_factory_level` int(11) unsigned DEFAULT 1 COMMENT '设备工厂的等级',
	  `food_factory_timer` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '食品工厂工作的开始时间',
	  `mine_factory_timer` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '矿山工厂工作的开始时间',
	  `crystal_factory_timer` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '水晶工厂工作的开始时间',
	  `equipment_factory_timer` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '设备工厂工作的开始时间',
	  `food_factory_workers` int(11) unsigned DEFAULT 0 COMMENT '食品工厂的工人',
	  `mine_factory_workers` int(11) unsigned DEFAULT 0 COMMENT '矿山工厂的工人',
	  `crystal_factory_workers` int(11) unsigned DEFAULT 0 COMMENT '水晶工厂的工人',
	  `equipment_factory_workers` int(11) unsigned DEFAULT 0 COMMENT '设备工厂的工人',
	  `totally_workers` int(11) unsigned DEFAULT 10 COMMENT '剩余可调配工人的数量(此工人可分配到各种类型的工厂)',
	  `food_storage` int(11) unsigned DEFAULT 0 COMMENT '存储的食物数量',
	  `iron_storage` int(11) unsigned DEFAULT 0 COMMENT '存储的铁数量',
	  `crystal_storage` int(11) unsigned DEFAULT 0 COMMENT '存储的水晶数量',
	  `equipment_storage` int(11) unsigned DEFAULT 0 COMMENT '存储的盔甲1数量',
	  `wishing_pool_level` int(11) unsigned DEFAULT 1 COMMENT '许愿池的等级',
	  `wishing_pool_timer` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '许愿的开始时间',
	  `acceleration_end_time` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '加速结束时间',
	  `wishing_pool_times` int(11) unsigned DEFAULT 0 COMMENT '许愿池次数',
	  `equipment_product_type` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '设备工厂产品类型',
	  PRIMARY KEY (`unique_id`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
	"""
	cursor.execute(statement)

def create_table_families(cursor):
	statement = \
	"""
	CREATE TABLE `families` (
	  `familyid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
	  `familyname` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
	  `level` int(11) DEFAULT 0 COMMENT '工会等级',
	  `icon` BLOB NULL DEFAULT (0x0) COMMENT '工会图标',
	  `experience` int(11) DEFAULT 0 COMMENT '工会经验',
	  `announcement` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '工会公告',
	  `news` varchar(4095) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '工会动态',
	  `president` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '会长游戏名',
	  `admin1` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '管理员1游戏名',
	  `admin2` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '管理员2游戏名',
	  `admin3` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '管理员3游戏名',
	  `elite1` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '精英1游戏名',
	  `elite2` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '精英2游戏名',
	  `elite3` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '精英3游戏名',
	  `elite4` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '精英4游戏名',
	  `elite5` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '精英5游戏名',
	  `remove_start_time` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '删除成员的开始时间',
	  `remove_times` int(6) DEFAULT 5 COMMENT '当天可删除的次数',
	  `disbanded_family_time` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '解散工会的开始时间',
	  PRIMARY KEY (`familyid`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
	"""
	cursor.execute(statement)

def create_table_friend(cursor):
	statement = \
	"""
	CREATE TABLE `friend` (
	  `unique_id` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家唯一标识',
	  `friend_id` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '朋友唯一标识',
	  `friend_name` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '朋友的名字',
	  `friend_level` int(6) DEFAULT 0 COMMENT '朋友的等级',
	  `recovery_time` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '朋友好感度恢复时间',
	  `become_friend_time` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '成为好友的时间',
	  PRIMARY KEY (`unique_id`,`friend_id`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
	"""
	cursor.execute(statement)

def create_table_leader_board(cursor):
	statement = \
	"""
	CREATE TABLE `leader_board` (
	  `unique_id` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家唯一标识',
	  `once_top_damage` int(255) unsigned DEFAULT 0 COMMENT '用户打世界Boss的单次伤害值',
	  `world_boss_damage` int(255) unsigned DEFAULT 0 COMMENT '用户打世界Boss的累计伤害值',
	  PRIMARY KEY (`unique_id`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
	"""
	cursor.execute(statement)

def create_table_player(cursor):
	statement = \
	"""
	CREATE TABLE `player` (
	  `unique_id` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家唯一标识',
	  `game_name` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '游戏名字',
	  `coin` int(11) DEFAULT 0 COMMENT '金币',
	  `iron` int(11) DEFAULT 0 COMMENT '铁',
	  `diamond` int(11) DEFAULT 0 COMMENT '钻石',
	  `energy` int(11) DEFAULT 0 COMMENT '能量',
	  `experience` int(11) DEFAULT 0 COMMENT '玩家经验',
	  `level` int(11) DEFAULT 0 COMMENT '玩家等级',
	  `role` int(11) DEFAULT 0 COMMENT '角色',
	  `stage` int(11) DEFAULT 0 COMMENT '关卡等级',
	  `tower_stage` int(11) DEFAULT 0 COMMENT '塔的阶段',
	  `skill_scroll_10` int(11) DEFAULT 0 COMMENT '低级卷轴',
	  `skill_scroll_30` int(11) DEFAULT 0 COMMENT '中级卷轴',
	  `skill_scroll_100` int(11) DEFAULT 0 COMMENT '高级卷轴',
	  `experience_potion` int(11) DEFAULT 0 COMMENT '经验药水',
	  `small_energy_potion` int(11) DEFAULT 0 COMMENT '小能量药水',
	  `recover_time` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '恢复开始时间',
	  `hang_stage` int(6) DEFAULT 0 COMMENT '挂机的关卡',
	  `hang_up_time` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '挂机开始时间',
	  `basic_summon_scroll` int(11) DEFAULT 0 COMMENT '低级召唤卷轴',
	  `pro_summon_scroll` int(11) DEFAULT 0 COMMENT '高级召唤卷轴',
	  `friend_gift` int(11) DEFAULT 0 COMMENT '朋友礼物',
	  `prophet_summon_scroll` int(11) DEFAULT 0 COMMENT '先知召唤卷轴',
	  `fortune_wheel_ticket_basic` int(11) DEFAULT 0 COMMENT '低级幸运循环票',
	  `fortune_wheel_ticket_pro` int(11) DEFAULT 0 COMMENT '高级幸运循环票',
	  `familyid` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '家族ID',
	  `world_boss_enter_time` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '进入世界boss的时间',
	  `world_boss_remaining_times` int(6) DEFAULT 0 COMMENT '进入世界boss的剩余次数',
	  `food` int(11) unsigned DEFAULT 0 COMMENT '食物',
	  `crystal` int(11) unsigned DEFAULT 0 COMMENT '水晶',
	  `sign_in_time` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '工会签到的日期',
	  `union_contribution` int(11) unsigned DEFAULT 0 COMMENT '工会贡献值',
	  `cumulative_contribution` int(11) unsigned DEFAULT 0 COMMENT '工会累积贡献值',
	  `leave_family_time` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '离开工会的开始时间',
	  `registration_time` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '用户注册的时间',
	  `login_in_time` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '用户登录的时间',
	  `mail_gift_time` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '参与活动的时间',
	  `add_friends_time` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '添加好友的时间',
	  `add_friends_times` int(11) unsigned DEFAULT 50 COMMENT '添加好友的次数',
	  `vip_experience` int(11) unsigned DEFAULT 0 COMMENT 'VIP经验',
	  `daily_reward_time` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT 'VIP每日奖励的刷新时间',
	  `universal_segment` int(11) unsigned DEFAULT 0 COMMENT '万能碎片',
	  `universal_segment_6` int(11) unsigned DEFAULT 0 COMMENT '6星万能碎片',
	  `vip_card_type` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '月卡类型',
	  `vip_card_deadline` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '月卡截止时间',
	  `coin_card` int(11) unsigned DEFAULT 0 COMMENT '金币卡',
	  `exp_card` int(11) unsigned DEFAULT 0 COMMENT '经验卡',
	  `food_card` int(11) unsigned DEFAULT 0 COMMENT '食物卡',
	  `mine_card` int(11) unsigned DEFAULT 0 COMMENT '合金卡',
	  `crystal_card` int(11) unsigned DEFAULT 0 COMMENT '水晶卡',
	  `diamond_card` int(11) unsigned DEFAULT 0 COMMENT '钻石卡',
	  PRIMARY KEY (`unique_id`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
	"""
	cursor.execute(statement)

def create_table_role(cursor):
	statement = \
	"""
	CREATE TABLE `role` (
	  `unique_id` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家唯一标识',
	  `role_name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色名字',
	  `role_star` smallint(6) DEFAULT 0 COMMENT '角色星数',
	  `role_level` smallint(6) DEFAULT 0 COMMENT '角色等级',
	  `passive_skill_1_level` smallint(6) DEFAULT 0 COMMENT '角色技能1',
	  `passive_skill_2_level` smallint(6) DEFAULT 0 COMMENT '角色技能2',
	  `passive_skill_3_level` smallint(6) DEFAULT 0 COMMENT '角色技能3',
	  `passive_skill_4_level` smallint(6) DEFAULT 0 COMMENT '角色技能4',
	  `skill_point` smallint(6) DEFAULT 0 COMMENT '角色技能点',
	  `segment` smallint(6) DEFAULT 0 COMMENT '角色碎片',
	  PRIMARY KEY (`unique_id`,`role_name`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
	"""
	cursor.execute(statement)

def create_table_skill(cursor):
	statement = \
	"""
	CREATE TABLE `skill` (
	  `unique_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'new_id',
	  `m1_level` tinyint(4) DEFAULT 0,
	  `m11_level` tinyint(4) DEFAULT 0,
	  `m12_level` tinyint(4) DEFAULT 0,
	  `m13_level` tinyint(4) DEFAULT 0,
	  `m111_level` tinyint(4) DEFAULT 0,
	  `m112_level` tinyint(4) DEFAULT 0,
	  `m113_level` tinyint(4) DEFAULT 0,
	  `m121_level` tinyint(4) DEFAULT 0,
	  `m122_level` tinyint(4) DEFAULT 0,
	  `m123_level` tinyint(4) DEFAULT 0,
	  `m131_level` tinyint(4) DEFAULT 0,
	  `m132_level` tinyint(4) DEFAULT 0,
	  `m133_level` tinyint(4) DEFAULT 0,
	  `p1_level` tinyint(4) DEFAULT 0,
	  `p11_level` tinyint(4) DEFAULT 0,
	  `p12_level` tinyint(4) DEFAULT 0,
	  `p13_level` tinyint(4) DEFAULT 0,
	  `p111_level` tinyint(4) DEFAULT 0,
	  `p112_level` tinyint(4) DEFAULT 0,
	  `p113_level` tinyint(4) DEFAULT 0,
	  `p121_level` tinyint(4) DEFAULT 0,
	  `p122_level` tinyint(4) DEFAULT 0,
	  `p123_level` tinyint(4) DEFAULT 0,
	  `p131_level` tinyint(4) DEFAULT 0,
	  `p132_level` tinyint(4) DEFAULT 0,
	  `p133_level` tinyint(4) DEFAULT 0,
	  `g1_level` tinyint(4) DEFAULT 0,
	  `g11_level` tinyint(4) DEFAULT 0,
	  `g12_level` tinyint(4) DEFAULT 0,
	  `g13_level` tinyint(4) DEFAULT 0,
	  `g111_level` tinyint(4) DEFAULT 0,
	  `g112_level` tinyint(4) DEFAULT 0,
	  `g113_level` tinyint(4) DEFAULT 0,
	  `g121_level` tinyint(4) DEFAULT 0,
	  `g122_level` tinyint(4) DEFAULT 0,
	  `g123_level` tinyint(4) DEFAULT 0,
	  `g131_level` tinyint(4) DEFAULT 0,
	  `g132_level` tinyint(4) DEFAULT 0,
	  `g133_level` tinyint(4) DEFAULT 0,
	  PRIMARY KEY (`unique_id`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
	"""
	cursor.execute(statement)

def create_table_weapon(cursor):
	statement = \
	"""
	CREATE TABLE `weapon` (
	  `unique_id` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家唯一标识',
	  `weapon_name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '武器名字',
	  `weapon_star` smallint(6) DEFAULT 0 COMMENT '武器星数',
	  `weapon_level` smallint(6) DEFAULT 0 COMMENT '武器等级',
	  `passive_skill_1_level` smallint(6) DEFAULT 0 COMMENT '武器技能1',
	  `passive_skill_2_level` smallint(6) DEFAULT 0 COMMENT '武器技能2',
	  `passive_skill_3_level` smallint(6) DEFAULT 0 COMMENT '武器技能3',
	  `passive_skill_4_level` smallint(6) DEFAULT 0 COMMENT '武器技能4',
	  `skill_point` smallint(6) DEFAULT 0 COMMENT '武器技能点',
	  `segment` smallint(6) DEFAULT 0 COMMENT '武器碎片',
	  PRIMARY KEY (`unique_id`,`weapon_name`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
	"""
	cursor.execute(statement)
def creat_table_task(cursor):
	"""
		login:0,            check_in:1,     level_up_role:2,    level_up_weapon:3,      pass_stage:4,           pass_tower:5
		pass_world_boss:6,  basic_summon:7, pro_summon:8,       get_factory_resource:9, send_friend_gift:10,    check_in_family:11
	"""
	statement = \
	"""
	CREATE TABLE `task` (
	  `unique_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家唯一标识',
	  `task_id` smallint(6) NOT NULL COMMENT '表示任务的数字编号',
	  `task_value` smallint(6) DEFAULT 0 COMMENT '表示任务是否完成0:false,1:true',
	  `task_reward` smallint(6) DEFAULT 0 COMMENT '表示奖励是否已经领取',
	  `timer` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '完成时间',
	  PRIMARY KEY (`unique_id`,`task_id`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
	"""
	cursor.execute(statement)
def create_achievement(cursor):
	statement = \
	"""
	CREATE TABLE `achievement` (
	  `unique_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'new_id',
	  `achievement_id` smallint(6) DEFAULT 0 COMMENT '表示成就的数字编号',
	  `achievement_value` smallint(6) DEFAULT 0 COMMENT '表示成就的次数',
	  `achievement_value_reward` smallint(6) DEFAULT 0 COMMENT '表示成就领取奖励的次数',
	  PRIMARY KEY (`unique_id`,`achievement_id`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
	"""
	cursor.execute(statement)
def create_check_in(cursor):
	statement = \
	"""
	CREATE TABLE `check_in` (
	  `unique_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '玩家唯一标识',
	  `date` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '签到日期',
	  `reward` smallint(6) DEFAULT 0 COMMENT '0：未领奖，1：已领奖',
	  PRIMARY KEY (`unique_id`, `date`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
	"""
	cursor.execute(statement)
def create_triggers_player(cursor):
	trigger1 = \
	"""
	CREATE TRIGGER `player_BEFORE_INSERT` BEFORE INSERT ON `player` FOR EACH ROW
	BEGIN
	INSERT INTO `skill` (unique_id) VALUES (new.unique_id);
	INSERT INTO `factory` (unique_id) VALUES (new.unique_id);
	INSERT INTO `dark_market` (unique_id) VALUES (new.unique_id);
	INSERT INTO `leader_board` (unique_id) VALUES (new.unique_id);
	END
	"""

	trigger2 = \
	"""
	CREATE TRIGGER `player_AFTER_DELETE` AFTER DELETE ON `player` FOR EACH ROW
	BEGIN
	DELETE FROM `armor` WHERE unique_id = OLD.unique_id;
	DELETE FROM `dark_market` WHERE unique_id = OLD.unique_id;
	DELETE FROM `factory` WHERE unique_id = OLD.unique_id;
	DELETE FROM `leader_board` WHERE unique_id = OLD.unique_id;
	DELETE FROM `role` WHERE unique_id = OLD.unique_id;
	DELETE FROM `skill` WHERE unique_id = OLD.unique_id;
	DELETE FROM `weapon` WHERE unique_id = OLD.unique_id;
	DELETE FROM `friend` WHERE unique_id = OLD.unique_id;
	DELETE FROM `friend` WHERE friend_id = OLD.unique_id;
	DELETE FROM `families` WHERE familyid = OLD.game_name;
	END
	"""
	cursor.execute(trigger1)
	cursor.execute(trigger2)

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

def already_exists(world):
	try:
		pymysql.connect(host = '192.168.1.102', user = 'root', password = 'lukseun', charset = 'utf8mb4', db = world)
	except pymysql.err.InternalError as e:
		code, msg = e.args
		if code == 1049: return False
	return True

def operating_test():
	c = pymysql.connect(host='192.168.1.102', user='root', password='lukseun', charset='utf8mb4', autocommit=True)
	c.select_db("aliya")
	cursor = c.cursor()
	# creat_table_task(cursor)
	# create_achievement(cursor)
	# create_table_union_store(cursor)
	# create_check_in(cursor)
	create_table_player(cursor)
	# create_table_families(cursor)


if __name__ == '__main__':
	operating_test()
	# world = input('Enter world name: ')
	# if not already_exists(world):
	# 	create_world(world)
	# else:
	# 	print('world database already exists, skipping...')
	# create_mailbox(world)
