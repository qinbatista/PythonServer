import json
import time
import os
import configparser
import asyncio
import tool_lukseun_client
import random
lukseun = tool_lukseun_client.LukseunClient('aliya', port = 8880)

def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))
world=""
unique_id=""

def print_method(my_string):
	print("\033[0;37;44m\t"+my_string+"\033[0m")
def print_module(my_string):
	print("\033[0;37;41m\t"+my_string+"\033[0m")

def get_token(my_unique_id):#模拟登录
	print_module("[get_token] unique_id="+my_unique_id)
	num = random.choice(["account","account","account"])
	if num =="account": account = my_unique_id+"account"
	if num =="email": account = my_unique_id+"@email.com"
	if num =="phone_number": account = "86"+my_unique_id[9:]
	response = send_tcp_message({'function' : 'login', 'data' : {'identifier':num, "value":account, "password":"123456"}})
	if response["status"]==0:
		return response["data"]["token"]
	else:
		return False
def login_unique():#游客登陆
	global world
	my_unique_id = unique_id
	print_module("[login_unique] unique_id="+my_unique_id)
	response = send_tcp_message({'function' : 'login_unique', 'data' : {'unique_id' : my_unique_id}})
	print(str(response))
	if response["status"]==0 or response["status"]==1:#登陆成功返回数据
		world = random.choice([0])#随机选择世界,目前世界只有0,未完成
		print_method("[login_unique] login success, token="+response["data"]["token"] + ",world="+str(world))
		token = response["data"]["token"]
		world_list = get_account_world_info(token)
		if len(world_list) != 0:
			world = enter_world(token, random.randint(0,len(world_list)-1))#选择世界,游客登陆需要返回一个用户不是很忙的服务器,目前只有世界0,未完成
		else:
			return "",""
		int_number = random.choice([0,0])#登陆成功是否绑定账户0账号绑定，1手机绑定，2邮箱绑定，目前手机和邮箱未完成
		if int_number==0:
			response = send_tcp_message({'function' : 'bind_account', 'data' : {"token":token, "password":"123456","account":my_unique_id+"account","email":"","phone_number":""}})
			print(str(response))
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
	my_unique_id = unique_id
	print_module("[login_account] unique_id="+my_unique_id)
	num = random.choice(["account","account","account"])
	if num =="account": account = my_unique_id+"account"
	if num =="email": account = my_unique_id+"@email.com"
	if num =="phone_number": account = "86"+my_unique_id[9:]
	response = send_tcp_message({'function' : 'login', 'data' : {'identifier':num, "value":account, "password":"123456"}})
	print(str(response))
	if response["status"]==0:
		token = response["data"]["token"]
	else:
		return login_unique()
	world_list = get_account_world_info(token)
	if len(world_list) != 0:
		world = enter_world(token, random.randint(0,0))#选择世界,游客登陆需要返回一个用户不是很忙的服务器,目前只有世界0,未完成

	if response["status"]==0:#登陆成功返回数据
		print_method("[login_account] login success, response="+str(response))
		return token,world
	else:#登陆失败, 0:继续尝试登陆, 1:返回空放弃登陆
		int_number = random.choice([0,1])
		if int_number==0:
			print_method("[login_account] login failed, try login again")
			return login_account()
		else:
			print_method("[login_account] login failed, give up login")
			return "",""


def enter_world(token,target_world):
	print_module("[enter_world]")
	response = send_tcp_message({'function' : 'enter_world', 'data' : {"token":token,"target_world":target_world}})
	print(str(response))
	if response["status"]==0:#已有角色，正常进入
		return target_world
	else:
		return create_player(token,target_world,"name_"+unique_id)

def create_player(token,target_world,game_name):
	print_module("[create_player] create user name="+game_name)
	response = send_tcp_message({"world":target_world,'function' : 'create_player', 'data' : {"token":token,"gn":game_name}})
	print(str(response))
	if response["status"]==0:#角色创建成功,返回世界
		return target_world
	elif response["status"]==98 or response["status"]==99:#角色名字重复
		print_method(f"repeated name name_{unique_id}, renamed again")
		return create_player(token,target_world,"name_fix_"+str(random.randint(0,999)))
	elif response["status"]==1:
		return target_world#已经创建过角色，返回用户信息直接开始进入游戏流程

def get_account_world_info(token):
	print_module("[get_account_world_info]")
	response = send_tcp_message({'function' : 'get_account_world_info', 'data' : {"token":token}})
	print(str(response))
	# response = {"status":0,"data":{"remaining": [{"word1":{"game_name":"","level":"2222","server_status":"0"}}]}}
	if response["status"]==0:#返回世界信息
		return response["data"]["worlds"]
	else:#返回错误，不再继续剩下流程
		return []
def login_module(unique_id_p: str):
	global world,unique_id
	unique_id = unique_id_p
	int_number = random.choice([0,1])
	if int_number==0:
		return login_account()
	else:
		return login_unique()

if __name__ == "__main__":
	login_module("0")