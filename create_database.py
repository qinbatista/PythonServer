import pymysql

IP="localhost"
ACCOUNT = "root"
PASSWORD = "Lukseun123"
DATA_BASE_NAME ="LukseunStuffDataBase"
def create_datatable():
	global IP,ACCOUNT,PASSWORD,DATA_BASE_NAME
	db = pymysql.connect(IP, ACCOUNT, PASSWORD, DATA_BASE_NAME)
	# 使用 cursor() 方法创建一个游标对象 cursor
	cursor = db.cursor()
	# 使用 execute() 方法执行 SQL，如果表存在则删除
	cursor.execute("DROP TABLE IF EXISTS userinfo")
	cursor.execute("DROP TABLE IF EXISTS timeinfo")
	# 使用预处理语句创建新的用户信息表
	user_sql = """
			CREATE TABLE userinfo(
			count INT NOT NULL AUTO_INCREMENT PRIMARY KEY,   -- 自增长计数
			session VARCHAR(20) NOT NULL,                    -- 计算机地址 
			ip VARCHAR(16) NULL,                             -- 计算机ip地址
			user_name VARCHAR(20) NOT NULL,                  -- 用户姓名
			gender VARCHAR(10) NULL,                         -- 用户性别
			email VARCHAR(50) NULL,                          -- 用户邮箱
			phone_number VARCHAR(11) NULL                    -- 用户电话号码
			)"""
	cursor.execute(user_sql)
	# 创建新的签到时间记录表
	time_sql ="""
			CREATE TABLE timeinfo(
			session VARCHAR(20) NOT NULL PRIMARY KEY,        -- 计算机地址 
			check_in VARCHAR(16) NULL,                       -- 上班签到时间
			check_out VARCHAR(20) NULL,                      -- 下班打卡时间
			data_time VARCHAR(20) NULL                       -- 打卡当天日期
			)"""
	cursor.execute(time_sql)
	# 关闭数据库连接
	db.close()
def create_table():

	"""
	create database in mysql, use following command to create database, if we can use python command to do that, that will be best.
	CREATE DATABASE `LukseunStuffDataBase`;
	"""
if __name__ == "__main__":
	create_table()
	create_datatable()