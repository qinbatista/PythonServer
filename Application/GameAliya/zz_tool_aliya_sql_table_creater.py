import os
import pymysql
def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
IP = "localhost"
ACCOUNT="root"
PASSWROD="lukseun"
DATABASE = "aliya"
def create_users_table():
	db = pymysql.connect(IP, ACCOUNT, PASSWROD, DATABASE)
	cursor = db.cursor()
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
			birth_day VARCHAR(20) NULL,
			last_time_login VARCHAR(20) NULL,
			registration_time VARCHAR(20) NULL
			)"""
	cursor.execute(user_sql)
	add_sql ="ALTER TABLE userinfo " \
			"ADD head_photo MEDIUMBLOB NULL;"
	cursor.execute(add_sql)
	db.commit()
def create_skill_table():
	db = pymysql.connect(IP, ACCOUNT, PASSWROD, DATABASE)
	cursor = db.cursor()
	user_sql = """
			CREATE TABLE skill(
			unique_id VARCHAR(128) NOT NULL AUTO_INCREMENT PRIMARY KEY,
			m1_level VARCHAR(10) NULL,
			m11_level VARCHAR(10) NULL,
			m12_level VARCHAR(10) NULL,
			m13_level VARCHAR(10) NULL,
			m111_level VARCHAR(10) NULL,
			m112_level VARCHAR(10) NULL,
			m113_level VARCHAR(10) NULL,
			m121_level VARCHAR(10) NULL,
			m122_level VARCHAR(10) NULL,
			m123_level VARCHAR(10) NULL,
			m131_level VARCHAR(10) NULL,
			m132_level VARCHAR(10) NULL,
			m133_level VARCHAR(10) NULL,
			p1_level VARCHAR(10) NULL,
			p11_level VARCHAR(10) NULL,
			p12_level VARCHAR(10) NULL,
			p13_level VARCHAR(10) NULL,
			p111_level VARCHAR(10) NULL,
			p112_level VARCHAR(10) NULL,
			p113_level VARCHAR(10) NULL,
			p121_level VARCHAR(10) NULL,
			p122_level VARCHAR(10) NULL,
			p123_level VARCHAR(10) NULL,
			p131_level VARCHAR(10) NULL,
			p132_level VARCHAR(10) NULL,
			p133_level VARCHAR(10) NULL,
			g1_level VARCHAR(10) NULL,
			g11_level VARCHAR(10) NULL,
			g12_level VARCHAR(10) NULL,
			g13_level VARCHAR(10) NULL,
			g111_level VARCHAR(10) NULL,
			g112_level VARCHAR(10) NULL,
			g113_level VARCHAR(10) NULL,
			g121_level VARCHAR(10) NULL,
			g122_level VARCHAR(10) NULL,
			g123_level VARCHAR(10) NULL,
			g131_level VARCHAR(10) NULL,
			g132_level VARCHAR(10) NULL,
			g133_level VARCHAR(10) NULL
			)"""
	cursor.execute(user_sql)
	db.commit()
def create_bag_table():
	db = pymysql.connect(IP, ACCOUNT, PASSWROD, DATABASE)
	cursor = db.cursor()
	user_sql = """
	CREATE TABLE scorll_bag(
		unique_id VARCHAR(50) NOT NULL PRIMARY KEY,
	scroll1 SMALLINT NULL,
	scroll2 SMALLINT NULL,
	scroll3 SMALLINT NULL,
	iron SMALLINT NULL,
	weapon1 SMALLINT NULL,
	weapon2 SMALLINT NULL,
	weapon3 SMALLINT NULL,
	weapon4 SMALLINT NULL,
	weapon5 SMALLINT NULL,
	weapon6 SMALLINT NULL,
	diamonds SMALLINT NULL,
	coin SMALLINT NULL
	)
	"""
	cursor.execute(user_sql)
	db.commit()
if __name__ == "__main__":
	create_users_table()
	create_skill_table()