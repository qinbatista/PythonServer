import time
import os
import codecs
import numpy as np
import matplotlib.pyplot as plt
def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
def ErrorRate(TotalProcesses,TotalThread,PortQuantity):
	FailedQuantity=0
	SuccessQuantity=1
	if os.path.isfile(PythonLocation()+"/../WorkingCat/failed"):
		f=open(PythonLocation()+'/../WorkingCat/failed','r')
		FailedQuantity = len(f.readlines())
	if os.path.isfile(PythonLocation()+"/../WorkingCat/Success"):
		f=open(PythonLocation()+'/../WorkingCat/Success','r')
		SuccessQuantity = len(f.readlines())
	print("Failed quantity: "+str(FailedQuantity))
	print("Successed quantity: "+str(SuccessQuantity))
	print("Failed rate:" +str(FailedQuantity/SuccessQuantity))
	if os.path.isfile(PythonLocation()+'/../WorkingCat/ErrorRate')==False:
		f=codecs.open(PythonLocation()+'/../WorkingCat/ErrorRate','w', 'UTF-8')
		f.close()
	f=open(PythonLocation()+'/../WorkingCat/ErrorRate','a')
	f.write(str(TotalProcesses)+","+str(TotalThread)+","+str(PortQuantity)+","+str(FailedQuantity/SuccessQuantity))
	f.write('\n')
	f.close()
def GetErrorRate():
	dataMat = []
	if os.path.isfile(PythonLocation()+'/../WorkingCat/ErrorRate')==False:
		print("[DebugUtility][GetErrorRate]->100% success!")
		return
	fr = open(PythonLocation()+'/../WorkingCat/ErrorRate')
	for line in fr.readlines():
		curLine = line.strip().split(',')
		fltLine = list(map(float,curLine)) #map all elements to float()
		dataMat.append(fltLine)
	myNP = np.array(dataMat)
	ErrorGraph(myNP)
def ErrorGraph(myNp):
	ListPortQuantity=[]
	ListErrorRate=[]
	Line = []
	plt.xlabel('Port Number')
	plt.ylabel('Error Rate')
	for i in range(0,len(myNp)):
		if((i+1)%10==0 and i!=0):
			ListPortQuantity.append(myNp[i][2])
			ListErrorRate.append(myNp[i][3])
			l1 = plt.plot(ListPortQuantity, ListErrorRate,"x-")
			plt.legend(l1, labels = [ str(100*i) for i in range(1,101)],loc = 'best')
			ListPortQuantity.clear()
			ListErrorRate.clear()
		else:
			ListPortQuantity.append(myNp[i][2])
			ListErrorRate.append(myNp[i][3])
	numberList = []
	for i in range(1,len(Line)+1):
		numberList.append("Total:"+str(i*1000))
	plt.show()
if __name__ == "__main__":
	GetErrorRate()