import time
import os
import codecs
import threading
import pymysql
def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
def working_cat(sql_command):
	print("[sql_manager][working_cat]sql_command:"+sql_command)
	DATABASE_IP = "localhost"
	DATABASE_ACCOUNT = "root"
	DATABASE_PASSWORD = "lukseun"
	DATABASE_TABLE = "staff"
	db = pymysql.connect(DATABASE_IP, DATABASE_ACCOUNT, DATABASE_PASSWORD, DATABASE_TABLE)
	cursor = db.cursor()
	sql = sql_command
	cursor.execute(sql)
	db.commit()
	return cursor.fetchall()
if __name__ == "__main__":
	ss = working_cat("select session from userinfo where unique_id='ACDE48001122'")
	print(ss[0])