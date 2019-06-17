# testing.py
#
# Contains test cases for the lukseun client and server.
# TODO More test cases will be added.

import time
import asyncio
import multiprocessing
import statistics
import random
from lukseun_client import LukseunClient

COLORS = {'pass' : '\033[92m', 'fail' : '\033[91m', 'end' : '\033[0m', \
		'ylw' : '\033[1;33;40m'}
client_type="aliya"
host="192.168.1.183"
MESSAGE_LIST = [ {'session':'', 'function':'login', 'random':'-906', 'data':{'unique_id':'mac', 'account':'abc', 'password':'123'}},
				 {'session':'', 'function':'login', 'random':'-906', 'data':{'unique_id':'mac', 'account':'', 'password':''}},
				 {'session':'mac_session', 'function':'skill_level_up', 'random':'-906', 'data':{'skill_id':'m1_level', 'scroll_id':'scroll_skill_30'}},
				 {'session':'mac_session', 'function':'get_skill', 'random':'-906', 'data':{'skill_id':'m1_level'}},
				 {'session':'mac_session', 'function':'increase_supplies', 'random':'-906', 'data':{'scroll_skill_10':'10','scroll_skill_30':'1'}},
				 {'session':'mac_session', 'function':'get_all_skill_level', 'random':'-906', 'data':""},
				 {'session':'mac_session', 'function':'get_all_supplies', 'random':'-906', 'data':""},
				 {"session":"4E71A852-60CA-51EF-B8CC-C80CD627A180_session", "function":"increase_supplies", "random":"603", "data":{"scroll_skill_10":"5", "scroll_skill_30":"5", "scroll_skill_100":"5", "iron":"5", "diamonds":"5", "coin":"5", "weapon1_segment":"5", "weapon2_segment":"5", "weapon3_segment":"5", "weapon4_segment":"5", "weapon5_segment":"5", "weapon6_segment":"5"}},
				 {'session':'mac_session', 'function':'random_gift_skill', 'random':'-906', 'data':""},
				 {"session":"4E71A852-60CA-51EF-B8CC-C80CD627A180_session", "function":"get_skill", "random":"973", "data":{"skill_id":"m11"}},
				 {'session':'mac_session', 'function':'level_up_scroll', 'random':'-906', 'data':{"scroll_skill_30":"3"}},
				 {'session':'mac_session', 'function':'level_up_weapon', 'random':'-906', 'data':{"weapon1":"30"}},
				]
LOGIN_AS_ACCOUNT = 0
LOGIN_AS_VISITOR = 1
SKILL_LEVEL_UP = 2
GET_SKILL = 3
INCREASE_SCROLL_SKILL_10=4
GET_ALL_SKILL_LEVEL=5
GET_ALL_SUPPLIES=6
ALL_SUPPLIES_ADD5= 7
RANDOM_GIFT_SKILL=8
GET_SKILL = 9
SCROLL_LEVEL_UP = 10
LEVEL_UP_WEAPON =11
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
	tasks = [asyncio.ensure_future(async_send_single_message(SCROLL_LEVEL_UP)) for i in range(10)]
	loop = asyncio.get_event_loop()
	return loop.run_until_complete(asyncio.gather(*tasks))

def get_skill_from_random():#技能不同概率抽取
	all = 0
	total=0
	quantity=39 #技能个数（修改需要修改每不同等级技能的概率）
	test_time = 1000
	for i in range(0,test_time):
		num = [0 for i in range(quantity)]
		total=0
		while(sum(num)!=quantity):
			chance = random.randint(0,9)
			skill_count=0
			if chance>=0 and chance<=5:
				skill_count = random.randint(0,2)
				num[skill_count] = 1
			if chance>=6 and chance<=8:
				skill_count = random.randint(3,11)
				num[skill_count] = 1
			if chance==9:
				skill_count = random.randint(12,38)
				num[skill_count] = 1
			total=total+1
		all = all+total
		continue
	print("1:skill quantity="+str(quantity)+"  avg test="+str(all/test_time)+"  test time = "+str(test_time))

def get_skill_from_stack():#按顺序抽取技能
	all = 0
	total=0
	quantity=39#技能修改
	test_time = 1000
	for i in range(0,test_time):
		num = [0 for i in range(quantity)]
		total=0
		while(sum(num)!=quantity):
			count = random.randint(0,quantity-1)
			num[count] = 1
			total=total+1
		all = all+total
		continue
	print("2:skill quantity="+str(quantity)+"  avg test="+str(all/test_time)+"  test time = "+str(test_time))
def level_up_skill_by_scroll():
	max_level=10 #技能最大等级
	test_time=1000
	for scroll_level in range(0,10):
		total=0
		for i in range(0,test_time):
			skill_level=0
			num = [0 for i in range(max_level)]
			all=0
			while(sum(num)!=max_level):
				levelup = random.randint(0,9)
				if levelup>=0 and levelup<=scroll_level:
					num[skill_level] = 1
					skill_level=skill_level+1
				# else:
				# 	#升级失败爆
				# 	num = [0 for i in range(max_level)]
				# 	skill_level=0
					#升级失败降级
					# num[skill_level] = 0
					# if skill_level>0:
					# 	skill_level=skill_level-1
				total=total+1
			all = all+total
			continue
		print("3:scroll_level="+str(scroll_level+1)+"0%" +"  avg test="+str(all/test_time)+"  test time = "+str(test_time)+" max_level="+str(max_level))
def main() -> None:
	# get_skill_from_random()
	# get_skill_from_stack()
	# level_up_skill_by_scroll()
	# new_test_multiple_message(int(input('How many messages to send (it will be n * 10 so be careful): ')))
	# send_single_message(LOGIN_AS_VISITOR)
	# send_single_message(GET_SKILL)
	# send_single_message(SKILL_LEVEL_UP)
	# send_single_message(INCREASE_SCROLL_SKILL_10)
	# send_single_message(ALL_SUPPLIES_ADD5)
	# send_single_message(RANDOM_GIFT_SKILL)
	#send_single_message(SCROLL_LEVEL_UP)
	send_single_message(LEVEL_UP_WEAPON)

if __name__ == '__main__':
	main()




