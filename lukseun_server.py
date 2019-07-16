# lukseun_server.py
#
# A simple proof of concept server for internal use only.
# Uses asnycio to handle simultaneous connections efficiently.
#
# The server implements the following protocol:
# 1) read the header from the client
# 2) if the header can be verified, read the remaining message
#    otherwise discard the message and close the connection
# 3) do the requested work and send a verification back to the client.
#    A new header has to be generated via the header_tool.
# 4) close the connection

import aiohttp
import asyncio
import concurrent.futures
from Utility.LogRecorder import LogUtility as Log
from Application.GameAliya import _00_Message_Handler as handler

# the size of the header in bytes that we expect to receive from the client.
HEADER_BUFFER_SIZE = 36

# some color codes to make log easier to read
COLORS = {'pass': '\033[92m', 'fail': '\033[91m', 'end': '\033[0m',
          'ylw': '\033[1;33;40m', 'grn': '\033[1;32;40m'}


class InvalidHeaderError(Exception):
	pass


class LukseunServer:
	def __init__(self, host: str = '', port: int = 8880, max_workers: int = None):
		self._host = host
		self._port = port
		self._clientsession = None
		self._handler = handler.MessageHandler()
		self._pool = concurrent.futures.ProcessPoolExecutor(max_workers=max_workers)
	
	async def run(self) -> None:
		'''
		run() binds the server to the host and port provided, and begins
		handling incoming connections.
		'''
		self._clientsession = aiohttp.ClientSession()
		server = await asyncio.start_server(self._handle_connection, self._host, self._port)
		Log('[lukseun_server.py][run()] Starting server on {addr}'.format(addr=server.sockets[0].getsockname()))
		async with server:
			await server.serve_forever()
		await self._clientsession.close()
	
	async def _handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
		'''
		_handle_connection() handles all incoming connections in accordance to the 
		protocol defined at the top of the file.
		'''
		
		try:
			raw_header = await reader.read(HEADER_BUFFER_SIZE)
			loop = asyncio.get_running_loop()
			size = await loop.run_in_executor(self._pool, self._handler.is_valid_header, raw_header)
			Log(COLORS['ylw'] + '[lukseun_server.py][_handle_connection] Received valid data from {}'.format(
				writer.get_extra_info('peername')) + COLORS['end'])
			message = await reader.read(size)
			
			# ResolveMsg and MakeHeader are two CPU intensive, blocking function calls that hamper the speed of the server.
			# We can use a ProcessPoolExecutor to run these functions concurrently in different processes, while yielding
			# control back to the main asyncio loop so that it can handle other requests.
			
			loop = asyncio.get_running_loop()
			decoded_message = await loop.run_in_executor(self._pool, self._handler.process_message_in, message)
			print("[LukseunServer][_handle_connection] -> decoded_message:" + str(decoded_message))
			unencoded_response = await self._handler.resolve(decoded_message, self._clientsession)
			print(f'Sending : {unencoded_response}')
			
			encoded_response = await loop.run_in_executor(self._pool, self._handler.process_message_out, unencoded_response)
			
			writer.write(encoded_response)
			await writer.drain()
			Log(COLORS['grn'] + '[lukseun_server.py][_handle_connection] Sent response to client {}'.format(
				writer.get_extra_info('peername')) + COLORS['end'])
		except handler.InvalidHeaderError:
			Log(COLORS['fail'] + '[lukseun_server.py][_handle_connection] Received illegal data from {}'.format(
				writer.get_extra_info('peername')) + COLORS['end'])
		finally:
			writer.close()


async def main() -> None:
	server = LukseunServer(max_workers=16)
	await server.run()


if __name__ == '__main__':
	asyncio.run(main())
