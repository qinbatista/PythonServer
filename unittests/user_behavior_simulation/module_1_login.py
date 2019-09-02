import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random
lukseun = tool_lukseun_client.LukseunClient('aliya', '127.0.0.1', port = 8880)

def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))
world=""
unique_id=""

def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def login_unique():#游客登陆
	global world
	my_unique_id = unique_id
	print_module("[login_unique] unique_id="+my_unique_id)
	response = send_tcp_message({'function' : 'login_unique', 'data' : {'unique_id' : my_unique_id}})
	if response["status"]==0 or response["status"]==1:#登陆成功返回数据
		world = random.choice([0])#随机选择世界,目前世界只有0,未完成
		print_method("[login_unique] login success， world="+str(world))
		token = response["data"]["token"]
		int_number = random.choice([0,0])#登陆成功是否绑定账户0账号绑定，1手机绑定，2邮箱绑定，目前手机和邮箱未完成
		if int_number==0:
			response = send_tcp_message({'function' : 'bind_account', 'data' : {"token":token, "password":"123456","account":my_unique_id+"account","email":"","phone_number":""}})
		return token,world
	elif response["status"]==2:#账户已经被绑定
		int_number = random.choice([0,1])
		if int_number==0:
			return login_account()
		else:
			return "",""
	else:
		int_number = random.choice([0,1])
		if int_number==0:
			print_method("[login_unique] login failed, try login again")
			login_unique()
		else:
			return "",""

def login_account():#账户登陆
	my_unique_id = random.choice(["error_test_account",unique_id])
	print_module("[login_account] unique_id="+my_unique_id)
	num = random.choice(["account","account","account"])
	if num =="account": account = my_unique_id+"account"
	if num =="email": account = my_unique_id+"@email.com"
	if num =="phone_number": account = "86"+my_unique_id[9:]
	response = send_tcp_message({'function' : 'login', 'data' : {'identifier':num, "value":account, "password":"123456"}})
	world = random.choice([0])#随机选择世界,目前世界只有0,未完成
	if response["status"]==0:#登陆成功返回数据
		print_method("[login_account] login success")
		return response["data"]["token"],world
	else:#登陆失败, 0:继续尝试登陆, 1:返回空放弃登陆
		int_number = random.choice([0,1])
		if int_number==0:
			print_method("[login_account] login failed, try login again")
			login_account()
		else:
			print_method("[login_account] login failed, give up login")
			return "",""
def create_player(token):
	response = send_tcp_message({'function' : 'get_account_world_info', 'data' : {"token":token}})
	if response["status"]=="0":
		pass#创建新账户成功
	elif response["status"]=="1":
		pass#角色名字重复
	elif response["status"]=="2":
		pass#已经创建过角色，返回用户信息直接开始进入游戏流程
	else:
		pass#角色信息错误
def choice_world(token):
	response = send_tcp_message({'function' : 'choice_world', 'data' : {"token":token}})
	if response["status"]=="0":
		pass#没有角色，需要创建角色
	elif response["status"]=="1":
		pass#已有角色，直接开始进入游戏流程
def get_account_world_info(token):
	pass#返回此玩家所有世界的数据
def login_module(unique_id_p: str):
	global world,unique_id
	unique_id = "unique_id"+unique_id_p
	int_number = random.choice([0,1])
	if int_number==0:
		return login_account()
	else:
		return login_unique()

if __name__ == "__main__":
	login_module("0")