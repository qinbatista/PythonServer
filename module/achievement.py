'''
achievement.py
'''

from module import enums
from module import common

#


async def get_all_achievement(uid, **kwargs):
	achievement = await common.execute(f'SELECT aid, value, reward FROM achievement WHERE uid = "{uid}";', **kwargs)
	kwargs.update({"aid":enums.Achievement.TOTAL_LOGIN.value,"value":1})
	await record_achievement(uid,**kwargs)
	return common.mt(0, 'success', {'achievements': [{'aid': a[0], 'value': a[1], 'reward': a[2]} for a in achievement]})

async def record_achievement(uid, **kwargs):# aid->enums.Achievement,value->string
	data = await common.execute(f'INSERT INTO achievement (uid, aid, value,reward) VALUES ("{uid}", {kwargs["aid"]}, {kwargs["value"]},0) ON DUPLICATE KEY UPDATE `value`= `value`+{kwargs["value"]}',**kwargs)
	return common.mt(0, 'record:'+str(kwargs["aid"])+" success")

async def get_achievement_reward(uid, **kwargs):
	config = kwargs["config"][str.lower(enums.Achievement(kwargs["data"]["achievement_id"]).name)]
	quantity = config["quantity"][::-1]
	amount = config["diamond"][::-1]
	data = await common.execute(f'SELECT value, reward FROM achievement WHERE uid = "{uid}" AND aid = "{kwargs["data"]["achievement_id"]}"',**kwargs)
	if len(quantity)!=len(amount):return common.mt(98,'data base problem, achievement configuration is not match')
	for qindex,my_quantity in enumerate(quantity):
		if data[0][0]>=my_quantity:
			for aindex,myamount in enumerate(amount):
				if data[0][1] == myamount:
					_,remaining = await common.try_item(uid,enums.Item.DIAMOND,amount[aindex-1], **kwargs)
					await common.execute_update(f'UPDATE achievement set reward = {amount[aindex-1] if data[0][1] != amount[0] else amount[aindex]} WHERE uid = "{uid}" AND aid = "{kwargs["data"]["achievement_id"]}";', **kwargs)
					return common.mt(0, 'get reward success',{"achievement":{"item":{"item_id":5,"remaining":remaining,"reward":amount[aindex-1] if data[0][1] != amount[0] else amount[aindex]},"achievement":{"value":data[0][0],"reward":quantity[aindex-1] if data[0][1] != quantity[0] else quantity[aindex],"aid":enums.Achievement(kwargs["data"]["achievement_id"])}}})
	return common.mt(99,'no reward for this achievement {str.lower(enums.Achievement.TOTAL_LOGIN.name}')
