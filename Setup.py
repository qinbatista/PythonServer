import os
import pymysql
def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
def create_database_table():
	db = pymysql.connect("localhost", "root", "lukseun", "staff")
	cursor = db.cursor()
	cursor.execute("DROP TABLE IF EXISTS userinfo")
	cursor.execute("DROP TABLE IF EXISTS timeinfo")
	# 使用预处理语句创建新的用户信息表
	user_sql = """
			CREATE TABLE userinfo(
			count INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
			account VARCHAR(128) NULL,
			password VARCHAR(128) NULL,
			unique_id VARCHAR(128)NULL,
			session  VARCHAR(128) NULL,
			ip VARCHAR(16) NULL,
			user_name VARCHAR(20) NULL,
			gender VARCHAR(10) NULL,
			email VARCHAR(50) NULL,
			phone_number VARCHAR(20) NULL,
			birth_day VARCHAR(20) NULL
			)"""
	cursor.execute(user_sql)
	# 创建新的签到时间记录表
	time_sql = """
			CREATE TABLE timeinfo(
			account VARCHAR(128) NULL,
			unique_id VARCHAR(128) NULL,
			check_in VARCHAR(16) NULL,
			check_out VARCHAR(20) NULL,
			data_time VARCHAR(20) NULL
			)"""
	cursor.execute(time_sql)
def get_required_packages():
	os.system("pip3 install -r "+PythonLocation()+"/requirements.txt")
	os.system("pip install -r "+PythonLocation()+"/requirements.txt")
	os.system("pip.exe install -r "+PythonLocation()+"/requirements.txt")
if __name__ == "__main__":
	get_required_packages()
	#create_database_table()