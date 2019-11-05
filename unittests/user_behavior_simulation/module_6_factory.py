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
		print("_________________________")
		print("0:刷新工厂")
		print("1:升级工厂")
		print("2:购买工人")
		print("3:添加工人")
		print("4:减少工人")
		print("5:武器许愿")
		print("6:购买加速")
		print("7:设置盔甲")
		print("8:获取配置文件")
		print("_________________________")
		operat_factory = 0
		int_number = input()#random.randint(1,1)
		#获取所有工厂信息
		if int_number=="0":#刷新工厂
			new_response = send_tcp_message({'world' : world, 'function' : 'refresh_factory', 'data' : {'token' : token}})
			print(str(new_response))
		elif int_number=="1":#升级工厂
			new_response = send_tcp_message({'world' : world, 'function' : 'upgrade_factory', 'data' : {'token':token, "fid":operat_factory}})
			print(str(new_response))
		elif int_number=="2":#购买工人
			new_response = send_tcp_message({'world' : world, 'function' : 'buy_worker_factory', 'data' : {'token':token, "fid":operat_factory, "num":1}})
			print(str(new_response))
		elif int_number=="3":#升级工厂
			new_response = send_tcp_message({'world' : world, 'function' : 'increase_worker_factory', 'data' : {'token':token, "fid":operat_factory, "num":1}})
			print(str(new_response))
		elif int_number=="4":#减少工人
			new_response = send_tcp_message({'world' : world, 'function' : 'decrease_worker_factory', 'data' : {'token':token, "fid":operat_factory, "num":1}})
			print(str(new_response))
		elif int_number=="5":#武器碎片许愿池
			new_response = send_tcp_message({'world' : world, 'function' : 'activate_wishing_pool_factory', 'data' : {'token':token, "wid":5}})
			print(str(new_response))
		elif int_number=="6":#购买加速
			new_response = send_tcp_message({'world' : world, 'function' : 'buy_acceleration_factory', 'data' : {'token' : token}})
			print(str(new_response))
		elif int_number=="7":#设置盔甲
			new_response = send_tcp_message({'world' : world, 'function' : 'set_armor_factory', 'data' : {'token' : token,'aid':1}})
			print(str(new_response))
		elif int_number=="8":#获取配置文件
			new_response = send_tcp_message({'world' : world, 'function' : 'get_config_factory', 'data' : {'token' : token}})
			print(str(new_response))
		else:
			print_method("输入错误")
			continue
