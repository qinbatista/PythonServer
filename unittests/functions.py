'''
functions.py
'''

import sys
import json
import string
import random
import inspect
import contextlib


'''
all functions derive from this abstract base class.
before_call is always called by the simulated user before sending the request.
after_call is always called by the simulated user after receiving a response.

both the global_state and state parameters are mutable.
'''
class Function:
	def __init__(self, fn):
		self.fn = {'function' : fn, 'data' : {}}
	
	def before_call(self, global_state, state):
		pass

	def after_call(self, global_state, state, metric):
		pass

	def dump(self, token, world):
		if token:
			self.fn['data']['token'] = token
		if world:
			self.fn['world'] = world
		return str(self.fn).replace("'", '"')

	@property
	def name(self):
		return self.fn['function']

# Private
class add_resources(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

# Account
class login_unique(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['unique_id'] = state.uid
	
	def after_call(self, global_state, state, metric):
		state.token = metric.resp['data']['token']
		state.functions.put(FunctionList.get('enter_world'))

# Armor
class get_all_armor(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class upgrade_armor(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['aid'] = 1
		self.fn['data']['level'] = 2

# Darkmarket
class get_all_market(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class refresh_market(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

# Family
class get_all_family(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def after_call(self, global_state, state, metric):
		if metric.resp['status'] == 0:
			global_state.remove('families', state.world, state.fn)
			state.fn = metric.resp['data']['name']
			state.familylist = {m['gn'] for m in metric.resp['data']['members']}
			global_state.add('families', state.world, state.fn)

class create_family(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['name'] = 'family_' + ''.join(random.choice(string.digits) for _ in range(15))
		self.fn['data']['icon'] = 1
	
	def after_call(self, global_state, state, metric):
		if metric.resp['status'] == 0:
			state.fn = metric.resp['data']['name']
			global_state.add('families', state.world, state.fn)

class leave_family(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def after_call(self, global_state, state, metric):
		if metric.resp['status'] == 0:
			global_state.remove('families', state.world, state.fn)
			state.fn = ''

class respond_family(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		key = ''
		for mail in state.mail:
			if mail['type'] == 3:
				key = mail['key']
		self.fn['data']['key'] = key

	def after_call(self, global_state, state, metric):
		if metric.resp['status'] == 0 and state.fn == '':
			state.fn = metric.resp['data']['name']

class remove_user_family(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['gn_target'] = global_state.random('users', state.world)
	
class invite_user_family(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['gn_target'] = global_state.random('users', state.world, default = '')

class request_join_family(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['name'] = global_state.random('families', state.world, default = '')

class set_role_family(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['gn_target'] = state.random('familylist', default = '')
		self.fn['data']['role'] = random.choice([0, 4, 8])

class set_icon_family(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['icon'] = random.randint(0, 4)

class set_blackboard_family(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['msg'] = f'Blackboard updated by {state.gn}'

class set_notice_family(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['msg'] = f'Notice updated by {state.gn}'

class change_name_family(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['name'] = 'family_' + ''.join(random.choice(string.digits) for _ in range(15))
	
	def after_call(self, global_state, state, metric):
		if metric.resp['status'] == 0:
			global_state.remove('families', state.world, state.fn)
			state.fn = metric.resp['data']['name']
			global_state.add('families', state.world, state.fn)

class disband_family(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class cancel_disband_family(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class check_in_family(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class abdicate_family(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['target'] = state.random('familylist', default = '')

class search_family(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['family_name'] = global_state.random('families', state.world, default = '')

class get_random_family(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)



# Friend
class get_all_friend(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def after_call(self, global_state, state, metric):
		state.friendlist = {f['gn'] for f in metric.resp['data']['friends']}

class send_gift_all(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class send_gift_friend(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

	def before_call(self, global_state, state):
		self.fn['data']['gn_target'] = state.random('friendlist', default = state.gn)

class request_friend(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

	def before_call(self, global_state, state):
		self.fn['data']['gn_target'] = global_state.random('users', state.world)

class remove_friend(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

	def before_call(self, global_state, state):
		if len(state.friendlist) != 0:
			self.fn['data']['gn_target'] = state.friendlist.pop()
		else:
			self.fn['data']['gn_target'] = state.gn

class respond_friend(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		key = ''
		for mail in state.mail:
			if mail['type'] == 2:
				key = mail['key']
		self.fn['data']['key'] = key
	
	def after_call(self, global_state, state, metric):
		if metric.resp['status'] == 0:
			state.friendlist.add(metric.resp['data']['gn'])

# Factory
class refresh_factory(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class upgrade_factory(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['fid'] = random.randint(0, 3)

class buy_worker_factory(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['fid'] = random.randint(0, 3)
		self.fn['data']['num'] = 1

class activate_wishing_pool_factory(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['wid'] = random.randint(1, 30)

class set_armor_factory(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['aid'] = random.randint(1, 4)

class buy_acceleration_factory(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

# Lottery
class fortune_wheel_basic(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['item'] = random.randint(1, 5)

class fortune_wheel_pro(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['item'] = random.randint(1, 5)

# Mail
class get_all_mail(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def after_call(self, global_state, state, metric):
		state.mail = metric.resp['data']['mail']

class get_new_mail(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

	def after_call(self, global_state, state, metric):
		state.mail.extend(metric.resp['data']['mail'])

class delete_mail(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['key'] = state.random('mail', default = {'key' : ''})['key']
	
	def after_call(self, global_state, state, metric):
		if metric.resp['status'] == 0:
			for key in metric.resp['data']['keys']:
				with contextlib.suppress(ValueError):
					state.mail.remove(key)

class delete_read_mail(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

	def after_call(self, global_state, state, metric):
		state.mail = [m for m in state.mail if m['key'] not in metric.resp['data']['keys']]

class mark_read_mail(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

	def before_call(self, global_state, state):
		self.fn['data']['key'] = state.random('mail', default = {'key' : ''})['key']
	

class send_mail(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['gn_target'] = global_state.random('users', state.world)
		self.fn['data']['subj'] = f'Message from {state.gn}'
		self.fn['data']['body'] = 'Hey whats up!!!!'

# Player
class enter_world(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		state.world = 's0'

	def after_call(self, global_state, state, metrics):
		if metrics.resp['status'] == 0:
			state.functions.put(FunctionList.get('get_info_player'))
		else:
			state.functions.put(FunctionList.get('create_player'))



class create_player(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['gn'] = 'sim_' + ''.join(random.choice(string.digits) for _ in range(15))
	
	def after_call(self, global_state, state, metrics):
		if metrics.resp['status'] != 0:
			raise Exception('GN Already Taken')
		state.gn = metrics.resp['data']['gn']
		state.functions.put(FunctionList.get('add_resources'))

class get_info_player(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def after_call(self, global_state, state, metric):
		state.gn = metric.resp['data']['gn']
		state.fn = metric.resp['data']['family_name']
		if state.gn:
			global_state.add('users', state.world, state.gn)
		if state.fn:
			global_state.add('families', state.world, state.fn)

class accept_gifts(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['gift'] = [m['key'] for m in state.mail if m['type'] == 1]
		self.fn['data']['other'] = [m['key'] for m in state.mail if m['type'] != 1]

# Role
class level_up_role(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['role'] = random.randint(1, 2)
		self.fn['data']['amount'] = random.randint(0, 30000)

class level_up_star_role(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['role'] = random.randint(1, 2)

# Skill
class get_all_skill(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class level_up_skill(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['skill'] = random.randint(0, 38)
		self.fn['data']['item'] = random.randint(6, 8)


# Summoning
class basic_summon(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['item'] = random.randint(1, 5)

class pro_summon(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['item'] = random.randint(1, 5)

class friend_summon(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['item'] = random.randint(1, 5)

class basic_summon_skill(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['item'] = random.randint(1, 5)


class pro_summon_skill(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['item'] = random.randint(1, 5)

class friend_summon_skill(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['item'] = random.randint(1, 5)

class basic_summon_role(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['item'] = random.randint(1, 5)

class pro_summon_role(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['item'] = random.randint(1, 5)

class friend_summon_role(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['item'] = random.randint(1, 5)

class pro_summon_10_times(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['item'] = random.randint(1, 5)

class friend_summon_10_times(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['item'] = random.randint(1, 5)

class basic_summon_skill_10_times(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['item'] = random.randint(1, 5)

class pro_summon_skill_10_times(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['item'] = random.randint(1, 5)

class friend_summon_skill_10_times(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['item'] = random.randint(1, 5)

class basic_summon_role_10_times(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['item'] = random.randint(1, 5)

class pro_summon_role_10_times(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['item'] = random.randint(1, 5)

class friend_summon_role_10_times(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['item'] = random.randint(1, 5)

class refresh_diamond_store(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class refresh_coin_store(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class refresh_gift_store(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class buy_refresh_diamond(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class buy_refresh_coin(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class buy_refresh_gift(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class single_pump_diamond(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class single_pump_coin(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class single_pump_gift(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class dozen_pump_diamond(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class dozen_pump_coin(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class dozen_pump_gift(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class integral_convert(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

# Weapon
class level_up_weapon(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['weapon'] = random.randint(1, 30)
		self.fn['data']['amount'] = random.randint(30, 400)

class level_up_star_weapon(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['weapon'] = random.randint(1, 30)

class level_up_passive_weapon(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['weapon'] = random.randint(1, 30)
		self.fn['data']['passive'] = random.randint(1, 4)

class reset_skill_point_weapon(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, global_state, state):
		self.fn['data']['weapon'] = random.randint(1, 30)





#######################################################################################
class FunctionList:
	'''
	loads the list of all functions declared in this file.
	this removes the need to manually add function classes to a list.
	'''
	def load_functions():
		special, normal = {}, {}
		for name, obj in inspect.getmembers(sys.modules[__name__]):
			if inspect.isclass(obj) and obj != Function and issubclass(obj, Function):
				if name not in {'login_unique', 'enter_world', 'create_player', 'get_info_player', \
						'add_resources'}:
					normal[name] = obj
				else:
					special[name] = obj
		return special, normal

	special, normal = load_functions()
	seq = [f for f in normal.values()]	

	@staticmethod
	def get(fn = None):
		if fn:
			with contextlib.suppress(KeyError):
				return FunctionList.special[fn]()
			return FunctionList.normal[fn]()
		return random.choice(FunctionList.seq)()


