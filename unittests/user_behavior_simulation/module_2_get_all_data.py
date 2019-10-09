import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random


lukseun = tool_lukseun_client.LukseunClient('aliya',port = 8880)
world = "0"
token = ""
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))
def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def get_level_info():#获取所有关卡信息
	response = send_tcp_message({'world' : int(world), 'function' : 'get_level_info', 'data' : {'token' : token}})#挑战成功
	print_method("[get_level_info]"+str(response))
	return response

def get_stage_info():#获取关卡信息消耗，奖励和设置
	response = send_tcp_message({'function' : 'get_stage_info','data':{'token' : token}})#升级请求
	print_method("[get_stage_info]"+str(response))
	return response

def get_monster_info():#获取怪物参数
	response = send_tcp_message({'function' : 'get_monster_info', 'data' : {'token' : token}})#升级请求
	print_method("[get_monster_info]"+str(response))
	return response

def get_all_friend():#获取所有朋友信息
	response = send_tcp_message({'world' : world, 'function' : 'get_all_friend', 'data' : {'token' : token}})#获取所有好友信息
	print_method("[get_all_friend]"+str(response))
	return response

def get_all_skill():#获取所有技能信息
	response = send_tcp_message({'world' : world, 'function' : 'get_all_skill', 'data' : {'token' : token}})#升级请求
	print_method("[get_all_skill]"+str(response))
	return response

def get_all_weapon():#获取所有武器信息
	response = send_tcp_message({'world' : world, 'function' : 'get_all_weapon', 'data' : {'token' : token}})#升级请求
	print_method("[get_all_weapon]"+str(response))
	return response

def refresh_all_storage():#获取所有仓库信息
	response = send_tcp_message({'world' : world, 'function' : 'refresh_all_storage','data' : {'token' : token}})
	print_method("[refresh_all_storage]"+str(response))
	return response

def get_all_roles():#获取角色信息
	response = send_tcp_message({'world' : world, 'function' : 'get_all_roles', 'data' : {'token' : token}})#升级请求
	print_method("[get_all_roles]"+str(response))
	return response

def get_factory_info():#获取工厂详细参数
	response = send_tcp_message({'world' : world, 'function' : 'get_factory_info', 'data' : {'token' : token}})#升级请求
	print_method("[get_factory_info]"+str(response))
	return response

def get_all_family_info():#获取家族详细参数
	response = send_tcp_message({'world' : world, 'function' : 'get_all_family_info', 'data' : {'token' : token}})#升级请求
	print_method("[get_all_family_info]"+str(response))
	return response

def get_all_mail():#获取所有邮件
	response = send_tcp_message({'world' : world, 'function' : 'get_all_mail', 'data' : {'token' : token}})#升级请求
	print_method("[get_all_mail]"+str(response))
	return response

def get_all_armor():#获取所有护甲信息
	response = send_tcp_message({'world' : world, 'function' : 'get_all_armor', 'data' : {'token' : token}})#升级请求
	print_method("[get_all_armor]"+str(response))
	return response

def get_lottery_config_info():#获取抽奖数值信息
	response = send_tcp_message({'world' : world, 'function' : 'get_lottery_config_info', 'data' : {'token' : token}})#升级请求
	print_method("[get_lottery_config_info]"+str(response))
	return response

def player_config():#获取玩家配置文件
	response = send_tcp_message({'world' : world, 'function' : 'player_config', 'data' : {'token' : token}})#升级请求
	print_method("[player_config]"+str(response))
	return response

def get_weapon_config():#获取武器配置
	response = send_tcp_message({'world' : world, 'function' : 'get_weapon_config', 'data' : {'token' : token}})#升级请求
	print_method("[get_weapon_config]"+str(response))
	return response

def get_skill_level_up_config():#获取技能配置
	response = send_tcp_message({'world' : world, 'function' : 'get_skill_level_up_config', 'data' : {'token' : token}})#升级请求
	print_method("[get_skill_level_up_config]"+str(response))
	return response

def get_family_config():#获取家族配置
	response = send_tcp_message({'world' : world, 'function' : 'get_family_config', 'data' : {'token' : token}})#升级请求
	print_method("[get_family_config]"+str(response))
	return response

def get_role_config():#获取角色配置
	response = send_tcp_message({'world' : world, 'function' : 'get_role_config', 'data' : {'token' : token}})#升级请求
	print_method("[get_role_config]"+str(response))
	return response

def get_hang_up_info():#获取挂机信息了
	response = send_tcp_message({'world' : world, 'function' : 'get_hang_up_info', 'data' : {'token' : token}})#升级请求
	print_method("[get_hang_up_info]"+str(response))
	return response

def get_player_info():#加载玩家体力和黑市信息
	response = send_tcp_message({'world' : world, 'function' : 'get_player_info', 'data' : {'token' : token}})#升级请求
	print_method("[get_hang_up_info]"+str(response))
	return response

def get_all_supplies():#获取玩家所有到物资信息
	response = send_tcp_message({'world' : world, 'function' : 'get_all_supplies', 'data' : {'token' : token}})#升级请求
	print_method("[get_all_supplies]"+str(response))
	return response

def mail_gift():#获取公告奖励
	response = send_tcp_message({'world' : world, 'function' : 'mail_gift', 'data' : {'token' : token}})#升级请求
	print_method("[get_all_supplies]"+str(response))
	return response

def get_picture_link():#获取图片下载到链接
	response = send_tcp_message({'world' : world, 'function' : 'get_picture_link', 'data' : {'token' : token}})#升级请求
	print_method("[get_all_supplies]"+str(response))
	return response

def get_all_achievement():#获取所有成就
	response = send_tcp_message({'world' : world, 'function' : 'get_all_achievement', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张
	print_method("[achievement_dialog]"+str(response))
	return response

def get_all_resource():#获取所有成就
	response = send_tcp_message({'world' : world, 'function' : 'get_all_resource', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张
	print_method("[get_all_resource]"+str(response))
	return response

def get_all_tower():#获取所有成就
	response = send_tcp_message({'world' : world, 'function' : 'get_all_tower', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张
	print_method("[get_all_resource]"+str(response))
	return response

def get_all_task():#获取所有成就
	response = send_tcp_message({'world' : world, 'function' : 'get_all_task', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张
	print_method("[get_all_resource]"+str(response))
	return response

def get_all_check_in_table():#获取所有成就
	response = send_tcp_message({'world' : world, 'function' : 'get_all_check_in_table', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张
	print_method("[get_all_resource]"+str(response))
	return response



def get_all_info(_token,_world):
	print_module("[module_2_get_all_data] get_all_info")
	global world,token
	world = _world
	token = _token
	get_all_achievement_str = get_all_achievement()
	get_all_armor_str = get_all_armor()
	get_all_resource_str = get_all_resource()
	get_all_tower_str = get_all_tower()
	get_all_task_str = get_all_task()
	get_all_weapon_str = get_all_weapon()
	get_all_check_in_table_str = get_all_check_in_table()
	get_all_friend_str = get_all_friend()
	get_all_skill_str = get_all_skill()
	get_player_info_str =get_player_info()
	automatically_refresh_store_str =automatically_refresh_store()
	stage_reward_config_str = stage_reward_config()
	get_lottery_config_info_str = get_lottery_config_info()
	refresh_all_storage_str = refresh_all_storage()
	get_all_vip_info_str = get_all_vip_info()
	get_all_roles_str = get_all_roles()
	get_factory_info_str = get_factory_info()
	get_all_family_info_str = get_all_family_info()
	get_family_config_str = get_family_config()
	check_boss_status_str = check_boss_status()




	return [get_level_info_str,get_stage_info_str,get_monster_info_str,get_all_friend_info_str,
	get_all_skill_level_str,get_all_weapon_str,refresh_all_storage_str,get_all_roles_str,
	get_factory_info_str,get_all_family_info_str,get_all_mail_str,get_all_armor_info_str,
	get_lottery_config_info_str,player_config_str,get_weapon_config_str,get_skill_level_up_config_str,
	get_family_config_str,get_role_config_str,get_hang_up_info_str,get_all_supplies_str,get_player_info_str,get_picture_link_str,mail_gift_str]

if __name__ == "__main__":
	pass