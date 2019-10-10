import json
import requests

from utility import config_reader
from utility import repeating_timer
from module import mail
from module import enums
from module import skill
from module import family
from module import friend
from module import common
from module import account
from module import lottery
from module import weapon
from module import summoning
from module import achievement
from module import armor
from module import player
from module import role
from module import task
from datetime import datetime, timedelta


CFG = config_reader.wait_config()

TOKEN_BASE_URL = CFG['token_server']['addr'] + ':' + CFG['token_server']['port']
MAIL_BASE_URL = CFG['mail_server']['addr'] + ':' + CFG['mail_server']['port']
#MAIL_BASE_URL = 'http://127.0.0.1:8020'

class MessageHandler:
	def __init__(self):
		self._functions = FUNCTION_LIST
		self._is_first_start = True
		self.is_first_month = False
		self._boss_life=[]
		self._boss_life_remaining=[]
		self._timer = repeating_timer.RepeatingTimer(5, self._refresh_configuration)
		self._timer.start()

	def firstDayOfMonth(self, dt):
		return (dt + timedelta(days= -dt.day + 1)).replace(hour=0, minute=0, second=0, microsecond=0)
	def _refresh_configuration(self):
		r = requests.get('http://localhost:8000/get_game_manager_config')
		d = r.json()
		self._mall_config = d['mall']
		self._factory_config = d['factory']
		self._family_config = d['family']
		self._stage_reward = d['reward']
		self._skill_scroll_functions = d['skill']['skill_scroll_functions']
		self._upgrade_chance = d['skill']['upgrade_chance']
		self._weapon_config = d['weapon']
		self._role_config = d['role']
		self._lottery = d['lottery']
		self._player = d['player']
		self._hang_reward = d['hang_reward']
		self._entry_consumables = d['entry_consumables']
		self._announcement = d['announcement']
		self._player_experience = d['player_experience']
		self._monster_config = d['monster_config']
		self._level_enemy_layouts = d['level_enemy_layouts']
		self._acheviement = d['acheviement']
		self._task = d['task']
		self._check_in = d['check_in']
		self._vip_config = d['vip_config']
		if self.firstDayOfMonth(datetime.today()).day == datetime.today().day and self.is_first_month==False:
			self._is_first_start = True
			self.is_first_month=True
		if self.firstDayOfMonth(datetime.today()).day != datetime.today().day and self.is_first_month==True:
			self.is_first_month=False
		if self._is_first_start:
			self._boss_life=[]
			self._boss_life_remaining=[]
			self._is_first_start = False
			self._world_boss = d['world_boss']
			self._max_enter_time = self._world_boss['max_enter_time']
			self._max_upload_damage = self._world_boss['max_upload_damage']
			for i in range(0,10):
				self._boss_life_remaining.append(self._world_boss["boss"+str(i+1)]["life_value"])
				self._boss_life.append(self._world_boss["boss"+str(i+1)]["life_value"])


	async def shutdown(self):
		pass

	# json.decoder.JSONDecodeError
	async def resolve(self, message: str, resource) -> str:
		'''
		Resolves the message included in the request. If required, ensures that a valid token is present.
		'''
		message = json.loads(message)
		try:
			fn = self._functions[message['function']]
		except KeyError:
			return '{"status" : 10, "message" : "function is not in function list"}'
		if message['function'] not in DOES_NOT_NEED_TOKEN:
			try:
				validated, uid = await self.validate_token(message, resource['session'])
				if not validated: return '{"status" : 11, "message" : "invalid token"}'
				message['data']['unique_id'] = uid
			except KeyError:
				return '{"status" : 12, "message" : "token not present"}'
		message['session'] = resource['session']
		message['redis'] = resource['redis']
		message['worlddb'] = resource['db']
		message['accountdb'] = resource['accountdb']
		message['tokenserverbaseurl'] = TOKEN_BASE_URL
		message['mailserverbaseurl'] = MAIL_BASE_URL
		message['world'] = '0'
		return json.dumps(await fn(self, message))

	async def validate_token(self, msg, session):
		async with session.post(TOKEN_BASE_URL + '/validate', data = {'token' : msg['data']['token']}) as r:
			validated = await r.json(content_type = 'text/json')
			return (False, None) if validated['status'] != 0 else (True, validated['data']['unique_id'])


	###################### account.py ######################
	async def _login_unique(self, data: dict) -> str:
		return await account.login_unique(data['data']['unique_id'], **data)

	async def _login(self, data: dict) -> str:
		return await account.login(data['data']['identifier'], data['data']['value'], data['data']['password'], **data)

	async def _bind_account(self, data: dict) -> str:
		return await account.bind_account(data['data']['unique_id'], data['data']['account'], data['data']['password'], **data)

	async def _bind_email(self, data: dict) -> str:
		return await account.bind_email(data['data']['unique_id'], data['data']['email'], **data)

	async def _verify_email_code(self, data: dict) -> str:
		return await account.verify_email_code(data['data']['unique_id'], data['data']['code'], **data)

	# TODO


	async def _get_player_info(self, data: dict) -> str:
		return await player.get_player_info(data['data']['unique_id'], **data)

	async def _get_player_config(self, data: dict) -> str:
		return common.mt(0, 'success', {'player_config': self._player})

	async def _create_account(self, data: dict) -> str:
		return 'function'

	async def _change_game_name(self, data: dict) -> str:
		return 'function'

	###################### player.py ######################
	async def _create_player(self, data: dict) -> str:
		return await player.create(data['data']['unique_id'], data['data']['gn'], **data)

	async def _enter_world(self, data: dict) -> str:
		return await player.enter_world(data['data']['unique_id'], **data)

	async def _get_account_world_info(self, data: dict) -> str:
		return await player.get_account_world_info(data['data']['unique_id'], **data)

	async def _accept_gift(self, data: dict) -> str:
		return await player.accept_gift(data['data']['unique_id'], data['data']['key'], **data)


	###################### family.py ######################
	async def _create_family(self, data: dict) -> str:
		return await family.create(data['data']['unique_id'], data['data']['name'], **data)

	async def _leave_family(self, data: dict) -> str:
		return await family.leave(data['data']['unique_id'], **data)

	async def _remove_user_family(self, data: dict) -> str:
		return await family.remove_user(data['data']['unique_id'], data['data']['gn_target'], **data)

	async def _invite_user_family(self, data: dict) -> str:
		return await family.invite_user(data['data']['unique_id'], data['data']['gn_target'], **data)

	async def _request_join_family(self, data: dict) -> str:
		return await family.request_join(data['data']['unique_id'], data['data']['name'], **data)

	async def _respond_family(self, data: dict) -> str:
		return await family.respond(data['data']['unique_id'], data['data']['key'], **data)

	# TODO

	async def _sign_in_family(self, data: dict) -> str:
		return 'function'

	async def _get_store_family(self, data: dict) -> str:
		return 'function'

	async def _market_purchase_family(self, data: dict) -> str:
		return 'function'

	async def _gift_package_family(self, data: dict) -> str:
		return 'function'

	async def _officer_family(self, data: dict) -> str:
		return 'function'

	async def _dismiss_officer_family(self, data: dict) -> str:
		return 'function'

	async def _change_name_family(self, data: dict) -> str:
		return 'function'

	async def _blackboard_family(self, data: dict) -> str:
		return 'function'

	async def _announcement_family(self, data: dict) -> str:
		return 'function'

	async def _update_login_in_time(self, data: dict) -> str:
		return 'function'

	async def _disband_family(self, data: dict) -> str:
		return 'function'

	async def _cancel_disbanded_family(self, data: dict) -> str:
		return 'function'

	async def _get_config_family(self, data: dict) -> str:
		return 'function'

	async def _get_all_info_family(self, data: dict) -> str:
		return 'function'

	###################### mail.py ######################
	async def _send_mail(self, data: dict) -> str:
		return await mail.send_mail(enums.MailType.SIMPLE, await family._get_uid(data['data']['gn_target'], **data), **data)

	async def _get_new_mail(self, data: dict) -> str:
		return await mail.get_new_mail(data['data']['unique_id'], **data)

	async def _get_all_mail(self, data: dict) -> str:
		return await mail.get_all_mail(data['data']['unique_id'], **data)

	async def _delete_mail(self, data: dict) -> str:
		return await mail.delete_mail(data['data']['unique_id'], data['data']['key'], **data)

	async def _delete_read_mail(self, data: dict) -> str:
		return await mail.delete_read(data['data']['unique_id'], **data)

	async def _mark_read_mail(self, data: dict) -> str:
		return await mail.mark_read(data['data']['unique_id'], data['data']['key'], **data)

	# TODO
	async def _send_merchandise(self, data: dict) -> str:
		return 'function'

	###################### summoning.py ######################
	async def _basic_summon(self, data: dict) -> str:
		return await summoning.summon(data['data']['unique_id'], enums.Item(int(data['data']['item'])), enums.Tier.BASIC, enums.Group.WEAPON, **data)

	async def _pro_summon(self, data: dict) -> str:
		return await summoning.summon(data['data']['unique_id'], enums.Item(int(data['data']['item'])), enums.Tier.PRO, enums.Group.WEAPON, **data)

	async def _friend_summon(self, data: dict) -> str:
		return await summoning.summon(data['data']['unique_id'], enums.Item(int(data['data']['item'])), enums.Tier.FRIEND, enums.Group.WEAPON, **data)

	async def _prophet_summon(self, data: dict) -> str:
		return await summoning.summon(data['data']['unique_id'], enums.Item(int(data['data']['item'])), enums.Tier.PROPHET, enums.Group.WEAPON, **data)

	async def _basic_summon_skill(self, data: dict) -> str:
		return await summoning.summon(data['data']['unique_id'], enums.Item(int(data['data']['item'])), enums.Tier.BASIC, enums.Group.SKILL, **data)

	async def _pro_summon_skill(self, data: dict) -> str:
		return await summoning.summon(data['data']['unique_id'], enums.Item(int(data['data']['item'])), enums.Tier.PRO, enums.Group.SKILL, **data)

	async def _friend_summon_skill(self, data: dict) -> str:
		return await summoning.summon(data['data']['unique_id'], enums.Item(int(data['data']['item'])), enums.Tier.FRIEND, enums.Group.SKILL, **data)

	async def _basic_summon_role(self, data: dict) -> str:
		return await summoning.summon(data['data']['unique_id'], enums.Item(int(data['data']['item'])), enums.Tier.BASIC, enums.Group.ROLE, **data)

	async def _pro_summon_role(self, data: dict) -> str:
		return await summoning.summon(data['data']['unique_id'], enums.Item(int(data['data']['item'])), enums.Tier.PRO, enums.Group.ROLE, **data)

	async def _friend_summon_role(self, data: dict) -> str:
		return await summoning.summon(data['data']['unique_id'], enums.Item(int(data['data']['item'])), enums.Tier.FRIEND, enums.Group.ROLE, **data)

	async def _basic_summon_10_times(self, data: dict) -> str:
		return await summoning.summon_multi(data['data']['unique_id'], enums.Item(int(data['data']['item'])), enums.Tier.BASIC, enums.Group.WEAPON, **data)

	async def _pro_summon_10_times(self, data: dict) -> str:
		return await summoning.summon_multi(data['data']['unique_id'], enums.Item(int(data['data']['item'])), enums.Tier.PRO, enums.Group.WEAPON, **data)

	async def _friend_summon_10_times(self, data: dict) -> str:
		return await summoning.summon_multi(data['data']['unique_id'], enums.Item(int(data['data']['item'])), enums.Tier.FRIEND, enums.Group.WEAPON, **data)

	async def _basic_summon_skill_10_times(self, data: dict) -> str:
		return await summoning.summon_multi(data['data']['unique_id'], enums.Item(int(data['data']['item'])), enums.Tier.BASIC, enums.Group.SKILL, **data)

	async def _pro_summon_skill_10_times(self, data: dict) -> str:
		return await summoning.summon_multi(data['data']['unique_id'], enums.Item(int(data['data']['item'])), enums.Tier.PRO, enums.Group.SKILL, **data)

	async def _friend_summon_skill_10_times(self, data: dict) -> str:
		return await summoning.summon_multi(data['data']['unique_id'], enums.Item(int(data['data']['item'])), enums.Tier.FRIEND, enums.Group.SKILL, **data)

	async def _basic_summon_role_10_times(self, data: dict) -> str:
		return await summoning.summon_multi(data['data']['unique_id'], enums.Item(int(data['data']['item'])), enums.Tier.BASIC, enums.Group.ROLE, **data)

	async def _pro_summon_role_10_times(self, data: dict) -> str:
		return await summoning.summon_multi(data['data']['unique_id'], enums.Item(int(data['data']['item'])), enums.Tier.PRO, enums.Group.ROLE, **data)

	async def _friend_summon_role_10_times(self, data: dict) -> str:
		return await summoning.summon_multi(data['data']['unique_id'], enums.Item(int(data['data']['item'])), enums.Tier.FRIEND, enums.Group.ROLE, **data)

	###################### lottery.py ######################
	async def _fortune_wheel_basic(self, data: dict) -> str:
		return await lottery.fortune_wheel(data['data']['unique_id'], enums.Tier.BASIC, enums.Item(int(data['data']['item'])), **data)

	async def _fortune_wheel_pro(self, data: dict) -> str:
		return await lottery.fortune_wheel(data['data']['unique_id'], enums.Tier.PRO, enums.Item(int(data['data']['item'])), **data)

	async def _get_config_info_lottery(self, data: dict) -> str:
		return 'function'

	###################### skill.py ######################
	async def _get_skill(self, data: dict) -> str:
		return await skill.get_skill(data['data']['unique_id'], int(data['data']['skill']), **data)

	async def _get_all_skill(self, data: dict) -> str:
		return await skill.get_all_levels(data['data']['unique_id'], **data)

	async def _level_up_skill(self, data: dict) -> str:
		return await skill.level_up(data['data']['unique_id'], int(data['data']['skill']), int(data['data']['item']),  **data)

	# TODO
	async def _get_level_up_config_skill(self, data: dict) -> str:
		return 'function'

	###################### friend.py ######################
	async def _get_all_friend(self, data: dict) -> str:
		return await friend.get_all(data['data']['unique_id'], **data)

	async def _remove_friend(self, data: dict) -> str:
		return await friend.remove(data['data']['unique_id'], data['data']['gn_target'], **data)

	async def _request_friend(self, data: dict) -> str:
		return await friend.request(data['data']['unique_id'], data['data']['gn_target'], **data)

	async def _respond_friend(self, data: dict) -> str:
		return await friend.respond(data['data']['unique_id'], data['data']['key'], **data)

	async def _send_gift_friend(self, data: dict) -> str:
		return await friend.send_gift(data['data']['unique_id'], data['data']['gn_target'], **data)

	# TODO 原 send_all_friend_gift
	async def _send_all_gift_friend(self, data: dict) -> str:
		return 'function'

	# TODO 原 redeem_all_nonce
	async def _accept_all_gift_friend(self, data: dict) -> str:
		return 'function'

	###################### weapon.py ######################
	async def _level_up_weapon(self, data: dict) -> str:
		return await weapon.level_up(data['data']['unique_id'], int(data['data']['weapon']), int(data['data']['amount']), **data)

	async def _level_up_passive_weapon(self, data: dict) -> str:
		return await weapon.level_up_passive(data['data']['unique_id'], int(data['data']['weapon']), int(data['data']['passive']), **data)

	async def _level_up_star_weapon(self, data: dict) -> str:
		return await weapon.level_up_star(data['data']['unique_id'], int(data['data']['weapon']), **data)

	async def _reset_skill_point_weapon(self, data: dict) -> str:
		return await weapon.reset_skill_point(data['data']['unique_id'], int(data['data']['weapon']), **data)
	
	async def _get_all_weapon(self, data: dict) -> str:
		return await weapon.get_all(data['data']['unique_id'], **data)

	async def _get_config_weapon(self, data: dict) -> str:
		return await weapon.get_config(**data)

	###################### role.py ######################
	async def _get_all_role(self, data: dict) -> str:
		return await role.get_all(data['data']['unique_id'], **data)

	async def _level_up_role(self, data: dict) -> str:
		return await role.level_up(data['data']['unique_id'], int(data['data']['role']), int(data['data']['amount']), **data)

	async def _level_up_star_role(self, data: dict) -> str:
		return await role.level_up_star(data['data']['unique_id'], int(data['data']['role']), **data)

	async def _get_config_role(self, data: dict) -> str:
		return await role.get_config(**data)





	###################### 签到系统 ######################
	# TODO
	async def _check_in(self, data: dict) -> str:
		return 'function'

	async def _supplement_check_in(self, data: dict) -> str:
		return 'function'

	async def _get_all_check_in_table(self, data: dict) -> str:
		return common.mt(0, 'success', {'check_in': [{'date':  '2019-10-05', 'reward': 0}, {'date':  '2019-10-06', 'reward': 0}]})

	###################### VIP ######################
	# TODO
	async def _purchase_vip_gift(self, data: dict) -> str:
		return 'function'

	async def _check_vip_daily_reward(self, data: dict) -> str:
		return 'function'

	async def _purchase_vip_card(self, data: dict) -> str:
		return 'function'

	async def _get_all_vip_info(self, data: dict) -> str:
		return {'status' : 0, 'message' : 'temp function success', 'data' :{'vip' :
					{
						'level':"4",
						'exp':"2000",
						'full_exp':"1000",
						'vip_dialy_reward':
							{
							"diamond_card":10,
							"coin":0,
							"small_energy_potion":0,
							"food_card":0,
							"mine_card":0,
							"crystal_card":0
							},
						'vip_speical_package':
							{
									"price":300,
									"item":
									{
										"small_energy_potion":4,
										"universal_segment":20,
										"universal_segment_6":0
									},
							}
					}}}

	###################### player ######################
	# TODO
	async def _exchange_card(self, data: dict) -> str:
		return 'function'

	async def _get_all_resource(self, data: dict) -> str:
		return await player.get_all_resource(data['data']['unique_id'], **data)

	###################### achievement ######################
	async def _get_all_achievement(self, data: dict) -> str:
		return await achievement.get_all_achievement(data['data']['unique_id'], **data)

	###################### armor ######################
	# TODO
	async def _upgrade_armor(self, data: dict) -> str:
		return 'function'

	async def _get_all_armor(self, data: dict) -> str:
		return await armor.get_all_armor(data['data']['unique_id'], **data)

	###################### stage ######################
	async def _get_all_tower(self, data: dict) -> str:
		return common.mt(0, 'success', {'tower_config': self._entry_consumables})

	###################### tasks ######################
	async def _get_all_task(self, data: dict) -> str:
		return await task.get_all_task(data['data']['unique_id'], **data)
		# return common.mt(0, 'success', {'tasks': [{'tid': 1, 'value': 1, 'reward': 0, 'timer': '2019-10-05'}, {'tid': 2, 'value': 1, 'reward': 0, 'timer': '2019-10-06'}]})




	# TODO 新增
	async def _automatically_refresh_store(self, data: dict) -> str:
		darkmarket = {
			"refresh_time": "2019-10-10 12:41:52",
			"refreshable_quantity": 3,
			"items": [
				{"item":1,"quantity":100, "currency_item":5,"quantity":100},
				{"item":2,"quantity":1200,"currency_item":5,"quantity":100},
				{"item":3,"quantity":3100,"currency_item":5,"quantity":100},
				{"item":4,"quantity":100, "currency_item":5,"quantity":100},
				{"item":5,"quantity":1200,"currency_imte":5,"quantity":100},
				{"item":6,"quantity":1200,"currency_imte":5,"quantity":100},
				{"item":7,"quantity":1200,"currency_imte":5,"quantity":100},
				{"item":8,"quantity":1200,"currency_imte":5,"quantity":100}
			]
		}
		return common.mt(0, 'success', {'darkmarket': darkmarket})

	# TODO Done 在这里直接返回配置信息，后面配置信息存放位置变动会做相应的改动
	async def _stage_reward_config(self, data: dict) -> str:
		return common.mt(0, 'success', {'config': self._stage_reward})

	# TODO Done 在这里直接返回配置信息，后面配置信息存放位置变动会做相应的改动
	async def _get_lottery_config_info(self, data: dict) -> str:
		cost = {
			"skills": self._lottery["skills"]["cost"],
			"weapons": self._lottery["weapons"]["cost"],
			"roles": self._lottery["roles"]["cost"],
			"fortune_wheel": self._lottery["fortune_wheel"]["cost"]
		}
		return common.mt(0, 'success', {'config': cost})

	# TODO
	async def _get_hang_up_info(self, data: dict) -> str:
		# 这个信息不知道怎么去拿，后面详细说一下，新数据库不知道这些放到哪里了
		# sql_str = "SELECT hang_up_time, hang_stage, stage, tower_stage FROM player WHERE unique_id='%s'" % unique_id
		return 'function'

	# TODO
	async def _check_boss_status(self, data: dict) -> str:
		return {'status' : 0, 'message' : 'temp function success', 'data' :{'boss' :{'world_boss_enter_time':"2019/10/10 17:00:00",'world_boss_remaining_times':"20",'hp_values':["%.2f" %(int(self._boss_life_remaining[i])/int(self._boss_life[i])) for i in range(0,9)]}}}

	# TODO Done 在这里直接返回配置信息，后面配置信息存放位置变动会做相应的改动
	async def _get_family_config(self, data: dict) -> str:
		return common.mt(0, 'success', {'config': self._family_config})

	# TODO Done 在这里直接返回配置信息，后面配置信息存放位置变动会做相应的改动
	async def _get_factory_info(self, data: dict) -> str:
		return common.mt(0, 'success', {'config': self._factory_config})

	# TODO
	async def _refresh_all_storage(self, data: dict) -> str:
		return {'status' : 0, 'message' : 'temp function success', 'data' :
				{
					'worker':200,
					'factory':
					[
						{"fid":0,"worker":5,"level":5,"storage":2222,"time":"2019-01-01 22:22:22","setting":""},
						{"fid":1,"worker":5,"level":5,"storage":2222,"time":"2019-01-01 22:22:22","setting":""},
						{"fid":2,"worker":5,"level":15,"storage":2222,"time":"2019-01-01 22:22:22","setting":""},
						{"fid":3,"worker":5,"level":35,"storage":2222,"time":"2019-01-01 22:22:22","setting":{"armorid":1}},
						{"fid":4,"worker":0,"level":35,"storage":0,"time":"2019-01-01 22:22:22","setting":""},
					]
				}
		}

	async def _get_all_family_info(self, data: dict) -> str:
		return {"status" : 0, "message" : "temp function success", "data" :
    			{
					"famliy" :{"name":"LOL","icon":"2","exp":1222,"notice":"everyone must buy red pack","announcement":"we are top family"},
					"member":
					[
						{"name":"Matthew","level":"100","postion":"0","check_in":0},
						{"name":"houyao","level":"100","postion":"1","check_in":0},
						{"name":"覃yupeng","level":"100","postion":"2","check_in":0}
					],
					"blackboard":
					[
						["Matthew kick out children"],
						["children join our family, welcome!"],
						["children bought red pack for everyone"],
						["Matthew set children as owner"],
						["children disband family, family will disband in 24 hours"],
						["Matthew cancel disband family"],
						["children leave family"]
					]
				}
				}





	###################### TODO.py ######################
	async def _get_all_supplies(self, data: dict) -> str:
		return {'status' : 0, 'message' : 'temp function success', 'data' : {'remaining' : {}}}


##########################################################################################################
##########################################################################################################

DOES_NOT_NEED_TOKEN = {'login_unique', 'login'}

FUNCTION_LIST = {
	###################### TODO.py ######################
	'get_all_supplies' : MessageHandler._get_all_supplies,


	###################### account.py ######################
	'login_unique' : MessageHandler._login_unique,
	'login' : MessageHandler._login,
	'bind_account' : MessageHandler._bind_account,
	'bind_email' : MessageHandler._bind_email,
	'verify_email_code' : MessageHandler._verify_email_code,
	# TODO
	'get_player_info' : MessageHandler._get_player_info,
	'get_player_config' : MessageHandler._get_player_config,
	'create_account' : MessageHandler._create_account,
	'change_game_name' : MessageHandler._change_game_name,

	###################### player.py ######################
	'enter_world' : MessageHandler._enter_world,
	'accept_gift' : MessageHandler._accept_gift,
	'create_player' : MessageHandler._create_player,
	'get_account_world_info' : MessageHandler._get_account_world_info,

	###################### family.py ######################
	'create_family': MessageHandler._create_family,
	'leave_family' : MessageHandler._leave_family,
	'remove_user_family' : MessageHandler._remove_user_family,
	'invite_user_family' : MessageHandler._invite_user_family,
	'request_join_family' : MessageHandler._request_join_family,
	'respond_family' : MessageHandler._respond_family,
	# TODO
	'sign_in_family' : MessageHandler._sign_in_family,
	'get_store_family' : MessageHandler._get_store_family,
	'market_purchase_family' : MessageHandler._market_purchase_family,
	'gift_package_family' : MessageHandler._gift_package_family,
	'officer_family' : MessageHandler._officer_family,
	'dismiss_officer_family' : MessageHandler._dismiss_officer_family,
	'change_name_family' : MessageHandler._change_name_family,
	'blackboard_family' : MessageHandler._blackboard_family,
	'announcement_family' : MessageHandler._announcement_family,
	'update_login_in_time' : MessageHandler._update_login_in_time,
	'disband_family' : MessageHandler._disband_family,
	'cancel_disbanded_family' : MessageHandler._cancel_disbanded_family,
	'get_config_family' : MessageHandler._get_config_family,
	'get_all_info_family' : MessageHandler._get_all_info_family,

	###################### mail.py ######################
	'send_mail' : MessageHandler._send_mail,
	'get_new_mail' : MessageHandler._get_new_mail,
	'get_all_mail' : MessageHandler._get_all_mail,
	'delete_mail' : MessageHandler._delete_mail,
	'delete_read_mail' : MessageHandler._delete_read_mail,
	'mark_read_mail' : MessageHandler._mark_read_mail,
	# TODO
	'send_merchandise' : MessageHandler._send_merchandise,

	###################### summoning.py ######################
	'basic_summon' : MessageHandler._basic_summon,
	'pro_summon' : MessageHandler._pro_summon,
	'friend_summon' : MessageHandler._friend_summon,
	'prophet_summon' : MessageHandler._friend_summon,
	'basic_summon_skill' : MessageHandler._basic_summon_skill,
	'pro_summon_skill' : MessageHandler._pro_summon_skill,
	'friend_summon_skill' : MessageHandler._friend_summon_skill,
	'basic_summon_role' : MessageHandler._basic_summon_role,
	'pro_summon_role' : MessageHandler._pro_summon_role,
	'friend_summon_role' : MessageHandler._friend_summon_role,
	'basic_summon_10_times' : MessageHandler._basic_summon_10_times,
	'pro_summon_10_times' : MessageHandler._pro_summon_10_times,
	'friend_summon_10_times' : MessageHandler._friend_summon_10_times,
	'basic_summon_skill_10_times' : MessageHandler._basic_summon_skill_10_times,
	'pro_summon_skill_10_times' : MessageHandler._pro_summon_skill_10_times,
	'friend_summon_skill_10_times' : MessageHandler._friend_summon_skill_10_times,
	'basic_summon_role_10_times' : MessageHandler._basic_summon_role_10_times,
	'pro_summon_role_10_times' : MessageHandler._pro_summon_role_10_times,
	'friend_summon_role_10_times' : MessageHandler._friend_summon_role_10_times,

	###################### lottery.py ######################
	'fortune_wheel_basic' : MessageHandler._fortune_wheel_basic,
	'fortune_wheel_pro' : MessageHandler._fortune_wheel_pro,
	# TODO
	'get_config_info_lottery' : MessageHandler._get_config_info_lottery,

	###################### skill.py ######################
	'get_skill' : MessageHandler._get_skill,
	'get_all_skill' : MessageHandler._get_all_skill,
	'level_up_skill' : MessageHandler._level_up_skill,
	# TODO
	'get_level_up_config_skill': MessageHandler._get_level_up_config_skill,

	###################### friend.py ######################
	'get_all_friend' : MessageHandler._get_all_friend,
	'remove_friend' : MessageHandler._remove_friend,
	'request_friend' : MessageHandler._request_friend,
	'respond_friend' : MessageHandler._respond_friend,
	'send_gift_friend' : MessageHandler._send_gift_friend,
	# TODO
	'send_all_gift_friend' : MessageHandler._send_all_gift_friend,
	'accept_all_gift_friend' : MessageHandler._accept_all_gift_friend,

	###################### weapon.py ######################
	'level_up_weapon' : MessageHandler._level_up_weapon,
	'level_up_passive_weapon' : MessageHandler._level_up_passive_weapon,
	'level_up_star_weapon' : MessageHandler._level_up_star_weapon,
	'reset_skill_point_weapon' : MessageHandler._reset_skill_point_weapon,
	'get_all_weapon' : MessageHandler._get_all_weapon,
	'get_config_weapon' : MessageHandler._get_config_weapon,

	# TODO
	###################### role.py ######################
	'level_up_star_role' : MessageHandler._level_up_star_role,
	'level_up_role' : MessageHandler._level_up_role,
	'get_all_role' : MessageHandler._get_all_role,
	'get_config_role' : MessageHandler._get_config_role,

	# TODO
	###################### 签到系统 ######################
	'check_in' : MessageHandler._check_in,
	'supplement_check_in' : MessageHandler._supplement_check_in,
	'get_all_check_in_table' : MessageHandler._get_all_check_in_table,

	# TODO
	###################### VIP ######################
	'purchase_vip_gift' : MessageHandler._purchase_vip_gift,
	'check_vip_daily_reward' : MessageHandler._check_vip_daily_reward,
	'purchase_vip_card' : MessageHandler._purchase_vip_card,
	'get_all_vip_info': MessageHandler._get_all_vip_info,

	# TODO
	###################### player ######################
	'exchange_card': MessageHandler._exchange_card,
	'get_all_resource': MessageHandler._get_all_resource,

	# TODO
	###################### achievement ######################
	'get_all_achievement': MessageHandler._get_all_achievement,

	# TODO
	###################### armor ######################
	'upgrade_armor': MessageHandler._upgrade_armor,
	'get_all_armor': MessageHandler._get_all_armor,

	# TODO
	###################### stage ######################
	'get_all_tower': MessageHandler._get_all_tower,

	###################### tasks ######################
	'get_all_task': MessageHandler._get_all_task,


	# TODO 新增
	'automatically_refresh_store': MessageHandler._automatically_refresh_store,
	'stage_reward_config': MessageHandler._stage_reward_config,
	'get_lottery_config_info': MessageHandler._get_lottery_config_info,
	'get_hang_up_info': MessageHandler._get_hang_up_info,
	'check_boss_status':MessageHandler._check_boss_status,
	'get_family_config':MessageHandler._get_family_config,
	'get_factory_info':MessageHandler._get_factory_info,
	'refresh_all_storage':MessageHandler._refresh_all_storage,
	'get_all_family_info': MessageHandler._get_all_family_info
}

