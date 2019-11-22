'''
task.py
'''

from module import enums
from module import common
from module import vip
from datetime import datetime
import time
from module import task




######################################################### 私有 #########################################################

async def mall(uid, cty, ity, iid, gty, qty, **kwargs):
	"""
	参数详解：
	cty：消耗品类型       包含 钻石diamond，金币coin，人民币rmb
	ity：物品类型         包含 消耗品consume，装饰品decoration，卡片物品card
	iid：物品id           包含 item枚举下的所有可以购买的物品id
	gty：礼包类型         包含 1个购买"1"，10个购买"10"，30个购买"30"
	qty：礼包购买数量     代表购买几个相同的礼包
	配置结构：
	cty:(diamond、coin、rmb)
		- cid(消耗品的item id，rmb为-1)
		- merchandise:(商品信息)
			- ity:(物品类型暂时分为 消耗品consume和装饰品decoration)
				- iid:(物品iid，根据item枚举设置)
					- gty:(礼包类型，暂时分为1个购买"1"，10个购买"10"，30个购买"30")
						c_quantity(消耗品数量)
						m_quantity(商品数量)
	数据返回格式：
	0 -
	96 -
	97 - 此方法非人民币商城方法,消耗品类型错误{cty}
	98 - {cty}商城配置文件缺失cid关键字
	99 - 消耗品类型错误{cty}
	"""
	config = kwargs['config']['mall'].get(cty, False)
	if not config: return common.mt(99, f'消耗品类型错误{cty}')
	cid = config.get('cid', -999)
	if cid == -999: return common.mt(98, f'{cty}商城配置文件缺失cid关键字')
	if cid == -1: return common.mt(97, f'此方法非人民币商城方法,消耗品类型错误{cty}')
	# 以下是钻石商城和金币商城通用代码
	return common.mt(0, '暂未完成')

	# scroll_config = self._mall_config["scroll"]
	# if quantity <= 0:
	# 	return self._message_typesetting(status=99, message="The quantity purchased must be a positive integer")
	# mall_scroll_type = scroll_config["scroll_type"]
	# if scroll_type not in mall_scroll_type:
	# 	return self._message_typesetting(status=98, message="This scroll cannot be purchased")
	# mall_purchase_type = scroll_config[scroll_type]["purchase_type"]
	# if purchase_type not in mall_purchase_type:
	# 	return self._message_typesetting(status=97, message="No such purchase type")
	# mall_consume = scroll_config[scroll_type][purchase_type]["consume"]
	# mall_quantity = -1 * scroll_config[scroll_type][purchase_type]["quantity"] * quantity
	# mall_scroll_quantity = scroll_config[scroll_type][purchase_type]["scroll_quantity"] * quantity
	# consume_data = await eval(f"self.try_{mall_consume}({world}, {unique_id}, {mall_quantity})")
	# if consume_data["status"] == 1:
	# 	return self._message_typesetting(status=96, message=f"Insufficient {mall_consume}")
	# await self._execute_statement_update(world=world, statement=f"update player set {scroll_type}={scroll_type}+{mall_scroll_quantity} where unique_id='{unique_id}'")
	# scroll_quantity = await self._get_material(world=world, unique_id=unique_id, material=scroll_type)
	# return self._message_typesetting(status=0, message="Purchase success", data={"remaining": {mall_consume: consume_data["remaining"], scroll_type: scroll_quantity}, "reward": {scroll_type: mall_scroll_quantity}})


async def rmb_mall(key, **kwargs):
	"""
	参数详解：
	cty：消耗品类型       包含 钻石diamond，金币coin，人民币rmb
	ity：物品类型         包含 消耗品consume，装饰品decoration，卡片物品card
	iid：物品id           包含 item枚举下的所有可以购买的物品id
	gty：礼包类型         包含 1个购买"1"，10个购买"10"，30个购买"30"
	qty：礼包购买数量     代表购买几个相同的礼包
	配置结构：
	cty:(diamond、coin、rmb)
		- cid(消耗品的item id，rmb为-1)
		- merchandise:(商品信息)
			- ity:(物品类型暂时分为 消耗品consume和装饰品decoration)
				- iid:(物品iid，根据item枚举设置)
					- gty:(礼包类型，暂时分为1个购买"1"，10个购买"10"，30个购买"30")
						c_quantity(消耗品数量)
						m_quantity(商品数量)
	数据返回格式：
	0 - Purchase success
	96 - 物品{iid}礼包{gty}类型缺失商品数量
	97 - 物品{iid}没有礼包{gty}类型
	98 - 没有出售此物品{iid}
	99 - 物品类型错误{ity}
	"""
	uid, ity, iid, gty, qty = decode_key(key)  # str, str, str, int
	config = kwargs['config']['mall']['rmb']['merchandise'].get(ity, False)
	if not config: return common.mt(99, f'物品类型错误{ity}')
	merchandise = config.get(iid, False)
	if not merchandise: return common.mt(98, f'没有出售此物品{iid}')
	commodity = merchandise.get(gty, False)
	if not commodity: return common.mt(97, f'物品{iid}没有礼包{gty}类型')
	m_quantity = commodity.get('m_quantity', False)
	if not m_quantity: return common.mt(96, f'物品{iid}礼包{gty}类型缺失商品数量')
	qty = abs(qty * m_quantity)
	if ity == 'card':
		for i in qty: await vip.buy_card(uid, int(iid))


def decode_key(key):
	"""
	key = 'uid:consume:5:1:1'
	"""
	uid, ity, iid, gty, qty = [v if i < 4 else int(v) for i, v in enumerate(key.split(':'))]
	return uid, ity, iid, gty, qty
