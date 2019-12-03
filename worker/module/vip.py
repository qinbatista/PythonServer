'''
vip.py
'''

from module import (enums, common)
from datetime import datetime, timedelta

DAYS = 31


async def get_config(uid, **kwargs):
	"""返回VIP的配置信息"""
	return common.mt(0, 'success', {'config': kwargs['config']['vip']})


async def get_info(uid, **kwargs):
	"""返回VIP经验相关信息，VIP过期剩余时间，VIP月卡类型"""
	exp_info = await increase_exp(uid, 0, **kwargs)
	min_card, max_card, perpetual_card = await check_card(uid, **kwargs)
	min_seconds, max_seconds = 0, 0
	if min_card:
		timer = await common.execute(f'SELECT time FROM timer WHERE uid="{uid}" AND tid="{enums.Timer.VIP_MIN_END_TIME.value}";', **kwargs)
		min_seconds = int((datetime.strptime(timer[0][0], '%Y-%m-%d %H:%M:%S').replace(tzinfo=common.TZ_SH) - datetime.now(tz=common.TZ_SH)).total_seconds())
	if max_card:
		timer = await common.execute(f'SELECT time FROM timer WHERE uid="{uid}" AND tid="{enums.Timer.VIP_MAX_END_TIME.value}";', **kwargs)
		max_seconds = int((datetime.strptime(timer[0][0], '%Y-%m-%d %H:%M:%S').replace(tzinfo=common.TZ_SH) - datetime.now(tz=common.TZ_SH)).total_seconds())

	timer = await common.execute(f'SELECT time FROM timer WHERE uid="{uid}" AND tid="{enums.Timer.VIP_COOLING_TIME.value}";', **kwargs)
	if timer == ():
		await common.execute(f'INSERT INTO timer (uid, tid) VALUE ("{uid}", "{enums.Timer.VIP_COOLING_TIME.value}");', **kwargs)
		timer = await common.execute(f'SELECT time FROM timer WHERE uid="{uid}" AND tid="{enums.Timer.VIP_COOLING_TIME.value}";', **kwargs)
	cooling_time = -1
	if timer[0][0] != '':
		cooling_time = int((datetime.strptime(timer[0][0], '%Y-%m-%d %H:%M:%S').replace(tzinfo=common.TZ_SH) - datetime.now(tz=common.TZ_SH)).total_seconds())
	return common.mt(0, 'success', {'exp_info': exp_info, 'min_card': min_card, 'max_card': max_card, 'min_seconds': min_seconds, 'max_seconds': max_seconds, 'perpetual_card': perpetual_card, 'cooling_time': cooling_time})


async def get_daily_reward(uid, **kwargs):
	"""获得VIP每日奖励
	0 - success
	98 - You're not a VIP
	99 - The cooling time is not over
	"""
	config = kwargs['config']['vip']
	current = datetime.now(tz=common.TZ_SH)
	timer = await common.execute(f'SELECT time FROM timer WHERE uid="{uid}" AND tid="{enums.Timer.VIP_COOLING_TIME.value}";', **kwargs)
	if timer == ():
		await common.execute(f'INSERT INTO timer (uid, tid) VALUE ("{uid}", "{enums.Timer.VIP_COOLING_TIME.value}");', **kwargs)
		timer = await common.execute(f'SELECT time FROM timer WHERE uid="{uid}" AND tid="{enums.Timer.VIP_COOLING_TIME.value}";', **kwargs)
	if timer[0][0] != '' and current < datetime.strptime(timer[0][0], '%Y-%m-%d %H:%M:%S').replace(tzinfo=common.TZ_SH):
		return common.mt(99, 'The cooling time is not over')

	min_card, max_card, perpetual_card = await check_card(uid, **kwargs)
	data = {'remaining': {'min_card': {'card': min_card}, 'max_card': {'card': max_card}, 'perpetual_card': {'card': perpetual_card}},
			'reward': {'min_card': {}, 'max_card': {}, 'perpetual_card': {}}}
	exp_info = {}
	if min_card:
		exp_info = await increase_exp(uid, config['card_increase_experience'].get('min', 10), **kwargs)
		remaining, reward = await increase_item(uid, config['vip_daily_reward'][f'{exp_info["level"]}'], **kwargs)
		data['remaining']['min_card']['item'] = remaining
		data['reward']['min_card']['item'] = reward
	if max_card:
		exp_info = await increase_exp(uid, config['card_increase_experience'].get('max', 15), **kwargs)
		remaining, reward = await increase_item(uid, config['vip_daily_reward'][f'{exp_info["level"]}'], **kwargs)
		data['remaining']['max_card']['item'] = remaining
		data['reward']['max_card']['item'] = reward
	if perpetual_card:
		exp_info = await increase_exp(uid, config['card_increase_experience'].get('permanent', 20), **kwargs)
		remaining, reward = await increase_item(uid, config['vip_daily_reward'][f'{exp_info["level"]}'], **kwargs)
		data['remaining']['perpetual_card']['item'] = remaining
		data['reward']['perpetual_card']['item'] = reward
	if exp_info == {}: return common.mt(98, "You're not a VIP")
	current = (current + timedelta(seconds=config["vip_daily_reward"].get("cooling_time", 86400))).strftime("%Y-%m-%d %H:%M:%S")
	await common.execute(f'UPDATE timer SET time="{current}" WHERE uid="{uid}" AND tid="{enums.Timer.VIP_COOLING_TIME.value}";', **kwargs)
	data['remaining']['exp_info'] = exp_info
	return common.mt(0, 'success', data)


async def buy_package(uid, tier, **kwargs):
	"""购买VIP礼包，VIP等级以下的可以购买
	tier: 与VIP指等级相对应
	gift: 指对应等级下的礼物
	98 - Diamond insufficient
	99 - You don't have enough VIP status(VIP等级不够，无法购买那一层的礼包)
	"""
	exp_info = await increase_exp(uid, 0, **kwargs)
	if tier > exp_info['level']: return common.mt(99, "You don't have enough VIP status")

	config = kwargs['config']['vip']['vip_special_package'][f'{tier}']
	cast_diamond = -config.get('cast_diamond', 0)
	can, diamond = await common.try_item(uid, enums.Item.DIAMOND, cast_diamond, **kwargs)
	if not can: return common.mt(98, 'Diamond insufficient')

	data = {'remaining': {'diamond': diamond, 'gifts': []}, 'reward': {'diamond': cast_diamond, 'gifts': []}, 'exp_info': exp_info}
	gift_package = common.decode_items(','.join(config['package']))
	for gid, item, qty in gift_package:
		value = -1
		if gid == enums.Group.ITEM:
			_, value = await common.try_item(uid, item, qty, **kwargs)
		elif gid == enums.Group.WEAPON:  # 只增加武器碎片
			_, value = await common.try_weapon(uid, item, qty, **kwargs)
		elif gid == enums.Group.ROLE:  # 只增加角色碎片
			_, value = await common.try_role(uid, item, qty, **kwargs)
		data['reward']['gifts'].append({'gid': gid.value, 'mid': item.value, 'qty': qty})
		data['remaining']['gifts'].append({'gid': gid.value, 'mid': item.value, 'qty': value})
	return common.mt(0, 'success', data)


async def buy_card(uid, cid, **kwargs):
	"""
	购买VIP卡，分为小月卡、大月卡、永久月卡
	小月卡：登录领取VIP每日奖励获得VIP经验10点，一个月的过期期限
	大月卡：登录领取VIP每日奖励获得VIP经验15点，一个月的过期期限
	永久月卡：登录领取VIP每日奖励获得VIP经验20点，无过期期限
	0 - success
	99 - card id error
	TODO 人民币购买
	"""
	card_kind = [enums.Item.VIP_CARD_MIN.value, enums.Item.VIP_CARD_MAX.value, enums.Item.VIP_CARD_PERPETUAL.value]
	if cid not in card_kind: return common.mt(99, 'card id error')
	min_card, max_card, _ = await check_card(uid, **kwargs)

	seconds = -1
	await common.execute(f'UPDATE item SET value=1 WHERE uid="{uid}" AND iid={cid};', **kwargs)
	if cid != enums.Item.VIP_CARD_PERPETUAL.value:
		tid = enums.Timer.VIP_MIN_END_TIME.value if cid == enums.Item.VIP_CARD_MIN.value else enums.Timer.VIP_MAX_END_TIME.value
		current = datetime.now(tz=common.TZ_SH)
		if min_card and cid == enums.Item.VIP_CARD_MIN.value or max_card and cid == enums.Item.VIP_CARD_MAX.value:
			timer = (await common.execute(f'SELECT time FROM timer WHERE uid="{uid}" AND tid="{tid}";', **kwargs))[0][0]
			timer = datetime.strptime(timer, '%Y-%m-%d %H:%M:%S').replace(tzinfo=common.TZ_SH) + timedelta(days=DAYS)
			seconds = int((timer - current).total_seconds())
			current = timer.strftime('%Y-%m-%d %H:%M:%S')
		else:
			seconds = DAYS * 24 * 3600
			current = (current + timedelta(days=DAYS)).strftime('%Y-%m-%d %H:%M:%S')
		await common.execute(f'UPDATE timer SET time="{current}" WHERE uid="{uid}" AND tid="{tid}";', **kwargs)
	return common.mt(0, 'success', {'cooling_time': seconds, 'card_id': cid})


####################################################################################
async def check_card(uid, **kwargs):
	"""检查月卡等级，返回是否存在VIP月卡，月卡等级信息"""
	current = datetime.now(tz=common.TZ_SH)
	min_card = False
	item = await common.execute(f'SELECT value FROM item WHERE uid="{uid}" AND iid="{enums.Item.VIP_CARD_MIN.value}";', **kwargs)
	if item == ():
		await common.execute(f'INSERT INTO item (uid, iid, value) VALUES ("{uid}", "{enums.Item.VIP_CARD_MIN.value}", 0);', **kwargs)
		await common.execute(f'INSERT INTO timer (uid, tid) VALUES ("{uid}", "{enums.Timer.VIP_MIN_END_TIME.value}");', **kwargs)
	else:
		timer = await common.execute(f'SELECT time FROM timer WHERE uid="{uid}" AND tid="{enums.Timer.VIP_MIN_END_TIME.value}";', **kwargs)
		if timer == (): await common.execute(f'DELETE FROM item WHERE uid="{uid}" AND iid="{enums.Item.VIP_CARD_MIN.value}";', **kwargs)
		elif timer[0][0] == '': pass
		else: min_card = datetime.strptime(timer[0][0], '%Y-%m-%d %H:%M:%S').replace(tzinfo=common.TZ_SH) > current

	max_card = False
	item = await common.execute(f'SELECT value FROM item WHERE uid="{uid}" AND iid="{enums.Item.VIP_CARD_MAX.value}";', **kwargs)
	if item == ():
		await common.execute(f'INSERT INTO item (uid, iid, value) VALUES ("{uid}", "{enums.Item.VIP_CARD_MAX.value}", 0);', **kwargs)
		await common.execute(f'INSERT INTO timer (uid, tid) VALUES ("{uid}", "{enums.Timer.VIP_MAX_END_TIME.value}");', **kwargs)
	else:
		timer = await common.execute(f'SELECT time FROM timer WHERE uid="{uid}" AND tid="{enums.Timer.VIP_MAX_END_TIME.value}";', **kwargs)
		if timer == (): await common.execute(f'DELETE FROM item WHERE uid="{uid}" AND iid="{enums.Item.VIP_CARD_MAX.value}";', **kwargs)
		elif timer[0][0] == '': pass
		else: max_card = datetime.strptime(timer[0][0], '%Y-%m-%d %H:%M:%S').replace(tzinfo=common.TZ_SH) > current

	perpetual_card = False
	item = await common.execute(f'SELECT value FROM item WHERE uid="{uid}" AND iid="{enums.Item.VIP_CARD_PERPETUAL.value}";', **kwargs)
	if item == (): await common.execute(f'INSERT INTO item (uid, iid, value) VALUES ("{uid}", "{enums.Item.VIP_CARD_PERPETUAL.value}", 0);', **kwargs)
	elif item[0][0] == 1: perpetual_card = True
	return min_card, max_card, perpetual_card


async def increase_exp(uid, exp, **kwargs):
	"""增加VIP经验
	exp为0则获得经验，反之取绝对值增加经验，
	并返回总经验和等级，升到下一级需要的经验
	"""
	# 取配置和数据
	exp_config = kwargs['config']['vip']['vip_level']['experience']
	exp_data = await common.execute(f'SELECT vipexp FROM progress WHERE uid = "{uid}";', **kwargs)
	if exp_data == ():
		await common.execute(f'INSERT INTO progress (uid) VALUE ("{uid}");', **kwargs)
		exp_data = await common.execute(f'SELECT vipexp FROM progress WHERE uid = "{uid}";', **kwargs)
	# 计算等级和需要的经验
	exp_s = exp_data[0][0]
	exp_list = [e for e in exp_config if e > exp_s]
	level, need = exp_config.index(exp_list[0]) if exp_list != [] else len(exp_config), exp_list[0] - exp_s if exp_list != [] else 0
	if exp == 0: return {'exp': exp_s, 'level': level, 'need': need}
	# 重新计算等级和需要的经验
	exp_s += exp
	exp_list = [e for e in exp_config if e > exp_s]
	level, need = exp_config.index(exp_list[0]) if exp_list != [] else len(exp_config), exp_list[0] - exp_s if exp_list != [] else 0
	await common.execute_update(f'UPDATE progress SET vipexp = {exp_s} WHERE uid = "{uid}";', **kwargs)
	# 成就刷新判断
	achievement_data = await common.execute(f'SELECT value FROM achievement WHERE uid="{uid}" and aid = "{enums.Achievement.VIP_LEVEL.value}"', **kwargs)
	if achievement_data == () or achievement_data[0][0] < level: await common.execute(f'INSERT INTO achievement (uid, aid, value,reward) VALUES ("{uid}", {enums.Achievement.VIP_LEVEL.value}, {level},0) ON DUPLICATE KEY UPDATE `value`= {level}', **kwargs)
	# 返回总经验、等级、需要经验
	return {'exp': exp_s, 'level': level, 'need': need}


async def increase_item(uid, vip_config, **kwargs) -> (list, list):
	remaining = []
	reward = []
	for iid in vip_config.keys():
		_, value = await common.try_item(uid, enums.Item(int(iid)), vip_config[iid], **kwargs)
		reward.append({'iid': iid, 'value': vip_config[iid]})
		remaining.append({'iid': iid, 'value': value})
	return remaining, reward





