'''
message_handler.py
'''

import json

from module import mail
from module import chat
from module import enums
from module import skill
from module import family
from module import factory
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
from module import stage
from module import check_in
from module import darkmarket
from module import package
from module import vip
from module import mall


from utility import metrics
C = metrics.Collector()

class MessageHandler:
	def __init__(self, *, token_addr, token_port, mail_addr, mail_port):
		self.functions      = FUNCTION_LIST
		self.mail_base_url  = mail_addr  + ':' + str(mail_port)
		self.token_base_url = token_addr + ':' + str(token_port)

	async def shutdown(self):
		pass

	# json.decoder.JSONDecodeError
	@C.collect_async
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
		message['mailserverbaseurl']  = self.mail_base_url
		message['tokenserverbaseurl'] = self.token_base_url
		message['config'] = configs  ############configs#################
		return json.dumps(await fn(self, message))

	async def validate_token(self, msg, session):
		async with session.post(self.token_base_url+'/validate',data={'token' : msg['data']['token']}) as r:
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
		return await player.create(data['data']['unique_id'], data['data']['gn'], **data)

	async def _enter_world(self, data: dict) -> str:
		return await player.enter_world(data['data']['unique_id'], **data)

	async def _get_account_world_info(self, data: dict) -> str:
		return await player.get_account_world_info(data['data']['unique_id'], **data)

	async def _accept_gifts(self, data: dict) -> str:
		return await player.accept_gifts(data['data']['unique_id'], data['data']['keys'], **data)

	async def _get_info_player(self, data: dict) -> str:
		data['player_energy'] = data['config']['player']['energy']
		return await player.get_info(data['data']['unique_id'], **data)


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

	async def _set_notice_family(self, data: dict) -> str:
		return await family.set_notice(data['data']['unique_id'], data['data']['msg'], **data)

	async def _set_blackboard_family(self, data: dict) -> str:
		return await family.set_blackboard(data['data']['unique_id'], data['data']['msg'], **data)

	async def _set_role_family(self, data: dict) -> str:
		return await family.set_role(data['data']['unique_id'], data['data']['gn_target'], int(data['data']['role']), **data)

	async def _change_name_family(self, data: dict) -> str:
		return await family.change_name(data['data']['unique_id'], data['data']['name'], **data)

	async def _get_all_family(self, data: dict) -> str:
		return await family.get_all(data['data']['unique_id'], **data)

	async def _get_store_family(self, data: dict) -> str:
		return await family.get_store(**data)

	async def _market_purchase_family(self, data: dict) -> str:
		return await family.purchase(data['data']['unique_id'], data['data']['item'], **data)

	async def _disband_family(self, data: dict) -> str:
		return await family.disband(data['data']['unique_id'], **data)

	async def _cancel_disband_family(self, data: dict) -> str:
		return await family.cancel_disband(data['data']['unique_id'], **data)

	async def _check_in_family(self, data: dict) -> str:
		return await family.check_in(data['data']['unique_id'], **data)

	async def _get_config_family(self, data: dict) -> str:
		return await family.config(**data)

	async def _gift_package_family(self, data: dict) -> str:
		return await family.gift_package(data['data']['unique_id'], **data)

	async def _get_random_family(self, data: dict) -> str:
		return await family.get_random(**data)

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
	async def _basic_summon(self, data: dict) -> str:
		return await summoning.summon(data['data']['unique_id'], int(data['data']['item']), enums.Tier.BASIC, enums.Group.WEAPON, **data)

	async def _pro_summon(self, data: dict) -> str:
		return await summoning.summon(data['data']['unique_id'], int(data['data']['item']), enums.Tier.PRO, enums.Group.WEAPON, **data)

	async def _friend_summon(self, data: dict) -> str:
		return await summoning.summon(data['data']['unique_id'], int(data['data']['item']), enums.Tier.FRIEND, enums.Group.WEAPON, **data)

	async def _prophet_summon(self, data: dict) -> str:
		return await summoning.summon(data['data']['unique_id'], int(data['data']['item']), enums.Tier.PROPHET, enums.Group.WEAPON, **data)

	async def _basic_summon_skill(self, data: dict) -> str:
		return await summoning.summon(data['data']['unique_id'], int(data['data']['item']), enums.Tier.BASIC, enums.Group.SKILL, **data)

	async def _pro_summon_skill(self, data: dict) -> str:
		return await summoning.summon(data['data']['unique_id'], int(data['data']['item']), enums.Tier.PRO, enums.Group.SKILL, **data)

	async def _friend_summon_skill(self, data: dict) -> str:
		return await summoning.summon(data['data']['unique_id'], int(data['data']['item']), enums.Tier.FRIEND, enums.Group.SKILL, **data)

	async def _basic_summon_role(self, data: dict) -> str:
		return await summoning.summon(data['data']['unique_id'], int(data['data']['item']), enums.Tier.BASIC, enums.Group.ROLE, **data)

	async def _pro_summon_role(self, data: dict) -> str:
		return await summoning.summon(data['data']['unique_id'], int(data['data']['item']), enums.Tier.PRO, enums.Group.ROLE, **data)

	async def _friend_summon_role(self, data: dict) -> str:
		return await summoning.summon(data['data']['unique_id'], int(data['data']['item']), enums.Tier.FRIEND, enums.Group.ROLE, **data)

	async def _basic_summon_10_times(self, data: dict) -> str:
		return await summoning.summon_multi(data['data']['unique_id'], int(data['data']['item']), enums.Tier.BASIC, enums.Group.WEAPON, **data)

	async def _pro_summon_10_times(self, data: dict) -> str:
		return await summoning.summon_multi(data['data']['unique_id'], int(data['data']['item']), enums.Tier.PRO, enums.Group.WEAPON, **data)

	async def _friend_summon_10_times(self, data: dict) -> str:
		return await summoning.summon_multi(data['data']['unique_id'], int(data['data']['item']), enums.Tier.FRIEND, enums.Group.WEAPON, **data)

	async def _basic_summon_skill_10_times(self, data: dict) -> str:
		return await summoning.summon_multi(data['data']['unique_id'], int(data['data']['item']), enums.Tier.BASIC, enums.Group.SKILL, **data)

	async def _pro_summon_skill_10_times(self, data: dict) -> str:
		return await summoning.summon_multi(data['data']['unique_id'], int(data['data']['item']), enums.Tier.PRO, enums.Group.SKILL, **data)

	async def _friend_summon_skill_10_times(self, data: dict) -> str:
		return await summoning.summon_multi(data['data']['unique_id'], int(data['data']['item']), enums.Tier.FRIEND, enums.Group.SKILL, **data)

	async def _basic_summon_role_10_times(self, data: dict) -> str:
		return await summoning.summon_multi(data['data']['unique_id'], int(data['data']['item']), enums.Tier.BASIC, enums.Group.ROLE, **data)

	async def _pro_summon_role_10_times(self, data: dict) -> str:
		return await summoning.summon_multi(data['data']['unique_id'], int(data['data']['item']), enums.Tier.PRO, enums.Group.ROLE, **data)

	async def _friend_summon_role_10_times(self, data: dict) -> str:
		return await summoning.summon_multi(data['data']['unique_id'], int(data['data']['item']), enums.Tier.FRIEND, enums.Group.ROLE, **data)

	###################### lottery.py ######################
	async def _fortune_wheel_basic(self, data: dict) -> str:
		return await lottery.fortune_wheel(data['data']['unique_id'], enums.Tier.BASIC, enums.Item(int(data['data']['item'])), **data)

	async def _fortune_wheel_pro(self, data: dict) -> str:
		return await lottery.fortune_wheel(data['data']['unique_id'], enums.Tier.PRO, enums.Item(int(data['data']['item'])), **data)

	async def _get_config_lottery(self, data: dict) -> str:
		return common.mt(0, 'success', {'config': \
				{'skills': data['config']['lottery']['random_gift']['SKILL']['cost'], \
				'weapons': data['config']['lottery']['random_gift']['WEAPON']['cost'], \
				'roles': data['config']['lottery']['random_gift']['ROLE']['cost'], \
				'fortune_wheel': data['config']['lottery']['fortune_wheel']['cost']}})

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
		return await factory.set_armor(data['data']['unique_id'], enums.Armor(int(data['data']['aid'])), **data)

	async def _buy_acceleration_factory(self, data: dict) -> str:
		return await factory.buy_acceleration(data['data']['unique_id'], **data)

	async def _get_config_factory(self, data: dict) -> str:
		return common.mt(0, 'success', data['config']['factory'])



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
	async def _check_in(self, data: dict) -> str:
		data.update({"check_in_config": data['config']['check_in']})
		return await check_in.check_in(data['data']['unique_id'],**data)

	async def _supplement_check_in(self, data: dict) -> str:
		data.update({"check_in_config": data['config']['check_in']})
		return await check_in.supplement_check_in(data['data']['unique_id'],**data)

	async def _get_all_check_in_table(self, data: dict) -> str:
		data.update({"config": data['config']['check_in']})
		return await check_in.get_all_check_in_table(data['data']['unique_id'],**data)

	async def _get_config_check_in(self, data: dict) -> str:
		return common.mt(0, 'success', {'check_in_config': data['config']['check_in']})

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
		return await player.get_all_resource(data['data']['unique_id'], **data)

	###################### achievement ######################
	async def _get_all_achievement(self, data: dict) -> str:
		return await achievement.get_all_achievement(data['data']['unique_id'], **data)

	async def _get_achievement_reward(self, data: dict) -> str:
		data.update({"config":self._acheviement})
		return await achievement.get_achievement_reward(data['data']['unique_id'], data["data"]["achievement_id"], **data)

	async def _get_achievement_config(self, data: dict) -> str:
		return common.mt(0, 'success', data={'config': self._acheviement})

	async def _get_config_achievement(self, data: dict) -> str:
		return common.mt(0, 'success', {'achievement_config': self._acheviement})

	###################### armor ######################
	async def _upgrade_armor(self, data: dict) -> str:
		return await armor.upgrade(data['data']['unique_id'], data['data']['aid'], data['data']['level'], **data)

	async def _get_all_armor(self, data: dict) -> str:
		return await armor.get_all(data['data']['unique_id'], **data)

	###################### stage ######################
	async def _get_all_tower(self, data: dict) -> str:
		return common.mt(0, 'success', {'tower_config': data['config']['entry_consumables']})

	async def _enter_stage(self, data: dict) -> str:
		data.update({'player_energy': data['config']['player']['energy']})  # try_energy
		data.update({'entry_consume': data['config']['entry_consumables'], \
				'enemy_layouts': data['config']['enemy_layouts']})
		data['monster_config'] = data['config']['monster']
		data['boss_life_remaining'] = data['config']['world_boss']['boss_life_remaining']
		data['boss_life'] = data['config']['world_boss']['boss_life']
		data['max_enter_time'] = data['config']['world_boss']['max_enter_time']
		data['max_upload_damage'] = data['config']['world_boss']['max_upload_damage']
		return await stage.enter_stage(data['data']['unique_id'], data['data']['stage'], **data)

	async def _pass_stage(self, data: dict) -> str:
		data['boss_life_remaining'] = data['config']['world_boss']['boss_life_remaining']
		data['boss_life'] = data['config']['world_boss']['boss_life']
		data['pass_rewards'] = data['config']['stage_reward'] 
		data['max_upload_damage'] = data['config']['world_boss']['max_upload_damage']
		return await stage.pass_stage(data['data']['unique_id'], data['data']['stage'], **data)

	async def _get_config_stage(self, data: dict) -> str:
		return common.mt(0, 'success', {'entry_consumables_config': data['config']['entry_consumables'], \
				'stage_reward_config': data['config']['stage_reward'], \
				'hang_reward_config': data['config']['hang_reward']})

	async def _get_top_damage(self, data: dict) -> str:
		return await stage.get_top_damage(data['data']['unique_id'], data['data']['page'], **data)

	async def _get_config_boss(self, data: dict):
		return common.mt(0, 'success', {'config': data['config']['world_boss']})

	async def _start_hang_up(self, data: dict) -> str:
		data.update({'hang_rewards': data['config']['hang_reward']})
		return await stage.start_hang_up(data['data']['unique_id'], data['data']['stage'], **data)

	async def _get_hang_up_reward(self, data: dict) -> str:
		data.update({'hang_rewards': data['config']['hang_reward']})
		return await stage.get_hang_up_reward(data['data']['unique_id'], **data)

	# async def _get_hang_up_info(self, data: dict) -> str:
	# 	data.update({'hang_rewards': data['config']['hang_reward']})
	# 	return await stage.get_hang_up_info(data['data']['unique_id'], **data)


	###################### tasks ######################
	async def _get_all_task(self, data: dict) -> str:
		data.update({"config": data['config']['task']})
		return await task.get_all_task(data['data']['unique_id'],**data)

	async def _get_task_config(self, data: dict) -> str:
		return common.mt(0, 'success', data={'config': data['config']['task']})

	async def _get_task_reward(self, data: dict) -> str:
		data.update({"config": data['config']['task']},)
		return await task.get_task_reward(data['data']['unique_id'],data['data']['task_id'], **data)

	async def _get_config_task(self, data: dict) -> str:
		return common.mt(0, 'success', {'task_config': data['config']['task']})

	###################### darkmarket ######################
	async def _get_all_market(self, data: dict) -> str:
		data['dark_market'] = data['config']['player']['dark_market']
		return await darkmarket.get_all_market(data['data']['unique_id'], **data)

	async def _refresh_market(self, data: dict) -> str:
		data['dark_market'] = data['config']['player']['dark_market']
		return await darkmarket.refresh_market(data['data']['unique_id'], **data)

	async def _darkmarket_transaction(self, data: dict) -> str:
		return await darkmarket.transaction(data['data']['unique_id'], data['data']['pid'], **data)

	# TODO Done 在这里直接返回配置信息，后面配置信息存放位置变动会做相应的改动
	async def _stage_reward_config(self, data: dict) -> str:
		return common.mt(0, 'success', {'config': data['config']['stage_reward']})


	async def _get_config_mall(self, data: dict) -> str:
		return common.mt(0, 'success', {'mall_config': data['config']['mall']})

	# TODO
	async def _check_boss_status(self, data: dict) -> str:
		data['boss_life_remaining'] = data['config']['world_boss']['boss_life_remaining']
		data['boss_life'] = data['config']['world_boss']['boss_life']
		data['max_enter_time'] = data['config']['world_boss']['max_enter_time']
		data['max_upload_damage'] = data['config']['world_boss']['max_upload_damage']
		return await stage.check_boss_status(data['data']['unique_id'], **data)
		# return {'status' : 0, 'message' : 'temp function success', 'data' :{'boss' :{'world_boss_enter_time':"2019/10/10 17:00:00",'world_boss_remaining_times':"20",'hp_values':["%.2f" %(int(self._boss_life_remaining[i])/int(self._boss_life[i])) for i in range(0,9)]}}}

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

	async def _get_config_player(self, data: dict) -> str:
		data['exp_config'] = data['config']['exp']['player_level']['experience']
		energy = data['config']['player']['energy']
		return common.mt(0, 'success', {'player_config': data['config']['exp'], \
				'energy': {'time': energy["cooling_time"] * 60, 'max_energy': energy['max_energy']}})

	async def _get_config_version(self, data: dict) -> str:
		return common.mt(0, 'success', {'version': data['config']['version']})

	async def _exchange_card(self, data: dict) -> str:
		return await package.exchange(data['data']['unique_id'], int(data['data']['card_id']), int(data['data']['quantity']), **data)

	async def _get_config_card(self, data: dict) -> str:
		return await package.config(data['data']['unique_id'], **data)

	async def _send_gift_mail(self, data: dict) -> str:
		return await common._send_gift_mail(data['data']['unique_id'], data['data']['gn_target'],data['data']['group_id'],data['data']['item_id'],data['data']['quantity'], **data)

	async def _send_text_mail(self, data: dict) -> str:
		return await common._send_text_mail(data['data']['unique_id'],data['data']['gn_target'], data['data']['msg'], **data)

	async def _purchase_success(self, data: dict) -> str:
		return await mall.rmb_mall(data['data']['pid'], data['data']['order_id'], data['data']['channel'], data['data']['user_name'], data['data']['currency'], **data)


##########################################################################################################
##########################################################################################################

DOES_NOT_NEED_TOKEN = {'login_unique', 'login'}

FUNCTION_LIST = {
	###################### account.py ######################
	'login_unique' : MessageHandler._login_unique,
	'login' : MessageHandler._login,
	'bind_account' : MessageHandler._bind_account,
	'bind_email' : MessageHandler._bind_email,
	'verify_email_code' : MessageHandler._verify_email_code,
	# TODO
	'get_player_config' : MessageHandler._get_player_config,
	'create_account' : MessageHandler._create_account,
	'change_game_name' : MessageHandler._change_game_name,

	###################### skill.py ######################
	'get_login_token_chat' : MessageHandler._get_login_token_chat,

	###################### player.py ######################
	'enter_world' : MessageHandler._enter_world,
	'accept_gifts' : MessageHandler._accept_gifts,
	'create_player' : MessageHandler._create_player,
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
	'set_role_family' : MessageHandler._set_role_family,
	'change_name_family' : MessageHandler._change_name_family,
	'get_all_family' : MessageHandler._get_all_family,
	'disband_family' : MessageHandler._disband_family,
	'cancel_disband_family' : MessageHandler._cancel_disband_family,
	'get_store_family' : MessageHandler._get_store_family,
	'market_purchase_family' : MessageHandler._market_purchase_family,
	'check_in_family' : MessageHandler._check_in_family,
	'gift_package_family' : MessageHandler._gift_package_family,
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

	###################### skill.py ######################
	'get_all_skill' : MessageHandler._get_all_skill,
	'level_up_skill' : MessageHandler._level_up_skill,

	###################### friend.py ######################
	'get_all_friend' : MessageHandler._get_all_friend,
	'remove_friend' : MessageHandler._remove_friend,
	'request_friend' : MessageHandler._request_friend,
	'send_gift_friend' : MessageHandler._send_gift_friend,
	'send_gift_all' : MessageHandler._send_gift_all,
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

	###################### weapon.py ######################
	'level_up_weapon' : MessageHandler._level_up_weapon,
	'level_up_passive_weapon' : MessageHandler._level_up_passive_weapon,
	'level_up_star_weapon' : MessageHandler._level_up_star_weapon,
	'reset_skill_point_weapon' : MessageHandler._reset_skill_point_weapon,
	'get_all_weapon' : MessageHandler._get_all_weapon,

	# TODO
	###################### role.py ######################
	'level_up_star_role' : MessageHandler._level_up_star_role,
	'level_up_role' : MessageHandler._level_up_role,
	'get_all_role' : MessageHandler._get_all_role,

	# TODO
	###################### 签到系统 ######################
	'check_in' : MessageHandler._check_in,
	'supplement_check_in' : MessageHandler._supplement_check_in,
	'get_all_check_in_table' : MessageHandler._get_all_check_in_table,

	###################### VIP ######################
	'get_vip_daily_reward' : MessageHandler._get_vip_daily_reward,
	'purchase_vip_gift' : MessageHandler._purchase_vip_gift,
	'purchase_vip_card' : MessageHandler._purchase_vip_card,
	'get_info_vip' : MessageHandler._get_info_vip,

	# TODO
	###################### player ######################
	'get_all_resource': MessageHandler._get_all_resource,

	# TODO
	###################### achievement ######################
	'get_all_achievement': MessageHandler._get_all_achievement,
	'get_achievement_reward':MessageHandler._get_achievement_reward,
	'get_achievement_config':MessageHandler._get_achievement_config,

	###################### armor ######################
	'upgrade_armor': MessageHandler._upgrade_armor,
	'get_all_armor': MessageHandler._get_all_armor,

	# TODO
	###################### stage ######################
	'get_all_tower': MessageHandler._get_all_tower,
	'enter_stage': MessageHandler._enter_stage,
	'pass_stage': MessageHandler._pass_stage,
	# 'enter_tower': MessageHandler._enter_tower,
	# 'pass_tower': MessageHandler._pass_tower,
	'start_hang_up': MessageHandler._start_hang_up,
	'get_hang_up_reward': MessageHandler._get_hang_up_reward,

	###################### tasks ######################
	'get_task_config':MessageHandler._get_task_config,
	'get_all_task': MessageHandler._get_all_task,
	'get_task_reward': MessageHandler._get_task_reward,

	###################### darkmarket ######################
	'get_all_market': MessageHandler._get_all_market,
	'refresh_market': MessageHandler._refresh_market,
	'darkmarket_transaction': MessageHandler._darkmarket_transaction,

	# TODO 新增
	'stage_reward_config': MessageHandler._stage_reward_config,
	# 'get_hang_up_info': MessageHandler._get_hang_up_info,
	'check_boss_status':MessageHandler._check_boss_status,
	'get_factory_info':MessageHandler._get_factory_info,
	'refresh_all_storage':MessageHandler._refresh_all_storage,
	'get_all_family_info': MessageHandler._get_all_family_info,
	'get_top_damage':MessageHandler._get_top_damage,

	###################### get_config ######################
	'get_config_stage': MessageHandler._get_config_stage,
	'get_config_boss': MessageHandler._get_config_boss,
	'get_config_lottery': MessageHandler._get_config_lottery,
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
	'get_config_card': MessageHandler._get_config_card,

	###################### package ######################
	'exchange_card': MessageHandler._exchange_card,

	###################### private(comment before release) ######################
	'send_gift_mail': MessageHandler._send_gift_mail,
	'send_text_mail': MessageHandler._send_text_mail,
	'purchase_success': MessageHandler._purchase_success,
}

