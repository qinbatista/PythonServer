import json
import time
import os
import requests
import configparser
import asyncio
import user_behavior_simulation
import random
from socket import *
from time import ctime
import os 
import threading
class LukseunClient:
	def __init__(self, nonce: str = 'workingcat', host: str = '127.0.0.1', port: int = 8880):
		self._host = host
		self._port = port
		self.nonce = nonce
		self.reader=""
		self.writer=""
	async def create(self):
		self.reader, self.writer = await asyncio.open_connection(self._host, self._port)
	async def send_message(self, message: str) -> dict:
		'''
		send_message() sends the given message to the server and
		returns the decoded callback response
		'''
		# reader, writer = await asyncio.open_connection(self._host, self._port)
		self.writer.write((message + '\r\n').encode())
		await self.writer.drain()

	async def receive_message(self) -> dict:
		if self.reader._buffer==b"":
			return ""
		raw = await self.reader.readuntil(b'\r\n')
		resp = raw.decode().strip()
		# self.writer.close()
		# await self.writer.wait_closed()
		# if resp != '':
		# 	data = json.loads(resp, encoding = 'utf-8')
		# 	if 'data' in data and 'token' in data['data']:
		# 		self.token = data['data']['token']
		# 	return data
		return resp
	async def close(self, message: str) -> dict:
		self.writer.close()
		await self.writer.wait_closed()

def get_login_token_chat(token,world,info):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_login_token_chat', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张
	print(response)
	return response['data']['token']
def chat_loop(lc):
	asyncio.get_event_loop().run_until_complete(lc.create())
	asyncio.get_event_loop().run_until_complete(lc.send_message("00REGISTER"+get_login_token_chat(token,world,info)))
	print(asyncio.get_event_loop().run_until_complete(lc.receive_message()))
	asyncio.get_event_loop().run_until_complete(lc.send_message("0000PUBLICaaaaaa"))
	print(asyncio.get_event_loop().run_until_complete(lc.receive_message()))
def chat_dialog(token,world,info):
	lc = LukseunClient(get_login_token_chat(token,world,info),'192.168.1.165',9000)

	x = threading.Thread(target=chat_loop, args=(lc,))
	x.start()




if __name__ == "__main__":
	pass