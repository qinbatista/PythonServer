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
def get_routes(file_path):
	file_object = open(file_path,encoding="utf-8")
	global routes_code
	all_the_text = file_object.readlines()
	is_find_key=False
	print("finding routes:"+file_path)
	for i in all_the_text:
		if is_find_key == False and i.find("@ROUTES.post")!=-1:
			is_find_key = True
			routes_code.append(i)
		elif is_find_key==True and i.find("__name__")==-1:
			routes_code.append(i)
		elif is_find_key==True and i.find("__name__")!=-1:
			break
	return routes_code

def get_class_method(file_path):
	file_object = open(file_path,encoding="utf-8")
	global class_method_code
	all_the_text = file_object.readlines()
	is_find_key=False
	start_continue=False
	print("finding class method:"+file_path)
	for i in all_the_text:
		print(i.count("\t"))
		if is_find_key == False and i.find("\tasync def")!=-1:
			is_find_key = True
			class_method_code.append(i)
		elif is_find_key==True and i.find("\t")==0:
			if i.find("_execute_statement")!=-1 or i.find("message_typesetting")!=-1:
				start_continue = True
			elif start_continue == True:
				print("["+str(i.find("\t")))
				print("["+str(i.count("\t")))
				if i.find("\t")<=0 and i.count("\t")<=1:
					start_continue=False
					class_method_code.append(i)
				else:
					continue
			else:
				class_method_code.append(i)
		elif is_find_key==True and i.find("\t")!=0 and i != "\n" and i != "\r":
			break
	print(class_method_code)
	return class_method_code
def start_merge(_path):
	file_list = FindAll(_path)
	for file_name in file_list:
		route_list = get_routes(file_name)
		class_method_list = get_class_method(file_name)
	with open(PythonLocation()+"/route_list.py", 'w',encoding="utf-8") as json_file:
		for i in route_list:
			json_file.writelines(i)
	with open(PythonLocation()+"/class_method_list.py", 'w',encoding="utf-8") as json_file:
		for i in class_method_list:
			json_file.writelines(i)
	print(PythonLocation()+"/route_list.py")
	print(PythonLocation()+"/class_method_list.py")
def merge_code():
	list_folder = FindAllInFolder(PythonLocation())
	for i in list_folder:
		if os.path.isdir(i):
			start_merge(i)

if __name__ == '__main__':
	merge_code()
