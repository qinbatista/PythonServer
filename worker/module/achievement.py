'''
achievement.py
'''

from module import enums
from module import common
from module import mail
from datetime import datetime


async def get_all_achievement(uid, **kwargs):
    kwargs.update({"aid": enums.Achievement.TOTAL_LOGIN})
    await record_achievement(uid, **kwargs)
    achievement = await common.execute(f'SELECT aid, value, reward FROM achievement WHERE uid = "{uid}";', **kwargs)
    if achievement == (): return common.mt(0, 'success', {'achievements': []})
    return common.mt(0, 'success', {
        'achievements': [{'aid': a[0], 'value': a[1], 'reward': a[2]} for a in
                         achievement]})


async def record_achievement(uid, achievement_value=1, **kwargs):  # aid->enums.Achievement,value->string
    if kwargs["aid"] == enums.Achievement.TOTAL_LOGIN:
        current_time = datetime.now().strftime("%Y-%m-%d")
        await common.execute(f'INSERT INTO timer (uid, tid, time) VALUES ("{uid}",{enums.Timer.LOGIN_TIME},"{current_time}") ON DUPLICATE KEY UPDATE `time`= "{current_time}"',**kwargs)
        timer_data = await common.execute(f'SELECT time FROM timer WHERE uid = "{uid}" AND tid = "{enums.Timer.CONTINUOUS_LOGIN}";', **kwargs)
        if timer_data!=():
            difference_day = datetime.now() - datetime.strptime(timer_data[0][0], '%Y-%m-%d')
            if difference_day.days == 0:
                pass
            elif difference_day.days == 1:
                await common.execute(f'INSERT INTO achievement (uid, aid, value,reward) VALUES ("{uid}", {kwargs["aid"]}, {1},0) ON DUPLICATE KEY UPDATE `value`= `value`+{1}',**kwargs)
                await common.execute(f'INSERT INTO achievement (uid, aid, value,reward) VALUES ("{uid}",{enums.Achievement.KEEPING_LOGIN},{1},0) ON DUPLICATE KEY UPDATE `value`= `value`+{1}',**kwargs)
                await common.execute(f'INSERT INTO timer (uid, tid, time) VALUES ("{uid}",{enums.Timer.CONTINUOUS_LOGIN},"{current_time}") ON DUPLICATE KEY UPDATE `time`= "{current_time}"',**kwargs)
            elif difference_day.days >=2:
                await common.execute(f'INSERT INTO achievement (uid, aid, value,reward) VALUES ("{uid}", {kwargs["aid"]}, {1},0) ON DUPLICATE KEY UPDATE `value`= `value`+{1}',**kwargs)
                await common.execute(f'INSERT INTO achievement (uid, aid, value,reward) VALUES ("{uid}",{enums.Achievement.KEEPING_LOGIN},{1},0) ON DUPLICATE KEY UPDATE `value`= {1}',**kwargs)
                await common.execute(f'INSERT INTO timer (uid, tid, time) VALUES ("{uid}",{enums.Timer.CONTINUOUS_LOGIN},"{current_time}") ON DUPLICATE KEY UPDATE `time`= "{current_time}"',**kwargs)
        else:
            await common.execute(f'INSERT INTO achievement (uid, aid, value,reward) VALUES ("{uid}", {kwargs["aid"]}, {1},0) ON DUPLICATE KEY UPDATE `value`= `value`+{1}',**kwargs)
            await common.execute(f'INSERT INTO achievement (uid, aid, value,reward) VALUES ("{uid}", {enums.Achievement.KEEPING_LOGIN}, {1},0) ON DUPLICATE KEY UPDATE `value`= {1}',**kwargs)
            await common.execute(f'INSERT INTO timer (uid, tid, time) VALUES ("{uid}", {enums.Timer.CONTINUOUS_LOGIN}, "{current_time}") ON DUPLICATE KEY UPDATE `time`= "{current_time}"',**kwargs)
    else:
        if achievement_value <= 0: return common.mt(0, 'record:' + str(kwargs["aid"]) + " failure, 记录值不能为负数")
        await common.execute(f'INSERT INTO achievement (uid, aid, value,reward) VALUES ("{uid}", {kwargs["aid"]}, {achievement_value},0) ON DUPLICATE KEY UPDATE `value`= `value`+{achievement_value}',**kwargs)
    return common.mt(0, 'record:' + str(kwargs["aid"]) + " success")


async def check_achievement(uid, aid, value=1, reward=0, tid=None, **kwargs):
    now = datetime.now()
    if value <= 0:
        return common.mt(0, f"record:{aid} failure, 记录值不能为负数")
    if tid is not None:
        tim = await common.get_timer(uid, tid=tid, timeformat='%Y-%m-%d')
        tim = now if tim is not None else tim
        if aid == enums.Achievement.TOTAL_LOGIN:
            await common.update_achievement(uid, enums.Achievement.KEEPING_LOGIN,
                                            value=1, reward=reward,
                                            reset=(now - tim).days >= 2,
                                            **kwargs)
        await common.set_timer(uid, tid, now, timeformat='%Y-%m-%d')
    await common.update_achievement(uid, aid, value, reward=reward, **kwargs)
    return common.mt(0, f"record:{aid} success")


async def get_achievement_reward(uid, aid, **kwargs):
    if aid not in enums.Achievement._value2member_map_.keys(): return common.mt(97, 'Aid does not exist')
    config = kwargs["config"][str.lower(enums.Achievement(aid).name)]
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
