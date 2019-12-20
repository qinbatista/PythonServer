'''
package.py
'''

from module import enums
from module import common
from module import stage
from random import choice
import re


ENERGY = [
	enums.Item.ENERGY_POTION_S_MIN,
	enums.Item.ENERGY_POTION_S_MAX
]
WEAPON = [
	enums.Item.WEAPON4_UNIVERSAL_SEGMENT,
	enums.Item.WEAPON5_UNIVERSAL_SEGMENT
]
ROLE = [
	enums.Item.ROLE4_UNIVERSAL_SEGMENT,
	enums.Item.ROLE5_UNIVERSAL_SEGMENT
]
UNIVERSAL = [
	enums.Item.UNIVERSAL4_SEGMENT,
	enums.Item.UNIVERSAL5_SEGMENT,
	enums.Item.UNIVERSAL6_SEGMENT
]

async def exchange(uid, cid, qty=1, **kwargs):
	if cid not in enums.Item._value2member_map_.keys(): return common.mt(99, 'iid error')
	config = kwargs['config']['package']['exchange_card']
	cname = enums.Item(cid).name  # iid是卡片id
	if cname not in config.keys(): return common.mt(98, 'card kind error (kind:18-23)')
	sql_table = config[cname]['sqltable']
	if sql_table not in SQL_TABLE.keys(): return common.mt(97, 'config sql table kind error')
	if qty <= 0: return common.mt(96, 'The quantity can only be positive')
	can, card_num = await common.try_item(uid, enums.Item(cid), -qty, **kwargs)  # 卡片的剩余数量
	if not can: return common.mt(95, 'Insufficient card')
	exp_info, rnum, vnum = await SQL_TABLE[sql_table](uid, config[cname]['mid'], qty * config[cname]['bnum'], **kwargs)
	return common.mt(0, 'success', {'remaining': {'sql_table': sql_table, 'mid': config[cname]['mid'], 'mnum': rnum, 'cid': cid, 'cnum': card_num}, 'reward': {'sql_table': sql_table, 'mid': config[cname]['mid'], 'mnum': vnum, 'cid': cid, 'cnum': -qty}, 'exp_info': exp_info})


async def use_item(uid, iid, eid, **kwargs):
	"""
	iid: 格式为"1:2:6"，代表兑换消耗品，1是gid：gid都是item类，2是iid，6是iid消耗的数量暂时未使用
	eid: 格式为"1:2:1", 代表兑换的成品
	"""
	consume = 1
	c = common.decode_items(iid)[0]
	# consume = c[2]
	if c[0] == enums.Group.ITEM:
		can, remain = await common.try_item(uid, c[1], -consume, **kwargs)
		if not can: return common.mt(96, '兑换消耗品不足')
		iid = iid[:iid.rfind(':')]
		if c[1] in ENERGY:
			energy = kwargs['config']['package']['exchange_item'][c[1].name.lower()]
			energy_data = (await common.try_energy(uid, energy, **kwargs))['data']
			return common.mt(0, 'success', {'remaining': {'item': f"{iid}:{remain}", 'energy': energy_data['energy'], 'cooling_time': energy_data['cooling_time']}, 'reward': {'item': f"{iid}:{-consume}", 'energy': energy}})
		else:
			if c[1] in WEAPON:
				seg = kwargs['config']['package']['exchange_item'][c[1].name.lower()]
				kind = enums.Weapon[choice([k for k in enums.Weapon.__members__.keys() if 'W' + re.search(r"\d", c[1].name).group(0) in k])]
				seg_data = await common.try_weapon(uid, kind, seg, **kwargs)
				return common.mt(1, 'success', {'remaining': {'item': f"{iid}:{remain}", 'eitem': f"{enums.Group.WEAPON.value}:{kind.value}:{seg_data}"}, 'reward': {'item': f"{iid}:{-consume}", 'eitem': f"{enums.Group.WEAPON.value}:{kind.value}:{seg}"}})
			elif c[1] in ROLE:
				seg = kwargs['config']['package']['exchange_item'][c[1].name.lower()]
				kind = enums.Role[choice([k for k in enums.Role.__members__.keys() if 'R' + re.search(r"\d", c[1].name).group(0) in k])]
				seg_data = await common.try_role(uid, kind, seg, **kwargs)
				return common.mt(2, 'success', {'remaining': {'item': f"{iid}:{remain}", 'eitem': f"{enums.Group.ROLE.value}:{kind.value}:{seg_data}"}, 'reward': {'item': f"{iid}:{-consume}", 'eitem': f"{enums.Group.ROLE.value}:{kind.value}:{seg}"}})
			elif c[1] in UNIVERSAL:
				e = common.decode_items(eid)[0]
				eid = eid[:eid.rfind(':')]
				seg = kwargs['config']['package']['exchange_item'][c[1].name.lower()]
				if (e[0] == enums.Group.ROLE and e[1].name not in [k for k in enums.Role.__members__.keys() if 'R' + re.search(r"\d", c[1].name).group(0) in k]) or \
					(e[0] == enums.Group.WEAPON and e[1].name not in [k for k in enums.Weapon.__members__.keys() if 'W' + re.search(r"\d", c[1].name).group(0) in k]):
					await common.try_item(uid, c[1], consume, **kwargs)  # 还原
					return common.mt(97, '兑换碎片类型不匹配')
				else:
					seg_data = await (common.try_weapon(uid, e[1], seg, **kwargs) if e[0] == enums.Group.WEAPON else common.try_role(uid, e[1], seg, **kwargs))
					return common.mt(3, 'success', {'remaining': {'item': f"{iid}:{remain}", 'eitem': f"{eid}:{seg_data}"}, 'reward': {'item': f"{iid}:{-consume}", 'eitem': f"{eid}:{seg}"}})
			else:
				await common.try_item(uid, c[1], consume, **kwargs)  # 还原
				return common.mt(98, '兑换成品类型错误')
	else:
		return common.mt(99, f'意外消耗品{iid}')

async def config(uid, **kwargs):
	return common.mt(0, 'success', {'config': kwargs['config']['package']})

########################################## 私有 ##########################################
async def update_item(uid, mid, bnum, **kwargs):
	exp_info = await stage.increase_exp(uid, 0, **kwargs)
	vnum = exp_info['level'] * bnum
	_, rnum = await common.try_item(uid, enums.Item(mid), vnum, **kwargs)
	return exp_info, rnum, vnum


async def update_progress(uid, mid, bnum, **kwargs):
	exp_info = await stage.increase_exp(uid, 0, **kwargs)
	vnum = exp_info['level'] * bnum
	await common.execute(f'UPDATE progress SET exp = exp + {vnum} WHERE uid = "{uid}";', **kwargs)
	data = await common.execute(f'SELECT exp FROM progress WHERE uid = "{uid}";', **kwargs)
	exp_info = await stage.increase_exp(uid, 0, **kwargs)
	return exp_info, data[0][0], vnum


SQL_TABLE = {'item': update_item, 'progress': update_progress}
