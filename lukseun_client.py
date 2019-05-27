# lukseun_client.py
#
# A simple proof of concept client for internal use only.
# Uses asyncio to handle the sending and receipt of messages to the server.
#

import asyncio
from Utility import AnalysisHeader, EncryptionAlgorithm
from Utility.LogRecorder import LogUtility as Log


# the size of the header in bytes that we will send to and receive from the server.
HEADER_BUFFER_SIZE = 36

class LukseunClient:
	def __init__(self, client_type: str = 'aliya', host: str = '127.0.0.1', port: int = 8888):
		self._client_type = client_type
		self._host = host
		self._port = port
		self._header_tool = AnalysisHeader.Header()
		self._des = EncryptionAlgorithm.DES()


	async def send_message(self, message: str) -> bytes:
		'''
		send_message() sends the given message to the server and
		returns the decoded callback response
		'''
		reader, writer = await asyncio.open_connection(self._host, self._port)
		encrypted_message = self._des.encrypt(message)
		await self._send_header(writer, len(encrypted_message))
		await self._send_message(writer, encrypted_message)
		response = await self._receive_response(reader)
		writer.close()
		return response

	async def _send_header(self, writer: asyncio.StreamWriter, message_len: int) -> None:
		'''
		_send_header() sends the header to the server which contains the size of the
		message that we will send next.
		'''
		header = self._header_tool.MakeHeader(self._client_type, str(message_len))
		writer.write(header)
		await writer.drain()
		Log('[lukseun_client.py][_send_header()] Sent header {} to {}'.format(bytes.decode(header), writer.get_extra_info('peername')))


	async def _send_message(self, writer: asyncio.StreamWriter, message: bytes) -> None:
		'''
		_send_message() sends the encrypted message to the server. called after
		the header has already been sent to the server.
		'''
		writer.write(message)
		await writer.drain()
		Log('[lukseun_client.py][_send_message()] Sent message {} to {}'.format(bytes.decode(message), writer.get_extra_info('peername')))


	async def _receive_response(self, reader: asyncio.StreamReader) -> bytes:
		'''
		_receive_response() receives the callback response from the server.
		'''
		header_raw = await reader.read(HEADER_BUFFER_SIZE)
		header = AnalysisHeader.Header(header_raw)
		response = await reader.read(int(header.size))
		Log('[lukseun_client.py][_receive_response()] Received response {} from server'.format(bytes.decode(response)))
		return response


