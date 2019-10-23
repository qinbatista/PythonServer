'''
armor.py
'''

from module import enums
from module import common


async def upgrade(uid, aid, level, **kwargs):
	if level < 1 or level > 10: return common.mt(99, 'invalid level')  # 最高合成10级盔甲
	if int(aid) not in enums.Armor._value2member_map_: return common.mt(98, 'invalid aid')
	b_quantity = await _get_armor(uid, aid, level - 1)
	r_quantity = await _get_armor(uid, aid, level)
	if b_quantity < 3: return common.mt(97, 'Insufficient basic armor')
	b_quantity -= 3
	r_quantity += 1
	await common.execute(f'UPDATE armor SET quantity = {b_quantity} WHERE uid = "{uid}" AND aid = {aid} AND level = {level - 1};', **kwargs)
	await common.execute(f'UPDATE armor SET quantity = {r_quantity} WHERE uid = "{uid}" AND aid = {aid} AND level = {level};', **kwargs)
	return common.mt(0, 'success', {'armors': [{'aid': aid, 'level': level - 1, 'quantity': b_quantity}, {'aid': aid, 'level': level, 'quantity': r_quantity}]})


async def get_all(uid, **kwargs):
	armor = await common.execute(f'SELECT aid, level, quantity FROM armor WHERE uid = "{uid}";', **kwargs)
	return common.mt(0, 'success', {'armors': [{'aid': a[0], 'level': a[1], 'quantity': a[2]} for a in armor]})


############################################# PRIVATE #############################################


async def _get_armor(uid, aid, level, **kwargs):
	quantity = await common.execute(f'SELECT quantity FROM armor WHERE uid = "{uid}" AND aid = {aid} AND level = {level};', **kwargs)
	if quantity == ():
		await common.execute(f'INSERT INTO armor (uid, aid, level) VALUES ("{uid}", {aid}, {level});', **kwargs)
		quantity = await common.execute(f'SELECT quantity FROM armor WHERE uid = "{uid}" AND aid = {aid} AND level = {level};', **kwargs)
	return quantity[0][0]
