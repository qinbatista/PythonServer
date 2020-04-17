'''
author:hy
task.py
'''
from datetime import datetime
from module import enums
from module import common
from module import vip
from module import stage
from module import task


# 99 - You have already signed in today
# 98 - no day missing
# 97 - materials insufficient
# 0 - success


async def supplement(uid, **kwargs):
    """补签"""
    config = kwargs['config']['check_in']
    now = datetime.now(common.TZ_SH)
    today = now.day
    nd = await common.execute(f'select date from check_in where uid="{uid}" '
                              f'and date like "{now.strftime("%Y-%m-")}%"', **kwargs)
    mul = today - len(nd)
    if mul == 0: return common.mt(98, 'no day missing')
    can, cmw = await common.consume_items(uid, ','.join(config["consume"]), mul=mul, **kwargs)
    if not can:
        return common.mt(97, 'materials insufficient')
    results = {'supplement': {}}
    results['remain'], results['reward'] = stage.rm_rw(cmw)
    for d in range(1, today):
        day = f'{d}'.zfill(2)
        result = await sign(uid, day, **kwargs)
        results['supplement'].update({day: result["data"]})
    return common.mt(0, 'Successful signing', results)


async def sign(uid, day=None, **kwargs):
    """每日签到"""
    # 0 - Sign-in success
    # 99 - You have already signed in today
    tim = datetime.now(common.TZ_SH).strftime('%Y-%m-%d' if day is None else f'%Y-%m-{day}')
    nd = await common.execute(f'SELECT * FROM check_in WHERE uid="{uid}"'
                              f' AND date="{tim}"', **kwargs)
    if nd != (): return common.mt(99, 'You have already signed in today')
    wd = int(tim[-2:]) % 7
    vds = await vip.increase_exp(uid, 0, **kwargs)
    mul = 1 if wd >= vds['level'] else 2
    rms = [kwargs['config']['check_in']['reward'][f'{wd}']]
    results = {}
    await stage.rw_common(uid, rms, results, mul=mul, **kwargs)
    await common.execute(f'INSERT INTO check_in(uid, date, reward) '
                         f'VALUES("{uid}", "{tim}", 1)', **kwargs)
    await task.record(uid, enums.Task.CHECK_IN, **kwargs)
    return common.mt(0, 'Sign-in success', results)


async def all(uid, **kwargs):
    """获取所有签到情况"""
    # 0 - Successfully obtained all check-in status
    now = datetime.now(common.TZ_SH)
    cds = await common.execute(f'SELECT * FROM check_in WHERE uid="{uid}" '
                               f'AND date LIKE "{now.strftime("%Y-%m-")}%"', **kwargs)
    history = {d[1][-2:]: {'date': d[1], 'reward': d[2]} for d in cds}
    return common.mt(0, 'Successfully obtained all check-in status this month',
                     {'today': now.day, 'cd': common.remaining_cd(),
                      'history': history})
