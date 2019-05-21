import os
import pymysql
def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
def create_database_table():
	db = pymysql.connect("localhost", "root", "FAeX9ftoXd%_", "staff")
	cursor = db.cursor()
	cursor.execute("DROP TABLE IF EXISTS userinfo")
	cursor.execute("DROP TABLE IF EXISTS timeinfo")
	# 使用预处理语句创建新的用户信息表
	user_sql = """
			CREATE TABLE userinfo(
			-- count INT NOT NULL AUTO_INCREMENT PRIMARY KEY,   -- 自增长计数
			session VARCHAR(128) NOT NULL PRIMARY KEY,        -- 计算机用户id
			ip VARCHAR(16) NULL,                             -- 计算机ip地址
			user_name VARCHAR(20) NULL,                      -- 用户姓名
			gender VARCHAR(10) NULL,                         -- 用户性别
			email VARCHAR(50) NULL,                          -- 用户邮箱
			phone_number VARCHAR(11) NULL                    -- 用户电话号码
			)"""
	cursor.execute(user_sql)
	# 创建新的签到时间记录表
	time_sql = """
			CREATE TABLE timeinfo(
			count INT NOT NULL AUTO_INCREMENT PRIMARY KEY,   -- 这里的计数应该是唯一的
			session VARCHAR(128)  NULL ,               -- 计算机用户id
			check_in VARCHAR(16) NULL,                       -- 上班签到时间
			check_out VARCHAR(20) NULL,                      -- 下班打卡时间
			data_time VARCHAR(20) NULL                       -- 打卡当天日期
			)"""
	cursor.execute(time_sql)
def get_required_packages():
	os.system("pip3 install -r "+PythonLocation()+"/requirements.txt")
	os.system("pip install -r "+PythonLocation()+"/requirements.txt")
	os.system("pip.exe install -r "+PythonLocation()+"/requirements.txt")
if __name__ == "__main__":
	get_required_packages()
	create_database_table()