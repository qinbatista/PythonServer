'''
armor.py
'''

from module import enums
from module import common


async def upgrade(uid, aid, level, n=1, **kwargs):
	"""盔甲等级限制1-10，level限制2-11"""
	# 0 - success
	# 97 - Insufficient basic armor
	# 98 - invalid aid
	# 99 - invalid level
	if level < 2 or level > 11: return common.mt(99, 'invalid level')  # 最高合成10级盔甲
	if int(aid) not in enums.Armor._value2member_map_: return common.mt(98, 'invalid aid')
	index = level - 1
	s_tier, e_tier = await _get_armor(uid, aid, **kwargs)
	_upgrade(e_tier, index-1, index, n)
	if s_tier == e_tier: return common.mt(97, 'Insufficient basic armor')
	e_tier[index] += n
	for i, qty in enumerate(e_tier): await _set_armor(uid, aid, i + 1, qty, **kwargs)
	remaining = {i + 1: qty for i, qty in enumerate(e_tier)}
	reward = {i + 1: qty - s_tier[i] for i, qty in enumerate(e_tier)}
	return common.mt(0, 'success', {'aid': aid, 'remaining': remaining, 'reward': reward})


async def get_all(uid, **kwargs):
	# 0 - success
	armor = await common.execute(f'SELECT aid, level, quantity FROM armor WHERE uid = "{uid}";', **kwargs)
	return common.mt(0, 'success', {'armors': [{'aid': a[0], 'level': a[1], 'quantity': a[2]} for a in armor]})


############################################# PRIVATE #############################################


async def _get_armor(uid, aid, **kwargs) -> (list, list):
	tier = await common.execute(f'SELECT quantity FROM armor WHERE uid = "{uid}" AND aid = {aid} ORDER BY level ASC;', **kwargs)
	if len(tier) < enums.ArmorTier.__len__():
		await common.execute(f'INSERT INTO armor (uid, aid, level) VALUES ("{uid}", {aid}, {enums.ArmorTier.T1.value}), \
		("{uid}", {aid}, {enums.ArmorTier.T2.value}), ("{uid}", {aid}, {enums.ArmorTier.T3.value}), \
		("{uid}", {aid}, {enums.ArmorTier.T4.value}), ("{uid}", {aid}, {enums.ArmorTier.T5.value}), \
		("{uid}", {aid}, {enums.ArmorTier.T6.value}), ("{uid}", {aid}, {enums.ArmorTier.T7.value}), \
		("{uid}", {aid}, {enums.ArmorTier.T8.value}), ("{uid}", {aid}, {enums.ArmorTier.T9.value}), \
		("{uid}", {aid}, {enums.ArmorTier.T10.value}), ("{uid}", {aid}, {enums.ArmorTier.T11.value}) ON DUPLICATE KEY UPDATE aid=`aid`;', **kwargs)
		tier = await common.execute(f'SELECT quantity FROM armor WHERE uid = "{uid}" AND aid = {aid};', **kwargs)
	return [t[0] for t in tier], [t[0] for t in tier]


async def _set_armor(uid, aid, level, qty, **kwargs):
	await common.execute(f'UPDATE armor SET quantity = {qty} WHERE uid = "{uid}" AND aid = {aid} AND level = {level};', **kwargs)


def _upgrade(tier, i, j, n):
	"""
	tier: 需要升级转化的列表
	i: j-1
	j: 需要升级成的盔甲位置索引，不能大于数组列表数量
	n: 需要升级完成的数量
	"""
	if tier[i] >= 3 * n:
		for k in range(i+1, j): tier[k] = 0
		tier[i] -= 3 * n
	elif i == 0: pass
	else: _upgrade(tier, i - 1, j, 3 * n - tier[i])
