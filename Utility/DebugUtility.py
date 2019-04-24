import time
import os
import codecs
def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
def ErrorRate():
	if os.path.isfile(PythonLocation()+"/../WorkingCat/failed"):
		f=open(PythonLocation()+'/../WorkingCat/failed','r')
		FailedQuantity = len(f.readlines())
	if os.path.isfile(PythonLocation()+"/../WorkingCat/Success"):
		f=open(PythonLocation()+'/../WorkingCat/Success','r')
		SuccessQuantity = len(f.readlines())
	print("Failed quantity: "+str(FailedQuantity))
	print("Successed quantity: "+str(SuccessQuantity))
	print("Failed rate:" +str(FailedQuantity/SuccessQuantity))
if __name__ == "__main__":
	ErrorRate()
