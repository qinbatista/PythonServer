import os
def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
def get_required_packages():
	os.system("pip3 install -r "+PythonLocation()+"/requirements.txt")
	os.system("pip install -r "+PythonLocation()+"/requirements.txt")
	os.system("pip.exe install -r "+PythonLocation()+"/requirements.txt")
if __name__ == "__main__":
	get_required_packages()