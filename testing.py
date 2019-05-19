# testing.py
#
# Contains test cases for the lukseun client and server.
# TODO More test cases will be added.

import time
import asyncio
import multiprocessing
from lukseun_client import LukseunClient

COLORS = {'pass' : '\033[92m', 'fail' : '\033[91m', 'end' : '\033[0m'}


def test_multiple_message(n: int):
	start = time.time()
	with multiprocessing.Pool() as pool:
		for _ in pool.imap_unordered(send_single_message, range(n)):
			pass
	print(f'It took {time.time() - start} seconds to complete {n} messages.')


def send_single_message(message_id: int):
	client = LukseunClient()
	d = {'session': 'ACDE48001122', 'function': 'CheckTime', 'random': '744', 'data': {'user_name': 'yupeng', 'gender': 'male', 'email': 'qin@lukseun.com', 'phone_number': '15310568888'}}
	start = time.time()
	asyncio.run(client.send_message(str(d)))
	print(f"Message #{message_id} took {COLORS['pass']} {time.time() - start} {COLORS['end']} seconds to complete.")

##########################################################################################3
def new_test_multiple_message(n: int):
	start = time.time()
	with multiprocessing.Pool() as pool:
		for _ in pool.imap_unordered(async_multi_message, range(n)):
			pass
	print(f'It took {time.time() - start} seconds to complete {n * 10} messages.')

async def async_send_single_message(message_id: int):
	client = LukseunClient()
	d = {'session': 'ACDE48001122', 'function': 'CheckTime', 'random': '744', 'data': {'user_name': 'yupeng', 'gender': 'male', 'email': 'qin@lukseun.com', 'phone_number': '15310568888'}}
	start = time.time()
	await client.send_message(str(d))
	print(f"Message #{message_id} took {COLORS['pass']} {time.time() - start} {COLORS['end']} seconds to complete.")

def async_multi_message(message_id: int):
	client = LukseunClient()
	d = {'session': 'ACDE48001122', 'function': 'CheckTime', 'random': '744', 'data': {'user_name': 'yupeng', 'gender': 'male', 'email': 'qin@lukseun.com', 'phone_number': '15310568888'}}
	#start = time.time()
	tasks = [asyncio.ensure_future(async_send_single_message(message_id * i)) for i in range(10)]
	loop = asyncio.get_event_loop()
	loop.run_until_complete(asyncio.gather(*tasks))
	#print(f"Message #{message_id} took {COLORS['pass']} {time.time() - start} {COLORS['end']} seconds to complete.")


def main() -> None:
	#test_multiple_message(int(input('How many messages to send: ')))
	new_test_multiple_message(int(input('How many messages to send (it will be n * 10 so be careful): ')))


if __name__ == '__main__':
	main()




