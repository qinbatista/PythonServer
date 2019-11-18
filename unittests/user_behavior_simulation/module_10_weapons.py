import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client as tc
import random

lukseun = tc.LukseunClient('aliya',  port = 8880)
logger = tc.logger

world = "0"
token = ""
weapon_list = [i for i in range(1,40)]
armor_list = ["armor1", "armor2", "armor3", "armor4", "armor5", "armor6", "armor7", "armor8", "armor9", "armor10"]
passive_list = [i for i in range(1,4)]
def send_tcp_message(msg):
	return asyncio.get_event_loop().run_until_complete(lukseun.send_message(str(msg).replace("'", "\"")))


def get_random_weapon():
	while True:
		int_n = random.randint(0,1)
		if int_n == 0: #金币召唤
			is_10 = random.choice([0,1])
			if is_10==0:
				new_response = send_tcp_message({'world' : world, 'function' : 'basic_summon', 'data' : {'token' : token,"cost_item":"coin"}})
			else:
				new_response = send_tcp_message({'world' : world, 'function' : 'basic_summon_10_times', 'data' : {'token' : token,"cost_item":"coin"}})#发送好友信息
			logger.debug(new_response)
			if new_response["status"]!=0:
				purchase_item_success("coin")#购买金币
				coin_item = random.randint(0,2)
				if coin_item==0:
					continue#继续抽
				elif coin_item==2:
					break#不抽


		elif int_n == 1:#高级召唤
			is_10 = random.choice([0,1])
			if is_10==0:
				new_response = send_tcp_message({'world' : world, 'function' : 'pro_summon', 'data' : {'token' : token,"cost_item":"basic_summon_scroll"}})
			else:
				new_response = send_tcp_message({'world' : world, 'function' : 'pro_summon_10_times', 'data' : {'token' : token,"cost_item":"basic_summon_scroll"}})
			if new_response["status"]!=0:
				purchase_item_success("basic_summon_scroll")#购买卷轴
				if random.choice([0,1])==0:
					continue
				else:
					break

def weapon_dialog(_token,_world,get_all_skill_info):
	global token, world
	token = _token
	world = _world
	weapon_list = [i for i in range(1,30)]

	weapon_id = random.randint(1,30)
	new_response = send_tcp_message({'world' : world, 'function' : 'level_up_weapon', 'data' : {'token' : token, "weapon":weapon_id,"amount":random.randint(30,400)}})#升级请求
	logger.debug("[get_random_weapon] coin to get weapon="+str(new_response))

	new_response = send_tcp_message({'world' : world, 'function' : 'level_up_star_weapon', 'data' : {'token' : token, "weapon":weapon_id}})#升级请求
	logger.debug("[level_up_star_weapon] level up weapon star:"+str(new_response))

	new_response = send_tcp_message({'world' : world, 'function' : 'level_up_passive_weapon', 'data' : {'token' : token, "weapon":weapon_id,"passive":random.choice(passive_list)}})#升级请求
	logger.debug("[level_up_passive_weapon] level up weapon skill"+str(new_response))

	new_response = send_tcp_message({'world' : world, 'function' : 'reset_skill_point_weapon', 'data' : {'token' : token, "weapon":weapon_id}})#升级请求
	logger.debug("[reset_skill_point_weapon] reset weapon skill"+str(new_response))

	new_response = send_tcp_message({'world' : world, 'function' : 'upgrade_armor', 'data' : {'token' : token, "aid":random.randint(1,4),"level":random.randint(1,9)}})#升级请求
	logger.debug("[weapon_dialog] level up armor star:"+str(new_response))


if __name__ == '__main__':
	response = send_tcp_message({'function': 'login_unique', 'data': {'unique_id': '1'}})
	print(response)
	token = response['data']['token']
	# response = send_tcp_message({'world': 0, 'function': 'get_all_weapon', 'data': {'token': token}})
	# response = send_tcp_message({'world': 0, 'function': 'level_up_star_weapon', 'data': {'token': token, 'weapon': 1}})
	# response = send_tcp_message({'world': 0, 'function': 'level_up_passive_weapon', 'data': {'token': token, 'weapon': 1, 'passive': 3}})
	response = send_tcp_message({'world': 0, 'function': 'reset_skill_point_weapon', 'data': {'token': token, 'weapon': 1}})
	print(response)
