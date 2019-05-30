import sys
import json
import time
import os
import codecs
import threading
import pymysql
import datetime;
import random
def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
from Utility import LogRecorder,EncryptionAlgorithm
from Utility.LogRecorder import LogUtility as Log
from Utility.sql_manager import game_aliya as gasql
DESKey = "67891234"
DESVector = "6789123467891234"

MessageList=[
	"{\"status\":\"0\",\"message\":\"success\"}",
	"{\"status\":\"1\",\"message\":\"failed\",\"time\":\"%s\"}"
]
class SkillSystemClass():
	def __init__(self, *args, **kwargs):
		pass
	def _skill_level_up(self,message_info):
		"""
		level up skill, if skill level is 0, can't level up, level up skill need scroll, scroll have probability to level up.
		"""
		pass
	def _get_all_skill_level(self,message_info):
		"""
		give all skills' level to client
		"""
		pass
if __name__ == "__main__":
	pass

