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


def test_multiple_message(n: int):
	start = time.time()
	with multiprocessing.Pool() as pool:
		for _ in pool.imap_unordered(send_single_message, range(n)):
			pass
	print(f'It took {time.time() - start} seconds to complete {n} messages.')


def send_single_message(message_id: int):
	client = LukseunClient()
	# d = {'session': '', 'function': 'get_session', 'random': '744', 'data': {'unique_id': 'ACDE480011228888', 'account': '', 'password': ''}}
	#d = {'session': 'ACDE480011228888_session', 'function': 'check_time', 'random': '744', 'data': ""}
	#d = {'session': 'ACDE480011228888_session', 'function': 'get_staff_current_status', 'random': '744', 'data': ""}

	# d = {'session': '', 'function': 'login', 'random': '744', 'data': {'unique_id': 'ACDE480011228888', 'account': 'a', 'password': 'a'}}#aliya login
	d = {'session': '', 'function': 'create_account', 'random': '744', 'data': {'unique_id': 'ACDE480011228888', 'account': 'a', 'password': 'a',"ip":"","user_name":"","gender":"","birth_day":"","last_time_login":"","registration_time":""}}#aliya create account
	start = time.time()
	asyncio.run(client.send_message(str(d)))
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
	client = LukseunClient()
	d = {'session': 'ACDE48001122', 'function': 'login', 'random': '744', 'data': {'user_name': 'yupeng', 'gender': 'male', 'email': 'qin@lukseun.com', 'phone_number': '15310568888'}}
	start = time.time()
	await client.send_message(str(d))
	end = time.time()
	print(f"Message #{message_id} took {COLORS['pass']} {end - start} {COLORS['end']} seconds to complete.")
	return end - start

def async_multi_message(message_id: int):
	tasks = [asyncio.ensure_future(async_send_single_message(message_id * i)) for i in range(10)]
	loop = asyncio.get_event_loop()
	return loop.run_until_complete(asyncio.gather(*tasks))


def main() -> None:
	#test_multiple_message(int(input('How many messages to send: ')))
	#new_test_multiple_message(int(input('How many messages to send (it will be n * 10 so be careful): ')))
	send_single_message(1)


if __name__ == '__main__':
	main()




