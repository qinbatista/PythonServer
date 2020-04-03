'''
summoning.py
'''

from module import enums
from module import common
from module import lottery
from module import task
from module import role
from module import achievement
import random
from datetime import datetime, timedelta
import asyncio
# Tier
# basic, friend, pro, prophet
# RewardGroup
# weapon, skill, role

SWITCH = {}
# 99 - insufficient materials
# 98 - error item
# 97 - error item, item type
# 96 - ???
# 95 - Insufficient number of lucky draw
# 94 - cid error
# 93 - The configuration file does not exist


async def summon(uid, item, tier, rewardgroup, **kwargs):
	if item not in enums.Item._value2member_map_.keys():
		return common.mt(97, f'error item:{item}, item type:{type(item)}')
	item = enums.Item(item)
	return await _base_summon(uid, item, tier, rewardgroup, **kwargs)

async def summon_multi(uid, item, tier, rewardgroup, num_times = 10, **kwargs):
	if item not in enums.Item._value2member_map_.keys():
		return common.mt(97, f'error item:{item}, item type:{type(item)}')
	item = enums.Item(item)
	return await _base_summon_multi(uid, item, tier, rewardgroup, num_times, **kwargs)

##############################################################

async def _base_summon(uid, item, tier, rewardgroup, **kwargs):
	if f'{enums.Group.ITEM.value}:{item.value}' not in kwargs['config']['lottery']['random_gift'][rewardgroup.name]['cost'][tier.name].keys(): return common.mt(98, f'error item:{item}')
	cost = kwargs['config']['lottery']['random_gift'][rewardgroup.name]['cost'][tier.name][f'{enums.Group.ITEM.value}:{item.value}']
	can_pay, remaining = await common.try_item(uid, item, -cost, **kwargs)
	if not can_pay: return common.mt(99, 'insufficient materials')
	new, reward = await lottery.random_gift(uid, tier, rewardgroup, **kwargs)

	await achievement.record(uid, enums.Achievement.SUMMON_TIMES, **kwargs)
	if enums.Tier.BASIC == tier:
		await task.task(uid, enums.Task.BASIC_SUMMONING, **kwargs)
	if enums.Tier.PRO == tier:
		await task.record(uid, enums.Task.PRO_SUMMONING, **kwargs)
		await achievement.record(uid, enums.Achievement.PRO_SUMMON_TIMES, **kwargs)

	return await _response_factory(uid, rewardgroup, new, reward, item, remaining, cost, **kwargs)

async def _base_summon_multi(uid, item, tier, rewardgroup, num_times, **kwargs):
	if f'{enums.Group.ITEM.value}:{item.value}' not in kwargs['config']['lottery']['random_gift'][rewardgroup.name]['cost'][tier.name].keys(): return common.mt(98, f'error item:{item}')
	cost = kwargs['config']['lottery']['random_gift'][rewardgroup.name]['cost'][tier.name][f'{enums.Group.ITEM.value}:{item.value}']
	can_pay, remaining = await common.try_item(uid, item, -cost * num_times, **kwargs)
	if not can_pay: return common.mt(99, 'insufficient materials')
	response = {'remaining' : {}, 'reward' : {}}
	for time in range(num_times):
		if enums.Tier.BASIC == tier:
			await task.record(uid, enums.Task.BASIC_SUMMONING, **kwargs)
		if enums.Tier.PRO == tier:
			await task.record(uid, enums.Task.PRO_SUMMONING, **kwargs)
			await achievement.record(uid, enums.Achievement.PRO_SUMMON_TIMES, **kwargs)

		new, reward = await lottery.random_gift(uid, tier, rewardgroup, **kwargs)
		result = await _response_factory(uid, rewardgroup, new, reward, item, remaining, cost, **kwargs)
		response['remaining'][time] = result['data']['remaining']
		response['reward'][time] = result['data']['reward']
	return common.mt(0, 'success', response)


async def _response_factory(uid, rewardgroup, new, reward, item, remaining, cost, **kwargs):
	return await SWITCH[rewardgroup](uid, rewardgroup, new, reward, item, remaining, cost, **kwargs)

async def _response_factory_weapon(uid, rewardgroup, new, reward, item, remaining, cost, **kwargs):
	if new:
		return common.mt(2, 'new weapon unlocked', {'remaining' : {'weapon' : reward.value, 'star' : 1, 'segment' : 0, 'cost_item' : item.value, 'cost_quantity' : remaining}, 'reward' : {'weapon' : reward.value, 'star' : 1, 'segment': 0, 'cost_item' : item.value, 'cost_quantity': cost}})
	else:
		star, segment = (await common.execute(f'SELECT star, segment FROM weapon WHERE uid = "{uid}" AND wid = "{reward.value}";', **kwargs))[0]
		return common.mt(3, 'get segment',{'remaining' : {'weapon' : reward.value, 'star' : star, 'segment' : segment, 'cost_item' : item.value, 'cost_quantity' : remaining}, 'reward' : {'weapon' : reward.value, 'star' : 0, 'segment': 30, 'cost_item' : item.value, 'cost_quantity': cost}})

async def _response_factory_skill(uid, rewardgroup, new, reward, item, remaining, cost, **kwargs):
	if new:
		return common.mt(0, 'new skill unlocked', {'remaining' : {'skill' : reward.value, 'level' : 1, 'scroll_id' : -1, 'scroll_quantity' : -1, 'cost_item' : item.value, 'cost_quantity' : remaining}, 'reward' : {'skill' : reward.value, 'level' : 1, 'scroll_id' : -1, 'scroll_quantity' : -1, 'cost_item' : item.value, 'cost_quantity' : cost}})
	else:
		scroll_quantity = (await common.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = {reward.value};', **kwargs))[0][0]
		return common.mt(1, 'get scroll', {'remaining' : {'skill' : -1, 'level' : -1, 'scroll_id' : reward.value, 'scroll_quantity' : scroll_quantity, 'cost_item' : item.value, 'cost_quantity' : remaining}, 'reward' : {'skill' : -1, 'level' : -1, 'scroll_id' : reward.value, 'scroll_quantity' : 1, 'cost_item' : item.value, 'cost_quantity' : cost}})

async def _response_factory_role(uid, rewardgroup, new, reward, item, remaining, cost, **kwargs):
	if new:
		return common.mt(4, 'new role unlocked', {'remaining' : {'role' : reward.value, 'star' : 1, 'segment' : 0, 'cost_item' : item.value, 'cost_quantity' : remaining}, 'reward' : {'role' : reward.value, 'star' : 1, 'segment': 0, 'cost_item' : item.value, 'cost_quantity': cost}})
	else:
		star, segment = (await common.execute(f'SELECT star, segment FROM role WHERE uid = "{uid}" AND rid = "{reward.value}";', **kwargs))[0]
		return common.mt(5, 'get segment',{'remaining' : {'role' : reward.value, 'star' : star, 'segment' : segment, 'cost_item' : item.value, 'cost_quantity' : remaining}, 'reward' : {'role' : reward.value, 'star' : 0, 'segment': 30, 'cost_item' : item.value, 'cost_quantity': cost}})


SWITCH[enums.Group.WEAPON] = _response_factory_weapon
SWITCH[enums.Group.SKILL] = _response_factory_skill
SWITCH[enums.Group.ROLE] = _response_factory_role


# TODO 2019年12月19日
# ##################################################################
# ################### 2019年12月19日之后加入的方法 #################
# ##################################################################
GRID = 12


async def integral_convert(uid, **kwargs):
	"""积分兑换"""
	# TODO 限制条件检查
	_, integral = await common.try_item(uid, enums.Item.INTEGRAL, 0, **kwargs)
	acp = await _get_acp(uid, **kwargs)
	can, acp = _integral_inspect(acp, integral)
	if not can: return common.mt(99, 'insufficient materials')
	config = kwargs['config']['summon']['convert']
	await common.set_limit(uid, enums.Limits.INTEGRAL, acp, **kwargs)
	# TODO 奖励物品
	if acp in [200, 400, 600, 800]:
		mid = config['special']['mid'] if acp == 600 else random.choice(config['role']['mid'])
		can, rid = await lottery.try_unlock_role(uid, mid, **kwargs)
		status, msg = (0, 'You unlocked a role') if can else (1, 'You get 30 segments')
		value = lottery.STANDARD_SEG_COUNT
		remain_v = await common.try_role(uid, rid, 0, **kwargs)
		_, star = await role._get_role_info(uid, rid, 'star', **kwargs)
		return common.mt(status, msg, {'acp': acp, 'rid': mid, 'star': star[0], 'remain_seg': remain_v, 'reward_seg': value})
	else:  # 1000
		iid, value = config['item']['mid'], abs(config['item']['qty'])
		_, remain_v = await common.try_item(uid, enums.Item(iid), value, **kwargs)
		return common.mt(2, 'You get the universal segments', {'acp': acp, 'iid': iid, 'remain_v': remain_v, 'reward_v': value})


async def dozen_d(uid, **kwargs):
	"""钻石12抽，不足12次没有双倍积分，但可以连抽"""
	cid = enums.Item.DIAMOND
	grid = await _get_isb_count(uid, cid, isb=0, **kwargs)
	grid = grid if grid != 0 else (await _refresh(uid, cid, **kwargs), GRID)[1]
	isb_data = await _get_summon_isb(uid, cid, isb=0, **kwargs)
	# TODO 消耗物品
	consume_id, consume = enums.Item.SUMMON_SCROLL_D, grid
	can, qty = await common.try_item(uid, consume_id, -consume, **kwargs)
	if not can:
		consume_id, consume = cid, abs(kwargs['config']['summon']['resource'][cid.name]['qty']) * grid
		can, qty = await common.try_item(uid, consume_id, -consume, **kwargs)
		if not can: return common.mt(99, 'insufficient materials')
	# TODO 奖励物品
	multiple = grid * (1 if grid < GRID else 2)  # 计算抽奖获得的积分倍数
	data = {'remaining': [f'{enums.Group.ITEM.value}:{consume_id.value}:{qty}'], 'reward': [f'{enums.Group.ITEM.value}:{consume_id.value}:{consume}'], 'pid': [d[0] for d in isb_data]}
	article = [d[1] for d in isb_data]  # 获取所有的物品
	extra = [f'{r[:r.rfind(":")]}:{int(r[r.rfind(":") + 1:]) * multiple}' for r in kwargs['config']['summon']['resource'][cid.name]['reward']]  # 获取所有的额外物品
	items = f"{','.join(article)},{','.join(extra)}"
	results = await reward_items(uid, items, **kwargs)
	for gid, iid, remain_v, value in results:
		data['remaining'].append(f'{gid.value}:{iid.value}:{remain_v}')
		data['reward'].append(f'{gid.value}:{iid.value}:{value}')
	# TODO 重置所有物品
	reset = await _refresh(uid, cid, **kwargs)
	data['refresh'] = reset['data']['refresh']
	data['constraint'] = reset['data']['constraint']
	# TODO 完成任务
	await task.record(uid, enums.Task.PRO_SUMMONING, **kwargs)
	# TODO 完成成就
	await achievement.record(uid, enums.Achievement.PRO_SUMMON_TIMES, **kwargs)
	return common.mt(0, 'success', data=data)


async def dozen_c(uid, **kwargs):
	"""金币12抽，不足12次依然可以连抽，但受到次数限制"""
	cid = enums.Item.COIN
	grid = await _get_isb_count(uid, cid, isb=0, **kwargs)
	grid = grid if grid != 0 else (await _refresh(uid, cid, **kwargs), GRID)[1]
	isb_data = await _get_summon_isb(uid, cid, isb=0, **kwargs)
	# TODO 次数检查和限制
	now = datetime.now(tz=common.TZ_SH)
	tim = await common.get_timer(uid, enums.Timer.SUMMON_C, timeformat='%Y-%m-%d', **kwargs)
	lim = await common.get_limit(uid, enums.Limits.SUMMON_C, **kwargs)
	lim = (kwargs['config']['summon']['resource'][cid.name]['constraint']['times'] if lim is None or tim is None or tim < now else lim) - grid
	tim = (now + timedelta(days=1)) if tim is None or tim < now else tim
	if lim < 0: return common.mt(95, 'Insufficient number of lucky draw')
	await common.set_timer(uid, enums.Timer.SUMMON_C, tim, timeformat='%Y-%m-%d', **kwargs)
	await common.set_limit(uid, enums.Limits.SUMMON_C, lim, **kwargs)
	# TODO 消耗物品
	consume_id, consume = enums.Item.SUMMON_SCROLL_C, grid
	can, qty = await common.try_item(uid, consume_id, -consume, **kwargs)
	if not can:
		consume_id, consume = cid, abs(kwargs['config']['summon']['resource'][cid.name]['qty']) * grid
		can, qty = await common.try_item(uid, consume_id, -consume, **kwargs)
		if not can: return common.mt(99, 'insufficient materials')
	# TODO 奖励物品
	multiple = grid  # 计算抽奖获得的积分倍数
	data = {'remaining': [f'{enums.Group.ITEM.value}:{consume_id.value}:{qty}'], 'reward': [f'{enums.Group.ITEM.value}:{consume_id.value}:{consume}'], 'pid': [d[0] for d in isb_data]}
	article = [d[1] for d in isb_data]  # 获取所有的物品
	extra = [f'{r[:r.rfind(":")]}:{int(r[r.rfind(":") + 1:]) * multiple}' for r in kwargs['config']['summon']['resource'][cid.name]['reward']]  # 获取所有的额外物品
	items = f"{','.join(article)},{','.join(extra)}"
	results = await reward_items(uid, items, **kwargs)
	for gid, iid, remain_v, value in results:
		data['remaining'].append(f'{gid.value}:{iid.value}:{remain_v}')
		data['reward'].append(f'{gid.value}:{iid.value}:{value}')
	# TODO 重置所有物品
	reset = await _refresh(uid, cid, **kwargs)
	data['refresh'] = reset['data']['refresh']
	data['constraint'] = reset['data']['constraint']
	# TODO 完成任务
	await task.record(uid, enums.Task.BASIC_SUMMONING, **kwargs)
	return common.mt(0, 'success', data=data)


async def dozen_g(uid, **kwargs):
	"""朋友爱心12抽，不足12次依然可以连抽"""
	cid = enums.Item.FRIEND_GIFT
	grid = await _get_isb_count(uid, cid, isb=0, **kwargs)
	grid = grid if grid != 0 else (await _refresh(uid, cid, **kwargs), GRID)[1]
	isb_data = await _get_summon_isb(uid, cid, isb=0, **kwargs)
	# TODO 消耗物品
	consume_id, consume = cid, abs(kwargs['config']['summon']['resource'][cid.name]['qty']) * grid
	can, qty = await common.try_item(uid, consume_id, -consume, **kwargs)
	if not can: return common.mt(99, 'insufficient materials')
	# TODO 奖励物品
	multiple = grid  # 计算抽奖获得的积分倍数
	data = {'remaining': [f'{enums.Group.ITEM.value}:{consume_id.value}:{qty}'], 'reward': [f'{enums.Group.ITEM.value}:{consume_id.value}:{consume}'], 'pid': [d[0] for d in isb_data]}
	article = [d[1] for d in isb_data]  # 获取所有的物品
	extra = [f'{r[:r.rfind(":")]}:{int(r[r.rfind(":") + 1:]) * multiple}' for r in kwargs['config']['summon']['resource'][cid.name]['reward']]  # 获取所有的额外物品
	items = f"{','.join(article)},{','.join(extra)}"
	results = await reward_items(uid, items, **kwargs)
	for gid, iid, remain_v, value in results:
		data['remaining'].append(f'{gid.value}:{iid.value}:{remain_v}')
		data['reward'].append(f'{gid.value}:{iid.value}:{value}')
	# TODO 重置所有物品
	reset = await _refresh(uid, cid, **kwargs)
	data['refresh'] = reset['data']['refresh']
	data['constraint'] = reset['data']['constraint']
	return common.mt(0, 'success', data=data)


async def single_d(uid, **kwargs):
	"""钻石单抽"""
	cid = enums.Item.DIAMOND
	if await _get_isb_count(uid, cid, isb=0, **kwargs) == 0: await refresh_d(uid, **kwargs)  # 防止未刷新就调取这个方法
	isb_data = await _get_summon_isb(uid, cid, isb=0, **kwargs)
	# TODO 根据权重随机抽取奖励物品的pid, mid, wgt, isb信息
	isb_wgt = sum([d[2] for d in isb_data])  # 计算总权重值
	weights = [round(d[2]/isb_wgt, 2) for d in isb_data]
	weights[-1] = 1 - sum(weights[:-1])
	pid, mid, wgt, isb = random.choices(isb_data, weights=weights, k=1)[0]
	# TODO 次数检查和限制
	can, lim = await _refresh_lim(uid, cid, var=1, **kwargs)
	# TODO 消耗物品
	if can:
		await common.set_limit(uid, enums.Limits.SUMMON_D, lim, **kwargs)
		consume_id, consume = cid, 0 if lim == 1 else abs(kwargs['config']['summon']['resource'][cid.name]['qty']) // 2
		can, qty = await common.try_item(uid, consume_id, -consume, **kwargs)
	else:
		consume_id, consume = enums.Item.SUMMON_SCROLL_D, 1
		can, qty = await common.try_item(uid, consume_id, -consume, **kwargs)
		if not can:
			consume_id, consume = cid, abs(kwargs['config']['summon']['resource'][cid.name]['qty'])
			can, qty = await common.try_item(uid, consume_id, -consume, **kwargs)
	if not can:  # 材料不足恢复原来的次数
		await common.set_limit(uid, enums.Limits.SUMMON_D, lim - 1, **kwargs)
		return common.mt(99, 'insufficient materials')
	# TODO 奖励物品
	data = {'remaining': [f'{enums.Group.ITEM.value}:{consume_id.value}:{qty}'], 'reward': [f'{enums.Group.ITEM.value}:{consume_id.value}:{consume}'], 'pid': pid, 'constraint': {'limit': lim, 'cooling': common.remaining_cd()}}
	items = f"{mid},{','.join(kwargs['config']['summon']['resource'][cid.name]['reward'])}"
	results = await reward_items(uid, items, **kwargs)
	await _set_summon(uid, cid, pid, mid, wgt, 1, **kwargs)  # 设置物品已被购买过
	for gid, iid, remain_v, value in results:
		data['remaining'].append(f'{gid.value}:{iid.value}:{remain_v}')
		data['reward'].append(f'{gid.value}:{iid.value}:{value}')
	# TODO 完成任务
	await task.record(uid, enums.Task.PRO_SUMMONING, **kwargs)
	# TODO 完成成就
	await achievement.record(uid, enums.Achievement.PRO_SUMMON_TIMES, **kwargs)
	return common.mt(0, 'success', data=data)


async def single_c(uid, **kwargs):
	"""金币单抽"""
	cid = enums.Item.COIN
	if await _get_isb_count(uid, cid, isb=0, **kwargs) == 0: await refresh_c(uid, **kwargs)  # 防止未刷新就调取这个方法
	isb_data = await _get_summon_isb(uid, cid, isb=0, **kwargs)
	# TODO 根据权重随机抽取奖励物品的pid, mid, wgt, isb信息
	isb_wgt = sum([d[2] for d in isb_data])  # 计算总权重值
	weights = [round(d[2]/isb_wgt, 2) for d in isb_data]
	weights[-1] = 1 - sum(weights[:-1])
	pid, mid, wgt, isb = random.choices(isb_data, weights=weights, k=1)[0]
	# TODO 消耗低级代抽券
	consume_id, consume = enums.Item.SUMMON_SCROLL_C, 1
	c_can, qty = await common.try_item(uid, consume_id, -consume, **kwargs)
	# TODO 次数检查和限制
	can, lim = await _refresh_lim(uid, cid, var=0 if c_can else -1, **kwargs)
	if can is False: common.mt(95, 'Insufficient number of lucky draw')
	# TODO 消耗物品
	if not c_can:
		consume_id, consume = cid, abs(kwargs['config']['summon']['resource'][cid.name]['qty'])
		can, qty = await common.try_item(uid, consume_id, -consume, **kwargs)
		if not can:  # 材料不足恢复原来的次数
			await common.set_limit(uid, enums.Limits.SUMMON_C, lim + 1, **kwargs)
			return common.mt(99, 'insufficient materials')
	# TODO 奖励物品
	data = {'remaining': [f'{enums.Group.ITEM.value}:{consume_id.value}:{qty}'], 'reward': [f'{enums.Group.ITEM.value}:{consume_id.value}:{consume}'], 'pid': pid, 'constraint': {'limit': lim, 'cooling': common.remaining_cd()}}
	items = f"{mid},{','.join(kwargs['config']['summon']['resource'][cid.name]['reward'])}"
	results = await reward_items(uid, items, **kwargs)
	await _set_summon(uid, cid, pid, mid, wgt, 1, **kwargs)  # 设置物品已被购买过
	for gid, iid, remain_v, value in results:
		data['remaining'].append(f'{gid.value}:{iid.value}:{remain_v}')
		data['reward'].append(f'{gid.value}:{iid.value}:{value}')
	# TODO 完成任务
	await task.record(uid, enums.Task.BASIC_SUMMONING, **kwargs)
	return common.mt(0, 'success', data=data)


async def single_g(uid, **kwargs):
	"""朋友爱心单抽"""
	cid = enums.Item.FRIEND_GIFT
	if await _get_isb_count(uid, cid, isb=0, **kwargs) == 0: await refresh_g(uid, **kwargs)  # 防止未刷新就调取这个方法
	isb_data = await _get_summon_isb(uid, cid, isb=0, **kwargs)
	# TODO 根据权重随机抽取奖励物品的pid, mid, wgt, isb信息
	isb_wgt = sum([d[2] for d in isb_data])  # 计算总权重值
	weights = [round(d[2]/isb_wgt, 2) for d in isb_data]
	weights[-1] = 1 - sum(weights[:-1])
	pid, mid, wgt, isb = random.choices(isb_data, weights=weights, k=1)[0]
	# TODO 消耗物品
	consume = abs(kwargs['config']['summon']['resource'][cid.name]['qty'])
	can, qty = await common.try_item(uid, cid, -consume, **kwargs)
	if not can: return common.mt(99, 'insufficient materials')
	# TODO 奖励物品
	data = {'remaining': [f'{enums.Group.ITEM.value}:{cid.value}:{qty}'], 'reward': [f'{enums.Group.ITEM.value}:{cid.value}:{consume}'], 'pid': pid}
	items = f"{mid},{','.join(kwargs['config']['summon']['resource'][cid.name]['reward'])}"
	results = await reward_items(uid, items, **kwargs)
	await _set_summon(uid, cid, pid, mid, wgt, 1, **kwargs)  # 设置物品已被购买过
	for gid, iid, remain_v, value in results:
		data['remaining'].append(f'{gid.value}:{iid.value}:{remain_v}')
		data['reward'].append(f'{gid.value}:{iid.value}:{value}')
	return common.mt(0, 'success', data=data)


async def refresh_d(uid, **kwargs):
	"""刷新钻石抽奖市场方法"""
	end_time = await common.get_timer(uid, enums.Timer.SUMMON_D_END, **kwargs)
	current = datetime.now(tz=common.TZ_SH)
	cid = enums.Item.DIAMOND
	count = await _get_isb_count(uid, cid, isb=0, **kwargs)  # 获取未被抽中的数量
	if end_time is not None and end_time > current and count > 0:
		data = await _get_summon(uid, cid, **kwargs)
		refresh_data = [{'pid': d[0], 'mid': d[1], 'wgt': d[2], 'isb': d[3]} for d in data]
		config = kwargs['config']['summon']['resource'].get(cid.name, None)
		constraint = {'cid': cid.value, 'limit': (await _refresh_lim(uid, cid, **kwargs))[1], 'cooling_refresh': await _refresh_count_down(uid, cid, current, **kwargs)}
		constraint.update({'cooling': int((end_time - current).total_seconds()), 'qty': config['qty'], 'refresh': config['constraint']['refresh'], 'acp': await _get_acp(uid, **kwargs)})
		return common.mt(1, 'get all refresh info', {'refresh': refresh_data, 'constraint': constraint})
	return await _refresh(uid, cid, **kwargs)


async def refresh_c(uid, **kwargs):
	"""刷新金币抽奖市场方法"""
	end_time = await common.get_timer(uid, enums.Timer.SUMMON_C_END, **kwargs)
	current = datetime.now(tz=common.TZ_SH)
	cid = enums.Item.COIN
	count = await _get_isb_count(uid, cid, isb=0, **kwargs)  # 获取未被抽中的数量
	if end_time is not None and end_time > current and count > 0:
		data = await _get_summon(uid, cid, **kwargs)
		refresh_data = [{'pid': d[0], 'mid': d[1], 'wgt': d[2], 'isb': d[3]} for d in data]
		config = kwargs['config']['summon']['resource'].get(cid.name, None)
		constraint = {'cid': cid.value, 'limit': (await _refresh_lim(uid, cid, **kwargs))[1], 'cooling_refresh': await _refresh_count_down(uid, cid, current, **kwargs)}
		constraint.update({'cooling': int((end_time - current).total_seconds()), 'qty': config['qty'], 'refresh': config['constraint']['refresh'], 'acp': await _get_acp(uid, **kwargs)})
		return common.mt(1, 'get all refresh info', {'refresh': refresh_data, 'constraint': constraint})
	return await _refresh(uid, cid, **kwargs)


async def refresh_g(uid, **kwargs):
	"""刷新朋友爱心抽奖市场方法"""
	end_time = await common.get_timer(uid, enums.Timer.SUMMON_G_END, **kwargs)
	current = datetime.now(tz=common.TZ_SH)
	cid = enums.Item.FRIEND_GIFT
	count = await _get_isb_count(uid, cid, isb=0, **kwargs)  # 获取未被抽中的数量
	if end_time is not None and end_time > current and count > 0:
		data = await _get_summon(uid, cid, **kwargs)
		refresh_data = [{'pid': d[0], 'mid': d[1], 'wgt': d[2], 'isb': d[3]} for d in data]
		config = kwargs['config']['summon']['resource'].get(cid.name, None)
		constraint = {'cid': cid.value, 'cooling_refresh': await _refresh_count_down(uid, cid, current, **kwargs), 'acp': await _get_acp(uid, **kwargs)}
		constraint.update({'cooling': int((end_time - current).total_seconds()), 'qty': config['qty'], 'refresh': config['constraint']['refresh']})
		return common.mt(1, 'get all refresh info', {'refresh': refresh_data, 'constraint': constraint})
	return await _refresh(uid, cid, **kwargs)


async def buy_refresh(uid, cid, **kwargs):
	"""购买刷新,并获取所有刷新信息"""
	if cid not in BUY_REFRESH.keys(): return common.mt(94, 'cid error')
	now = datetime.now(tz=common.TZ_SH)
	tim = await common.get_timer(uid, BUY_REFRESH[cid], timeformat='%Y-%m-%d', **kwargs)
	# TODO 消耗物品
	consume, tim = (0, now + timedelta(days=1)) if tim is None or tim < now else (abs(kwargs['config']['summon']['resource'][cid.name]['constraint']['refresh']), tim)
	can, qty = await common.try_item(uid, enums.Item.DIAMOND, -consume, **kwargs)
	await common.set_timer(uid, BUY_REFRESH[cid], tim, timeformat='%Y-%m-%d', **kwargs)
	if not can: return common.mt(99, 'insufficient materials')
	# TODO 重构刷新的数据
	data = (await _refresh(uid, cid, **kwargs))['data']
	data['consume'] = {'remain_v': qty, 'value': consume}
	return common.mt(0, 'success', data)
# ############################# 私有方法 ###########################


async def _get_acp(uid, **kwargs):
	"""获取进度积分"""
	acp = await common.get_limit(uid, enums.Limits.INTEGRAL, **kwargs)
	return 0 if acp is None else acp


def _integral_inspect(lim, integral):
	for i in [200, 400, 600, 800, 1000]:
		if lim < i <= integral: return True, i
	return False, lim


async def reward_items(uid, items: str, **kwargs):
	"""返回奖励之后的改变情况"""
	decoded, results = common.decode_items(items), []
	for gid, iid, value in decoded:
		if gid == enums.Group.ITEM:
			_, remain_v = await common.try_item(uid, iid, value, **kwargs)
		elif gid == enums.Group.WEAPON:
			remain_v = await common.try_weapon(uid, iid, value, **kwargs)
		elif gid == enums.Group.SKILL:
			can, iid = await lottery.try_unlock_skill(uid, iid.value, **kwargs)
			gid, remain_v, value = (enums.Group.SKILL, 1, 1) if can else (enums.Group.ITEM, (await common.try_item(uid, iid, 0, **kwargs))[1], 1)
		elif gid == enums.Group.ROLE:
			remain_v = await common.try_role(uid, iid, value, **kwargs)
		else:
			print(f'不解析此组物品gid={gid},iid={iid}')
			remain_v = 0  # gid不属于以上四种情况时需要处理
		results.append((gid, iid, remain_v, value))
	return results


async def _refresh(uid, cid: enums, **kwargs):
	"""刷新抽奖市场方法，cid代表消耗品类型"""
	if cid not in SUMMON_SWITCH.keys(): return common.mt(94, 'cid error')
	now = datetime.now(tz=common.TZ_SH)
	constraint = {'cid': cid.value, 'cooling_refresh': await _refresh_count_down(uid, cid, now, **kwargs)}
	if cid in SUMMON_CONSTRAINT.keys():
		constraint['limit'] = (await _refresh_lim(uid, cid, **kwargs))[1]
	config = kwargs['config']['summon']['resource'].get(cid.name, None)
	if config is None: return common.mt(93, 'The configuration file does not exist')
	constraint.update({'qty': config['qty'], 'refresh': config['constraint']['refresh']})
	rds = []
	# grids = [i for i in range(config['constraint'].get('grid', GRID))]
	grids = [i for i in range(GRID)]
	random.shuffle(grids)
	goods = config['must']['goods']
	await random_summon(uid, cid, grids, goods, rds, 0, **kwargs)
	gdk = len(goods)
	k = len(grids) - gdk
	if k > 0:
		goods = random.choices(kwargs['config']['summon']['merchandise'], k=k)
		await random_summon(uid, cid, grids, goods, rds, gdk, **kwargs)
	hours = config['constraint']['hours']
	tim = await common.get_timer(uid, SUMMON_SWITCH[cid], **kwargs) or now
	cooling = int((tim - now).total_seconds())
	if cooling <= 0:
		cooling = hours * 3600
		end_time = now + timedelta(seconds=cooling)
		await common.set_timer(uid, SUMMON_SWITCH[cid], end_time, **kwargs)  # 设置玩家下次刷新的开始时间
	constraint['cooling'] = cooling
	constraint['acp'] = await _get_acp(uid, **kwargs)
	return common.mt(0, 'success', {'refresh': rds, 'constraint': constraint})


async def random_summon(uid, cid, grids, goods, rds, inc, **kwargs):
	for i, m in enumerate(goods):
		pid = grids[i + inc]
		mid = f'{m["gid"]}:{random.choice(m["mid"])}:{m["qty"]}'
		wgt = m['weight']
		await _set_summon(uid, cid, pid, mid, wgt, 0, **kwargs)
		rds.append({'pid': pid, 'mid': mid, 'wgt': wgt, 'isb': 0})


async def _refresh_lim(uid, cid, var=0, **kwargs):
	"""检查刷新钻石商城和金币商城的次数限制"""
	now = datetime.now(tz=common.TZ_SH)
	etm, elm, func = SUMMON_CONSTRAINT[cid]
	tim = await common.get_timer(uid, etm, timeformat='%Y-%m-%d', **kwargs)
	lim = await common.get_limit(uid, elm, **kwargs)
	lim, tim = (func(kwargs['config']['summon']['resource']) + var, now + timedelta(days=1)) if (lim is None or tim is None or tim < now) else (lim + var, tim)
	if cid == enums.Item.DIAMOND:
		if lim > 2: return False, lim
	else:  # enums.Item.COIN
		if lim < 0: return False, lim
	await common.set_timer(uid, etm, tim, timeformat='%Y-%m-%d', **kwargs)
	await common.set_limit(uid, elm, lim, **kwargs)
	return True, lim


async def _refresh_count_down(uid, cid, now, **kwargs) -> int:
	"""返回下次刷新需要的秒钟数"""
	tim = await common.get_timer(uid, BUY_REFRESH[cid], timeformat='%Y-%m-%d', **kwargs)
	tim = now if tim is None else tim
	return int((tim - now).total_seconds())


async def _get_isb_count(uid, cid, isb=0, **kwargs):
	return (await common.execute(f'SELECT COUNT(*) FROM summon WHERE uid = "{uid}" AND cid = {cid} AND isb = {isb};', **kwargs))[0][0]


async def _get_summon_isb(uid, cid, isb=0, **kwargs):
	return await common.execute(f'SELECT pid, mid, wgt, isb FROM summon WHERE uid = "{uid}" AND cid = {cid} AND isb = {isb};', **kwargs)


async def _get_summon(uid, cid, **kwargs):
	return await common.execute(f'SELECT pid, mid, wgt, isb FROM summon WHERE uid = "{uid}" AND cid = {cid};', **kwargs)


async def _set_summon(uid, cid, pid, mid, wgt, isb, **kwargs):
	await common.execute(f'INSERT INTO summon (uid, cid, pid, mid, wgt, isb) VALUES ("{uid}", {cid}, {pid}, "{mid}", {wgt}, {isb}) ON DUPLICATE KEY UPDATE `mid`= VALUES(`mid`), `wgt`= VALUES(`wgt`), `isb`= VALUES(`isb`);', **kwargs)


async def refresh_integral(uid, **kwargs):
	"""用于刷新积分的所有情况"""
	timer = await common.get_timer(uid, enums.Timer.INTEGRAL, timeformat='%Y-%m-%d', **kwargs)
	now = datetime.now(tz=common.TZ_SH)
	timer = now if timer is None else timer
	if timer.isocalendar()[1] != now.isocalendar()[1]:
		await asyncio.gather(
			common.execute(f'INSERT INTO item (uid, iid, value) VALUES ("{uid}", {enums.Item.INTEGRAL}, 0) ON DUPLICATE KEY UPDATE `value` = 0;', **kwargs),
			common.set_timer(uid, enums.Timer.INTEGRAL, now, timeformat='%Y-%m-%d', **kwargs),
			common.set_limit(uid, enums.Limits.INTEGRAL, 0, **kwargs)
		)
	elif timer == now:
		await common.set_timer(uid, enums.Timer.INTEGRAL, timer, timeformat='%Y-%m-%d', **kwargs)


SUMMON_SWITCH = {
	enums.Item.DIAMOND:     enums.Timer.SUMMON_D_END,
	enums.Item.COIN:        enums.Timer.SUMMON_C_END,
	enums.Item.FRIEND_GIFT: enums.Timer.SUMMON_G_END,
}

SUMMON_CONSTRAINT = {
	enums.Item.DIAMOND:     (enums.Timer.SUMMON_D, enums.Limits.SUMMON_D, lambda config: 0),
	enums.Item.COIN:        (enums.Timer.SUMMON_C, enums.Limits.SUMMON_C, lambda config: config['COIN']['constraint']['times']),
}

BUY_REFRESH = {
	enums.Item.DIAMOND:     enums.Timer.SUMMON_D_REFRESH,
	enums.Item.COIN:        enums.Timer.SUMMON_C_REFRESH,
	enums.Item.FRIEND_GIFT: enums.Timer.SUMMON_G_REFRESH,
}
