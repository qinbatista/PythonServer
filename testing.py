# testing.py
#
# Contains test cases for the lukseun client and server.
# TODO More test cases will be added.

import time
import asyncio
import multiprocessing
import statistics
from lukseun_client import LukseunClient

COLORS = {'pass' : '\033[92m', 'fail' : '\033[91m', 'end' : '\033[0m', \
		'ylw' : '\033[1;33;40m'}
client_type="aliya"
host="192.168.1.183"
MESSAGE_LIST = [ {'session':'', 'function':'login', 'random':'-906', 'data':{'unique_id':'mac', 'account':'abc', 'password':'123'}},
				 {'session':'', 'function':'login', 'random':'-906', 'data':{'unique_id':'mac', 'account':'', 'password':''}},
				 {'session':'mac_session', 'function':'skill_level_up', 'random':'-906', 'data':{'skill_id':'m1_level', 'scroll_id':'scroll_skill_10'}},
				 {'session':'mac_session', 'function':'get_skill', 'random':'-906', 'data':{'skill_id':'m1_level'}},
				 {'session':'mac_session', 'function':'increase_supplies', 'random':'-906', 'data':{'scroll_skill_10':'1','scroll_skill_30':'1'}}
				]
LOGIN_AS_ACCOUNT = 0
LOGIN_AS_VISITOR = 1
SKILL_LEVEL_UP = 2
GET_SKILL = 3
INCREASE_SCROLL_SKILL_10=4
def test_multiple_message(n: int):
	start = time.time()
	with multiprocessing.Pool() as pool:
		for _ in pool.imap_unordered(send_single_message, range(n)):
			pass
	print(f'It took {time.time() - start} seconds to complete {n} messages.')


def send_single_message(message_id: int):
	client = LukseunClient(client_type,host)
	start = time.time()
	newstring  =  str(MESSAGE_LIST[message_id]).replace("'","\"")
	asyncio.run(client.send_message(newstring))
	print(f"Message #{message_id} took {COLORS['pass']} {time.time() - start} {COLORS['end']} seconds to complete.")

##########################################################################################3
def new_test_multiple_message(n: int):
	start = time.time()
	with multiprocessing.Pool() as pool:
		times = []
		for r in pool.imap_unordered(async_multi_message, range(n)):
			times.extend(r)

	print('\n\n####################################')
	print(f'It took {time.time() - start} seconds to complete {len(times)} messages.')
	print(f"Fastest: {COLORS['pass']} {min(times)} {COLORS['end']} seconds.")
	print(f"Average: {COLORS['ylw']} {statistics.mean(times)} {COLORS['end']} seconds.")
	print(f"Slowest: {COLORS['fail']} {max(times)} {COLORS['end']} seconds.")

async def async_send_single_message(message_id: int) -> float:
	client = LukseunClient(client_type,host)
	#d = {'session': 'ACDE48001122', 'function': 'login', 'random': '744', 'data': {'user_name': 'yupeng', 'gender': 'male', 'email': 'qin@lukseun.com', 'phone_number': '15310568888'}}
	start = time.time()
	await client.send_message(str(MESSAGE_LIST[message_id]).replace("'","\""))
	end = time.time()
	print(f"Message #{message_id} took {COLORS['pass']} {end - start} {COLORS['end']} seconds to complete.")
	return end - start

def async_multi_message(message_id: int):
	tasks = [asyncio.ensure_future(async_send_single_message(message_id * i)) for i in range(10)]
	loop = asyncio.get_event_loop()
	return loop.run_until_complete(asyncio.gather(*tasks))


def main() -> None:
	#new_test_multiple_message(int(input('How many messages to send (it will be n * 10 so be careful): ')))
	# send_single_message(LOGIN_AS_VISITOR)
	#send_single_message(SKILL_LEVEL_UP)
	#send_single_message(GET_SKILL)
	send_single_message(INCREASE_SCROLL_SKILL_10)


if __name__ == '__main__':
	main()




