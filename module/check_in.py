'''
task.py
'''
from datetime import datetime, timedelta
from module import enums
from module import common
import time

async def supplement_check_in(uid, **kwargs) -> dict:
	print("!supplement_check_in")
	"""补签"""
	# 0 - Successful signing
	# 98 - You have completed all current check-ins
	# 99 - Insufficient diamond
	month_pre = time.strftime('%Y-%m-', time.localtime())  # 获取每月需要补签的日期前缀
	data = await common.execute(f'select date from check_in where uid="{uid}" and date like "{month_pre}%"',**kwargs)
	day_list = [int(d[0][-2:]) for d in data]
	today = datetime.today()
	# max_day = calendar.monthrange(today.year, today.month)[1]  # 获取本月的总天数
	missing_num = today.day - len(day_list)
	if missing_num == 0:
		return common.mt(98, 'You have completed all current check-ins')
	need_diamond = -1 * missing_num * check_in['patch_diamond']
	diamond_data = await common.try_item(uid,enums.Item.DIAMOND,amount[aindex-1], **kwargs)
	if diamond_data['status'] != 0:
		return common.mt(99, 'Insufficient diamond')
	# remaining = {'diamond': diamond_data['remaining'], 'missing_date': []}
	remaining = {'missing_date': []}
	for d in range(1, today.day + 1):
		if d not in day_list:
			check_date = f'{month_pre}{d}'
			if d < 10: check_date = f'{month_pre}0{d}'
			remaining['missing_date'].append(check_date)
			await common.execute_update( f'insert into check_in(uid, date) values("{uid}", "{check_date}")',**kwargs)
	data = await receive_all_check_reward( uid)
	remaining.update({'check_in_data': data['data']})
	return common.mt(0, 'Successful signing', data={'remaining': remaining})

async def check_in(uid, **kwargs) -> dict:
	print("!check_in")
	"""每日签到"""
	# 0 - Sign-in success
	# 99 - You have already signed in today
	current_time = time.strftime('%Y-%m-%d', time.localtime())
	s_data = await common.execute( f'select * from check_in where uid="{uid}" and date="{current_time}"', **kwargs)
	if s_data != ():
		return common.mt(99, 'You have already signed in today')
	# 更新签到表
	config  = kwargs["config"]
	await common.execute_update( f'insert into check_in(uid, date) values("{uid}", "{current_time}")',**kwargs)
	data = await receive_all_check_reward( uid)
	return common.mt(0, 'Sign-in success', data=data['data'])

async def get_all_check_in_table(uid, **kwargs) -> dict:
	print("!get_all_check_in_table")
	"""获取所有签到情况"""
	# 0 - Successfully obtained all check-in status
	# 0 - Successfully obtained all check-in status this month
	# data = await common.execute( f'select * from check_in where uid="{uid}"')
	month_pre = time.strftime('%Y-%m-', time.localtime())  # 获取本月的日期前缀
	data = await common.execute( f'select * from check_in where uid="{uid}" and date like "{month_pre}%"',**kwargs)
	print(str(data))
	remaining = {}
	for i, d in enumerate(data):
		remaining.update({i: {'date': d[1], 'reward': d[2]}})
	return common.mt(0, 'Successfully obtained all check-in status this month', data={'remaining': remaining})

async def receive_all_check_reward(uid, **kwargs) -> dict:
	"""领取本月所有签到奖励"""
	# 0 - Successfully received the reward
	month_pre = time.strftime('%Y-%m-', time.localtime())  # 获取本月的日期前缀
	data = await common.execute( f'select * from check_in where uid="{uid}" and date like "{month_pre}%" and reward=0', **kwargs)
	key_words = ['role', 'weapon']
	vip_dict = await self.increase_vip_exp( uid, 0)
	if vip_dict == {}: return common.mt(99, 'function increase_vip_exp error')
	vip_level = vip_dict['vip_level']
	remaining = {}
	reward = {}
	for d in data:
		# 领奖的操作
		day = int(d[1][-2:])
		item_index = day % 7
		if item_index < vip_level:
			for key, value in self._check_in[str(item_index + 1)].items():
				if key in key_words:
					k = value['type']
					quantity = 2 * value['quantity']
					select_str = f'select segment from {key} where uid="{uid}" and {key}_name="{k}"'
					update_str = f'update {key} set segment=segment+{quantity} where uid="{uid}" and {key}_name="{k}"'
					insert_str = f'insert into {key}(uid, {key}_name, segment) values("{uid}", "{k}", {quantity})'
					k_data = await common.execute( select_str)
					if k_data == ():
						await common.execute_update( insert_str)
						remaining.update({key: {k: quantity}})
					else:
						await common.execute_update( update_str)
						remaining.update({key: {k: k_data[0][0] + quantity}})
					if key in reward.keys():
						if k in reward[key].keys():
							reward[key][k] += quantity
						else:
							reward[key].update({k: quantity})
					else:
						reward.update({key: {k: quantity}})
				else:
					quantity = 2 * value
					key_data = await self._try_material( uid, key, quantity)
					remaining.update({key: key_data['remaining']})
					if key in reward.keys():
						reward[key] += quantity
					else:
						reward.update({key: quantity})
		else:
			for key, value in self._check_in[str(item_index + 1)].items():
				if key in key_words:
					k = value['type']
					quantity = value['quantity']
					select_str = f'select segment from {key} where uid="{uid}" and {key}_name="{k}"'
					update_str = f'update {key} set segment=segment+{quantity} where uid="{uid}" and {key}_name="{k}"'
					insert_str = f'insert into {key}(uid, {key}_name, segment) values("{uid}", "{k}", {quantity})'
					k_data = await common.execute( select_str)
					if k_data == ():
						await common.execute_update( insert_str)
						remaining.update({key: {k: quantity}})
					else:
						await common.execute_update( update_str)
						remaining.update({key: {k: k_data[0][0] + quantity}})
					if key in reward.keys():
						if k in reward[key].keys():
							reward[key][k] += quantity
						else:
							reward[key].update({k: quantity})
					else:
						reward.update({key: {k: quantity}})
				else:
					quantity = value
					key_data = await self._try_material( uid, key, quantity)
					remaining.update({key: key_data['remaining']})
					if key in reward.keys():
						reward[key] += quantity
					else:
						reward.update({key: quantity})
		# 领完奖励后，将签到表中的reward置为1
		await common.execute_update( f'update check_in set reward=1 where uid="{uid}" and date="{d[1]}"')

	return common.mt(0, 'Successfully received the reward', data={'remaining': remaining, 'reward': reward})