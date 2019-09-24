# testing.py
#
# Contains test cases for the lukseun client and server.
# TODO More test cases will be added.

import time
import asyncio
import multiprocessing
import statistics
import random
import requests
from lukseun_client import LukseunClient

COLORS = {'pass' : '\033[92m', 'fail' : '\033[91m', 'end' : '\033[0m',
		'ylw' : '\033[1;33;40m'}
client_type="aliya"
# host="192.168.1.183"
host="127.0.0.1"
token =""
MESSAGE_LIST = [
		{'function': 'send_mail', 'data':{'unique_id' : '1', 'gn_target' : 'cuck'}}
				]


def send_single_message(message_id: int):
	client = LukseunClient(client_type)
	start = time.time()
	newstring  =  str(MESSAGE_LIST[message_id]).replace("'","\"")
	print('sending message...')
	asyncio.run(client.send_message(newstring))
	print(f"Message #{message_id} took {COLORS['pass']} {time.time() - start} {COLORS['end']} seconds to complete.")
	return client.token


def main() -> None:
	send_single_message(0)


if __name__ == '__main__':
	main()




