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
		#{'function': 'level_up_weapon', 'data':{'unique_id' : '1', 'weapon' : '1', 'amount' : 40}}
		#{'function': 'level_up_passive_weapon', 'data':{'unique_id' : '1', 'weapon' : '1', 'passive' : '2'}}
		#{'function': 'level_up_star_weapon', 'data':{'unique_id' : '1', 'weapon' : '1'}}
		#{'function': 'reset_skill_point_weapon', 'data':{'unique_id' : '1', 'weapon' : '1'}},
		#{'function': 'send_gift_friend', 'data':{'unique_id' : '1', 'gn_target' : 'バカ'}},
		#{'function' : 'send_mail', 'data' : {'gn_target' : 'placeholder', 'subj' : 'delete me liang', 'body' : 'please delete me!!!'}}
		{'function': 'delete_read_mail', 'data':{}}
				]


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
	m = {'function': 'login_unique', 'data':{'unique_id' : '1'}}
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




