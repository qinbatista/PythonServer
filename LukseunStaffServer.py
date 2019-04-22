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
	while True:
		# cs include laddr is server and raddr is client
		cs,address = s.accept()# wait client connect # 阻塞等待链接,创建新链接对象（obj)和客户端地址（addr)
		ra=cs.recv(2048)# 返回得到的数据，最多接受2048个字节
		# message = ra.decode(encoding='utf-8')
		IPAdress = str(list(address)[0])
		status = WorkingTimeRecoder.StaffCheckIn(ra,IPAdress)
		cs.send(status)# 通过新链接对象发送数据
		LogRecorder.LogUtility("["+IPAdress+"][LukseunStaffServer][run]->sent encrypted message to client:"+ str(status))

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