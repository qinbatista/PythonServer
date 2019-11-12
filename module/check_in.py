'''
task.py
'''
from datetime import datetime, timedelta
from module import enums
from module import common
import time
from module import lottery
from module import achievement
from module import task
async def supplement_check_in(uid, **kwargs):
	"""补签"""
	# 0 - Successful signing
	# 98 - You have completed all current check-ins
	# 99 - Insufficient diamond
	month_pre = time.strftime('%Y-%m-', time.localtime())  # 获取每月需要补签的日期前缀
	data = await common.execute(f'select date from check_in where uid="{uid}" and date like "{month_pre}%"',**kwargs)
	today_number = datetime.today().day
	missing_days = today_number - len(data)
	if missing_days == 0:return common.mt(98, 'no day missing')
	isok, diamond = await common.try_item(uid, enums.Item.DIAMOND, -missing_days * kwargs["config"]["patch_diamond"], **kwargs)
	if isok == False:return common.mt(99, 'Insufficient diamond')
	check_data={}
	for i in range(1,today_number):
		kwargs.update({"hard_day": f'{"" if i > 9 else "0"}{i}'})
		result = await check_in(uid,**kwargs)
		check_data.update({i: result["data"]})
	return common.mt(0, 'Successful signing', data={'supplement': check_data, 'remaining': {'diamond': diamond}, 'reward': {'diamond': missing_days * kwargs["config"]["patch_diamond"]}})

async def check_in(uid, **kwargs):
	"""每日签到"""
	# 0 - Sign-in success
	# 99 - You have already signed in today
	kwargs.update({"tid": enums.Task.CHECK_IN})
	await task.record_task(uid,**kwargs)
	current_time = time.strftime('%Y-%m-'+str(kwargs["hard_day"]), time.localtime()) if kwargs.__contains__("hard_day") else time.strftime('%Y-%m-%d', time.localtime())
	s_data = await common.execute( f'select * from check_in where uid="{uid}" and date="{current_time}"', **kwargs)
	if s_data != ():return common.mt(99, 'You have already signed in today')
	which_day = int(current_time[-2:])%7
	item_set = kwargs["config"][str(which_day)].split(":")
	vip_exp  = kwargs["vip_exp"]["vip_level"]["experience"]
	my_exp = await common.get_vip_exp(uid,**kwargs)
	for i, exp in enumerate(vip_exp):
		if my_exp <= exp:
			vip_level = i
			break
	vip_bond =1 if which_day >= vip_level else 2
	if int(item_set[0])==enums.Group.ITEM.value: _, quantity = await common.try_item(   uid, enums.Item(int(item_set[1])),   vip_bond*int(item_set[2]), **kwargs)
	if int(item_set[0])==enums.Group.WEAPON.value:  quantity = await common.try_weapon( uid, enums.Weapon(int(item_set[1])), vip_bond*int(item_set[2]), **kwargs)
	if int(item_set[0])==enums.Group.ROLE.value:    quantity = await common.try_role(   uid, enums.Role(int(item_set[1])),   vip_bond*int(item_set[2]), **kwargs)
	await common.execute_update( f'insert into check_in(uid, date, reward) values("{uid}", "{current_time}", 1)',**kwargs)
	return common.mt(0, 'Sign-in success',{"remaining":[f'{item_set[0]}:{enums.Item(int(item_set[1]))}:{quantity}'],"reward":[f'{item_set[0]}:{enums.Item(int(item_set[1]))}:{vip_bond*int(item_set[2])}']})

async def get_all_check_in_table(uid, **kwargs):
	"""获取所有签到情况"""
	# 0 - Successfully obtained all check-in status
	data = await common.execute( f'select * from check_in where uid="{uid}" and date like "{time.strftime("%Y-%m-", time.localtime())}%"',**kwargs)
	remaining = {}
	for d in data:
		remaining.update({int(d[1][-2:]): {'date': d[1], 'reward': d[2]}})
	seconds = int((datetime.strptime((datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d 00:00:00'), '%Y-%m-%d %H:%M:%S') - datetime.now()).total_seconds())
	return common.mt(0, 'Successfully obtained all check-in status this month', data={'today': datetime.today().day, 'time': f'{seconds//3600}:{"0" if seconds%3600//60 < 10 else ""}{seconds%3600//60}:{"0" if seconds%60 < 10 else ""}{seconds%60}', 'remaining': remaining, 'config': kwargs['config']})