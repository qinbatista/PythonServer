import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random


lukseun = tool_lukseun_client.LukseunClient('aliya', '127.0.0.1', port = 8880)
world = "0"
unique_id = "4"
token = ""
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))
def purchase_energy():
	global token
	# msg = {'world' : world, 'function' : 'enter_stage', 'data' : {'token' : token, 'stage' : '1'}}
	# response = send_tcp_message(msg)
	return True
def registered_account(world:str, unique_id: str):
	print_module("[registered_account]")
	msg = {'function' : 'login_unique', 'data' : {'unique_id' : unique_id}}
	response = asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))
	myjson = response
	if myjson["status"]==0:
		print_method("[registered_account] login success")
		return myjson["data"]["token"]
	else:
		print_method("[registered_account] login failed, try login again")
		registered_account(world,unique_id)

def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")
def enter_level():
	print_module("[enter_level]")
	global token
	msg = {'world' : world, 'function' : 'get_hang_up_info', 'data' : {'token' : token}}
	response = send_tcp_message(msg)#挑战成功
	while True:
		my_number = random.randint(0,0)
		if my_number==0:#剧情
			yourstage = response["data"]["remaining"]["stage"]
			print_method("[enter_level] play normal level")
			stage = random.randint(1,yourstage+1)
			msg = {'world' : world, 'function' : 'enter_stage', 'data' : {'token' : token, 'stage' : str(stage)}}
			response_enter = send_tcp_message(msg)#进入关卡
			if response_enter["status"]==0:
				msg = {'world' : '0', 'function' : 'pass_stage', 'data' : {'token' : token, 'stage' : str(stage), 'clear_time' : 'we dont care what this string is'}}
				response_enter = send_tcp_message(msg)#挑战成功
				print_method("[enter_level] normal level passed")
			else:
				my_choice = random.choice([0,1])
				if my_choice==0:
					purchase_energy()
				else:
					break
		elif my_number==1:#世界boss
			print_method("[enter_level] play world boss")
			msg = {'world' : world, 'function' : 'enter_world_boss_stage', 'data' : {'token' : token}}
			response_enter = send_tcp_message(msg)
			if response_enter["status"]==0:
				msg = {'world' : world, 'function' : 'leave_world_boss_stage', 'data' : {'token' : token,"total_damage":random.randint(1,100000)}}
				response_enter = send_tcp_message(msg)
				print_method("[enter_level] challange boss success")
			else:
				my_choice = random.choice([0,1])
				if my_choice==0:
					msg = {'world' : world, 'function' : 'get_top_damage', 'data' : {'token' : token,"range_number":random.randint(1,5)}}
					response_enter = send_tcp_message(msg)
					print_method("[enter_level] get top damage")
				else:
					break
		elif my_number==2:#无尽试炼
			print_method("[enter_level] endless training")
		elif my_number==3:#活动试炼
			yourstage = response["remaining"]["tower_stage"]
			print_method("[enter_level] party training")
		elif my_number==4:#退出
			print_method("[enter_level] quit level playing")
			break
def freind_dialog():
	print_module("[freind_dialog]")
	global token
	msg = {'world' : world, 'function' : 'get_all_friend_info', 'data' : {'token' : token}}
	response = send_tcp_message(msg)#获取所有好友信息
	# print(str(response))
	while True:
		int_random = random.randint(0,4)
		if int_random==0:#发送一个好友
			for i in range(0,len(response["data"]["remaining"]["f_name"])):
				send_msg = {'world' : world, 'function' : 'send_friend_gift', 'data' : {'token' : token,"friend_name":str(response["data"]["remaining"]["f_name"][i])}}
				new_response = send_tcp_message(send_msg)#发送好友信息
				if new_response["status"]=="0":
					print_method("[freind_dialog] send friend gift:"+new_response["data"]["remaining"]["f_name"][i])
				else:
					print_method(f'[freind_dialog] send {response["data"]["remaining"]["f_name"][i]} gift but failed, error:{new_response["message"]}')
		elif int_random==1:#发送所有好友信息
			send_msg = {'world' : world, 'function' : 'send_all_friend_gift', 'data' : {'token' : token}}
			new_response = send_tcp_message(send_msg)#发送好友信息s
			print_method("[freind_dialog] send all gift:"+"")
		elif int_random==2:#加好友
			friend_name = random.randint(0,100)
			send_msg = {'world' : world, 'function' : 'request_friend', 'data' : {'token' : token,"friend_name":str(friend_name)}}
			new_response = send_tcp_message(send_msg)#发送好友信息
			print_method("[freind_dialog] requst_friend:"+str(friend_name)+" "+"")
		elif int_random==3:#删好友
			friend_name = random.randint(0,100)
			send_msg = {'world' : world, 'function' : 'delete_friend', 'data' : {'token' : token,"friend_name":str(friend_name)}}
			new_response = send_tcp_message(send_msg)#发送好友信息
			print_method("[freind_dialog] delete_friend:"+str(friend_name)+" "+"")
		elif int_random ==4:
			print_method("[freind_dialog] quit friend dialog")
			break
def purchase_item_success(item_id):
	print_method("[freind_dialog] purchase item")
def get_random_skill():
	print_module("[get_random_skill]")
	while True:
		int_n = random.randint(0,1)
		if int_n == 0: #朋友召唤
			print_method("[freind_dialog] friend gift to get skill")
			is_10 = random.choice([0,1])
			if is_10==0:
				send_msg = {'world' : world, 'function' : 'basic_summon_skill', 'data' : {'token' : token,"cost_item":"friend_gift"}}
			else:
				send_msg = {'world' : world, 'function' : 'basic_summon_skill_10_times', 'data' : {'token' : token,"cost_item":"friend_gift"}}
			new_response = send_tcp_message(send_msg)#发送好友信息
		elif int_n == 1:#高级召唤
			print_method("[freind_dialog] diamond gift to get skill")
			is_10 = random.choice([0,1])
			if is_10==0:
				send_msg = {'world' : world, 'function' : 'pro_summon_skill', 'data' : {'token' : token,"cost_item":"basic_summon_scroll"}}
			else:
				send_msg = {'world' : world, 'function' : 'pro_summon_skill_10_times', 'data' : {'token' : token,"cost_item":"basic_summon_scroll"}}
			new_response = send_tcp_message(send_msg)#发送好友信息
			if new_response["status"]!=0:
				purchase_item_success("basic_summon_scroll")#购买卷轴
				if random.choice([0,1])==0:
					continue
				else:
					break
			else:
				break
def get_random_weapon():
	print_module("[get_random_weapon]")
	while True:
		int_n = random.randint(0,1)
		if int_n == 0: #金币召唤
			print_method("[get_random_weapon] coin to get weapon")
			is_10 = random.choice([0,1])
			if is_10==0:
				send_msg = {'world' : world, 'function' : 'basic_summon', 'data' : {'token' : token,"cost_item":"coin"}}
			else:
				send_msg = {'world' : world, 'function' : 'basic_summon_10_times', 'data' : {'token' : token,"cost_item":"coin"}}
			new_response = send_tcp_message(send_msg)#发送好友信息
			if new_response["status"]!=0:
				purchase_item_success("coin")#购买金币
				coin_item = random.choice([0,2])
				if coin_item==0:
					continue#继续抽
				elif coin_item==1:
					enter_level()#进入关卡
					break
				elif coin_item==2:
					break#不抽
			else:
				break
		elif int_n == 1:#高级召唤
			print_method("[get_random_weapon] diamond gift to get weapon")
			is_10 = random.choice([0,1])
			if is_10==0:
				send_msg = {'world' : world, 'function' : 'pro_summon', 'data' : {'token' : token,"cost_item":"basic_summon_scroll"}}
			else:
				send_msg = {'world' : world, 'function' : 'pro_summon_10_times', 'data' : {'token' : token,"cost_item":"basic_summon_scroll"}}
			new_response = send_tcp_message(send_msg)#发送好友信息
			if new_response["status"]!=0:
				purchase_item_success("basic_summon_scroll")#购买卷轴
				if random.choice([0,1])==0:
					continue
				else:
					break
			else:
				break
def get_random_role():
	print_module("[get_random_role]")
	while True:
		int_n = random.randint(0,2)
		if int_n == 0: #金币召唤
			print_method("[get_random_role] coin to get role")
			is_10 = random.choice([0,1])
			if is_10==0:
				send_msg = {'world' : world, 'function' : 'basic_summon_roles', 'data' : {'token' : token,"cost_item":"coin"}}
			else:
				send_msg = {'world' : world, 'function' : 'basic_summon_roles_10_times', 'data' : {'token' : token,"cost_item":"coin"}}
			new_response = send_tcp_message(send_msg)#发送好友信息
			if new_response["status"]!=0:
				purchase_item_success("basic_summon_scroll")#购买卷轴
				coin_item = random.choice([0,2])
				if coin_item==0:
					continue#继续抽
				elif coin_item==1:
					enter_level()#进入关卡
					break
				elif coin_item==2:
					break#不抽
			else:
				break
		elif int_n == 1:#高级召唤
			print_method("[get_random_role] diamond gift to get role")
			is_10 = random.choice([0,1])
			if is_10==0:
				send_msg = {'world' : world, 'function' : 'pro_summon_roles', 'data' : {'token' : token,"cost_item":"basic_summon_scroll"}}
			else:
				send_msg = {'world' : world, 'function' : 'pro_summon_roles_10_times', 'data' : {'token' : token,"cost_item":"basic_summon_scroll"}}
			new_response = send_tcp_message(send_msg)#发送好友信息
			if new_response["status"]!=0:
				purchase_item_success("basic_summon_scroll")#购买卷轴
				if random.choice([0,1])==0:
					continue
				else:
					break
			else:
				break
		elif int_n == 2:#朋友召唤
			print_method("[get_random_role] coin to get role")
			is_10 = random.choice([0,1])
			if is_10==0:
				send_msg = {'world' : world, 'function' : 'basic_summon_roles', 'data' : {'token' : token,"cost_item":"friend_gift"}}
			else:
				send_msg = {'world' : world, 'function' : 'basic_summon_roles_10_times', 'data' : {'token' : token,"cost_item":"friend_gift"}}
			new_response = send_tcp_message(send_msg)#朋友抽


def skill_dialog():
	print_module("[skill_dialog]")
	send_msg = {'world' : world, 'function' : 'get_all_skill_level', 'data' : {'token' : token}}
	new_response = send_tcp_message(send_msg)#升级请求
	while True:
		skill_id = random.choice(["m1_level", "p1_level", "g1_level", "m11_level", "m12_level", "m13_level", "p11_level", "p12_level", "p13_level", "g11_level", "g12_level", "g13_level",
				"m111_level", "m112_level", "m113_level", "m121_level", "m122_level", "m123_level", "m131_level", "m132_level", "m133_level",
				"p111_level", "p112_level", "p113_level", "p121_level", "p122_level", "p123_level", "p131_level", "p132_level", "p133_level",
				"g111_level", "g112_level", "g113_level", "g121_level", "g122_level", "g123_level", "g131_level", "g132_level", "g133_level"])
		skill_level = new_response["data"]["remaining"][skill_id]
		if skill_level==0:
			get_random_skill()
		else:
			scroll_id = random.choice(["skill_scroll_10","skill_scroll_30","skill_scroll_100"])
			send_msg = {'world' : world, 'function' : 'level_up_skill', 'data' : {'token' : token,"skill_id":skill_id,"scroll_id":scroll_id}}
			new_response = send_tcp_message(send_msg)#升级请求
			print_method("[skill_dialog] level up skill success" + "")
def weapon_dialog():
	print_module("[weapon_dialog]")
	send_msg = {'world' : world, 'function' : 'get_all_weapon', 'data' : {'token' : token}}
	new_response = send_tcp_message(send_msg)#升级请求
	print_method("[weapon_dialog] get all weapon info")
	while True:
		random_int = random.randint(0,4)
		if random_int ==0:#升级武器
			send_msg = {'world' : world, 'function' : 'level_up_weapon', 'data' : {'token' : token, "weapon":random.choice(["weapon1", "weapon2", "weapon3", "weapon4", "weapon5", "weapon6", "weapon7", "weapon8", "weapon9", "weapon10", "weapon11", "weapon12", "weapon13", "weapon14", "weapon15", "weapon16", "weapon17", "weapon18", "weapon19", "weapon20", "weapon21", "weapon22", "weapon23", "weapon24", "weapon25", "weapon26", "weapon27", "weapon28", "weapon29", "weapon30", "weapon31", "weapon32", "weapon33", "weapon34", "weapon35", "weapon36", "weapon37", "weapon38", "weapon39", "weapon40"]),"iron":random.randint(30,400)}}
			new_response = send_tcp_message(send_msg)#升级请求
			print_method("[weapon_dialog] level up weapon:")
			if new_response["status"]==95:#武器没有抽武器
				get_random_weapon()
			if new_response["status"]==95:#材料不足冲关卡
				enter_level()
		elif random_int ==1:#突破武器
			send_msg = {'world' : world, 'function' : 'level_up_weapon_star', 'data' : {'token' : token, "weapon":random.choice(["weapon1", "weapon2", "weapon3", "weapon4", "weapon5", "weapon6", "weapon7", "weapon8", "weapon9", "weapon10", "weapon11", "weapon12", "weapon13", "weapon14", "weapon15", "weapon16", "weapon17", "weapon18", "weapon19", "weapon20", "weapon21", "weapon22", "weapon23", "weapon24", "weapon25", "weapon26", "weapon27", "weapon28", "weapon29", "weapon30", "weapon31", "weapon32", "weapon33", "weapon34", "weapon35", "weapon36", "weapon37", "weapon38", "weapon39", "weapon40"])}}
			new_response = send_tcp_message(send_msg)#升级请求
			print_method("[weapon_dialog] level up weapon star:")
			if new_response["status"]==98:
				get_random_weapon()
		elif random_int ==2:#升级被动
			send_msg = {'world' : world, 'function' : 'level_up_passive', 'data' : {'token' : token, "weapon":random.choice(["weapon1", "weapon2", "weapon3", "weapon4", "weapon5", "weapon6", "weapon7", "weapon8", "weapon9", "weapon10", "weapon11", "weapon12", "weapon13", "weapon14", "weapon15", "weapon16", "weapon17", "weapon18", "weapon19", "weapon20", "weapon21", "weapon22", "weapon23", "weapon24", "weapon25", "weapon26", "weapon27", "weapon28", "weapon29", "weapon30", "weapon31", "weapon32", "weapon33", "weapon34", "weapon35", "weapon36", "weapon37", "weapon38", "weapon39", "weapon40"]),"passive":random.choice(["passive_skill_1_level", "passive_skill_2_level", "passive_skill_3_level", "passive_skill_4_level"])}}
			new_response = send_tcp_message(send_msg)#升级请求
			print_method("[weapon_dialog] level up weapon skill")
		elif random_int ==3:#重制技能
			send_msg = {'world' : world, 'function' : 'reset_weapon_skill_point', 'data' : {'token' : token,"weapon":["weapon1", "weapon2", "weapon3", "weapon4", "weapon5", "weapon6", "weapon7", "weapon8", "weapon9", "weapon10", "weapon11", "weapon12", "weapon13", "weapon14", "weapon15", "weapon16", "weapon17", "weapon18", "weapon19", "weapon20", "weapon21", "weapon22", "weapon23", "weapon24", "weapon25", "weapon26", "weapon27", "weapon28", "weapon29", "weapon30", "weapon31", "weapon32", "weapon33", "weapon34", "weapon35", "weapon36", "weapon37", "weapon38", "weapon39", "weapon40"]}}
			new_response = send_tcp_message(send_msg)#升级请求
			print_method("[weapon_dialog] reset weapon skill")
		elif random_int ==4:#退出
			print_method("[weapon_dialog] quit weapon_dialog")
			break
def factory_dialog():
	print_module("[factory_dialog]")
	send_msg = {'world' : world, 'function' : 'refresh_all_storage','data' : {'token' : token}}
	new_response = send_tcp_message(send_msg)
	while True:
		int_number = random.randint(0,5)
		#获取所有工厂信息
		if int_number==0:#购买工人
			print_method("[factory_dialog]buy workers")
			send_msg = {'world' : world, 'function' : 'buy_workers', 'data' : {'token' : token, "workers_quantity":"5"}}
			new_response = send_tcp_message(send_msg)
			if new_response["status"]==98:
				choice = random.choice([0,1])
				if choice == 1:
					send_msg = {'world' : world, 'function' : 'upgrade_food_factory', 'data' : {'token' : token}}
					new_response = send_tcp_message(send_msg)
					print_method("[factory_dialog]upgrade_food_factory:")
				else:
					send_msg = {'world' : world, 'function' : 'distribution_workers', 'data' : {'token' : token,"workers_quantity":str(random.randint(1,3)),"factory_kind":"food"}}
					new_response = send_tcp_message(send_msg)
					print_method("[factory_dialog]distribution_workers:")
		elif int_number==1:#升级工厂
			print_method("[factory_dialog]upgrade factory")
			send_msg = {'world' : world, 'function' : random.choice(['upgrade_food_factory',"upgrade_crystal_factory","upgrade_mine_factory","upgrade_wishing_pool"]), 'data' : {'token' : token}}
			new_response = send_tcp_message(send_msg)
			if new_response["status"]==2:
				num = random.choice([0,1])
				if num ==0:
					send_msg = {'world' : world, 'function' : 'upgrade_crystal_factory', 'data' : {'token' : token}}
					new_response = send_tcp_message(send_msg)
					print_method("[factory_dialog] insufficient, upgrade crystal")
				else:
					continue
		elif int_number==2:#改变工人
			print_method("[factory_dialog]distribute workers")
			send_msg = {'world' : world, 'function' : 'distribution_workers', 'data' : {'token' : token,"workers_quantity":str(random.randint(-3,3)),"factory_kind":random.choice(["food", "mine", "crystal", "equipment"])}}
			new_response = send_tcp_message(send_msg)
		elif int_number==3:#选择盔甲
			print_method("[factory_dialog]equipment_manufacturing_armor")
			send_msg = {'world' : world, 'function' : 'equipment_manufacturing_armor', 'data' : {'token' : token,"armor_kind":random.choice(["armor1", "armor2", "armor3", "armor4", "armor5", "armor6", "armor7", "armor8", "armor9", "armor10"])}}
			new_response = send_tcp_message(send_msg)
		elif int_number==4:#获得碎片
			print_method("[factory_dialog]active_wishing_pool")
			send_msg = {'world' : world, 'function' : 'active_wishing_pool', 'data' : {'token' : token,"weapon_id":random.choice(["weapon1", "weapon2", "weapon3", "weapon4", "weapon5", "weapon6", "weapon7", "weapon8", "weapon9", "weapon10","weapon11", "weapon12", "weapon13", "weapon14", "weapon15", "weapon16", "weapon17", "weapon18", "weapon19", "weapon20","weapon21", "weapon22", "weapon23", "weapon24", "weapon25", "weapon26", "weapon27", "weapon28", "weapon29", "weapon30","weapon31", "weapon32", "weapon33", "weapon34", "weapon35", "weapon36", "weapon37", "weapon38", "weapon39", "weapon40"])}}
			new_response = send_tcp_message(send_msg)
			if new_response["status"]==99:
				purchase_item_success("diamond")
		elif int_number==5:#不做选择
			print_method("[factory_dialog]quit")
			break
def get_random_item():
	print_module("[get_random_item]")
	while True:
		int_number = random.randint(0,3)
		if int_number==0: get_random_role()
		if int_number==1: get_random_skill()
		if int_number==2: get_random_weapon()
		if int_number==3: break
def role_dialog():
	print_module("[role_dialog]")
	while True:
		random_int = random.randint(0,0)
		if random_int ==0:#升级角色
			send_msg = {'world' : world, 'function' : 'upgrade_role_level', 'data' : {'token' : token, "role":random.choice(["role1", "role2", "role3", "role4", "role5", "role6", "role7", "role8", "role9", "role10", "role11", "role12", "role13", "role14", "role15", "role16", "role17", "role18", "role19", "role20", "role21", "role22", "role23", "role24", "role25", "role26", "role27", "role28", "role29", "role30", "role31", "role32", "role33", "role34", "role35", "role36", "role37", "role38", "role39", "role40"]),"experience_potion":random.randint(30,400)}}
			new_response = send_tcp_message(send_msg)#升级请求
			print_method("[role_dialog] level up role:")
			if new_response["status"]==95:#没有此角色
				get_random_role()
			if new_response["status"]==97:#材料不足冲关卡
				enter_level()
		elif random_int ==1:#突破角色
			send_msg = {'world' : world, 'function' : 'upgrade_role_star', 'data' : {'token' : token, "role":random.choice(["role1", "role2", "role3", "role4", "role5", "role6", "role7", "role8", "role9", "role10", "role11", "role12", "role13", "role14", "role15", "role16", "role17", "role18", "role19", "role20", "role21", "role22", "role23", "role24", "role25", "role26", "role27", "role28", "role29", "role30", "role31", "role32", "role33", "role34", "role35", "role36", "role37", "role38", "role39", "role40"])}}
			new_response = send_tcp_message(send_msg)#升级请求
			print_method("[role_dialog] level up role star:")
			if new_response["status"]==98:
				get_random_role()
		elif random_int ==2:#退出
			print_method("[role_dialog] quit role_dialog")
			break
if __name__ == "__main__":
	token = registered_account("0",unique_id)#账号注册
	enter_level()#关卡界面
	freind_dialog()#朋友界面
	skill_dialog()#技能界面
	weapon_dialog()#武器界面
	factory_dialog()#工厂界面
	get_random_item()#抽奖界面
	role_dialog()#角色界面
