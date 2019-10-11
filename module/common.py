'''
common.py

Contains definitions of commonly used generic functions.
When desinging a function, try to make it as general as possible to allow the reuse of code.
'''
from module import enums
import time
from datetime import datetime, timedelta


async def exists(table, *conditions, account = False, **kwargs):
	condition = ' AND '.join([f'`{cond[0]}` = "{cond[1]}"' for cond in conditions])
	data = await execute(f'SELECT EXISTS (SELECT 1 FROM {table} WHERE {condition});', account, **kwargs)
	if data == () or () in data: return False
	return data[0][0] != 0

async def execute(statement, account = False, **kwargs):
	async with ((await get_db(**kwargs)).acquire() if not account else kwargs['accountdb'].acquire()) as conn:
		# await conn.select_db()
		async with conn.cursor() as cursor:
			await cursor.execute(statement)
			return await cursor.fetchall()

async def execute_update(statement, account = False, **kwargs):
	async with ((await get_db(**kwargs)).acquire() if not account else kwargs['accountdb'].acquire()) as conn:
		# await conn.select_db()
		async with conn.cursor() as cursor:
			affected = await cursor.execute(statement)
			return (affected, await cursor.fetchall())

async def get_gn(uid, **kwargs):
	data = await execute(f'SELECT gn FROM player WHERE uid = "{uid}";', **kwargs)
	return data[0][0]

async def get_uid(gn, **kwargs):
	data = await execute(f'SELECT uid FROM player WHERE gn = "{gn}";', **kwargs)
	return data[0][0]

async def try_item(uid, item, value, **kwargs):
	async with (await get_db(**kwargs)).acquire() as conn:
		# await conn.select_db()
		async with conn.cursor() as cursor:
			await cursor.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = "{item.value}" FOR UPDATE;')
			quantity = await cursor.fetchall()
			if value >= 0 or (quantity != () and quantity[0][0] + value >= 0):
				await cursor.execute(f'INSERT INTO item (uid, iid, value) VALUES ("{uid}", {item.value}, value) ON DUPLICATE KEY UPDATE value = value + {value};')
				return (True, quantity[0][0] + value) if quantity != () else (True, value)
			return (False, quantity[0][0] + value) if quantity != () else (False, value)

async def get_db(**kwargs):
	return kwargs['worlddb']

def encode_item(gid, iid, value):
	return f'{gid.value}:{iid.value}:{value}'

def decode_items(items):
	decoded = []
	for item in items.split(','):
		gid, iid, value = item.split(':')
		gid = enums.Group(int(gid))
		if gid == enums.Group.ITEM:
			decoded.append((gid, enums.Item(int(iid)), int(value)))
		elif gid == enums.Group.WEAPON:
			decoded.append((gid, enums.Weapon(int(iid)), int(value)))
		elif gid == enums.Group.SKILL:
			decoded.append((gid, enums.Skill(int(iid)), int(value)))
		elif gid == enums.Group.ROLE:
			decoded.append((gid, enums.Role(int(iid)), int(value)))
		elif gid == enums.Group.ARMOR:
			decoded.append((gid, enums.Armor(int(iid)), int(value)))
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
	max_energy = kwargs['max_energy']  # self._player["energy"]["max_energy"]
	data = await execute(f'SELECT energy FROM progress WHERE uid = "{uid}";', **kwargs)
	sql_energy = data[0][0]
	if sql_energy >= max_energy:
		await execute_update(f'UPDATE timer SET time = "" WHERE uid = "{uid}" AND tid = "{enums.Timer.ENERGY_RECOVER_TIME.value}";')
	if amount > 0:  # 购买能量
		data = (await _decrease_energy(uid, 0, **kwargs))['data']
		status, energy_data = await execute_update(f'UPDATE progress SET energy = energy + {amount} WHERE uid = "{uid}";', **kwargs)
		if status == 0:
			return mt(status=99, message="Database operation error")
		elif energy_data[0][0] >= max_energy:
			await execute_update(f'UPDATE timer SET time = "" WHERE uid = "{uid}" AND tid = "{enums.Timer.ENERGY_RECOVER_TIME.value}";')
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
	max_energy = kwargs['max_energy']  # self._player["energy"]["max_energy"]
	_cooling_time = kwargs['cooling_time']  # self._player["energy"]["cooling_time"]
	data = await execute(f'SELECT energy FROM progress WHERE uid = "{uid}";', **kwargs)
	current_energy = data[0][0]
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
		if current_energy >= max_energy: current_time = ""  # 能量超出满能力状态时，不计算恢复时间
		cooling_time = _cooling_time * 60
		await execute_update(f'UPDATE progress SET energy = {current_energy} WHERE uid = "{uid}";')
		await execute_update(f'UPDATE timer SET time = "{current_time}" WHERE uid = "{uid}" AND tid = "{enums.Timer.ENERGY_RECOVER_TIME.value}";')
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
				await execute_update(f'UPDATE progress SET energy = {current_energy} WHERE uid = "{uid}";')
				await execute_update(f'UPDATE timer SET time = "{recover_time}" WHERE uid = "{uid}" AND tid = "{enums.Timer.ENERGY_RECOVER_TIME.value}";')
				return mt(4, 'Energy has been fully restored, successful energy update', {'energy': current_energy, 'recover_time': recover_time, 'cooling_time': cooling_time})
			# 成功4：如果有恢复时间且是获取能量值，则加上获取的能量值，并判断能量值是否满足上限
			# 不满足上限的情况：将能恢复的能量值计算出来，并且计算恢复后的能量值current_energy
			# 和恢复时间与恢复能量消耗的时间相减的恢复时间值
			else:
				recover_time, current_energy = (datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=recovered_energy * _cooling_time)).strftime("%Y-%m-%d %H:%M:%S"), current_energy + recovered_energy
				delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S')
				cooling_time = 60 * _cooling_time - int(delta_time.total_seconds())  # 计算下一点能量需要多少的恢复时间
				await execute_update(f'UPDATE progress SET energy = {current_energy} WHERE uid = "{uid}";')
				await execute_update(f'UPDATE timer SET time = "{recover_time}" WHERE uid = "{uid}" AND tid = "{enums.Timer.ENERGY_RECOVER_TIME.value}";')
				return mt(5, 'Energy has not fully recovered, successful energy update', {'energy': current_energy, 'recover_time': recover_time, 'cooling_time': cooling_time})

		if recovered_energy + current_energy >= max_energy:
			# 成功5：如果有恢复时间且是消耗能量
			# 满足上限的情况是用上限能量值减去要消耗的能量值，然后设置减去之后的能量值和当前的时间分别存入能量值项和恢复时间项
			current_energy = max_energy - amount
			cooling_time = _cooling_time * 60
			await execute_update(f'UPDATE progress SET energy = {current_energy} WHERE uid = "{uid}";')
			await execute_update(f'UPDATE timer SET time = "{current_time}" WHERE uid = "{uid}" AND tid = "{enums.Timer.ENERGY_RECOVER_TIME.value}";')
			return mt(6, 'After refreshing the energy, the energy value and recovery time are successfully updated', {'energy': current_energy, 'recover_time': current_time, 'cooling_time': cooling_time})
		elif recovered_energy + current_energy - amount >= 0:
			# 成功6：如果有恢复时间且是消耗能量
			# 不满足上限的情况是用当前数据库的能量值和当前恢复的能量值相加然后减去消耗的能量值为要存入数据库的能量值项
			# 数据库中的恢复时间与恢复能量消耗的时间相减的恢复时间值存入到数据库的恢复时间项
			current_energy = recovered_energy + current_energy - amount
			recover_time = (datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=recovered_energy * _cooling_time)).strftime("%Y-%m-%d %H:%M:%S")
			delta_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S')
			cooling_time = 60 * _cooling_time - int(delta_time.total_seconds())
			await execute_update(f'UPDATE progress SET energy = {current_energy} WHERE uid = "{uid}";')
			await execute_update(f'UPDATE timer SET time = "{recover_time}" WHERE uid = "{uid}" AND tid = "{enums.Timer.ENERGY_RECOVER_TIME.value}";')
			return mt(7, 'Energy has been refreshed, not fully recovered, energy has been consumed, energy value and recovery time updated successfully', {'energy': current_energy, 'recover_time': recover_time, 'cooling_time': cooling_time})
		else:  # 发生的情况是当前能量值和恢复能量值相加比需要消耗的能量值少
			return mt(98, 'Not enough energy consumption')

def mt(status, message, data = {}):
	return {'status' : status, 'message' : message, 'data' : data}
