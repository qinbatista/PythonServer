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
port1 = 10001
port2 = 10002
DESKey = "67891234"
DESVector = "6789123467891234"
def main():
	threads = [StartServer(args=((10000+n,""))) for n in range(0,10)]
	for t in threads:
		t.start()
	for t in threads:
	 	t.join()
	# thread1 = threading.Thread(target=runPort1,name="thread",args=("paramMessage1","paramMessage2"))
	# thread1.start()
	# thread2 = threading.Thread(target=runPort2,name="thread",args=("paramMessage1","paramMessage2"))
	# thread2.start()

class StartServer(threading.Thread):
	def run(self):
		s=socket.socket()
		s.bind(('',self._args[0]))
		s.listen(65535)
		LogRecorder.LogUtility("[Server][LukseunStaffServer][run][]->Server Started, Port:"+str(self._args[0]))
		while True:
			try:
				cs,address = s.accept()
				#solve header verification
				HeaderMessage,IPAdress = self.HeaderSolution(cs,address)
				if HeaderMessage == "":
					LogRecorder.LogUtility("["+IPAdress+"][LukseunStaffServer][runPort1]->Recive illegal data from:"+IPAdress)
					continue
				else:
					LogRecorder.LogUtility("["+IPAdress+"][LukseunStaffServer][runPort1]->Recive legal data from:"+IPAdress)
				#solve message information
				self.MessageSolution(HeaderMessage,cs,IPAdress)
			except socket.error:
				LogRecorder.LogUtility("["+IPAdress+"][LukseunStaffServer][runPort1]->connecting failed, restart")
		cs.close()
	def HeaderSolution(self,cs,address):
		ra = cs.recv(36)
		HeaderMessage = AnalysisHeader.Header(ra)
		IPAdress = str(list(address)[0])
		LogRecorder.LogUtility("[Server][LukseunStaffServer][runPort1]->Recived header: "+bytes.decode(ra))
		LogRecorder.LogUtility("[Server][LukseunStaffServer][runPort1]->decrypt header: new.size="+HeaderMessage.size+" new.Legal="+HeaderMessage.Legal+" new.md5="+HeaderMessage.md5)
		if HeaderMessage.Legal=="":
			return "",IPAdress
		cs.send(str.encode(HeaderMessage.md5))
		LogRecorder.LogUtility("[Server][LukseunStaffServer][runPort1]->IPAdress="+IPAdress+" pass")
		return HeaderMessage,IPAdress

	def MessageSolution(self,HeaderMessage,cs,IPAdress):
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
			myWTR = WorkingTimeRecoder.WorkingTimeRecoderClass()
			status = myWTR.ResolveMsg(reMsg,IPAdress)
		if HeaderMessage.Legal =="natasha":
			myWTR = WorkingTimeRecoder.WorkingTimeRecoderClass()
			status = myWTR.ResolveMsg(reMsg,IPAdress)
		LogRecorder.LogUtility("["+IPAdress+"][LukseunStaffServer][runPort1]->sent encrypted message to client:"+ str(status))
		cs.send(status)




if __name__ == '__main__':
	main()