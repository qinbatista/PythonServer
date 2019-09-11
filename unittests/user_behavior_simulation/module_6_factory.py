import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random


lukseun = tool_lukseun_client.LukseunClient('aliya', port = 8880)
world = "0"
token = ""
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))


def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")
def purchase_item_success(item_id):
	pass
def factory_dialog(token,world,get_all_weapon):
	print_module("[factory_dialog]")
	new_response = get_all_weapon
	while True:
		int_number = random.randint(0,5)
		#获取所有工厂信息
		if int_number==0:#购买工人
			new_response = send_tcp_message({'world' : world, 'function' : 'buy_workers', 'data' : {'token' : token, "workers_quantity":random.randint(1,5)}})
			print_method("[factory_dialog]buy workers:"+str(new_response))
			if new_response["status"]==98:
				choice = random.choice([0,1])
				if choice == 1:
					new_response = send_tcp_message({'world' : world, 'function' : 'upgrade_food_factory', 'data' : {'token' : token}})
					print_method("[factory_dialog]upgrade_food_factory:"+str(new_response))
				else:
					new_response = send_tcp_message({'world' : world, 'function' : 'distribution_workers', 'data' : {'token' : token,"workers_quantity":str(random.randint(1,3)),"factory_kind":"food"}})
					print_method("[factory_dialog]distribution_workers:"+str(new_response))
		elif int_number==1:#升级工厂
			new_response = send_tcp_message({'world' : world, 'function' : random.choice(['upgrade_food_factory',"upgrade_crystal_factory","upgrade_mine_factory","upgrade_wishing_pool"]), 'data' : {'token' : token}})
			print_method("[factory_dialog]upgrade factory:"+str(new_response))
			if new_response["status"]==2:
				num = random.choice([0,1])
				if num ==0:
					new_response = send_tcp_message({'world' : world, 'function' : 'upgrade_crystal_factory', 'data' : {'token' : token}})
					print_method("[factory_dialog] insufficient, upgrade crystal:"+str(new_response))
				else:
					continue
		elif int_number==2:#改变工人
			new_response = send_tcp_message({'world' : world, 'function' : 'distribution_workers', 'data' : {'token' : token,"workers_quantity":random.randint(-3,3),"factory_kind":random.choice(["food", "mine", "crystal", "equipment"])}})
			print_method("[factory_dialog]distribute workers:"+str(new_response))
		elif int_number==3:#选择盔甲
			new_response = send_tcp_message({'world' : world, 'function' : 'equipment_manufacturing_armor', 'data' : {'token' : token,"armor_kind":random.choice(["armor1", "armor2", "armor3", "armor4", "armor5", "armor6", "armor7", "armor8", "armor9", "armor10"])}})
			print_method("[factory_dialog]equipment_manufacturing_armor:"+str(new_response))
		elif int_number==4:#获得碎片
			new_response = send_tcp_message({'world' : world, 'function' : 'active_wishing_pool', 'data' : {'token' : token,"weapon_id":random.choice(["weapon1", "weapon2", "weapon3", "weapon4", "weapon5", "weapon6", "weapon7", "weapon8", "weapon9", "weapon10","weapon11", "weapon12", "weapon13", "weapon14", "weapon15", "weapon16", "weapon17", "weapon18", "weapon19", "weapon20","weapon21", "weapon22", "weapon23", "weapon24", "weapon25", "weapon26", "weapon27", "weapon28", "weapon29", "weapon30","weapon31", "weapon32", "weapon33", "weapon34", "weapon35", "weapon36", "weapon37", "weapon38", "weapon39", "weapon40"])}})
			print_method("[factory_dialog]active_wishing_pool"+str(new_response))
			if new_response["status"]==99:
				purchase_item_success("diamond")
		elif int_number==5:#不做选择
			print_method("[factory_dialog]quit")
			break