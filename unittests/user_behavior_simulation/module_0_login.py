import json
import time
import os
import configparser
import asyncio
import tool_lukseun_client
import random
import user_behavior_simulation

lukseun = tool_lukseun_client.LukseunClient('aliya', port=8880)


def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))


world = ""
unique_id = ""


def get_token(my_unique_id):  # 模拟登录
	num = random.choice(["account", "account", "account"])
	if num == "account": account = "account_" + my_unique_id
	if num == "email": account = my_unique_id + "@email.com"
	if num == "phone_number": account = "86" + my_unique_id[9:]
	response = user_behavior_simulation.send_tcp_message({'function': 'login', 'data': {'identifier': num, "value": account, "password": "123456"}})
	if response["status"] == 0:
		return response["data"]["token"]
	else:
		return False


def login_unique():  # 游客登陆
	global world
	my_unique_id = unique_id
	response = user_behavior_simulation.send_tcp_message(
		{'function': 'login_unique', 'data': {'unique_id': my_unique_id}})
	if response["status"] == 0 or response["status"] == 1:  # 登陆成功返回数据
		world = random.choice([0])  # 随机选择世界,目前世界只有0,未完成
		token = response["data"]["token"]
		world_list = get_account_world_info(token)
		if len(world_list) != 0:
			max = len(world_list) - 1
			world = enter_world(token, world_list[random.randint(0, 0)]["world"])  # 选择世界,游客登陆需要返回一个用户不是很忙的服务器,目前只有世界0,未完成
		else:
			return "", ""
		int_number = random.choice([0, 0])  # 登陆成功是否绑定账户0账号绑定，1手机绑定，2邮箱绑定，目前手机和邮箱未完成
		if int_number == 0:
			response = user_behavior_simulation.send_tcp_message({'function': 'bind_account', 'data': {"token": token, "password": "123456", "account": "account_" + my_unique_id, "email": "", "phone_number": ""}})
		return token, world
	elif response["status"] == 2:  # 账户已经被绑定
		int_number = random.choice([0, 1])
		if int_number == 0:
			return login_account()
		else:
			return "", ""
	else:
		return "", ""


def login_account():  # 账户登陆
	global world
	my_unique_id = unique_id
	num = random.choice(["account", "account", "account"])
	if num == "account": account = "account_" + my_unique_id
	if num == "email": account = my_unique_id + "@email.com"
	if num == "phone_number": account = "86" + my_unique_id[9:]
	response = user_behavior_simulation.send_tcp_message(
		{'function': 'login', 'data': {'identifier': num, "value": account, "password": "123456"}})
	if response["status"] == 0:
		token = response["data"]["token"]
	else:
		return login_unique()
	world_list = get_account_world_info(token)
	if len(world_list) != 0:
		# world = enter_world(token, random.randint(0,0))#选择世界,游客登陆需要返回一个用户不是很忙的服务器,目前只有世界0,未完成
		world = enter_world(token, "s0")  # 选择世界,游客登陆需要返回一个用户不是很忙的服务器,目前只有世界0,未完成

	if response["status"] == 0:  # 登陆成功返回数据
		return token, world
	else:  # 登陆失败, 0:继续尝试登陆, 1:返回空放弃登陆
		int_number = random.choice([0, 1])
		if int_number == 0:
			return login_account()
		else:
			return "", ""


def enter_world(token, target_world):
	response = user_behavior_simulation.send_tcp_message(
		{'function': 'enter_world', 'world': str(target_world), 'data': {"token": token, "target_world": target_world}})
	if response["status"] == 0:  # 已有角色，正常进入
		return target_world
	else:
		return create_player(token, target_world, "name_" + unique_id)


def create_player(token, target_world, game_name):
	response = user_behavior_simulation.send_tcp_message(
		{"world": target_world, 'function': 'create_player', 'data': {"token": token, "gn": game_name}})
	if response["status"] == 0:  # 角色创建成功,返回世界
		return target_world
	elif response["status"] == 98 or response["status"] == 99:  # 角色名字重复
		return create_player(token, target_world, "name_fix_" + str(random.randint(0, 999)))
	elif response["status"] == 1:
		return target_world  # 已经创建过角色，返回用户信息直接开始进入游戏流程


def get_account_world_info(token):
	response = user_behavior_simulation.send_tcp_message(
		{'function': 'get_account_world_info', 'data': {"token": token}})
	# response = {"status":0,"data":{"remaining": [{"word1":{"game_name":"","level":"2222","server_status":"0"}}]}}
	if response["status"] == 0:  # 返回世界信息
		return response["data"]["worlds"]
	else:  # 返回错误，不再继续剩下流程
		return []


def login_module(unique_id_p: str):
	global world, unique_id
	unique_id = unique_id_p
	int_number = random.choice([0, 1])
	if int_number == 0:
		return login_account()
	else:
		return login_unique()


if __name__ == "__main__":
	# login_module("0")
	# token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODA4OTQwOTQsInVpZCI6IjAwNTNmOWRjYWZlZDQ5MzFhNmQ2MTZiZDA2YWFhMWFhIn0.UyA_Sf-UlcJ1xKQLay6YDx4CPiD-eItFfGyX9j6Femg"
	token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzkxNjE4MjMsInVpZCI6IjAifQ.sAnQoaJ5ZWxxUjKcOcR-QZ7W2BsKpIPPeNEiBavHlbU"
	world = "s1"
	user_behavior_simulation.send_tcp_message({"world": world, 'function': 'get_info_player', 'data': {"token": token, "gn": "tgn0"}})
	# user_behavior_simulation.send_tcp_message({"world": world, 'function': 'enter_stage', 'data': {"token": token, "stage": 1001}})
	# user_behavior_simulation.send_tcp_message({"world": world, 'function': 'create_player', 'data': {"token": token, "gn": "tgn0"}})
	# user_behavior_simulation.send_tcp_message({"world": world, 'function': 'account_all_info', 'data': {"token": token, "email": "2428437133@qq.com"}})
	# user_behavior_simulation.send_tcp_message({"world": world, 'function': 'bind_email', 'data': {"token": token, "email": "2428437133@qq.com"}})
	# code = input("code:")
	# user_behavior_simulation.send_tcp_message({"world": world, 'function': 'verify_email_code', 'data': {"token": token, "code": code, "status": 0}})
	# user_behavior_simulation.send_tcp_message({"world": world, 'function': 'unbind_email', 'data': {"token": token, "email": "2428437133@qq.com"}})
	# code = input("code:")
	# user_behavior_simulation.send_tcp_message({"world": world, 'function': 'verify_email_code', 'data': {"token": token, "code": code, "status": 1}})
	# user_behavior_simulation.send_tcp_message({"world": world, 'function': 'bind_phone', 'data': {"token": token, "phone_number": "18323019610"}})
	# code = input("code:")
	# user_behavior_simulation.send_tcp_message({"world": world, 'function': 'verify_phone_code', 'data': {"token": token, "code": code, "status": 0}})
	# user_behavior_simulation.send_tcp_message({"world": world, 'function': 'unbind_phone', 'data': {"token": token, "phone_number": "18323019610"}})
	# code = input("code:")
	# user_behavior_simulation.send_tcp_message({"world": world, 'function': 'verify_phone_code', 'data': {"token": token, "code": code, "status": 1}})
