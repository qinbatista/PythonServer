import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client
import random
import user_behavior_simulation


def get_all_task(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_all_task', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张

def get_task_reward(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_task_reward', 'data' : {'token' : token,"task_id":random.randint(1,7)}})#能量包，1是1张， 2是3张，3是10张


def task_dialog(token,world,respons):
	get_all_task(token,world)
	get_task_reward(token,world)





