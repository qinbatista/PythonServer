import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client as tc
import random
import user_behavior_simulation

def skill_dialog(token,world,get_all_skill_info):
	response = user_behavior_simulation.send_tcp_message({'world': world, 'function': 'get_all_skill', 'data': {'token' : token}})
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'level_up_skill', 'data' : {'token' : token,"skill":random.choice([i for i in range(0,38)]),"item":random.choice([6,7,8])}})#升级请求


if __name__ == "__main__":
	pass
