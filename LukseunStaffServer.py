import sys, os
import os.path
import threading
import socket
from time import ctime
import time
import json
import Utility.LogRecorder
from Utility import LogRecorder
from  WorkingCat import WorkingTimeRecoder
from Utility import AnalysisHeader
from Utility import EncryptionAlgorithm
port = 2002
DESKey = "67891234"
DESVector = "6789123467891234"
def main():
	thread1 = threading.Thread(target=run,name="thread",args=("paramMessage1","paramMessage2"))
	thread1.start()

def HeaderSolution(cs,address):
	ra = cs.recv(36) #先接受消息头
	HeaderMessage = AnalysisHeader.Header(ra)
	IPAdress = str(list(address)[0])
	LogRecorder.LogUtility("[Server][LukseunStaffServer][run]->Recived header: "+bytes.decode(ra))
	LogRecorder.LogUtility("[Server][LukseunStaffServer][run]->decrypt header: new.size="+HeaderMessage.size+" new.Legal="+HeaderMessage.Legal+" new.md5="+HeaderMessage.md5)
	if HeaderMessage.Legal=="":
		return "",IPAdress
	cs.send(str.encode(HeaderMessage.md5))# 通过新链接对象发送数据
	LogRecorder.LogUtility("[Server][LukseunStaffServer][run]->IPAdress="+IPAdress+" pass")
	return HeaderMessage,IPAdress

def MessageSolution(HeaderMessage,cs,IPAdress):
	sizebuffer = int(HeaderMessage.size)
	reMsg=b""
	ReciveBufferSize = 1024
	while sizebuffer!=0:
		if int(sizebuffer)>ReciveBufferSize:
			reMsg =reMsg+ cs.recv(ReciveBufferSize)
			sizebuffer=sizebuffer-ReciveBufferSize
		else:
			reMsg=reMsg+cs.recv(sizebuffer)
			sizebuffer = 0
	#send result message to client
	if HeaderMessage.Legal =="workingcat":
		status = WorkingTimeRecoder.StaffCheckIn(reMsg,IPAdress)
	LogRecorder.LogUtility("["+IPAdress+"][LukseunStaffServer][run]->sent encrypted message to client:"+ str(status))
	cs.send(status)

def run(param1,param2):
	s=socket.socket()
	s.bind(('',port))
	s.listen(65535)
	LogRecorder.LogUtility("[Server][LukseunStaffServer][run]->Server Started")
	while True:
		try:
			cs,address = s.accept()
			#solve header verification
			HeaderMessage,IPAdress = HeaderSolution(cs,address)
			if HeaderMessage == "":
				LogRecorder.LogUtility("["+IPAdress+"][LukseunStaffServer][run]->Recive illegal data from:"+IPAdress)
				continue
			else:
				LogRecorder.LogUtility("["+IPAdress+"][LukseunStaffServer][run]->Recive legal data from:"+IPAdress)
			#solve message information
			MessageSolution(HeaderMessage,cs,IPAdress)
		except socket.error:
			LogRecorder.LogUtility("["+IPAdress+"][LukseunStaffServer][run]->connecting failed, restart")
	cs.close()


if __name__ == '__main__':
	main()