import json
import account_manager
import game_manager

from utility import config_reader

CFG = config_reader.wait_config()

TOKEN_BASE_URL = CFG['token_server']['addr'] + ':' + CFG['token_server']['port']
MAIL_BASE_URL = CFG['mail_server']['addr'] + ':' + CFG['mail_server']['port']

class InvalidTokenError(Exception):
	pass

class MessageHandler:
	def __init__(self):
		self._functions = FUNCTION_LIST
		self.am = account_manager.AccountManager()
		self.gm = game_manager.GameManager()

	async def shutdown(self):
		if self.am._pool:
			self.am._pool.close()
			await self.am._pool.wait_closed()

	# json.decoder.JSONDecodeError
	async def resolve(self, message: str, session) -> str:
		'''
		Resolves the message included in the request. If required, ensures that a valid token is present.
		'''
		try:
			message = json.loads(message)
			try:
				fn = self._functions[message['function']]
			except KeyError:
				return '{"status" : 10, "message" : "function is not in function list"}'
			if message['function'] not in DOES_NOT_NEED_TOKEN:
				try:
					message['data']['unique_id'] = await self.validate_token(message['data']['token'], session)
				except KeyError:
					return '{"status" : 10, "message" : "missing required token"}'
			message['session'] = session
			return await fn(self, message)
		except InvalidTokenError:
			return '{"status" : 11, "message" : "unauthorized. invalid token."}'



	async def validate_token(self, token, session):
		async with session.post(TOKEN_BASE_URL + '/validate', data = {'token' : token}) as r:
			validated = await r.json(content_type = 'text/json')
			if validated['status'] != 0:
				raise InvalidTokenError
			return validated['data']['unique_id']

	async def _login(self, data: dict) -> str:
		return json.dumps(await self.am.login(data['data']['identifier'], data['data']['value'], data['data']['password']))

	async def _login_unique(self, data: dict) -> str:
		return json.dumps(await self.am.login_unique(data['data']['unique_id']))

	async def _bind_account(self, data: dict) -> str:
		return json.dumps(await self.am.bind_account(data['data']['unique_id'], data['data']['password'], data['data']['account'], data['data']['email'], data['data']['phone_number']))

	async def _level_up_skill(self, data: dict) -> str:
		return json.dumps(await self.gm.level_up_skill(data['world'], data['data']['unique_id'], data['data']['skill_id'], data['data']['scroll_id']))

	async def _get_all_skill_level(self, data: dict) -> str:
		return json.dumps(await self.gm.get_all_skill_level(data['world'], data['data']['unique_id']))

	async def _get_all_supplies(self, data: dict) -> str:
		return json.dumps(await self.gm.get_all_supplies(data['world'], data['data']['unique_id']))

	async def _get_skill(self, data: dict) -> str:
		return json.dumps(await self.gm.get_skill(data['world'], data['data']['unique_id'], data['data']['skill_id']))

	async def _level_up_scroll(self, data: dict) -> str:
		return json.dumps(await self.gm.level_up_scroll(data['world'], data['data']['unique_id'], data['data']['scroll_id']))
	# region _01_Manager_Weapon.py
	async def _level_up_weapon(self, data: dict) -> str:
		return json.dumps(await self.gm.level_up_weapon(data['world'], data['data']['unique_id'], data['data']['weapon'], data['data']['iron']))

	async def _level_up_passive(self, data: dict) -> str:
		return json.dumps(await self.gm.level_up_passive(data['world'], data['data']['unique_id'], data['data']['weapon'], data['data']['passive']))

	async def _reset_weapon_skill_point(self, data: dict) -> str:
		return json.dumps(await self.gm.reset_weapon_skill_point(data['world'], data['data']['unique_id'], data['data']['weapon']))

	async def _level_up_weapon_star(self, data: dict) -> str:
		return json.dumps(await self.gm.level_up_weapon_star(data['world'], data['data']['unique_id'], data['data']['weapon']))

	async def _get_all_weapon(self, data: dict) -> str:
		return json.dumps(await self.gm.get_all_weapon(data['world'], data['data']['unique_id']))

	async def _disintegrate_weapon(self, data: dict) -> str:
		return json.dumps(await self.gm.disintegrate_weapon(data['world'], data['data']['unique_id'], data['data']['weapon']))
	# endregion

	async def _enter_tower(self, data: dict) -> str:
		return json.dumps(await self.gm.enter_tower(data['world'], data['data']['unique_id'], data['data']['stage']))

	async def _pass_tower(self, data: dict) -> str:
		return json.dumps(await self.gm.pass_tower(data['world'], data['data']['unique_id'], data['data']['stage'], data['data']['clear_time']))

	async def _get_all_stage_info(self, data: dict) -> str:
		return json.dumps(await self.gm.get_all_stage_info())

	async def _get_all_armor_info(self, data: dict) -> str:
		return json.dumps(await self.gm.get_all_armor_info(data['world'], data['data']['unique_id']))

	async def _pass_stage(self, data: dict) -> str:
		return json.dumps(await self.gm.pass_stage(data['world'], data['data']['unique_id'], data['data']['stage'], data['data']['clear_time']))

	# 以后会删除这个方法
	async def _add_supplies(self, data: dict) -> str:
		return json.dumps(await self.gm.add_supplies(data['world'], data['data']['unique_id'], data['data']['supply'], data['data']['value']))

	async def _get_all_head(self, data: dict) -> str:
		return json.dumps(await self.gm.get_all_head(data['world'], data['data']['table']))

	async def _get_all_material(self, data: dict) -> str:
		return json.dumps(await self.gm.get_all_material(data['world'], data['data']['unique_id']))

	async def _try_coin(self, data: dict) -> str:
		return json.dumps(await self.gm.try_coin(data['world'], data['data']['unique_id'], data['data']['value']))

	async def _try_unlock_skill(self, data: dict) -> str:
		return json.dumps(await self.gm.try_unlock_skill(data['world'], data['data']['unique_id'], data['data']['skill_id']))

	async def _try_unlock_weapon(self, data: dict) -> str:
		return json.dumps(await self.gm.try_unlock_weapon(data['world'], data['data']['unique_id'], data['data']['weapon']))

	async def _basic_summon(self, data: dict) -> str:
		return json.dumps(await self.gm.basic_summon(data['world'], data['data']['unique_id'], data['data']['cost_item'], 'weapons'))

	async def _pro_summon(self, data: dict) -> str:
		return json.dumps(await self.gm.pro_summon(data['world'], data['data']['unique_id'], data['data']['cost_item'], 'weapons'))

	async def _friend_summon(self, data: dict) -> str:
		return json.dumps(await self.gm.friend_summon(data['world'], data['data']['unique_id'], data['data']['cost_item'], 'weapons'))

	async def _basic_summon_10_times(self, data: dict) -> str:
		return json.dumps(await self.gm.basic_summon_10_times(data['world'], data['data']['unique_id'], data['data']['cost_item'], 'weapons'))

	async def _pro_summon_10_times(self, data: dict) -> str:
		return json.dumps(await self.gm.pro_summon_10_times(data['world'], data['data']['unique_id'], data['data']['cost_item'], 'weapons'))

	async def _friend_summon_10_times(self, data: dict) -> str:
		return json.dumps(await self.gm.friend_summon_10_times(data['world'], data['data']['unique_id'], data['data']['cost_item'], 'weapons'))

	async def _basic_summon_roles(self, data: dict) -> str:
		return json.dumps(await self.gm.basic_summon(data['world'], data['data']['unique_id'], data['data']['cost_item'], 'roles'))

	async def _pro_summon_roles(self, data: dict) -> str:
		return json.dumps(await self.gm.pro_summon(data['world'], data['data']['unique_id'], data['data']['cost_item'], 'roles'))

	async def _friend_summon_roles(self, data: dict) -> str:
		return json.dumps(await self.gm.friend_summon(data['world'], data['data']['unique_id'], data['data']['cost_item'], 'roles'))

	async def _basic_summon_roles_10_times(self, data: dict) -> str:
		return json.dumps(await self.gm.basic_summon_10_times(data['world'], data['data']['unique_id'], data['data']['cost_item'], 'roles'))

	async def _pro_summon_roles_10_times(self, data: dict) -> str:
		return json.dumps(await self.gm.pro_summon_10_times(data['world'], data['data']['unique_id'], data['data']['cost_item'], 'roles'))

	async def _friend_summon_roles_10_times(self, data: dict) -> str:
		return json.dumps(await self.gm.friend_summon_10_times(data['world'], data['data']['unique_id'], data['data']['cost_item'], 'roles'))

	async def _basic_summon_skill(self, data: dict) -> str:
		return json.dumps(await self.gm.basic_summon(data['world'], data['data']['unique_id'], data['data']['cost_item'], 'skills'))

	async def _pro_summon_skill(self, data: dict) -> str:
		return json.dumps(await self.gm.pro_summon(data['world'], data['data']['unique_id'], data['data']['cost_item'], 'skills'))

	async def _friend_summon_skill(self, data: dict) -> str:
		return json.dumps(await self.gm.friend_summon(data['world'], data['data']['unique_id'], data['data']['cost_item'], 'skills'))

	async def _basic_summon_skill_10_times(self, data: dict) -> str:
		return json.dumps(await self.gm.basic_summon_10_times(data['world'], data['data']['unique_id'], data['data']['cost_item'], 'skills'))

	async def _pro_summon_skill_10_times(self, data: dict) -> str:
		return json.dumps(await self.gm.pro_summon_10_times(data['world'], data['data']['unique_id'], data['data']['cost_item'], 'skills'))

	async def _friend_summon_skill_10_times(self, data: dict) -> str:
		return json.dumps(await self.gm.friend_summon_10_times(data['world'], data['data']['unique_id'], data['data']['cost_item'], 'skills'))

	async def _prophet_summon_10_times(self, data: dict) -> str:
		return json.dumps(await self.gm.prophet_summon_10_times(data['world'], data['data']['unique_id'], data['data']['cost_item'], 'weapons'))

	async def _start_hang_up(self, data: dict) -> str:
		return json.dumps(await self.gm.start_hang_up(data['world'], data['data']['unique_id'], data['data']['stage']))

	async def _enter_stage(self, data: dict) -> str:
		return json.dumps(await self.gm.enter_stage(data['world'], data['data']['unique_id'], data['data']['stage']))

	async def _fortune_wheel_basic(self, data: dict) -> str:
		return json.dumps(await self.gm.fortune_wheel_basic(data['world'], data['data']['unique_id'], data['data']['cost_item']))

	async def _fortune_wheel_pro(self, data: dict) -> str:
		return json.dumps(await self.gm.fortune_wheel_pro(data['world'], data['data']['unique_id'], data['data']['cost_item']))

	async def _automatically_refresh_store(self, data: dict) -> str:
		return json.dumps(await self.gm.automatically_refresh_store(data['world'], data['data']['unique_id']))

	async def _manually_refresh_store(self, data: dict) -> str:
		return json.dumps(await self.gm.manually_refresh_store(data['world'], data['data']['unique_id']))

	async def _diamond_refresh_store(self, data: dict) -> str:
		return json.dumps(await self.gm.diamond_refresh_store(data['world'], data['data']['unique_id']))

	async def _black_market_transaction(self, data: dict) -> str:
		return json.dumps(await self.gm.black_market_transaction(data['world'], data['data']['unique_id'], data['data']['code']))

	async def _show_energy(self, data: dict) -> str:
		return json.dumps(await self.gm.show_energy(data['world'], data['data']['unique_id']))

	async def _upgrade_armor(self, data: dict) -> str:
		return json.dumps(await self.gm.upgrade_armor(data['world'], data['data']['unique_id'], data['data']['armor_id'], data['data']['level']))

	async def _send_friend_gift(self, data: dict) -> str:
		return json.dumps(await self.gm.send_friend_gift(data['world'], data['data']['unique_id'], data['data']['friend_name']))

	async def _redeem_nonce(self, data: dict) -> str:
		return json.dumps(await self.gm.redeem_nonce(data['world'], data['data']['unique_id'], data['data']['nonce']))

	async def _send_merchandise(self, data: dict) -> str:
		return json.dumps(await self.gm.send_merchandise(data['world'], data['data']['unique_id'], data['data']['merchandise'], data['data']['quantities']))

	async def _level_enemy_layouts_config(self, data: dict) -> str:
		return json.dumps(await self.gm.level_enemy_layouts_config(data['world'], data['data']['unique_id']))

	async def _monster_config(self, data: dict) -> str:
		return json.dumps(await self.gm.monster_config(data['world'], data['data']['unique_id']))

	async def _get_stage_reward_config(self, data: dict) -> str:
		return json.dumps(await self.gm.get_stage_reward_config())

	async def _get_hang_up_info(self, data: dict) -> str:
		return json.dumps(await self.gm.get_hang_up_info(data['world'], data['data']['unique_id']))

	async def _get_hang_up_reward(self, data: dict) -> str:
		return json.dumps(await self.gm.get_hang_up_reward(data['world'], data['data']['unique_id']))

	async def _get_all_friend_info(self, data: dict) -> str:
		return json.dumps(await self.gm.get_all_friend_info(data['world'], data['data']['unique_id']))

	async def _request_friend(self, data: dict) -> str:
		return json.dumps(await self.gm.request_friend(data['world'], data['data']['unique_id'], data['data']['friend_name']))

	async def _response_friend(self, data: dict) -> str:
		return json.dumps(await self.gm.response_friend(data['world'], data['data']['unique_id'], data['data']['nonce']))

	async def _delete_friend(self, data: dict) -> str:
		return json.dumps(await self.gm.delete_friend(data['world'], data['data']['unique_id'], data['data']['friend_name']))
	async def _send_all_friend_gift(self, data: dict) -> str:
		return json.dumps(await self.gm.send_all_friend_gift(data['world'], data['data']['unique_id']))

	async def _check_boss_status(self, data: dict) -> str:
		return json.dumps(await self.gm._check_boss_status(data['world'], data['data']['unique_id']))

	async def _enter_world_boss_stage(self, data: dict) -> str:
		return json.dumps(await self.gm._enter_world_boss_stage(data['world'], data['data']['unique_id']))

	async def _leave_world_boss_stage(self, data: dict) -> str:
		return json.dumps(await self.gm._leave_world_boss_stage(data['world'], data['data']['unique_id'], data['data']['total_damage']))

	async def _get_top_damage(self, data: dict) -> str:
		return json.dumps(await self.gm._get_top_damage(data['world'], data['data']['unique_id'], data['data']['range_number']))

	async def _leave_family(self, data: dict) -> str:
		return json.dumps(await self.gm.leave_family(data['world'], data['data']['unique_id']))

	async def _create_family(self, data: dict) -> str:
		return json.dumps(await self.gm.create_family(data['world'], data['data']['unique_id'], data['data']['fname']))

	async def _invite_user_family(self, data: dict) -> str:
		return json.dumps(await self.gm.invite_user_family(data['world'], data['data']['unique_id'], data['data']['target']))

	async def _remove_user_family(self, data: dict) -> str:
		return json.dumps(await self.gm.remove_user_family(data['world'], data['data']['unique_id'], data['data']['user']))

	async def _request_join_family(self, data: dict) -> str:
		return json.dumps(await self.gm.request_join_family(data['world'], data['data']['unique_id'], data['data']['fname']))

	async def _respond_family(self, data: dict) -> str:
		return json.dumps(await self.gm.respond_family(data['world'], data['data']['unique_id'], data['data']['nonce']))


	async def _buy_workers(self, data: dict) -> str:
		return json.dumps(await self.gm.buy_workers(data['world'], data['data']['unique_id'], data['data']['workers_quantity']))

	async def _refresh_all_storage(self, data: dict) -> str:
		return json.dumps(await self.gm.refresh_all_storage(data['world'], data['data']['unique_id']))

	async def _upgrade_food_factory(self, data: dict) -> str:
		return json.dumps(await self.gm.upgrade_food_factory(data['world'], data['data']['unique_id']))

	async def _upgrade_crystal_factory(self, data: dict) -> str:
		return json.dumps(await self.gm.upgrade_crystal_factory(data['world'], data['data']['unique_id']))

	async def _upgrade_mine_factory(self, data: dict) -> str:
		return json.dumps(await self.gm.upgrade_mine_factory(data['world'], data['data']['unique_id']))

	async def _upgrade_wishing_pool(self, data: dict) -> str:
		return json.dumps(await self.gm.upgrade_wishing_pool(data['world'], data['data']['unique_id']))

	async def _equipment_manufacturing_armor(self, data: dict) -> str:
		return json.dumps(await self.gm.equipment_manufacturing_armor(data['world'], data['data']['unique_id'], data['data']['armor_kind']))

	async def _active_wishing_pool(self, data: dict) -> str:
		return json.dumps(await self.gm._active_wishing_pool(data['world'], data['data']['unique_id'], data['data']['weapon_id']))

	async def _distribution_workers(self, data: dict) -> str:
		return json.dumps(await self.gm.distribution_workers(data['world'], data['data']['unique_id'], data['data']['workers_quantity'], data['data']['factory_kind']))


	async def _get_account_world_info(self, data: dict) -> str:
		return json.dumps(await self.gm.get_account_world_info(data['data']['unique_id']))

	# not designed yet
	# async def _get_chat_server(self, data: dict):
	# 	return self._map[data['world']]['chatserver']

	async def _choice_world(self, data: dict) -> str:
		return json.dumps(await self.gm.choice_world(data['data']['unique_id'], data['data']['target_world']))

	async def _create_player(self, data: dict) -> str:
		return json.dumps(await self.gm.create_player(data['world'], data['data']['unique_id'], data['data']['game_name']))
	#not sure where to use them
	# async def _join_world(self, data: dict) -> str:
	# 	return json.dumps(await self.gm.join_world(data['world'], data['data']['unique_id'], data['data']['game_name']))

	# async def _bind_gamename(self, data: dict) -> str:
	# 	return json.dumps(await self.gm.bind_gamename(data['world'], data['data']['unique_id'], data['data']['game_name']))

	# async def _try_all_material(self, data: dict) -> str:
	# 	return json.dumps(await self.gm.try_all_material(data['world'], data['data']['unique_id'], data['data']['stage']))

	async def _get_stage_info(self,data:dict) -> str:
		return json.dumps(self.gm.get_stage_info())

	async def _get_monster_info(self,data:dict) -> str:
		return json.dumps(self.gm.get_monster_info())

	async def _get_all_roles(self, data: dict) -> str:
		return json.dumps(await self.gm.get_all_roles(data['world'], data['data']['unique_id']))

	async def _get_factory_info(self, data: dict) -> str:
		return json.dumps(await self.gm.get_factory_info(data['world'], data['data']['unique_id']))
	#未完成
	# async def _get_all_family_info(self, data: dict) -> str:
	# 	return json.dumps(await self.gm.get_all_family_info(data['world'], data['data']['unique_id']))

	#未完成
	async def _get_all_mail(self, data: dict) -> str:
		async with data['session'].post(MAIL_BASE_URL + '/get_all_mail', data = {'world' : data['world'], 'unique_id' : data['data']['unique_id']}) as r:
			return await r.text()

	async def _get_lottery_config_info(self, data: dict) -> str:
		return json.dumps(await self.gm.get_lottery_config_info())
	#未完成
	# async def _player_config(self, data: dict) -> str:
	# 	return json.dumps(await self.gm.player_config())

	async def _get_weapon_config(self, data: dict) -> str:
		return json.dumps(await self.gm.get_weapon_config())

	async def _get_skill_level_up_config(self, data: dict) -> str:
		return json.dumps(await self.gm.get_skill_level_up_config())

	#未完成
	# async def _get_family_config(self) -> str:
	# 	return json.dumps(await self.gm.get_family_config())

	async def _get_role_config(self, data: dict) -> str:
		return json.dumps(await self.gm.get_role_config())

	async def _redeem_all_nonce(self, data: dict) -> str:
		return json.dumps(await self.gm.redeem_all_nonce(data['world'], data['data']['unique_id'],data['data']['type_list'],data['data']['nonce_list']))

	#未完成 邮件为不同系统
	async def _get_new_mail(self, data: dict) -> str:
		async with data['session'].post(MAIL_BASE_URL + '/get_new_mail', data = {'world' : data['world'], 'unique_id' : data['data']['unique_id']}) as r:
			return await r.text()
	# 	return json.dumps(await self.gm.get_new_mail(data['world'], data['data']['unique_id']))
	async def _delete_mail(self, data: dict) -> str:
		async with data['session'].post(MAIL_BASE_URL + '/delete_mail', data = {'world' : data['world'], 'unique_id' : data['data']['unique_id'], 'key' : data['data']['key']}) as r:
			return await r.text()
	# 	return json.dumps(await self.gm.delete_mail(data['world'], data['data']['unique_id'],data['data']['nonce']))
	# async def _delete_all_mail(self, data: dict) -> str:
	# 	return json.dumps(await self.gm.delete_all_mail(data['world'], data['data']['unique_id']))

	async def _acceleration_technology(self, data: dict) -> str:
		return json.dumps(await self.gm.acceleration_technology(data['world'], data['data']['unique_id']))

	async def _refresh_food_storage(self, data: dict) -> str:
		return json.dumps(await self.gm.refresh_food_storage(data['world'], data['data']['unique_id']))

	async def _refresh_mine_storage(self, data: dict) -> str:
		return json.dumps(await self.gm.refresh_mine_storage(data['world'], data['data']['unique_id']))

	async def _refresh_crystal_storage(self, data: dict) -> str:
		return json.dumps(await self.gm.refresh_crystal_storage(data['world'], data['data']['unique_id']))

	async def _refresh_equipment_storage(self, data: dict) -> str:
		return json.dumps(await self.gm.refresh_equipment_storage(data['world'], data['data']['unique_id']))

	async def _upgrade_role_level(self, data: dict) -> str:
		return json.dumps(await self.gm.upgrade_role_level(data['world'], data['data']['unique_id'],data['data']['role'],data['data']['experience_potion']))

	async def _upgrade_role_star(self, data: dict) -> str:
		return json.dumps(await self.gm.upgrade_role_star(data['world'], data['data']['unique_id'],data['data']['role']))

	async def _get_player_info(self, data: dict) -> str:
		return json.dumps(await self.gm.get_player_info())


		# async with session.post(self._game_manager_base_url("0") + '/get_account_world_info', data={'unique_id': message['data']['unique_id']}) as resp:
		# 	return await resp.text()
###############################################################################



DOES_NOT_NEED_TOKEN = {'login', 'login_unique'}

FUNCTION_LIST = {
		# utility
	# 'get_chat_server' : MessageHandler._get_chat_server,
	# account_manager
	'login': MessageHandler._login,
	'login_unique': MessageHandler._login_unique,
	'bind_account': MessageHandler._bind_account,
	'choice_world': MessageHandler._choice_world,
	'get_account_world_info': MessageHandler._get_account_world_info,
	'create_player': MessageHandler._create_player,

	# game_manager
	# 'join_world' : MessageHandler._join_world,
	# 'bind_gamename' : MessageHandler._bind_gamename,
	'get_all_head' : MessageHandler._get_all_head,
	'get_all_material' : MessageHandler._get_all_material,
	'get_all_supplies' : MessageHandler._get_all_supplies,
	'add_supplies' : MessageHandler._add_supplies,
	'level_up_scroll' : MessageHandler._level_up_scroll,
	# 'try_all_material' : MessageHandler._try_all_material,
	'try_coin' : MessageHandler._try_coin,
	'level_up_skill' : MessageHandler._level_up_skill,
	'get_all_skill_level' : MessageHandler._get_all_skill_level,
	'get_skill' : MessageHandler._get_skill,
	'try_unlock_skill' : MessageHandler._try_unlock_skill,
	'level_up_weapon' : MessageHandler._level_up_weapon,
	'level_up_passive' : MessageHandler._level_up_passive,
	'level_up_weapon_star' : MessageHandler._level_up_weapon_star,
	'reset_weapon_skill_point' : MessageHandler._reset_weapon_skill_point,
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

	#'get_level_info' : MessageHandler._get_level_info,未完成
	'get_stage_info' : MessageHandler._get_stage_info,
	'get_monster_info' : MessageHandler._get_monster_info,
	'get_all_friend_info' : MessageHandler._get_all_friend_info,
	'get_all_weapon' : MessageHandler._get_all_weapon,
	'refresh_all_storage' : MessageHandler._refresh_all_storage,
	'get_all_roles' : MessageHandler._get_all_roles,
	'get_factory_info' : MessageHandler._get_factory_info,
	# 'get_all_family_info' : MessageHandler._get_all_family_info,
	'get_all_mail' : MessageHandler._get_all_mail,
	# 'player_config' : MessageHandler._player_config,
	'get_weapon_config' : MessageHandler._get_weapon_config,
	'get_skill_level_up_config' : MessageHandler._get_skill_level_up_config,
	# 'get_family_config' : MessageHandler._get_family_config,
	'get_role_config' : MessageHandler._get_role_config,




	'get_lottery_config_info' : MessageHandler._get_lottery_config_info,
	#'get_all_tower_info' : MessageHandler._get_all_tower_info,
	'level_enemy_layouts_config' : MessageHandler._level_enemy_layouts_config,
	'monster_config' : MessageHandler._monster_config,
	'get_stage_reward_config' : MessageHandler._get_stage_reward_config,
	'get_hang_up_info' : MessageHandler._get_hang_up_info,


	'delete_friend': MessageHandler._delete_friend,
	'request_friend': MessageHandler._request_friend,
	'response_friend': MessageHandler._response_friend,
	'send_friend_gift': MessageHandler._send_friend_gift,
	'send_all_friend_gift': MessageHandler._send_all_friend_gift,
	'redeem_nonce': MessageHandler._redeem_nonce,
	'redeem_all_nonce': MessageHandler._redeem_all_nonce,
	'get_new_mail': MessageHandler._get_new_mail,
	'delete_mail': MessageHandler._delete_mail,
	# 'delete_all_mail': MessageHandler._delete_all_mail,

	'send_merchandise': MessageHandler._send_merchandise,

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

	'buy_workers' : MessageHandler._buy_workers,
	'upgrade_food_factory' : MessageHandler._upgrade_food_factory,
	'upgrade_crystal_factory' : MessageHandler._upgrade_crystal_factory,
	'upgrade_mine_factory' : MessageHandler._upgrade_mine_factory,
	'upgrade_wishing_pool' : MessageHandler._upgrade_wishing_pool,
	'distribution_workers':MessageHandler._distribution_workers,
	'equipment_manufacturing_armor':MessageHandler._equipment_manufacturing_armor,
	'active_wishing_pool':MessageHandler._active_wishing_pool,
	'acceleration_technology':MessageHandler._acceleration_technology,
	'refresh_food_storage':MessageHandler._refresh_food_storage,
	'refresh_mine_storage':MessageHandler._refresh_mine_storage,
	'refresh_crystal_storage':MessageHandler._refresh_crystal_storage,
	'refresh_equipment_storage':MessageHandler._refresh_equipment_storage,


	'upgrade_role_level':MessageHandler._upgrade_role_level,
	'upgrade_role_star':MessageHandler._upgrade_role_star,
	'get_player_info':MessageHandler._get_player_info
}

