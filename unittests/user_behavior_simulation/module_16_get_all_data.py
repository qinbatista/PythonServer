import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random
import user_behavior_simulation
import random



def get_config_stage():
	user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_config_stage', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张

def get_config_lottery():
	user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_config_lottery', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张

def get_config_weapon():
	user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_config_weapon', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张

def get_config_skill():
	user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_config_skill', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张

def get_config_mall():
	user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_config_mall', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张

def get_config_role():
	user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_config_role', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张

def get_config_task():
	user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_config_task', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张

def get_config_achievement():
	user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_config_achievement', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张

def get_config_check_in():
	user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_config_check_in', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张

def get_config_vip():
	user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_config_vip', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张

def get_config_player():
	user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_config_player', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张

def get_config_factory():
	user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_config_factory', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张


def get_all_info(_token,_world):
	global world,token
	world = _world
	token = _token
	return [
			get_config_stage(),# 获取关卡的消耗列表与关卡的奖励列表entry_consumables_config.json,stage_reward_config.json 关卡 hang_reward_config.json挂机信息
			get_config_lottery(),# 获取lottery.json的配置文件  抽奖和转盘
			get_config_weapon (),#获取weapon_config.json 武器升级的概率
			get_config_skill (),#获取skill_level_up_config 技能升级的概率
			get_config_mall(),# 获取mall_config.json 商店的物品
			get_config_role(),# 获取role_config.json 角色的物品
			get_config_task(),# 获取task.json 任务奖励
			get_config_achievement(),# 获取achievement_config.json 获取成就
			get_config_check_in(),# 获取check_in.json 获取签到成就
			get_config_vip(),# 获取vip_config.json 获得vip系统
			get_config_player(),# 获取player_config.json（卡片兑换，体力上限，恢复时间）和player_experience.json, 玩家当前体力信息，金币数量，
			get_config_factory()#   获取get_factory_config.json 获取工厂配置信息
			]


if __name__ == "__main__":
	pass