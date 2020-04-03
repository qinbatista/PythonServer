'''
science.py
'''

from module import enums
from module import common
from module import task
from module import achievement
from module import summoning
from module import stage
from module import vip
from datetime import datetime, timedelta
import random
import asyncio


# 99 - insufficient level
# 98 - max level
# 97 - config does not exist
# 96 - materials insufficient
# 95 -
# 94 -
# 93 -
# 92 -
# 91 -
# 90 -
# 89 -
# 88 -
# 87 -
# 86 -
# 0 - success


async def infos(uid, **kwargs):
    # rn = (await common.execute(f'SELECT COUNT(*) FROM role WHERE uid="{uid}" AND star >= 1', **kwargs))[0][0]
    # wn = (await common.execute(f'SELECT COUNT(*) FROM weapon WHERE uid="{uid}" AND star >= 1', **kwargs))[0][0]
    science = await _all(uid, **kwargs)
    return common.mt(0, 'success', {'science': science})


# ################################# factory #################################
async def fr_up(uid, **kwargs):
    pid = enums.Science.FACTORY
    sid = enums.ScienceSub.ROLE
    return await _up(uid, pid, sid, **kwargs)


# ################################# private #################################
async def _up(uid, pid, sid, **kwargs):
    config = kwargs['config']['sciences'][f'{pid}'][f'{sid}']
    lv = (await stage.increase_exp(uid, 0, **kwargs))['level']
    if lv < config['constraint']['level']:
        return common.mt(99, 'insufficient level')
    _lv = await common.get_science(uid, pid, sid, **kwargs) + 1
    if _lv > len(config['consume'].keys()):
        return common.mt(98, 'max level')
    cms = config['consume'].get(f'{_lv}')
    if cms is None:
        return common.mt(97, 'config does not exist')
    can, cmw = await common.consume_items(uid, ','.join(cms), **kwargs)
    if not can:
        return common.mt(96, 'materials insufficient')
    await common.set_science(uid, pid, sid, _lv, **kwargs)
    results = {'science': await _all(uid, **kwargs), 'rws': {f'{pid}': {f'{sid}': 1}}}
    results['remain'], results['reward'] = stage.rm_rw(cmw)
    return common.mt(0, 'success', results)


async def _all(uid, **kwargs):
    sds = await common.execute(f'SELECT pid, sid, level FROM sciences WHERE uid="{uid}"', **kwargs)
    return {f'{p}': {f'{s}': l} for p, s, l in sds}


