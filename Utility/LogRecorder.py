import time
def LogUtility(message):
	print(message) #print message on log
	f=open('WorkingTimeRecodderLog','a')
	f.write("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"] "+message)
	f.write('\n')
	f.close()