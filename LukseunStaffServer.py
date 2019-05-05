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
HEADER_BUFFER_SIZE = 36
def main():
	threads = [StartServer(args=((10000 + n, ""))) for n in range(0,10)]
	for t in threads:
		t.start()
	for t in threads:
		t.join()

class StartServer(threading.Thread):
	def run(self):
		"""
		create a port to get message from client
		"""
		s=socket.socket()
		s.bind(('',self._args[0]))
		s.listen(65535)
		LogRecorder.LogUtility("[Server][LukseunStaffServer][run][]->Server Started, Port:"+str(self._args[0]))
		while True:
			try:
				cs,address = s.accept()
				if self.__get_all_message(cs,address):# 处理消息内容
					LogRecorder.LogUtility("["+str(list(address)[0])+"][LukseunStaffServer][runPort1]->Recive App data from:"+str(list(address)[0]))#目前没有natasha的相关数据
				else:
					LogRecorder.LogUtility("["+str(list(address)[0])+"][LukseunStaffServer][runPort1]->Recive illegal data from:"+str(list(address)[0]))
			except socket.error:
				LogRecorder.LogUtility("["+address+"][LukseunStaffServer][runPort1]->connecting failed, restart")
		cs.close()

	def __get_all_message(self,cs,address):
		"""
		handle one client message
		"""
		header_message,ip_address = self.__get_header(cs,address)
		if header_message=="":
			return False
		status = self.__get_message(header_message,cs,ip_address)
		self.__send_callback(cs,header_message,status,ip_address)
		return True

	def __get_header(self,cs,address):
		"""
		solve header, if header is illegal, return null string
		"""
		ra = cs.recv(HEADER_BUFFER_SIZE)#先接受36个字节，这是md5加密字符串 和数据的长度
		if ra=="":
			return "",""
		header_message = AnalysisHeader.Header(ra)#初始化
		ip_address = str(list(address)[0])
		LogRecorder.LogUtility("[Server][LukseunStaffServer][runPort1]->decrypt header: new.size=" + header_message.size + " new.App="+header_message.App+" new.md5="+header_message.md5)
		if header_message.App == "":
			return "",ip_address
		return header_message,ip_address

	def __get_message(self,header_message,cs,ip_address):
		"""
		solve main message
		"""
		sizebuffer = int(header_message.size)
		reMsg=b""# 用于存放客户端发上来的详细信息
		ReciveBufferSize = 2048
		while sizebuffer != 0:
			if sizebuffer > ReciveBufferSize:# 此条件成立，说明后面还有数据
				reMsg += cs.recv(ReciveBufferSize)# 再拿取2048个字节
				sizebuffer = sizebuffer - ReciveBufferSize# 获取还剩下的字节数
			else:
				reMsg += cs.recv(sizebuffer)# 获取全部的字节
				sizebuffer = 0
		return self.__app_solution(header_message,reMsg,ip_address)

	def __send_callback(self,cs,header_message,status,ip_address):
		"""
		send callback message to clent
		"""
		headertool = AnalysisHeader.Header()
		header_message = headertool.MakeHeader(header_message.App,str(len(status)))
		cs.send(header_message+status)
		LogRecorder.LogUtility("[Server][LukseunStaffServer][runPort1]->Send callback header: "+bytes.decode(header_message))
		LogRecorder.LogUtility("["+ip_address+"][LukseunStaffServer][runPort1]->sent encrypted message to client:"+ str(status))

	def __app_solution(self,header_message,reMsg,ip_address):
		"""
		solve different application data and send status back
		"""
		if header_message.App =="workingcat":
			myWTR = WorkingTimeRecoder.WorkingTimeRecoderClass()
			status = myWTR.ResolveMsg(reMsg, ip_address)#客户端发过来的详细数据，IP地址 ---> 服务器发送给客户端的加密之后的数据
		if header_message.App =="natasha":
			myWTR = WorkingTimeRecoder.WorkingTimeRecoderClass()
			status = myWTR.ResolveMsg(reMsg,ip_address)
		return status

if __name__ == '__main__':
	main()