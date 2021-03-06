'''
common.py

Contains definitions of commonly used generic functions.
When desinging a function, try to make it as general as possible to allow the reuse of code.
'''
from module import enums
from module import mail
import time
import calendar
from datetime import datetime, timedelta
from dateutil import tz
TZ_SH = tz.gettz('Asia/Shanghai')


async def exists(table, *conditions, account = False, **kwargs):
    condition = ' AND '.join([f'`{cond[0]}` = "{cond[1]}"' for cond in conditions])
    data = await execute(f'SELECT EXISTS (SELECT 1 FROM {table} WHERE {condition});', account, **kwargs)
    if data == () or () in data: return False
    return data[0][0] != 0

async def execute(statement, account=False, mall=False, exchange=False, **kwargs):
    async with ((((await get_db(**kwargs)).acquire() if not account
            else kwargs['accountdb'].acquire()) if not mall
            else kwargs['malldb'].acquire()) if not exchange
            else kwargs['exchangedb'].acquire()) as conn:
        if not account and not mall and not exchange:
            await conn.select_db(translate_world(**kwargs))
        async with conn.cursor() as cursor:
            await cursor.execute(statement)
            return await cursor.fetchall()

async def get_gn(uid, **kwargs):
    data = await execute(f'SELECT gn FROM player WHERE uid = "{uid}";', **kwargs)
    return "" if data == () else data[0][0]

async def get_uid(gn, **kwargs):
    data = await execute(f'SELECT uid FROM player WHERE gn = "{gn}";', **kwargs)
    return "" if data == () else data[0][0]

def remaining_cd():
    cd_time = datetime.strptime((datetime.now(tz=TZ_SH) + timedelta(days=1)).strftime("%Y-%m-%d"), "%Y-%m-%d").replace(tzinfo=TZ_SH) - datetime.now(tz=TZ_SH)
    return int(cd_time.total_seconds())

def remaining_month_cd():
    month_days = calendar.monthrange(datetime.today().year, datetime.today().month)[1]
    cd_time = datetime.strptime(datetime.now(tz=TZ_SH).strftime("%Y-%m"), "%Y-%m").replace(tzinfo=TZ_SH) + timedelta(days=month_days) - datetime.now(tz=TZ_SH)
    return int(cd_time.total_seconds())

async def try_item(uid, item, value, **kwargs):
    async with (await get_db(**kwargs)).acquire() as conn:
        await conn.select_db(translate_world(**kwargs))
        async with conn.cursor() as cursor:
            await cursor.execute(f'SELECT value FROM item WHERE uid = "{uid}" AND iid = "{item.value}" FOR UPDATE;')
            quantity = await cursor.fetchall()
            if value >= 0 or (quantity != () and quantity[0][0] + value >= 0):
                if await cursor.execute(f'INSERT INTO item (uid, iid, value) VALUES ("{uid}", {item.value}, value) ON DUPLICATE KEY UPDATE `value` = `value` + {value};') == 1:
                    await cursor.execute(f'UPDATE item SET value = {value} WHERE uid = "{uid}" AND iid = {item.value};')
                return (True, quantity[0][0] + value) if quantity != () else (True, value)
            return (False, quantity[0][0] + value) if quantity != () else (False, value)

async def try_armor(uid, aid, level, value, **kwargs):
    async with (await get_db(**kwargs)).acquire() as conn:
        await conn.select_db(translate_world(**kwargs))
        async with conn.cursor() as cursor:
            await cursor.execute(f'SELECT `quantity` FROM `armor` WHERE `uid` = "{uid}" AND \
                    `aid` = {aid} AND `level` = {level} FOR UPDATE;')
            qty = await cursor.fetchall()
            if value >= 0 or (qty != () and qty[0][0] + value >= 0):
                if await cursor.execute(f'INSERT INTO `armor` VALUES ("{uid}", {aid}, {level}, \
                        {value}) ON DUPLICATE KEY UPDATE quantity = quantity + {value};') == 1:
                    await cursor.execute(f'UPDATE `armor` SET `quantity` = {value} WHERE `uid` = "{uid}" \
                            AND `aid` = {aid} AND `level` = {level};')
                return (True, qty[0][0] + value) if qty != () else (True, value)
            return (False, qty[0][0] + value) if qty != () else (False, value)

async def try_weapon(uid, wid, val, **kwargs):
    val += await get_weapon(uid, wid, **kwargs)
    await set_weapon(uid, wid, val, **kwargs)
    return val

async def try_role(uid, rid, val, **kwargs):
    val += await get_role(uid, rid, **kwargs)
    await set_role(uid, rid, val, **kwargs)
    return val

async def try_skill(uid, sid, **kwargs):
    data = await execute(f'SELECT level FROM skill WHERE uid = "{uid}" AND sid = {sid};', **kwargs)
    can = data == ()
    if can:
        await execute(f'INSERT INTO skill (uid, sid, level) VALUES ("{uid}", {sid}, 1);', **kwargs)
    return can

async def get_weapon(uid, wid, key='segment', **kwargs):
    data = await execute(f'SELECT {key} FROM weapon WHERE uid = "{uid}" AND wid = {wid};', **kwargs)
    return 0 if data == () else data[0][0]

async def set_weapon(uid, wid, val, key='segment', **kwargs):
    await execute(f'INSERT INTO weapon (uid, wid, {key}) VALUES ("{uid}", {wid}, {val}) ON DUPLICATE KEY UPDATE {key}=VALUES({key});', **kwargs)

async def get_role(uid, rid, key='segment', **kwargs):
    data = await execute(f'SELECT {key} FROM role WHERE uid = "{uid}" AND rid = {rid};', **kwargs)
    return 0 if data == () else data[0][0]

async def set_role(uid, rid, val, key='segment', **kwargs):
    await execute(f'INSERT INTO role (uid, rid, {key}) VALUES ("{uid}", {rid}, {val}) ON DUPLICATE KEY UPDATE {key}=VALUES({key});', **kwargs)

async def get_timer(uid, tid, timeformat = '%Y-%m-%d %H:%M:%S', **kwargs):
    data = await execute(f'SELECT `time` FROM `timer` WHERE `uid` = "{uid}" AND \
            `tid` = {tid.value};', **kwargs)
    try:
        tim = datetime.strptime(data[0][0], timeformat).replace(tzinfo=TZ_SH) if data != () else None
    except ValueError:
        tim = datetime.strptime(f'{data[0][0]} 00:00:00', timeformat).replace(tzinfo=TZ_SH)
    return tim

async def set_timer(uid, tid, time, timeformat = '%Y-%m-%d %H:%M:%S', **kwargs):
    await execute(f'INSERT INTO `timer` VALUES ("{uid}", {tid.value}, \
            "{time.strftime(timeformat)}") ON DUPLICATE KEY UPDATE \
            `time` = "{time.strftime(timeformat)}";', **kwargs)

async def get_limit(uid, lid, **kwargs):
    data = await execute(f'SELECT `value` FROM `limits` WHERE `uid` = "{uid}" AND \
            `lid` = {lid};', **kwargs)
    return data[0][0] if data != () else None

async def set_limit(uid, lid, value, **kwargs):
    await execute(f'INSERT INTO `limits` VALUES ("{uid}", {lid}, {value}) \
            ON DUPLICATE KEY UPDATE `value` = {value};', **kwargs)

async def get_progress(uid, pid, **kwargs):
    data = await execute(f'SELECT {pid} FROM `progress` WHERE `uid` = "{uid}";', **kwargs)
    return data[0][0] if data != () else None

async def set_progress(uid, pid, value, **kwargs):
    await execute(f'INSERT INTO `progress` (uid, {pid}) VALUES ("{uid}", "{value}") ON DUPLICATE KEY UPDATE {pid}="{value}";', **kwargs)

async def get_player(uid, pid, **kwargs):
    data = await execute(f'SELECT {pid} FROM `player` WHERE `uid` = "{uid}";', **kwargs)
    return data[0][0] if data != () else None

async def set_player(uid, pid, value, **kwargs):
    await execute(f'UPDATE `player` SET {pid}="{value}" WHERE uid="{uid}";', **kwargs)

async def get_friend(uid, fid, **kwargs):
    data = await execute(f'SELECT recover, since, isre FROM `friend` WHERE `uid` = "{uid}" AND `fid` = "{fid}";', **kwargs)
    return data[0] if data != () else None

async def set_friend(uid, fid, *conditions, **kwargs):
    condition = ', '.join([f'`{cond[0]}` = "{cond[1]}"' for cond in conditions])
    await execute(f'UPDATE `friend` SET {condition} WHERE uid="{uid}" AND `fid` = "{fid}";', **kwargs)

async def set_famliy(name, fid, value, **kwargs):
    await execute(f'UPDATE `family` SET {fid}="{value}" WHERE name="{name}";', **kwargs)

async def set_achievement(uid, aid, value, reset=False, **kwargs):
    if not reset: value = f'`value` + {value}'
    await execute(f'INSERT INTO achievement(uid, aid, value, reward) VALUES ("{uid}", {aid}, {value}, 0) ON DUPLICATE KEY UPDATE `value`= {value}', **kwargs)

async def get_stage(uid, sid, **kwargs):
    data = await execute(f'SELECT `stage`, `btm` FROM `stages` WHERE `uid` = "{uid}" AND `sid` = {sid};', **kwargs)
    return data[0]

async def set_stage(uid, sid, stage, btm, **kwargs):
    await execute(f'INSERT INTO `stages` VALUES ("{uid}", {sid}, {stage}, "{btm}") ON DUPLICATE KEY UPDATE `stage` = {stage}, `btm` = "{btm}";', **kwargs)

async def get_element(uid, eid, **kwargs):
    data = await execute(f'SELECT val FROM `elements` WHERE `uid`="{uid}" AND `eid`={eid};', **kwargs)
    return data[0][0] if data != () else None

async def set_element(uid, eid, val, **kwargs):
    await execute(f'INSERT INTO `elements` VALUES ("{uid}", "{eid}", "{val}") ON DUPLICATE KEY UPDATE val="{val}";', **kwargs)

async def get_science(uid, ssa, **kwargs):
    data = await execute(f'SELECT level FROM `sciences` WHERE `uid`="{uid}" AND `ssa`={ssa};', **kwargs)
    return data[0][0] if data != () else 0

async def set_science(uid, ssa, level, **kwargs):
    await execute(f'INSERT INTO `sciences` VALUES ("{uid}", "{ssa}", "{level}") ON DUPLICATE KEY UPDATE level="{level}";', **kwargs)

async def get_db(**kwargs):
    return kwargs['worlddb']

def encode_item(gid, iid, value):
    return f'{gid.value}:{iid.value}:{value}'

# H O(n) can easily be refactored to O(1) using hash table with world as key
def translate_world(**kwargs):
    '''
    translates the current world into its merged form.
    worlds can occasionally be merged together to keep them active.
    in this case, the world names will need to be translated to the new world name.
    '''
    try:
        for world in kwargs['config']['world']['worlds']:
            if world['id'] == kwargs['world']:
                return str(kwargs['world']) if world['id'] == world['merge'] else str(world['merge'])
    except KeyError:
        print('ERROR: common.translate_world could not find "merge" keyword in world.json config.')
        return str(kwargs['world'])

# H O(n) can easily be refactored to O(1) using hash table with world as key
def translate_uid(uid, **kwargs):
    '''
    translates the given uid to the correct form, based on the world provided
    returns translated_uid if a translation took place, uid otherwise
    '''
    try:
        for world in kwargs['config']['world']['worlds']:
            if world['id'] == kwargs['world']:
                return uid if world['id'] == world['merge'] else f'{uid}_{world["id"]}'
    except KeyError:
        print('ERROR: common.translate_uid could not find "merge" keyword in world.json config.')
        return uid

def decode_items(items, mul=1):
    decoded = []
    if items != '':
        for item in items.split(','):  # "gid:iid:value,gid:iid:value"
            gid, iid, value = [int(v) if i < 2 else v for i, v in enumerate(item.split(':', maxsplit=2))]
            gid = enums.Group(gid)
            if gid == enums.Group.ITEM:
                decoded.append((gid, enums.Item(iid), mul * int(value)))
            elif gid == enums.Group.WEAPON:
                decoded.append((gid, enums.Weapon(iid), mul * int(value)))
            elif gid == enums.Group.SKILL:
                decoded.append((gid, enums.Skill(iid), mul * int(value)))  # undecided
            elif gid == enums.Group.ROLE:
                decoded.append((gid, enums.Role(iid), mul * int(value)))
            elif gid == enums.Group.ARMOR:
                decoded.append((gid, enums.Armor(iid), mul * int(value)))
                # decoded.append((gid, enums.Armor(iid), value))  # value => 'level:value' => '1:1'
    return decoded


async def try_energy(uid, amount, **kwargs):
    # amount > 0 ???????????????
    # amount == 0 ??????????????????
    # amount < 0 ????????????
    # success ===> 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7
    # - 0 - ?????????????????? === Purchase energy successfully
    # - 1 - ??????????????????????????????????????? === Purchase energy successfully, energy is not fully restored
    # - 2 - ?????????????????? === Get energy successfully
    # - 3 - ?????????????????????????????????????????????????????? === Energy has been consumed, energy value and recovery time updated successfully
    # - 4 - ?????????????????????????????????????????? === Energy has been fully restored, successful energy update
    # - 5 - ????????????????????????????????????????????? === Energy has not fully recovered, successful energy update
    # - 6 - ??????????????????????????????????????????????????????????????? === After refreshing the energy, the energy value and recovery time are successfully updated.
    # - 7 - ??????????????????????????????????????????????????????????????????????????????????????? === Energy has been refreshed, not fully recovered, energy has been consumed, energy value and recovery time updated successfully
    # - 97 - ???????????? === Parameter error
    # - 98 - ????????????????????? === Not enough energy consumption
    max_energy = kwargs['config']['player']['energy']['max_energy']
    sql_energy = await get_progress(uid, 'energy', **kwargs)
    sql_energy = max_energy if sql_energy is None else sql_energy
    now100 = datetime.now(tz=TZ_SH) + timedelta(days=36500)
    if sql_energy >= max_energy:
        await set_timer(uid, enums.Timer.ENERGY_RECOVER, now100, **kwargs)
    if amount > 0:  # ????????????
        data = (await _decrease_energy(uid, 0, sql_energy, max_energy, **kwargs))['data']
        sql_energy += amount
        await set_progress(uid, 'energy', sql_energy, **kwargs)
        if sql_energy >= max_energy:
            await set_timer(uid, enums.Timer.ENERGY_RECOVER, now100, **kwargs)
            return mt(0, "Purchase energy successfully", {'energy': sql_energy, 'recover_time': '', 'cooling_time': -1})
        else:
            data['energy'] = sql_energy
            return mt(1, "Purchase energy successfully, energy is not fully restored", data)
    elif sql_energy + amount < 0:
        return mt(status=97, message="Parameter error")
    else:  # ??????????????????????????????
        return await _decrease_energy(uid, abs(amount), sql_energy, max_energy, **kwargs)


async def _decrease_energy(uid, amount, sql_energy, max_energy, **kwargs) -> dict:
    _cooling, now = kwargs['config']['player']['energy']['cooling_time'] * 60, datetime.now(tz=TZ_SH)
    cooling, now100 = _cooling, now + timedelta(days=36500)
    tim = await get_timer(uid, enums.Timer.ENERGY_RECOVER, **kwargs)
    tim = now if tim is None else tim
    if tim >= now:
        """???????????????"""
        if amount == 0:  # ????????????
            # ??????1?????????????????????????????????????????????????????????????????????????????????????????????
            return mt(2, 'Get energy successfully', {'energy': sql_energy, 'recover_time': tim.strftime('%Y-%m-%d %H:%M:%S'), 'cooling_time': -1})
        # ??????2?????????????????????????????????????????????????????????????????????????????????????????????????????????
        # ????????????????????????????????????????????????????????????????????? ???????????????
        sql_energy -= amount
        if sql_energy < 0: return mt(98, 'Not enough energy consumption')
        tim, cooling = (now100, -1) if sql_energy >= max_energy else (now, _cooling)
        await __update_energy(uid, sql_energy, tim, **kwargs)
        return mt(3, 'Energy has been consumed, energy value and recovery time updated successfully', {'energy': sql_energy, 'recover_time': tim.strftime('%Y-%m-%d %H:%M:%S'), 'cooling_time': cooling})
    else:
        """??????????????????"""
        delta = now - tim
        cooling, _energy = int(delta.total_seconds()) % _cooling, int(delta.total_seconds()) // _cooling + sql_energy  # ??????????????????????????????
        cooling, now = _cooling - cooling, now - timedelta(seconds=cooling)
        if amount == 0:  # ????????????
            # ???????????????????????????????????????????????????????????????????????????????????????????????????????????????
            # ??????3?????????????????????????????????????????????????????????????????????????????????????????????????????????
            # ??????4??????????????????????????????????????????????????????????????????????????????????????????????????????sql_energy
            # ?????????????????????????????????????????????????????????????????????
            tim, sql_energy, cooling = (now100, max_energy, -1) if _energy >= max_energy else (now, _energy, cooling)
            status, msg = (4, 'Energy has been fully restored, successful energy update') if cooling == -1 else (5, 'Energy has not fully recovered, successful energy update')
            await __update_energy(uid, sql_energy, tim, **kwargs)
            return mt(status, msg, {'energy': sql_energy, 'recover_time': tim.strftime('%Y-%m-%d %H:%M:%S'), 'cooling_time': cooling})
        if _energy >= max_energy:
            # ??????5??????????????????????????????????????????
            # ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
            tim, sql_energy, cooling = now, max_energy - amount, _cooling
            await __update_energy(uid, sql_energy, tim, **kwargs)
            return mt(6, 'After refreshing the energy, the energy value and recovery time are successfully updated', {'energy': sql_energy, 'recover_time': tim.strftime('%Y-%m-%d %H:%M:%S'), 'cooling_time': cooling})
        elif _energy >= amount:
            # ??????6??????????????????????????????????????????
            # ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
            # ?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
            tim, sql_energy = now, _energy - amount
            await __update_energy(uid, sql_energy, tim, **kwargs)
            return mt(7, 'Energy has been refreshed, not fully recovered, energy has been consumed, energy value and recovery time updated successfully', {'energy': sql_energy, 'recover_time': tim.strftime('%Y-%m-%d %H:%M:%S'), 'cooling_time': cooling})
        else:  # ???????????????????????????????????????????????????????????????????????????????????????
            return mt(98, 'Not enough energy consumption')


async def __update_energy(uid, energy, tim, **kwargs):
    await set_progress(uid, 'energy', energy, **kwargs)
    await set_timer(uid, enums.Timer.ENERGY_RECOVER, tim, **kwargs)


def mt(status, message, data=None):
    return {'status': status, 'message': message, 'data': data or {}}


# private message
async def _redeem_all_mail(uid, gn_target, mail_type, group_id, item_id, quantity, **kwargs):
    return mt(0, 'success')


async def _send_text_mail(uid, gn_target, msg, **kwargs):
    fid = await get_uid(gn_target, **kwargs)
    #kwargs['msg'] = msg
    #kwargs['from_'] = await get_gn(uid, **kwargs)
    #sent = await mail.send_mail(0, fid, **kwargs)
    await mail.send_mail({'type' : enums.MailType.SIMPLE, 'from' : await get_gn(uid, **kwargs), 'subj' : 'subj', 'body' : msg}, fid, **kwargs)
    return mt(0, 'success')


async def _send_gift_mail(uid, gn_target, group_id, item_id, quantity, **kwargs):
    fid = await get_uid(gn_target, **kwargs)
    if fid == "": return mt(99, '')
    #kwargs['items'] = encode_item(enums.Group(group_id), enums.Item(item_id), quantity)
    #kwargs['from_'] = await get_gn(uid, **kwargs)
    #sent = await mail.send_mail(1, fid, **kwargs)
    await mail.send_mail({'type' : enums.MailType.GIFT, 'from' : await get_gn(uid, **kwargs),
            'subj' : enums.MailTemplate.SYSTEM_REWARD.name, 'body' : enums.MailTemplate.GIFT_1.name,
            'items' : encode_item(enums.Group(group_id), enums.Item(item_id), quantity)}, fid, **kwargs)
    return mt(0, 'success')


async def send_gift_sys_mail(uid, items, **kwargs):
    """?????????uid??????????????????"""
    await mail.send_mail({'type': enums.MailType.GIFT.value, 'from': 'lukseun team',
            'subj': enums.MailTemplate.SYSTEM_REWARD.name, 'body': enums.MailTemplate.GIFT_1.name,
            'items': items}, uid, **kwargs)


async def consume_items(uid, items, mul=1, **kwargs):
    items, results = decode_items(items, mul=mul), []
    for gid, iid, qty in items:
        if gid == enums.Group.ITEM:
            _, _qty = await try_item(uid, iid, 0, **kwargs)
            if _qty < qty: return False, results
        else:
            print(f'???????????????gid={gid}')
    for gid, iid, qty in items:
        if gid == enums.Group.ITEM:
            _, rm_qty = await try_item(uid, iid, -qty, **kwargs)
            results.append((gid, iid, rm_qty, qty))
    return True, results


async def rw_common(uid, items, results, mul=1, **kwargs):
    """????????????????????????????????????"""
    res = await reward_items(uid, ','.join(items), mul=mul, **kwargs)
    results['remain'], results['reward'] = rm_rw(res)


def rm_rw(results):
    """??????????????????????????????"""
    return [f'{g}:{i}:{v}' for g, i, v, _ in results], [f'{g}:{i}:{v}' for g, i, _, v in results]


async def reward_items(uid, items: str,  mul=1, module=None, **kwargs):
    """?????????????????????????????????"""
    decoded, results = decode_items(items, mul=mul), []
    for gid, iid, value in decoded:
        if gid == enums.Group.ITEM:
            _, remain_v = await try_item(uid, iid, value, **kwargs)
        elif gid == enums.Group.WEAPON:
            remain_v = await try_weapon(uid, iid, value, **kwargs)
        elif gid == enums.Group.ROLE:
            remain_v = await try_role(uid, iid, value, **kwargs)
        elif gid == enums.Group.ARMOR:
            _, remain_v = await try_armor(uid, iid, 1, value, **kwargs)
        elif gid == enums.Group.SKILL:
            can = await try_skill(uid, iid, **kwargs)
            remain_v = 1
            if not can:
                gid, iid, value = enums.Group.ITEM, enums.Item.SKILL_SCROLL_10, 1
                _, remain_v = await try_item(uid, iid, value, **kwargs)
        else:
            print(f'?????????????????????gid={gid},iid={iid}')
            remain_v = 0  # gid??????????????????????????????????????????
        results.append((gid, iid, remain_v, value))
    return results


def __calculate(config: list, sql_exp: int) -> (int, int):
    values = [e for e in config if e > sql_exp]
    level, need = config.index(values[0]) if values != [] else len(config), values[0] - sql_exp if values != [] else 0
    return level, need
