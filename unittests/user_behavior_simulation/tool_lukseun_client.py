# lukseun_client.py
#
# A simple proof of concept client for internal use only.
# Uses asyncio to handle the sending and receipt of messages to the server.
#
import sys, os
import ssl
sys.path.insert(0, '..')

import asyncio
import json
import logging
logging.basicConfig(
	level=logging.DEBUG,
	format='%(asctime)s [%(filename)s] [%(funcName)s][line:%(lineno)d] %(levelname)s message：%(message)s',
	datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)
print = logging.getLogger(__name__).debug


def loc():
	return os.path.dirname(os.path.realpath(__file__))

class LukseunClient:
	def __init__(self, client_type: str = 'workingcat', host: str = '127.0.0.1', port: int = 8880):
		self._host = host
		self._port = port
		self.token = ""

	async def send_message(self, message: str) -> dict:
		'''
		send_message() sends the given message to the server and
		returns the decoded callback response
		'''
		context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
		# 加载服务器所用证书和私钥
		context.load_verify_locations(os.path.join(loc() + '/../../gate/cert/mycert.crt'))
		context.check_hostname = False
		reader, writer = await asyncio.open_connection(self._host, self._port, ssl=context)

		writer.write((message + '\r\n').encode())
		await writer.drain()
		raw = await reader.readuntil(b'\r\n')
		resp = raw.decode().strip()
		writer.close()
		await writer.wait_closed()
		if resp != '':
			data = json.loads(resp, encoding = 'utf-8')
			if 'data' in data and 'token' in data['data']:
				self.token = data['data']['token']
			return data
		return {}

async def main():
	lukseun = LukseunClient()
	print(await lukseun.send_message('{"function":"login_unique", "data" : {"unique_id" : "4"}}'))


if __name__ == "__main__":
	asyncio.run(main())
