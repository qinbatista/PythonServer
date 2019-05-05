import sys, os
import os.path
import threading
import socket
from time import ctime
import time
import json
from Utility import LogRecorder,AnalysisHeader,EncryptionAlgorithm
from WorkingCat import WorkingTimeRecoder

DESKey = "67891234"
DESVector = "6789123467891234"
def main():
	threads = [StartServer(args=((10000 + n, ""))) for n in range(0,10)]
	for t in threads:
		t.start()
	for t in threads:
		t.join()

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
				if self.__get_all_message(cs,address):
					LogRecorder.LogUtility("["+str(list(address)[0])+"][LukseunStaffServer][runPort1]->Recive App data from:"+str(list(address)[0]))#目前没有natasha的相关数据
				else:
					LogRecorder.LogUtility("["+str(list(address)[0])+"][LukseunStaffServer][runPort1]->Recive illegal data from:"+str(list(address)[0]))
					continue
			except socket.error:
				LogRecorder.LogUtility("["+address+"][LukseunStaffServer][runPort1]->connecting failed, restart")
		cs.close()

	def __get_all_message(self,cs,address):
		HeaderMessage,IPAdress = self.__get_header(cs,address)
		if HeaderMessage=="":
			return False
		status = self.__get_message(HeaderMessage,cs,IPAdress)
		self.__send_callback(cs,HeaderMessage,status,IPAdress)
		return True
	def __get_header(self,cs,address):
		# **** 1 第一次接收客户端发上来的数据，此信息内容包含：1.软件名字  2.消息体的长度 ****
		ra = cs.recv(36)#先接受36个字节，这是md5加密字符串 和数据的长度
		HeaderMessage = AnalysisHeader.Header(ra)#初始化
		IPAdress = str(list(address)[0])
		LogRecorder.LogUtility("[Server][LukseunStaffServer][runPort1]->Recived header: " + bytes.decode(ra))
		LogRecorder.LogUtility("[Server][LukseunStaffServer][runPort1]->decrypt header: new.size=" + HeaderMessage.size + " new.App="+HeaderMessage.App+" new.md5="+HeaderMessage.md5)
		if HeaderMessage.App == "":
			return "",IPAdress
		mytime = "6275e26419211d1f526e674d97110e15"# 这个字符串只需要保证是32位就没问题
		# # **** 2 第一次向客户端发送数据，此信息内容作废，这次发送的目的是：通知客户端我已经接收到了消息，请求发送消息体 ****
		# cs.send(str.encode(mytime)) #[qin]client will send all the message, so don't need to send recive success message back
		LogRecorder.LogUtility("[Server][LukseunStaffServer][runPort1]->Send header:"+mytime)
		return HeaderMessage,IPAdress

	def __get_message(self,HeaderMessage,cs,IPAdress):
		sizebuffer = int(HeaderMessage.size)
		reMsg=b""# 用于存放客户端发上来的详细信息
		ReciveBufferSize = 2048
		# **** 3 第二次接收客户端发送的消息，此信息内容包含：完整的消息体，但使用了des加密 ****
		while sizebuffer != 0:
			if sizebuffer > ReciveBufferSize:# 此条件成立，说明后面还有数据
				reMsg += cs.recv(ReciveBufferSize)# 再拿取2048个字节
				sizebuffer = sizebuffer - ReciveBufferSize# 获取还剩下的字节数
			else:
				reMsg += cs.recv(sizebuffer)# 获取全部的字节
				sizebuffer = 0
		#send result message to client 发送结果到客户端
		if HeaderMessage.App =="workingcat":
			myWTR = WorkingTimeRecoder.WorkingTimeRecoderClass()
			status = myWTR.ResolveMsg(reMsg, IPAdress)#客户端发过来的详细数据，IP地址 ---> 服务器发送给客户端的加密之后的数据
		if HeaderMessage.App =="natasha":
			myWTR = WorkingTimeRecoder.WorkingTimeRecoderClass()
			status = myWTR.ResolveMsg(reMsg,IPAdress)
		return status

	def __send_callback(self,cs,HeaderMessage,status,IPAdress):
		# **** 4 第二次发送消息给客户端，此信息内容包含：1.软件名字   2.消息体的长度 ****
		header_message = self.ServerHeader(HeaderMessage, status)
		headertool = AnalysisHeader.Header()
		header_message = headertool.MakeHeader(HeaderMessage.App,str(len(status)))
		cs.send(header_message+status)# send header and message
		LogRecorder.LogUtility("[Server][LukseunStaffServer][runPort1]->Send callback header: "+bytes.decode(header_message))
		# # **** 5 第三次接收客户端发送的消息，此信息内容作废，这次接收的目的是：知道客户端已经接收到了消息体的长度，要求服务器发送消息体 ****
		# rs = cs.recv(32) [qin] server send all message to client, don't need recv callback from client
		# LogRecorder.LogUtility("[Server][LukseunStaffServer][runPort1]->recv callback header: "+ bytes.decode(rs))#这里输出的是没用的数据
		# 这是一次性发出数据，这里后面过了2048个字节会出现问题，目前可以不纠结
		# **** 6 第三次发送消息给客户端，此信息内容包含：详细的消息体 ****
		#cs.send(status)# 这次的数据才是真实数据
		LogRecorder.LogUtility("["+IPAdress+"][LukseunStaffServer][runPort1]->sent encrypted message to client:"+ str(status))

	def CallBackMsgToClient(self,cs,HeaderMessage,status,IPAdress):
		# **** 4 第二次发送消息给客户端，此信息内容包含：1.软件名字   2.消息体的长度 ****
		header_message = self.ServerHeader(HeaderMessage, status)
		cs.send(header_message+status)# send header and message
		LogRecorder.LogUtility("[Server][LukseunStaffServer][runPort1]->Send callback header: "+bytes.decode(header_message))
		# # **** 5 第三次接收客户端发送的消息，此信息内容作废，这次接收的目的是：知道客户端已经接收到了消息体的长度，要求服务器发送消息体 ****
		# rs = cs.recv(32) [qin] server send all message to client, don't need recv callback from client
		# LogRecorder.LogUtility("[Server][LukseunStaffServer][runPort1]->recv callback header: "+ bytes.decode(rs))#这里输出的是没用的数据
		# 这是一次性发出数据，这里后面过了2048个字节会出现问题，目前可以不纠结
		# **** 6 第三次发送消息给客户端，此信息内容包含：详细的消息体 ****
		#cs.send(status)# 这次的数据才是真实数据
		LogRecorder.LogUtility("["+IPAdress+"][LukseunStaffServer][runPort1]->sent encrypted message to client:"+ str(status))

if __name__ == '__main__':
	main()