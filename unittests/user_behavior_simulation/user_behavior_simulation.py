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
import module_16_daily_task
import multiprocessing
import time
from datetime import datetime, timedelta
world = "0"
token = ""
testing_people_number = 20
def call_login(unique_id):
	global world,token
	while True:
		world = module_1_login.login_module(unique_id)
		if world!=None:
			token,world = world
			if token!="" and world!="":break
def get_number():
	return testing_people_number

def call_friend_dialog(get_all_friend_info):
	module_3_friends.freind_dialog(token,world,get_all_friend_info)

def skill_dialog(get_all_skill_info):
	module_4_skills.skill_dialog(token,world,get_all_skill_info)

def weapon_dialog(get_all_weapon):
	module_5_weapons.weapon_dialog(token,world,get_all_weapon)

def factory_dialog(refresh_all_storage):
	module_6_factory.factory_dialog(token,world,refresh_all_storage)

def get_random_item():
	module_7_lottery.get_random_item(token,world)

def role_dialog():
	module_8_roles.role_dialog(token,world)

def family_dialog(get_all_family_info,player_info):
	module_9_family.family_dialog(token,world,get_all_family_info, player_info)

def stage_dialog(get_level_info):
	module_10_stage.enter_stage(token,world,get_level_info)

def mail_dialog(get_all_mail,name):
	module_11_mail.mail_dialog(token,world,get_all_mail,name)

def announcement():
	pass

def dark_market():
	pass

def vip_system():
	module_14_vip.vip_dialog(token,world)
unique_id=""
def run_task(name):
	global unique_id
	unique_id = name
	call_login(str(name))
	info_list =  module_2_get_all_data.get_all_info(token,world)#加载所有参数信息
	# module_13_achievement.achievement_dialog(token,world,info_list[0])
	# module_15_summon.summon_dialog(token,world)#召唤所有
	# module_5_weapons.weapon_dialog(token,world,info_list[5])
	# module_8_roles.role_dialog(token,world)
	module_7_lottery.get_random_item(token,world)
	# module_16_daily_task.task_dialog(token,world,info_list[5])
	# module_10_stage.stage_dialog(token,world,info_list[5])
	# dark_market()#*加载黑市信息
	# mail_dialog(info_list[10],name)#邮箱界面
	# call_friend_dialog(info_list[3])#朋友界面
	# skill_dialog(info_list[4])#技能界面
	# weapon_dialog(info_list[5])#武器界面
	# factory_dialog(info_list[6])#工厂界面
	# role_dialog()#角色界面
	# family_dialog(info_list[9],info_list[19])

	# announcement()#公告界面
	# vip_system()


def run_all_task():
	starttime = datetime.now()
	print("cpu:"+str(multiprocessing.cpu_count()))
	p = multiprocessing.Pool()
	for i in range(0,testing_people_number):
		p.apply_async(run_task, args=(i,))
	p.close()
	p.join()
	endtime = datetime.now()
	print("cost time:["+str((endtime - starttime).seconds)+"]s")
if __name__ == "__main__":
	run_task("11")
	# run_all_task()
