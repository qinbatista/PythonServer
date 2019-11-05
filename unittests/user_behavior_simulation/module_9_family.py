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

def family_dialog(_token,_world,info):
	create_family(_token,_world)
	# leave_family(_token,_world)
	invite_user_family(_token,_world)
	# remove_user_family(_token,_world)
	# request_join_family(_token,_world)
	# get_all_family(_token,_world)
	# market_purchase_family(_token,_world)
	# set_notice_family(_token,_world)
	# set_blackboard_family(_token,_world)
	# set_role_family(_token,_world)

	return
	print_module("player_info="+str(info))
	print_module("get_all_family_info="+str(info))
	myLevel = info["data"]["remaining"]["level"]

	if myLevel<18:
		response = send_tcp_message({'world' : 0, 'function' : 'request_join_family', 'data' : {'token': token, 'fname': 'family_name_'+str(random.randint(0,user_behavior_simulation.testing_people_number))}})
		print_method(str(response))
	else:
		response = send_tcp_message({'world' : 0, 'function' : 'create_family', 'data' : {'token': token, 'fname': 'family_name_'+user_behavior_simulation.unique_id}})
		print_method(str(response))



	response = send_tcp_message({'world' : 0, 'function' : 'family_sign_in', 'data' : {'token': token}})
	print_method(str(response))


	response = send_tcp_message({'world' : 0, 'function' : 'invite_user_family', 'data' : {'token': token, 'target': 'name_unique_id'+user_behavior_simulation.unique_id}})
	print_method(str(response))

	# response = send_tcp_message({'world' : 0, 'function' : 'respond_family', 'data' : {'token': token, 'nonce': '234567899'}})#玩家接受加入家族的邀请
	# print(response)

	response = send_tcp_message({'world' : 0, 'function' : 'family_officer', 'data' : {'token': token, 'target': 'game name', 'position': random.randint(0,3)}})
	print_method(str(response))

	response = send_tcp_message({'world' : 0, 'function' : 'dismissal_family_officer', 'data' : {'token': token, 'target': '123'}})
	print_method(str(response))

	response = send_tcp_message({'world' : 0, 'function' : 'family_change_name', 'data' : {'token': token, 'family_name': 'name_unique_id_rename_'+user_behavior_simulation.unique_id}})
	print_method(str(response))

	response = send_tcp_message({'world' : 0, 'function' : 'family_blackboard', 'data' : {'token': token}})#刷新工会信息
	print_method(str(response))

	response = send_tcp_message({'world' : 0, 'function' : 'family_announcement', 'data' : {'token': token}})
	print_method(str(response))

	response = send_tcp_message({'world' : 0, 'function' : 'get_family_store', 'data' : {'token': token}})
	print_method(str(response))

	response = send_tcp_message({'world' : 0, 'function' : 'family_market_purchase', 'data' : {'token': token, 'merchandise': 'merchandise'}})
	print_method(str(response))

	response = send_tcp_message({'world' : 0, 'function' : 'family_gift_package', 'data' : {'token': token}})
	print_method(str(response))

	response = send_tcp_message({'world' : 0, 'function' : 'get_family_config', 'data' : {'token': token}})
	print_method(str(response))

	response = send_tcp_message({'world' : 0, 'function' : 'remove_user_family', 'data' : {'token': token, 'user': 'game name'}})
	print_method(str(response))

	response = send_tcp_message({'world' : 0, 'function' : 'disbanded_family', 'data' : {'token': token}})
	print_method(str(response))

	response = send_tcp_message({'world' : 0, 'function' : 'cancel_disbanded_family', 'data' : {'token': token}})
	print_method(str(response))

	response = send_tcp_message({'world' : 0, 'function' : 'leave_family', 'data' : {'token': token}})
	print_method(str(response))




if __name__ == '__main__':
	# response = send_tcp_message({'function' : 'login_unique', 'data' : {'unique_id' : '4'}})
	# print_method(str(response))
	# token = response['data']['token']
	# family_dialog(token, 0, '')
	# invite_user_family()
	pass
