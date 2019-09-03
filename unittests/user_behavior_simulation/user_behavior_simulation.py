import tool_lukseun_client
import module_1_login
import module_2_get_all_data
import module_3_friends
import module_4_skills
world = "0"
token = ""
def call_login(unique_id):
	global world,token
	while True:
		world = module_1_login.login_module(unique_id)
		if world!=None:
			token,world = world
			if token!="":break
def call_get_all_info():
	return module_2_get_all_data.get_all_info(token,world)

def call_friend_dialog(get_all_friend_info):
	module_3_friends.freind_dialog(token,world,get_all_friend_info)

def skill_dialog(get_all_friend_info):
	module_4_skills.skill_dialog(token,world,get_all_friend_info)

if __name__ == "__main__":
	call_login("0")
	get_level_info,get_all_friend_info,get_all_skill_level,get_all_weapon,refresh_all_storage,get_all_roles,get_stage_info,get_monster_info,get_factory_info,get_all_family_info,get_all_mail,get_all_armor_info = call_get_all_info()#加载所有参数信息
	# call_friend_dialog(get_all_friend_info)#朋友界面
	skill_dialog(get_all_skill_level)#技能界面
	# weapon_dialog(token)#武器界面
	# faåctory_dialog(token)#工厂界面
	# get_random_item(token)#抽奖界面
	# role_dialog(token)#角色界面
