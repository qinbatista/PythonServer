'''
message_handler.py
'''

import json
import random

from module import mail
from module import chat
from module import enums
from module import skill
from module import family
from module import factory
from module import friend
from module import common
from module import account
from module import weapon
from module import summoning
from module import achievement
from module import armor
from module import player
from module import role
from module import task
from module import stage
from module import check_in
from module import darkmarket
from module import package
from module import vip
from module import mall
from module import science



class MessageHandler:
	def __init__(self, *, token_addr, token_port, mail_addr, mail_port):
		self.functions      = FUNCTION_LIST
		self.mail_base_url  = f'http://{mail_addr}:{mail_port}'
		self.token_base_url = f'http://{token_addr}:{token_port}'

	async def shutdown(self):
		pass

	async def resolve(self, message: dict, resource, configs) -> str:
		'''
		Resolves the message included in the request. If required, ensures that a valid token is present.
		'''
		try:
			fn = self.functions[message['function']]
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
		message['malldb'] = resource['malldb']
		message['exchangedb'] = resource['exchangedb']
		message['mailserverbaseurl']  = self.mail_base_url
		message['tokenserverbaseurl'] = self.token_base_url
		message['config'] = configs  # ###########configs#################
		return json.dumps(await fn(self, message))

	async def validate_token(self, msg, session):
		async with session.post(self.token_base_url+'/validate_token', \
				data={'token' : msg['data']['token']}) as r:
			validated = await r.json()
			return (False, None) if validated['status'] != 0 else (True, validated['data']['uid'])


	###################### account.py ######################
	async def _register(self, data: dict) -> str:
		return await account.register(data['data']['unique_id'], data['data']['account'], data['data']['password'], **data)

	async def _login_unique(self, data: dict) -> str:
		return await account.login_unique(data['data']['unique_id'], **data)

	async def _login(self, data: dict) -> str:
		return await account.login(data['data']['identifier'], data['data']['value'], data['data']['password'], **data)

	async def _account_all_info(self, data: dict) -> str:
		return await account.all_info(data['data']['unique_id'], **data)

	async def _bind_account(self, data: dict) -> str:
		return await account.bind_account(data['data']['unique_id'], data['data']['account'], data['data']['password'], **data)

	async def _bind_email(self, data: dict) -> str:
		return await account.bind_email(data['data']['unique_id'], data['data']['email'], **data)

	async def _unbind_email(self, data: dict) -> str:
		return await account.unbind_email(data['data']['unique_id'], data['data']['email'], **data)

	async def _verify_email_code(self, data: dict) -> str:
		return await account.verify_email_code(data['data']['unique_id'], data['data']['code'], status=data['data'].get('status', 0), **data)

	async def _bind_phone(self, data: dict) -> str:
		return await account.bind_phone(data['data']['unique_id'], data['data']['phone_number'], **data)

	async def _unbind_phone(self, data: dict) -> str:
		return await account.unbind_phone(data['data']['unique_id'], data['data']['phone_number'], **data)

	async def _verify_phone_code(self, data: dict) -> str:
		return await account.verify_phone_code(data['data']['unique_id'], data['data']['code'], status=data['data'].get('status', 0), **data)


	async def _get_player_config(self, data: dict) -> str:
		return common.mt(0, 'success', {'player_config': data['config']['player']})

	async def _create_account(self, data: dict) -> str:
		return 'function'

	async def _change_game_name(self, data: dict) -> str:
		return 'function'


	###################### chat.py ######################
	async def _get_login_token_chat(self, data: dict) -> str:
		return await chat.get_login_token(data['data']['unique_id'], **data)


	###################### player.py ######################
	async def _create_player(self, data: dict) -> str:
		return await player.create(data['data']['unique_id'], data['data']['gn'], data['data']['icon'], **data)

	async def _change_player_name(self, data: dict) -> str:
		return await player.change_name(data['data']['unique_id'], data['data']['gn'], **data)

	async def _player_set_intro(self, data: dict) -> str:
		return await player.set_intro(data['data']['unique_id'], data['data']['intro'], **data)

	async def _player_set_icon(self, data: dict) -> str:
		return await player.set_icon(data['data']['unique_id'], data['data']['icon'], **data)

	async def _enter_world(self, data: dict) -> str:
		return await player.enter_world(data['data']['unique_id'], **data)

	async def _get_account_world_info(self, data: dict) -> str:
		return await player.get_account_world_info(data['data']['unique_id'], **data)

	async def _accept_gifts(self, data: dict) -> str:
		return await player.accept_gifts(data['data']['unique_id'], data['data']['gift'], \
				data['data']['other'], **data)

	async def _get_info_player(self, data: dict) -> str:
		return await player.get_info(data['data']['unique_id'], **data)


	###################### science.py ######################
	async def _science_infos(self, data: dict) -> str:
		return await science.infos(data['data']['unique_id'], **data)

	async def _science_up(self, data: dict) -> str:
		return await science.up(data['data']['unique_id'], int(data['data']['ssa']), **data)

	###################### family.py ######################
	async def _create_family(self, data: dict) -> str:
		return await family.create(data['data']['unique_id'], data['data']['name'],data['data']['icon'],**data)

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

	async def _set_notice_family(self, data: dict) -> str:
		return await family.set_notice(data['data']['unique_id'], data['data']['msg'], **data)

	async def _set_blackboard_family(self, data: dict) -> str:
		return await family.set_blackboard(data['data']['unique_id'], data['data']['msg'], **data)

	async def _set_icon_family(self, data: dict) -> str:
		return await family.set_icon(data['data']['unique_id'], int(data['data']['icon']), **data)

	async def _set_role_family(self, data: dict) -> str:
		return await family.set_role(data['data']['unique_id'], data['data']['gn_target'], int(data['data']['role']), **data)

	async def _change_name_family(self, data: dict) -> str:
		return await family.change_name(data['data']['unique_id'], data['data']['name'], **data)

	async def _get_all_family(self, data: dict) -> str:
		return await family.get_all(data['data']['unique_id'], **data)

	async def _get_store_family(self, data: dict) -> str:
		return await family.get_store(**data)

	async def _market_purchase_family(self, data: dict) -> str:
		return await family.purchase(data['data']['unique_id'], data['data']['sid'], **data)

	async def _welfare_purchase_family(self, data: dict) -> str:
		return await family.welfare(data['data']['unique_id'], data['data']['sid'], **data)

	async def _disband_family(self, data: dict) -> str:
		return await family.disband(data['data']['unique_id'], **data)

	async def _cancel_disband_family(self, data: dict) -> str:
		return await family.cancel_disband(data['data']['unique_id'], **data)

	async def _check_in_family(self, data: dict) -> str:
		return await family.check_in(data['data']['unique_id'], **data)

	async def _abdicate_family(self, data: dict) -> str:
		return await family.abdicate(data['data']['unique_id'], data['data']['target'], **data)

	async def _get_config_family(self, data: dict) -> str:
		return await family.config(**data)

	async def _search_family(self, data: dict) -> str:
		return await family.search(data['data']['family_name'], **data)

	async def _get_random_family(self, data: dict) -> str:
		return await family.get_random(int(data['data'].get('number', 5)), **data)

	###################### mail.py ######################
	async def _send_mail(self, data: dict) -> str:
		return await mail.send_mail_public(data['data']['unique_id'], data['data']['gn_target'], **data)

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
	async def _refresh_diamond_store(self, data: dict) -> str:
		return await summoning.refresh_d(data['data']['unique_id'], **data)

	async def _refresh_coin_store(self, data: dict) -> str:
		return await summoning.refresh_c(data['data']['unique_id'], **data)

	async def _refresh_gift_store(self, data: dict) -> str:
		return await summoning.refresh_g(data['data']['unique_id'], **data)

	async def _buy_refresh_diamond(self, data: dict) -> str:
		return await summoning.buy_refresh(data['data']['unique_id'], enums.Item.DIAMOND, **data)

	async def _buy_refresh_coin(self, data: dict) -> str:
		return await summoning.buy_refresh(data['data']['unique_id'], enums.Item.COIN, **data)

	async def _buy_refresh_gift(self, data: dict) -> str:
		return await summoning.buy_refresh(data['data']['unique_id'], enums.Item.FRIEND_GIFT, **data)

	async def _single_pump_diamond(self, data: dict) -> str:
		return await summoning.single_d(data['data']['unique_id'], **data)

	async def _single_pump_coin(self, data: dict) -> str:
		return await summoning.single_c(data['data']['unique_id'], **data)

	async def _single_pump_gift(self, data: dict) -> str:
		return await summoning.single_g(data['data']['unique_id'], **data)

	async def _dozen_pump_diamond(self, data: dict) -> str:
		return await summoning.dozen_d(data['data']['unique_id'], **data)

	async def _dozen_pump_coin(self, data: dict) -> str:
		return await summoning.dozen_c(data['data']['unique_id'], **data)

	async def _dozen_pump_gift(self, data: dict) -> str:
		return await summoning.dozen_g(data['data']['unique_id'], **data)

	async def _integral_convert(self, data: dict) -> str:
		return await summoning.integral_convert(data['data']['unique_id'], **data)

	###################### skill.py ######################
	async def _get_all_skill(self, data: dict) -> str:
		return await skill.get_all(data['data']['unique_id'], **data)

	async def _level_up_skill(self, data: dict) -> str:
		return await skill.level_up(data['data']['unique_id'], int(data['data']['skill']), int(data['data']['item']), **data)

	async def _get_config_skill(self, data: dict) -> str:
		return await skill.config(**data)

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

	async def _send_gift_all(self, data: dict) -> str:
		return await friend.send_gift_all(data['data']['unique_id'], **data)

	async def _get_gifts_friend(self, data: dict) -> str:
		return await friend.get_gifts(data['data']['unique_id'], data['data']['gns'], **data)

	async def _find_person(self, data: dict) -> str:
		return await friend.find_person(data['data']['unique_id'],data['data']['gn_target'], **data)
	###################### factory.py ######################
	async def _refresh_factory(self, data: dict) -> str:
		return await factory.refresh(data['data']['unique_id'], **data)

	async def _upgrade_factory(self, data: dict) -> str:
		return await factory.upgrade(data['data']['unique_id'], enums.Factory(int(data['data']['fid'])), **data)

	async def _activate_wishing_pool_factory(self, data: dict) -> str:
		return await factory.wishing_pool(data['data']['unique_id'], enums.Weapon(int(data['data']['wid'])), **data)

	async def _buy_worker_factory(self, data: dict) -> str:
		return await factory.buy_worker(data['data']['unique_id'], **data)

	async def _update_worker_factory(self, data: dict) -> str:
		return await factory.update_worker(data['data']['unique_id'], data['data']['worker'], **data)

	async def _set_armor_factory(self, data: dict) -> str:
		return await factory.set_armor(data['data']['unique_id'], enums.Armor(int(data['data'].get('aid', -1))), **data)

	async def _gather_resource_factory(self, data: dict) -> str:
		return await factory.gather_resource(data['data']['unique_id'], data['data']['resource'], **data)

	async def _iron_convert_factory(self, data: dict) -> str:
		return await factory.iron_convert(data['data']['unique_id'], data['data']['aid'], int(data['data']['qty']), **data)

	async def _buy_acceleration_factory(self, data: dict) -> str:
		return await factory.buy_acceleration(data['data']['unique_id'], **data)

	async def _get_config_factory(self, data: dict) -> str:
		return common.mt(0, 'success', data['config']['factory'])



	###################### weapon.py ######################
	async def _level_up_weapon(self, data: dict) -> str:
		return await weapon.level_up(data['data']['unique_id'], int(data['data']['weapon']), data['data'].get('delta', 1), **data)

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
		return await role.level_up(data['data']['unique_id'], int(data['data']['role']), data['data'].get('delta', 1), **data)

	async def _level_up_star_role(self, data: dict) -> str:
		return await role.level_up_star(data['data']['unique_id'], int(data['data']['role']), **data)

	async def _unlock_passive_role(self, data: dict) -> str:
		return await role.unlock_passive(data['data']['unique_id'], int(data['data']['rid']), int(data['data']['pid']), **data)

	async def _get_config_role(self, data: dict) -> str:
		return await role.get_config(**data)





	###################### ???????????? ######################
	async def _check_in_sign(self, data: dict) -> str:
		return await check_in.sign(data['data']['unique_id'],**data)

	async def _check_in_supplement(self, data: dict) -> str:
		return await check_in.supplement(data['data']['unique_id'],**data)

	async def _check_in_all(self, data: dict) -> str:
		return await check_in.all(data['data']['unique_id'],**data)

	async def _get_config_check_in(self, data: dict) -> str:
		return common.mt(0, 'success', {'config': data['config']['check_in']})

	###################### VIP ######################

	async def _get_vip_daily_reward(self, data: dict) -> str:
		return await vip.get_daily_reward(data['data']['unique_id'], **data)

	async def _purchase_vip_gift(self, data: dict) -> str:
		return await vip.buy_package(data['data']['unique_id'], data['data']['tier'], **data)

	async def _purchase_vip_card(self, data: dict) -> str:
		return await vip.buy_card(data['data']['unique_id'], int(data['data']['card_id']), **data)

	async def _get_info_vip(self, data: dict) -> str:
		return await vip.get_info(data['data']['unique_id'], **data)

	async def _get_config_vip(self, data: dict) -> str:
		return await vip.get_config(data['data']['unique_id'], **data)

	###################### player ######################
	async def _get_all_resource(self, data: dict) -> str:
		return await player.all_resource(data['data']['unique_id'], **data)

	async def _player_element_lv(self, data: dict) -> str:
		return await player.element_lv(data['data']['unique_id'], int(data['data']['eid']), **data)

	async def _player_element_all(self, data: dict) -> str:
		return await player.element_all(data['data']['unique_id'], **data)

	async def _player_element_reset(self, data: dict) -> str:
		return await player.element_reset(data['data']['unique_id'], **data)

	###################### achievement ######################
	async def _activate_achievement(self, data: dict) -> str:
		return await achievement.activate(data['data']['unique_id'], int(data["data"]["aid"]), **data)

	async def _get_all_achievement(self, data: dict) -> str:
		return await achievement.all(data['data']['unique_id'], **data)

	async def _get_achievement_reward(self, data: dict) -> str:
		return await achievement.reward(data['data']['unique_id'], data["data"]["achievement_id"], **data)

	async def _get_achievement_config(self, data: dict) -> str:
		return common.mt(0, 'success', data={'config': data['config']['achievement']})

	async def _get_config_achievement(self, data: dict) -> str:
		return common.mt(0, 'success', {'achievement_config': data['config']['achievement']})

	###################### armor ######################
	async def _upgrade_armor(self, data: dict) -> str:
		return await armor.upgrade(data['data']['unique_id'], data['data']['aid'], data['data']['level'], int(data['data'].get('num', 1)), **data)

	async def _get_all_armor(self, data: dict) -> str:
		return await armor.get_all(data['data']['unique_id'], **data)

	###################### stage ######################
	async def _stage_enter_general(self, data: dict) -> str:
		return await stage.enter(data['data']['unique_id'], enums.Stage.GENERAL, int(data['data']['stage']), **data)

	async def _stage_victory_general(self, data: dict) -> str:
		return await stage.victory(data['data']['unique_id'], enums.Stage.GENERAL, int(data['data']['stage']), **data)

	async def _stage_enter_endless(self, data: dict) -> str:
		return await stage.enter(data['data']['unique_id'], enums.Stage.ENDLESS, int(data['data']['stage']), **data)

	async def _stage_victory_endless(self, data: dict) -> str:
		return await stage.victory(data['data']['unique_id'], enums.Stage.ENDLESS, int(data['data']['stage']), **data)

	async def _stage_enter_boss(self, data: dict) -> str:
		return await stage.enter(data['data']['unique_id'], enums.Stage.BOSS, int(data['data']['stage']), **data)

	async def _stage_victory_boss(self, data: dict) -> str:
		return await stage.victory(data['data']['unique_id'], enums.Stage.BOSS, int(data['data']['stage']), data['data'].get('damage', 0), **data)

	async def _stage_enter_coin(self, data: dict) -> str:
		return await stage.enter(data['data']['unique_id'], enums.Stage.COIN, int(data['data']['stage']), **data)

	async def _stage_victory_coin(self, data: dict) -> str:
		return await stage.victory(data['data']['unique_id'], enums.Stage.COIN, int(data['data']['stage']), **data)

	async def _stage_enter_exp(self, data: dict) -> str:
		return await stage.enter(data['data']['unique_id'], enums.Stage.EXP, int(data['data']['stage']), **data)

	async def _stage_victory_exp(self, data: dict) -> str:
		return await stage.victory(data['data']['unique_id'], enums.Stage.EXP, int(data['data']['stage']), data['data'].get('damage', 0), **data)

	async def _stage_refresh_boss(self, data: dict) -> str:
		return await stage.refresh_boss(data['data']['unique_id'], **data)

	async def _stage_all_infos(self, data: dict) -> str:
		return await stage.all_infos(data['data']['unique_id'], **data)

	async def _stage_damage_ranking(self, data: dict) -> str:
		return await stage.damage_ranking(data['data']['unique_id'], data['data'].get('stage', 3000), data['data'].get('page', 1), **data)

	async def _stage_hang_up(self, data: dict) -> str:
		return await stage.hang_up(data['data']['unique_id'], **data)

	async def _stage_hu_show(self, data: dict) -> str:
		return await stage.hu_show(data['data']['unique_id'], **data)

	async def _stage_mopping_up(self, data: dict) -> str:
		return await stage.mopping_up(data['data']['unique_id'], data['data']['stage'], data['data'].get('count', 1), **data)

	async def _get_config_stage(self, data: dict) -> str:
		return common.mt(0, 'success', data['config']['stages'])

	###################### tasks ######################
	async def _get_all_task(self, data: dict) -> str:
		data.update({"config": data['config']['task']})
		return await task.get_all_task(data['data']['unique_id'],**data)

	async def _get_task_config(self, data: dict) -> str:
		return common.mt(0, 'success', data={'config': data['config']['task']})

	async def _get_task_reward(self, data: dict) -> str:
		return await task.get_task_reward(data['data']['unique_id'],data['data']['task_id'], **data)

	async def _get_config_task(self, data: dict) -> str:
		return common.mt(0, 'success', {'task_config': data['config']['task']})

	###################### darkmarket ######################
	async def _get_all_market(self, data: dict) -> str:
		return await darkmarket.get_all_market(data['data']['unique_id'], **data)

	async def _refresh_market(self, data: dict) -> str:
		return await darkmarket.refresh_market(data['data']['unique_id'], **data)

	async def _darkmarket_transaction(self, data: dict) -> str:
		return await darkmarket.transaction(data['data']['unique_id'], data['data']['pid'], **data)


	async def _get_config_mall(self, data: dict) -> str:
		return common.mt(0, 'success', {'mall_config': data['config']['mall']})

	async def _get_config_player(self, data: dict) -> str:
		data['exp_config'] = data['config']['exp']['player_level']['experience']
		energy = data['config']['player']['energy']
		return common.mt(0, 'success', {'player_config': data['config']['exp'], \
				'energy': {'time': energy["cooling_time"] * 60, 'max_energy': energy['max_energy']}})

	async def _get_config_version(self, data: dict) -> str:
		return common.mt(0, 'success', {'version': data['config']['version']})

	async def _buy_energy(self, data: dict) -> str:
		return await package.buy_energy(data['data']['unique_id'], **data)

	async def _buy_coin(self, data: dict) -> str:
		return await package.buy_coin(data['data']['unique_id'], int(data['data'].get('qty', 1)), **data)

	async def _exchange_card(self, data: dict) -> str:
		return await package.exchange(data['data']['unique_id'], int(data['data']['cid']), int(data['data'].get('qty', 1)), **data)

	async def _use_item(self, data: dict) -> str:
		return await package.use_item(data['data']['unique_id'], data['data']['item_id'], data['data'].get('exchange_id', ''), **data)

	async def _get_config_exchange(self, data: dict) -> str:
		return await package.config(data['data']['unique_id'], **data)

	async def _send_gift_mail(self, data: dict) -> str:
		return await common._send_gift_mail(data['data']['unique_id'], data['data']['gn_target'],data['data']['group_id'],data['data']['item_id'],data['data']['quantity'], **data)

	async def _send_text_mail(self, data: dict) -> str:
		return await common._send_text_mail(data['data']['unique_id'],data['data']['gn_target'], data['data']['msg'], **data)

	async def _purchase_success(self, data: dict) -> str:
		return await mall.rmb_mall(data['data']['pid'], data['data']['order_id'], data['data']['channel'], data['data']['user_name'], data['data']['currency'], **data)

	async def _exchange_prop(self, data: dict) -> str:
		return await mall.exchange(data['data']['unique_id'], data['data']['game_id'], data['data']['exchange_id'], **data)

	async def _add_resources(self, data: dict) -> str:
		results = {}
		await common.rw_common(data['data']['unique_id'], data['data']['items'], results, **data)
		# await stage.increase_exp(data['data']['unique_id'], random.randint(15000, 5000000), **data)
		return common.mt(0, 'success', results)

	async def _get_config_notice(self, data: dict) -> str:
		return common.mt(0, 'success', {'config': data['config']['notice']})

	async def _get_config_science(self, data: dict) -> str:
		return common.mt(0, 'success', {'config': data['config']['sciences']})

	async def _update_init(self, data: dict) -> str:
		# pds = await common.execute(f'SELECT uid FROM `player`;', **data)
		# for pd in pds:
		# 	await player._element_init(pd[0], **data)
		return common.mt(0, 'success')

##########################################################################################################
##########################################################################################################

DOES_NOT_NEED_TOKEN = {'register', 'login_unique', 'login'}

FUNCTION_LIST = {
	'update_init' : MessageHandler._update_init,
	###################### account.py ######################
	'register' : MessageHandler._register,
	'login_unique' : MessageHandler._login_unique,
	'login' : MessageHandler._login,
	'account_all_info' : MessageHandler._account_all_info,
	'bind_account' : MessageHandler._bind_account,
	'bind_email' : MessageHandler._bind_email,
	'unbind_email' : MessageHandler._unbind_email,
	'verify_email_code' : MessageHandler._verify_email_code,
	'bind_phone' : MessageHandler._bind_phone,
	'unbind_phone' : MessageHandler._unbind_phone,
	'verify_phone_code' : MessageHandler._verify_phone_code,
	# TODO
	'get_player_config' : MessageHandler._get_player_config,
	'create_account' : MessageHandler._create_account,
	'change_game_name' : MessageHandler._change_game_name,

	###################### chat.py ######################
	'get_login_token_chat' : MessageHandler._get_login_token_chat,

	###################### player.py ######################
	'enter_world' : MessageHandler._enter_world,
	'accept_gifts' : MessageHandler._accept_gifts,
	'create_player' : MessageHandler._create_player,
	'change_player_name' : MessageHandler._change_player_name,
	'player_set_intro' : MessageHandler._player_set_intro,
	'player_set_icon' : MessageHandler._player_set_icon,
	'get_account_world_info' : MessageHandler._get_account_world_info,
	'get_info_player' : MessageHandler._get_info_player,

	###################### family.py ######################
	'create_family': MessageHandler._create_family,
	'leave_family' : MessageHandler._leave_family,
	'remove_user_family' : MessageHandler._remove_user_family,
	'invite_user_family' : MessageHandler._invite_user_family,
	'request_join_family' : MessageHandler._request_join_family,
	'respond_family' : MessageHandler._respond_family,
	'set_notice_family' : MessageHandler._set_notice_family,
	'set_blackboard_family' : MessageHandler._set_blackboard_family,
	'set_icon_family' : MessageHandler._set_icon_family,
	'set_role_family' : MessageHandler._set_role_family,
	'change_name_family' : MessageHandler._change_name_family,
	'get_all_family' : MessageHandler._get_all_family,
	'disband_family' : MessageHandler._disband_family,
	'cancel_disband_family' : MessageHandler._cancel_disband_family,
	'get_store_family' : MessageHandler._get_store_family,
	'market_purchase_family' : MessageHandler._market_purchase_family,
	'welfare_purchase_family': MessageHandler._welfare_purchase_family,
	'check_in_family' : MessageHandler._check_in_family,
	'abdicate_family' : MessageHandler._abdicate_family,
	'search_family' : MessageHandler._search_family,
	'get_random_family' : MessageHandler._get_random_family,

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
	'refresh_diamond_store' : MessageHandler._refresh_diamond_store,
	'refresh_coin_store' : MessageHandler._refresh_coin_store,
	'refresh_gift_store' : MessageHandler._refresh_gift_store,
	'buy_refresh_diamond' : MessageHandler._buy_refresh_diamond,
	'buy_refresh_coin' : MessageHandler._buy_refresh_coin,
	'buy_refresh_gift' : MessageHandler._buy_refresh_gift,
	'single_pump_diamond' : MessageHandler._single_pump_diamond,
	'single_pump_coin' : MessageHandler._single_pump_coin,
	'single_pump_gift' : MessageHandler._single_pump_gift,
	'dozen_pump_diamond' : MessageHandler._dozen_pump_diamond,
	'dozen_pump_coin' : MessageHandler._dozen_pump_coin,
	'dozen_pump_gift' : MessageHandler._dozen_pump_gift,
	'integral_convert' : MessageHandler._integral_convert,

	###################### skill.py ######################
	'get_all_skill' : MessageHandler._get_all_skill,
	'level_up_skill' : MessageHandler._level_up_skill,

	###################### friend.py ######################
	'get_all_friend' : MessageHandler._get_all_friend,
	'remove_friend' : MessageHandler._remove_friend,
	'request_friend' : MessageHandler._request_friend,
	'send_gift_friend' : MessageHandler._send_gift_friend,
	'send_gift_all' : MessageHandler._send_gift_all,
	'get_gifts_friend' : MessageHandler._get_gifts_friend,
	'respond_friend':MessageHandler._respond_friend,
	'find_person':MessageHandler._find_person,

	###################### factory.py ######################
	'refresh_factory' : MessageHandler._refresh_factory,
	'upgrade_factory' : MessageHandler._upgrade_factory,
	'buy_worker_factory' : MessageHandler._buy_worker_factory,
	'update_worker_factory' : MessageHandler._update_worker_factory,
	'activate_wishing_pool_factory' : MessageHandler._activate_wishing_pool_factory,
	'buy_acceleration_factory' : MessageHandler._buy_acceleration_factory,
	'set_armor_factory' : MessageHandler._set_armor_factory,
	'gather_resource_factory' : MessageHandler._gather_resource_factory,
	'iron_convert_factory' : MessageHandler._iron_convert_factory,

	###################### weapon.py ######################
	'level_up_weapon' : MessageHandler._level_up_weapon,
	'level_up_passive_weapon' : MessageHandler._level_up_passive_weapon,
	'level_up_star_weapon' : MessageHandler._level_up_star_weapon,
	'reset_skill_point_weapon' : MessageHandler._reset_skill_point_weapon,
	'get_all_weapon' : MessageHandler._get_all_weapon,

	###################### role.py ######################
	'level_up_star_role' : MessageHandler._level_up_star_role,
	'level_up_role' : MessageHandler._level_up_role,
	'get_all_role' : MessageHandler._get_all_role,
	'unlock_passive_role' : MessageHandler._unlock_passive_role,

	###################### ???????????? ######################
	'check_in_sign' : MessageHandler._check_in_sign,
	'check_in_supplement' : MessageHandler._check_in_supplement,
	'check_in_all' : MessageHandler._check_in_all,

	###################### VIP ######################
	'get_vip_daily_reward' : MessageHandler._get_vip_daily_reward,
	'purchase_vip_gift' : MessageHandler._purchase_vip_gift,
	'purchase_vip_card' : MessageHandler._purchase_vip_card,
	'get_info_vip' : MessageHandler._get_info_vip,

	###################### player ######################
	'get_all_resource': MessageHandler._get_all_resource,
	'player_element_lv': MessageHandler._player_element_lv,
	'player_element_all': MessageHandler._player_element_all,
	'player_element_reset': MessageHandler._player_element_reset,

	###################### player ######################
	'science_infos': MessageHandler._science_infos,
	'science_up': MessageHandler._science_up,

	###################### achievement ######################
	'activate_achievement': MessageHandler._activate_achievement,
	'get_all_achievement': MessageHandler._get_all_achievement,
	'get_achievement_reward':MessageHandler._get_achievement_reward,
	'get_achievement_config':MessageHandler._get_achievement_config,

	###################### armor ######################
	'upgrade_armor': MessageHandler._upgrade_armor,
	'get_all_armor': MessageHandler._get_all_armor,

	###################### stage ######################
	# TODO 2020???3???25?????????????????????????????????
	'stage_enter_general': MessageHandler._stage_enter_general,
	'stage_victory_general': MessageHandler._stage_victory_general,
	'stage_enter_endless': MessageHandler._stage_enter_endless,
	'stage_victory_endless': MessageHandler._stage_victory_endless,
	'stage_enter_boss': MessageHandler._stage_enter_boss,
	'stage_victory_boss': MessageHandler._stage_victory_boss,
	'stage_enter_coin': MessageHandler._stage_enter_coin,
	'stage_victory_coin': MessageHandler._stage_victory_coin,
	'stage_enter_exp': MessageHandler._stage_enter_exp,
	'stage_victory_exp': MessageHandler._stage_victory_exp,
	'stage_refresh_boss': MessageHandler._stage_refresh_boss,
	'stage_all_infos': MessageHandler._stage_all_infos,
	'stage_damage_ranking': MessageHandler._stage_damage_ranking,
	'stage_hang_up': MessageHandler._stage_hang_up,
	'stage_hu_show': MessageHandler._stage_hu_show,
	'stage_mopping_up': MessageHandler._stage_mopping_up,


	###################### tasks ######################
	'get_task_config':MessageHandler._get_task_config,
	'get_all_task': MessageHandler._get_all_task,
	'get_task_reward': MessageHandler._get_task_reward,

	###################### darkmarket ######################
	'get_all_market': MessageHandler._get_all_market,
	'refresh_market': MessageHandler._refresh_market,
	'darkmarket_transaction': MessageHandler._darkmarket_transaction,

	###################### get_config ######################
	'get_config_stage': MessageHandler._get_config_stage,
	'get_config_weapon': MessageHandler._get_config_weapon,
	'get_config_skill': MessageHandler._get_config_skill,
	'get_config_mall': MessageHandler._get_config_mall,
	'get_config_role': MessageHandler._get_config_role,
	'get_config_task': MessageHandler._get_config_task,
	'get_config_achievement': MessageHandler._get_config_achievement,
	'get_config_check_in': MessageHandler._get_config_check_in,
	'get_config_vip': MessageHandler._get_config_vip,
	'get_config_player': MessageHandler._get_config_player,
	'get_config_factory': MessageHandler._get_config_factory,
	'get_config_version': MessageHandler._get_config_version,
	'get_config_family': MessageHandler._get_config_family,
	'get_config_exchange': MessageHandler._get_config_exchange,
	'get_config_notice': MessageHandler._get_config_notice,
	'get_config_science': MessageHandler._get_config_science,

	###################### package ######################
	'buy_energy': MessageHandler._buy_energy,
	'buy_coin': MessageHandler._buy_coin,
	'exchange_card': MessageHandler._exchange_card,
	'use_item': MessageHandler._use_item,

	###################### private(comment before release) ######################
	'send_gift_mail': MessageHandler._send_gift_mail,
	'send_text_mail': MessageHandler._send_text_mail,
	'purchase_success': MessageHandler._purchase_success,
	'exchange_prop': MessageHandler._exchange_prop,
	'add_resources': MessageHandler._add_resources
}

