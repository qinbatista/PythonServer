# testing.py
MESSAGE_LIST = [
		#{'world' : '0', 'function': 'request_friend', 'data':{'gn_target' : '123456'}}
		{'world' : '0', 'function': 'get_all_mail', 'data':{}}
				]
#
# Contains test cases for the lukseun client and server.
# TODO More test cases will be added.

# lukseun_client.py
#
# A simple proof of concept client for internal use only.
# Uses asyncio to handle the sending and receipt of messages to the server.
#
import sys
sys.path.insert(0, '..')

import ssl
import asyncio
import json


class LukseunClient:
	def __init__(self, client_type: str = 'workingcat', host: str = '127.0.0.1', port: int = 8880):
		self._host = host
		self._port = port
		self.token = ""
		self.response = None

	async def send_message(self, message: str) -> dict:
		'''
		send_message() sends the given message to the server and
		returns the decoded callback response
		'''
		context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
		path = './gate/cert'
		context.load_verify_locations(path + '/mycert.crt')
		context.check_hostname = False
		#context.verify_mode = ssl.CERT_NONE
		reader, writer = await asyncio.open_connection(self._host, self._port, ssl = context)
		writer.write((message + '\r\n').encode())
		await writer.drain()
		raw = await reader.readuntil(b'\r\n')
		resp = raw.decode().strip()
		writer.close()
		await writer.wait_closed()
		if resp != '':
			data = json.loads(resp)
			print(f'received: {data}')
			self.response = data
			return data
		return {}





import time
import asyncio
import multiprocessing
import statistics
import random
import requests

COLORS = {'pass' : '\033[92m', 'fail' : '\033[91m', 'end' : '\033[0m',
		'ylw' : '\033[1;33;40m'}
client_type="aliya"
# host="192.168.1.183"
host="127.0.0.1"
token =""


def send_single_message(message_id: int):
	client = LukseunClient(client_type)
	start = time.time()
	m = MESSAGE_LIST[message_id]
	m['data']['token'] = token
	newstring  =  str(m).replace("'","\"")
	print('sending message...')
	asyncio.run(client.send_message(newstring))
	print(f"Message #{message_id} took {COLORS['pass']} {time.time() - start} {COLORS['end']} seconds to complete.")
	return client.response

def get_token():
	m = {'function': 'login_unique', 'data':{'unique_id' : 'matthewtest'}}
	client = LukseunClient(client_type)
	newstring  =  str(m).replace("'","\"")
	asyncio.run(client.send_message(newstring))
	global token
	token = client.response['data']['token']

def test_error():
	while True:
		response = send_single_message(0)
		if response['status'] == -1:
			break


def main() -> None:
	get_token()

	for i in range(len(MESSAGE_LIST)):
		send_single_message(i)


if __name__ == '__main__':
	main()




