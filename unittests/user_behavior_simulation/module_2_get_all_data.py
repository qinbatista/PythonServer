import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random
import module_1_login
import random
import pymysql
lukseun = tool_lukseun_client.LukseunClient('aliya',port = 8880)
world = "0"
token = ""
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))
def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

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

def get_all_role():#获取角色信息
	response = send_tcp_message({'world' : world, 'function' : 'get_all_role', 'data' : {'token' : token}})#升级请求
	print("[get_all_role]"+str(response))
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
	print_method("[get_player_info]"+str(response))
	return response

def get_all_supplies():#获取玩家所有到物资信息
	response = send_tcp_message({'world' : world, 'function' : 'get_all_supplies', 'data' : {'token' : token}})#升级请求
	print_method("[get_all_supplies]"+str(response))
	return response

def mail_gift():#获取公告奖励
	response = send_tcp_message({'world' : world, 'function' : 'mail_gift', 'data' : {'token' : token}})#升级请求
	print_method("[mail_gift]"+str(response))
	return response

def get_picture_link():#获取图片下载到链接
	response = send_tcp_message({'world' : world, 'function' : 'get_picture_link', 'data' : {'token' : token}})#升级请求
	print_method("[get_picture_link]"+str(response))
	return response

def get_all_achievement():
	response = send_tcp_message({'world' : world, 'function' : 'get_all_achievement', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张
	print_method("[get_all_achievement]"+str(response))
	return response

def get_all_resource():
	response = send_tcp_message({'world' : world, 'function' : 'get_all_resource', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张
	print_method("[get_all_resource]"+str(response))
	return response

def get_all_tower():
	response = send_tcp_message({'world' : world, 'function' : 'get_all_tower', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张
	print_method("[get_all_tower]"+str(response))
	return response

def get_all_task():
	response = send_tcp_message({'world' : world, 'function' : 'get_all_task', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张
	print_method("[get_all_task]"+str(response))
	return response

def get_all_check_in_table():
	response = send_tcp_message({'world' : world, 'function' : 'get_all_check_in_table', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张
	print_method("[get_all_check_in_table]"+str(response))
	return response

def automatically_refresh_store():
	response = send_tcp_message({'world' : world, 'function' : 'automatically_refresh_store', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张
	print_method("[automatically_refresh_store]"+str(response))
	return response

def stage_reward_config():
	response = send_tcp_message({'world' : world, 'function' : 'stage_reward_config', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张
	print_method("[stage_reward_config]"+str(response))
	return response

def get_all_vip_info():
	response = send_tcp_message({'world' : world, 'function' : 'get_all_vip_info', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张
	print_method("[get_all_vip_info]"+str(response))
	return response

def check_boss_status():
	response = send_tcp_message({'world' : world, 'function' : 'check_boss_status', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张
	print_method("[check_boss_status]"+str(response))
	return response

def get_player_config():
	response = send_tcp_message({'world' : world, 'function' : 'get_player_config', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张
	print_method("[get_player_config]"+str(response))
	return response

def get_task_config():
	response = send_tcp_message({'world' : world, 'function' : 'get_task_config', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张
	print_method("[get_task_config]"+str(response))
	return response

def get_achievement_config():
	response = send_tcp_message({'world' : world, 'function' : 'get_achievement_config', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张
	print_method("[get_achievement_config]"+str(response))
	return response

def get_all_market():
	response = send_tcp_message({'world' : world, 'function' : 'get_all_market', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张
	print_method("[get_achievement_config]"+str(response))
	return response

def get_all_info(_token,_world):
	print_module("[module_2_get_all_data] get_all_info")
	global world,token
	world = _world
	token = _token
	return [
			# get_config_stage 获取关卡的消耗列表与关卡的奖励列表entry_consumables_config.json,stage_reward_config.json 关卡 hang_reward_config.json挂机信息
			# get_config_lottery 获取lottery.json的配置文件  抽奖和转盘
			# get_config_weapon 获取weapon_config.json 武器升级的概率
			# get_config_skill 获取skill_level_up_config 技能升级的概率
			# get_config_mall 获取mall_config.json 商店的物品
			# get_config_role 获取role_config.json 角色的物品
			# get_config_task 获取task.json 任务奖励
			# get_config_achievement 获取achievement_config.json 获取成就
			# get_config_check_in 获取check_in.json 获取签到成就
			# get_config_vip 获取vip_config.json 获得vip系统
			# get_config_player 获取player_config.json（卡片兑换，体力上限，恢复时间）和player_experience.json, 玩家当前体力信息，金币数量，
			# get_config_factory   获取get_factory_config.json 获取工厂配置信息

			get_all_achievement(),
			get_all_armor(),
			get_all_resource(),
			get_all_tower(),
			get_all_task(),
			get_all_weapon(),
			get_all_check_in_table(),
			get_all_friend(),
			get_all_skill(),
			get_player_info(),
			get_all_mail(),
			automatically_refresh_store(),
			stage_reward_config(),
			get_lottery_config_info(),
			refresh_all_storage(),
			get_all_vip_info(),
			get_all_role(),
			get_factory_info(),
			get_all_family_info(),
			get_family_config(),
			check_boss_status(),
			get_task_config(),
			get_achievement_config()
			]

def _execute_statement(statement: str) -> tuple:
		db = pymysql.connect('192.168.1.102', 'root', 'lukseun', 'experimental')
		cursor = db.cursor()
		cursor.execute(statement)
		db.commit()

if __name__ == "__main__":
	pass