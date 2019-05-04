import time
import os
import codecs
import numpy as np
import matplotlib.pyplot as plt
import threading
def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
class DebugUtility():
	def __init__(self):
		self.success_count=0
		self.failed_count=0
	def increase_success_count(self):
		self.success_count = self.success_count+1
	def increase_fail_count(self):
		self.failed_count = self.failed_count+1
	def record_error_rate(self,TotalProcesses,TotalThread,PortQuantity,Probability = None):
		if os.path.isfile(PythonLocation()+'/../WorkingCat/ErrorRate')==False:
			f=codecs.open(PythonLocation()+'/../WorkingCat/ErrorRate','w', 'UTF-8')
			f.close()
		f=open(PythonLocation()+'/../WorkingCat/ErrorRate','a+')
		f.write(str(TotalProcesses)+","+str(TotalThread)+","+str(PortQuantity)+"," + (str(Probability) if Probability else str(0 if self.failed_count==0 else self.failed_count/self.success_count)))
		f.write('\n')
		f.close()
	def port_error_graph(self):
		dataMat = []
		if os.path.isfile(PythonLocation()+'/../WorkingCat/ErrorRate')==False:
			print("[DebugUtility][GetErrorRate]->100% success!")
			return
		fr = open(PythonLocation()+'/../WorkingCat/ErrorRate')
		for line in fr.readlines():
			curLine = line.strip().split(',')
			fltLine = list(map(float,curLine)) #map all elements to float()
			dataMat.append(fltLine)
		myNp = np.array(dataMat)
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
				plt.legend(l1, labels = [ str(100*i) for i in range(1,11)],loc = 'best')
				ListPortQuantity.clear()
				ListErrorRate.clear()
			else:
				ListPortQuantity.append(myNp[i][2])
				ListErrorRate.append(myNp[i][3])
		numberList = []
		for i in range(1,len(Line)+1):
			numberList.append("Total:"+str(i*1000))
		plt.show()
	def port_threading_graph(self):
		"""
		each 100 threading as as port
		"""
		total_port = 10
		dataMat = []
		fr = open(PythonLocation()+'/../WorkingCat/ErrorRate')
		for line in fr.readlines():
			curLine = line.strip().split(',')
			fltLine = list(map(float, curLine))  # map all elements to float()
			dataMat.append(fltLine)
		myNp = np.array(dataMat)
		total_threading = int(len(myNp)/10)
		ListThreadingQuantity = []
		ListErrorRate = []
		Line = []
		plt.xlabel('threading number')
		plt.ylabel('error rate')
		for i in range(0,total_port+1):
			totalthreading = myNp[0][0]*myNp[0][1]
		if(totalthreading % 100 == 0):
			for ten in range(0,total_threading):
				ListThreadingQuantity.append(totalthreading*(ten+1))
			if ten == 0:
				ListErrorRate.append(myNp[ten+i][3])
			else:
				ListErrorRate.append(myNp[ten*10-1+i][3])
		l1 = plt.plot(ListThreadingQuantity, ListErrorRate, "x-")
		plt.legend(l1, labels=[str(1*i)
				for i in range(1, total_port+1)], loc='best')
		ListThreadingQuantity.clear()
		ListErrorRate.clear()
		numberList = []
		for i in range(1, len(Line)+1):
			numberList.append("Total:"+str(i*1000))
		plt.show()
if __name__ == "__main__":
	ts = DebugUtility()
	ts.port_error_graph()
	ts.port_threading_graph()