# lukseun_client.py
#
# A simple proof of concept client for internal use only.
# Uses asyncio to handle the sending and receipt of messages to the server.
#
import sys
sys.path.insert(0, '..')

import pyDes
import base64
import asyncio
import json
import message_handler as handler



DESIv = '67891234'
DESKey = '6789123467891234'

MD5_ALIYA = b'e3cb970693574ea75d091a6049f8a3ff'

# the size of the header in bytes that we will send to and receive from the server.
HEADER_BUFFER_SIZE = 37


class LukseunClient:
	def __init__(self, client_type: str = 'workingcat', host: str = '127.0.0.1', port: int = 8888):
		self._client_type = client_type
		self._host = host
		self._port = port
		self._k = pyDes.triple_des(DESKey, pyDes.CBC, DESIv, pad=None, padmode=pyDes.PAD_PKCS5)
		self._handler = handler.MessageHandler()
		self.token = ""
	
	async def send_message(self, message: str) -> dict:
		'''
		send_message() sends the given message to the server and
		returns the decoded callback response
		'''
		reader, writer = await asyncio.open_connection(self._host, self._port)
		
		encoded_message = self._encode_message(message)
		await self._send_header(writer, self._make_header(len(encoded_message)))
		await self._send_message(writer, encoded_message)
		response = await self._receive_response(reader)
		writer.close()
		decoded_message = self._decode_message(response)
		if decoded_message != '':
			return json.loads(decoded_message, encoding='utf-8')
		return {}
	
	async def _send_header(self, writer: asyncio.StreamWriter, header: bytes) -> None:
		'''
		_send_header() sends the header to the server which contains the size of the
		message that we will send next.
		'''
		writer.write(header)
		await writer.drain()
	
	#	Log('[lukseun_client.py][_send_header()] Sent header {} to {}'.format(bytes.decode(header), writer.get_extra_info('peername')))
	
	async def _send_message(self, writer: asyncio.StreamWriter, message: bytes) -> None:
		'''
		_send_message() sends the encrypted message to the server. called after
		the header has already been sent to the server.
		'''
		writer.write(message)
		await writer.drain()
	
	#	Log('[lukseun_client.py][_send_message()] Sent message {} to {}'.format(bytes.decode(message), writer.get_extra_info('peername')))
	
	async def _receive_response(self, reader: asyncio.StreamReader) -> bytes:
		'''
		_receive_response() receives the callback response from the server.
		'''
		header_raw = await reader.read(HEADER_BUFFER_SIZE)
		size = self._handler.is_valid_header(header_raw)
		response = await reader.read(size)
		# Log('[lukseun_client.py][_receive_response()] Received response {} from server'.format(bytes.decode(response)))
		return response
	
	def _make_header(self, message_len: int) -> bytes:
		return MD5_ALIYA + str(message_len).zfill(5).encode()
	
	def _encode_message(self, message: str) -> bytes:
		return base64.encodebytes(self._k.encrypt(message.encode()))
	
	def _decode_message(self, message: bytes) -> str:
		return self._k.decrypt(base64.decodebytes(message))


async def main():
	lukseun = LukseunClient()
	# await lukseun.send_message("{'session': '', 'function': 'get_staff_current_status', 'random': '744', 'data': {'unique_id': '', 'account': '', 'password': ''}}")


if __name__ == "__main__":
	asyncio.run(main())
