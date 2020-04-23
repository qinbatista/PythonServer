'''
package.py
'''

from module import enums
from module import common
from module import stage
from module import vip
from random import choice
from datetime import datetime, timedelta
import re


ENERGY = [
	enums.Item.ENERGY_POTION_S_MIN,
	enums.Item.ENERGY_POTION_S_MAX
]
WEAPON = {
	enums.Item.WEAPON4_UNIVERSAL_SEGMENT: [401, 402, 405],
	enums.Item.WEAPON5_UNIVERSAL_SEGMENT: [501, 502, 503, 504, 505, 506, 507],
	enums.Item.WEAPON6_UNIVERSAL_SEGMENT: [601]
}
ROLE = {
	enums.Item.ROLE4_UNIVERSAL_SEGMENT: [402, 403, 404, 405, 406, 407],
	enums.Item.ROLE5_UNIVERSAL_SEGMENT: [501, 504, 505, 506],
	enums.Item.ROLE6_UNIVERSAL_SEGMENT: [601]
}
UNIVERSAL = [
	enums.Item.UNIVERSAL4_SEGMENT,
	enums.Item.UNIVERSAL5_SEGMENT,
	enums.Item.UNIVERSAL6_SEGMENT
]
SCROLL = {
	enums.Item.SKILL_SCROLL_10: enums.Item.SKILL_SCROLL_30,
	enums.Item.SKILL_SCROLL_30: enums.Item.SKILL_SCROLL_100
}
DIAMONDS = [30, 60, 90, 120, 150, 180]


async def get_lim(uid, tid, lid, top, **kwargs):
	now = datetime.now(tz=common.TZ_SH)
	lim = await common.get_limit(uid, lid, **kwargs)
	tim = await common.get_timer(uid, tid, timeformat='%Y-%m-%d', **kwargs)
	if tim is None or tim < now:
		tim, lim = now + timedelta(days=1), top
		await common.set_limit(uid, lid, lim, **kwargs)
		await common.set_timer(uid, tid, tim, timeformat='%Y-%m-%d', **kwargs)
	return lim


async def buy_energy(uid, **kwargs):
	top = len(DIAMONDS)
	lid, tid = enums.Limits.PACKAGE_ENERGY, enums.Timer.PACKAGE_ENERGY
	lim = await get_lim(uid, tid, lid, top, **kwargs) - 1
	if lim < 0:
		return common.mt(98, 'Insufficient purchase times')
	drw, erw = DIAMONDS[top - lim - 1], 30
	can, drm = await common.try_item(uid, enums.Item.DIAMOND, -drw, **kwargs)
	if not can:
		return common.mt(99, 'Insufficient materials')
	energy = (await common.try_energy(uid, erw, **kwargs))['data']
	await common.set_limit(uid, lid, lim, **kwargs)
	return common.mt(0, 'success', {'diamond': {'remain': drm, 'reward': drw},
	                                'energy': {**energy, 'reward': erw},
	                                'lim': lim, 'cd': common.remaining_cd()})


async def buy_coin(uid, qty, **kwargs):
	drw, crw = 300*qty, qty
	gid, did, cid = enums.Group.ITEM, enums.Item.DIAMOND, enums.Item.COIN_CARD
	can, drm = await common.try_item(uid, did, -drw, **kwargs)
	if not can:
		return common.mt(99, 'Insufficient materials')
	_, crm = await common.try_item(uid, cid, crw, **kwargs)
	return common.mt(0, 'success',
	                 {'remain': [f'{gid}:{did}:{drm}', f'{gid}:{cid}:{crm}'],
	                  'reward': [f'{gid}:{did}:{drw}', f'{gid}:{cid}:{crw}']})


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
	# consume = 1
	g, i, mul = common.decode_items(iid)[0]
	if g == enums.Group.ITEM:
		if i in SCROLL and mul % 3 != 0: return common.mt(95, 'Scroll upgrades require multiples of 3')
		can, iq = await common.try_item(uid, i, -mul, **kwargs)  # 是卷轴则消耗三倍低级卷轴生成一倍高级卷轴
		if not can: return common.mt(96, '兑换消耗品不足')
		iid = iid[:iid.rfind(':')]
		if i in ENERGY:
			energy = kwargs['config']['package']['exchange_item'][i.name] * mul
			energy_data = (await common.try_energy(uid, energy, **kwargs))['data']
			return common.mt(0, 'success', {'remaining': {'item': f"{iid}:{iq}", 'energy': energy_data['energy'], 'cooling_time': energy_data['cooling_time']}, 'reward': {'item': f"{iid}:{mul}", 'energy': energy}})
		else:
			if i in WEAPON:
				seg = kwargs['config']['package']['exchange_item'][i.name] * mul
				kind = choice(WEAPON[i])
				# kind = enums.Weapon[choice([k for k in enums.Weapon.__members__ if 'W' + re.search(r"\d", i.name).group(0) in k])]
				seg_data = await common.try_weapon(uid, kind, seg, **kwargs)
				return common.mt(1, 'success', {'remaining': {'item': f"{iid}:{iq}", 'eitem': f"{enums.Group.WEAPON}:{kind}:{seg_data}"}, 'reward': {'item': f"{iid}:{mul}", 'eitem': f"{enums.Group.WEAPON}:{kind}:{seg}"}})
			elif i in ROLE:
				seg = kwargs['config']['package']['exchange_item'][i.name] * mul
				kind = choice(ROLE[i])
				# kind = enums.Role[choice([k for k in enums.Role.__members__ if 'R' + re.search(r"\d", i.name).group(0) in k])]
				seg_data = await common.try_role(uid, kind, seg, **kwargs)
				return common.mt(2, 'success', {'remaining': {'item': f"{iid}:{iq}", 'eitem': f"{enums.Group.ROLE}:{kind}:{seg_data}"}, 'reward': {'item': f"{iid}:{mul}", 'eitem': f"{enums.Group.ROLE}:{kind}:{seg}"}})
			elif i in UNIVERSAL:
				eg, ei, eq = common.decode_items(eid)[0]
				eid = eid[:eid.rfind(':')]
				seg = kwargs['config']['package']['exchange_item'][i.name] * mul
				if (eg == enums.Group.ROLE and ei.name not in [k for k in enums.Role.__members__ if 'R' + re.search(r"\d", i.name).group(0) in k]) or \
					(eg == enums.Group.WEAPON and ei.name not in [k for k in enums.Weapon.__members__ if 'W' + re.search(r"\d", i.name).group(0) in k]):
					await common.try_item(uid, i, mul, **kwargs)  # 还原
					return common.mt(97, '兑换碎片类型不匹配')
				else:
					seg_data = await (common.try_weapon(uid, ei, seg, **kwargs) if eg == enums.Group.WEAPON else common.try_role(uid, ei, seg, **kwargs))
					return common.mt(3, 'success', {'remaining': {'item': f"{iid}:{iq}", 'eitem': f"{eid}:{seg_data}"}, 'reward': {'item': f"{iid}:{mul}", 'eitem': f"{eid}:{seg}"}})
			elif i in SCROLL:
				eg, ei, eq = enums.Group.ITEM, SCROLL[i], mul//3
				_, _eq = await common.try_item(uid, ei, eq, **kwargs)
				return common.mt(4, 'success', {'remaining': {'item': f"{iid}:{iq}", 'eitem': f"{eg}:{ei}:{_eq}"}, 'reward': {'item': f"{iid}:{mul}", 'eitem': f"{eg}:{ei}:{eq}"}})
			else:
				await common.try_item(uid, i, mul, **kwargs)  # 还原
				return common.mt(98, '兑换成品类型错误')
	else:
		return common.mt(99, f'意外消耗品{iid}')


async def config(uid, **kwargs):
	return common.mt(0, 'success', {'config': kwargs['config']['package']})


#  ######################################### 私有 ##########################################
async def update_item(uid, mid, bnum, **kwargs):
	exp_info = await stage.increase_exp(uid, 0, **kwargs)
	vnum = exp_info['level'] * bnum
	_, rnum = await common.try_item(uid, enums.Item(mid), vnum, **kwargs)
	return exp_info, rnum, vnum


async def update_progress(uid, mid, bnum, **kwargs):
	if mid == 'exp':
		vnum = (await stage.increase_exp(uid, 0, **kwargs))['level'] * bnum
		exp_info = await stage.increase_exp(uid, vnum, **kwargs)
	else:
		vnum = (await vip.increase_exp(uid, 0, **kwargs))['level'] * bnum
		exp_info = await vip.increase_exp(uid, vnum, **kwargs)
	return exp_info, exp_info['exp'], vnum


SQL_TABLE = {'item': update_item, 'progress': update_progress}
