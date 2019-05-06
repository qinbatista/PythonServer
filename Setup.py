import os
def get_required_packages():
	os.system("pip3 install -r requirements.txt")
	os.system("pip install -r requirements.txt")
	os.system("pip.exe install -r requirements.txt")
if __name__ == "__main__":
	get_required_packages()