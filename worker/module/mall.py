'''
task.py
'''

from module import enums
from module import common
from module import vip
from datetime import datetime
import time
import secrets
# secrets.randbits

RMB_LIMIT = {
	"VIP_CARD_NORMAL": 26,
	"VIP_CARD_ULTIMATE": 27,
	"VIP_CARD_PERMANENT": 28,
	"DIAMOND_MIN": 5,
	"DIAMOND_SMALL": 5,
	"DIAMOND_LARGE": 5,
	"DIAMOND_PLENTY": 5,
	"DIAMOND_BAG": 5,
	"EXPERIENCE_POTION_MIN": 9,
	"EXPERIENCE_POTION_SMALL": 9,
	"EXPERIENCE_POTION_LARGE": 9,
	"EXPERIENCE_POTION_PLENTY": 9,
	"EXPERIENCE_POTION_BAG": 9,
	"ENERGY_POTION_MIN": 10,
	"ENERGY_POTION_SMALL": 10,
	"ENERGY_POTION_LARGE": 10,
	"ENERGY_POTION_PLENTY": 10,
	"ENERGY_POTION_BAG": 10,
	"IRON_MIN": 2,
	"IRON_SMALL": 2,
	"IRON_LARGE": 2,
	"IRON_PLENTY": 2,
	"IRON_BAG": 2,
	"SKILL_SCROLL_10_MIN": 6,
	"SKILL_SCROLL_10_SMALL": 6,
	"SKILL_SCROLL_10_LARGE": 6,
	"SKILL_SCROLL_10_PLENTY": 6,
	"SKILL_SCROLL_10_BAG": 6,
	"SKILL_SCROLL_30_MIN": 7,
	"SKILL_SCROLL_30_SMALL": 7,
	"SKILL_SCROLL_30_LARGE": 7,
	"SKILL_SCROLL_30_PLENTY": 7,
	"SKILL_SCROLL_30_BAG": 7,
	"SKILL_SCROLL_100_MIN": 8,
	"SKILL_SCROLL_100_SMALL": 8,
	"SKILL_SCROLL_100_LARGE": 8,
	"SKILL_SCROLL_100_PLENTY": 8,
	"SKILL_SCROLL_100_BAG": 8,
	"SUMMON_SCROLL_BASIC_MIN": 11,
	"SUMMON_SCROLL_BASIC_SMALL": 11,
	"SUMMON_SCROLL_BASIC_LARGE": 11,
	"SUMMON_SCROLL_BASIC_PLENTY": 11,
	"SUMMON_SCROLL_BASIC_BAG": 11,
	"SUMMON_SCROLL_PRO_MIN": 12,
	"SUMMON_SCROLL_PRO_SMALL": 12,
	"SUMMON_SCROLL_PRO_LARGE": 12,
	"SUMMON_SCROLL_PRO_PLENTY": 12,
	"SUMMON_SCROLL_PRO_BAG": 12,
	"SUMMON_SCROLL_PROPHET_MIN": 13,
	"SUMMON_SCROLL_PROPHET_SMALL": 13,
	"SUMMON_SCROLL_PROPHET_LARGE": 13,
	"SUMMON_SCROLL_PROPHET_PLENTY": 13,
	"SUMMON_SCROLL_PROPHET_BAG": 13,
	"FORTUNE_WHEEL_BASIC_MIN": 14,
	"FORTUNE_WHEEL_BASIC_SMALL": 14,
	"FORTUNE_WHEEL_BASIC_LARGE": 14,
	"FORTUNE_WHEEL_BASIC_PLENTY": 14,
	"FORTUNE_WHEEL_BASIC_BAG": 14,
	"FORTUNE_WHEEL_PRO_MIN": 15,
	"FORTUNE_WHEEL_PRO_SMALL": 15,
	"FORTUNE_WHEEL_PRO_LARGE": 15,
	"FORTUNE_WHEEL_PRO_PLENTY": 15,
	"FORTUNE_WHEEL_PRO_BAG": 15,
	"COIN_CARD_MIN": 18,
	"COIN_CARD_SMALL": 18,
	"COIN_CARD_LARGE": 18,
	"COIN_CARD_PLENTY": 18,
	"COIN_CARD_BAG": 18,
	"EXP_CARD_MIN": 19,
	"EXP_CARD_SMALL": 19,
	"EXP_CARD_LARGE": 19,
	"EXP_CARD_PLENTY": 19,
	"EXP_CARD_BAG": 19,
	"FOOD_CARD_MIN": 20,
	"FOOD_CARD_SMALL": 20,
	"FOOD_CARD_LARGE": 20,
	"FOOD_CARD_PLENTY": 20,
	"FOOD_CARD_BAG": 20,
	"MINE_CARD_MIN": 21,
	"MINE_CARD_SMALL": 21,
	"MINE_CARD_LARGE": 21,
	"MINE_CARD_PLENTY": 21,
	"MINE_CARD_BAG": 21,
	"CRYSTAL_CARD_MIN": 22,
	"CRYSTAL_CARD_SMALL": 22,
	"CRYSTAL_CARD_LARGE": 22,
	"CRYSTAL_CARD_PLENTY": 22,
	"CRYSTAL_CARD_BAG": 22,
	"DIAMOND_CARD_MIN": 23,
	"DIAMOND_CARD_SMALL": 23,
	"DIAMOND_CARD_LARGE": 23,
	"DIAMOND_CARD_PLENTY": 23,
	"DIAMOND_CARD_BAG": 23,
}


async def purchase_vip_card(pid, order_id, channel, user_name, currency, **kwargs):
	if pid not in RMB_LIMIT.keys(): return common.mt(99, "pid error")
	if RMB_LIMIT[pid] not in []: return common.mt(99, "pid error")


async def exchange(uid, eid, **kwargs):
	data = await common.execute(f'SELECT uid FROM mall WHERE oid="{eid}";', mall=True, **kwargs)
	if data == (): return common.mt(99, '')
	if data[0][0] != uid: return common.mt(98, '')

######################################################### 私有 #########################################################
async def rmb_mall(pid, order_id, channel, user_name, currency, **kwargs):
	"""
	参数详解：
	pid: 道具道具内部识别id
	order_id: 订单号
	channel: 渠道名字
	user_name: 用户名
	currency: 购买币种
	数据返回格式：
	0 - success
	96 - 物品{iid}礼包{gty}类型缺失商品数量
	97 - 物品{iid}没有礼包{gty}类型
	98 - 没有出售此物品{iid}
	99 - 物品类型错误{ity}
	"""
	if pid not in RMB_LIMIT.keys(): return common.mt(98, "pid error")
	config = kwargs['config']['mall'].get(pid, False)
	if not config: return common.mt(97, "config error")
	uid = await common.get_uid(user_name, **kwargs)
	if uid == "": return common.mt(99, "username error")
	if config["repeatable"] == "n":
		data = (await vip.buy_card(uid, RMB_LIMIT[pid], **kwargs))["data"]
	else:
		_, qty = await common.try_item(uid, enums.Item(RMB_LIMIT[pid]), int(config["quantity"]), **kwargs)
		data = {'remaining': {'iid': RMB_LIMIT[pid], 'qty': qty}, 'reward': {'iid': RMB_LIMIT[pid], 'qty': config["quantity"]}}
	await common.execute(f'INSERT INTO mall(oid, world, uid, username, currency, cqty, mid, mqty, channel, time, repeatable, receive) \
							VALUES ("{order_id}", "{kwargs["world"]}", "{uid}", "{user_name}", "{currency}", "{config["price"][currency]}", \
							"{RMB_LIMIT[pid]}", "{config["quantity"]}", "{channel}", "{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}", \
							"{config["repeatable"]}", 1);', mall=True, **kwargs)
	return common.mt(0, 'success', data)


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


def decode_key(key):
	"""
	key = 'uid:consume:5:1:1'
	"""
	uid, ity, iid, gty, qty = [v if i < 4 else int(v) for i, v in enumerate(key.split('_'))]
	return uid, ity, iid, gty, qty
