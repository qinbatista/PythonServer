import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client as tc
import random
import user_behavior_simulation
logger = tc.logger
lukseun = tc.LukseunClient('aliya', port = 8880)
world = "0"
token = ""
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))


def purchase_item_success(item_id):
	pass
def factory_dialog(token,world,get_all_weapon):
	new_response = get_all_weapon
	operat_factory = random.randint(0,3)
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'refresh_factory', 'data' : {'token' : token}})

	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'upgrade_factory', 'data' : {'token':token, "fid":operat_factory}})

	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'buy_worker_factory', 'data' : {'token':token, "fid":operat_factory, "num":1}})

	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'activate_wishing_pool_factory', 'data' : {'token':token, "wid":5}})

	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'buy_acceleration_factory', 'data' : {'token' : token}})

	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'set_armor_factory', 'data' : {'token' : token,'aid':1}})

	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'update_worker_factory', 'data' : {'token' : token, "worker": {"0": 1, "1": 1, "2": 1}}})


	# while True:
	# 	print("_________________________")
	# 	print("0:刷新工厂")
	# 	print("1:升级工厂")
	# 	print("2:购买工人")
	# 	print("5:武器许愿")
	# 	print("6:购买加速")
	# 	print("7:设置盔甲")
	# 	print("8:获取配置文件")
	# 	print("9:更新工厂工人")
	# 	print("_________________________")
	# 	operat_factory = 0
	# 	int_number = input()#random.randint(1,1)
	# 	#获取所有工厂信息
	# 	if int_number=="0":# 刷新工厂
	# 		new_response = send_tcp_message({'world' : world, 'function' : 'refresh_factory', 'data' : {'token' : token}})
	# 		logger.debug(str(new_response))
	# 	elif int_number=="1":# 升级工厂
	# 		new_response = send_tcp_message({'world' : world, 'function' : 'upgrade_factory', 'data' : {'token':token, "fid":operat_factory}})
	# 		logger.debug(str(new_response))
	# 	elif int_number=="2":# 购买工人
	# 		new_response = send_tcp_message({'world' : world, 'function' : 'buy_worker_factory', 'data' : {'token':token, "fid":operat_factory, "num":1}})
	# 		logger.debug(str(new_response))
	# 	elif int_number=="5":# 武器碎片许愿池
	# 		new_response = send_tcp_message({'world' : world, 'function' : 'activate_wishing_pool_factory', 'data' : {'token':token, "wid":5}})
	# 		logger.debug(str(new_response))
	# 	elif int_number=="6":# 购买加速
	# 		new_response = send_tcp_message({'world' : world, 'function' : 'buy_acceleration_factory', 'data' : {'token' : token}})
	# 		logger.debug(str(new_response))
	# 	elif int_number=="7":# 设置盔甲
	# 		new_response = send_tcp_message({'world' : world, 'function' : 'set_armor_factory', 'data' : {'token' : token,'aid':1}})
	# 		logger.debug(str(new_response))
	# 	elif int_number=="8":# 获取配置文件
	# 		new_response = send_tcp_message({'world' : world, 'function' : 'get_config_factory', 'data' : {'token' : token}})
	# 		logger.debug(str(new_response))
	# 	elif int_number=="9":# 更新工厂工人
	# 		new_response = send_tcp_message({'world' : world, 'function' : 'update_worker_factory', 'data' : {'token' : token, "worker": {"0": 1, "1": 1, "2": 1}}})
	# 		logger.debug(str(new_response))
	# 	else:
	# 		logger.debug("输入错误")
	# 		continue


if __name__ == '__main__':
	tk1 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODEyNDc2NTAsInVpZCI6ImZkZTM4ZThiOWUzNWY2NDYzZGZlYzliMDg3YmVlM2JjOTY3OWYxY2QifQ.dL-yTPFs49KAEpIE0__kBsZt-PuKP0dTQd7zByzQ1gA'
	wd1 = 's6'
	response = user_behavior_simulation.send_tcp_message({'world' : wd1, 'function' : 'refresh_factory', 'data' : {'token' : tk1}})

