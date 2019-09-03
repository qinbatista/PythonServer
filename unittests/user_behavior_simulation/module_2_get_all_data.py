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
token = ""
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))
def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def get_level_info():#获取所有关卡信息
	response = send_tcp_message({'world' : int(world), 'function' : 'get_hang_up_info', 'data' : {'token' : token}})#挑战成功
	print_method("[get_level_info]"+str(response))
	return response

def get_stage_info():#获取关卡信息消耗，奖励和设置
	response = send_tcp_message({'world' : world, 'function' : 'get_stage_info', 'data' : {'token' : token}})#升级请求
	print_method("[get_stage_info]"+str(response))
	return response

def get_monster_info():#获取怪物参数
	response = send_tcp_message({'world' : world, 'function' : 'get_monster_info', 'data' : {'token' : token}})#升级请求
	print_method("[get_monster_info]"+str(response))
	return response

def get_all_friend_info():#获取所有朋友信息
	response = send_tcp_message({'world' : world, 'function' : 'get_all_friend_info', 'data' : {'token' : token}})#获取所有好友信息
	print_method("[get_all_friend_info]"+str(response))
	return response

def get_all_skill_level():#获取所有技能信息
	response = send_tcp_message({'world' : world, 'function' : 'get_all_skill_level', 'data' : {'token' : token}})#升级请求
	print_method("[get_all_skill_level]"+str(response))
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

def get_all_armor_info():#获取所有护甲信息
	response = send_tcp_message({'world' : world, 'function' : 'get_all_armor_info', 'data' : {'token' : token}})#升级请求
	print_method("[get_all_armor_info]"+str(response))
	return response

def get_lottery_config():#获取抽奖数值信息
	response = send_tcp_message({'world' : world, 'function' : 'get_lottery_config', 'data' : {'token' : token}})#升级请求
	print_method("[get_lottery_config]"+str(response))
	return response

def get_all_info(_token,_world):
	print_module("[module_2_get_all_data] get_all_info")
	global world,token
	world = _world
	token = _token
	return get_level_info(),get_all_friend_info(),get_all_skill_level(),get_all_weapon(),refresh_all_storage(),get_all_roles(),get_stage_info(),get_monster_info(),get_factory_info(),get_all_family_info(),get_all_mail(),get_all_armor_info()

if __name__ == "__main__":
	pass