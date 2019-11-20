
import tool_lukseun_client
import module_0_login
import module_1_stage
import module_2_summon
import module_3_lottery
import module_6_darkmarket

import module_10_weapons
import module_11_friends
import module_12_chat
import module_13_mail
import module_14_armor
import module_15_skills
import module_16_get_all_data

import module_18_family
import module_19_factory
import module_20_store
import module_21_roles
import module_22_announcement
import module_23_daily_task

import module_24_achievement
import module_25_check_in
import module_26_bag
import module_27_vip

import multiprocessing
import time
import random
import asyncio
import pymysql
from datetime import datetime, timedelta
import os
import gevent
# from gevent import monkey; monkey.patch_all()
logger = tool_lukseun_client.logger
lukseun = tool_lukseun_client.LukseunClient('aliya',host="192.168.1.165", port = 8880)
world = "0"
token = ""
unique_id=""
testing_people_number = 1000
DEBUG_LOG = True
DEBUG_LOG_DETAIL=False



def call_login(unique_id):
	global world,token
	while True:
		world = module_0_login.login_module(unique_id)
		if world!=None:
			token,world = world
			if token!="" and world!="":break
def get_number():
	return testing_people_number

def debug_log(time,method_name,string,level=1):
	if DEBUG_LOG == False:
		return
	print(f"\033[1;9{1 if level!=1 else 2}m\t{format(time, '0.3f')} S\033[0m\033[1;93m\t[{method_name}]\033[0m\033[1;\t{string if DEBUG_LOG_DETAIL==True else ''}\033[0m")
	with open(os.path.dirname(os.path.realpath(__file__))+"/log_history/"+method_name+".txt","a") as f:
		f.writelines(f"{time} { '' if string=='' else string['status']} {datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')}\r\n")
def send_tcp_message(msg):
	start = time.time()
	msg_resutl= asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))
	end = time.time()
	debug_log(end-start,msg['function'],msg_resutl)
	return msg_resutl

def _execute_statement(statement: str) -> tuple:
		db = pymysql.connect('192.168.1.102', 'root', 'lukseun', '0')
		cursor = db.cursor()
		cursor.execute(statement)
		db.commit()

def create_data(name):
	global unique_id,token
	unique_id = name
	#mail_type: SIMPLE = 0,GIFT = 1, FRIEND_REQUEST = 2 FAMILY_REQUEST = 3
	#item_id: COIN = 1,IRON = 2,FOOD = 3,CRYSTAL = 4,DIAMOND = 5
	for i in range(0,5):
		send_tcp_message({'function' : 'send_gift_mail', 'data' : {"token":token, "gn_target":"去污", "group_id":3, "item_id":random.randint(1,5), "quantity":random.randint(100,500)}})#送物品
		mytime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		friend_time = time.strftime('%Y-%m-%d', time.localtime())
		mydata = time.strftime('%Y-%m', time.localtime())
		_execute_statement(f'INSERT INTO achievement (uid, aid, value,reward) VALUES ("{unique_id}", {random.randint(1,31)}, {random.randint(1,1000)},{0}) ON DUPLICATE KEY UPDATE `reward`= values(`reward`)')
		_execute_statement(f'INSERT INTO armor (uid, aid, level,quantity) VALUES ("{unique_id}", {random.randint(1,31)}, {random.randint(1,10)},{random.randint(1,100)})  ON DUPLICATE KEY UPDATE `quantity`= values(`quantity`)')
		_execute_statement(f'INSERT INTO item (uid, iid, value) VALUES ("{unique_id}", {random.randint(1,31)}, {random.randint(1,1000)}) ON DUPLICATE KEY UPDATE `value`= values(`value`)')
		_execute_statement(f'INSERT INTO weapon (uid, wid, star,level, skillpoint, segment) VALUES ("{unique_id}", {random.randint(1,31)}, {random.randint(1,5)},{0},{random.randint(1,5000)},{random.randint(1,5000)}) ON DUPLICATE KEY UPDATE `segment`= values(`segment`)')
		fname = f'f_unique_id_{random.randint(1,31)}'
		_execute_statement(f'INSERT INTO friend (uid, fid, recover,since) VALUES ("{unique_id}", "{fname}", "{friend_time}","{friend_time}") ON DUPLICATE KEY UPDATE `since`= values(`since`)')
		_execute_statement(f'INSERT INTO player (uid, gn, fid) VALUES ("{fname}", "f_name_{random.randint(1,31)}", "") ON DUPLICATE KEY UPDATE `fid`= values(`fid`)')
		_execute_statement(f'INSERT INTO skill (uid, sid, level) VALUES ("{unique_id}", {random.randint(1,31)}, {random.randint(1,31)}) ON DUPLICATE KEY UPDATE `level`= values(`level`)')
		_execute_statement(f'INSERT INTO role (uid, rid, star, level, skillpoint, segment) VALUES ("{unique_id}", {random.randint(1,31)}, {random.randint(1,5)},{random.randint(1,30)},{random.randint(1,5)},{random.randint(1,500)}) ON DUPLICATE KEY UPDATE `level`= values(`level`)')
		_execute_statement(f'INSERT INTO darkmarket (pid,uid, mid, gid, qty, cid, amt) VALUES ({random.randint(0,7)},"{unique_id}", {random.randint(1,5)}, {random.randint(1,5)},{random.randint(1,30)},{random.randint(1,5)},{random.randint(1,500)}) ON DUPLICATE KEY UPDATE `amt`= values(`amt`)')
		_execute_statement(f'INSERT INTO family (name, icon, exp) VALUES ("{unique_id}", {random.randint(1,5)}, {random.randint(1,500)}) ON DUPLICATE KEY UPDATE `exp`= values(`exp`)')
		_execute_statement(f'INSERT INTO familyrole (uid, name, role) VALUES ("{unique_id}", "{"lol"+str(random.randint(1,5))}", "{random.randint(1,500)}") ON DUPLICATE KEY UPDATE `role`= values(`role`)')
		_execute_statement(f'INSERT INTO task (uid, tid, value,reward,timer) VALUES ("{unique_id}", {random.randint(1,13)}, {random.randint(0,1)},{0},"{mytime}") ON DUPLICATE KEY UPDATE `reward`= values(`reward`)')
		_execute_statement(f'INSERT INTO check_in (uid, date, reward) VALUES ("{unique_id}", "{mydata+"-"+str(random.randint(10,31))}", {1}) ON DUPLICATE KEY UPDATE `reward`= values(`reward`)')
def run_task(name):
	global unique_id
	unique_id = name
	call_login(str(name))
	# create_data(name)
	start = time.time()
	info_list =  module_16_get_all_data.get_all_info(token,world)#加载所有参数信息
	# module_1_stage.stage_dialog(token,world,info_list[5])##战役
	# module_2_summon.summon_dialog(token,world)#召唤法政
	# module_3_lottery.get_random_item(token,world)#转盘
	# module_6_darkmarket.darkmarket_dialog(token,world)#市场
	# module_10_weapons.weapon_dialog(token,world,info_list[5])#铁匠铺
	# module_11_friends.freind_dialog(token,world)#朋友
	# module_14_armor.armor_dialog(token,world,info_list[1])#盔甲合成
	# module_15_skills.skill_dialog(token,world,info_list[5])#技能天赋
	# # module_18_family.family_dialog(token,world,get_all_family_info, player_info)#家族系统（后测试）
	# module_19_factory.factory_dialog(token,world,info_list[5])#建造
	# # module_20_shoping.shoping_dialog(token,world,info_list[5])#商场(内部方法)
	# module_21_roles.role_dialog(token,world)#玩家卡牌
	# # module_22_announcement.announcement_dialog(token,world)#公告系统（后测试）
	# module_23_daily_task.task_dialog(token,world,info_list[5])#每日任务
	# module_24_achievement.achievement_dialog(token,world)#成就系统
	# module_25_check_in.check_in_dialog(token,world,info_list[5])#签到系统
	# module_26_bag.bag_dialog(token,world,info_list[5])#玩家背包
	# module_27_vip.vip_dialog(token,world,info_list[5])#vip系统
	end = time.time()
	debug_log(end-start,"user_"+str(unique_id),"",level=2)
	gevent.sleep(0)


def run_all_task_multiprocessing():
	starttime = datetime.now()
	p = multiprocessing.Pool(processes=12)
	for i in range(0,testing_people_number):
		p.apply_async(run_task, args=(str(i),))
	p.close()
	p.join()
	endtime = datetime.now()
	print("cost time:["+str((endtime - starttime).seconds)+"]s")

def run_all_task_gevent():
	starttime = datetime.now()
	gevent.joinall([gevent.spawn(run_task, i) for i in range(0, testing_people_number)])
	endtime = datetime.now()
	print("cost time:["+str((endtime - starttime).seconds)+"]s")
if __name__ == "__main__":
	# run_task("1")
	run_all_task_multiprocessing()

