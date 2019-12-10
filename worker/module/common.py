'''
common.py

Contains definitions of commonly used generic functions.
When desinging a function, try to make it as general as possible to allow the reuse of code.
'''
from module import enums
from module import mail
import time
import calendar
from datetime import datetime, timedelta
from dateutil import tz
TZ_SH = tz.gettz('Asia/Shanghai')


async def exists(table, *conditions, account = False, **kwargs):
	condition = ' AND '.join([f'`{cond[0]}` = "{cond[1]}"' for cond in conditions])
	data = await execute(f'SELECT EXISTS (SELECT 1 FROM {table} WHERE {condition});', account, **kwargs)
	if data == () or () in data: return False
	return data[0][0] != 0

async def execute(statement, account=False, mall=False, exchange=False, **kwargs):
	async with ((((await get_db(**kwargs)).acquire() if not account
			else kwargs['accountdb'].acquire()) if not mall
			else kwargs['malldb'].acquire()) if not exchange
			else kwargs['exchangedb'].acquire()) as conn:
		if not account and not mall and not exchange:
			await conn.select_db(str(kwargs['world']))
		async with conn.cursor() as cursor:
			await cursor.execute(statement)
			return await cursor.fetchall()

async def execute_update(statement, account=False, mall=False, exchange=False, **kwargs):
	async with ((((await get_db(**kwargs)).acquire() if not account
			else kwargs['accountdb'].acquire()) if not mall
			else kwargs['malldb'].acquire()) if not exchange
			else kwargs['exchangedb'].acquire()) as conn:
		if not account and not mall and not exchange:
			await conn.select_db(str(kwargs['world']))
		async with conn.cursor() as cursor:
			affected = await cursor.execute(statement)
			return (affected, await cursor.fetchall())

async def get_gn(uid, **kwargs):
	data = await execute(f'SELECT gn FROM player WHERE uid = "{uid}";', **kwargs)
	return data[0][0]

async def get_uid(gn, **kwargs):
	data = await execute(f'SELECT uid FROM player WHERE gn = "{gn}";', **kwargs)
	if data == ():return ""
	else:return data[0][0]

def remaining_cd():
	cd_time = datetime.strptime((datetime.now(tz=TZ_SH) + timedelta(days=1)).strftime("%Y-%m-%d"), "%Y-%m-%d").replace(tzinfo=TZ_SH) - datetime.now(tz=TZ_SH)
	return int(cd_time.total_seconds())

def remaining_month_cd():
	month_days = calendar.monthrange(datetime.today().year, datetime.today().month)[1]
	cd_time = datetime.strptime(datetime.now(tz=TZ_SH).strftime("%Y-%m"), "%Y-%m").replace(tzinfo=TZ_SH) + timedelta(days=month_days) - datetime.now(tz=TZ_SH)
	return int(cd_time.total_seconds())

async def try_item(uid, item, value, **kwargs):
	async with (await get_db(**kwargs)).acquire() as conn:
		await conn.select_db(str(kwargs['world']))
		async with conn.cursor() as cursor:
			await cursor.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = "{item.value}" FOR UPDATE;')
			quantity = await cursor.fetchall()
			if value >= 0 or (quantity != () and quantity[0][0] + value >= 0):
				if await cursor.execute(f'INSERT INTO item (uid, iid, value) VALUES ("{uid}", {item.value}, value) ON DUPLICATE KEY UPDATE `value` = `value` + {value};') == 1:
					await cursor.execute(f'UPDATE item SET value = {value} WHERE uid = "{uid}" AND iid = {item.value};')
				return (True, quantity[0][0] + value) if quantity != () else (True, value)
			return (False, quantity[0][0] + value) if quantity != () else (False, value)

async def try_armor(uid, aid, level, value, **kwargs):
	async with (await get_db(**kwargs)).acquire() as conn:
		await conn.select_db(str(kwargs['world']))
		async with conn.cursor() as cursor:
			await cursor.execute(f'SELECT `quantity` FROM `armor` WHERE `uid` = "{uid}" AND \
					`aid` = {aid.value} AND `level` = {level} FOR UPDATE;')
			quantity = await cursor.fetchall()
			if value >= 0 or (quantity != () and quantity[0][0] + value >= 0):
				if await cursor.execute(f'INSERT INTO `armor` VALUES ("{uid}", {aid.value}, {level}, \
						{value}) ON DUPLICATE KEY UPDATE quantity = quantity + {value};') == 1:
					await cursor.execute(f'UPDATE `armor` SET `quantity` = {value} WHERE `uid` = "{uid}" \
							AND `aid` = {aid.value} AND `level` = {level};')
				return (True, quantity[0][0] + value) if quantity != () else (True, value)
			return (False, quantity[0][0] + value) if quantity != () else (False, value)

async def try_weapon(uid, weapon, quantity, **kwargs):
	data = await execute(f'SELECT segment FROM weapon WHERE uid = "{uid}" AND wid = {weapon.value};', **kwargs)
	if data == ():
		await execute(f'INSERT INTO weapon (uid, wid, segment) VALUES ("{uid}", {weapon.value}, {quantity});', **kwargs)
	else:
		quantity += data[0][0]
		await execute(f'UPDATE weapon SET segment = {quantity} WHERE uid = "{uid}" AND wid = {weapon.value};', **kwargs)
	return quantity

async def try_role(uid, role, quantity, **kwargs):
	data = await execute(f'SELECT segment FROM role WHERE uid = "{uid}" AND rid = {role.value};', **kwargs)
	if data == ():
		await execute(f'INSERT INTO role (uid, rid, segment) VALUES ("{uid}", {role.value}, {quantity});', **kwargs)
	else:
		quantity += data[0][0]
		await execute(f'UPDATE role SET segment = {quantity} WHERE uid = "{uid}" AND rid = {role.value};', **kwargs)
	return quantity

async def get_timer(uid, tid, timeformat = '%Y-%m-%d %H:%M:%S', **kwargs):
	data = await execute(f'SELECT `time` FROM `timer` WHERE `uid` = "{uid}" AND \
			`tid` = {tid.value};', **kwargs)
	return datetime.strptime(data[0][0], timeformat).replace(tzinfo=TZ_SH) if data != () else None

async def set_timer(uid, tid, time, timeformat = '%Y-%m-%d %H:%M:%S', **kwargs):
	await execute(f'INSERT INTO `timer` VALUES ("{uid}", {tid.value}, \
			"{time.strftime(timeformat)}") ON DUPLICATE KEY UPDATE \
			`time` = "{time.strftime(timeformat)}";', **kwargs)

async def get_limit(uid, lid, **kwargs):
	data = await execute(f'SELECT `value` FROM `limits` WHERE `uid` = "{uid}" AND \
			`lid` = {lid.value};', **kwargs)
	return data[0][0] if data != () else None

async def set_limit(uid, lid, value, **kwargs):
	await execute(f'INSERT INTO `limits` VALUES ("{uid}", {lid.value}, {value}) \
			ON DUPLICATE KEY UPDATE `value` = {value};', **kwargs)


async def get_db(**kwargs):
	return kwargs['worlddb']

def encode_item(gid, iid, value):
	return f'{gid.value}:{iid.value}:{value}'

def decode_items(items):
	decoded = []
	for item in items.split(','):  # "gid:iid:value,gid:iid:value"
		gid, iid, value = [int(v) if i < 2 else v for i, v in enumerate(item.split(':', maxsplit=2))]
		gid = enums.Group(gid)
		if gid == enums.Group.ITEM:
			decoded.append((gid, enums.Item(iid), int(value)))
		elif gid == enums.Group.WEAPON:
			decoded.append((gid, enums.Weapon(iid), int(value)))
		elif gid == enums.Group.SKILL:
			decoded.append((gid, enums.Skill(iid), int(value)))  # undecided
		elif gid == enums.Group.ROLE:
			decoded.append((gid, enums.Role(iid), int(value)))
		elif gid == enums.Group.ARMOR:
			decoded.append((gid, enums.Armor(iid), int(value)))
			# decoded.append((gid, enums.Armor(iid), value))  # value => 'level:value' => '1:1'
	return decoded


async def try_energy(uid, amount, **kwargs):
	# amount > 0 硬增加能量
	# amount == 0 自动恢复能量
	# amount < 0 消耗能量
	# success ===> 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7
	# - 0 - 购买能量成功 === Purchase energy successfully
	# - 1 - 购买能量成功，能量未恢复满 === Purchase energy successfully, energy is not fully restored
	# - 2 - 获取能量成功 === Get energy successfully
	# - 3 - 能量已消耗，能量值及恢复时间更新成功 === Energy has been consumed, energy value and recovery time updated successfully
	# - 4 - 能量已完全恢复，能量更新成功 === Energy has been fully restored, successful energy update
	# - 5 - 能量尚未完全恢复，能量更新成功 === Energy has not fully recovered, successful energy update
	# - 6 - 能量刷新后已消耗，能量值及恢复时间更新成功 === After refreshing the energy, the energy value and recovery time are successfully updated.
	# - 7 - 能量已刷新，未恢复满，已消耗能量，能量值及恢复时间更新成功 === Energy has been refreshed, not fully recovered, energy has been consumed, energy value and recovery time updated successfully
	# - 97 - 参数错误 === Parameter error
	# - 98 - 无足够能量消耗 === Not enough energy consumption
	# - 99 - 数据库操作错误 === Database operation error
	max_energy = kwargs['config']['player']['energy']['max_energy']
	data = await execute(f'SELECT energy FROM progress WHERE uid = "{uid}";', **kwargs)
	if data == ():
		await execute_update(f'INSERT INTO progress (uid) VALUE ("{uid}");', **kwargs)
		data = await execute(f'SELECT energy FROM progress WHERE uid = "{uid}";', **kwargs)
	sql_energy = data[0][0]
	if sql_energy >= max_energy:
		timer_data = await execute(f'SELECT time FROM timer WHERE uid = "{uid}" AND tid = "{enums.Timer.ENERGY_RECOVER_TIME.value}";', **kwargs)
		if timer_data == (): await execute_update(f'INSERT INTO timer (uid, tid) VALUES ("{uid}", "{enums.Timer.ENERGY_RECOVER_TIME.value}");', **kwargs)
		else: await execute(f'UPDATE timer SET time = "" WHERE uid = "{uid}" AND tid = "{enums.Timer.ENERGY_RECOVER_TIME.value}";', **kwargs)

	if amount > 0:  # 购买能量
		data = (await _decrease_energy(uid, 0, **kwargs))['data']
		status, _ = await execute_update(f'UPDATE progress SET energy = energy + {amount} WHERE uid = "{uid}";', **kwargs)
		energy_data = await execute(f'SELECT energy FROM progress WHERE uid = "{uid}";', **kwargs)
		if energy_data == ():
			await execute_update(f'INSERT INTO progress (uid) VALUE ("{uid}");', **kwargs)
			energy_data = await execute(f'SELECT energy FROM progress WHERE uid = "{uid}";', **kwargs)
		if status == 0:
			return mt(status=99, message="Database operation error")
		elif energy_data[0][0] >= max_energy:
			await execute_update(f'UPDATE timer SET time = "" WHERE uid = "{uid}" AND tid = "{enums.Timer.ENERGY_RECOVER_TIME.value}";', **kwargs)
			data['energy'] = energy_data[0][0]
			data['recover_time'] = ''
			data['cooling_time'] = -1
			return mt(0, "Purchase energy successfully", data)
		else:
			data['energy'] = energy_data[0][0]
			return mt(1, "Purchase energy successfully, energy is not fully restored", data)
	elif max_energy + amount < 0:
		return mt(status=97, message="Parameter error")
	else:  # 消耗能量或者查询能量
		return await _decrease_energy(uid, abs(amount), **kwargs)


async def _decrease_energy(uid, amount, **kwargs) -> dict:
	max_energy = kwargs['config']['player']['energy']['max_energy']
	_cooling_time = kwargs['config']['player']['energy']['cooling_time']
	data = await execute(f'SELECT energy FROM progress WHERE uid = "{uid}";', **kwargs)
	if data == ():
		await execute_update(f'INSERT INTO progress (uid) VALUE ("{uid}");', **kwargs)
		data = await execute(f'SELECT energy FROM progress WHERE uid = "{uid}";', **kwargs)
	current_energy = data[0][0]
	data = await execute(f'SELECT time FROM timer WHERE uid = "{uid}" AND tid = "{enums.Timer.ENERGY_RECOVER_TIME.value}";', **kwargs)
	if data == ():
		await execute_update(f'INSERT INTO timer (uid, tid) VALUES ("{uid}", "{enums.Timer.ENERGY_RECOVER_TIME.value}");', **kwargs)
		data = await execute(f'SELECT time FROM timer WHERE uid = "{uid}" AND tid = "{enums.Timer.ENERGY_RECOVER_TIME.value}";', **kwargs)
	recover_time = data[0][0]
	current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
	if recover_time == '':
		"""此时 current_energy == _max_energy 成立，即能力无消耗，满能量状态"""
		if amount == 0:  # 获取能量
			# 成功1：如果没有恢复时间且是获取能量值，则直接拿取数据库的值给客户端
			return mt(2, 'Get energy successfully', {'energy': current_energy, 'recover_time': recover_time, 'cooling_time': -1})
		current_energy -= amount
		# 成功2：如果没有恢复时间且是消耗能量值，则直接用数据库的值减去消耗的能量值，
		# 然后存入消耗之后的能量值，以及将当前的时间存入 恢复时间项
		if current_energy >= max_energy:  # 能量超出满能力状态时，不计算恢复时间
			current_time = ""
			cooling_time = -1
		else:
			await execute_update(f'UPDATE timer SET time = "{current_time}" WHERE uid = "{uid}" AND tid = "{enums.Timer.ENERGY_RECOVER_TIME.value}";', **kwargs)
			cooling_time = 60 * _cooling_time
		await execute_update(f'UPDATE progress SET energy = {current_energy} WHERE uid = "{uid}";', **kwargs)
		return mt(3, 'Energy has been consumed, energy value and recovery time updated successfully', {'energy': current_energy, 'recover_time': current_time, 'cooling_time': cooling_time})
	else:
		"""此时 current_energy != _max_energy 成立，即能力已消耗，恢复能量状态"""
		delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S')
		recovered_energy = int(delta_time.total_seconds()) // 60 // _cooling_time  # 计算恢复能量的点数
		if amount == 0:  # 获取能量
			# 成功3：如果有恢复时间且是获取能量值，则加上获取的能量值，并判断能量值是否满足上限
			# 满足上限的情况：直接将满能量值和空字符串分别存入能量值项和恢复时间项
			if current_energy + recovered_energy >= max_energy:
				recover_time, current_energy, cooling_time = "", max_energy, -1
				await execute_update(f'UPDATE progress SET energy = {current_energy} WHERE uid = "{uid}";', **kwargs)
				await execute_update(f'UPDATE timer SET time = "{recover_time}" WHERE uid = "{uid}" AND tid = "{enums.Timer.ENERGY_RECOVER_TIME.value}";', **kwargs)
				return mt(4, 'Energy has been fully restored, successful energy update', {'energy': current_energy, 'recover_time': recover_time, 'cooling_time': cooling_time})
			# 成功4：如果有恢复时间且是获取能量值，则加上获取的能量值，并判断能量值是否满足上限
			# 不满足上限的情况：将能恢复的能量值计算出来，并且计算恢复后的能量值current_energy
			# 和恢复时间与恢复能量消耗的时间相减的恢复时间值
			else:
				recover_time, current_energy = (datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=recovered_energy * _cooling_time)).strftime("%Y-%m-%d %H:%M:%S"), current_energy + recovered_energy
				delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S')
				cooling_time = 60 * _cooling_time - int(delta_time.total_seconds())  # 计算下一点能量需要多少的恢复时间
				await execute_update(f'UPDATE progress SET energy = {current_energy} WHERE uid = "{uid}";', **kwargs)
				await execute_update(f'UPDATE timer SET time = "{recover_time}" WHERE uid = "{uid}" AND tid = "{enums.Timer.ENERGY_RECOVER_TIME.value}";', **kwargs)
				return mt(5, 'Energy has not fully recovered, successful energy update', {'energy': current_energy, 'recover_time': recover_time, 'cooling_time': cooling_time})

		if recovered_energy + current_energy >= max_energy:
			# 成功5：如果有恢复时间且是消耗能量
			# 满足上限的情况是用上限能量值减去要消耗的能量值，然后设置减去之后的能量值和当前的时间分别存入能量值项和恢复时间项
			current_energy = max_energy - amount
			cooling_time = _cooling_time * 60
			await execute_update(f'UPDATE progress SET energy = {current_energy} WHERE uid = "{uid}";', **kwargs)
			await execute_update(f'UPDATE timer SET time = "{current_time}" WHERE uid = "{uid}" AND tid = "{enums.Timer.ENERGY_RECOVER_TIME.value}";', **kwargs)
			return mt(6, 'After refreshing the energy, the energy value and recovery time are successfully updated', {'energy': current_energy, 'recover_time': current_time, 'cooling_time': cooling_time})
		elif recovered_energy + current_energy - amount >= 0:
			# 成功6：如果有恢复时间且是消耗能量
			# 不满足上限的情况是用当前数据库的能量值和当前恢复的能量值相加然后减去消耗的能量值为要存入数据库的能量值项
			# 数据库中的恢复时间与恢复能量消耗的时间相减的恢复时间值存入到数据库的恢复时间项
			current_energy = recovered_energy + current_energy - amount
			recover_time = (datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=recovered_energy * _cooling_time)).strftime("%Y-%m-%d %H:%M:%S")
			delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S')
			cooling_time = 60 * _cooling_time - int(delta_time.total_seconds())
			await execute_update(f'UPDATE progress SET energy = {current_energy} WHERE uid = "{uid}";', **kwargs)
			await execute_update(f'UPDATE timer SET time = "{recover_time}" WHERE uid = "{uid}" AND tid = "{enums.Timer.ENERGY_RECOVER_TIME.value}";', **kwargs)
			return mt(7, 'Energy has been refreshed, not fully recovered, energy has been consumed, energy value and recovery time updated successfully', {'energy': current_energy, 'recover_time': recover_time, 'cooling_time': cooling_time})
		else:  # 发生的情况是当前能量值和恢复能量值相加比需要消耗的能量值少
			return mt(98, 'Not enough energy consumption')

def mt(status, message, data = {}):
	return {'status' : status, 'message' : message, 'data' : data}

#private message
async def _redeem_all_mail(uid, gn_target, mail_type, group_id, item_id, quantity, **kwargs):
	return mt(0, 'success')

async def _send_text_mail(uid, gn_target, msg, **kwargs):
	fid = await get_uid(gn_target, **kwargs)
	#kwargs['msg'] = msg
	#kwargs['from_'] = await get_gn(uid, **kwargs)
	#sent = await mail.send_mail(0, fid, **kwargs)
	await mail.send_mail({'type' : enums.MailType.SIMPLE.value, 'from' : await get_gn(uid, **kwargs), \
			'subj' : kwargs['data']['subj'], 'body' : kwargs['data']['body']}, fid, **kwargs)



	return mt(0, 'success')

async def _send_gift_mail(uid, gn_target, group_id, item_id, quantity, **kwargs):
	fid = await get_uid(gn_target, **kwargs)
	if fid=="": return mt(99, '')
	#kwargs['items'] = encode_item(enums.Group(group_id), enums.Item(item_id), quantity)
	#kwargs['from_'] = await get_gn(uid, **kwargs)
	#sent = await mail.send_mail(1, fid, **kwargs)

	await mail.send_mail({'type' : enums.MailType.GIFT.value, 'from' : await get_gn(uid, **kwargs), \
			'subj' : enums.MailTemplate.SYSTEM_REWARD.name, 'body' : enums.MailTemplate.GIFT_1.name, \
			'items' : encode_item(enums.Group(group_id), enums.Item(item_id), quantity)}, \
			fid, **kwargs)



	return mt(0, 'success')


def __calculate(config: list, sql_exp: int) -> (int, int):
	expl = [e for e in config if e > sql_exp]
	level, need = config.index(expl[0]) if expl != [] else len(config), expl[0] - sql_exp if expl != [] else 0
	return level, need
