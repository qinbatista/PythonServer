import time
import os
import codecs
def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
def LogUtility(message):
	print(message) #print message on log
	if os.path.isfile(PythonLocation()+'/../WorkingCat/WorkingTimeRecodderLog')==False:
		f=codecs.open(PythonLocation()+'/../WorkingCat/WorkingTimeRecodderLog','w', 'UTF-8')
		f.write("{}")
		f.close()
	f=open(PythonLocation()+'/../WorkingCat/WorkingTimeRecodderLog','a')
	f.write("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"] "+message)
	f.write('\n')
	f.close()