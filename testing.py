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
MESSAGE_LIST = [ {'function':'login', 'random':'-906', 'data':{'unique_id':'mac', 'identifier' : 'account', 'value' : 'childrensucks', 'password' : 'keepo'}},
				 {'function':'login_unique', 'random':'-906', 'data':{'unique_id':'4', 'identifier':'', 'value' : '','password':''}},
				 {'function':'skill_level_up', 'random':'-906', 'data':{'skill_id':'m1_level', 'scroll_id':'scroll_skill_30'}},
				 {'function':'get_skill', 'random':'-906', 'data':{'skill_id':'m1_level'}},
				# 4 --- 7
				 {'function':'increase_supplies', 'random':'-906', 'data':{'scroll_skill_10':'10','scroll_skill_30':'1'}},
				 {'function':'get_all_supplies', 'random':'-906', 'data':{}},
				 {'function':'random_gift_skill', 'random':'-906', 'data':{}},
				 {'function':'level_up_scroll', 'random':'-906', 'data':{"scroll_id": "skill_scroll_10"}},
				# 8 --- 11
				 {'function':'level_up_weapon','random':'-906', 'data':{"weapon":"weapon1", "iron": "20"}},#data: [weapon1] means which weapon you want to level up, [1020] means how much iron you want to cast, we set 20 iron to level up in server, if you send 1020 iron, server will level up weapon to 51.(max weapon level is 100)
				 {'function':'level_up_skill','random':'-906', 'data':{"skill_id":"m1_level", "scroll_id": "skill_scroll_10"}},
				 {'function':'level_up_passive','random':'-906', 'data':{"weapon":"weapon1", "passive": "passive_skill_4_level"}},
				 {'function':'reset_weapon_skill_point','random':'-906', 'data':{"weapon": "weapon1"}},#data: [weapon1] means which weapon you want to reset skill, [100] means cost resources, right now it is coin in our code,it will be change in furture, make sure it is easy change.
				# 12 --- 15
				 {'function':'level_up_weapon_star','random':'-906', 'data':{"weapon": "weapon1"}},# data: [weapon1] means which weapon you want to increase star, [30] means how much weapon segment weapon need to level up, it's just reference, server will handle really message, righ now level up weapon start cost 30 segment, every level increase 30 segment(1:30,2:60,3:90), make sure the cost segment value can be change easily(star also means number of this weapon).
				 {'function':'get_all_weapon','random':'-906', 'data':{}},
				 {'function':'random_gift_segment','random':'-906', 'data':{"weapon_kind": "100"}},
				 {'function':'pass_stage','random':'-906', 'data':{"stage":1}},
				# 16 --- 17
				 {'function':'decrease_energy','random':'-906', 'data':{"energy": "1"}},
				 {'function':'increase_energy','random':'-906', 'data':{"energy": "1"}}
				]
LOGIN_AS_ACCOUNT = 0
LOGIN_AS_VISITOR = 1
SKILL_LEVEL_UP = 2
GET_SKILL = 3

INCREASE_SUPPLIES = 4
GET_ALL_SKILL_LEVEL = 5
RANDOM_GIFT_SKILL = 6
LEVEL_UP_SCROLL = 7

LEVEL_UP_WEAPON = 8
LEVEL_UP_SKILL = 9
LEVEL_UP_PASSIVE = 10
RESET_WEAPON_SKILL_POINT = 11

LEVEL_UP_WEAPON_STAR = 12
GET_ALL_WEAPON = 13
RANDOM_GIFT_SEGMENT = 14
PASS_STAGE = 15

DECREASE_ENERGY = 16
INCREASE_ENERGY = 17



GET_ALL_SUPPLIES=5
def test_multiple_message(n: int):
	start = time.time()
	with multiprocessing.Pool() as pool:
		for _ in pool.imap_unordered(send_single_message, range(n)):
			pass
	print(f'It took {time.time() - start} seconds to complete {n} messages.')


def send_single_message(message_id: int):
	client = LukseunClient(client_type, host, port=8880)
	start = time.time()
	MESSAGE_LIST[message_id]["data"]['token']=token
	newstring  =  str(MESSAGE_LIST[message_id]).replace("'","\"")
	asyncio.run(client.send_message(newstring))
	print(f"Message #{message_id} took {COLORS['pass']} {time.time() - start} {COLORS['end']} seconds to complete.")
	return client.token

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
	#d = {'token': 'ACDE48001122', 'function': 'login', 'random': '744', 'data': {'user_name': 'yupeng', 'gender': 'male', 'email': 'qin@lukseun.com', 'phone_number': '15310568888'}}
	start = time.time()
	await client.send_message(str(MESSAGE_LIST[message_id]).replace("'","\""))
	end = time.time()
	print(f"Message #{message_id} took {COLORS['pass']} {end - start} {COLORS['end']} seconds to complete.")
	return end - start

def async_multi_message(message_id: int):
	tasks = [asyncio.ensure_future(async_send_single_message(LEVEL_UP_SCROLL)) for i in range(10)]
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



def TEST_EQUAL(test_message: str, lhs, rhs):
	print(test_message, end='.....')
	if lhs == rhs:
		print(COLORS['pass'] + 'OK' + COLORS['end'])
	else:
		print(COLORS['fail'] + f'FAIL  expected {rhs} got {lhs}' + COLORS['end'] )


def test_token_server():
	# ENSURE TOKEN SERVER IS RUNNING
	# ENSURE USER DATABASE IS RUNNING
	LOGIN_URL = 'http://localhost:8080/login'
	LOGIN_UNIQUE_URL = 'http://localhost:8080/login_unique'
	VALIDATE_URL = 'http://localhost:8080/validate'

	print('TESTING TOKEN SERVER')


	r = requests.post(LOGIN_UNIQUE_URL, data = {'unique_id' : '4'})
	TEST_EQUAL('Testing login with non-bound unique_id', r.status_code, 200)
	time.sleep(1)

	r = requests.post(LOGIN_UNIQUE_URL, data = {'unique_id' : '2'})
	TEST_EQUAL('Testing login with bound unique_id', r.status_code, 400)
	time.sleep(1)

	r = requests.post(LOGIN_URL, data = {'identifier' : 'account', 'value' : 'childrensucks', 'password' : 'keepo'})
	TEST_EQUAL('Testing login with account name and password', r.status_code, 200)
	time.sleep(1)

	r = requests.post(LOGIN_URL, data = {'identifier' : 'account', 'value' : 'childrensucks', 'password' : 'keep232o'})
	TEST_EQUAL('Testing login with account name and wrong password', r.status_code, 400)
	time.sleep(1)

	r = requests.post(LOGIN_URL, data = {'identifier' : 'account', 'value' : 'childre232nsucks', 'password' : 'keepo'})
	TEST_EQUAL('Testing login with wrong account name and password', r.status_code, 400)
	time.sleep(1)

	r = requests.post(LOGIN_UNIQUE_URL, data = {'unique_id' : '4'})
	r = requests.get(VALIDATE_URL, headers = {'Authorization' : r.json()['token']})
	TEST_EQUAL('Can validate with valid token', r.status_code, 200)
	time.sleep(1)

	r = requests.post(LOGIN_UNIQUE_URL, data = {'unique_id' : '4'})
	old_token = r.json()['token']
	r = requests.post(LOGIN_UNIQUE_URL, data = {'unique_id' : '4'})
	r = requests.get(VALIDATE_URL, headers = {'Authorization' : old_token})
	TEST_EQUAL('Can not validate with old token', r.status_code, 400)


def main() -> None:
	global token
	# get_skill_from_random()
	# get_skill_from_stack()
	# level_up_skill_by_scroll()
	# new_test_multiple_message(int(input('How many messages to send (it will be n * 10 so be careful): ')))

	# send_single_message(LOGIN_AS_ACCOUNT)
	token = send_single_message(LOGIN_AS_VISITOR)
	print(f'this is token = {token}')
	# send_single_message(SKILL_LEVEL_UP)
	# send_single_message(GET_SKILL)
	# send_single_message(INCREASE_SUPPLIES)
	# send_single_message(GET_ALL_SKILL_LEVEL)
	# send_single_message(RANDOM_GIFT_SKILL)
	# send_single_message(LEVEL_UP_SCROLL)
	# send_single_message(LEVEL_UP_WEAPON)
	send_single_message(LEVEL_UP_SKILL)
	# send_single_message(LEVEL_UP_PASSIVE)
	# send_single_message(RESET_WEAPON_SKILL_POINT)
	# send_single_message(LEVEL_UP_WEAPON_STAR)
	# send_single_message(GET_ALL_WEAPON)
	# send_single_message(RANDOM_GIFT_SEGMENT)
	# send_single_message(PASS_STAGE)
	# send_single_message(DECREASE_ENERGY)

	# test_token_server()


if __name__ == '__main__':
	main()




