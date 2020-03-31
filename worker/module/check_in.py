'''
task.py
'''
from datetime import datetime, timedelta
from module import enums
from module import common
from module import vip
from module import lottery
from module import achievement
from module import task


async def supplement_check_in(uid, **kwargs):
	"""补签"""
	# 0 - Successful signing
	# 98 - You have completed all current check-ins
	# 99 - Insufficient diamond
	config = kwargs['config']['check_in']
	now = datetime.now(common.TZ_SH)
	today = now.day
	month_pre = now.strftime('%Y-%m-')
	nd = await common.execute(f'select date from check_in where uid="{uid}" and date like "{month_pre}%"', **kwargs)
	lacks = today - len(nd)
	if lacks == 0: return common.mt(98, 'no day missing')
	can, diamond = await common.try_item(uid, enums.Item.DIAMOND, -lacks * config["patch_diamond"], **kwargs)
	if not can: return common.mt(99, 'Insufficient diamond')
	checks = {}
	for day in range(1, today):
		day = f'{"" if day > 9 else "0"}{day}'
		result = await check_in(uid, day, **kwargs)
		checks.update({day: result["data"]})
	return common.mt(0, 'Successful signing', data={'supplement': checks, 'remaining': {'diamond': diamond},
													'reward': {'diamond': lacks * config["patch_diamond"]}})


async def check_in(uid, day=None, **kwargs):
	"""每日签到"""
	# 0 - Sign-in success
	# 99 - You have already signed in today
	kwargs.update({"task_id": enums.Task.CHECK_IN})
	await task.record_task(uid, **kwargs)

	kwargs.update({"aid":enums.Achievement.TOTAL_LOGIN})
	await achievement.record_achievement(uid,**kwargs)

	now = datetime.now(common.TZ_SH)
	today = now.day
	_now = now.strftime('%Y-%m-%d' if day is None else f'%Y-%m-{day}')
	nd = await common.execute(f'select * from check_in where uid="{uid}" and date="{_now}"', **kwargs)
	if nd != (): return common.mt(99, 'You have already signed in today')
	which_day = today % 7
	item_set = kwargs["check_in_config"][f'{which_day}'].split(":")
	vip_info = await vip.increase_exp(uid, 10, **kwargs)
	vip_bond = 1 if which_day >= vip_info['level'] else 2
	gid = enums.Group(int(item_set[0]))
	if gid == enums.Group.ITEM: _, quantity = await common.try_item(uid, enums.Item(int(item_set[1])), vip_bond * int(item_set[2]), **kwargs)
	if gid == enums.Group.WEAPON:  quantity = await common.try_weapon(uid, enums.Weapon(int(item_set[1])), vip_bond * int(item_set[2]), **kwargs)
	if gid == enums.Group.ROLE:    quantity = await common.try_role(uid, enums.Role(int(item_set[1])), vip_bond * int(item_set[2]), **kwargs)
	await common.execute_update(f'insert into check_in(uid, date, reward) values("{uid}", "{_now}", 1)', **kwargs)
	return common.mt(0, 'Sign-in success', {"remaining": [f'{item_set[0]}:{item_set[1]}:{quantity}'], "reward": [f'{item_set[0]}:{item_set[1]}:{vip_bond*int(item_set[2])}']})


async def get_all_check_in_table(uid, **kwargs):
	"""获取所有签到情况"""
	# 0 - Successfully obtained all check-in status
	data = await common.execute(f'select * from check_in where uid="{uid}" and date like "{datetime.now(common.TZ_SH).strftime("%Y-%m-")}%"', **kwargs)
	remaining = {}
	for d in data:
		remaining.update({d[1][-2:]: {'date': d[1], 'reward': d[2]}})
	seconds = common.remaining_cd()
	return common.mt(0, 'Successfully obtained all check-in status this month', data={'today': datetime.now(common.TZ_SH).day, 'time': f'{seconds//3600}:{"0" if seconds%3600//60 < 10 else ""}{seconds%3600//60}:{"0" if seconds%60 < 10 else ""}{seconds%60}', 'remaining': remaining, 'config': kwargs['config']})
