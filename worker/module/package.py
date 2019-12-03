'''
package.py
'''

from module import enums
from module import common
from module import stage


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


async def config(uid, **kwargs):
	return common.mt(0, 'success', {'config': kwargs['config']['package']['exchange_card']})

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
