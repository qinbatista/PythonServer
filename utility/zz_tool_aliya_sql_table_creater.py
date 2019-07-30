"""
    创建数据库用户表，技能表，卷轴表
    SELECT CONCAT( 'DROP TABLE ', GROUP_CONCAT(table_name) , ';' ) AS statement FROM information_schema.tables WHERE table_schema = 'aliya' AND table_name LIKE '%';
"""

import json
import os
import pymysql  # 数据库连接
from DBUtils.PooledDB import PooledDB  # 用于数据库连接池


def PythonLocation():
    return os.path.dirname(os.path.realpath(__file__))


JSON_NAME = PythonLocation() + "/Configuration/mysql_data_config.json"


# 建立数据库连接池
POOL = PooledDB(
    pymysql, 5,  # 5为连接池里的最少连接数
    # host="127.0.0.1",
    host="192.168.1.102",
    user="root",
    passwd="lukseun",
    db="aliya",
    port=3306,
    setsession=["SET AUTOCOMMIT = 1"]  # 设置线程池是否打开自动更新的配置，0为False，1为True
)


def json_operating(table_name: str, table_attribute: list) -> None:
    if not os.path.exists(JSON_NAME):
        data = {table_name: table_attribute}
    else:
        data = json.load(open(JSON_NAME, encoding="utf-8"))
        data.update({table_name: table_attribute})
    with open(JSON_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def sql_table_constructor(table_name: str, table_dict: dict) -> None:
    """
    mysql 表单构造器
    """
    db = POOL.connection()
    cursor = db.cursor()
    sql_str = "CREATE TABLE %s(" % table_name
    sql_str_end = ");"
    for key in table_dict.keys():
        sql_str += key + " " + table_dict[key] + ","
    sql_str = sql_str[:len(sql_str) - 1] + sql_str_end
    cursor.execute(sql_str)
    # db.commit()
    json_operating(table_name=table_name, table_attribute=list(table_dict.keys()))


def create_player_table() -> None:
    """
    创建玩家表
    """
    table_name = "player"
    table_dict = {
        "unique_id": "VARCHAR(128) NOT NULL PRIMARY KEY COMMENT '玩家唯一标识'",
        "game_name": "VARCHAR(64) NULL DEFAULT '' COMMENT '游戏名字'",
        "coin": "INT(11) NULL DEFAULT(0) COMMENT '金币'",
        "iron": "INT(11) NULL DEFAULT(0) COMMENT '铁'",
        "diamond": "INT(11) NULL DEFAULT(0) COMMENT '钻石'",
        "energy": "INT(11) NULL DEFAULT(0) COMMENT '能量'",
        "experience": "INT(11) NULL DEFAULT(0) COMMENT '玩家经验'",
        "level": "INT(11) NULL DEFAULT(0) COMMENT '玩家等级'",
        "role": "INT(11) NULL DEFAULT(0) COMMENT '角色'",
        "stage": "INT(11) NULL DEFAULT(0) COMMENT '关卡等级'",
        "tower_stage": "INT(11) NULL DEFAULT(0) COMMENT '塔的阶段'",
        "skill_scroll_10": "INT(11) NULL DEFAULT(0) COMMENT '低级卷轴'",
        "skill_scroll_30": "INT(11) NULL DEFAULT(0) COMMENT '中级卷轴'",
        "skill_scroll_100": "INT(11) NULL DEFAULT(0) COMMENT '高级卷轴'",
        "experience_potion": "INT(11) NULL DEFAULT(0) COMMENT '经验药水'",
        "small_energy_potion": "INT(11) NULL DEFAULT(0) COMMENT '小能量药水'",
        "recover_time": "VARCHAR(64) NULL DEFAULT '' COMMENT '恢复开始时间'",
        "hang_stage": "INT(6) NULL DEFAULT(0) COMMENT '挂机的关卡'",
        "hang_up_time": "VARCHAR(64) NULL DEFAULT '' COMMENT '挂机开始时间'",
        "basic_summon_scroll": "INT(11) NULL DEFAULT(0) COMMENT '低级召唤卷轴'",
        "pro_summon_scroll": "INT(11) NULL DEFAULT(0) COMMENT '高级召唤卷轴'",
        "friend_gift": "INT(11) NULL DEFAULT(0) COMMENT '朋友礼物'",
        "prophet_summon_scroll": "INT(11) NULL DEFAULT(0) COMMENT '先知召唤卷轴'",
        "fortune_wheel_ticket_basic": "INT(11) NULL DEFAULT(0) COMMENT '低级幸运循环票'",
        "fortune_wheel_ticket_pro": "INT(11) NULL DEFAULT(0) COMMENT '高级幸运循环票'"
    }
    sql_table_constructor(table_name=table_name, table_dict=table_dict)


def create_skill_table() -> None:
    """
    创建技能表
    """
    table_name = "skill"
    table_dict = {
        "unique_id": "VARCHAR(128) NOT NULL PRIMARY KEY COMMENT '玩家唯一标识'",
        "m1_level": "TINYINT NULL DEFAULT(0) COMMENT '魔法技能'",
        "m11_level": "TINYINT NULL DEFAULT(0) COMMENT '魔法技能'",
        "m12_level": "TINYINT NULL DEFAULT(0) COMMENT '魔法技能'",
        "m13_level": "TINYINT NULL DEFAULT(0) COMMENT '魔法技能'",
        "m111_level": "TINYINT NULL DEFAULT(0) COMMENT '魔法技能'",
        "m112_level": "TINYINT NULL DEFAULT(0) COMMENT '魔法技能'",
        "m113_level": "TINYINT NULL DEFAULT(0) COMMENT '魔法技能'",
        "m121_level": "TINYINT NULL DEFAULT(0) COMMENT '魔法技能'",
        "m122_level": "TINYINT NULL DEFAULT(0) COMMENT '魔法技能'",
        "m123_level": "TINYINT NULL DEFAULT(0) COMMENT '魔法技能'",
        "m131_level": "TINYINT NULL DEFAULT(0) COMMENT '魔法技能'",
        "m132_level": "TINYINT NULL DEFAULT(0) COMMENT '魔法技能'",
        "m133_level": "TINYINT NULL DEFAULT(0) COMMENT '魔法技能'",
        "p1_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "p11_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "p12_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "p13_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "p111_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "p112_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "p113_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "p121_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "p122_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "p123_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "p131_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "p132_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "p133_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "g1_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "g11_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "g12_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "g13_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "g111_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "g112_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "g113_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "g121_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "g122_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "g123_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "g131_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "g132_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'",
        "g133_level": "TINYINT NULL DEFAULT(0) COMMENT '技能'"
    }
    sql_table_constructor(table_name=table_name, table_dict=table_dict)


def create_weapon_table() -> None:
    """
    创建武器背包表以及武器信息表
    """
    table_name = "weapon_bag"
    table_dict = {"unique_id": "VARCHAR(128) NOT NULL PRIMARY KEY COMMENT '玩家唯一标识'"}
    weapon_dict = {
        "unique_id": "VARCHAR(128) NOT NULL PRIMARY KEY COMMENT '玩家唯一标识'",
        "weapon_level": "SMALLINT(6) NULL DEFAULT(0) COMMENT '武器等级'",
        "passive_skill_1_level": "SMALLINT(6) NULL DEFAULT(0) COMMENT '武器技能1'",
        "passive_skill_2_level": "SMALLINT(6) NULL DEFAULT(0) COMMENT '武器技能2'",
        "passive_skill_3_level": "SMALLINT(6) NULL DEFAULT(0) COMMENT '武器技能3'",
        "passive_skill_4_level": "SMALLINT(6) NULL DEFAULT(0) COMMENT '武器技能4'",
        "skill_point": "SMALLINT(6) NULL DEFAULT(0) COMMENT '武器技能点'",
        "segment": "SMALLINT(6) NULL DEFAULT(0) COMMENT '武器碎片'"
    }
    for i in range(1, 41):
        weapon_name = "weapon" + str(i)
        sql_table_constructor(table_name=weapon_name, table_dict=weapon_dict)  # 创建武器信息表
        table_dict.update({weapon_name: "SMALLINT(6) NULL DEFAULT(0) COMMENT '武器%s的星数'" % i})
    sql_table_constructor(table_name=table_name, table_dict=table_dict)  # 创建武器背包表


def create_role_table() -> None:
    """
    创建角色背包表以及角色信息表
    """
    table_name = "role_bag"
    table_dict = {"unique_id": "VARCHAR(128) NOT NULL PRIMARY KEY COMMENT '玩家唯一标识'"}
    weapon_dict = {
        "unique_id": "VARCHAR(128) NOT NULL PRIMARY KEY COMMENT '玩家唯一标识'",
        "weapon_level": "SMALLINT(6) NULL DEFAULT(0) COMMENT '角色等级'",
        "passive_skill_1_level": "SMALLINT(6) NULL DEFAULT(0) COMMENT '角色技能1'",
        "passive_skill_2_level": "SMALLINT(6) NULL DEFAULT(0) COMMENT '角色技能2'",
        "passive_skill_3_level": "SMALLINT(6) NULL DEFAULT(0) COMMENT '角色技能3'",
        "passive_skill_4_level": "SMALLINT(6) NULL DEFAULT(0) COMMENT '角色技能4'",
        "skill_point": "SMALLINT(6) NULL DEFAULT(0) COMMENT '角色技能点'",
        "segment": "SMALLINT(6) NULL DEFAULT(0) COMMENT '角色碎片'"
    }
    for i in range(1, 41):
        weapon_name = "role" + str(i)
        sql_table_constructor(table_name=weapon_name, table_dict=weapon_dict)  # 创建角色信息表
        table_dict.update({weapon_name: "SMALLINT(6) NULL DEFAULT(0) COMMENT '角色%s的星数'" % i})
    sql_table_constructor(table_name=table_name, table_dict=table_dict)  # 创建角色背包表


def create_user_table() -> None:
    """
    创建武器背包表以及武器信息表
    """
    table_name = "user_info"
    table_dict = {
        "unique_id": "VARCHAR(128) NOT NULL PRIMARY KEY COMMENT '玩家唯一标识'",
        "token": "VARCHAR(255) NULL DEFAULT '' COMMENT '用于服务器和客户端的交互'",
        "account": "VARCHAR(32) NULL DEFAULT '' COMMENT '用户账号'",
        "password": "VARCHAR(32) NULL DEFAULT '' COMMENT '用户密码'",
        "email": "VARCHAR(32) NULL DEFAULT '' COMMENT '用户邮件'",
        "phone_number": "VARCHAR(32) NULL DEFAULT '' COMMENT '用户电话'",
        "avatar": "MEDIUMBLOB NULL DEFAULT(0x0) COMMENT '用户头像'"
    }
    sql_table_constructor(table_name=table_name, table_dict=table_dict)  # 创建武器背包表


def create_dark_market_table() -> None:
    """
    创建武器背包表以及武器信息表
    """
    table_name = "dark_market"
    table_dict = {
        "unique_id": "VARCHAR(128) NOT NULL PRIMARY KEY COMMENT '玩家唯一标识'",
        "merchandise1": "VARCHAR(32) NULL DEFAULT '' COMMENT '黑市中展示可以买的材料1'",
        "merchandise1_quantity": "INT(6) NULL DEFAULT(0) COMMENT '黑市中展示可以买的材料1的数量'",
        "currency_type1": "VARCHAR(32) NULL DEFAULT '' COMMENT '材料1的价值(金币或者钻石)'",
        "currency_type1_price": "INT(6) NULL DEFAULT(0) COMMENT '材料1的价格'",

        "merchandise2": "VARCHAR(32) NULL DEFAULT '' COMMENT '黑市中展示可以买的材料2'",
        "merchandise2_quantity": "INT(6) NULL DEFAULT(0) COMMENT '黑市中展示可以买的材料2的数量'",
        "currency_type2": "VARCHAR(32) NULL DEFAULT '' COMMENT '材料2的价值(金币或者钻石)'",
        "currency_type2_price": "INT(6) NULL DEFAULT(0) COMMENT '材料2的价格'",

        "merchandise3": "VARCHAR(32) NULL DEFAULT '' COMMENT '黑市中展示可以买的材料3'",
        "merchandise3_quantity": "INT(6) NULL DEFAULT(0) COMMENT '黑市中展示可以买的材料3的数量'",
        "currency_type3": "VARCHAR(32) NULL DEFAULT '' COMMENT '材料3的价值(金币或者钻石)'",
        "currency_type3_price": "INT(6) NULL DEFAULT(0) COMMENT '材料3的价格'",

        "merchandise4": "VARCHAR(32) NULL DEFAULT '' COMMENT '黑市中展示可以买的材料4'",
        "merchandise4_quantity": "INT(6) NULL DEFAULT(0) COMMENT '黑市中展示可以买的材料4的数量'",
        "currency_type4": "VARCHAR(32) NULL DEFAULT '' COMMENT '材料4的价值(金币或者钻石)'",
        "currency_type4_price": "INT(6) NULL DEFAULT(0) COMMENT '材料4的价格'",

        "merchandise5": "VARCHAR(32) NULL DEFAULT '' COMMENT '黑市中展示可以买的材料5'",
        "merchandise5_quantity": "INT(6) NULL DEFAULT(0) COMMENT '黑市中展示可以买的材料5的数量'",
        "currency_type5": "VARCHAR(32) NULL DEFAULT '' COMMENT '材料5的价值(金币或者钻石)'",
        "currency_type5_price": "INT(6) NULL DEFAULT(0) COMMENT '材料5的价格'",

        "merchandise6": "VARCHAR(32) NULL DEFAULT '' COMMENT '黑市中展示可以买的材料6'",
        "merchandise6_quantity": "INT(6) NULL DEFAULT(0) COMMENT '黑市中展示可以买的材料6的数量'",
        "currency_type6": "VARCHAR(32) NULL DEFAULT '' COMMENT '材料6的价值(金币或者钻石)'",
        "currency_type6_price": "INT(6) NULL DEFAULT(0) COMMENT '材料6的价格'",

        "merchandise7": "VARCHAR(32) NULL DEFAULT '' COMMENT '黑市中展示可以买的材料7'",
        "merchandise7_quantity": "INT(6) NULL DEFAULT(0) COMMENT '黑市中展示可以买的材料7的数量'",
        "currency_type7": "VARCHAR(32) NULL DEFAULT '' COMMENT '材料7的价值(金币或者钻石)'",
        "currency_type7_price": "INT(6) NULL DEFAULT(0) COMMENT '材料7的价格'",

        "merchandise8": "VARCHAR(32) NULL DEFAULT '' COMMENT '黑市中展示可以买的材料8'",
        "merchandise8_quantity": "INT(6) NULL DEFAULT(0) COMMENT '黑市中展示可以买的材料8的数量'",
        "currency_type8": "VARCHAR(32) NULL DEFAULT '' COMMENT '材料8的价值(金币或者钻石)'",
        "currency_type8_price": "INT(6) NULL DEFAULT(0) COMMENT '材料8的价格'",

        "refresh_time": "VARCHAR(32) NULL DEFAULT '' COMMENT '刷新所有材料的刷新时间'",
        "refreshable_quantity": "INT(6) NULL DEFAULT(0) COMMENT '可以刷新所有材料的次数'"
    }
    sql_table_constructor(table_name=table_name, table_dict=table_dict)  # 创建武器背包表


def create_friend_list_table() -> None:
    """
    创建武器背包表以及武器信息表
    """
    table_name = "friend_list"
    table_dict = {
        "unique_id": "VARCHAR(128) NOT NULL PRIMARY KEY COMMENT '玩家唯一标识'",
    }
    for i in range(1, 31):
        data = {
            "friend_id" + str(i): "VARCHAR(128) NOT NULL DEFAULT '' COMMENT '朋友%s唯一标识'" % i,
            "friend_name" + str(i): "VARCHAR(32) NOT NULL DEFAULT '' COMMENT '朋友%s的名字'" % i,
            "friend_level" + str(i): "INT(6) NOT NULL DEFAULT(0) COMMENT '朋友%s的等级'" % i,
            "recovery_time" + str(i): "VARCHAR(32) NOT NULL DEFAULT '' COMMENT '朋友%s好感度恢复时间'" % i
        }
        table_dict.update(data)
    sql_table_constructor(table_name=table_name, table_dict=table_dict)  # 创建武器背包表


def update_avatar(table_name: str, unique_id: str, img_path: str):  # png
    """
    更新用户表中的头像
    """
    avatar = pymysql.Binary(open(img_path, "rb").read())
    db = POOL.connection()
    cursor = db.cursor()
    cursor.execute("UPDATE %s SET avatar=%s WHERE unique_id=%s;", (table_name, avatar, unique_id))
    db.commit()


def load_avatar(table_name:str, unique_id: str, img_path: str):
    """
    从数据库中下载头像
    """
    db = POOL.connection()
    cursor = db.cursor()
    cursor.execute("SELECT avatar From %s  WHERE unique_id = %s;", (table_name, unique_id))
    with open(img_path, "wb") as f:
        f.write(cursor.fetchone()[0])


if __name__ == '__main__':
    # 创建数据库表
    # create_player_table()
    # create_skill_table()
    # create_weapon_table()
    # create_role_table()
    # create_user_table()
    # create_dark_market_table()
    create_friend_list_table()
    # 下面关于头像的方法暂时没测试
    # update_avatar(table_name="user_info", unique_id="4", img_path="D:/FileDocument/零碎文件/avatar.png")
    # load_avatar(table_name="user_info", unique_id="4", img_path="D:/FileDocument/零碎文件/avatar2.png")