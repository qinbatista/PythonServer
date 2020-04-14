'''
achievement.py
'''

from module import enums
from module import common
from module import mail
from datetime import datetime, timedelta


async def get_all(uid, **kwargs):
    now = datetime.now(tz=common.TZ_SH)
    tim = await common.get_timer(uid, enums.Timer.LOGIN, **kwargs)
    tim = now - timedelta(days=1) if tim is None else tim
    if now.day != tim.day:
        await record(uid, enums.Achievement.TOTAL_LOGIN, **kwargs)
        await common.set_timer(uid, enums.Timer.LOGIN, now, **kwargs)
    ads = await common.execute(f'SELECT aid, value, reward FROM achievement WHERE uid = "{uid}";', **kwargs)
    if ads == (): return common.mt(0, 'success', {'achievements': []})
    return common.mt(0, 'success', {
        'achievements': [{'aid': a[0], 'value': a[1], 'reward': a[2]}
                         for a in ads]})


async def record(uid, aid, value=1, **kwargs):
    if value <= 0:
        return common.mt(0, f"record:{aid} failure, 记录值不能为负数")
    if aid == enums.Achievement.TOTAL_LOGIN:
        now = datetime.now(tz=common.TZ_SH)
        tid = enums.Timer.CONTINUOUS_LOGIN
        tim = await common.get_timer(uid, tid, **kwargs)
        tim = now if tim is None else tim
        await common.set_achievement(uid, enums.Achievement.KEEPING_LOGIN,
                                     value=1, reset=(now - tim).days >= 2,
                                     **kwargs)
        await common.set_timer(uid, tid, now, **kwargs)
    await common.set_achievement(uid, aid, value, **kwargs)
    return common.mt(0, f"record:{aid} success")


async def get_reward(uid, aid, **kwargs):
    if aid not in enums.Achievement._value2member_map_: return common.mt(97, 'Aid does not exist')
    config = kwargs["config"]["achievement"][f'{aid}']
    count = config["count"]
    qty = config["qty"]
    data = await common.execute(f'SELECT value, reward FROM achievement WHERE uid = "{uid}" AND aid = "{aid}"',**kwargs)
    if data == ():
        return common.mt(98, f'no reward for this achievement:{aid}')
    if len(count) != len(qty):
        return common.mt(98, 'data base problem, achievement configuration is not match')
    val, _rwv = data[0]
    for i, rwv in enumerate(count):
        if _rwv < rwv <= val:  # reward是领奖时的成就次数，value是完成成就的次数
            gid = enums.Group.ITEM
            iid = enums.Item.DIAMOND
            _, _qty = await common.try_item(uid, iid, qty[i], **kwargs)
            await common.execute(f'UPDATE achievement set reward = {rwv} WHERE uid = "{uid}" AND aid = "{aid}";', **kwargs)
            return common.mt(0, 'success',
                             {"remain": [f'{gid}:{iid}:{_qty}'],
                              "reward": [f'{gid}:{iid}:{qty[i]}'],
                              "achievement": f'{aid}:{val}:{rwv}'})
    return common.mt(99, f'no reward for this achievement:{aid}')
