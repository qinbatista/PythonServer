import tool_lukseun_client
import module_1_login
import module_2_get_all_data
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
	module_2_get_all_data.get_all_info(token,world)
if __name__ == "__main__":
	call_login("0")
	call_get_all_info()#加载所有参数信息
	# freind_dialog(token)#朋友界面
	# skill_dialog(token)#技能界面
	# weapon_dialog(token)#武器界面
	# factory_dialog(token)#工厂界面
	# get_random_item(token)#抽奖界面
	# role_dialog(token)#角色界面
