'''
author:hy
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
import contextlib
import random
import asyncio


# 99 - insufficient level
# 98 - max level
# 97 - config does not exist
# 96 - materials insufficient
# 95 - The level of science master is inadequate
# 94 - ssa error
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
    # rn = (await common.execute(f'SELECT COUNT(*) FROM role WHERE uid="{uid}"'
    #                            f' AND star >= 1', **kwargs))[0][0]
    # wn = (await common.execute(f'SELECT COUNT(*) FROM weapon WHERE uid="{uid}"'
    #                            f' AND star >= 1', **kwargs))[0][0]
    science = await _all(uid, **kwargs)
    return common.mt(0, 'success', {'science': science})


async def up(uid, ssa, **kwargs):
    dss = _decrypt(ssa)
    if dss is None:
        return common.mt(94, 'ssa error')
    pid, sid, aid = dss
    config = kwargs['config']['sciences'][f'{pid}']
    lv = (await stage.increase_exp(uid, 0, **kwargs))['level']
    if lv < config['constraint']['level']:
        return common.mt(99, 'insufficient level')
    _lv = await common.get_science(uid, ssa, **kwargs) + 1
    if _lv > config['constraint']['slv']:
        return common.mt(98, 'max level')
    cds = await _constraint_lv(uid, pid, sid, _lv, **kwargs)
    if isinstance(cds, tuple):
        return common.mt(cds[0], cds[1])
    cms = _consume(_lv, pid, sid)
    can, cmw = await common.consume_items(uid, cms, **kwargs)
    if not can:
        return common.mt(96, 'materials insufficient')
    await common.set_science(uid, ssa, _lv, **kwargs)
    results = {'science': await _all(uid, **kwargs), 'rws': {f'{ssa}': 1}}
    results['remain'], results['reward'] = stage.rm_rw(cmw)
    return common.mt(0, 'success', results)


async def init(uid, **kwargs):
    await common.set_science(uid, _encrypt(enums.Science.FACTORY, enums.ScienceSub.MASTER), 1, **kwargs)


# ################################# private #################################
async def _constraint_lv(uid, pid, sid, _lv, **kwargs):
    ssa = _encrypt(pid, enums.ScienceSub.MASTER)
    if pid == enums.Science.FACTORY and sid != enums.ScienceSub.MASTER:
        lv = await common.get_science(uid, ssa, **kwargs)
        if lv < _lv:
            return 95, 'The level of science master is inadequate'


async def _all(uid, **kwargs):
    sds = await common.execute(f'SELECT ssa, level FROM sciences '
                               f'WHERE uid="{uid}"', **kwargs)
    return {f'{ssa}': lv for ssa, lv in sds}


def _consume(lv, pid, sid):
    gid, qty = enums.Group.ITEM, 0
    if pid == enums.Science.FACTORY:
        if sid == enums.ScienceSub.ROLE:
            if lv <= 5:
                qty = (lv - 1) * 200 + 100
            elif lv <= 9:
                qty = (lv - 4) * 1000
            elif lv <= 14:
                qty = (lv - 9) * 10000
            elif lv <= 18:
                qty = (lv - 13) * 40000
            else:
                qty = (lv - 14) * 50000
            return f'{gid}:{enums.Item.CRYSTAL}:{qty},{gid}:{enums.Item.COIN}:{qty * 10}'
        if sid == enums.ScienceSub.MASTER:
            if lv <= 7:
                qty = 6000 * (lv + 2)
            elif lv <= 17:
                qty = 54000 + (lv - 7) * 12000
            else:
                qty = 174000 + (lv - 17) * 60000
            return f'{gid}:{enums.Item.CRYSTAL}:{qty}'
    return ''


def _encrypt(pid, sid, aid=0):
    """加密"""
    return (pid << 16) + (sid << 8) + aid


def _decrypt(ssa):
    """解密"""
    with contextlib.suppress(ValueError):
        pid = enums.Science(ssa>>16)
        sid = enums.ScienceSub((ssa&0xff00)>>8)
        aid = enums.SSAffiliate(ssa&0xff)
        return pid, sid, aid



