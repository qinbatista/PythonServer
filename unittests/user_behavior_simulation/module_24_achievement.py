import json
import time
import os
import requests
import configparser
import asyncio
import tool_lukseun_client as tc
import random
import user_behavior_simulation


def get_achievement_reward(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_achievement_reward', 'data' : {'token' : token,"achievement_id":random.randint(1,1), "value":1}})



def get_all_achievement(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_all_achievement', 'data' : {'token' : token}})


def achievement_dialog(token,world):
	get_achievement_reward(token,world)
	get_all_achievement(token,world)

