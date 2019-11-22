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
from datetime import datetime
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
		self.writer.write((message + '\r\n').encode())
		await self.writer.drain()

	async def receive_message(self) -> dict:
		raw = await self.reader.readuntil(b'\r\n')
		resp = raw.decode().strip()
		return resp
	async def close(self, message: str) -> dict:
		self.writer.close()
		await self.writer.wait_closed()

def get_login_token_chat(token,world):
	response = user_behavior_simulation.send_tcp_message({'world' : world, 'function' : 'get_login_token_chat', 'data' : {'token' : token}})#能量包，1是1张， 2是3张，3是10张
	return response['data']['token']

async def send_loop(lc):
	# while True:
	await lc.send_message("0000PUBLIC"+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

async def recv_loop(lc):
	while True:
		print(await lc.receive_message())

async def wrapper(nonce):
	client = LukseunClient(nonce, 'remote1.magicwandai.com', 9000)
	await client.create()
	await client.send_message('00REGISTER' + nonce)
	asyncio.create_task(send_loop(client))
	asyncio.create_task(recv_loop(client))
	while True:
		await asyncio.sleep(100)

def chat_dialog(token,world,info):
	nonce = get_login_token_chat(token, world)
	asyncio.get_event_loop().run_until_complete(wrapper(nonce))





if __name__ == "__main__":
	pass