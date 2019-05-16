import sys
import os
import threading
import time
import uuid
import socket
# sys.path.insert(0,sys.path[0]+"/Utility")
# sys.path.append(sys.path[0]+"/Utility")
import multiprocessing
from Utility import LogRecorder,DebugUtility,EncryptionAlgorithm,AnalysisHeader
import random
"""
发送消息内容为：
mac地址,签到状态,用户名

比如：
ac:de:48:00:11:22,1,覃于澎

总消息长不能超过2048个字节
"""
# host  = 'magicwandai.com' # 这是服务器的电脑的ip
# host  = '155.138.222.30' # 这是服务器的电脑的ip
host = "127.0.0.1"
DESKey = "67891234"
DESVector = "6789123467891234"
HeaderBufferSize = 36

def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))


class LukseunClient():
	def __init__(self, myHeader, port=8887, port_number=10):  # 软件名字，端口号，服务器端口号
		self.header = myHeader
		self.port = port
		self.port_number = port_number
		self.debug_utility = DebugUtility.DebugUtility()

	def __get_mac_address(self):
		mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
		return ":".join([mac[e:e+2] for e in range(0, 11, 2)])

	def __send_tcp_message(self, msg, TotalProcessesID, ThreadID):# 信息、进程、线程（Information, process, thread）
		"""
		send tcp message to server
		"""
		Finished = True
		while Finished:
			s = None
			DesMessage = ""
			try:
				LogRecorder.LogUtility("[LukseunClient][LogRecorder][run] port = "+str(self.port + ThreadID % self.port_number))
				Portvalue = 8888#self.port + ThreadID % self.port_number#端口号 10003
				address = (host, Portvalue)#ip、端口
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# 创建TCP Socket
				s.settimeout(5)# 设置套接字操作的超时期，超时5秒
				s.connect(address)# 连接到address处的套接字。一般address的格式为元组（hostname,port），如果连接出错，返回socket.error错误。
				callback_message = self.__send_all_message(s, msg)
				s.settimeout(None)
				s.close()
				self.debug_utility.increase_success_count()
				Finished = False
				LogRecorder.LogUtility("[LukseunClient][LogRecorder][run]send success, call back="+str(callback_message))
			except socket.error as e:
				LogRecorder.LogUtility("[LukseunClient][LogRecorder][run]error->"+str(e))
				self.debug_utility.increase_fail_count()
				if s != None:
					s.close()
				time.sleep(1)
			finally:
				if DesMessage != "":Finished = False

	def __send_all_message(self, s, TestMessage):
		"""
		send all message to server and get callback
		"""
		self.__send_header(s, TestMessage)# send header
		callback = self.__send_message(s, TestMessage)# send main message
		return callback

	def __send_header(self, s, TestMessage):
		"""
		send header
		"""
		des = EncryptionAlgorithm.DES(DESKey, DESVector)# 两把钥匙
		TestMessage = des.encrypt(TestMessage)# 加密好的数据
		# send header
		headertool = AnalysisHeader.Header()
		message = headertool.MakeHeader(self.header, str(len(TestMessage)))# 字节长度为36  --->  1，3，5，7是长度
		s.send(message)# 发送数据
		LogRecorder.LogUtility(
			"[LukseunClient][LogRecorder][__send_header]->send encrypted header: " + bytes.decode(message))

	def __send_message(self, s, TestMessage):
		"""
		send message
		"""
		des = EncryptionAlgorithm.DES(DESKey, DESVector)
		TestMessage = des.encrypt(TestMessage)
		sizebuffer = len(TestMessage)
		while sizebuffer != 0:
			if int(sizebuffer) > 2048:
				data = data + s.send(TestMessage[0:2048])
				TestMessage = TestMessage[2048:]
				sizebuffer = sizebuffer-2048
			else:
				s.send(TestMessage)
				sizebuffer = 0
		LogRecorder.LogUtility(
			"[LukseunClient][LogRecorder][__SendMessage]->send encrypted msg: " + bytes.decode(TestMessage))
		data = s.recv(HeaderBufferSize)
		LogRecorder.LogUtility(
			"[LukseunClient][LogRecorder][__SendMessage]->recv encrypted data: " + bytes.decode(data))
		headertool = AnalysisHeader.Header(data)
		sizebuffer = int(headertool.size)
		reMsg = b""
		ReciveBufferSize = 2048
		while sizebuffer != 0:
			if int(sizebuffer) > ReciveBufferSize:
				reMsg += s.recv(ReciveBufferSize)
				sizebuffer = sizebuffer-ReciveBufferSize
			else:
				LogRecorder.LogUtility(
					"[LukseunClient][LogRecorder][__SendMessage]->buffersize:"+str(sizebuffer))
				reMsg += s.recv(sizebuffer)
				sizebuffer = 0
		des = EncryptionAlgorithm.DES(DESKey, DESVector)
		LogRecorder.LogUtility(
			"[LukseunClient][LogRecorder][__SendMessage]->recived encrypted message: "+str(reMsg))
		DesMessage = des.decrypt(reMsg)
		LogRecorder.LogUtility(
			"[LukseunClient][LogRecorder][__SendMessage]-> decrypted message: "+str(DesMessage))
		return DesMessage

	def SendMsg(self, msg, TotalProcessesID=1, ThreadID=1):
		"""
		public method for users
		"""
		self.__send_tcp_message(msg, TotalProcessesID=TotalProcessesID, ThreadID=ThreadID)# 发送tcp数据

	def DownloadData(self):
		pass

	def UploadData(self):
		pass


def __ThreadRunClass(ct, message, ProcessesID, TotalThread):
	threadpool = []
	for ThreadID in range(0, TotalThread):
		th = threading.Thread(target=ct.SendMsg, args=(message, ProcessesID, ThreadID))
		threadpool.append(th)
	for th in threadpool:
		th.start()
	for th in threadpool:
		th.join()
	return ct.debug_utility.failed_count, ct.debug_utility.success_count

def Test_MultMessage(ct, msg, TotalProcesses=1, TotalThread=1000):
	print("[LukseunStaffClient][Test_MultMessage]->TotalProcesses=" +
		str(TotalProcesses)+"  TotalThread="+str(TotalThread))
	time.sleep(1)
	start = time.time()
	pool = multiprocessing.Pool(processes=TotalProcesses)
	pool_list = []
	for i in range(TotalProcesses):
		pool_list.append(pool.apply_async(__ThreadRunClass, (ct, msg, i, TotalThread)))
	pool.close()
	pool.join()
	end = time.time()
	failed_count = 0
	success_count = 0
	for data in pool_list:
		failed_count += int(data.get()[0])
		success_count += int(data.get()[1])
	ct.debug_utility.record_error_rate(TotalProcesses, TotalThread, ct.port_number, 0if failed_count==0 else failed_count/success_count)
	print("Total time：" + str(end - start))

def DelCache():
	if os.path.isfile(PythonLocation()+"/WorkingCat/ErrorRate"):
		os.remove(PythonLocation()+"/WorkingCat/ErrorRate")

def multi_message_test():
	DelCache()  # 存在文件就删除文件
	message_dic = {"session": "ACDE48001122",
		"function": "GetMyAlldata",
		"random": "774",
		"data":
		{
			"user_name": "yupeng",
			"gender": "male",
			"email": "qin@lukseun.com",
			"phone_number": "15310568888"
		}
	}
	ct = LukseunClient("workingcat")# 设置3个端口
	# ct.SendMsg(str(message_dic))# 发送单个数据
	for threading_count in range(100,600,100):# 发送多个数据
		for port_count in range(1,6):
			ct.port_number = port_count
			Test_MultMessage(ct, str(message_dic), 1, threading_count)
def singal_message_test():
	message_dic = {"session": "ACDE48001122",
		"function": "CheckTime",
		"random": "774",
		"data":
		{
			"user_name": "yupeng",
			"gender": "male",
			"email": "qin@lukseun.com",
			"phone_number": "15310568888"
		}
	}
	ct = LukseunClient("workingcat")# 设置3个端口
	ct.SendMsg(str(message_dic))# 发送单个数据

if __name__ == '__main__':
	#singal_message_test()#just send 1 message to server
	multi_message_test()#proccess 1 threading 100-500(increase 100), port 1-5

