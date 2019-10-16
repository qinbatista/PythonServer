'''
black_market.py
'''

from module import enums
from module import common

#


async def automatically_refresh(uid, **kwargs) -> dict:
	"""
	success -> 0 and 1
	# 0 - First refresh market success
	# 1 - Refresh market success
	# 2 - Refresh time is not over yet, market information has been obtained
	# 98 - Unexpected element, please update the configuration table
	# 99 - database operation error
	"""
	dark_market_data = kwargs['dark_market']  # self._player['dark_market']
	merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity = await self._get_dark_market_material(world, unique_id, code = 1)

	remaining = {}
	if refresh_time == '':
		refreshable_quantity = 3
		refresh_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		tier_choice = random.choices(dark_market_data['names'], dark_market_data['weights'], k = 8)
		key_list = [(random.choices(dark_market_data[tier], k = 1))[0] for tier in tier_choice]
		for i in range(len(key_list)):
			merchandise = key_list[i]
			code = i + 1
			if merchandise in dark_market_data['weapon']:
				currency_type = (random.choices(list(dark_market_data['segment'].keys()), k = 1))[0]
				merchandise_quantity = random.randint(int(dark_market_data['segment'][currency_type]['quantity_min']), int(dark_market_data['segment'][currency_type]['quantity_max']))
				currency_type_price = random.randint(int(dark_market_data['segment'][currency_type]['cost_range_min']), int(dark_market_data['segment'][currency_type]['cost_range_max']))
				if await self._set_dark_market_material(world, unique_id, code, merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity) == 0:
					return self._message_typesetting(99, 'database operation error')
			elif merchandise in dark_market_data['skill']:
				currency_type = (random.choices(list(dark_market_data['reward_skill'].keys()), k=1))[0]
				merchandise_quantity = 1
				currency_type_price = random.randint(int(dark_market_data['reward_skill'][currency_type]['cost_range_min']), int(dark_market_data['reward_skill'][currency_type]['cost_range_max']))
				if await self._set_dark_market_material(world, unique_id, code, merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity) == 0:
					return self._message_typesetting(99, 'database operation error')
			elif merchandise in dark_market_data['other'].keys():
				currency_type = (random.choices(list(dark_market_data['other'][merchandise].keys()), k=1))[0]
				merchandise_quantity = random.randint(int(dark_market_data['other'][merchandise][currency_type]['quantity_min']), int(dark_market_data['other'][merchandise][currency_type]['quantity_max']))
				if await self._set_dark_market_material(world, unique_id, code, merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity) == 0:
					return self._message_typesetting(99, 'database operating error')
			else:
				return self._message_typesetting(98, 'Unexpected element, please update the configuration table.')
			remaining.update({'merchandise%s' % code : merchandise, 'merchandise%s_quantity' % code : merchandise_quantity, 'currency_type%s' % code : currency_type, 'currency_type%s_price' % code : currency_type_price})
		remaining.update({'refresh_time' : refresh_time, 'refreshable_quantity' : int(refreshable_quantity)})
		return self._message_typesetting(0, 'First refresh market success', {'remaining' : remaining})
	else:
		current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(refresh_time, '%Y-%m-%d %H:%M:%S')
		if delta_time.total_seconds() // 3600 >= 3:
			frequency = delta_time.total_seconds() // 3600 // 3
			refreshable_quantity += frequency
			if refreshable_quantity > 3:
				refreshable_quantity = 3
			refresh_time = (datetime.strptime(refresh_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours = frequency*3)).strftime('%Y-%m-%d %H:%M:%S')

			tier_choice = random.choices(dark_market_data['names'], dark_market_data['weights'], k = 8)
			key_list = [(random.choices(dark_market_data[tier], k = 1))[0] for tier in tier_choice]
			for i in range(len(key_list)):
				merchandise = key_list[i]
				code = i + 1
				if merchandise in dark_market_data['weapon']:
					currency_type = (random.choices(list(dark_market_data['segment'].keys()), k = 1))[0]
					merchandise_quantity = random.randint(int(dark_market_data['segment'][currency_type]['quantity_min']), int(dark_market_data['segment'][currency_type]['quantity_max']))
					currency_type_price = random.randint(int(dark_market_data['segment'][currency_type]['cost_range_min']), int(dark_market_data['segment'][currency_type]['cost_range_max']))
					if await self._set_dark_market_material(world, unique_id, code, merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity) == 0:
						return self._message_typesetting(99, 'database operation error')
				elif merchandise in dark_market_data['skill']:
					currency_type = (random.choices(list(dark_market_data['reward_skill'].keys()), k=1))[0]
					merchandise_quantity = 1
					currency_type_price = random.randint(int(dark_market_data['reward_skill'][currency_type]['cost_range_min']), int(dark_market_data['reward_skill'][currency_type]['cost_range_max']))
					if await self._set_dark_market_material(world, unique_id, code, merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity) == 0:
						return self._message_typesetting(99, 'database operation error')
				elif merchandise in dark_market_data['other'].keys():
					currency_type = (random.choices(list(dark_market_data['other'][merchandise].keys()), k=1))[0]
					merchandise_quantity = random.randint(int(dark_market_data['other'][merchandise][currency_type]['quantity_min']), int(dark_market_data['other'][merchandise][currency_type]['quantity_max']))
					currency_type_price = random.randint(int(dark_market_data['other'][merchandise][currency_type]['cost_range_min']), int(dark_market_data['other'][merchandise][currency_type]['cost_range_max']))
					if await self._set_dark_market_material(world, unique_id, code, merchandise, merchandise_quantity, currency_type, currency_type_price, refresh_time, refreshable_quantity) == 0:
						return self._message_typesetting(99, 'database operating error')
				else:
					return self._message_typesetting(98, 'Unexpected element, please update the configuration table.')
				remaining.update({'merchandise%s' % code : merchandise, 'merchandise%s_quantity' % code : merchandise_quantity, 'currency_type%s' % code : currency_type, 'currency_type%s_price' % code : currency_type_price})
			remaining.update({'refresh_time' : refresh_time, 'refreshable_quantity' : int(refreshable_quantity)})
			return self._message_typesetting(1, 'refresh market success', {'remaining' : remaining})
		else:
			headers = [x[0] for x in list(await self._execute_statement(world, 'desc dark_market;'))]
			content = (await self._execute_statement(world, f'SELECT * FROM dark_market WHERE unique_id = "{unique_id}";'))[0]
			for i in range(len(headers)):
				remaining.update({headers[i] : content[i]})
			remaining.pop('unique_id')
			return self._message_typesetting(2, 'Refresh time is not over yet, market information has been obtained', {'remaining' : remaining})

