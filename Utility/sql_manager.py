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
def game_aliya(sql_command):
	print("[sql_manager][game_aliya]sql_command:"+sql_command)
	DATABASE_IP = "localhost"
	DATABASE_ACCOUNT = "root"
	DATABASE_PASSWORD = "lukseun"
	DATABASE_TABLE = "aliya"
	db = pymysql.connect(DATABASE_IP, DATABASE_ACCOUNT, DATABASE_PASSWORD, DATABASE_TABLE)
	cursor = db.cursor()
	sql = sql_command
	cursor.execute(sql)
	db.commit()
	return cursor.fetchall()

def game_aliya_update(sql_command) -> int:
	print("[sql_manager][game_aliya_update] -> sql_command:"+sql_command)
	DATABASE_IP = "localhost"
	DATABASE_ACCOUNT = "root"
	DATABASE_PASSWORD = "lukseun"
	DATABASE_TABLE = "aliya"
	db = pymysql.connect(DATABASE_IP, DATABASE_ACCOUNT, DATABASE_PASSWORD, DATABASE_TABLE)
	cursor = db.cursor()
	sql = sql_command
	sql_value = cursor.execute(sql)
	db.commit()
	return sql_value

def game_aliya_table(sql_command):
	print("[sql_manager][game_aliya]sql_command:"+sql_command)
	DATABASE_IP = "localhost"
	DATABASE_ACCOUNT = "root"
	DATABASE_PASSWORD = "lukseun"
	DATABASE_TABLE = "aliya"
	db = pymysql.connect(DATABASE_IP, DATABASE_ACCOUNT, DATABASE_PASSWORD, DATABASE_TABLE)
	cursor = db.cursor()
	sql = sql_command
	cursor.execute(sql)
	db.commit()
	return cursor.description,cursor.fetchall()
if __name__ == "__main__":
	ss ,aa= game_aliya_table("select * from skill where unique_id='mac'")
	# print(ss[0][0])
	# print(ss[1][0])
	print(aa[0][0])
	print(aa[0][1])