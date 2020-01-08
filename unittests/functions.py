'''
functions.py
'''

import sys
import json
import string
import random
import inspect
import contextlib


class Function:
	def __init__(self, fn):
		self.fn = {'function' : fn, 'data' : {}}
	
	def before_call(self, state):
		pass

	def after_call(self, state, raw):
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

# Account
class login_unique(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['unique_id'] = state['uid']

# Armor
class get_all_armor(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class upgrade_armor(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
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


# Friend
class get_all_friend(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def after_call(self, state, raw):
		resp = json.loads(raw.decode().strip())
		state['friendlist'] = {f['gn'] for f in resp['data']['friends']}

class send_gift_all(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class send_gift_friend(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

	def before_call(self, state):
		if len(state['friendlist']) != 0:
			self.fn['data']['gn_target'] = random.choice(tuple(state['friendlist']))
		else:
			self.fn['data']['gn_target'] = state['gn']

class request_friend(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

	def before_call(self, state):
		self.fn['data']['gn_target'] = random.choice(tuple(state['gamenames'][state['world']]))

class remove_friend(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

	def before_call(self, state):
		if len(state['friendlist']) != 0:
			self.fn['data']['gn_target'] = state['friendlist'].pop()
		else:
			self.fn['data']['gn_target'] = state['gn']

class respond_friend(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		key = ''
		for mail in state['mail']:
			if mail['type'] == 2:
				key = mail['key']
		self.fn['data']['key'] = key
	
	def after_call(self, state, raw):
		resp = json.loads(raw.decode().strip())
		if resp['status'] == 0:
			state['friendlist'].add(resp['data']['gn'])

# Factory
class refresh_factory(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class upgrade_factory(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['fid'] = random.randint(0, 3)

class buy_worker_factory(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['fid'] = random.randint(0, 3)
		self.fn['data']['num'] = 1

class activate_wishing_pool_factory(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['wid'] = random.randint(1, 30)

class set_armor_factory(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['aid'] = random.randint(1, 4)

class buy_acceleration_factory(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

# Lottery
class fortune_wheel_basic(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['item'] = random.randint(1, 5)

class fortune_wheel_pro(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['item'] = random.randint(1, 5)

# Mail
class get_all_mail(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def after_call(self, state, raw):
		resp = json.loads(raw.decode().strip())
		state['mail'] = resp['data']['mail']

class get_new_mail(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

	def after_call(self, state, raw):
		resp = json.loads(raw.decode().strip())
		state['mail'].extend(resp['data']['mail'])

class delete_mail(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		if len(state['mail']) != 0:
			self.fn['data']['key'] = (random.choice(state['mail']))['key']
		else:
			self.fn['data']['key'] = ''
	
	def after_call(self, state, raw):
		resp = json.loads(raw.decode().strip())
		if resp['status'] == 0:
			for k in resp['data']['keys']:
				with contextlib.suppress(ValueError):
					state['mail'].remove(k)

class mark_read_mail(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

	def before_call(self, state):
		if len(state['mail']) != 0:
			self.fn['data']['key'] = (random.choice(state['mail']))['key']
		else:
			self.fn['data']['key'] = ''
	

class send_mail(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['gn_target'] = random.choice(tuple(state['gamenames'][state['world']]))
		self.fn['data']['subj'] = f'Message from {state["gn"]}'
		self.fn['data']['body'] = 'Hey whats up!!!!'

# Player
class enter_world(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class create_player(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['gn'] = 'sim_' + ''.join(random.choice(string.digits) for _ in range(15))

class get_info_player(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def after_call(self, state, raw):
		resp = json.loads(raw.decode().strip())
		state['gn'] = resp['data']['gn']
		state['fn'] = resp['data']['family_name']
		if state['gn'] != '':
			state['gamenames'][state['world']].add(state['gn'])
		if state['fn'] != '':
			state['familynames'][state['world']].add(state['fn'])

class accept_gifts(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['keys'] = [m['key'] for m in state['mail'] if m['type'] == 1]

# Role
class level_up_role(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['role'] = random.randint(1, 2)
		self.fn['data']['amount'] = random.randint(0, 30000)

class level_up_star_role(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['role'] = random.randint(1, 2)

# Skill
class get_all_skill(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)

class level_up_skill(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['skill'] = random.randint(0, 38)
		self.fn['data']['item'] = random.randint(6, 8)


# Summoning
class basic_summon(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['item'] = random.randint(1, 5)

class pro_summon(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['item'] = random.randint(1, 5)

class friend_summon(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['item'] = random.randint(1, 5)

class basic_summon_skill(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['item'] = random.randint(1, 5)


class pro_summon_skill(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['item'] = random.randint(1, 5)

class friend_summon_skill(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['item'] = random.randint(1, 5)

class basic_summon_role(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['item'] = random.randint(1, 5)

class pro_summon_role(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['item'] = random.randint(1, 5)

class friend_summon_role(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['item'] = random.randint(1, 5)

class pro_summon_10_times(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['item'] = random.randint(1, 5)

class friend_summon_10_times(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['item'] = random.randint(1, 5)

class basic_summon_skill_10_times(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['item'] = random.randint(1, 5)

class pro_summon_skill_10_times(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['item'] = random.randint(1, 5)

class friend_summon_skill_10_times(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['item'] = random.randint(1, 5)

class basic_summon_role_10_times(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['item'] = random.randint(1, 5)

class pro_summon_role_10_times(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['item'] = random.randint(1, 5)

class friend_summon_role_10_times(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
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
	
	def before_call(self, state):
		self.fn['data']['weapon'] = random.randint(1, 30)
		self.fn['data']['amount'] = random.randint(30, 400)

class level_up_star_weapon(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['weapon'] = random.randint(1, 30)

class level_up_passive_weapon(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['weapon'] = random.randint(1, 30)
		self.fn['data']['passive'] = random.randint(1, 4)

class reset_skill_point_weapon(Function):
	def __init__(self):
		super().__init__(self.__class__.__name__)
	
	def before_call(self, state):
		self.fn['data']['weapon'] = random.randint(1, 30)





#######################################################################################
class FunctionList:
	def load_functions():
		special, normal = {}, {}
		for name, obj in inspect.getmembers(sys.modules[__name__]):
			if inspect.isclass(obj) and obj != Function and issubclass(obj, Function):
				if name not in {'login_unique', 'enter_world', 'create_player', 'get_info_player'}:
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
				return FunctionList.special[fn]
			return FunctionList.normal[fn]
		return random.choice(FunctionList.seq)


