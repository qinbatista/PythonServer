import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client as tc
import random
import user_behavior_simulation

lukseun = tc.LukseunClient('aliya', port = 8880)
logger = tc.logger


def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))

# def login_decoration(func):
# 	def wrapper(token,world):
# 		func(token,world) if kwargs.__contains__("world") else (lambda response=send_tcp_message({'function': 'login_unique', 'data': {'unique_id': '1'}}): func(**{'token': response['data['token, 'world': 0}))()
# 	return wrapper

#
def basic_summon(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'basic_summon', 'data' : {'token' : token,"item":random.choice([1,5])}})


#
def pro_summon(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'pro_summon', 'data' : {'token' : token,"item":random.choice([1,5])}})


#
def friend_summon(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'friend_summon', 'data' : {'token' : token,"item":random.choice([1,5])}})


#
def basic_summon_skill(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'basic_summon_skill', 'data' : {'token' : token,"item":random.choice([1,5])}})


#
def pro_summon_skill(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'pro_summon_skill', 'data' : {'token' : token,"item":random.choice([1,5])}})


#
def friend_summon_skill(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'friend_summon_skill', 'data' : {'token' : token,"item":random.choice([1,5])}})


#
def basic_summon_role(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'basic_summon_role', 'data' : {'token' : token,"item":random.choice([1,5])}})


#
def pro_summon_role(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'pro_summon_role', 'data' : {'token' : token,"item":random.choice([1,5])}})


#
def friend_summon_role(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'friend_summon_role', 'data' : {'token' : token,"item":random.choice([1,5])}})


#
def basic_summon_10_times(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'basic_summon_10_times', 'data' : {'token' : token,"item":random.choice([1,5])}})



def pro_summon_10_times(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'basic_summon_10_times', 'data' : {'token' : token,"item":random.choice([1,5])}})



def friend_summon_10_times(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'friend_summon_10_times', 'data' : {'token' : token,"item":random.choice([1,5])}})#能量包，1是1张， 2是3张，3是10张



def basic_summon_skill_10_times(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'basic_summon_skill_10_times', 'data' : {'token' : token,"item":random.choice([1,5])}})#能量包，1是1张， 2是3张，3是10张



def pro_summon_skill_10_times(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'pro_summon_skill_10_times', 'data' : {'token' : token,"item":random.choice([1,5])}})#能量包，1是1张， 2是3张，3是10张



def friend_summon_skill_10_times(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'friend_summon_skill_10_times', 'data' : {'token' : token,"item":random.choice([1,5])}})#能量包，1是1张， 2是3张，3是10张



def basic_summon_role_10_times(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'basic_summon_role_10_times', 'data' : {'token' : token,"item":random.choice([1,5])}})#能量包，1是1张， 2是3张，3是10张



def pro_summon_role_10_times(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'pro_summon_role_10_times', 'data' : {'token' : token,"item":random.choice([1,5])}})#能量包，1是1张， 2是3张，3是10张



def friend_summon_role_10_times(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'friend_summon_role_10_times', 'data' : {'token' : token,"item":random.choice([1,5])}})#能量包，1是1张， 2是3张，3是10张


def summon_dialog(token,world):
	basic_summon(token,world)
	pro_summon(token,world)
	friend_summon(token,world)

	basic_summon_skill(token,world)
	pro_summon_skill(token,world)
	friend_summon_skill(token,world)

	basic_summon_role(token,world)
	pro_summon_role(token,world)
	friend_summon_role(token,world)

	basic_summon_10_times(token,world)
	pro_summon_10_times(token,world)
	friend_summon_10_times(token,world)

	basic_summon_skill_10_times(token,world)
	pro_summon_skill_10_times(token,world)
	friend_summon_skill_10_times(token,world)

	basic_summon_role_10_times(token,world)
	pro_summon_role_10_times(token,world)
	friend_summon_role_10_times(token,world)



if __name__ == '__main__':
	# response = send_tcp_message({'function': 'login_unique', 'data': {'unique_id': '1'}})
	# # response = send_tcp_message({'function': 'login_unique', 'data': {'unique_id': '12'}})
	# print(response)
	# response = send_tcp_message({'world': 0, 'function': 'basic_summon', 'data': {'token': token, "item":random.choice([1, 5, 11])}})
	# response = send_tcp_message({'world': 0, 'function': 'friend_summon', 'data': {'token': token, "item":random.choice([1, 5, 11])}})
	# response = send_tcp_message({'world': 0, 'function': 'check_boss_status', 'data': {'token': token, "item": 11}})
	# response = send_tcp_message({'world': 0, 'function': 'update_worker_factory', 'data': {'token': token, "worker": {"0": 0, "1": 1, "2": 0}}})
	# response = send_tcp_message({'world': 0, 'function': 'check_boss_status', 'data': {'token': token, 'page': 1, 'item': 6}})
	# response = send_tcp_message({'world': 0, 'function': 'get_top_damage', 'data': {'token': token, "page": 1}})
	# response = send_tcp_message({'world': 0, 'function': 'enter_stage', 'data': {'token': token, "stage": 1, "damage": 110000}})
	# response = send_tcp_message({'world': 0, 'function': 'pass_stage', 'data': {'token': token, "stage": 3000, "damage": 110001}})
	# response = send_tcp_message({'world': 0, 'function': 'invite_user_family', 'data': {'token': token, "gn_target": 'matthewtesting'}})
	# response = send_tcp_message({'world': 0, 'function': 'respond_family', 'data': {'token': token, "key": '1573454081.M824901P5352Q255.debian'}})
	# response = send_tcp_message({'world': 0, 'function': 'set_role_family', 'data': {'token': token, "gn_target": 'matthewtesting', 'role': 4}})
	# response = send_tcp_message({'world': 0, 'function': 'set_notice_family', 'data': {'token': token, "msg": '仅仅是测试'}})
	# response = send_tcp_message({'world': 0, 'function': 'set_blackboard_family', 'data': {'token': token, "msg": '仅仅是公告测试'}})
	# response = send_tcp_message({'world': 0, 'function': 'get_all_family', 'data': {'token': token, "msg": '仅仅是公告测试'}})
	# response = send_tcp_message({'world': 0, 'function': 'get_store_family', 'data': {'token': token, "msg": '仅仅是公告测试'}})
	# response = send_tcp_message({'world': 0, 'function': 'market_purchase_family', 'data': {'token': token, "item": '3:6:1'}})
	# response = send_tcp_message({'world': 0, 'function': 'change_name_family', 'data': {'token': token, "name": '1newname'}})
	# response = send_tcp_message({'world': 0, 'function': 'disband_family', 'data': {'token': token, "name": '1newname'}})
	# response = send_tcp_message({'world': 0, 'function': 'remove_user_family', 'data': {'token': token, "gn_target": '哈哈'}})
	# response = send_tcp_message({'world': 0, 'function': 'request_join_family', 'data': {'token': token, "name": '1newname'}})
	# response = send_tcp_message({'world': 0, 'function': 'get_new_mail', 'data': {'token': token, "name": '1newname'}})
	# response = send_tcp_message({'world': 0, 'function': 'get_all_mail', 'data': {'token': token, "name": '1newname'}})
	# response = send_tcp_message({'world': 0, 'function': 'get_all_role', 'data': {'token': token, "name": '1newname'}})
	# response = send_tcp_message({'world': 0, 'function': 'level_up_role', 'data': {'token': token, 'role': 1, "amount": '10'}})
	# response = send_tcp_message({'world': 0, 'function': 'level_up_star_role', 'data': {'token': token, 'role': 1, "amount": '10'}})
	# response = send_tcp_message({'world': 0, 'function': 'get_config_role', 'data': {'token': token, 'role': 1, "amount": '10'}})
	# response = send_tcp_message({'world': 0, 'function': 'get_task_reward', 'data': {'token': token, 'task_id': 1, "amount": '10'}})
	# response = send_tcp_message({'world': 0, 'function': 'get_all_task', 'data': {'token': token, 'task_id': 1, "amount": '10'}})
	# response = send_tcp_message({'world': 0, 'function': 'get_achievement_reward', 'data': {'token': token, 'achievement_id': 1, "amount": '10'}})
	# print(str(response).replace("'", "\""))
	# response = send_tcp_message({'world': 0, 'function': 'get_all_achievement', 'data': {'token': token, 'achievement_id': 1, "amount": '10'}})
	# response = send_tcp_message({'world': 0, 'function': 'get_all_market', 'data': {'token': token, 'achievement_id': 1, "amount": '10'}})
	# response = send_tcp_message({'world': 0, 'function': 'darkmarket_transaction', 'data': {'token': token, 'pid': 1}})
	# response = send_tcp_message({'world': 0, 'function': 'exchange_card', 'data': {'token': token, 'card_id': 19}})
	# response = send_tcp_message({'world': 0, 'function': 'get_info_player', 'data': {'token': token, 'card_id': 19}})
	# response = send_tcp_message({'world': 0, 'function': 'find_person', 'data': {'token': token, 'gn_target': '打广告'}})
	# response = send_tcp_message({'world': 0, 'function': 'get_config_player', 'data': {'token': token, 'gn_target': '打广告'}})
	# response = send_tcp_message({'world': 0, 'function': 'get_config_card', 'data': {'token': token, 'card_id': 19}})
	# response = send_tcp_message({'world': 0, 'function': 'check_in_family', 'data': {'token': token, 'card_id': 18}})
	# response = send_tcp_message({'world': 0, 'function': 'refresh_market', 'data': {'token': token, 'pid': 1}})
	# response = send_tcp_message({'world': 0, 'function': 'get_config_family', 'data': {'token': token, 'pid': 1}})
	# response = send_tcp_message({'world': 0, 'function': 'get_vip_daily_reward', 'data': {'token': token}})
	# response = send_tcp_message({'world': 0, 'function': 'purchase_vip_card', 'data': {'token': token, 'card_id': 27}})
	# response = send_tcp_message({'world': 0, 'function': 'get_config_vip', 'data': {'token': token, 'card_id': 27}})
	# response = send_tcp_message({'world': 0, 'function': 'get_info_vip', 'data': {'token': token, 'card_id': 27}})
	# response = send_tcp_message({'world': 0, 'function': 'purchase_vip_gift', 'data': {'token': token, 'tier': 1}})
	# response = send_tcp_message({'world': 0, 'function': 'fortune_wheel_pro', 'data': {'token': token, 'item': 5}})
	# response = send_tcp_message({'world': 0, 'function': 'check_in', 'data': {'token': token, 'item': 5}})
	# response = send_tcp_message({'world': 0, 'function': 'supplement_check_in', 'data': {'token': token, 'item': 5}})
	# response = send_tcp_message({'world': 0, 'function': 'get_account_world_info', 'data': {'token': token, 'item': 5}})
	# response = send_tcp_message({'world': 0, 'function': 'basic_summon', 'data': {'token': token, 'item': 1}})
	world = "s1"
	token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1Nzg3MjgxMzEsInVpZCI6ImgwMDAifQ.C_CRmyMSK8a1MxW74UfwzmfraVJ74XYt2wqYkn0xgo4"
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'integral_convert', 'data': {'token' : token}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'refresh_diamond_store', 'data': {'token' : token}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'single_pump_gift', 'data': {'token' : token}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'single_pump_coin', 'data': {'token' : token}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'dozen_pump_diamond', 'data': {'token' : token}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'single_pump_diamond', 'data': {'token' : token}})
	user_behavior_simulation.send_tcp_message({'world': world, 'function': 'refresh_coin_store', 'data': {'token' : token}})
	# user_behavior_simulation.send_tcp_message({'world': world, 'function': 'refresh_gift_store', 'data': {'token' : token}})




