import json
import account_manager
import game_manager

TOKEN_BASE_URL = 'http://127.0.0.1:8001'

class InvalidTokenError(Exception):
	pass

class MessageHandler:
	def __init__(self):
		self._functions = FUNCTION_LIST
		self.am = account_manager.AccountManager()
		self.gm = game_manager.GameManager()

	# json.decoder.JSONDecodeError
	async def resolve(self, message: str, session) -> str:
		'''
		Resolves the message included in the request. If required, ensures that a valid token is present.
		'''
		try:
			message = json.loads(message)
			fn = self._functions[message['function']]
			if message['function'] not in DOES_NOT_NEED_TOKEN:
				message['data']['unique_id'] = await self.validate_token(message['data']['token'], session)
			return await fn(self, message['data'])
		except InvalidTokenError:
			return '{"status" : 11, "message" : "unauthorized. invalid token."}'
		except KeyError:
			return '{"status" : 10, "message" : "invalid message format"}'

	async def validate_token(self, token, session):
		async with session.post(TOKEN_BASE_URL + '/validate', data = {'token' : token}) as r:
			validated = await r.json(content_type = 'text/json')
			if validated['status'] != 0:
				raise InvalidTokenError
			return validated['data']['unique_id']
			
	async def _login(self, data: dict) -> str:
		return json.dumps(await self.am.login(data['identifier'], data['value'], data['password']))

	async def _login_unique(self, data: dict) -> str:
		return json.dumps(await self.am.login_unique(data['unique_id']))

	async def _bind_account(self, data: dict) -> str:
		return json.dumps(await self.am.bind_account(data['unique_id'], data['password'], data['account'], data['email'], data['phone_number']))

	async def _level_up_skill(self, data: dict) -> str:
		return json.dumps(await self.gm.level_up_skill(data['world'], data['unique_id'], data['skill_id'], data['scroll_id']))

	async def _get_all_skill_level(self, data: dict) -> str:
		return json.dumps(await self.gm.get_all_skill_level(data['world'], data['unique_id']))

	async def _get_all_supplies(self, data: dict) -> str:
		return json.dumps(await self.gm.get_all_supplies(data['world'], data['unique_id']))

	async def _get_skill(self, data: dict) -> str:
		return json.dumps(await self.gm.get_skill(data['world'], data['unique_id'], data['skill_id']))

	async def _level_up_scroll(self, data: dict) -> str:
		return json.dumps(await self.gm.level_up_scroll(data['world'], data['unique_id'], data['scroll_id']))
	# region _01_Manager_Weapon.py
	async def _level_up_weapon(self, data: dict) -> str:
		return json.dumps(await self.gm.level_up_weapon(data['world'], data['unique_id'], data['weapon'], data['iron']))

	async def _level_up_passive(self, data: dict) -> str:
		return json.dumps(await self.gm.level_up_passive(data['world'], data['unique_id'], data['weapon'], data['passive']))

	async def _reset_weapon_skill_point(self, data: dict) -> str:
		return json.dumps(await self.gm.reset_weapon_skill_point(data['world'], data['unique_id'], data['weapon']))

	async def _level_up_weapon_star(self, data: dict) -> str:
		return json.dumps(await self.gm.level_up_weapon_star(data['world'], data['unique_id'], data['weapon']))

	async def _get_all_weapon(self, data: dict) -> str:
		return json.dumps(await self.gm.get_all_weapon(data['world'], data['unique_id']))

	async def _disintegrate_weapon(self, data: dict) -> str:
		return json.dumps(await self.gm.disintegrate_weapon(data['world'], data['unique_id'], data['weapon']))
	# endregion

	async def _enter_tower(self, data: dict) -> str:
		return json.dumps(await self.gm.enter_tower(data['world'], data['unique_id'], data['stage']))

	async def _pass_tower(self, data: dict) -> str:
		return json.dumps(await self.gm.pass_tower(data['world'], data['unique_id'], data['stage'], data['clear_time']))

	async def _get_all_stage_info(self, data: dict) -> str:
		return json.dumps(await self.gm.get_all_stage_info())

	async def _get_all_armor_info(self, data: dict) -> str:
		return json.dumps(await self.gm.get_all_armor_info(data['world'], data['unique_id']))

	async def _pass_stage(self, data: dict) -> str:
		return json.dumps(await self.gm.pass_stage(data['world'], data['unique_id'], data['stage'], data['clear_time']))

	# 以后会删除这个方法
	async def _add_supplies(self, data: dict) -> str:
		return json.dumps(await self.gm.add_supplies(data['world'], data['unique_id'], data['supply'], data['value']))

	async def _get_all_head(self, data: dict) -> str:
		return json.dumps(await self.gm.get_all_head(data['world'], data['table']))

	async def _get_all_material(self, data: dict) -> str:
		return json.dumps(await self.gm.get_all_material(data['world'], data['unique_id']))

	async def _try_coin(self, data: dict) -> str:
		return json.dumps(await self.gm.try_coin(data['world'], data['unique_id'], data['value']))

	async def _try_unlock_skill(self, data: dict) -> str:
		return json.dumps(await self.gm.try_unlock_skill(data['world'], data['unique_id'], data['skill_id']))

	async def _try_unlock_weapon(self, data: dict) -> str:
		return json.dumps(await self.gm.try_unlock_weapon(data['world'], data['unique_id'], data['weapon']))

	async def _basic_summon(self, data: dict) -> str:
		return json.dumps(await self.gm.basic_summon(data['world'], data['unique_id'], data['cost_item'], 'weapons'))

	async def _pro_summon(self, data: dict) -> str:
		return json.dumps(await self.gm.pro_summon(data['world'], data['unique_id'], data['cost_item'], 'weapons'))

	async def _friend_summon(self, data: dict) -> str:
		return json.dumps(await self.gm.friend_summon(data['world'], data['unique_id'], data['cost_item'], 'weapons'))

	async def _basic_summon_10_times(self, data: dict) -> str:
		return json.dumps(await self.gm.basic_summon_10_times(data['world'], data['unique_id'], data['cost_item'], 'weapons'))

	async def _pro_summon_10_times(self, data: dict) -> str:
		return json.dumps(await self.gm.pro_summon_10_times(data['world'], data['unique_id'], data['cost_item'], 'weapons'))

	async def _friend_summon_10_times(self, data: dict) -> str:
		return json.dumps(await self.gm.friend_summon_10_times(data['world'], data['unique_id'], data['cost_item'], 'weapons'))

	async def _basic_summon_roles(self, data: dict) -> str:
		return json.dumps(await self.gm.basic_summon_roles(data['world'], data['unique_id'], data['cost_item'], 'roles'))

	async def _pro_summon_roles(self, data: dict) -> str:
		return json.dumps(await self.gm.pro_summon_roles(data['world'], data['unique_id'], data['cost_item'], 'roles'))

	async def _friend_summon_roles(self, data: dict) -> str:
		return json.dumps(await self.gm.friend_summon_roles(data['world'], data['unique_id'], data['cost_item'], 'roles'))

	async def _basic_summon_roles_10_times(self, data: dict) -> str:
		return json.dumps(await self.gm.basic_summon_10_times(data['world'], data['unique_id'], data['cost_item'], 'roles'))

	async def _pro_summon_roles_10_times(self, data: dict) -> str:
		return json.dumps(await self.gm.pro_summon_10_times(data['world'], data['unique_id'], data['cost_item'], 'roles'))

	async def _friend_summon_roles_10_times(self, data: dict) -> str:
		return json.dumps(await self.gm.friend_summon_10_times(data['world'], data['unique_id'], data['cost_item'], 'roles'))

	async def _basic_summon_skill(self, data: dict) -> str:
		return json.dumps(await self.gm.basic_summon_skill(data['world'], data['unique_id'], data['cost_item'], 'skills'))

	async def _pro_summon_skill(self, data: dict) -> str:
		return json.dumps(await self.gm.pro_summon_skill(data['world'], data['unique_id'], data['cost_item'], 'skills'))

	async def _friend_summon_skill(self, data: dict) -> str:
		return json.dumps(await self.gm.friend_summon_skill(data['world'], data['unique_id'], data['cost_item'], 'skills'))

	async def _basic_summon_skill_10_times(self, data: dict) -> str:
		return json.dumps(await self.gm.basic_summon_10_times(data['world'], data['unique_id'], data['cost_item'], 'skills'))

	async def _pro_summon_skill_10_times(self, data: dict) -> str:
		return json.dumps(await self.gm.pro_summon_10_times(data['world'], data['unique_id'], data['cost_item'], 'skills'))

	async def _friend_summon_skill_10_times(self, data: dict) -> str:
		return json.dumps(await self.gm.friend_summon_10_times(data['world'], data['unique_id'], data['cost_item'], 'skills'))

	async def _prophet_summon_10_times(self, data: dict) -> str:
		return json.dumps(await self.gm.prophet_summon_10_times(data['world'], data['unique_id'], data['cost_item'], 'weapons'))

	async def _start_hang_up(self, data: dict) -> str:
		return json.dumps(await self.gm.start_hang_up(data['world'], data['unique_id'], data['stage']))

	async def _get_hang_up_info(self, data: dict) -> str:
		return json.dumps(await self.gm.get_hang_up_info(data['world'], data['unique_id']))

	async def _enter_stage(self, data: dict) -> str:
		return json.dumps(await self.gm.enter_stage(data['world'], data['unique_id'], data['stage']))

	async def _fortune_wheel_basic(self, data: dict) -> str:
		return json.dumps(await self.gm.fortune_wheel_basic(data['world'], data['unique_id'], data['cost_item']))

	async def _fortune_wheel_pro(self, data: dict) -> str:
		return json.dumps(await self.gm.fortune_wheel_pro(data['world'], data['unique_id'], data['cost_item']))

	async def _automatically_refresh_store(self, data: dict) -> str:
		return json.dumps(await self.gm.automatically_refresh_store(data['world'], data['unique_id']))

	async def _manually_refresh_store(self, data: dict) -> str:
		return json.dumps(await self.gm.manually_refresh_store(data['world'], data['unique_id']))

	async def _diamond_refresh_store(self, data: dict) -> str:
		return json.dumps(await self.gm.diamond_refresh_store(data['world'], data['unique_id']))

	async def _black_market_transaction(self, data: dict) -> str:
		return json.dumps(await self.gm.diamond_refresh_store(data['world'], data['unique_id'], data['code']))

	async def _show_energy(self, data: dict) -> str:
		return json.dumps(await self.gm.show_energy(data['world'], data['unique_id']))

	async def _upgrade_armor(self, data: dict) -> str:
		return json.dumps(await self.gm.upgrade_armor(data['world'], data['unique_id'], data['armor_id'], data['level']))

	async def _send_friend_gift(self, data: dict) -> str:
		return json.dumps(await self.gm.send_friend_gift(data['world'], data['unique_id'], data['friend_name']))

	async def _redeem_nonce(self, data: dict) -> str:
		return json.dumps(await self.gm.redeem_nonce(data['world'], data['unique_id'], data['nonce']))

	async def _level_enemy_layouts_config(self, data: dict) -> str:
		return json.dumps(await self.gm.level_enemy_layouts_config(data['world'], data['unique_id']))

	async def _monster_config(self, data: dict) -> str:
		return json.dumps(await self.gm.monster_config(data['world'], data['unique_id']))

	async def _get_stage_reward_config(self, data: dict) -> str:
		return json.dumps(await self.gm.get_stage_reward_config(data['world'], data['unique_id']))

	async def _get_lottery_config_info(self, data: dict) -> str:
		return json.dumps(await self.gm.get_lottery_config_info(data['world'], data['unique_id']))

	async def _get_hang_up_info(self, data: dict) -> str:
		return json.dumps(await self.gm.get_hang_up_info(data['world'], data['unique_id']))

	async def _get_hang_up_reward(self, data: dict) -> str:
		return json.dumps(await self.gm.get_hang_up_reward(data['world'], data['unique_id']))

	async def _get_all_friend_info(self, data: dict) -> str:
		return json.dumps(await self.gm.get_all_friend_info(data['world'], data['unique_id']))

	async def _request_friend(self, data: dict) -> str:
		return json.dumps(await self.gm.request_friend(data['world'], data['unique_id'], data['friend_name']))

	async def _response_friend(self, data: dict) -> str:
		return json.dumps(await self.gm.response_friend(data['world'], data['unique_id'], data['nonce']))

	async def _delete_friend(self, data: dict) -> str:
		return json.dumps(await self.gm.delete_friend(data['world'], data['unique_id'], data['friend_name']))
	async def _send_all_friend_gift(self, data: dict) -> str:
		return json.dumps(await self.gm.send_all_friend_gift(data['world'], data['unique_id']))

	async def _check_boss_status(self, data: dict) -> str:
		return json.dumps(await self.gm._check_boss_status(data['world'], data['unique_id']))

	async def _enter_world_boss_stage(self, data: dict) -> str:
		return json.dumps(await self.gm._enter_world_boss_stage(data['world'], data['unique_id']))

	async def _leave_world_boss_stage(self, data: dict) -> str:
		return json.dumps(await self.gm._leave_world_boss_stage(data['world'], data['unique_id'], data['total_damage']))

	async def _get_top_damage(self, data: dict) -> str:
		return json.dumps(await self.gm._get_top_damage(data['world'], data['unique_id'], data['range_number']))

	async def _leave_family(self, data: dict) -> str:
		return json.dumps(await self.gm.leave_family(data['world'], data['unique_id']))

	async def _create_family(self, data: dict) -> str:
		return json.dumps(await self.gm.create_family(data['world'], data['unique_id'], data['fname']))

	async def _invite_user_family(self, data: dict) -> str:
		return json.dumps(await self.gm.invite_user_family(data['world'], data['unique_id'], data['target']))

	async def _remove_user_family(self, data: dict) -> str:
		return json.dumps(await self.gm.remove_user_family(data['world'], data['unique_id'], data['user']))

	async def _request_join_family(self, data: dict) -> str:
		return json.dumps(await self.gm.request_join_family(data['world'], data['unique_id'], data['fname']))

	async def _respond_family(self, data: dict) -> str:
		return json.dumps(await self.gm.respond_family(data['world'], data['unique_id'], data['nonce']))


	async def _buy_workers(self, data: dict) -> str:
		return json.dumps(await self.gm.buy_workers(data['world'], data['unique_id'], data['workers_quantity']))

	async def _refresh_all_storage(self, data: dict) -> str:
		return json.dumps(await self.gm.refresh_all_storage(data['world'], data['unique_id']))

	async def _upgrade_food_factory(self, data: dict) -> str:
		return json.dumps(await self.gm.upgrade_food_factory(data['world'], data['unique_id']))

	async def _upgrade_crystal_factory(self, data: dict) -> str:
		return json.dumps(await self.gm.upgrade_crystal_factory(data['world'], data['unique_id']))

	async def _upgrade_mine_factory(self, data: dict) -> str:
		return json.dumps(await self.gm.upgrade_mine_factory(data['world'], data['unique_id']))

	async def _upgrade_wishing_pool(self, data: dict) -> str:
		return json.dumps(await self.gm.upgrade_wishing_pool(data['world'], data['unique_id']))

	async def _equipment_manufacturing_armor(self, data: dict) -> str:
		return json.dumps(await self.gm.equipment_manufacturing_armor(data['world'], data['unique_id'], data['armor_kind']))

	async def _active_wishing_pool(self, data: dict) -> str:
		return json.dumps(await self.gm._active_wishing_pool(data['world'], data['unique_id'], data['weapon_id']))

	async def _distribution_workers(self, data: dict) -> str:
		return json.dumps(await self.gm.distribution_workers(data['world'], data['unique_id'], data['workers_quantity'], data['factory_kind']))
###############################################################################



DOES_NOT_NEED_TOKEN = {'login', 'login_unique'}

FUNCTION_LIST = {
	# account_manager
	'login': MessageHandler._login,
	'login_unique': MessageHandler._login_unique,
	'bind_account': MessageHandler._bind_account,

	# game_manager
	'get_all_head' : MessageHandler._get_all_head,
	'get_all_material' : MessageHandler._get_all_material,
	'get_all_supplies' : MessageHandler._get_all_supplies,
	'add_supplies' : MessageHandler._add_supplies,
	'level_up_scroll' : MessageHandler._level_up_scroll,
	'try_coin' : MessageHandler._try_coin,
	'level_up_skill' : MessageHandler._level_up_skill,
	'get_all_skill_level' : MessageHandler._get_all_skill_level,
	'get_skill' : MessageHandler._get_skill,
	'try_unlock_skill' : MessageHandler._try_unlock_skill,
	'level_up_weapon' : MessageHandler._level_up_weapon,
	'level_up_passive' : MessageHandler._level_up_passive,
	'level_up_weapon_star' : MessageHandler._level_up_weapon_star,
	'reset_weapon_skill_point' : MessageHandler._reset_weapon_skill_point,
	'get_all_weapon' : MessageHandler._get_all_weapon,
	'disintegrate_weapon' : MessageHandler._disintegrate_weapon,
	'try_unlock_weapon' : MessageHandler._try_unlock_weapon,
	'pass_stage' : MessageHandler._pass_stage,
	'basic_summon' : MessageHandler._basic_summon,
	'basic_summon_10_times' : MessageHandler._basic_summon_10_times,
	'pro_summon' : MessageHandler._pro_summon,
	'pro_summon_10_times' : MessageHandler._pro_summon_10_times,
	'friend_summon' : MessageHandler._friend_summon,
	'friend_summon_10_times' : MessageHandler._friend_summon_10_times,
	'basic_summon_roles' : MessageHandler._basic_summon_roles,
	'basic_summon_roles_10_times' : MessageHandler._basic_summon_roles_10_times,
	'pro_summon_roles' : MessageHandler._pro_summon_roles,
	'pro_summon_roles_10_times' : MessageHandler._pro_summon_roles_10_times,
	'friend_summon_roles' : MessageHandler._friend_summon_roles,
	'friend_summon_roles_10_times' : MessageHandler._friend_summon_roles_10_times,


	'basic_summon_skill' : MessageHandler._basic_summon_skill,
	'basic_summon_skill_10_times' : MessageHandler._basic_summon_skill_10_times,
	'pro_summon_skill' : MessageHandler._pro_summon_skill,
	'pro_summon_skill_10_times' : MessageHandler._pro_summon_skill_10_times,
	'friend_summon_skill' : MessageHandler._friend_summon_skill,
	'friend_summon_skill_10_times' : MessageHandler._friend_summon_skill_10_times,
	'prophet_summon_10_times' : MessageHandler._prophet_summon_10_times,



	'start_hang_up' : MessageHandler._start_hang_up,
	'get_hang_up_reward' : MessageHandler._get_hang_up_reward,
	'enter_stage' : MessageHandler._enter_stage,
	'fortune_wheel_basic' : MessageHandler._fortune_wheel_basic,
	'fortune_wheel_pro' : MessageHandler._fortune_wheel_pro,

	'automatically_refresh_store': MessageHandler._automatically_refresh_store,
	'manually_refresh_store': MessageHandler._manually_refresh_store,
	'diamond_refresh_store': MessageHandler._diamond_refresh_store,
	'black_market_transaction': MessageHandler._black_market_transaction,
	'show_energy': MessageHandler._show_energy,
	'upgrade_armor': MessageHandler._upgrade_armor,
	'pass_tower' : MessageHandler._pass_tower,
	'enter_tower' : MessageHandler._enter_tower,
	'get_all_stage_info' : MessageHandler._get_all_stage_info,
	'get_all_armor_info' : MessageHandler._get_all_armor_info,


	'get_lottery_config_info' : MessageHandler._get_lottery_config_info,
	#'get_all_tower_info' : MessageHandler._get_all_tower_info,
	#'get_all_armor_info' : MessageHandler._get_all_armor_info,
	'level_enemy_layouts_config' : MessageHandler._level_enemy_layouts_config,
	'monster_config' : MessageHandler._monster_config,
	'get_stage_reward_config' : MessageHandler._get_stage_reward_config,
	'get_hang_up_info' : MessageHandler._get_hang_up_info,


	'get_all_friend_info': MessageHandler._get_all_friend_info,
	'delete_friend': MessageHandler._delete_friend,
	'request_friend': MessageHandler._request_friend,
	'response_friend': MessageHandler._response_friend,
	'send_friend_gift': MessageHandler._send_friend_gift,
	'send_all_friend_gift': MessageHandler._send_all_friend_gift,
	'redeem_nonce': MessageHandler._redeem_nonce,


	'check_boss_status' : MessageHandler._check_boss_status,
	'enter_world_boss_stage' : MessageHandler._enter_world_boss_stage,
	'leave_world_boss_stage' : MessageHandler._leave_world_boss_stage,
	'get_top_damage' : MessageHandler._get_top_damage,

	'leave_family' : MessageHandler._leave_family,
	'create_family' : MessageHandler._create_family,
	'invite_user_family' : MessageHandler._invite_user_family,
	'remove_user_family' : MessageHandler._remove_user_family,
	'request_join_family' : MessageHandler._request_join_family,
	'respond_family' : MessageHandler._respond_family,

	'refresh_all_storage' : MessageHandler._refresh_all_storage,
	'buy_workers' : MessageHandler._buy_workers,
	'upgrade_food_factory' : MessageHandler._upgrade_food_factory,
	'upgrade_crystal_factory' : MessageHandler._upgrade_crystal_factory,
	'upgrade_mine_factory' : MessageHandler._upgrade_mine_factory,
	'upgrade_wishing_pool' : MessageHandler._upgrade_wishing_pool,
	'distribution_workers':MessageHandler._distribution_workers,
	'equipment_manufacturing_armor':MessageHandler._equipment_manufacturing_armor,
	'active_wishing_pool':MessageHandler._active_wishing_pool
}

