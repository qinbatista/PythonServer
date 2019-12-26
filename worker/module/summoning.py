'''
summoning.py
'''

from module import enums
from module import common
from module import lottery
from module import task
from module import achievement
import random
from datetime import datetime, timedelta
# Tier
# basic, friend, pro, prophet
# RewardGroup
# weapon, skill, role

SWITCH = {}

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

	kwargs.update({"aid":enums.Achievement.SUMMON_TIMES})
	await achievement.record_achievement(kwargs['data']['unique_id'],**kwargs)

	if enums.Tier.BASIC == tier:
		kwargs.update({"task_id":enums.Task.BASIC_SUMMONING})
		await task.record_task(uid,**kwargs)
	if enums.Tier.PRO == tier:
		kwargs.update({"task_id":enums.Task.PRO_SUMMONING})
		await task.record_task(uid,**kwargs)
		kwargs.update({"aid":enums.Achievement.PRO_SUMMON_TIMES})
		await achievement.record_achievement(kwargs['data']['unique_id'],**kwargs)

	return await _response_factory(uid, rewardgroup, new, reward, item, remaining, cost, **kwargs)

async def _base_summon_multi(uid, item, tier, rewardgroup, num_times, **kwargs):
	if f'{enums.Group.ITEM.value}:{item.value}' not in kwargs['config']['lottery']['random_gift'][rewardgroup.name]['cost'][tier.name].keys(): return common.mt(98, f'error item:{item}')
	cost = kwargs['config']['lottery']['random_gift'][rewardgroup.name]['cost'][tier.name][f'{enums.Group.ITEM.value}:{item.value}']
	can_pay, remaining = await common.try_item(uid, item, -cost * num_times, **kwargs)
	if not can_pay: return common.mt(99, 'insufficient materials')
	response = {'remaining' : {}, 'reward' : {}}
	for time in range(num_times):

		if enums.Tier.BASIC == tier:
			kwargs.update({"task_id":enums.Task.BASIC_SUMMONING})
			await task.record_task(uid,**kwargs)
		if enums.Tier.PRO == tier:
			kwargs.update({"task_id":enums.Task.PRO_SUMMONING})
			await task.record_task(uid,**kwargs)
			kwargs.update({"aid":enums.Achievement.PRO_SUMMON_TIMES})
			await achievement.record_achievement(kwargs['data']['unique_id'],**kwargs)

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


async def dozen_d(uid, **kwargs):
	"""钻石12抽"""
	cid = enums.Item.DIAMOND
	if await _get_isb_count(uid, cid, isb=0, **kwargs) < GRID: return common.mt(98, f'Less than {GRID} grid')
	isb_data = await _get_summon_isb(uid, cid, isb=0, **kwargs)
	# TODO 消耗物品
	consume = abs(kwargs['config']['summon']['resource'][cid.name]['qty']) * GRID
	can, qty = await common.try_item(uid, cid, -consume, **kwargs)
	if not can: return common.mt(99, 'diamond insufficient')
	# TODO 奖励物品
	data = {'remaining': [f'{enums.Group.ITEM.value}:{cid.value}:{qty}'], 'reward': [f'{enums.Group.ITEM.value}:{cid.value}:{consume}'], 'pid': [d[0] for d in isb_data]}
	article = [d[1] for d in isb_data]  # 获取所有的物品
	extra = [f'{r[:r.rfind(":")]}:{int(r[r.rfind(":") + 1:]) * GRID * 2}' for r in kwargs['config']['summon']['resource'][cid.name]['reward']]  # 获取所有的额外物品
	items = f"{','.join(article)},{','.join(extra)}"
	results = await _summon_reward(uid, items, **kwargs)
	for gid, iid, remain_v, value in results:
		data['remaining'].append(f'{gid.value}:{iid.value}:{remain_v}')
		data['reward'].append(f'{gid.value}:{iid.value}:{value}')
	# TODO 重置所有物品
	reset = await _refresh(uid, cid, **kwargs)
	data['refresh'] = reset['data']['refresh']
	data['cooling'] = reset['data']['cooling']
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
	# TODO 消耗物品
	consume = abs(kwargs['config']['summon']['resource'][cid.name]['qty'])
	grid = len(isb_data)
	consume = 0 if grid == GRID else (consume//2 if grid == GRID - 1 else consume)
	can, qty = await common.try_item(uid, cid, -consume, **kwargs)
	if not can: return common.mt(99, 'diamond insufficient')
	# TODO 奖励物品
	data = {'remaining': [f'{enums.Group.ITEM.value}:{cid.value}:{qty}'], 'reward': [f'{enums.Group.ITEM.value}:{cid.value}:{consume}'], 'pid': pid}
	items = f"{mid},{','.join(kwargs['config']['summon']['resource'][cid.name]['reward'])}"
	results = await _summon_reward(uid, items, **kwargs)
	await _set_summon(uid, cid, pid, mid, wgt, 1, **kwargs)  # 设置物品已被购买过
	for gid, iid, remain_v, value in results:
		data['remaining'].append(f'{gid.value}:{iid.value}:{remain_v}')
		data['reward'].append(f'{gid.value}:{iid.value}:{value}')
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
	# TODO 消耗物品
	consume = abs(kwargs['config']['summon']['resource'][cid.name]['qty'])
	can, qty = await common.try_item(uid, cid, -consume, **kwargs)
	if not can: return common.mt(99, 'coin insufficient')
	# TODO 奖励物品
	data = {'remaining': [f'{enums.Group.ITEM.value}:{cid.value}:{qty}'], 'reward': [f'{enums.Group.ITEM.value}:{cid.value}:{consume}'], 'pid': pid}
	items = f"{mid},{','.join(kwargs['config']['summon']['resource'][cid.name]['reward'])}"
	results = await _summon_reward(uid, items, **kwargs)
	await _set_summon(uid, cid, pid, mid, wgt, 1, **kwargs)  # 设置物品已被购买过
	for gid, iid, remain_v, value in results:
		data['remaining'].append(f'{gid.value}:{iid.value}:{remain_v}')
		data['reward'].append(f'{gid.value}:{iid.value}:{value}')
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
	if not can: return common.mt(99, 'friend gift insufficient')
	# TODO 奖励物品
	data = {'remaining': [f'{enums.Group.ITEM.value}:{cid.value}:{qty}'], 'reward': [f'{enums.Group.ITEM.value}:{cid.value}:{consume}'], 'pid': pid}
	items = f"{mid},{','.join(kwargs['config']['summon']['resource'][cid.name]['reward'])}"
	results = await _summon_reward(uid, items, **kwargs)
	await _set_summon(uid, cid, pid, mid, wgt, 1, **kwargs)  # 设置物品已被购买过
	for gid, iid, remain_v, value in results:
		data['remaining'].append(f'{gid.value}:{iid.value}:{remain_v}')
		data['reward'].append(f'{gid.value}:{iid.value}:{value}')
	return common.mt(0, 'success', data=data)


async def refresh_d(uid, **kwargs):
	"""刷新钻石抽奖市场方法"""
	end_time = await common.get_timer(uid, enums.Timer.SUMMON_D_END, **kwargs)
	current  = datetime.now(tz=common.TZ_SH)
	cid = enums.Item.DIAMOND
	count = await _get_isb_count(uid, cid, isb=0, **kwargs)  # 获取未被抽中的数量
	if end_time is not None and end_time > current and count > 0:
		data = await _get_summon(uid, cid, **kwargs)
		refresh_data = [{'cid': cid.value, 'pid': d[0], 'mid': d[1], 'wgt': d[2], 'isb': d[3]} for d in data]
		return common.mt(1, 'get all refresh info', {'refresh': refresh_data, 'cooling': int((end_time - current).total_seconds())})
	return await _refresh(uid, cid, **kwargs)


async def refresh_c(uid, **kwargs):
	"""刷新金币抽奖市场方法"""
	end_time = await common.get_timer(uid, enums.Timer.SUMMON_C_END, **kwargs)
	current  = datetime.now(tz=common.TZ_SH)
	cid = enums.Item.COIN
	count = await _get_isb_count(uid, cid, isb=0, **kwargs)  # 获取未被抽中的数量
	if end_time is not None and end_time > current and count > 0:
		data = await _get_summon(uid, cid, **kwargs)
		refresh_data = [{'cid': cid.value, 'pid': d[0], 'mid': d[1], 'wgt': d[2], 'isb': d[3]} for d in data]
		return common.mt(1, 'get all refresh info', {'refresh': refresh_data, 'cooling': int((end_time - current).total_seconds())})
	return await _refresh(uid, cid, **kwargs)


async def refresh_g(uid, **kwargs):
	"""刷新朋友爱心抽奖市场方法"""
	end_time = await common.get_timer(uid, enums.Timer.SUMMON_G_END, **kwargs)
	current  = datetime.now(tz=common.TZ_SH)
	cid = enums.Item.FRIEND_GIFT
	count = await _get_isb_count(uid, cid, isb=0, **kwargs)  # 获取未被抽中的数量
	if end_time is not None and end_time > current and count > 0:
		data = await _get_summon(uid, cid, **kwargs)
		refresh_data = [{'cid': cid.value, 'pid': d[0], 'mid': d[1], 'wgt': d[2], 'isb': d[3]} for d in data]
		return common.mt(1, 'get all refresh info', {'refresh': refresh_data, 'cooling': int((end_time - current).total_seconds())})
	return await _refresh(uid, cid, **kwargs)

# ############################# 私有方法 ###########################


async def _summon_reward(uid, items: str, **kwargs):
	"""返回奖励之后的改变情况"""
	decoded = common.decode_items(items)
	results = []
	for gid, iid, value in decoded:
		if gid == enums.Group.ITEM:
			_, remain_v = await common.try_item(uid, iid, value, **kwargs)
		elif gid == enums.Group.WEAPON:
			remain_v = await common.try_weapon(uid, iid, value, **kwargs)
		elif gid == enums.Group.SKILL:
			can, iid = await lottery._try_unlock_skill(uid, iid.value, **kwargs)
			gid, remain_v, value = (enums.Group.SKILL, 1, 1) if can else (enums.Group.ITEM, (await common.try_item(uid, iid, 0, **kwargs))[1], 1)
		elif gid == enums.Group.ROLE:
			remain_v = await common.try_role(uid, iid, value, **kwargs)
		else:
			remain_v = -1  # gid不属于以上四种情况时需要处理
		results.append((gid, iid, remain_v, value))
	return results


async def _refresh(uid, cid: enums, **kwargs):
	"""刷新抽奖市场方法，cid代表消耗品类型"""
	if cid not in SUMMON_SWITCH.keys(): return common.mt(99, 'cid error')
	config = kwargs['config']['summon']['resource'].get(cid.name, None)
	if config is None: return common.mt(98, 'The configuration file does not exist')
	data = []
	# grids = [i for i in range(config['constraint'].get('grid', GRID))]
	grids = [i for i in range(GRID)]
	random.shuffle(grids)
	goods = config['must']['goods']
	goods_qty = len(goods)
	if len(grids) >= goods_qty:
		for i, m in enumerate(goods):
			pid = grids[i]
			mid = f'{m["gid"]}:{random.choice(m["mid"])}:{m["qty"]}'
			wgt = m['weight']
			await _set_summon(uid, cid, pid, mid, wgt, 0, **kwargs)
			data.append({'cid': cid.value, 'pid': pid, 'mid': mid, 'wgt': wgt, 'isb': 0})
		optional = random.choices(kwargs['config']['summon']['merchandise'], k=len(grids) - goods_qty)
		for i, m in enumerate(optional):
			pid = grids[goods_qty + i]
			mid = f'{m["gid"]}:{random.choice(m["mid"])}:{m["qty"]}'
			wgt = m['weight']
			await _set_summon(uid, cid, pid, mid, wgt, 0, **kwargs)
			data.append({'cid': cid.value, 'pid': pid, 'mid': mid, 'wgt': wgt, 'isb': 0})
	else:
		for i, pid in enumerate(grids):
			m = goods[i]
			mid = f'{m["gid"]}:{random.choice(m["mid"])}:{m["qty"]}'
			wgt = m['weight']
			await _set_summon(uid, cid, pid, mid, wgt, 0, **kwargs)
			data.append({'cid': cid.value, 'pid': pid, 'mid': mid, 'wgt': wgt, 'isb': 0})
	hours = config['constraint']['hours']
	end_time = datetime.now(tz=common.TZ_SH) + timedelta(hours=hours)
	await common.set_timer(uid, SUMMON_SWITCH[cid], end_time, **kwargs)  # 设置玩家下次刷新的开始时间
	return common.mt(0, 'success', {'refresh': data, 'cooling': hours * 3600})


async def _get_isb_count(uid, cid, isb=0, **kwargs):
	return (await common.execute(f'SELECT COUNT(*) FROM summon WHERE uid = "{uid}" AND cid = {cid} AND isb = {isb};', **kwargs))[0][0]


async def _get_summon_isb(uid, cid, isb=0, **kwargs):
	return await common.execute(f'SELECT pid, mid, wgt, isb FROM summon WHERE uid = "{uid}" AND cid = {cid} AND isb = {isb};', **kwargs)


async def _get_summon(uid, cid, **kwargs):
	return await common.execute(f'SELECT pid, mid, wgt, isb FROM summon WHERE uid = "{uid}" AND cid = {cid};', **kwargs)


async def _set_summon(uid, cid, pid, mid, wgt, isb, **kwargs):
	await common.execute(f'INSERT INTO summon (uid, cid, pid, mid, wgt, isb) VALUES ("{uid}", {cid}, {pid}, "{mid}", {wgt}, {isb}) ON DUPLICATE KEY UPDATE `mid`= VALUES(`mid`), `wgt`= VALUES(`wgt`), `isb`= VALUES(`isb`);', **kwargs)


SUMMON_SWITCH = {
	enums.Item.DIAMOND:     enums.Timer.SUMMON_D_END,
	enums.Item.COIN:        enums.Timer.SUMMON_C_END,
	enums.Item.FRIEND_GIFT: enums.Timer.SUMMON_G_END,
}

