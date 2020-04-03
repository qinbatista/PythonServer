'''
friend.py

CHECKED RETURN TYPES WITH LIANG
'''

import json
import asyncio

from module import mail
from module import enums
from module import common
from module import task
from module import achievement
from module import family
from datetime import datetime

MAX_PERSON = 50


async def get_all(uid, **kwargs):
    info = await _get_friend_info(uid, **kwargs)
    return common.mt(0, 'got all friends', {'friends': [
        {'gn': i[0], 'exp': i[1], 'recover': i[2], 'since': i[3],
         'fid': '' if i[4] is None else i[4], 'intro': i[5], 'icon': 101} for i
        in info]})


async def remove(uid, gn_target, **kwargs):
    uid_target = await common.get_uid(gn_target, **kwargs)
    if uid == uid_target: return common.mt(99, 'don\'t be an idiot')
    await common.execute(
        f'DELETE FROM friend WHERE (uid = "{uid}" AND fid = "{uid_target}") OR (uid = "{uid_target}" AND fid = "{uid}");',
        **kwargs)
    return common.mt(0, 'removed target', {'gn': gn_target})


async def request(uid, gn_target, **kwargs):
    if await _is_request_max(uid, **kwargs):
        return common.mt(96, '6 request for 1 day, try tommorrow')
    uid_target = await common.get_uid(gn_target, **kwargs)
    if uid_target == "": return common.mt(97, 'no such person')
    if uid == uid_target: return common.mt(99, 'do not be an idiot')
    friends, _, _ = await _are_friends(uid, uid_target, **kwargs)
    if friends: return common.mt(95, 'already friends')
    await common.execute(
        f'INSERT INTO friend (uid, fid) VALUES ("{uid}", "{uid_target}") ON DUPLICATE KEY UPDATE uid = uid;',
        **kwargs)

    sent = await mail.send_mail({'type': enums.MailType.FRIEND_REQUEST.value,
                                 'from': await common.get_gn(uid, **kwargs),
                                 'subj': '', 'body': '', 'uid_sender': uid},
                                uid_target, **kwargs)
    if sent[uid_target]['status'] == 1:
        return common.mt(94, 'target mailbox full')
    if sent[uid_target]['status'] != 0:
        return common.mt(98, 'could not send mail')
    await achievement.record(uid, enums.Achievement.FRIEND_REQUEST, **kwargs)
    await common.execute(f'INSERT INTO limits(uid, lid, value) VALUES ("{uid}", {enums.Limits.REQUEST_FRIEND_LIMITS}, value+1) ON DUPLICATE KEY UPDATE value = value+1;', **kwargs)
    return common.mt(0, 'request sent', {'gn': gn_target})


async def respond(uid, nonce, **kwargs):
    uid_sender = await _lookup_nonce(nonce, **kwargs)
    if not uid_sender: return common.mt(99, 'invalid nonce')
    count = (await common.execute(
        f'SELECT COUNT(*) FROM friend WHERE uid="{uid}" AND since!="";',
        **kwargs))[0][0]
    if count >= MAX_PERSON:
        return common.mt(97, 'Your buddy list is full')
    await _add_friend(uid, uid_sender, **kwargs)
    info = await _get_friend_info(uid_sender, **kwargs)
    await mail.delete_mail(uid, nonce, **kwargs)
    if info == ():
        return common.mt(98, 'this person has date exception')
    return common.mt(0, 'success', {'gn': info[0][0], 'exp': info[0][1]})


async def send_gift(uid, gn_target, infos=None, **kwargs):
    # 发送朋友礼物
    if infos is None:
        fid = await common.get_uid(gn_target, **kwargs)
        friends, recover, since = await _are_friends(uid, fid, **kwargs)
        if not friends or since == '': return common.mt(99, 'not friends')
    else:
        fid, recover = infos
    now = datetime.now(tz=common.TZ_SH)
    if not _can_send_gift(now, recover): return common.mt(98, 'gift cooldown')

    sent = await mail.send_mail({'type': enums.MailType.GIFT.value,
                                 'from': await common.get_gn(uid, **kwargs),
                                 'subj': enums.MailTemplate.FRIEND_GIFT.name,
                                 'body': '',
                                 'items': common.encode_item(enums.Group.ITEM,
                                                             enums.Item.FRIEND_GIFT,
                                                             1)},
                                fid, **kwargs)
    if sent[fid]['status'] == 1:
        return common.mt(96, 'target mailbox full')
    if sent[fid]['status'] != 0:
        return common.mt(97, 'mailbox error')

    await common.execute(
        f'UPDATE friend SET recover = "{now.strftime("%Y-%m-%d")}" WHERE uid = "{uid}" AND fid = "{fid}";',
        **kwargs)
    await task.record(uid, enums.Task.SEND_FRIEND_GIFT, **kwargs)
    await achievement.record(uid, enums.Achievement.FRIEND_GIFT, **kwargs)
    return common.mt(0, 'success')


async def send_gift_all(uid, **kwargs):
    """info ==> 0:uid 2:fid 2:fgn 3:recover 4:since"""
    # info = await get_info(**kwargs)
    info = await common.execute(f'SELECT friend.uid, player.uid, player.gn, friend.recover, friend.since FROM friend JOIN player ON player.uid = friend.fid;', **kwargs)
    results = [(i[2], await send_gift(uid, i[2], infos=[i[1], i[3]], **kwargs))
               for i in info if i[0] == uid and i[4] != '']
    if not results: return common.mt(99, 'no friend to send gift')
    msgs = [r[0] for r in results if r[1]["status"] == 0]
    return common.mt(0, 'you send all friend gift success', msgs)


async def find_person(uid, gn_target, **kwargs):
    data = await _get_person_info(await common.get_uid(gn_target, **kwargs),
                                  **kwargs)
    uid_target = await common.get_uid(gn_target, **kwargs)
    if uid == uid_target: return common.mt(98, "can't add yourself")
    if data == (): return common.mt(99, 'no such person')
    stage, _ = await common.get_stage(uid, enums.Stage.GENERAL, **kwargs)
    isfriends, _, _ = await _are_friends(uid, uid_target, **kwargs)
    canfamily = await _can_invite_family(uid, uid_target, **kwargs)
    return common.mt(0, 'find person success',
                     {'gn': data[0][0], 'intro': data[0][1],
                      'fid': data[0][2] or '', 'exp': data[0][3],
                      'role': data[0][4], 'stage': stage,
                      "isfriend": isfriends, "canfamily": canfamily})


###########################################################################################################
# async def get_info(**kwargs):
#     info = await kwargs['redis'].get(f'{kwargs["worlddb"]}.friend')
#     return await _mysql_to_redis(**kwargs) if info is None else json.loads(str(info).replace('\'', '"'))


# async def _mysql_to_redis(**kwargs):
#     info = await common.execute(f'SELECT friend.uid, player.uid, player.gn, friend.recover, friend.since FROM friend JOIN player ON player.uid = friend.fid;', **kwargs)
#     await kwargs['redis'].set(f'{kwargs["worlddb"]}.friend', f'{[list(i) for i in info]}', expire=300)
#     return info


def _can_send_gift(now, recover):
    if recover == '': return True
    delta_time = now - datetime.strptime(recover, '%Y-%m-%d').replace(
        tzinfo=common.TZ_SH)
    return delta_time.days >= 1


async def _is_request_max(uid, **kwargs):
    now = datetime.now(tz=common.TZ_SH).strftime('%Y-%m-%d')
    data = await common.execute(
        f"SELECT limits.value, timer.time FROM limits JOIN timer ON limits.uid = timer.uid WHERE limits.uid='{uid}' and limits.lid={enums.Limits.REQUEST_FRIEND_LIMITS} and timer.tid={enums.Timer.REQUEST_FRIEND_TIME}",
        **kwargs)
    if data == ():
        await common.execute(
            f'INSERT INTO limits(uid, lid, value) VALUES ("{uid}", {enums.Limits.REQUEST_FRIEND_LIMITS}, 0) ON DUPLICATE KEY UPDATE value = 0;',
            **kwargs)
        await common.execute(
            f'INSERT INTO timer(uid, tid, time) VALUES ("{uid}", {enums.Timer.REQUEST_FRIEND_TIME}, "{now}") ON DUPLICATE KEY UPDATE time = "{now}";',
            **kwargs)
        count, record_time = 0, now
    else:
        count, record_time = data[0][0], data[0][1]
    delta_time = datetime.now(tz=common.TZ_SH) - datetime.strptime(record_time,
                                                                   '%Y-%m-%d').replace(
        tzinfo=common.TZ_SH)
    if delta_time.days >= 1:
        await common.execute(
            f'INSERT INTO timer(uid, tid, time) VALUES ("{uid}", {enums.Timer.REQUEST_FRIEND_TIME}, "{now}") ON DUPLICATE KEY UPDATE time = "{now}";',
            **kwargs)
        await common.execute(
            f'INSERT INTO limits(uid, lid, value) VALUES ("{uid}", {enums.Limits.REQUEST_FRIEND_LIMITS}, 0) ON DUPLICATE KEY UPDATE value = 0;',
            **kwargs)
    if delta_time.days < 1 and count <= 5:
        return False
    if delta_time.days < 1 and count > 5:
        return True


async def _add_friend(uid, fid, **kwargs):
    now = datetime.now(tz=common.TZ_SH).strftime('%Y-%m-%d')
    await asyncio.gather(common.execute(
        f'INSERT INTO friend(uid, fid, since) VALUES ("{uid}", "{fid}", "{now}") ON DUPLICATE KEY UPDATE since = "{now}";',
        **kwargs), common.execute(
        f'INSERT INTO friend(uid, fid, since) VALUES ("{fid}", "{uid}", "{now}") ON DUPLICATE KEY UPDATE since = "{now}";',
        **kwargs))


async def _are_friends(uid, fid, **kwargs):
    data = await common.execute(
        f'SELECT recover, since FROM friend WHERE uid = "{uid}" AND fid = "{fid}";',
        **kwargs)
    return (True, data[0][0], data[0][1]) if data != () else (
        False, None, None)
    # info = await get_info(**kwargs)
    # for u, f, fgn, r, s in info:
    #     if u == uid and f == fid:
    #         return True, r, s
    # return False, None, None


async def _can_invite_family(uid, fid, **kwargs):
    is_family, u_fid, has_family = await _are_family(uid, fid, **kwargs)
    if is_family or u_fid is None or has_family: return False
    return family._check_invite_permissions(
        await family._get_role(uid, u_fid, **kwargs))


async def _are_family(uid, fid, **kwargs):
    u_fid = (
        await common.execute(f'SELECT fid FROM player WHERE uid = "{uid}"',
                             **kwargs))[0][0]
    f_fid = (
        await common.execute(f'SELECT fid FROM player WHERE uid = "{fid}"',
                             **kwargs))[0][0]
    return u_fid is not None and u_fid == f_fid, u_fid, f_fid is not None


async def _get_friend_info(uid, **kwargs):
    return await common.execute(f'SELECT player.gn, progress.exp, friend.recover, friend.since, player.fid, player.intro FROM friend JOIN progress ON progress.uid = friend.fid JOIN player ON player.uid = friend.fid WHERE friend.uid = "{uid}";', **kwargs)


async def _get_person_info(uid, **kwargs):
    return await common.execute(f'SELECT player.gn, player.intro, player.fid, progress.exp, progress.rid FROM progress JOIN player ON progress.uid = player.uid WHERE player.uid = "{uid}";', **kwargs)


async def _lookup_nonce(nonce, **kwargs):
    async with kwargs['session'].post(
            kwargs['tokenserverbaseurl'] + '/redeem_nonce',
            json={'keys': [nonce]}) as resp:
        data = await resp.json()
        return None if data[nonce]['status'] != 0 else data[nonce][
            'uid_sender']
