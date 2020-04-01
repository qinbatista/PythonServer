'''
science.py
'''

from module import enums
from module import common
from module import task
from module import achievement
from module import summoning
from module import vip
from datetime import datetime, timedelta
import random
import asyncio


# 99 -
# 98 -
# 97 -
# 96 -
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
    rn = (await common.execute(f'SELECT COUNT(*) FROM role WHERE uid="{uid}" AND star >= 1', **kwargs))[0][0]
    wn = (await common.execute(f'SELECT COUNT(*) FROM weapon WHERE uid="{uid}" AND star >= 1', **kwargs))[0][0]
    return common.mt(0, 'success', {'illustration': {'rn': rn, 'wn': wn}})



