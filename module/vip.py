'''
vip.py
'''

import asyncio

from module import enums
from module import common


async def get_config(uid, **kwargs):
	"""返回VIP的配置信息"""
	return common.mt(0, 'success', {'config': kwargs['config']['vip']})


async def get_daily_reward(uid, wid, amount, **kwargs):
	"""获得VIP每日奖励"""
	pass


async def buy_package(uid, wid, amount, **kwargs):
	"""购买VIP礼包，VIP等级以下的可以购买"""
	pass


async def buy_card(uid, wid, amount, **kwargs):
	"""购买VIP卡，分为小月卡、大月卡、永久月卡
	 小月卡：登录领取VIP每日奖励获得VIP经验10点，一个月的过期期限
	 大月卡：登录领取VIP每日奖励获得VIP经验15点，一个月的过期期限
	 永久月卡：登录领取VIP每日奖励获得VIP经验20点，无过期期限
	 TODO 人民币购买
	 """
	pass


####################################################################################
async def increase_exp(uid, exp, **kwargs):
	"""增加VIP经验
	exp为0则获得经验，反之取绝对值增加经验，
	并返回总经验和等级，升到下一级需要的经验
	"""
	exp_config = kwargs['config']['vip']
	exp_data = await common.execute(f'SELECT exp FROM progress WHERE uid = "{uid}";', **kwargs)
	if exp_data == ():
		await common.execute(f'INSERT INTO progress (uid) VALUE ("{uid}");', **kwargs)
		return False, {'exp': 0, 'level': 0, 'need': 0}
	exp_s = exp_data[0][0]
	exp_list = [e for e in exp_config if e > exp_s]
	if exp == 0: return True, {'exp': exp_s, 'level': exp_config.index(exp_list[0]) if exp_list != [] else len(exp_config), 'need': exp_list[0] - exp_s if exp_list != [] else 0}
	exp_s += exp
	await common.execute_update(f'UPDATE progress SET exp = {exp_s} WHERE uid = "{uid}";', **kwargs)
	return True, {'exp': exp_s, 'level': exp_config.index(exp_list[0]) if exp_list != [] else len(exp_config), 'need': exp_list[0] - exp_s if exp_list != [] else 0}





