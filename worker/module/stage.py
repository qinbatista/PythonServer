'''
stage.py
'''

from module import enums
from module import common
from module import task
from module import achievement
from module import summoning
from module import vip
from datetime import datetime, timedelta
import contextlib
import random
import json
import asyncio
# TODO 2020年1月14日
# ##################################################################
# ################### 2020年1月14日之后加入的方法 ###################
# ##################################################################
# 99 - Do not sweep until you pass this checkpoint
# 98 - There is no configuration information for this stage
# 97 - energy insufficient
# 96 - Can only be a positive integer
# 95 - materials insufficient
# 94 - stage mismatch
# 93 - abnormal damage
# 92 - no more ticket, try tomorrow
# 91 - stage error
# 90 - level insufficient
# 89 - Page number error
# 88 - No data for this page
# 87 - You didn't go pass
# 86 - You never hung up before
# 0 - success


async def enter(uid, sid, stage, **kwargs):
    """进入关卡"""
    if not STAGE_CHECK[sid](stage):
        return common.mt(91, 'stage error')
    _stage, _ = await common.get_stage(uid, sid, **kwargs)
    if stage > 1 + _stage:
        return common.mt(91, 'stage error')
    config = kwargs['config']['stages']['stage'].get(f'{stage}', None),
    if config is None:  # 关卡无配置信息
        return common.mt(98, 'There is no configuration information for this stage')
    config = dict(config[0]) if isinstance(config, tuple) else config
    if (await increase_exp(uid, 0, **kwargs))['level'] < config['constraint']['level']:
        return common.mt(90, 'level insufficient')
    results = {}
    # H 部分约束信息
    tim, lms, eds = None, {}, {'stage': stage}
    if sid in VERIFY:
        can, tim, lms = await VERIFY[sid](uid, **kwargs)
        eds.update({f'{k}': v for k, v in lms.items()})
        lms = {k: lms[k] + (1 if i==0 else 0) for i, k in enumerate(lms)}
        if can:
            return common.mt(92, 'no more ticket, try tomorrow')
        results[sid.name] = {'limits': lms, 'cd': common.remaining_cd()}
    # H 检查特殊物资是否能消耗
    energy = config['consumes']['special'].get('energy', 0)
    if (await common.try_energy(uid, 0, **kwargs))['data']['energy'] < energy:
        return common.mt(97, 'energy insufficient')
    # H 尝试消耗通用物资
    can, cmw = await common.consume_items(uid, ','.join(config['consumes']['common']), **kwargs)
    if not can:
        return common.mt(95, 'materials insufficient')
    results['remain'], results['reward'] = rm_rw(cmw)
    # H 保存待消耗
    eds['energy'] = energy
    # H 消耗特殊物资(体力)
    energy = 0
    data = (await common.try_energy(uid, -energy, **kwargs))['data']
    # H 实现部分约束
    if sid in VERIFY:
        await REALIZE[sid](uid, tim, lms, **kwargs)
    # H 附加配置
    els, monsters = addition(stage, **kwargs)
    results['addition'] = {'els': els, 'monsters': monsters}
    # H 构建结果
    results['energy'] = {'cooling': data['cooling_time'], 'remain': data['energy'], 'reward': -energy}
    # H 设置关卡进入状态
    # btm = datetime.now(tz=common.TZ_SH).strftime('%Y-%m-%d %H:%M:%S')
    # await common.set_stage(uid, sid, _stage, btm, **kwargs)
    await kwargs['redis'].hmset_dict(f'stage.check.{uid}', eds)
    return common.mt(0, 'success', results)


async def victory(uid, sid, stage, damage=0, **kwargs):
    """通关"""
    if not STAGE_CHECK[sid](stage):
        return common.mt(91, 'stage error')
    _stage, _btm = await common.get_stage(uid, sid, **kwargs)
    eds = await kwargs['redis'].hgetall(f'stage.check.{uid}')
    # if _btm == '' or _stg is None or stage != int(_stg):
    eds = {k: int(v) for k, v in eds.items()}
    if len(eds) == 0 or stage != eds['stage']:
        return common.mt(94, 'stage mismatch')
    # 删除缓存
    await kwargs['redis'].delete(f'stage.check.{uid}')
    # H 消耗特殊物资(体力)
    rewards = {'energy_info': (await common.try_energy(uid, -eds['energy'], **kwargs))['data'], 'boss': {}}
    # H 实现部分约束
    if sid in VERIFY:
        eds.pop('stage')
        eds.pop('energy')
        await REALIZE[sid](uid, None, eds, **kwargs)
        rewards[sid.name] = {'limits': eds, 'cd': common.remaining_cd()}
    config = kwargs['config']['stages']['stage'].get(f'{stage}', None)
    # H 奖励普通物资
    rwc = config['rewards']['common']
    if config['constraint']['random'] == 1:
        rwc = random.choices(rwc, k=config['rewards']['random'])
    await rw_common(uid, rwc, rewards, **kwargs)
    # H 奖励特殊物资
    rewards['exp_info'] = await increase_exp(uid, config['rewards']['special'].get('exp', 0), **kwargs)
    rewards['max_stage'] = max(stage, _stage)
    # H 设置关卡通过状态
    if stage > _stage: await common.set_stage(uid, sid, stage, '', **kwargs)
    # H 特殊处理
    if sid in VICTORY_DISPOSE:
        cm = await VICTORY_DISPOSE[sid](uid, stage, _stage, damage, rewards, **kwargs)
        if isinstance(cm, tuple):
            return common.mt(cm[0], cm[1])
    await kwargs['redis'].delete(f'stage.{uid}')
    return common.mt(0, 'success', rewards)


async def mopping_up(uid, stage, count=1, **kwargs):
    """关于扫荡关卡的方法"""
    if count <= 0: return common.mt(96, 'Can only be a positive integer')
    _stage, _ = await common.get_stage(uid, enums.Stage.GENERAL, **kwargs)
    if stage > _stage:
        return common.mt(99, 'Do not sweep until you pass this checkpoint')
    config = kwargs['config']['stages']['mopping-up'].get(f'{stage}', None)
    if config is None:
        return common.mt(98, 'There is no configuration information for this stage')  # 扫荡序章或未写配置的关卡会返回此结果
    # H 检查特殊物资是否能消耗
    energy = config['consumes']['special'].get('energy', 0) * count
    if (await common.try_energy(uid, 0, **kwargs))['data']['energy'] < energy: return common.mt(97, 'energy insufficient')
    # H 尝试消耗通用物资
    if not (await common.consume_items(uid, ','.join([f'{r[:r.rfind(":")]}:{int(r[r.rfind(":") + 1:]) * count}' for r in config['consumes']['common']]), **kwargs))[0]:
        return common.mt(95, 'materials insufficient')
    # H 消耗特殊物资(体力)
    data = (await common.try_energy(uid, -energy, **kwargs))['data']
    rewards = {'energy': {'cooling': data['cooling_time'], 'remain': data['energy'], 'reward': -energy}}
    # H 奖励普通物资
    await rw_common(uid, config['rewards']['common'], rewards, mul=count, **kwargs)
    # H 奖励特殊物资
    rewards['exp_info'] = await increase_exp(uid, config['rewards']['special']['exp'] * count, **kwargs)
    # H 任务记录
    await task.record(uid, enums.Task.PASS_MAIN_STAGE, **kwargs)
    return common.mt(0, 'success', rewards)


async def refresh_boss(uid, **kwargs):
    config = kwargs['config']['boss']
    now, bds = datetime.now(tz=common.TZ_SH), {}
    lid, tlid = enums.LeaderBoard.WORLD_BOSS, enums.LeaderBoard.TOTAL_WB
    for s, hp in config['hp'][kwargs['world']].items():
        bds[s] = {
            'hp': hp,
            'ratio': "%.2f" % (hp / config['HP'][s]),
            'damage': await get_leaderboard(uid, lid, s, **kwargs),
            'total': await get_leaderboard(uid, tlid, s, **kwargs)
        }
    tid, lid = enums.Timer.STAGE_WORLD_BOSS, enums.Limits.STAGE_WORLD_BOSS
    tim, lim = await asyncio.gather(
        common.get_timer(uid, tid, timeformat='%Y-%m-%d', **kwargs),
        common.get_limit(uid, lid, **kwargs)
    )
    if tim is None or now > tim:
        lim, tim = kwargs['config']['boss']['limit'], now + timedelta(days=1)
        await common.set_limit(uid, lid, lim, **kwargs)
        await common.set_timer(uid, tid, tim, timeformat='%Y-%m-%d', **kwargs)
    return common.mt(0, 'Successfully get hook information',
                     {'bds': bds, 'limit': lim, 'cd': common.remaining_cd(),
                      'mcd': common.remaining_month_cd()})


async def all_infos(uid, **kwargs):
    """获取所有的关卡信息"""
    sts = await common.execute(f'SELECT `sid`, `stage` FROM `stages` WHERE `uid` = "{uid}";', **kwargs)
    infos = {s[0]: s[1] for s in sts}
    limits = {f'{sid}': {k: v + 1 for k, v in (await VERIFY[sid](uid, **kwargs))[2].items()} for sid in VERIFY}
    return common.mt(0, 'success', {'infos': infos, 'limits': limits})


async def damage_ranking(uid, stage, page, **kwargs):
    if page < 1:
        return common.mt(89, 'Page number error')
    rks = f'leaderboard.player.{kwargs["world"]}.{uid}.{stage}'
    rds = await kwargs['redis'].get(rks)
    if rds is None:
        rds = await rank_update(uid, rks, stage, **kwargs)
    else:
        rds = json.loads(rds)
    lid, tlid = enums.LeaderBoard.WORLD_BOSS, enums.LeaderBoard.TOTAL_WB
    adt = await rank_all(tlid, stage, page, **kwargs)
    if adt == (): return common.mt(88, 'No data for this page')
    # adw = await rank_all(lid, stage, page, **kwargs)
    rank = {f'{tlid}': await rank_info(adt, page, **kwargs)}
            # f'{lid}': await rank_info(adw, page, **kwargs)}
    return common.mt(0, 'success', {'page': page, 'own_rank': rds, 'rank': rank})


async def hang_up(uid, new=True, **kwargs):
    """开启挂机或获取挂机奖励"""
    if not new:
        return None
    now = datetime.now(tz=common.TZ_SH)
    tim = await common.get_timer(uid, enums.Timer.STAGE_HANG_UP, **kwargs)
    stage, _ = await common.get_stage(uid, enums.Stage.ENDLESS, **kwargs)
    if tim is None:
        if stage <= 1000:
            return common.mt(87, "You didn't go pass")
        await common.set_timer(uid, enums.Timer.STAGE_HANG_UP, now, **kwargs)
        return common.mt(86, "You never hung up before")
    cfc = kwargs['config']['stages']['constraint']['hang-up']['ENDLESS']
    mul = int(min((now - tim).total_seconds(), cfc['limit'])//cfc['step'])
    config = kwargs['config']['stages']['hang-up'][f'{stage}']['rewards']
    rewards = {}
    # H 奖励普通物资
    await rw_common(uid, config['common'], rewards, mul=mul, **kwargs)
    # H 奖励特殊物资
    rewards['exp_info'] = await increase_exp(uid, config['special'].get('exp', 0) * mul, **kwargs)
    await common.set_timer(uid, enums.Timer.STAGE_HANG_UP, now, **kwargs)
    return common.mt(0, 'success', rewards)


async def hu_show(uid, **kwargs):
    now = datetime.now(tz=common.TZ_SH)
    tim = await common.get_timer(uid, enums.Timer.STAGE_HANG_UP, **kwargs)
    stage, _ = await common.get_stage(uid, enums.Stage.ENDLESS, **kwargs)
    tim = tim or now
    if stage == 1000:
        stage = 1001
    cfc = kwargs['config']['stages']['constraint']['hang-up']['ENDLESS']
    config = kwargs['config']['stages']['hang-up'][f'{stage}']['rewards']
    mul = int(min((now - tim).total_seconds(), cfc['limit'])//cfc['step'])
    results = [f"{s[:s.rfind(':')]}:{int(s[s.rfind(':')+1:])*mul}" for s in config['common']]
    return common.mt(0, 'success', {'show': results})


# ########################################### 私有方法 ############################################
async def rank_info(ads, page, **kwargs) -> list:
    return [{'NO': (page - 1)*10 + 1 + i, 'name': d[0],
            'damage': d[1], 'fid': d[2] or '',
             'level': (await increase_exp(d[3], 0, **kwargs))['level']} for i, d in enumerate(ads)]


async def rank_update(uid, key, stage, **kwargs):
    lid, tlid = enums.LeaderBoard.WORLD_BOSS, enums.LeaderBoard.TOTAL_WB
    # ds = await rank_own(uid, lid, stage, **kwargs)
    sds = await rank_own(uid, tlid, stage, **kwargs)
    # if ds is not None and ds[1] is None:
    #     ds = await rank_own(uid, lid, stage, **kwargs)
    if sds is not None and sds[1] is None:
        sds = await rank_own(uid, tlid, stage, **kwargs)
    rds = {
        # f'{lid}': {'damage': ds[0], 'rank': ds[1]},
        f'{tlid}': {'damage': sds[0], 'rank': sds[1]}
    }
    await kwargs['redis'].set(key, json.dumps(rds), expire=30)
    return rds


async def rank_all(lid, stage, page, **kwargs):
    return await common.execute(f'SELECT p.gn, l.value, p.fid, p.uid FROM '
                                f'player p, leaderboard l WHERE p.uid = l.uid '
                                f'AND l.lid = {lid} AND l.stage = {stage} ORDER'
                                f' BY l.value DESC LIMIT {(page - 1)*50}, 50;', **kwargs)


async def rank_own(uid, lid, stage, **kwargs):
    sql = \
        f"""SELECT c.value, c.NO FROM (
            SELECT * FROM (
                SELECT p.gn, l.value, (@i:=@i + 1) AS NO
                FROM player p, leaderboard l
                WHERE p.uid = l.uid AND l.lid = {lid} AND l.stage = {stage} ORDER BY l.value DESC) temp,
                (SELECT (@i:=0)) t ORDER BY temp.`value` DESC
            ) c, player p
        WHERE p.uid = "{uid}" AND c.gn = p.gn"""
    data = await common.execute(sql, **kwargs)
    return (0, -1) if data == () else data[0]


def addition(stage, **kwargs):
    els = kwargs['config']['enemy_layouts']['enemyLayouts']
    monsters = kwargs['config']['monster']
    el = els[-1]['enemyLayout'] if stage > len(els) else els[stage - 1]['enemyLayout']
    els = []
    key_words = []
    for layout in el:
        for enemy in layout['enemyList']:
            en = enemy['enemysPrefString']
            if en not in key_words:
                key_words.append(en)
                els.append({en: monsters[en]})
    del key_words
    return els, monsters


async def g_dispose(uid, stage, _stage, **kwargs):
    await task.record(uid, enums.Task.PASS_MAIN_STAGE, **kwargs)
    if stage > _stage:
        await achievement.record(uid, enums.Achievement.PASS_STAGE, **kwargs)


async def b_dispose(uid, stage, damage, results, **kwargs):
    """BOSS伤害记录等信息处理"""
    config = kwargs['config']['boss']
    boss_hp = config['hp'][kwargs['world']]
    lid, tlid = enums.LeaderBoard.WORLD_BOSS, enums.LeaderBoard.TOTAL_WB
    _damage = await get_leaderboard(uid, lid, stage, **kwargs)
    damage = min(damage, kwargs['config']['boss'].get('damage', 100_0000))
    record = _damage < damage
    total = await get_leaderboard(uid, tlid, stage, **kwargs) + damage
    await set_leaderboard(uid, tlid, total, stage, **kwargs)
    hp = max(0, boss_hp[f'{stage}'] - damage)
    boss_hp[f'{stage}'] = hp
    if record:
        await set_leaderboard(uid, lid, damage, stage, **kwargs)
    results['boss'] = {'record': int(record), 'stage': stage, 'bds': {
        'hp': hp, 'ratio': "%.2f" % (hp / config['HP'][f'{stage}']),
        'damage': max(damage, _damage), 'total': total}}
    await task.record(uid, enums.Task.PASS_WORLD_BOSS, **kwargs)


async def e_dispose(uid, stage, _stage, **kwargs):
    await task.record(uid, enums.Task.PASS_SPECIAL_STAGE, **kwargs)
    if stage == 1001 and stage > _stage: await hang_up(uid, **kwargs)


async def rw_common(uid, items, rewards, mul=1, **kwargs):
    """通用奖励信息的处理和修改"""
    results = await summoning.reward_items(uid, ','.join(items), mul=mul, **kwargs)
    rewards['remain'], rewards['reward'] = rm_rw(results)


def rm_rw(results):
    """剩余和改变情况的构造"""
    return [f'{g}:{i}:{v}' for g, i, v, _ in results], [f'{g}:{i}:{v}' for g, i, _, v in results]


async def v_coin(uid, lids, **kwargs):
    """验证金币挑战模式下的约束情况"""
    lv = (await vip.increase_exp(uid, 0, **kwargs))['level']
    config = kwargs['config']['stages']['constraint']['stage']['COIN']
    lcs = [config['limit'], config['buy']['vip'].get(f'{lv}', 2)]
    return await v_constraint(uid, enums.Timer.STAGE_COIN, lids, lcs, **kwargs)


async def v_exp(uid, lids, **kwargs):
    """验证经验挑战模式下的约束情况"""
    lv = (await vip.increase_exp(uid, 0, **kwargs))['level']
    config = kwargs['config']['stages']['constraint']['stage']['EXP']
    lcs = [config['limit'], config['buy']['vip'].get(f'{lv}', 2)]
    return await v_constraint(uid, enums.Timer.STAGE_EXP, lids, lcs, **kwargs)


async def v_constraint(uid, tid, lids, lcs, **kwargs):
    """各个模式下的验证、修改和重置"""
    now = datetime.now(tz=common.TZ_SH)
    tim = await common.get_timer(uid, tid, timeformat='%Y-%m-%d', **kwargs)
    lms = [await common.get_limit(uid, lid, **kwargs) for lid in lids]
    lms, tim = ({lids[i]: (lm - 1 if i == 0 else lm) for i, lm in enumerate(lcs)}, now + timedelta(days=1)) \
        if tim is None or now > tim else ({lids[i]: (lm - 1 if i == 0 else lm) for i, lm in enumerate(lms)}, tim)
    return lms[lids[0]] < 0, tim, lms


async def r_constraint(uid, tid, tim, lms, **kwargs):
    """实现相应模式下的修改和重置"""
    if tim is not None:
        await common.set_timer(uid, tid, tim, timeformat='%Y-%m-%d', **kwargs)
    [await common.set_limit(uid, lid, lim, **kwargs) for lid, lim in lms.items()]


async def increase_exp(uid, exp, **kwargs):
    """
    exp为0则获得经验，反之增加经验，
    并返回总经验和等级，升到下一级需要的经验
    """
    # H 取配置和数据
    exp_config = kwargs['config']['exp']['player_level']['experience']
    sql_exp = await common.get_progress(uid, 'exp', **kwargs)
    # H 计算等级和需要的经验
    level, need = common.__calculate(exp_config, sql_exp)
    if exp == 0: return {'exp': sql_exp, 'level': level, 'need': need, 'reward': exp}
    # H 重新计算等级和需要的经验
    sql_exp += exp
    level, need = common.__calculate(exp_config, sql_exp)
    await common.set_progress(uid, 'exp', sql_exp, **kwargs)
    # H 返回总经验、等级、需要经验
    return {'exp': sql_exp, 'level': level, 'need': need, 'reward': exp}


async def get_leaderboard(uid, lid, stage=3000, **kwargs):
    data = await common.execute(f'SELECT value FROM leaderboard WHERE uid = "{uid}" AND lid = {lid} AND stage = {stage};', **kwargs)
    return 0 if data == () else data[0][0]


async def set_leaderboard(uid, lid, damage, stage=3000, **kwargs):
    await common.execute(f'INSERT INTO leaderboard VALUES ("{uid}", {lid}, {stage}, {damage}) ON DUPLICATE KEY UPDATE value="{damage}";;', **kwargs)


async def init(uid, **kwargs):
    await asyncio.gather(
        common.set_stage(uid, enums.Stage.GENERAL, 1, '', **kwargs),
        common.set_stage(uid, enums.Stage.ENDLESS, 1000, '', **kwargs),
        common.set_stage(uid, enums.Stage.BOSS, 3000, '', **kwargs),
        common.set_stage(uid, enums.Stage.COIN, 4000, '', **kwargs),
        common.set_stage(uid, enums.Stage.EXP, 4150, '', **kwargs),
    )


STAGE_CHECK = {
    enums.Stage.GENERAL: lambda s: 0 < s < 1000,
    enums.Stage.ENDLESS: lambda s: 1000 < s < 2000,
    enums.Stage.BOSS: lambda s: 3000 < s < 4000,
    enums.Stage.COIN: lambda s: 4000 < s < 4150,
    enums.Stage.EXP: lambda s: 4150 < s < 4300,
}


VERIFY = {
    enums.Stage.BOSS: lambda uid, **kwargs: v_constraint(uid, enums.Timer.STAGE_WORLD_BOSS, [enums.Limits.STAGE_WORLD_BOSS, ], [kwargs['config']['boss']['limit'], ], **kwargs),
    enums.Stage.COIN: lambda uid, **kwargs: v_coin(uid, [enums.Limits.STAGE_COIN, enums.Limits.STAGE_COIN_VIP], **kwargs),
    enums.Stage.EXP: lambda uid, **kwargs: v_exp(uid, [enums.Limits.STAGE_EXP, enums.Limits.STAGE_EXP_VIP], **kwargs),
}


REALIZE = {
    enums.Stage.BOSS: lambda uid, tim, lms, **kwargs: r_constraint(uid, enums.Timer.STAGE_WORLD_BOSS, tim, lms, **kwargs),
    enums.Stage.COIN: lambda uid, tim, lms, **kwargs: r_constraint(uid, enums.Timer.STAGE_COIN, tim, lms, **kwargs),
    enums.Stage.EXP: lambda uid, tim, lms, **kwargs: r_constraint(uid, enums.Timer.STAGE_EXP, tim, lms, **kwargs),
}


VICTORY_DISPOSE = {
    enums.Stage.GENERAL: lambda uid, stage, _stage, damage, results, **kwargs: g_dispose(uid, stage, _stage, **kwargs),
    enums.Stage.BOSS: lambda uid, stage, _stage, damage, results, **kwargs: b_dispose(uid, stage, damage, results, **kwargs),
    enums.Stage.ENDLESS: lambda uid, stage, _stage, damage, results, **kwargs: e_dispose(uid, stage, _stage, **kwargs),
}








