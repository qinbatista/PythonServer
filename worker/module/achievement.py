'''
achievement.py
'''

from module import enums
from module import common
from module import mail
from datetime import datetime


async def get_all(uid, **kwargs):
    await record(uid, enums.Achievement.TOTAL_LOGIN, tid=enums.Timer.CONTINUOUS_LOGIN, **kwargs)
    ads = await common.execute(f'SELECT aid, value, reward FROM achievement WHERE uid = "{uid}";', **kwargs)
    if ads == (): return common.mt(0, 'success', {'achievements': []})
    return common.mt(0, 'success', {
        'achievements': [{'aid': a[0], 'value': a[1], 'reward': a[2]}
                         for a in ads]})


async def record(uid, aid, value=1, reward=0, tid=None, **kwargs):
    if value <= 0:
        return common.mt(0, f"record:{aid} failure, 记录值不能为负数")
    if tid is not None:
        now = datetime.now(tz=common.TZ_SH)
        tim = await common.get_timer(uid, tid=tid, **kwargs)
        tim = now if tim is None else tim
        if aid == enums.Achievement.TOTAL_LOGIN:
            await common.set_achievement(uid, enums.Achievement.KEEPING_LOGIN,
                                         value=1, reward=reward,
                                         reset=(now - tim).days >= 2, **kwargs)
        await common.set_timer(uid, tid, now, **kwargs)
    await common.set_achievement(uid, aid, value, reward=reward, **kwargs)
    return common.mt(0, f"record:{aid} success")


async def get_reward(uid, aid, **kwargs):
    if aid not in enums.Achievement._value2member_map_.keys(): return common.mt(97, 'Aid does not exist')
    config = kwargs["config"]["achievement"][str.lower(enums.Achievement(aid).name)]
    quantity = config["quantity"]
    amount = config["diamond"]
    data = await common.execute(f'SELECT value, reward FROM achievement WHERE uid = "{uid}" AND aid = "{aid}"',**kwargs)
    if data == (): return common.mt(98, f'no reward for this achievement:{enums.Achievement(aid).name}')
    if len(quantity) != len(amount): return common.mt(98, 'data base problem, achievement configuration is not match')
    for index, my_quantity in enumerate(quantity):
        if data[0][1] < my_quantity <= data[0][0]:  # reward是领奖时的成就次数，value是完成成就的次数
            _, remaining = await common.try_item(uid, enums.Item.DIAMOND, amount[index], **kwargs)
            await common.execute_update(f'UPDATE achievement set reward = {my_quantity} WHERE uid = "{uid}" AND aid = "{aid}";', **kwargs)
            return common.mt(0, 'get reward success',{"remaining": {"item_id": 5, "item_value": remaining, "aid": aid, "value": data[0][0]},"reward": {"item_id": 5, "item_value": amount[index], "aid": aid, "value": quantity[index]}})
    return common.mt(99, f'no reward for this achievement:{enums.Achievement(aid).name}')
