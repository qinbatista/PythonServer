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


