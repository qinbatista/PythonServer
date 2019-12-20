'''
summoning.py
'''

from module import enums
from module import common
from module import lottery
from module import task
from module import achievement
import random
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


# ############################# 私有方法 ###########################


async def refresh_d(uid, **kwargs):
	"""刷新钻石抽奖市场方法"""
	# TODO 1.消耗操作
	# TODO 2.奖励积分操作
	return await _refresh(uid, str(enums.Item.DIAMOND.value), **kwargs)


async def refresh_c(uid, **kwargs):
	"""刷新金币抽奖市场方法"""
	# TODO 1.消耗操作
	# TODO 2.奖励积分操作
	return await _refresh(uid, str(enums.Item.COIN.value), **kwargs)


async def refresh_g(uid, **kwargs):
	"""刷新朋友爱心抽奖市场方法"""
	# TODO 1.消耗操作
	# TODO 2.奖励积分操作
	return await _refresh(uid, str(enums.Item.FRIEND_GIFT.value), **kwargs)


async def _refresh(uid, cid: str, **kwargs):
	"""刷新抽奖市场方法，cid代表消耗品类型5, 1, 16"""
	if cid not in ['5', '1', '16']: return common.mt(99, 'cid错误')
	config = kwargs['config']['summon']['resource'].get(cid, None)
	if config is None: return common.mt(98, '配置文件不存在')
	data = []
	grids = [i for i in range(config['constraint'].get('grid', 12))]
	random.shuffle(grids)
	goods = config['must']['goods']
	goods_qty = len(goods)
	if len(grids) >= goods_qty:
		for i, m in enumerate(goods):
			pid = grids[i]
			mid = f'{m["gid"]}:{random.choice(m["mid"])}:{m["qty"]}'
			wgt = m['weight']
			await _set_summon(uid, cid, pid, mid, wgt, 0, **kwargs)
			data.append({'cid': cid, 'pid': pid, 'mid': mid, 'wgt': wgt, 'isb': 0})
		optional = random.choices(kwargs['config']['summon']['merchandise'], k=len(grids) - goods_qty)
		for i, m in enumerate(optional):
			pid = grids[goods_qty + i]
			mid = f'{m["gid"]}:{random.choice(m["mid"])}:{m["qty"]}'
			wgt = m['weight']
			await _set_summon(uid, cid, pid, mid, wgt, 0, **kwargs)
			data.append({'cid': cid, 'pid': pid, 'mid': mid, 'wgt': wgt, 'isb': 0})
	else:
		for i, pid in enumerate(grids):
			m = goods[i]
			mid = f'{m["gid"]}:{random.choice(m["mid"])}:{m["qty"]}'
			wgt = m['weight']
			await _set_summon(uid, cid, pid, mid, wgt, 0, **kwargs)
			data.append({'cid': cid, 'pid': pid, 'mid': mid, 'wgt': wgt, 'isb': 0})
	return common.mt(0, 'success', {'refresh': data})


async def _set_summon(uid, cid, pid, mid, wgt, isb, **kwargs):
	await common.execute_update(f'INSERT INTO summon (uid, cid, pid, mid, wgt, isb) VALUES ("{uid}", {cid}, {pid}, "{mid}", {wgt}, {isb}) ON DUPLICATE KEY UPDATE `mid`= VALUES(`mid`), `wgt`= VALUES(`wgt`), `isb`= VALUES(`isb`);', **kwargs)

