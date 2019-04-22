import time
import os
import codecs
def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
def LogUtility(message, fileName = "WorkingTimeRecodderLog",printLog = True, RecordLog = True):
	if printLog==True:
		print(message) #print message on log
	if RecordLog == True:
		if os.path.isfile(PythonLocation()+'/../WorkingCat/'+fileName+'')==False:
			f=codecs.open(PythonLocation()+'/../WorkingCat/'+fileName+'','w', 'UTF-8')
			f.close()
		f=open(PythonLocation()+'/../WorkingCat/'+fileName+'','a')
		f.write("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"] "+message)
		f.write('\n')
		f.close()