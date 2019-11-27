'''
armor.py
'''

from module import enums
from module import common


async def upgrade(uid, aid, level, **kwargs):
	"""盔甲等级限制1-10，level限制2-10"""
	# 0 - success
	# 97 - Insufficient basic armor
	# 98 - invalid aid
	# 99 - invalid level
	if level <= 0 or level >= 10: return common.mt(99, 'invalid level')  # 最高合成10级盔甲
	if int(aid) not in enums.Armor._value2member_map_: return common.mt(98, 'invalid aid')
	basic_quantity = await _get_armor(uid, aid, level, **kwargs)
	pro_quantity = await _get_armor(uid, aid, level+1, **kwargs)
	if basic_quantity < 3: return common.mt(99, 'Insufficient basic armor')
	remaining_basic_quantity = basic_quantity%3
	remaining_pro_quantity =pro_quantity + basic_quantity//3
	await common.execute(f'UPDATE armor SET quantity = {remaining_basic_quantity} WHERE uid = "{uid}" AND aid = {aid} AND level = {level};', **kwargs)
	await common.execute(f'UPDATE armor SET quantity = {remaining_pro_quantity} WHERE uid = "{uid}" AND aid = {aid} AND level = {level+1};', **kwargs)
	return common.mt(0, 'success', {'armors': {"resource":{'aid': aid, 'level': level, 'quantity': remaining_basic_quantity}, "production":{'aid': aid, 'level': level+1, 'quantity': remaining_pro_quantity}}})


async def get_all(uid, **kwargs):
	# 0 - success
	armor = await common.execute(f'SELECT aid, level, quantity FROM armor WHERE uid = "{uid}";', **kwargs)
	return common.mt(0, 'success', {'armors': [{'aid': a[0], 'level': a[1], 'quantity': a[2]} for a in armor]})


############################################# PRIVATE #############################################


async def _get_armor(uid, aid, level, **kwargs):
	quantity = await common.execute(f'SELECT quantity FROM armor WHERE uid = "{uid}" AND aid = {aid} AND level = {level};', **kwargs)
	if quantity == ():
		await common.execute(f'INSERT INTO armor (uid, aid, level) VALUES ("{uid}", {aid}, {level});', **kwargs)
		quantity = await common.execute(f'SELECT quantity FROM armor WHERE uid = "{uid}" AND aid = {aid} AND level = {level};', **kwargs)
	return quantity[0][0]
