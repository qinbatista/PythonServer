import tool_lukseun_client
import module_1_login
import module_2_get_all_data
import module_3_friends
import module_4_skills
import module_5_weapons
import module_6_factory
import module_7_lottery
import module_8_roles
import module_9_family
import module_10_stage
import module_11_mail
import module_13_achievement
import module_14_vip
import module_15_summon
import multiprocessing
import time
import random
import pymysql
import asyncio
from datetime import datetime, timedelta
world = "0"
token = ""
testing_people_number = 20
lukseun = tool_lukseun_client.LukseunClient('aliya', port = 8880)
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))
def call_login(unique_id):
	global world,token
	while True:
		world = module_1_login.login_module(unique_id)
		if world!=None:
			token,world = world
			if token!="" and world!="":break

def _execute_statement(statement: str) -> tuple:
		db = pymysql.connect('192.168.1.102', 'root', 'lukseun', '0')
		cursor = db.cursor()
		cursor.execute(statement)
		db.commit()
unique_id=""
def run_task(name):
	global unique_id,token
	unique_id = name
	call_login(str(name))
	#mail_type: SIMPLE = 0,GIFT = 1, FRIEND_REQUEST = 2 FAMILY_REQUEST = 3
	#item_id: COIN = 1,IRON = 2,FOOD = 3,CRYSTAL = 4,DIAMOND = 5
	for i in range(0,10):
		send_tcp_message({'function' : 'send_gift_mail', 'data' : {"token":token, "gn_target":"去污", "group_id":3, "item_id":random.randint(1,5), "quantity":random.randint(100,500)}})#送物品
		# send_tcp_message({'function' : 'send_text_mail', 'data' : {"token":token, "gn_target":"去污","msg":"msg:"+str(random.randint(1,100000000))}})#发送文字
		mytime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		friend_time = time.strftime('%Y-%m-%d', time.localtime())
		mydata = time.strftime('%Y-%m', time.localtime())
		_execute_statement(f'INSERT INTO achievement (uid, aid, value,reward) VALUES ("{module_1_login.unique_id}", {random.randint(1,31)}, {random.randint(1,1000)},{0}) ON DUPLICATE KEY UPDATE `reward`= values(`reward`)')
		_execute_statement(f'INSERT INTO armor (uid, aid, level,quantity) VALUES ("{module_1_login.unique_id}", {random.randint(1,31)}, {random.randint(1,10)},{random.randint(1,100)})  ON DUPLICATE KEY UPDATE `quantity`= values(`quantity`)')
		_execute_statement(f'INSERT INTO item (uid, iid, value) VALUES ("{module_1_login.unique_id}", {random.randint(1,31)}, {random.randint(1,1000)}) ON DUPLICATE KEY UPDATE `value`= values(`value`)')
		_execute_statement(f'INSERT INTO weapon (uid, wid, star,level, skillpoint, segment) VALUES ("{module_1_login.unique_id}", {random.randint(1,31)}, {random.randint(1,5)},{0},{random.randint(1,5000)},{random.randint(1,5000)}) ON DUPLICATE KEY UPDATE `segment`= values(`segment`)')
		fname = f'f_unique_id_{random.randint(1,31)}'
		_execute_statement(f'INSERT INTO friend (uid, fid, recover,since) VALUES ("{module_1_login.unique_id}", "{fname}", "{friend_time}","{friend_time}") ON DUPLICATE KEY UPDATE `since`= values(`since`)')
		_execute_statement(f'INSERT INTO player (uid, gn, fid) VALUES ("{fname}", "f_name_{random.randint(1,31)}", "") ON DUPLICATE KEY UPDATE `fid`= values(`fid`)')
		_execute_statement(f'INSERT INTO skill (uid, sid, level) VALUES ("{module_1_login.unique_id}", {random.randint(1,31)}, {random.randint(1,31)}) ON DUPLICATE KEY UPDATE `level`= values(`level`)')
		_execute_statement(f'INSERT INTO role (uid, rid, star, level, skillpoint, segment) VALUES ("{module_1_login.unique_id}", {random.randint(1,31)}, {random.randint(1,5)},{random.randint(1,30)},{random.randint(1,5)},{random.randint(1,500)}) ON DUPLICATE KEY UPDATE `level`= values(`level`)')
		_execute_statement(f'INSERT INTO darkmarket (pid,uid, mid, gid, qty, cid, amt) VALUES ({random.randint(0,7)},"{module_1_login.unique_id}", {random.randint(1,5)}, {random.randint(1,5)},{random.randint(1,30)},{random.randint(1,5)},{random.randint(1,500)}) ON DUPLICATE KEY UPDATE `amt`= values(`amt`)')
		_execute_statement(f'INSERT INTO family (name, icon, exp) VALUES ("{module_1_login.unique_id}", {random.randint(1,5)}, {random.randint(1,500)}) ON DUPLICATE KEY UPDATE `exp`= values(`exp`)')
		_execute_statement(f'INSERT INTO familyrole (uid, name, role) VALUES ("{module_1_login.unique_id}", "{"lol"+str(random.randint(1,5))}", "{random.randint(1,500)}") ON DUPLICATE KEY UPDATE `role`= values(`role`)')
		_execute_statement(f'INSERT INTO task (uid, tid, value,reward,timer) VALUES ("{module_1_login.unique_id}", {random.randint(1,13)}, {random.randint(0,1)},{0},"{mytime}") ON DUPLICATE KEY UPDATE `reward`= values(`reward`)')
		_execute_statement(f'INSERT INTO check_in (uid, date, reward) VALUES ("{module_1_login.unique_id}", "{mydata+"-"+str(random.randint(10,31))}", {1}) ON DUPLICATE KEY UPDATE `reward`= values(`reward`)')
if __name__ == "__main__":
	run_task("C2F09CC7-E5E0-5222-82C9-D4856270DAF7")
