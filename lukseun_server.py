# lukseun_server.py
#
# A simple proof of concept server for internal use only.
# Uses asnycio to handle simultaneous connections efficiently.
#
# The server implements the following protocol:
# 1) read the header from the client
# 2) if the header can be verified, read the remaining message
#	 otherwise discard the message and close the connection
# 3) do the requested work and send a verification back to the client.
#    A new header has to be generated via the header_tool.
# 4) close the connection

import asyncio
from WorkingCat import WorkingTimeRecoder
from Utility import AnalysisHeader
from Utility.LogRecorder import LogUtility as Log


# the size of the header in bytes that we expect to receive from the client.
HEADER_BUFFER_SIZE = 36


class LukseunServer:
	def __init__(self, host: str = '127.0.0.1', port: int = 8888):
		self._host = host
		self._port = port
		self._header_tool = AnalysisHeader.Header()
		self._wtr = WorkingTimeRecoder.WorkingTimeRecoderClass()


	async def run(self) -> None:
		'''
		run() binds the server to the host and port provided, and begins
		handling incomming connections.
		'''
		server = await asyncio.start_server(self._handle_connection, self._host, self._port)
		Log('[lukseun_server.py][run()] Starting server on {addr}'.format(addr = server.sockets[0].getsockname()))
		async with server:
			await server.serve_forever()


	async def _handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
		'''
		_handle_connection() handles all incoming connections in accordance to the 
		protocol defined at the top of the file.
		'''
		header = await self._receive_header(reader)
		if (self._is_valid_header(header)):
			Log('[lukseun_server.py][_handle_connection] Received valid data from {}'.format(writer.get_extra_info('peername')))
			message = await reader.read(int(header.size))
			status = self._wtr.ResolveMsg(message, writer.get_extra_info('peername')[0])
			response_header = self._header_tool.MakeHeader(header.App, str(len(status)))
			writer.write(response_header + status)
			await writer.drain()
			Log('[lukseun_server.py][_handle_connection] Sent response to client {}'.format(writer.get_extra_info('peername')))
		else:
			Log('[lukseun_server.py][_handle_connection] Received illegal data from {}'.format(writer.get_extra_info('peername')))
		writer.close()

	async def _receive_header(self, reader: asyncio.StreamReader) -> AnalysisHeader.Header:
		'''
		_receive_header() reads the first HEADER_BUFFER_SIZE bytes from the client which
		contains the header. Returns an AnalysisHeader.Header object.
		'''
		header_raw = await reader.read(HEADER_BUFFER_SIZE)
		return AnalysisHeader.Header(header_raw)


	def _is_valid_header(self, header: AnalysisHeader.Header) -> bool:
		'''
		_is_valid_header() returns True if the header is valid, False otherwise.
		'''
		return header.App != ''



async def main() -> None:
	server = LukseunServer()
	await server.run()

if __name__ == '__main__':
	asyncio.run(main())
