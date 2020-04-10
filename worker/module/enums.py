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
    EXP_POINT = 9  # 经验点，用于角色升级
    ENERGY_POTION_S = 10  # 能量瓶 暂未使用
    SUMMON_SCROLL_BASIC = 11  # 暂未使用
    SUMMON_SCROLL_PRO = 12  # 暂未使用
    SUMMON_SCROLL_PROPHET = 13  # 暂未使用
    FORTUNE_WHEEL_BASIC = 14  # 暂未使用
    FORTUNE_WHEEL_PRO = 15  # 暂未使用
    FRIEND_GIFT = 16
    UNIVERSAL_SEGMENT = 17  # 万能碎片  暂未使用
    COIN_CARD = 18
    EXP_CARD = 19
    FOOD_CARD = 20
    MINE_CARD = 21  # 暂未使用
    CRYSTAL_CARD = 22
    DIAMOND_CARD = 23
    MINE = 24  # 暂未使用，被IRON代替
    SMALL_ENERGY_POTION = 25  # 暂未使用
    VIP_CARD_MIN = 26
    VIP_CARD_MAX = 27
    VIP_CARD_PERPETUAL = 28
    WEAPON5_UNIVERSAL_SEGMENT = 29  # 5星武器万能碎片
    ROLE5_UNIVERSAL_SEGMENT = 30  # 5星角色万能碎片
    WEAPON6_UNIVERSAL_SEGMENT = 31  # 6星武器万能碎片
    ROLE6_UNIVERSAL_SEGMENT = 32  # 6星角色万能碎片
    ENERGY_POTION_S_MIN = 33  # 小能量瓶
    ENERGY_POTION_S_MAX = 34  # 大能量瓶
    FAMILY_CONTRIBUTE = 35  # 玩家家族贡献值
    FAMILY_COIN = 36
    FAMILY_COIN_RECORD = 37
    WEAPON4_UNIVERSAL_SEGMENT = 38  # 4星武器万能碎片
    ROLE4_UNIVERSAL_SEGMENT = 39  # 4星角色万能碎片
    UNIVERSAL4_SEGMENT = 40  # 4星万能碎片
    UNIVERSAL5_SEGMENT = 41  # 5星万能碎片
    UNIVERSAL6_SEGMENT = 42  # 6星万能碎片
    VIP_EXP_CARD = 43  # VIP经验卡兑换可获得50VIP经验
    INTEGRAL = 44  # 抽奖获得积分，积分兑换角色碎片
    SUMMON_SCROLL_D = 45  # 高级代抽券，存在时优先消耗，用于钻石抽奖
    SUMMON_SCROLL_C = 46  # 低级代抽券，存在时优先消耗，用于金币抽奖


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


class MailTemplate(enum.Enum):
    FAMILY_REQUEST = enum.auto()
    FAMILY_INVITATION = enum.auto()
    SYSTEM_REWARD = enum.auto()
    FRIEND_GIFT = enum.auto()
    COMPENSATE = enum.auto()
    SETTLEMENT = enum.auto()
    GIFT_1 = enum.auto()
    GIFT_2 = enum.auto()


class FamilyHistoryKeys(enum.Enum):
    ICON           = 'fm_5'
    ROLE           = 'fm_6'
    LEAVE          = 'fm_0'
    REMOVE         = 'fm_1'
    INVITE         = 'fm_2'
    RESPOND        = 'fm_3'
    DISBAND        = 'fm_8'
    PURCHASE       = 'fm_4'
    ABDICATE       = 'fm_10'
    CHANGE_NAME    = 'fm_7'
    CANCEL_DISBAND = 'fm_9'


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


class Stage(enum.IntEnum):
    """关卡模式"""
    GENERAL = 0  # 普通模式
    ENDLESS = 1  # 无尽模式
    BOSS = 3  # 世界BOSS模式
    COIN = 4  # 金币挑战模式
    EXP = 5  # 经验挑战模式


class Element(enum.IntEnum):
    """玩家技能元素"""
    FLAME = 1000  # 火
    THUNDER = 1001  # 雷
    FREEZE = 1002  # 冰
    TOXIN = 1003  # 毒


class Weapon(enum.IntEnum):
    W101 = 101
    W102 = 102
    W103 = 103
    W104 = 104
    W105 = 105
    W106 = 106
    W107 = 107
    W108 = 108
    W109 = 109
    W110 = 110
    W201 = 201
    W202 = 202
    W203 = 203
    W204 = 204
    W205 = 205
    W206 = 206
    W207 = 207
    W208 = 208
    W209 = 209
    W210 = 210
    W301 = 301
    W302 = 302
    W303 = 303
    W304 = 304
    W305 = 305
    W306 = 306
    W307 = 307
    W308 = 308
    W309 = 309
    W310 = 310
    W401 = 401
    W402 = 402
    W403 = 403
    W404 = 404
    W405 = 405
    W406 = 406
    W407 = 407
    W408 = 408
    W409 = 409
    W410 = 410
    W501 = 501
    W502 = 502
    W503 = 503
    W504 = 504
    W505 = 505
    W506 = 506
    W507 = 507
    W508 = 508
    W509 = 509
    W510 = 510
    W601 = 601
    W602 = 602
    W603 = 603
    W604 = 604
    W605 = 605
    W606 = 606
    W607 = 607
    W608 = 608
    W609 = 609
    W610 = 610


class WeaponPassive(enum.IntEnum):
    P1 = 1
    P2 = 2
    P3 = 3
    P4 = 4


class Skill(enum.IntEnum):
    S1 = 1
    S2 = 2
    S3 = 3
    S4 = 4
    S5 = 5
    S6 = 6
    S7 = 7
    S8 = 8
    S9 = 9
    S10 = 10
    S11 = 11
    S12 = 12
    S13 = 13
    S14 = 14
    S15 = 15
    S16 = 16
    S17 = 17
    S18 = 18
    S19 = 19
    S20 = 20
    S21 = 21
    S22 = 22
    S23 = 23
    S24 = 24
    S25 = 25
    S26 = 26
    S27 = 27
    S28 = 28
    S29 = 29
    S30 = 30
    S31 = 31
    S32 = 32
    S33 = 33
    S34 = 34
    S35 = 35
    S36 = 36
    S37 = 37
    S38 = 38
    S39 = 39
    S40 = 40


class Role(enum.IntEnum):
    R101 = 101
    R102 = 102
    R103 = 103
    R104 = 104
    R105 = 105
    R106 = 106
    R107 = 107
    R108 = 108
    R109 = 109
    R110 = 110
    R201 = 201
    R202 = 202
    R203 = 203
    R204 = 204
    R205 = 205
    R206 = 206
    R207 = 207
    R208 = 208
    R209 = 209
    R210 = 210
    R301 = 301
    R302 = 302
    R303 = 303
    R304 = 304
    R305 = 305
    R306 = 306
    R307 = 307
    R308 = 308
    R309 = 309
    R310 = 310
    R401 = 401
    R402 = 402
    R403 = 403
    R404 = 404
    R405 = 405
    R406 = 406
    R407 = 407
    R408 = 408
    R409 = 409
    R410 = 410
    R501 = 501
    R502 = 502
    R503 = 503
    R504 = 504
    R505 = 505
    R506 = 506
    R507 = 507
    R508 = 508
    R509 = 509
    R510 = 510
    R601 = 601
    R602 = 602
    R603 = 603
    R604 = 604
    R605 = 605
    R606 = 606
    R607 = 607
    R608 = 608
    R609 = 609
    R610 = 610


class RolePassive(enum.IntEnum):
    """P101-P199为维度被动技能范围
    P201-P299未定"""
    P101 = 101
    P102 = 102
    P103 = 103
    P104 = 104
    P105 = 105
    P106 = 106
    P107 = 107
    P108 = 108
    P109 = 109
    P110 = 110


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
    T11 = 11


class Timer(enum.IntEnum):
    HANG_UP_TIME = 1
    DAILY_REWARD_TIME = 2
    TASK_TIME = 3
    ADD_FRIENDS_TIME = 4
    DARK_MARKET_TIME = 5
    WORLD_BOSS_CHALLENGE_TIME = 6
    FAMILY_CHECK_IN = 7
    FAMILY_REMOVE_USER_TIME = 8
    FAMILY_DISBAND = 9
    FAMILY_LEAVE_TIME = 10
    ENERGY_RECOVER_TIME = 11
    LOGIN_TIME = 12
    FACTORY_REFRESH = 13
    FACTORY_ACCELERATION_START = 14
    FACTORY_ACCELERATION_END = 15
    FACTORY_WISHING_POOL = 16
    VIP_MIN_END_TIME = 17  # VIP小月卡结束时间
    VIP_MAX_END_TIME = 18  # VIP大月卡结束时间
    REQUEST_FRIEND_TIME = 19
    VIP_COOLING_TIME = 20  # VIP礼包领取冷却结束时间
    CONTINUOUS_LOGIN = 21
    MAIL_LAST_SENT = 22  # last time user sent SIMPLE mail to another player
    FAMILY_JOIN_END = 23  # 玩家退出工会后可以再次加入工会的结束时间
    FAMILY_NOTICE_END = 24  # 管理员发布公告后刷新公告发布次数的剩余时间
    FAMILY_INVITE_END = 25  # 管理员邀请成员后刷新邀请成员次数的剩余时间
    BIND_PHONE_END = 26  # 用户绑定手机次数刷新的结束时间
    SUMMON_D_END = 27  # 刷新钻石随机商城的结束时间
    SUMMON_C_END = 28  # 刷新金币随机商城的结束时间
    SUMMON_G_END = 29  # 刷新朋友礼物随机商城的结束时间
    INTEGRAL = 30  # 代表本周的某一天刷新时间，这里用作和某一天判断是否为同一周
    SUMMON_C = 31  # 记录金币抽奖次数刷新的开始日期，用于重置金币抽奖次数
    SUMMON_D = 32  # 记录钻石抽奖次数刷新的开始日期，用于重置钻石抽奖次数，这里用于限制钻石免费抽和半价抽
    SUMMON_C_REFRESH = 33  # 记录金币抽奖免费刷新的日期
    SUMMON_D_REFRESH = 34  # 记录钻石抽奖免费刷新的日期
    SUMMON_G_REFRESH = 35  # 记录爱心抽奖免费刷新的日期
    FAMILY_JOIN = 36  # 玩家当天可发送加入工会邮件的结束时间
    DT_ENERGY = 37  # 钻石购买体力的刷新时间
    STAGE_WORLD_BOSS = 38  # 世界BOSS下次刷新时间
    STAGE_COIN = 39  # 金币挑战模式下的挑战时间限制，时间满足则刷新可挑战次数和可购买挑战的次数
    STAGE_EXP = 40  # 经验挑战模式下的挑战时间限制，时间满足则刷新可挑战次数和可购买挑战的次数
    STAGE_HANG_UP = 41  # 挂机模式的开始时间


class Limits(enum.IntEnum):
    DARK_MARKET_LIMITS = 1
    ADD_FRIENDS_LIMITS = 2
    WORLD_BOSS_CHALLENGE_LIMITS = 3
    FAMILY_REMOVE_USER_LIMITS = 4
    FACTORY_WISHING_POOL = 5
    REQUEST_FRIEND_LIMITS = 6
    BUY_ENERGY_LIMITS = 7  # 购买体力上限次数键
    BUY_STAGE_LIMITS = 8  # 购买副本上限次数键
    MAIL_DAILY_SEND = 9
    FAMILY_NOTICE = 10  # 管理员可以发布公告的剩余次数
    FAMILY_INVITE = 11  # 管理员可以邀请成员的剩余次数
    BIND_PHONE = 12  # 用户绑定手机的剩余次数
    INTEGRAL = 13  # 代表获取了的阶段积分数值，大于此值时则获取
    SUMMON_C = 14  # 代表金币抽每天限制的次数，一天限制12次
    SUMMON_D = 15  # 代表钻石抽每天限制的次数，当天第一次抽奖免费，第二次抽奖半价，这里用于限制钻石免费抽和半价抽
    FAMILY_JOIN = 16  # 玩家当天可发送加入工会邮件的次数
    DT_ENERGY = 17  # 钻石购买体力的限制次数
    STAGE_WORLD_BOSS = 18  # 世界BOSS记录次数
    STAGE_COIN = 19  # 金币挑战模式下的挑战次数限制
    STAGE_COIN_VIP = 20  # 金币挑战模式下VIP相应等级可购买的挑战次数限制
    STAGE_EXP = 21  # 经验挑战模式下的挑战次数限制
    STAGE_EXP_VIP = 22  # 经验挑战模式下VIP相应等级可购买的挑战次数限制
    PLAYER_ELEMENT = 23  # 玩家可以清洗元素技能的剩余次数，不可重置


class Achievement(enum.IntEnum):
    TOTAL_LOGIN = 1  # 总登陆天数
    KEEPING_LOGIN = 2  # 保持登陆天数
    LV_VIP = 3
    GET_4R = 4
    GET_5R = 5
    GET_6R = 6
    LV_UPR = 7
    GET_4W = 8
    GET_5W = 9
    GET_6W = 10
    LV_UPW = 11
    SUMMON_C = 12  # 金币兑换券成就没有使用
    SUMMON_D = 13
    SUMMON_3W = 14
    SUMMON_4W = 15
    SUMMON_5W = 16
    SUMMON_3R = 17
    SUMMON_4R = 18
    SUMMON_5R = 19
    PASS_STAGE = 20
    COLLECT_FOOD = 21
    COLLECT_MINE = 22
    COLLECT_CRYSTAL = 23
    UPGRADE_FOOD = 24
    UPGRADE_MINE = 25
    UPGRADE_CRYSTAL = 26
    FRIEND_REQUEST = 27
    FRIEND_GIFT = 28
    FAMILY_CHECK_IN = 29


class Task(enum.IntEnum):
    LOGIN = 1  # 当天首次登陆
    CHECK_IN = 2  # 当天签到
    ROLE_LEVEL_UP = 3  # 角色升级
    WEAPON_LEVEL_UP = 4  # 武器升级
    PASS_MAIN_STAGE = 5  # 通过主线关卡
    PASS_SPECIAL_STAGE = 6  # 通关特殊关卡（未做）
    PASS_WORLD_BOSS = 7  #  通关BOSS关卡
    BASIC_SUMMONING = 8  # 完成金币抽奖
    PRO_SUMMONING = 9  # 完成钻石抽奖
    CHECK_FACTORY = 10  # 完成工厂资源增加
    SEND_FRIEND_GIFT = 11  # 完成发送好友礼物
    FAMILY_CHECK_IN = 12  # 完成家族签到
    DONE_10_TASK = 13  # 完成10个任务


class Factory(enum.IntEnum):
    WISHING_POOL = -2
    UNASSIGNED = -1  # 未分配工人的情况
    FOOD = 0
    IRON = 1
    CRYSTAL = 2
    ARMOR = 3


class LeaderBoard(enum.IntEnum):
    WORLD_BOSS = 1


class Science(enum.IntEnum):
    FACTORY = 1  # 工厂科技分支


class ScienceSub(enum.IntEnum):
    MASTER = 0
    ROLE = 1  # 角色科技
    WEAPON = 2  # 武器科技


class SSAffiliate(enum.IntEnum):
    NON = 0
    POR = 1  # 力量
    AGE = 2  # 敏捷
    SPT = 3  # 精神
    CON = 4  # 体质
    HIT = 5  # 命中率
    DOE = 6  # 闪避



