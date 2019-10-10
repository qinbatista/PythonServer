'''
stage.py
'''

from module import enums
from module import common


async def enter_stage(uid, stage, entry_consume, **kwargs):  # entry_consume=self._entry_consumables["stage"]
	can_e, energy = await common.try_item(uid, enums.Item.ENERGY, 0, **kwargs)
	can_s, stage_s = await get_progress(uid, 'stage', **kwargs)
	if not can_s or stage <= 0 or stage > stage_s + 1:
		return common.mt(99, 'Parameter error')

	stages = [int(x) for x in entry_consume.keys()]
	if stage not in stages: stage = max(stages)
	keys = list(entry_consume[str(stage)].keys())
	values = [-1 * int(v) for v in list(entry_consume[str(stage)].values())]
	remaining = {}
	reward = {'exp': 0, 'level': 0}
	for i in range(len(keys)):
		if keys[i] == 'exp':
			_, exp = await get_progress(uid, 'exp', **kwargs)
			remaining.update({'exp': exp + values[i]})
		await common.try_item(uid, 0)
		material_dict.update({keys[i]: values[i]})
	await common.execute(f'SELECT {", ".join(material_dict.keys())} FROM item WHERE ')
	condition = ' AND '.join([f'`{cond[0]}` = "{cond[1]}"' for cond in conditions])

	update_str, select_str = self._sql_str_operating(unique_id, material_dict)
	select_values = (await self._execute_statement(world, select_str))[0]
	for i in range(len(select_values)):
		values[i] = int(values[i]) + int(select_values[i])
		if values[i] < 0:
			return self._message_typesetting(98, "%s insufficient" % keys[i])
	if "energy" in keys:
		energy_data = await self.try_energy(world=world, unique_id=unique_id, amount=material_dict["energy"])
		if energy_data["status"] >= 97:
			return self._message_typesetting(status=97, message="Insufficient energy")

		level, experience = (await self._execute_statement(world=world,
														   statement=f'select level, experience from player where unique_id="{unique_id}"'))[
			0]  # try成功了，一定存在这个列表
		player_experience = self._player_experience['player_level']['experience'][level]
		max_level = self._player_experience['player_level']['max_level']
		reward['experience'] = 10 * abs(material_dict["energy"])
		experience += 10 * abs(material_dict["energy"])
		while experience >= player_experience:
			if level >= max_level: break
			reward['level'] += 1
			level += 1
			experience -= player_experience
			player_experience = self._player_experience['player_level']['experience'][level]
		await self._execute_statement_update(world,
											 f'update player set level={level}, experience={experience} where unique_id="{unique_id}"')
		remaining.update({'experience': experience, 'level': level, 'max_level': max_level})

		values.pop(keys.index("energy"))
		keys.remove("energy")
		material_dict.pop("energy")
		for i in range(len(energy_data["data"]["keys"])):
			remaining.update({energy_data["data"]["keys"][i]: energy_data["data"]["values"][i]})

	if material_dict:
		update_str, select_str = self._sql_str_operating(unique_id, material_dict)
		await self._execute_statement_update(world, update_str)
	for i in range(len(keys)):
		remaining.update({keys[i]: values[i]})
	enemyLayouts = self._level_enemy_layouts['enemyLayouts']
	if stage > len(enemyLayouts):
		enemyLayoutList = enemyLayouts[-1]['enemyLayout']
	else:
		enemyLayoutList = enemyLayouts[stage - 1]['enemyLayout']
	remaining.update({'enemyLayoutList': enemyLayoutList})
	enemyList = []
	for layout in enemyLayoutList:
		for enemy in layout['enemyList']:
			enemyList.append(enemy['enemysPrefString'])
	enemyList = list(set(enemyList))
	remaining.update({'enemy_kind': {}})
	for enemy in enemyList:
		if enemy not in list(self._monster_config.keys()):
			remaining['enemy_kind'].update({enemy: {}})
		else:
			remaining['enemy_kind'].update({enemy: self._monster_config[enemy]})

	return self._message_typesetting(0, "success", {"remaining": remaining, 'reward': reward})
	achievement = await common.execute(f'SELECT aid, value, reward FROM achievement WHERE uid = "{uid}";', **kwargs)
	return common.mt(0, 'success', {'achievements': [{'aid': a[0], 'value': a[1], 'reward': a[2]} for a in achievement]})




####################################################################################

async def get_progress(uid, pid, **kwargs):
	pdata = await common.execute(f'SELECT {pid} FROM progress WHERE uid = "{uid}";', **kwargs)
	return (True, pdata[0][0]) if pdata != () else (False, 0)


async def increase_exp(uid, exp, exp_config, **kwargs):
	"""
	exp:Need to increase the experience value
	exp = exp_increase
	exp_s:Exp data in the server
	exp_s = exp_server
	exp_config:Level configuration information
	exp_config = self._player['player_level']['experience']
	"""
	exp_data = await common.execute(f'SELECT exp FROM progress WHERE uid = "{uid}";', **kwargs)
	if exp_data == (): return False, {'exp': 0, 'level': 0, 'need': 0}
	exp_s = exp_data[0][0]
	exp_list = [e for e in exp_config if e > exp_s]
	if exp == 0: return True, {'exp': exp_s, 'level': exp_config.index(exp_list[0]) if exp_list != [] else len(exp_config), 'need': exp_list[0] - exp_s if exp_list != [] else 0}
	exp_s += exp
	_, exp_s = await common.execute_update(f'UPDATE progress SET exp = {exp_s} WHERE uid = "{uid}";', **kwargs)
	return True, {'exp': exp_s, 'level': exp_config.index(exp_list[0]) if exp_list != [] else len(exp_config), 'need': exp_list[0] - exp_s if exp_list != [] else 0}



