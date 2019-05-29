import os
import pymysql
def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
def create_database_table():
	db = pymysql.connect("localhost", "root", "lukseun", "aliya")
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
if __name__ == "__main__":
	create_database_table()