import sys, os
import threading
import time
import uuid
import socket
sys.path.insert(0,sys.path[0]+"/Utility")
import multiprocessing
import EncryptionAlgorithm
import LogRecorder
import AnalysisHeader
import DebugUtility
import random
"""
发送消息内容为：
mac地址,签到状态,用户名

比如：
ac:de:48:00:11:22,1,覃于澎

总消息长不能超过2048个字节
"""
#host  = 'magicwandai.com' # 这是服务器的电脑的ip
#host  = '155.138.222.30' # 这是服务器的电脑的ip
host = "127.0.0.1"
DESKey = "67891234"
DESVector = "6789123467891234"
def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
class LukseunClient():
	def __init__(self,myHeader,port = 10000,ServerPortNumber=10):
		self.header = myHeader
		self.port = port
		self.ServerPortNumber = ServerPortNumber
	def __get_mac_address(self):
		mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
		return ":".join([mac[e:e+2] for e in range(0,11,2)])
	def __ThreadRunClass(self,TotalProcessesID, msg):
		threadpool = []
		for ThreadID in range(0,self.TotalThread):
			th = threading.Thread(target=self.__run, args=(msg,TotalProcessesID, ThreadID))
			threadpool.append(th)
		for th in threadpool:
			th.start()
		for th in threadpool:
			threading.Thread.join(th)
	def __run(self,msg,TotalProcessesID=1,ThreadID=1):
		Finished=True
		while Finished:
			try:
				# print("ThreadID("+str(ThreadID)+")self.ServerPortNumber("+str(self.ServerPortNumber)+") remainder="+str(ThreadID%self.ServerPortNumber)+" value ="+self.port+ThreadID%self.ServerPortNumber)
				# time.sleep(5)
				Portvalue = self.port+ThreadID%self.ServerPortNumber
				address = (host, Portvalue)
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.settimeout(5)
				s.connect(address)
				TestMessage = msg
				self.__SendHeader(s,TestMessage)
				self.__SendMessage(s,TestMessage)
				s.settimeout(None)
				s.close()
				LogRecorder.LogUtility("[LukseunClient][LogRecorder][run][Port:"+str(Portvalue)+"][Processes:"+str(TotalProcessesID)+"][Thread:"+str(ThreadID)+"]:Successed","success",True,True)
				Finished=False
			except socket.error:
				time.sleep(5)
				LogRecorder.LogUtility("[LukseunClient][LogRecorder][run][Port:"+str(Portvalue)+"][Processes:"+str(TotalProcessesID)+"][Thread:"+str(ThreadID)+"]:connecting error","failed", True,True)
	def __HeaderSolution(self):
		pass
	def __SendHeader(self,s,TestMessage):
		des = EncryptionAlgorithm.DES(DESKey,DESVector)
		TestMessage = des.encrypt(TestMessage)
		LogRecorder.LogUtility("[LukseunClient][LogRecorder][run]->send encrypted header: "+ bytes.decode(TestMessage))
		#send header
		headertool = AnalysisHeader.Header()
		message = headertool.MakeHeader(self.header,str(len(TestMessage)))
		s.send(message)
		data = s.recv(32)
		LogRecorder.LogUtility("[LukseunClient][LogRecorder][run]->recv encrypted header: "+ bytes.decode(data))
		return data
	def __SendMessage(self,s,TestMessage):
		des = EncryptionAlgorithm.DES(DESKey,DESVector)
		TestMessage = des.encrypt(TestMessage)
		sizebuffer = len(TestMessage)
		while sizebuffer!=0:
			if int(sizebuffer)>2048:
				data =data+ s.send(TestMessage[0:2048])
				TestMessage = TestMessage[2048:]
				sizebuffer=sizebuffer-2048
			else:
				s.send(TestMessage)
				sizebuffer = 0
		LogRecorder.LogUtility("[LukseunClient][LogRecorder][run]->send encrypted msg: "+ bytes.decode(TestMessage))
		data = s.recv(36)
		LogRecorder.LogUtility("[LukseunClient][LogRecorder][run]->recv encrypted data: "+ bytes.decode(data))
		headertool = AnalysisHeader.Header(data)
		sizebuffer = int(headertool.size)
		reMsg=b""
		en = EncryptionAlgorithm.DES()
		mytime = en.MD5Encrypt(str(time.time()))
		s.send(str.encode(mytime))
		LogRecorder.LogUtility("[LukseunClient][LogRecorder][run]->send encrypted data: "+ str(mytime))
		ReciveBufferSize = 1024
		while sizebuffer!=0:
			if int(sizebuffer)>ReciveBufferSize:
				reMsg =reMsg+ s.recv(ReciveBufferSize)
				sizebuffer=sizebuffer-ReciveBufferSize
			else:
				reMsg=reMsg+s.recv(sizebuffer)
				sizebuffer = 0
		des = EncryptionAlgorithm.DES(DESKey,DESVector)
		LogRecorder.LogUtility("[LukseunClient][LogRecorder][run]->recived encrypted message: "+str(reMsg))
		DesMessage = des.decrypt(reMsg)
		LogRecorder.LogUtility("[LukseunClient][LogRecorder][run]-> decrypted message: "+str(DesMessage))
		return DesMessage
	def __MessageConstruction(self):
		pass
	"""
	⬆️above codes are private method
	"""
	def SendMsg(self,msg):
		self.__run(msg)
	def Test_MultMessage(self,msg,TotalProcesses=1,TotalThread=1000):
		self.TotalProcesses = TotalProcesses
		self.TotalThread = TotalThread
		print("[LukseunStaffClient][Test_MultMessage]->TotalProcesses="+str(TotalProcesses)+"  TotalThread="+str(TotalThread))
		start = time.time()
		pool = multiprocessing.Pool(processes=self.TotalProcesses)
		for i in range(self.TotalProcesses):
			pool.apply_async(self.__ThreadRunClass(i, msg))
		pool.close()
		pool.join()
		end = time.time()
		print("Total time：" + str(end - start))
	def DownloadData(self):
		pass
	def UploadData(self):
		pass
	"""
	⬆️above codes are public method
	"""
def DelCache():
	if os.path.isfile(PythonLocation()+"/WorkingCat/failed"):
		os.remove(PythonLocation()+"/WorkingCat/failed")
	if os.path.isfile(PythonLocation()+"/WorkingCat/success"):
		os.remove(PythonLocation()+"/WorkingCat/success")
	if os.path.isfile(PythonLocation()+"/WorkingCat/ErrorRate"):
		os.remove(PythonLocation()+"/WorkingCat/ErrorRate")
if __name__ == '__main__':
	DelCache()
	ct = LukseunClient("workingcat",ServerPortNumber=3)
	ct.SendMsg("{\"session\":\"ACDE48001122\", \"Function\":\"CheckTime\",\"UserName\":\"abc\", \"Random\":\"774\"}")
	# ct.Test_MultMessage("{\"MacAddress\":\"ACDE48001122\", \"Function\":\"CheckIn\",\"UserName\":\"abc\", \"Random\":\"774\"}",1,100)
	#ProcessNumber = 100
	# for ProccIncreaseIndex in range(1,101):
	# 	for PortIncreaseIndex in range(1,11):
	# 		ct = LukseunClient("workingcat",ServerPortNumber=PortIncreaseIndex)
	# 		ct.Test_MultMessage("{\"UserID\":\"ACDE48001122\", \"Function\":\"CheckIn\",\"UserName\":\"abc\", \"Random\":\"774\"}",1,ProcessNumber*ProccIncreaseIndex)
	# 		DebugUtility.ErrorRate(1,ProcessNumber*ProccIncreaseIndex,PortIncreaseIndex)
	# DebugUtility.GetErrorRate()


