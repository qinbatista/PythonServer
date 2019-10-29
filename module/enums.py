'''
enums.py

Contains definitions of global enums.
'''

import enum


class Item(enum.IntEnum):
	COIN = 1
	IRON = 2
	FOOD = 3
	CRYSTAL = 4
	DIAMOND = 5
	SKILL_SCROLL_10 = 6
	SKILL_SCROLL_30 = 7
	SKILL_SCROLL_100 = 8
	EXPERIENCE_POTION = 9
	ENERGY_POTION_S = 10
	SUMMON_SCROLL_BASIC = 11
	SUMMON_SCROLL_PRO = 12
	SUMMON_SCROLL_PROPHET = 13
	FORTUNE_WHEEL_BASIC = 14
	FORTUNE_WHEEL_PRO = 15
	FRIEND_GIFT = 16
	UNIVERSAL_SEGMENT = 17
	COIN_CARD = 18
	EXP_CARD = 19
	FOOD_CARD = 20
	MINE_CARD = 21
	CRYSTAL_CARD = 22
	DIAMOND_CARD = 23
	MINE = 24
	SMALL_ENERGY_POTION = 25


class FamilyRole(enum.IntEnum):
	BASIC = 0
	ELITE = 4
	ADMIN = 8
	OWNER = 10


class MailType(enum.IntEnum):
	SIMPLE = 0
	GIFT = 1
	FRIEND_REQUEST = 2
	FAMILY_REQUEST = 3


class Tier(enum.IntEnum):
	BASIC = 0
	FRIEND = 1
	PRO = 2
	PROPHET = 3


class Group(enum.IntEnum):
	WEAPON = 0
	SKILL = 1
	ROLE = 2
	ITEM = 3
	ARMOR = 4


class Weapon(enum.IntEnum):
	W1 = 1
	W2 = 2
	W3 = 3
	W4 = 4
	W5 = 5
	W6 = 6
	W7 = 7
	W8 = 8
	W9 = 9
	W10 = 10
	W11 = 11
	W12 = 12
	W13 = 13
	W14 = 14
	W15 = 15
	W16 = 16
	W17 = 17
	W18 = 18
	W19 = 19
	W20 = 20
	W21 = 21
	W22 = 22
	W23 = 23
	W24 = 24
	W25 = 25
	W26 = 26
	W27 = 27
	W28 = 28
	W29 = 29
	W30 = 30
	W31 = 31
	W32 = 32
	W33 = 33
	W34 = 34
	W35 = 35
	W36 = 36
	W37 = 37
	W38 = 38
	W39 = 39
	W40 = 40


class WeaponPassive(enum.IntEnum):
	P1 = 1
	P2 = 2
	P3 = 3
	P4 = 4


class Skill(enum.IntEnum):
	M1 = 0
	M11 = 1
	M12 = 2
	M13 = 3
	M111 = 4
	M112 = 5
	M113 = 6
	M121 = 7
	M122 = 8
	M123 = 9
	M131 = 10
	M132 = 11
	M133 = 12
	P1 = 13
	P11 = 14
	P12 = 15
	P13 = 16
	P111 = 17
	P112 = 18
	P113 = 19
	P121 = 20
	P122 = 21
	P123 = 22
	P131 = 23
	P132 = 24
	P133 = 25
	G1 = 26
	G11 = 27
	G12 = 28
	G13 = 29
	G111 = 30
	G112 = 31
	G113 = 32
	G121 = 33
	G122 = 34
	G123 = 35
	G131 = 36
	G132 = 37
	G133 = 38


class Role(enum.IntEnum):
	R1 = 1
	R2 = 2
	R3 = 3
	R4 = 4
	R5 = 5
	R6 = 6
	R7 = 7
	R8 = 8
	R9 = 9
	R10 = 10
	R11 = 11
	R12 = 12
	R13 = 13
	R14 = 14
	R15 = 15
	R16 = 16
	R17 = 17
	R18 = 18
	R19 = 19
	R20 = 20
	R21 = 21
	R22 = 22
	R23 = 23
	R24 = 24
	R25 = 25
	R26 = 26
	R27 = 27
	R28 = 28
	R29 = 29
	R30 = 30
	R31 = 31
	R32 = 32
	R33 = 33
	R34 = 34
	R35 = 35
	R36 = 36
	R37 = 37
	R38 = 38
	R39 = 39
	R40 = 40

class Armor(enum.IntEnum):
	A1 = 1
	A2 = 2
	A3 = 3
	A4 = 4


class ArmorTier(enum.IntEnum):
	T1 = 1
	T2 = 2
	T3 = 3
	T4 = 4
	T5 = 5
	T6 = 6
	T7 = 7
	T8 = 8
	T9 = 9
	T10 = 10


class Timer(enum.IntEnum):
	HANG_UP_TIME = 1
	DAILY_REWARD_TIME = 2
	TASK_TIME = 3
	ADD_FRIENDS_TIME = 4
	DARK_MARKET_TIME = 5
	WORLD_BOSS_CHALLENGE_TIME = 6
	FAMILY_CHECK_IN_TIME = 7
	FAMILY_REMOVE_USER_TIME = 8
	FAMILY_DISBANDED_TIME = 9
	FAMILY_LEAVE_TIME = 10
	ENERGY_RECOVER_TIME = 11
	LOGIN_TIME = 12
	FACTORY_REFRESH = 13
	FACTORY_ACCELERATION_START = 14
	FACTORY_ACCELERATION_END = 15
	FACTORY_WISHING_POOL = 16
	FACTORY_EQUIPMENT = 17
	REQUEST_FRIEND_TIME = 19


class Limits(enum.IntEnum):
	DARK_MARKET_LIMITS = 1
	ADD_FRIENDS_LIMITS = 2
	WORLD_BOSS_CHALLENGE_LIMITS = 3
	FAMILY_REMOVE_USER_LIMITS = 4
	FACTORY_WISHING_POOL_COUNT = 5
	REQUEST_FRIEND_LIMITS = 6


class Achievement(enum.IntEnum):
	TOTAL_LOGIN = 1
	KEEPING_LOGIN = 2
	VIP_LEVEL = 3
	GET_4_STAR_ROLE = 4
	GET_5_STAR_ROLE = 5
	GET_6_STAR_ROLE = 6
	LEVEL_UP_ROLE = 7
	GET_4_STAR_WEAPON = 8
	GET_5_STAR_WEAPON = 9
	GET_6_STAR_WEAPON = 10
	LEVEL_UP_WEAPON = 11
	PASS_STAGE = 12
	COLLECT_FOOD = 13
	COLLECT_MINE = 14
	COLLECT_CRYSTAL = 15
	UPGRADE_FOOD_FACTORY = 16
	UPGRADE_MINE_FACTORY = 17
	UPGRADE_CRYSTAL_FACTORY = 18
	SUMMON_TIMES = 19
	SUMMON_3_STAR_WEAPON_TIMES = 20
	SUMMON_4_STAR_WEAPON_TIMES = 21
	SUMMON_5_STAR_WEAPON_TIMES = 22
	SUMMON_3_STAR_ROLE_TIMES = 23
	SUMMON_4_STAR_ROLE_TIMES = 24
	SUMMON_5_STAR_ROLE_TIMES = 25
	PRO_SUMMON_TIMES = 26
	FRIEND_REQUEST = 27
	FRIEND_GIFT = 28
	CHECK_IN_FAMILY = 29


class Progress(enum.IntEnum):
	STAGE = 0
	HANG_STAGE = 1
	TOWER_STAGE = 2
	ENERGY = 3

class Task(enum.IntEnum):
	LOGIN = 1
	CHECK_IN = 2
	ROLE_LEVEL_UP = 3
	WEAPON_LEVEL_UP = 4
	PASS_MAIN_STAGE = 5
	PASS_SPECIAL_STAGE = 6
	PASS_WORLD_BOSS = 7
	BASIC_SUMMONING = 8
	PRO_SUMMONING = 9
	CHECK_FACTORY = 10
	GET_FRIEND_GIFT = 11
	FAMILY_CHECK_IN = 12
	DONE_10_TASK = 13


class Factory(enum.IntEnum):
	EQUIPMENT = -3
	WISHING_POOL = -2
	UNASSIGNED = -1
	FOOD = 0
	IRON = 1
	CRYSTAL = 2
