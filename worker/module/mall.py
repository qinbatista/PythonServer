'''
task.py
'''

from module import enums
from module import common
from module import vip
from datetime import datetime
import secrets

# secrets.randbits

RMB_LIMIT = {
    "VIP_CARD_NORMAL": enums.Item.VIP_CARD_MIN,
    "VIP_CARD_ULTIMATE": enums.Item.VIP_CARD_MAX,
    "VIP_CARD_PERMANENT": enums.Item.VIP_CARD_PERPETUAL,
    "DIAMOND_MIN": enums.Item.DIAMOND,
    "DIAMOND_SMALL": enums.Item.DIAMOND,
    "DIAMOND_LARGE": enums.Item.DIAMOND,
    "DIAMOND_PLENTY": enums.Item.DIAMOND,
    "DIAMOND_BAG": enums.Item.DIAMOND,
    "EXP_POINT_MIN": enums.Item.EXP_POINT,
    "EXP_POINT_SMALL": enums.Item.EXP_POINT,
    "EXP_POINT_LARGE": enums.Item.EXP_POINT,
    "EXP_POINT_PLENTY": enums.Item.EXP_POINT,
    "EXP_POINT_BAG": enums.Item.EXP_POINT,
    "ENERGY_POTION_MIN": enums.Item.ENERGY_POTION_S,
    "ENERGY_POTION_SMALL": enums.Item.ENERGY_POTION_S,
    "ENERGY_POTION_LARGE": enums.Item.ENERGY_POTION_S,
    "ENERGY_POTION_PLENTY": enums.Item.ENERGY_POTION_S,
    "ENERGY_POTION_BAG": enums.Item.ENERGY_POTION_S,
    "IRON_MIN": enums.Item.IRON,
    "IRON_SMALL": enums.Item.IRON,
    "IRON_LARGE": enums.Item.IRON,
    "IRON_PLENTY": enums.Item.IRON,
    "IRON_BAG": enums.Item.IRON,
    "SKILL_SCROLL_10_MIN": enums.Item.SKILL_SCROLL_10,
    "SKILL_SCROLL_10_SMALL": enums.Item.SKILL_SCROLL_10,
    "SKILL_SCROLL_10_LARGE": enums.Item.SKILL_SCROLL_10,
    "SKILL_SCROLL_10_PLENTY": enums.Item.SKILL_SCROLL_10,
    "SKILL_SCROLL_10_BAG": enums.Item.SKILL_SCROLL_10,
    "SKILL_SCROLL_30_MIN": enums.Item.SKILL_SCROLL_30,
    "SKILL_SCROLL_30_SMALL": enums.Item.SKILL_SCROLL_30,
    "SKILL_SCROLL_30_LARGE": enums.Item.SKILL_SCROLL_30,
    "SKILL_SCROLL_30_PLENTY": enums.Item.SKILL_SCROLL_30,
    "SKILL_SCROLL_30_BAG": enums.Item.SKILL_SCROLL_30,
    "SKILL_SCROLL_100_MIN": enums.Item.SKILL_SCROLL_100,
    "SKILL_SCROLL_100_SMALL": enums.Item.SKILL_SCROLL_100,
    "SKILL_SCROLL_100_LARGE": enums.Item.SKILL_SCROLL_100,
    "SKILL_SCROLL_100_PLENTY": enums.Item.SKILL_SCROLL_100,
    "SKILL_SCROLL_100_BAG": enums.Item.SKILL_SCROLL_100,
    "SUMMON_SCROLL_BASIC_MIN": enums.Item.SUMMON_SCROLL_BASIC,
    "SUMMON_SCROLL_BASIC_SMALL": enums.Item.SUMMON_SCROLL_BASIC,
    "SUMMON_SCROLL_BASIC_LARGE": enums.Item.SUMMON_SCROLL_BASIC,
    "SUMMON_SCROLL_BASIC_PLENTY": enums.Item.SUMMON_SCROLL_BASIC,
    "SUMMON_SCROLL_BASIC_BAG": enums.Item.SUMMON_SCROLL_BASIC,
    "SUMMON_SCROLL_PRO_MIN": enums.Item.SUMMON_SCROLL_PRO,
    "SUMMON_SCROLL_PRO_SMALL": enums.Item.SUMMON_SCROLL_PRO,
    "SUMMON_SCROLL_PRO_LARGE": enums.Item.SUMMON_SCROLL_PRO,
    "SUMMON_SCROLL_PRO_PLENTY": enums.Item.SUMMON_SCROLL_PRO,
    "SUMMON_SCROLL_PRO_BAG": enums.Item.SUMMON_SCROLL_PRO,
    "SUMMON_SCROLL_PROPHET_MIN": enums.Item.SUMMON_SCROLL_PROPHET,
    "SUMMON_SCROLL_PROPHET_SMALL": enums.Item.SUMMON_SCROLL_PROPHET,
    "SUMMON_SCROLL_PROPHET_LARGE": enums.Item.SUMMON_SCROLL_PROPHET,
    "SUMMON_SCROLL_PROPHET_PLENTY": enums.Item.SUMMON_SCROLL_PROPHET,
    "SUMMON_SCROLL_PROPHET_BAG": enums.Item.SUMMON_SCROLL_PROPHET,
    "FORTUNE_WHEEL_BASIC_MIN": enums.Item.FORTUNE_WHEEL_BASIC,
    "FORTUNE_WHEEL_BASIC_SMALL": enums.Item.FORTUNE_WHEEL_BASIC,
    "FORTUNE_WHEEL_BASIC_LARGE": enums.Item.FORTUNE_WHEEL_BASIC,
    "FORTUNE_WHEEL_BASIC_PLENTY": enums.Item.FORTUNE_WHEEL_BASIC,
    "FORTUNE_WHEEL_BASIC_BAG": enums.Item.FORTUNE_WHEEL_BASIC,
    "FORTUNE_WHEEL_PRO_MIN": enums.Item.FORTUNE_WHEEL_PRO,
    "FORTUNE_WHEEL_PRO_SMALL": enums.Item.FORTUNE_WHEEL_PRO,
    "FORTUNE_WHEEL_PRO_LARGE": enums.Item.FORTUNE_WHEEL_PRO,
    "FORTUNE_WHEEL_PRO_PLENTY": enums.Item.FORTUNE_WHEEL_PRO,
    "FORTUNE_WHEEL_PRO_BAG": enums.Item.FORTUNE_WHEEL_PRO,
    "COIN_CARD_MIN": enums.Item.COIN_CARD,
    "COIN_CARD_SMALL": enums.Item.COIN_CARD,
    "COIN_CARD_LARGE": enums.Item.COIN_CARD,
    "COIN_CARD_PLENTY": enums.Item.COIN_CARD,
    "COIN_CARD_BAG": enums.Item.COIN_CARD,
    "EXP_CARD_MIN": enums.Item.EXP_CARD,
    "EXP_CARD_SMALL": enums.Item.EXP_CARD,
    "EXP_CARD_LARGE": enums.Item.EXP_CARD,
    "EXP_CARD_PLENTY": enums.Item.EXP_CARD,
    "EXP_CARD_BAG": enums.Item.EXP_CARD,
    "FOOD_CARD_MIN": enums.Item.FOOD_CARD,
    "FOOD_CARD_SMALL": enums.Item.FOOD_CARD,
    "FOOD_CARD_LARGE": enums.Item.FOOD_CARD,
    "FOOD_CARD_PLENTY": enums.Item.FOOD_CARD,
    "FOOD_CARD_BAG": enums.Item.FOOD_CARD,
    "MINE_CARD_MIN": enums.Item.MINE_CARD,
    "MINE_CARD_SMALL": enums.Item.MINE_CARD,
    "MINE_CARD_LARGE": enums.Item.MINE_CARD,
    "MINE_CARD_PLENTY": enums.Item.MINE_CARD,
    "MINE_CARD_BAG": enums.Item.MINE_CARD,
    "CRYSTAL_CARD_MIN": enums.Item.CRYSTAL_CARD,
    "CRYSTAL_CARD_SMALL": enums.Item.CRYSTAL_CARD,
    "CRYSTAL_CARD_LARGE": enums.Item.CRYSTAL_CARD,
    "CRYSTAL_CARD_PLENTY": enums.Item.CRYSTAL_CARD,
    "CRYSTAL_CARD_BAG": enums.Item.CRYSTAL_CARD,
    "DIAMOND_CARD_MIN": enums.Item.DIAMOND_CARD,
    "DIAMOND_CARD_SMALL": enums.Item.DIAMOND_CARD,
    "DIAMOND_CARD_LARGE": enums.Item.DIAMOND_CARD,
    "DIAMOND_CARD_PLENTY": enums.Item.DIAMOND_CARD,
    "DIAMOND_CARD_BAG": enums.Item.DIAMOND_CARD,
}


async def purchase_vip_card(pid, oid, channel, user, currency,
                            **kwargs):
    if pid not in RMB_LIMIT.keys():
        return common.mt(98, "pid error")
    if RMB_LIMIT[pid] not in [enums.Item.VIP_CARD_MIN, enums.Item.VIP_CARD_MAX,
                              enums.Item.VIP_CARD_PERPETUAL]:
        return common.mt(96, "你购买的不是月卡")
    return await rmb_mall(pid, oid, channel, user, currency, **kwargs)


async def purchase_diamond(pid, oid, channel, user, currency,
                           **kwargs):
    if pid not in RMB_LIMIT.keys():
        return common.mt(98, "pid error")
    if RMB_LIMIT[pid] != enums.Item.DIAMOND:
        return common.mt(96, "你购买的不是钻石")
    return await rmb_mall(pid, oid, channel, user, currency, **kwargs)


async def purchase_skill_scroll(pid, oid, channel, user, currency,
                                **kwargs):
    if pid not in RMB_LIMIT.keys():
        return common.mt(98, "pid error")
    if RMB_LIMIT[pid] not in [enums.Item.SKILL_SCROLL_10,
                              enums.Item.SKILL_SCROLL_30,
                              enums.Item.SKILL_SCROLL_100]:
        return common.mt(96, "你购买的不是技能卷轴")
    return await rmb_mall(pid, oid, channel, user, currency, **kwargs)


async def purchase_summon_scroll(pid, oid, channel, user, currency,
                                 **kwargs):
    if pid not in RMB_LIMIT.keys():
        return common.mt(98, "pid error")
    if RMB_LIMIT[pid] not in [enums.Item.SUMMON_SCROLL_BASIC,
                              enums.Item.SUMMON_SCROLL_PRO,
                              enums.Item.SUMMON_SCROLL_PROPHET]:
        return common.mt(96, "你购买的不是召唤卷轴")
    return await rmb_mall(pid, oid, channel, user, currency, **kwargs)


async def purchase_resource_card(pid, oid, channel, user, currency,
                                 **kwargs):
    if pid not in RMB_LIMIT.keys():
        return common.mt(98, "pid error")
    if RMB_LIMIT[pid] not in [enums.Item.COIN_CARD, enums.Item.EXP_CARD,
                              enums.Item.FOOD_CARD,
                              enums.Item.MINE_CARD, enums.Item.CRYSTAL_CARD,
                              enums.Item.DIAMOND_CARD]:
        return common.mt(96, "你购买的不是资源卡")
    return await rmb_mall(pid, oid, channel, user, currency, **kwargs)


async def exchange(uid, gid, eid, **kwargs):
    eds = await common.execute(
        f'SELECT pid, etime, receive FROM exchange WHERE gid="{gid}" AND eid="{eid}";',
        exchange=True, **kwargs)
    if eds == ():
        return common.mt(99, '兑换码不存在')
    pid, etm, receive = eds[0]
    if receive <= 0:
        return common.mt(98, '兑换码已兑换完')
    if datetime.strptime(etm, "%Y-%m-%d %H:%M:%S").replace(
            tzinfo=common.TZ_SH) < datetime.now(tz=common.TZ_SH):
        return common.mt(97, '兑换码已过期')
    if pid not in RMB_LIMIT.keys():
        return common.mt(96, "pid error")
    config = kwargs['config']['mall'].get(pid)
    if config is None:
        return common.mt(95, "配置文件未更新")
    data = {"vip_card": {}, "item": {}}
    if config["repeatable"] == "n":
        data["vip_card"] = \
            (await vip.buy_card(uid, RMB_LIMIT[pid].value, **kwargs))["data"]
    else:
        _, qty = await common.try_item(uid, RMB_LIMIT[pid],
                                       int(config["quantity"]), **kwargs)
        data["item"] = {'remaining': {'iid': RMB_LIMIT[pid], 'qty': qty},
                        'reward': {'iid': RMB_LIMIT[pid],
                                   'qty': config["quantity"]}}
    data["etime"] = etm
    data["receive"] = receive - 1
    await common.execute(
        f'UPDATE exchange SET receive="{receive - 1}" WHERE gid="{gid}" AND eid="{eid}";',
        exchange=True, **kwargs)
    return common.mt(0, 'success', data)


# ######################################################## 私有 #########################################################
async def rmb_mall(pid, oid, channel, user, currency, **kwargs):
    """
    参数详解：
    pid: 道具道具内部识别id
    oid: 订单号
    channel: 渠道名字
    user: 用户名
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
    uid = await common.get_uid(user, **kwargs)
    if uid == "": return common.mt(99, "username error")
    await common.execute(
        f'INSERT INTO mall(oid, world, uid, username, currency, cqty, mid, mqty, channel, time, repeatable, receive) '
        f'VALUES ("{oid}", "{kwargs["world"]}", "{uid}", "{user}", "{currency}", "{config["price"][currency]}",'
        f'"{RMB_LIMIT[pid]}", "{config["quantity"]}", "{channel}", "{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}", '
        f'"{config["repeatable"]}", 1);', mall=True, **kwargs)
    if config["repeatable"] == "n":
        data = (await vip.buy_card(uid, RMB_LIMIT[pid].value, **kwargs))[
            "data"]
        return common.mt(1, 'success', data)
    else:
        _, qty = await common.try_item(uid, RMB_LIMIT[pid],
                                       int(config["quantity"]), **kwargs)
        data = {'remaining': {'iid': RMB_LIMIT[pid], 'qty': qty},
                'reward': {'iid': RMB_LIMIT[pid], 'qty': config["quantity"]}}
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
    if not config:
        return common.mt(99, f'消耗品类型错误{cty}')
    cid = config.get('cid', -999)
    if cid == -999:
        return common.mt(98, f'{cty}商城配置文件缺失cid关键字')
    if cid == -1:
        return common.mt(97, f'此方法非人民币商城方法,消耗品类型错误{cty}')
    # 以下是钻石商城和金币商城通用代码
    return common.mt(0, '暂未完成')


def decode_key(key):
    """
    key = 'uid:consume:5:1:1'
    """
    uid, ity, iid, gty, qty = [v if i < 4 else int(v) for i, v in
                               enumerate(key.split('_'))]
    return uid, ity, iid, gty, qty
