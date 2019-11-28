import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random
import user_behavior_simulation

lukseun = tool_lukseun_client.LukseunClient('aliya', port = 8880)
world = "0"
token = ""
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))

def login_decoration(func):
	def wrapper(*args, **kwargs):
		func(*args, **kwargs) if kwargs.__contains__("world") else (lambda response=send_tcp_message({'function': 'login_unique', 'data': {'unique_id': '1'}}): func(*args, **{'token': response['data']['token'], 'world': 0}))()
	return wrapper

def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def create_family(_token,_world):
	response = send_tcp_message({'world' : 0, 'function' : 'create_family', 'data' : {'token': _token, 'name': "四大天王"}})
	print_method(str(response))

def leave_family(_token,_world):
	response = send_tcp_message({'world' : 0, 'function' : 'leave_family', 'data' : {'token': _token}})
	print_method(str(response))

def invite_user_family(_token,_world):
	response = send_tcp_message({'world' : 0, 'function' : 'invite_user_family', 'data' : {'token': _token, 'gn_target': '四大天王1'}})
	print_method(str(response))

def remove_user_family(_token,_world):
	response = send_tcp_message({'world' : 0, 'function' : 'remove_user_family', 'data' : {'token': _token, 'gn_target': '四大天王1'}})
	print_method(str(response))

def request_join_family(_token,_world):
	response = send_tcp_message({'world' : 0, 'function' : 'request_join_family', 'data' : {'token': _token, 'name': 'a'}})
	print_method(str(response))

def get_all_family(_token,_world):
	response = send_tcp_message({'world' : 0, 'function' : 'get_all_family', 'data' : {'token': _token}})
	print_method(str(response))

def get_store_family(_token,_world):
	response = send_tcp_message({'world' : 0, 'function' : 'get_store_family', 'data' : {'token': _token}})
	print_method(str(response))

def market_purchase_family(_token,_world):
	response = send_tcp_message({'world' : 0, 'function' : 'market_purchase_family', 'data' : {'token': _token, 'item':"3:6:1"}})
	print_method(str(response))

def set_notice_family(_token,_world):
	response = send_tcp_message({'world' : 0, 'function' : 'set_notice_family', 'data' : {'token': _token, 'msg':"i呜呜呜呜呜呜呜"}})
	print_method(str(response))

def set_blackboard_family(_token,_world):
	response = send_tcp_message({'world' : 0, 'function' : 'set_blackboard_family', 'data' : {'token': _token, 'msg':"i呜呜呜呜呜呜呜"}})
	print_method(str(response))

def set_role_family(_token,_world):
	response = send_tcp_message({'world' : 0, 'function' : 'set_role_family', 'data' : {'token': _token, 'gn_target':"去污","role":4}})
	print_method(str(response))

def family_dialog(token,world,info,unique_id):
	while True:
		print("1: 创建家族")
		print("2: 离开家族")
		print("3: 删除成员家族")
		print("4: 邀请某人到家族")
		print("5: 申请加入家族")
		print("6: 同意到家族中")
		print("7: 获取家族所有信息")
		print("8: 获取家族商店")
		print("9: 购买家族商店物品")
		print("10:发放家族红包")
		print("11:设置家族公告")
		print("12:设置家族黑板")
		print("13:设置家族ICON")
		print("14:更改成员位置")
		print("15:更改家族名字")
		print("16:解散家族")
		print("17:取消解散家族")
		print("18:更改家族族长")
		print("19:家族签到")
		print("20:查询家族信息")
		print("21:随机5个获取家族信息")
		print("22:获取家族配置文件")
		print("unique_id="+unique_id)
		choice = input("你的输入：")
		if choice=="1": user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'create_family', 'data' : {'token' : token, "name":"family_"+unique_id, "icon":1}})
		if choice=="2": user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'leave_family', 'data' : {'token' : token, "name":"", "icon":1}})
		if choice=="3": user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'remove_user_family', 'data' : {'token' : token, "gn_target":"name_"+"q2"}})
		if choice=="4": user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'invite_user_family', 'data' : {'token' : token, "gn_target":"name_"+"q2"}})
		if choice=="5": user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'request_join_family', 'data' : {'token' : token, "name":"family_q1"}})
		if choice=="6": user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'respond_family', 'data' : {'token' : token, "name":"", "icon":1}})
		if choice=="7": user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_all_family', 'data' : {'token' : token, "name":"", "icon":1}})
		if choice=="8": user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_store_family', 'data' : {'token' : token, "name":"", "icon":1}})
		if choice=="9": user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'market_purchase_family', 'data' : {'token' : token, "name":"", "icon":1}})
		if choice=="10":user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'welfare_purchase_family', 'data' : {'token' : token, "name":"", "icon":1}})
		if choice=="11":user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'set_notice_family', 'data' : {'token' : token, "name":"", "icon":1}})
		if choice=="12":user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'set_blackboard_family', 'data' : {'token' : token, "name":"", "icon":1}})
		if choice=="13":user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'set_icon_family', 'data' : {'token' : token, "name":"", "icon":1}})
		if choice=="14":user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'set_role_family', 'data' : {'token' : token, "name":"", "icon":1}})
		if choice=="15":user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'change_name_family', 'data' : {'token' : token, "name":"", "icon":1}})
		if choice=="16":user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'disband_family', 'data' : {'token' : token, "name":"", "icon":1}})
		if choice=="17":user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'cancel_disband_family', 'data' : {'token' : token, "name":"", "icon":1}})
		if choice=="18":user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'abdicate_family', 'data' : {'token' : token, "name":"", "icon":1}})
		if choice=="19":user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'check_in_family', 'data' : {'token' : token, "name":"", "icon":1}})
		if choice=="20":user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'search_family', 'data' : {'token' : token, "name":"", "icon":1}})
		if choice=="21":user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_random_family', 'data' : {'token' : token, "name":"", "icon":1}})
		if choice=="22":user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_config_family', 'data' : {'token' : token, "name":"", "icon":1}})

	# create_family(_token,_world)
	# leave_family(_token,_world)
	# remove_user_family(_token,_world)
	# invite_user_family(_token,_world)
	# remove_user_family(_token,_world)
	# request_join_family(_token,_world)
	# get_all_family(_token,_world)
	# market_purchase_family(_token,_world)
	# set_notice_family(_token,_world)
	# set_blackboard_family(_token,_world)
	# set_role_family(_token,_world)





if __name__ == '__main__':
	# response = send_tcp_message({'function' : 'login_unique', 'data' : {'unique_id' : '4'}})
	# print_method(str(response))
	# token = response['data']['token']
	# family_dialog(token, 0, '')
	# invite_user_family()
	pass
