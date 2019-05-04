import sys, os
import os.path
import threading
import socket
from time import ctime
import time
import json
from Utility import LogRecorder,AnalysisHeader,EncryptionAlgorithm
from WorkingCat import WorkingTimeRecoder
port1 = 10001
port2 = 10002
DESKey = "67891234"
DESVector = "6789123467891234"
def main():
	threads = [StartServer(args=((10000 + n, ""))) for n in range(0,10)]
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
				# 接受TCP连接并返回（conn,address）,其中conn是新的套接字对象，可以用来接收和发送数据。address是连接客户端的地址。
				cs,address = s.accept()
				#solve header verification 这个解决头部的验证
				HeaderMessage,IPAdress = self.HeaderSolution(cs,address)
				if HeaderMessage== "":
					LogRecorder.LogUtility("["+IPAdress+"][LukseunStaffServer][runPort1]->Recive illegal data from:"+IPAdress)
					continue
				else:
					LogRecorder.LogUtility("["+IPAdress+"][LukseunStaffServer][runPort1]->Recive App data from:"+IPAdress)#目前没有natasha的相关数据
				#solve message information
				self.MessageSolution(HeaderMessage,cs,IPAdress)
			except socket.error:
				LogRecorder.LogUtility("["+IPAdress+"][LukseunStaffServer][runPort1]->connecting failed, restart")
		cs.close()
	def HeaderSolution(self,cs,address):
		ra = cs.recv(36)#先接受36个字节，这是md5加密字符串 和数据的长度
		HeaderMessage = AnalysisHeader.Header(ra)#初始化
		IPAdress = str(list(address)[0])
		LogRecorder.LogUtility("[Server][LukseunStaffServer][runPort1]->Recived header: "+bytes.decode(ra))
		LogRecorder.LogUtility("[Server][LukseunStaffServer][runPort1]->decrypt header: new.size="+HeaderMessage.size+" new.App="+HeaderMessage.App+" new.md5="+HeaderMessage.md5)
		if HeaderMessage.App=="":
			return "",IPAdress
		en = EncryptionAlgorithm.DES()# 加密初始化
		mytime = "6275e26419211d1f526e674d97110e15"#en.MD5Encrypt(str(time.time())) natasha的md5数据
		cs.send(str.encode(mytime))
		LogRecorder.LogUtility("[Server][LukseunStaffServer][runPort1]->Send header:"+mytime)
		return HeaderMessage,IPAdress
	def ServerHeader(self,header,TestMessage):
		headertool = AnalysisHeader.Header()
		return headertool.MakeHeader(header.App,str(len(TestMessage)))
	def CallBackMsgToClient(self,cs,HeaderMessage,status,IPAdress):
		# 客户端接收到的数据要进行相应的字符串的拆分，才知道软件的名字和后面真实数据的长度是多少
		cs.send(self.ServerHeader(HeaderMessage,status))# 软件名字 给客户端的加密数据--->执行后的结果是 软件名字
		LogRecorder.LogUtility("[Server][LukseunStaffServer][runPort1]->Send callback header: "+ bytes.decode(self.ServerHeader(HeaderMessage,status)))
		rs = cs.recv(32)#接收客户端的反馈
		LogRecorder.LogUtility("[Server][LukseunStaffServer][runPort1]->recv callback header: "+ bytes.decode(rs))
		cs.send(status)# 这次的数据才是真实数据
		LogRecorder.LogUtility("["+IPAdress+"][LukseunStaffServer][runPort1]->sent encrypted message to client:"+ str(status))
	def MessageSolution(self,HeaderMessage,cs,IPAdress):
		sizebuffer = int(HeaderMessage.size)
		reMsg=b""# 用于存放所有的信息
		ReciveBufferSize = 2048
		while sizebuffer!=0:
			if sizebuffer > ReciveBufferSize:# 此条件成立，说明后面还有数据
				reMsg += cs.recv(ReciveBufferSize)# 再拿取1024个字节
				sizebuffer = sizebuffer - ReciveBufferSize# 获取还剩下的字节数
			else:
				reMsg += cs.recv(sizebuffer)# 获取全部的字节
				sizebuffer = 0
		#send result message to client 发送结果到客户端
		if HeaderMessage.App =="workingcat":
			myWTR = WorkingTimeRecoder.WorkingTimeRecoderClass()
			status = myWTR.ResolveMsg(reMsg,IPAdress)#客户端发过来的详细数据，IP地址 解析之后传回来的是服务器发送给客户端加密之后的数据
		if HeaderMessage.App =="natasha":
			myWTR = WorkingTimeRecoder.WorkingTimeRecoderClass()
			status = myWTR.ResolveMsg(reMsg,IPAdress)
		self.CallBackMsgToClient(cs,HeaderMessage, status,IPAdress)

if __name__ == '__main__':
	main()