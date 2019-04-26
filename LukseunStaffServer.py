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
					LogRecorder.LogUtility("["+IPAdress+"][LukseunStaffServer][runPort1]->Recive App data from:"+IPAdress)
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
		LogRecorder.LogUtility("[Server][LukseunStaffServer][runPort1]->decrypt header: new.size="+HeaderMessage.size+" new.App="+HeaderMessage.App+" new.md5="+HeaderMessage.md5)
		if HeaderMessage.App=="":
			return "",IPAdress
		cs.send(str.encode(HeaderMessage.md5))
		LogRecorder.LogUtility("[Server][LukseunStaffServer][runPort1]->Send header: "+HeaderMessage.md5)
		return HeaderMessage,IPAdress
	def ServerHeader(self,header,TestMessage):
		headertool = AnalysisHeader.Header()
		return headertool.MakeHeader(header.App,str(len(TestMessage)))
	def CallBackMsgToClient(self,cs,HeaderMessage,status,IPAdress):
		cs.send(self.ServerHeader(HeaderMessage,status))
		LogRecorder.LogUtility("[Server][LukseunStaffServer][runPort1]->Send callback header: "+ bytes.decode(self.ServerHeader(HeaderMessage,status)))
		rs= cs.recv(32)
		LogRecorder.LogUtility("[Server][LukseunStaffServer][runPort1]->recv callback header: "+ bytes.decode(rs))
		cs.send(status)
		LogRecorder.LogUtility("["+IPAdress+"][LukseunStaffServer][runPort1]->sent encrypted message to client:"+ str(status))
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
		if HeaderMessage.App =="workingcat":
			myWTR = WorkingTimeRecoder.WorkingTimeRecoderClass()
			status = myWTR.ResolveMsg(reMsg,IPAdress)
		if HeaderMessage.App =="natasha":
			myWTR = WorkingTimeRecoder.WorkingTimeRecoderClass()
			status = myWTR.ResolveMsg(reMsg,IPAdress)
		self.CallBackMsgToClient(cs,HeaderMessage, status,IPAdress)

if __name__ == '__main__':
	main()