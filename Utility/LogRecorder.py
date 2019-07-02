import time
import os
import codecs
import threading


def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))


def LogUtility(message, fileName="WorkingTimeRecoderLog", printLog=True, RecordLog=False):
	mutex = threading.Lock()
	mutex.acquire()
	if printLog:
		print(message)  # print message on log
	if RecordLog:
		if not os.path.isfile(PythonLocation() + '/../WorkingCat/' + fileName + ''):
			f = codecs.open(PythonLocation() + '/../WorkingCat/' + fileName + '', 'w', 'UTF-8')
			f.close()
		f = open(PythonLocation() + '/../WorkingCat/' + fileName + '', 'a')
		f.write("[" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "] " + message)
		f.write('\n')
		f.close()
	mutex.release()
