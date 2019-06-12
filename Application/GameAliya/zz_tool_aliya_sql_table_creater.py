"""
    创建数据库用户表，技能表，卷轴表
"""

import os
import pymysql  # 数据库连接
from DBUtils.PooledDB import PooledDB  # 用于数据库连接池


def PythonLocation():
    return os.path.dirname(os.path.realpath(__file__))


# 建立数据库连接池
POOL = PooledDB(
    pymysql, 5,  # 5为连接池里的最少连接数
    host='localhost',
    user='root',
    passwd='lukseun',
    db='aliya',
    port=3306,
    setsession=['SET AUTOCOMMIT = 1']  # 设置线程池是否打开自动更新的配置，0为False，1为True
)


def create_users_table():
    """
    创建用户表
    :return:
    """
    db = POOL.connection()
    cursor = db.cursor()
    user_sql = """
		CREATE TABLE userinfo(
			count INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
			account VARCHAR(128)          NULL DEFAULT "",
			password VARCHAR(128)         NULL DEFAULT "",
			unique_id VARCHAR(128)        NULL DEFAULT "",
			session  VARCHAR(128)         NULL DEFAULT "",
			ip VARCHAR(16)                NULL DEFAULT "",
			user_name VARCHAR(20)         NULL DEFAULT "",
			gender VARCHAR(10)            NULL DEFAULT "",
			email VARCHAR(50)             NULL DEFAULT "",
			phone_number VARCHAR(20)      NULL DEFAULT "",
			birth_day VARCHAR(20)         NULL DEFAULT "",
			last_time_login VARCHAR(20)   NULL DEFAULT "",
			registration_time VARCHAR(20) NULL DEFAULT "",
			head_photo MEDIUMBLOB         NULL DEFAULT(0x0) # 图片为二进制数据
		)
	"""
    cursor.execute(user_sql)
    db.commit()


def create_skill_table():
    """
    创建技能表
    :return:
    """
    db = POOL.connection()
    cursor = db.cursor()
    skill_sql = """
		CREATE TABLE skill(
            unique_id VARCHAR(50) NOT NULL DEFAULT'new_id' PRIMARY KEY,
            m1_level   TINYINT NULL DEFAULT(0),
            m11_level  TINYINT NULL DEFAULT(0),
            m12_level  TINYINT NULL DEFAULT(0),
            m13_level  TINYINT NULL DEFAULT(0),
            m111_level TINYINT NULL DEFAULT(0),
            m112_level TINYINT NULL DEFAULT(0),
            m113_level TINYINT NULL DEFAULT(0),
            m121_level TINYINT NULL DEFAULT(0),
            m122_level TINYINT NULL DEFAULT(0),
            m123_level TINYINT NULL DEFAULT(0),
            m131_level TINYINT NULL DEFAULT(0),
            m132_level TINYINT NULL DEFAULT(0),
            m133_level TINYINT NULL DEFAULT(0),
            p1_level   TINYINT NULL DEFAULT(0),
            p11_level  TINYINT NULL DEFAULT(0),
            p12_level  TINYINT NULL DEFAULT(0),
            p13_level  TINYINT NULL DEFAULT(0),
            p111_level TINYINT NULL DEFAULT(0),
            p112_level TINYINT NULL DEFAULT(0),
            p113_level TINYINT NULL DEFAULT(0),
            p121_level TINYINT NULL DEFAULT(0),
            p122_level TINYINT NULL DEFAULT(0),
            p123_level TINYINT NULL DEFAULT(0),
            p131_level TINYINT NULL DEFAULT(0),
            p132_level TINYINT NULL DEFAULT(0),
            p133_level TINYINT NULL DEFAULT(0),
            g1_level   TINYINT NULL DEFAULT(0),
            g11_level  TINYINT NULL DEFAULT(0),
            g12_level  TINYINT NULL DEFAULT(0),
            g13_level  TINYINT NULL DEFAULT(0),
            g111_level TINYINT NULL DEFAULT(0),
            g112_level TINYINT NULL DEFAULT(0),
            g113_level TINYINT NULL DEFAULT(0),
            g121_level TINYINT NULL DEFAULT(0),
            g122_level TINYINT NULL DEFAULT(0),
            g123_level TINYINT NULL DEFAULT(0),
            g131_level TINYINT NULL DEFAULT(0),
            g132_level TINYINT NULL DEFAULT(0),
            g133_level TINYINT NULL DEFAULT(0)
	   	)
	"""
    cursor.execute(skill_sql)
    db.commit()


def create_bag_table():
    """
    创建卷轴表
    :return:
    """
    db = POOL.connection()
    cursor = db.cursor()
    bag_sql = """
        CREATE TABLE bag(
	        unique_id VARCHAR(50) NOT NULL DEFAULT'new_id' PRIMARY KEY,
	        scroll_skill_10  SMALLINT NULL DEFAULT(0),
	        scroll_skill_30  SMALLINT NULL DEFAULT(0),
	        scroll_skill_100 SMALLINT NULL DEFAULT(0),
	        iron     SMALLINT NULL DEFAULT(0),
	        weapon1  SMALLINT NULL DEFAULT(0),
	        weapon2  SMALLINT NULL DEFAULT(0),
	        weapon3  SMALLINT NULL DEFAULT(0),
	        weapon4  SMALLINT NULL DEFAULT(0),
	        weapon5  SMALLINT NULL DEFAULT(0),
	        weapon6  SMALLINT NULL DEFAULT(0),
	        diamonds SMALLINT NULL DEFAULT(0),
	        coin     SMALLINT NULL DEFAULT(0)
        )
    """
    cursor.execute(bag_sql)
    db.commit()


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
    :return:
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


if __name__ == '__main__':
    # 创建数据库表
    create_users_table()
    create_skill_table()
    create_bag_table()

    # 更新头像
    # update_avatar()