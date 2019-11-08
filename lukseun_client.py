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
		path = './cert'
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
			data = json.loads(resp, encoding = 'utf-8')
			print(f'received: {data}')
			self.response = data
			return data
		return {}

async def main():
	lukseun = LukseunClient()
	print(await lukseun.send_message('{"function":"login_unique", "data" : {"unique_id" : "4"}}'))


if __name__ == "__main__":
	asyncio.run(main())
