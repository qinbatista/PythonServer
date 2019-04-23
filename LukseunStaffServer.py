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
	# target：调用的方法名
	# args：方法中传递的参数
	# name：线程名字
	thread1 = threading.Thread(target=run,name="thread",args=("paramMessage1","paramMessage2"))
	thread1.start()

def run(param1,param2):
	s=socket.socket()
	s.bind(('',port))#server (ipAdress,port)
	s.listen(65535)# 监听最多10个连接请求 (Monitor up to 10 connection requests)
	LogRecorder.LogUtility("[Server][LukseunStaffServer][run]->Server Started")
	while True:
		try:
			# cs include laddr is server and raddr is client
			cs,address = s.accept()# wait client connect # 阻塞等待链接,创建新链接对象（obj)和客户端地址（addr)
			des = EncryptionAlgorithm.DES(DESKey,DESVector)
			ra = cs.recv(36) #先接受消息头
			new = AnalysisHeader.Header(ra)
			print(new.size)
			print(new.Legal)
			print(new.md5)
			IPAdress = str(list(address)[0])
			#status = str("").encode()#WorkingTimeRecoder.StaffCheckIn(ra,IPAdress)#测试服务器连接
			cs.send(str.encode("pass"))# 通过新链接对象发送数据
			sizebuffer = int(new.size)
			reMsg=b""
			while sizebuffer!=0:
				if int(sizebuffer)>2048:
					reMsg =reMsg+ cs.recv(2048)# 返回得到的数据，最多接受2048个字节
					sizebuffer=sizebuffer-2048
				else:
					reMsg=reMsg+cs.recv(sizebuffer)
					sizebuffer = 0
			status = WorkingTimeRecoder.StaffCheckIn(reMsg,IPAdress)#真实测试
			LogRecorder.LogUtility("["+IPAdress+"][LukseunStaffServer][run]->sent encrypted message to client:"+ str(status))
			cs.send(status)
		except socket.error:
			LogRecorder.LogUtility("["+IPAdress+"][LukseunStaffServer][run]->connecting failed, restart")
	cs.close()


if __name__ == '__main__':
	# data = "{\"MacAdress\":\"ACDE48001122\", \"UserName\":\"abc\", \"Random\":\"774\"}"
	# des = EncryptionAlgorithm.DES(DESKey,DESVector)
	# encryptdata = des.encrypt(data.encode('utf-8'))
	# encryptdataString =bytes.decode(encryptdata)
	# print(encryptdataString)
	# encryptdata = str.encode(encryptdataString)
	# print(encryptdata)
	# decryptdata = des.decrypt(encryptdata)
	# print(decryptdata)
	main()