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
import random
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
    # TODO 部分约束信息
    tim, lms = None, {}
    if sid in VERIFY:
        can, tim, lms = await VERIFY[sid](uid, **kwargs)
        if can:
            return common.mt(92, 'no more ticket, try tomorrow')
        results[sid.name] = {'limits': lms, 'cd': common.remaining_cd()}
    # TODO 检查特殊物资是否能消耗
    energy = config['consumes']['special'].get('energy', 0)
    if (await common.try_energy(uid, 0, **kwargs))['data']['energy'] < energy:
        return common.mt(97, 'energy insufficient')
    # TODO 尝试消耗通用物资
    can, cmw = await common.consume_items(uid, ','.join(config['consumes']['common']), **kwargs)
    if not can:
        return common.mt(95, 'materials insufficient')
    results['remain'], results['reward'] = rm_rw(cmw)
    # TODO 消耗特殊物资(体力)
    data = (await common.try_energy(uid, -energy, **kwargs))['data']
    # TODO 实现部分约束
    if sid in VERIFY:
        await REALIZE[sid](uid, tim, lms, **kwargs)
    # TODO 附加配置
    els, monsters = addition(stage, **kwargs)
    results['addition'] = {'els': els, 'monsters': monsters}
    # TODO 构建结果
    results['energy'] = {'cooling': data['cooling_time'], 'remain': data['energy'], 'reward': -energy}
    # TODO 设置关卡进入状态
    btm = datetime.now(tz=common.TZ_SH).strftime('%Y-%m-%d %H:%M:%S')
    await common.set_stage(uid, sid, _stage, btm, **kwargs)
    await kwargs['redis'].set(f'stage.{uid}', stage)
    return common.mt(0, 'success', results)


async def victory(uid, sid, stage, damage=0, **kwargs):
    """通关"""
    if not STAGE_CHECK[sid](stage):
        return common.mt(91, 'stage error')
    _stage, _btm = await common.get_stage(uid, sid, **kwargs)
    _stg = await kwargs['redis'].get(f'stage.{uid}')
    if _btm == '' or _stg is None or stage != int(_stg):
        return common.mt(94, 'stage mismatch')
    config, rewards = kwargs['config']['stages']['stage'].get(f'{stage}', None), {'boss': {}}
    # TODO 奖励普通物资
    rwc = config['rewards']['common']
    if config['constraint']['random'] == 1:
        rwc = random.choices(rwc, k=config['rewards']['random'])
    await rw_common(uid, rwc, rewards, **kwargs)
    # TODO 奖励特殊物资
    rewards['exp_info'] = await increase_exp(uid, config['rewards']['special'].get('exp', 0), **kwargs)
    rewards['max_stage'] = max(stage, _stage)
    # TODO 特殊处理
    if sid in VICTORY_DISPOSE:
        cm = await VICTORY_DISPOSE[sid](uid, stage, _stage, damage, rewards, **kwargs)
        if isinstance(cm, tuple):
            return common.mt(cm[0], cm[1])
    # TODO 设置关卡通过状态
    await common.set_stage(uid, sid, max(stage, _stage), '', **kwargs)
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
    # TODO 检查特殊物资是否能消耗
    energy = config['consumes']['special'].get('energy', 0) * count
    if (await common.try_energy(uid, 0, **kwargs))['data']['energy'] < energy: return common.mt(97, 'energy insufficient')
    # TODO 尝试消耗通用物资
    if not (await common.consume_items(uid, ','.join([f'{r[:r.rfind(":")]}:{int(r[r.rfind(":") + 1:]) * count}' for r in config['consumes']['common']]), **kwargs))[0]:
        return common.mt(95, 'materials insufficient')
    # TODO 消耗特殊物资(体力)
    data = (await common.try_energy(uid, -energy, **kwargs))['data']
    rewards = {'energy': {'cooling': data['cooling_time'], 'remain': data['energy'], 'reward': -energy}}
    # TODO 奖励普通物资
    await rw_common(uid, config['rewards']['common'], rewards, mul=count, **kwargs)
    # TODO 奖励特殊物资
    rewards['exp_info'] = await increase_exp(uid, config['rewards']['special']['exp'] * count, **kwargs)
    return common.mt(0, 'success', rewards)


async def refresh_boss(uid, **kwargs):
    config = kwargs['config']['boss']
    now = datetime.now(tz=common.TZ_SH)
    ratio = {s: "%.2f" % (hp / config['HP'][s]) for s, hp in
             config['hp'].items()}
    damage = await get_leaderboard(uid, enums.LeaderBoard.WORLD_BOSS, **kwargs)
    tid, lid = enums.Timer.STAGE_WORLD_BOSS, enums.Limits.STAGE_WORLD_BOSS
    tim = await common.get_timer(uid, tid, timeformat='%Y-%m-%d', **kwargs)
    lim = await common.get_limit(uid, lid, **kwargs)
    if tim is None or now > tim:
        lim, tim = kwargs['config']['boss']['limit'], now + timedelta(days=1)
        await common.set_limit(uid, lid, lim, **kwargs)
        await common.set_timer(uid, tid, tim, timeformat='%Y-%m-%d', **kwargs)
    return common.mt(0, 'Successfully get hook information', {'damage': damage, 'limit': lim, 'cd': common.remaining_cd(), 'mcd': common.remaining_month_cd(), 'ratio': ratio})


async def all_infos(uid, **kwargs):
    """获取所有的关卡信息"""
    sts = await common.execute(f'SELECT `sid`, `stage` FROM `stages` WHERE `uid` = "{uid}";', **kwargs)
    ds = {s[0]: s[1] for s in sts}
    return common.mt(0, 'success', ds)


async def damage_ranking(uid, page, **kwargs):
    if page < 1:
        return common.mt(89, 'Page number error')
    uid_str = f"""
    SELECT c.value, c.NO FROM (
        SELECT * FROM (
            SELECT p.gn, l.value, (@i:=@i + 1) AS NO
            FROM player p, leaderboard l
            WHERE p.uid = l.uid AND l.lid = {enums.LeaderBoard.WORLD_BOSS.value} ORDER BY l.value DESC) temp,
            (SELECT (@i:=0)) t ORDER BY temp.`value` DESC
        ) c, player p
    WHERE p.uid = "{uid}" AND c.gn = p.gn
    """
    damage = 0  # 玩家造成的伤害
    ranking = -1  # 玩家在世界boss表中的排行
    cached_uid_data = await kwargs['redis'].hgetall(f'leaderboard.player.{kwargs["world"]}.{uid}')
    if len(cached_uid_data) == 0:
        uid_data = await common.execute(uid_str, **kwargs)
        if uid_data != ():
            damage = uid_data[0][0]
            if uid_data[0][1] is None: uid_data = await common.execute(uid_str, **kwargs)
            ranking = int(uid_data[0][1])
            await kwargs['redis'].hmset_dict(f'leaderboard.player.{kwargs["world"]}.{uid}',
                                             {'damage' : uid_data[0][0], 'rank': int(uid_data[0][1])})
            await kwargs['redis'].expire(f'leaderboard.player.{kwargs["world"]}.{uid}', 30)
    else:
        damage, ranking = cached_uid_data['damage'], int(cached_uid_data['rank'])

    data = await common.execute(f'SELECT p.gn, l.value, p.fid, p.uid FROM player p, leaderboard l WHERE p.uid = l.uid AND l.lid = {enums.LeaderBoard.WORLD_BOSS} ORDER BY l.value DESC LIMIT {(page - 1)*10},10;', **kwargs)
    if data == (): return common.mt(88, 'No data for this page')
    rank = [{'NO': (page - 1)*10 + 1 + i, 'name': d[0], 'damage': d[1], 'fid': '' if d[2] is None else d[2], 'level': (await increase_exp(d[3], 0, **kwargs))['level']} for i, d in enumerate(data)]
    return common.mt(0, 'success', {'page': page, 'damage': damage, 'ranking': ranking, 'rank': rank})


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
    # TODO 奖励普通物资
    await rw_common(uid, config['common'], rewards, mul=mul, **kwargs)
    # TODO 奖励特殊物资
    rewards['exp_info'] = await increase_exp(uid, config['special'].get('exp', 0) * mul, **kwargs)
    await common.set_timer(uid, enums.Timer.STAGE_HANG_UP, now, **kwargs)
    return common.mt(0, 'success', rewards)


# ########################################### 私有方法 ############################################
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


async def b_dispose(uid, stage, damage, results, **kwargs):
    """BOSS伤害记录等信息处理"""
    config, _damage = kwargs['config']['boss'], await get_leaderboard(uid, enums.LeaderBoard.WORLD_BOSS, **kwargs)
    record = _damage < damage
    if damage < 0 or damage >= kwargs['config']['boss'].get('damage', 100_0000):
        return 93, "abnormal damage"
    else:
        hp = config['hp'][f'{stage}']
        config['hp'][f'{stage}'] = max(0, hp - damage)
        if record:
            await set_leaderboard(uid, enums.LeaderBoard.WORLD_BOSS, damage, **kwargs)
        ratio = {s: "%.2f" % (hp/config['HP'][s]) for s, hp in config['hp'].items()}
        results['boss'] = {'ratio': ratio, 'record': int(record), 'damage': max(damage, _damage)}


async def rw_common(uid, common, rewards, mul=1, **kwargs):
    """通用奖励信息的处理和修改"""
    cms = ','.join([f'{multiple_rw(mul, item)}' for item in common])
    results = await summoning.reward_items(uid, cms, **kwargs)
    rewards['remain'], rewards['reward'] = rm_rw(results)


def multiple_rw(mul, item):
    """倍数构造"""
    return f'{item[:item.rfind(":")]}:{int(item[item.rfind(":") + 1:]) * mul}'


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
    await common.set_timer(uid, tid, tim, timeformat='%Y-%m-%d', **kwargs)
    [await common.set_limit(uid, lid, lim, **kwargs) for lid, lim in lms.items()]


async def increase_exp(uid, exp, **kwargs):
    """
    exp为0则获得经验，反之增加经验，
    并返回总经验和等级，升到下一级需要的经验
    """
    # TODO 取配置和数据
    exp_config = kwargs['config']['exp']['player_level']['experience']
    sql_exp = await common.get_progress(uid, 'exp', **kwargs)
    # TODO 计算等级和需要的经验
    level, need = common.__calculate(exp_config, sql_exp)
    if exp == 0: return {'exp': sql_exp, 'level': level, 'need': need, 'reward': exp}
    # TODO 重新计算等级和需要的经验
    sql_exp += exp
    level, need = common.__calculate(exp_config, sql_exp)
    await common.set_progress(uid, 'exp', sql_exp, **kwargs)
    # TODO 返回总经验、等级、需要经验
    return {'exp': sql_exp, 'level': level, 'need': need, 'reward': exp}


async def get_leaderboard(uid, lid, **kwargs):
    data = await common.execute(f'SELECT value FROM leaderboard WHERE uid = "{uid}" AND lid = {lid};', **kwargs)
    return 0 if data == () else data[0][0]


async def set_leaderboard(uid, lid, damage, **kwargs):
    await common.execute(f'INSERT INTO leaderboard (uid, lid, value) VALUES ("{uid}", {lid}, {damage});', **kwargs)


async def init_stages(uid, **kwargs):
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
    enums.Stage.BOSS: lambda uid, stage, _stage, damage, results, **kwargs: b_dispose(uid, stage, damage, results, **kwargs),
    enums.Stage.ENDLESS: lambda uid, stage, _stage, damage, results, **kwargs: hang_up(uid, new=stage > _stage, **kwargs),
}








