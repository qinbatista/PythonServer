'''
achievement.py
'''

from module import enums
from module import common
from module import mail


#


async def get_all_achievement(uid, **kwargs):
	achievement = await common.execute(f'SELECT aid, value, reward FROM achievement WHERE uid = "{uid}";', **kwargs)
	if achievement == (): return common.mt(0, 'success', {'achievements': []})
	# kwargs.update({"aid":enums.Achievement.TOTAL_LOGIN.value})
	# await record_achievement(uid,**kwargs)
	# kwargs['items'] = common.encode_item(enums.Group.ITEM, enums.Item.DIAMOND, 1)
	# await mail.send_mail(enums.MailType.GIFT, uid, **kwargs)
	return common.mt(0, 'success',
					 {'achievements': [{'aid': a[0], 'value': a[1], 'reward': a[2]} for a in achievement]})


async def record_achievement(uid, **kwargs):  # aid->enums.Achievement,value->string
	data = await common.execute(
		f'INSERT INTO achievement (uid, aid, value,reward) VALUES ("{uid}", {kwargs["aid"]}, {1},0) ON DUPLICATE KEY UPDATE `value`= `value`+{1}',
		**kwargs)
	return common.mt(0, 'record:' + str(kwargs["aid"]) + " success")


async def get_achievement_reward(uid, aid, **kwargs):
	if aid not in enums.Achievement._value2member_map_.keys(): return common.mt(97, 'Aid does not exist')
	config = kwargs["config"][str.lower(enums.Achievement(aid).name)]
	quantity = config["quantity"]
	amount = config["diamond"]
	data = await common.execute(f'SELECT value, reward FROM achievement WHERE uid = "{uid}" AND aid = "{aid}"',
								**kwargs)
	if len(quantity) != len(amount): return common.mt(98, 'data base problem, achievement configuration is not match')
	for index, my_quantity in enumerate(quantity):
		if data[0][1] < my_quantity <= data[0][0]:  # reward是领奖时的成就次数，value是完成成就的次数
			_, remaining = await common.try_item(uid, enums.Item.DIAMOND, amount[index], **kwargs)
			await common.execute_update(
				f'UPDATE achievement set reward = {my_quantity} WHERE uid = "{uid}" AND aid = "{aid}";', **kwargs)
			return common.mt(0, 'get reward success',
							 {"remaining": {"item_id": 5, "item_value": remaining, "aid": aid, "value": data[0][0]},
							  "reward": {"item_id": 5, "item_value": amount[index], "aid": aid, "value": quantity[index]}})
	return common.mt(99, f'no reward for this achievement:{enums.Achievement(aid).name}')
