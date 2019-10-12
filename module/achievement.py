'''
achievement.py
'''

from module import enums
from module import common

#


async def get_all_achievement(uid, **kwargs):
	achievement = await common.execute(f'SELECT aid, value, reward FROM achievement WHERE uid = "{uid}";', **kwargs)
	kwargs.update({"aid":enums.Achievement.TOTAL_LOGIN,"value":1})
	await record_achievement(uid,**kwargs)
	return common.mt(0, 'success', {'achievements': [{'aid': a[0], 'value': a[1], 'reward': a[2]} for a in achievement]})

async def record_achievement(uid, **kwargs):
	data = await common.execute(f'INSERT INTO achievement (uid, aid, value,reward) VALUES ("{uid}", {kwargs["aid"]}, {kwargs["value"]},0) ON DUPLICATE KEY UPDATE `value`= `value`+{kwargs["value"]}',**kwargs)
	return common.mt(0, 'record:'+kwargs["aid"]+" success")

async def get_achievement_reward(uid, **kwargs):
	# world, unique_id, achievement_id, value
	# achievement_id_list=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
	# achievement_id_name_list=["total_login","keeping_login","vip_level","get_role_4_star","get_role_5_star","get_role_6_star","level_up_role","get_weapon_4_star","get_weapon_5_star","get_weapon_6_star","level_up_weapon","reward_level","collect_food","collect_mine","collect_crystal","upgrade_food_factory","upgrade_mine_factory","upgrade_crystal_crystal","summon_times","friend_request","friend_gift","check_in_family"]
	# if achievement_id not in achievement_id_list:#check if achievement is in list
	# 	return self._message_typesetting(99, f'this achivement is not in list: {str(achievement_id)}')
	config = kwargs["config"][str.lower(enums.Achievement.TOTAL_LOGIN.name)]
	quantity = config["quantity"][::-1]
	amount = config["diamond"][::-1]
	print("quantity="+str(quantity))
	print("amount="+str(amount))
	data = await common.execute(f'SELECT value, reward FROM achievement WHERE uid = "{uid}" AND aid = "{kwargs["data"]["achievement_id"]}"',**kwargs)
	print("data = "+str(data))
	for qindex,my_quantity in enumerate(quantity):
		if data[0][0]>=my_quantity:
			for aindex,myamount in enumerate(amount):
				if data[0][1] == myamount:
					_,remaining = await common.try_item(uid,enums.Item.DIAMOND,amount[aindex-1], **kwargs)
					await common.execute_update(f'UPDATE achievement set reward = {amount[aindex-1]} WHERE uid = "{uid}" AND aid = "{kwargs["data"]["achievement_id"]}";', **kwargs)
					return common.mt(0, 'get reward success',{"achievement":{"diamond":remaining,"value":data[0][0],"reward":amount[aindex-1],"name":str.lower(enums.Achievement.TOTAL_LOGIN.name)}})
	return common.mt(99,'no reward for this achievement {str.lower(enums.Achievement.TOTAL_LOGIN.name}')
	# kwargs["uid"]
	# achievement_id_name = achievement_id_name_list[achievement_id]
	# # print("achievement_id_name="+achievement_id_name)
	# quantity_list = self._acheviement[achievement_id_name]["quantity"]
	# index_reward = quantity_list.index(data[0][1])
	# # print("index_reward="+str(index_reward))
	# for this_quantity,index in enumerate(quantity_list):
	# 	# print("quantity_list="+str(quantity_list))
	# 	# print("data[0][0]="+str(data[0][0]))
	# 	# print("data[0][1]="+str(data[0][1]))
	# 	# print("this_quantity="+str(this_quantity))
	# 	# print("len(quantity_list)="+str(len(quantity_list)))
	# 	if len(quantity_list)==index_reward+1:
	# 		return self._message_typesetting(2, f'you already get all reward')
	# 	if  quantity_list[index_reward+1]<=data[0][0] and data[0][0]!=0:
	# 		# print(f'UPDATE player SET diamond = diamond+{self._acheviement[achievement_id_name]["diamond"][index+1]} WHERE unique_id = "{unique_id}";')
	# 		await self._execute_statement(world,f'UPDATE achievement SET achievement_value_reward = {quantity_list[index_reward+1]} WHERE unique_id = "{unique_id}" AND achievement_id = "{achievement_id}";')
	# 		await self._execute_statement(world,f'UPDATE player SET diamond = diamond+{self._acheviement[achievement_id_name]["diamond"][index+1]} WHERE unique_id = "{unique_id}";')
	# 		result_diamond = await self._execute_statement(world, f'SELECT diamond FROM player WHERE unique_id = "{unique_id}"')
	# 		# print("result_diamond="+str(result_diamond[0][0]))
	# 		data ={
	# 			"remaing":
	# 			{
	# 				"diamond":result_diamond[0][0]+self._acheviement[achievement_id_name]["diamond"][index+1],
	# 				"achievement_id":achievement_id,
	# 				"achievement_value":data[0][0],
	# 				"achievement_value_reward":quantity_list[index_reward+1]
	# 			},
	# 			"reward":
	# 			{
	# 				"diamond":self._acheviement[achievement_id_name]["diamond"][index+1],
	# 			}
	# 		}
	# 		return self._message_typesetting(0, f'get reward success',data)
	# return self._message_typesetting(98, f'can not get reward')