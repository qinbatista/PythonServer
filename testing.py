# testing.py
#
# Contains test cases for the lukseun client and server.
# TODO More test cases will be added.

import time
import asyncio
from lukseun_client import LukseunClient

COLORS = {'pass' : '\033[92m', 'fail' : '\033[91m', 'end' : '\033[0m'}

async def test_single_message():
	client = LukseunClient()
	d = {'session': 'ACDE48001122', 'function': 'CheckTime', 'random': '744', 'data': {'user_name': 'yupeng', 'gender': 'male', 'email': 'qin@lukseun.com', 'phone_number': '15310568888'}}
	try:
		response = await asyncio.wait_for(client.send_message(str(d)), timeout = 5)
		print(COLORS['pass'] + 'Success! Sent message within timeout' + COLORS['end'])
	except asyncio.TimeoutError:
		print(COLORS['fail'] + 'Fail! Did not send message within timeout' + COLORS['end'])


async def test_multiple_message(n: int):
	start = time.time()

	tasks = [asyncio.ensure_future(test_single_message()) for _ in range(n)]
	for t in asyncio.as_completed(tasks):
		await t
	end = time.time()
	print(f'It took {end - start} seconds to complete {n} messages.')



def main() -> None:
	asyncio.run(test_multiple_message(int(input('How many messages to send: '))))


if __name__ == '__main__':
	main()




