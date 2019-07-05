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
    host="localhost",
    user="root",
    passwd="lukseun",
    db="aliya",
    port=3306,
    setsession=["SET AUTOCOMMIT = 1"]  # 设置线程池是否打开自动更新的配置，0为False，1为True
)


def create_users_table() -> None:
    """
    创建用户表
    """
    table_name = "userinfo"
    table_attribute = ["unique_id", "account", "password", "token", "ip",
                       "user_name", "gender", "email","phone_number", "birth_day",
                       "last_time_login", "registration_time", "head_photo"]
    db = POOL.connection()
    cursor = db.cursor()
    user_sql = "CREATE TABLE " + table_name + """(
            %s VARCHAR(128) NOT NULL PRIMARY KEY,
            %s VARCHAR(128) NULL DEFAULT "",
            %s VARCHAR(128) NULL DEFAULT "",
            %s VARCHAR(255) NULL DEFAULT "",
            %s VARCHAR(16)  NULL DEFAULT "",
            
            %s VARCHAR(20)  NULL DEFAULT "",
            %s VARCHAR(10)  NULL DEFAULT "",
            %s VARCHAR(50)  NULL DEFAULT "",
            %s VARCHAR(20)  NULL DEFAULT "",
            %s VARCHAR(20)  NULL DEFAULT "",
            
            %s VARCHAR(20)  NULL DEFAULT "",
            %s VARCHAR(20)  NULL DEFAULT "",
            %s MEDIUMBLOB NULL DEFAULT(0x0)
        );""" % tuple(table_attribute)
    cursor.execute(user_sql)
    db.commit()
    json_operating(table_name=table_name, table_attribute=table_attribute)


def create_skill_table() -> None:
    """
    创建技能表
    """
    table_name = "skill"
    table_attribute = ["unique_id",
                       "m1_level", "m11_level", "m12_level", "m13_level",
                       "m111_level", "m112_level", "m113_level",
                       "m121_level", "m122_level", "m123_level",
                       "m131_level", "m132_level", "m133_level",

                       "p1_level", "p11_level", "p12_level", "p13_level",
                       "p111_level", "p112_level", "p113_level",
                       "p121_level", "p122_level", "p123_level",
                       "p131_level", "p132_level", "p133_level",

                       "g1_level", "g11_level", "g12_level", "g13_level",
                       "g111_level", "g112_level", "g113_level",
                       "g121_level", "g122_level", "g123_level",
                       "g131_level", "g132_level", "g133_level",
                       ]
    db = POOL.connection()
    cursor = db.cursor()
    skill_sql = "CREATE TABLE " + table_name + """(
            %s VARCHAR(50) NOT NULL DEFAULT 'new_id' PRIMARY KEY,
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),

            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),

            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0),
            %s TINYINT NULL DEFAULT(0)
        );""" % tuple(table_attribute)
    cursor.execute(skill_sql)
    db.commit()
    json_operating(table_name=table_name, table_attribute=table_attribute)


def create_bag_table() -> None:
    """
    武器列表
    """
    table_name = "bag"
    table_attribute = ["unique_id", "scroll_skill_10", "scroll_skill_30", "scroll_skill_100", "iron",
                       "diamonds", "experience_potion", "coin", "small_energy_potion"]
    db = POOL.connection()
    cursor = db.cursor()
    bag_sql = "CREATE TABLE " + table_name + """(
            %s VARCHAR(50) NOT NULL DEFAULT'new_id' PRIMARY KEY,
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0)
        );""" % tuple(table_attribute)
    cursor.execute(bag_sql)
    db.commit()
    json_operating(table_name=table_name, table_attribute=table_attribute)


def create_weapon_bag() -> None:
    """
    创建卷轴表
    """
    table_name = "weapon_bag"
    table_attribute = ["unique_id"]
    for i in range(1, 41):
        table_attribute.append("weapon" + str(i))

    db = POOL.connection()
    cursor = db.cursor()
    bag_sql = "CREATE TABLE " + table_name + """(
            %s VARCHAR(50) NOT NULL DEFAULT'new_id' PRIMARY KEY,
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),

            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),

            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),

            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0)
        );""" % tuple(table_attribute)
    cursor.execute(bag_sql)
    db.commit()
    json_operating(table_name=table_name, table_attribute=table_attribute)


def create_weapon_info() -> None:
    """
    武器n参数
    """
    for i in range(1, 41):
        table_name = "weapon" + str(i)
        table_attribute = ["unique_id", "weapon_level", "passive_skill_1_level",
                           "passive_skill_2_level", "passive_skill_3_level",
                           "passive_skill_4_level", "skill_point", "segment"]
        db = POOL.connection()
        cursor = db.cursor()
        bag_sql = "CREATE TABLE " + table_name + """(
                %s VARCHAR(50) NOT NULL DEFAULT'new_id' PRIMARY KEY,
                %s SMALLINT NULL DEFAULT(0),
                %s SMALLINT NULL DEFAULT(0),
                %s SMALLINT NULL DEFAULT(0),
                %s SMALLINT NULL DEFAULT(0),
                %s SMALLINT NULL DEFAULT(0),
                %s SMALLINT NULL DEFAULT(0),
                %s SMALLINT NULL DEFAULT(0)
            );""" % tuple(table_attribute)
        cursor.execute(bag_sql)
        db.commit()
        json_operating(table_name=table_name, table_attribute=table_attribute)


def create_user_info() -> None:
    """
    武器列表
    """
    table_name = "player_status"
    table_attribute = ["unique_id", "role_type", "level", "experience",
                       "stage_level", "energy"]
    db = POOL.connection()
    cursor = db.cursor()
    bag_sql = "CREATE TABLE " + table_name + """(
            %s VARCHAR(50) NOT NULL DEFAULT 'new_id' PRIMARY KEY,
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0),
            %s SMALLINT NULL DEFAULT(0)
        );""" % tuple(table_attribute)
    cursor.execute(bag_sql)
    db.commit()
    json_operating(table_name=table_name, table_attribute=table_attribute)


def update_avatar():
    """更新用户表中的头像"""
    # 读取图片文件
    img_name = "Screen.png"
    # img_path = "/Users/wankcn/Desktop/PythonCode/Test/data_table/test.png"
    try:
        with open(img_name, "rb") as f:  # 必须以二进制数据读取
            temp = f.read()
    except Exception as e:
        print(e)
    img = pymysql.Binary(temp)
    # 获取要更新的id
    id = "1"
    # 获取连接
    db = POOL.connection()
    cursor = db.cursor()
    sql = """
        UPDATE userinfo SET head_photo = %s WHERE unique_id = %s 
    """
    cursor.execute(sql, [img, id])
    db.commit()


def load_avatar():
    """
    从数据库中下载头像
    """
    save_img_name = "save.png"
    # save_img_path = "/Users/wankcn/Desktop/PythonCode/Test/data_table/test.png"
    db = POOL.connection()
    cursor = db.cursor()
    id = "1"  # 需要传入的unique_id
    sql = """
            SELECT head_photo From userinfo  WHERE unique_id = %s 
        """
    cursor.execute(sql, (id,))
    data = cursor.fetchone()[0]  # 获取图片的二进制信息
    # 把获取的图片写入
    with open(save_img_name, "wb") as f:
        f.write(data)


def json_operating(table_name: str, table_attribute: list) -> None:
    if not os.path.exists(JSON_NAME):
        data = {table_name: table_attribute}
    else:
        data = json.load(open(JSON_NAME, encoding="utf-8"))
        data.update({table_name: table_attribute})
    with open(JSON_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    # 创建数据库表
    create_users_table()
    create_skill_table()
    create_bag_table()
    create_weapon_bag()
    create_weapon_info()
    create_user_info()
    # 更新头像
    # update_avatar()
