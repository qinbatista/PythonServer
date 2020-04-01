'''
player.py
'''

from module import mail
from module import enums
from module import common
from module import stage
from module import summoning
from module import account
from datetime import datetime, timedelta
import asyncio
import re
GN_RE = re.compile(r'^[\u4e00-\u9fa5_a-zA-Z0-9]+$')
ELEMENT_LIM = 3


async def create(uid, gn, **kwargs):
    if uid == "" or gn == "" or not bool(GN_RE.match(gn)): return common.mt(98, 'Player uid or name is empty or Game name is not legal')
    if (await common.execute(f'SELECT COUNT(*) FROM player WHERE uid = "{uid}" OR gn = "{gn}";', **kwargs))[0][0] != 0: return common.mt(99, 'Player uid or name already exists')
    await common.execute(f'INSERT INTO player(uid, gn) VALUES ("{uid}", "{gn}") ON DUPLICATE KEY UPDATE gn = gn;', **kwargs)
    await asyncio.gather(
        common.execute(f'UPDATE progress SET energy={kwargs["config"]["player"]["energy"]["max_energy"]}, exp=180, rid={enums.Role.R401} WHERE uid="{uid}";', **kwargs),
        common.execute(f'INSERT INTO factory (uid, fid, workers, storage) VALUES ("{uid}", {enums.Factory.UNASSIGNED}, 3, 3);', **kwargs),
        common.execute(f'INSERT INTO role (uid, star, level, rid) VALUES ("{uid}", 1, 1, {enums.Role.R402}), ("{uid}", 1, 1, {enums.Role.R505}), ("{uid}", 1, 1, {enums.Role.R601});', **kwargs),
        common.execute(f'INSERT INTO weapon(uid, star, wid) VALUES ("{uid}", 1, {enums.Weapon.W301}), ("{uid}", 1, {enums.Weapon.W302}), ("{uid}", 1, {enums.Weapon.W303});', **kwargs),
        common.execute(f'INSERT INTO skill(uid, sid, level) VALUES ("{uid}", {enums.Skill.S1}, 1), ("{uid}", {enums.Skill.S2}, 1), ("{uid}", {enums.Skill.S3}, 1), ("{uid}", {enums.Skill.S4}, 1), ("{uid}", {enums.Skill.S5}, 1);', **kwargs),
        common.execute(f'INSERT INTO timer (uid, tid, time) VALUES ("{uid}", {enums.Timer.LOGIN_TIME}, "{common.datetime.now(tz=common.TZ_SH).strftime("%Y-%m-%d")}");',**kwargs),
        common.execute(f'INSERT INTO item (uid, iid, value) VALUES ("{uid}", {enums.Item.FAMILY_COIN}, 0), ("{uid}", {enums.Item.FAMILY_COIN_RECORD}, 0);',**kwargs),
        common.set_limit(uid, enums.Limits.PLAYER_ELEMENT, ELEMENT_LIM, **kwargs),
        stage.init_stages(uid, **kwargs),
        _element_init(uid, **kwargs)
    )
    await _meeting_gift(uid, **kwargs)
    return common.mt(0, 'success', {'gn': gn})


async def enter_world(uid, **kwargs):
    cid = (await common.execute(f'SELECT cuid FROM info WHERE unique_id = "{uid}";', account=True, **kwargs))[0][0]
    translated_uid = common.translate_uid(uid, **kwargs)
    kwargs['world'] = common.translate_world(**kwargs)
    existing_player = await common.exists('player', ('uid', translated_uid), **kwargs)
    session = (await account._request_new_token(translated_uid, is_session='1', **kwargs))['token']
    await update_time(uid, **kwargs)
    if not existing_player:
        return common.mt(98, 'have not been in this world before', {'cid': cid, 'session' : session})
    return common.mt(0, 'success', {'cid': cid, 'session' : session})


async def update_time(uid, **kwargs):
    pass


async def get_account_world_info(uid, **kwargs):
    worlds = []
    for world in kwargs['config']['world']['worlds']:
        kwargs['world'] = world['id']
        translated_uid = common.translate_uid(uid, **kwargs)
        data = await common.execute(f'SELECT `gn`, `exp` FROM `player` JOIN `progress` ON \
                `player`.`uid` = `progress`.`uid` WHERE `player`.`uid` = "{translated_uid}";', **kwargs)
        if data != ():
            exp_info = await stage.increase_exp(translated_uid, 0, **kwargs)
            worlds.append({'server_status' : world['status'], 'world' : world['id'],
                    'world_name' : world['name'], 'gn' : data[0][0], 'exp' : data[0][1], 'level': exp_info['level']})
        else:
            worlds.append({'server_status' : world['status'], 'world' : world['id'],
                    'world_name' : world['name'], 'gn' : '', 'exp' : 0, 'level' : 0})
    return common.mt(0, 'success', {'worlds' : worlds})


async def accept_gifts(uid, gift, other, **kwargs):
    error, success = [], {}
    await asyncio.gather(*[mail.mark_read(uid, o, **kwargs) for o in other])
    error.extend(other)
    for g in gift:
        valid, resp = await accept_gift(uid, g, **kwargs)
        if valid: success[g] = [dict(r) for r in resp]
        else: error.append(g)
    return common.mt(0, 'success', {'error' : error, 'success' : success})


async def accept_gift(uid, nonce, **kwargs):
    await mail.mark_read(uid, nonce, **kwargs)
    gift = await _lookup_nonce(nonce, **kwargs)
    if not gift: return False, None
    items, r = common.decode_items(gift), []
    for item in items:
        _, remaining = await common.try_item(uid, item[1], item[2], **kwargs)
        r.append({'gid' : item[0], 'id' : item[1], 'remaining' : remaining, 'reward' : item[2]})
    return True, r


async def change_name(uid, gn, **kwargs):
    """修改玩家名字"""
    if gn == "" or not bool(GN_RE.match(gn)): return common.mt(97, 'Player name is empty or Game name is not legal')
    if (await common.execute(f'SELECT COUNT(*) FROM player WHERE gn = "{gn}";', **kwargs))[0][0] != 0: return common.mt(99, 'The player name has been used')
    consume = 100
    can, remain = await common.try_item(uid, enums.Item.DIAMOND, -consume, **kwargs)
    if not can: return common.mt(98, 'materials insufficient')
    await common.execute(f'UPDATE player SET gn = "{gn}" WHERE uid="{uid}";', **kwargs),
    return common.mt(0, 'success', {'gn': gn, 'remaining': [f'{enums.Group.ITEM.value}:{enums.Item.DIAMOND.value}:{remain}'], 'reward': [f'{enums.Group.ITEM.value}:{enums.Item.DIAMOND.value}:{consume}']})


async def get_info(uid, **kwargs):
    gn, fn = (await common.execute(f'SELECT gn, fid FROM player WHERE uid = "{uid}";', **kwargs))[0]
    stages = await stage.all_infos(uid, **kwargs)
    energy = await common.try_energy(uid, 0, **kwargs)
    exp = await common.get_progress(uid, 'exp', **kwargs)
    es = await _element_all(uid, **kwargs)
    elm = await common.get_limit(uid, enums.Limits.PLAYER_ELEMENT, **kwargs)
    return common.mt(0, 'success',
                     {'gn': gn, 'fn': fn or '', 'energy_info': energy['data'],
                      'stages': stages['data'], 'exp': exp, 'elements': es,
                      'elm': elm})


async def get_all_resource(uid, **kwargs):
    await summoning.refresh_integral(uid, **kwargs)
    item = await common.execute(f'SELECT iid, value FROM item WHERE uid = "{uid}";', **kwargs)
    return common.mt(0, 'success', {'items': [{'iid': i[0], 'value': i[1]} for i in item]})


async def element_lv(uid, eid, **kwargs):
    """元素升级"""
    if eid not in enums.Element._value2member_map_:
        return common.mt(99, 'eid error')
    lv = (await stage.increase_exp(uid, 0, **kwargs))['level']
    evs = 1 + (lv - 15)//10
    elements = await _element_all(uid, **kwargs)
    if evs <= sum(elements.values()):
        return common.mt(98, 'insufficient element skill points')
    val = elements[eid] + 1
    if val > 5:
        return common.mt(97, 'max element skill')
    await common.set_element(uid, eid, val, **kwargs)
    elements[eid] = val
    return common.mt(0, 'success', {'elements': elements, 'reward': {eid: 1}})


async def element_reset(uid, **kwargs):
    """重置元素技能点"""
    lim = await common.get_limit(uid, enums.Limits.PLAYER_ELEMENT, **kwargs)
    lim = (ELEMENT_LIM if lim is None else lim) - 1
    if lim < 0:
        return common.mt(99, 'Insufficient resets')
    await _element_init(uid, **kwargs)
    await common.set_limit(uid, enums.Limits.PLAYER_ELEMENT, lim, **kwargs)
    elements = await _element_all(uid, **kwargs)
    return common.mt(0, 'success', {'elements': elements, 'lim': lim})


async def element_all(uid, **kwargs):
    elements = await _element_all(uid, **kwargs)
    lim = await common.get_limit(uid, enums.Limits.PLAYER_ELEMENT, **kwargs)
    return common.mt(0, 'success', {'elements': elements, 'lim': lim})


#########################################################################################
async def _element_all(uid, **kwargs):
    eds = await common.execute(f'SELECT eid, val FROM `elements` WHERE `uid`="{uid}";', **kwargs)
    return {ed[0]: ed[1] for ed in eds}


async def _element_init(uid, **kwargs):
    [await common.set_element(uid, eid, 0, **kwargs) for eid in enums.Element]


async def _lookup_nonce(nonce, **kwargs):
    async with kwargs['session'].post(kwargs['tokenserverbaseurl'] + '/redeem_nonce', \
            json = {'keys' : [nonce]}) as resp:
        data = await resp.json()
        return None if data[nonce]['status'] != 0 else data[nonce]['items']


async def _meeting_gift(uid, **kwargs):
    """玩家初次创建角色赠送的见面礼"""
    items = ','.join([f'{g}:{i}:{v}' for g, i, v in GIFTS])
    await common.send_gift_sys_mail(uid, items, **kwargs)


GIFTS = [
    (enums.Group.ITEM, enums.Item.DIAMOND, 1_0000_0000),
    (enums.Group.ITEM, enums.Item.COIN, 1_0000_0000),
    (enums.Group.ITEM, enums.Item.FOOD, 10_0000),
    (enums.Group.ITEM, enums.Item.IRON, 10_0000),
    (enums.Group.ITEM, enums.Item.CRYSTAL, 10_0000),
    (enums.Group.ITEM, enums.Item.SUMMON_SCROLL_D, 50),
    (enums.Group.ITEM, enums.Item.SUMMON_SCROLL_C, 100),
    (enums.Group.ITEM, enums.Item.FRIEND_GIFT, 1000),
    # (enums.Group.ITEM, enums.Item.VIP_EXP_CARD, 100),
    (enums.Group.ITEM, enums.Item.SKILL_SCROLL_10, 100_0000),
    (enums.Group.ITEM, enums.Item.SKILL_SCROLL_30, 100_0000),
    (enums.Group.ITEM, enums.Item.SKILL_SCROLL_100, 100_0000),
    (enums.Group.ITEM, enums.Item.UNIVERSAL4_SEGMENT, 100),
    (enums.Group.ITEM, enums.Item.UNIVERSAL5_SEGMENT, 100),
    (enums.Group.ITEM, enums.Item.ENERGY_POTION_S_MAX, 100),
    (enums.Group.ITEM, enums.Item.EXP_POINT, 100_0000),
]






