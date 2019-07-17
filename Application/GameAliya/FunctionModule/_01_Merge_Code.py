import os,platform

def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
def FindAllInFolder(_path):
	ListMyFolder = []
	for filename in os.listdir(_path):
		ListMyFolder.append(_path+"/"+filename)
	return ListMyFolder

def FindAll(_path):
	ListMyFolder = []
	for dirpath, dirnames, filenames in os.walk(_path):
		#print ('Directory', dirpath)
		dirnames
		for filename in filenames:
			#print (' File', filename)
			ListMyFolder.append(dirpath+"/"+filename)
	return ListMyFolder
def CurrentPlatform():
	sysstr = platform.system()
	if(sysstr =="Windows"):
		return "Windows"
	elif(sysstr == "Linux"):
		return "Linux"
	elif(sysstr == "Darwin"):
		return "Mac"
	else:
		return "None"
routes_code = []
class_method_code = []
import_code = []
def get_routes(file_path):
	file_object = open(file_path,encoding="utf-8")
	global routes_code
	all_the_text = file_object.readlines()
	is_find_key=False
	# print("finding routes:"+file_path)
	for i in all_the_text:
		if is_find_key == False and i.find("@ROUTES.post")!=-1:
			is_find_key = True
			routes_code.append(i)
		elif is_find_key==True:
			if i.find("\t")>=0:
				routes_code.append(i)
			elif i.find("async def")!=-1:
				routes_code.append(i)
			else:
				is_find_key=False


	# 	if i.find("\t")<0:
	# 		if i.find("async def")!=-1:
	# 			routes_code.append(i)
	# 			is_find_key=False
	# 		else:
	# 			continue
	return routes_code

def get_class_method(file_path):
	file_object = open(file_path,encoding="utf-8")
	global class_method_code
	all_the_text = file_object.readlines()
	is_find_key=False
	start_continue=False
	# print("finding class method:"+file_path)
	for i in all_the_text:
		if is_find_key == False and i.find("\tasync def")!=-1:
			is_find_key = True
			class_method_code.append(i)
		elif is_find_key==True and i.find("\t")==0:
			if i.find("async def _execute_statement")!=-1 or i.find("def message_typesetting")!=-1:
				start_continue = True
				# class_method_code.append(i)
			elif start_continue == True:
				if i.find("\t")<=0 and i.count("\t")<=1:
					start_continue=False
					class_method_code.append(i)
				else:
					continue
			else:
				class_method_code.append(i)
		elif is_find_key==True and i.find("\t")!=0 and i != "\n" and i != "\r":
			break
	return class_method_code
def get_import(file_path):
	file_object = open(file_path,encoding="utf-8")
	global import_code
	all_the_text = file_object.readlines()
	is_find_import_insert_key=False
	for i in all_the_text:
		if is_find_import_insert_key == False and i.find("import")==0:
			import_code.append(Re_check_import(i))
			is_find_import_insert_key=True
		elif is_find_import_insert_key == True:
			if i.find("class ")==0:
				break
			import_code.append(Re_check_import(i))
	return import_code
def Re_check_import(string_line):
	if string_line.find("CONFIG['bag_manager']")!=-1:
		string_line = string_line.replace("CONFIG['bag_manager']","CONFIG['_04_Manager_Player']")
	if string_line.find("../../Configuration/server.conf")!=-1:
		string_line = string_line.replace("../../Configuration/server.conf","../Configuration/server.conf")
	return string_line
def merge_content_to_manager(file_name):
	file_object = open(PythonLocation()+"/../"+file_name+".py",encoding="utf-8")
	print(PythonLocation()+"/../"+file_name+".py")
	new_file_content = []
	all_the_text = file_object.readlines()
	is_find_class_insert_key=False
	is_find_route_insert_key=False
	is_find_import_insert_key =False
	for i in all_the_text:
		if is_find_class_insert_key == False and i.find("class")==0:
			new_file_content.append(i)
			new_file_content = new_file_content+class_method_code
			is_find_class_insert_key=True
		elif is_find_route_insert_key == False and i.find("@ROUTES.get")==0:
			new_file_content = new_file_content+routes_code
			is_find_route_insert_key=True
			new_file_content.append(i)
		elif is_find_import_insert_key == False and i.find("import")==0:
			new_file_content = new_file_content+import_code
			is_find_import_insert_key=True
			new_file_content.append(i)
		else:
			new_file_content.append(i)
	with open(PythonLocation()+"/../"+file_name+".py", 'w',encoding="utf-8") as json_file:
		for i in new_file_content:
			json_file.writelines(i)

def search_merge_content(_path):
	file_list = FindAll(_path)
	for file_name in file_list:
		route_list = get_routes(file_name)
		class_method_list = get_class_method(file_name)
		import_list = get_import(file_name)
	# with open(PythonLocation()+"/route_list.py", 'w',encoding="utf-8") as json_file:
	# 	for i in route_list:
	# 		json_file.writelines(i)
	# with open(PythonLocation()+"/class_method_list.py", 'w',encoding="utf-8") as json_file:
	# 	for i in class_method_list:
	# 		json_file.writelines(i)

def merge_code():
	list_folder = FindAllInFolder(PythonLocation())
	for i in list_folder:
		if os.path.isdir(i):
			search_merge_content(i)
			merge_content_to_manager(i[i.rfind("/")+1:])

if __name__ == '__main__':
	merge_code()
