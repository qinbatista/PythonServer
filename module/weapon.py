'''
weapon.py
'''

from module import enums
from module import common

STANDARD_IRON = 40

async def level_up(uid, wid, amount, **kwargs):
	w = enums.Weapon(wid)
	star, level, sp = await _valid_level_up_target(uid, wid, **kwargs)
	if not star:
		return common.mt(99, 'invalid target')
	upgrade_cnt = min(amount // STANDARD_IRON, 100 - level)
	if upgrade_cnt == 0: return common.mt(98, 'too few incoming materials')
	can_pay, remaining = await common.try_item(uid, enums.Item.IRON, -upgrade_cnt * STANDARD_IRON, **kwargs)
	if not can_pay: return common.mt(97, 'can not pay for upgrade')
	await common.execute(f'UPDATE weapon SET level = {level + upgrade_cnt}, skillpoint = {sp + upgrade_cnt} WHERE uid = "{uid}" AND wid = {wid.value}', **kwargs)
	return common.mt(0, 'success', {'wid' : wid.value, 'level' : level + upgrade_cnt, 'skillpoint' : sp + upgrade_cnt, 'remaining' : remaining})

async def level_up_passive(uid, wid, pid, **kwargs):
	pass

async def level_up_star(uid, wid, **kwargs):
	pass

async def reset_skill_point(uid, wid, **kwargs):
	pass

async def get_all(uid, **kwargs):
	pass


####################################################################################

async def _valid_level_up_target(uid, wid, **kwargs):
	data = await common.execute(f'SELECT star, level, skillpoint FROM weapon WHERE uid = "{uid}" AND wid = {wid.value};', **kwargs)
	return data[0] if (data != () and data[0][0] > 0 and data[0][1] <= 100) else (None, None)
