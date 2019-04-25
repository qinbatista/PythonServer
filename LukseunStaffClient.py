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
TotalProcesses = 1
TotalThread = 1000
PortQuantity = 1
def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
class LukseunClient():
	def __init__(self,myHeader, myMessage,myPort):
		self.header = myHeader
		self.msg = myMessage
		self.port = myPort
	def get_mac_address(self):
		mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
		return ":".join([mac[e:e+2] for e in range(0,11,2)])
	def SingalMessage(self):
		self.run("1","1")
	def MultMessage(self):
		start = time.time()
		pool = multiprocessing.Pool(processes=TotalProcesses)
		for i in range(TotalProcesses):
			pool.apply_async(self.ThreadRunClass, (i, ""))
		pool.close()
		pool.join()
		end = time.time()
		print("Total time：" + str(end - start))
	def ThreadRunClass(self,p1, p2):
		threadpool = []
		for num in range(0,TotalThread):
			th = threading.Thread(target=self.run, args=(p1, num))
			threadpool.append(th)
		for th in threadpool:
			th.start()
		for th in threadpool:
			threading.Thread.join(th)
	def run(self,param1,param2):
		Finished=True
		while Finished:
			try:
				address = (host, self.port)
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.settimeout(10)
				s.connect(address)
				TestMessage = self.msg
				data = self.SendHeader(s,TestMessage)
				self.SendMessage(s,TestMessage)
				s.settimeout(None)
				s.close()
				LogRecorder.LogUtility("[LukseunClient][LogRecorder][run][Processes"+str(param1)+"]->[Thread"+str(param2)+"]:Successed","success",True,True)
				Finished=False
			except socket.error:
				s.close()
				time.sleep(5)
				print(s)
				LogRecorder.LogUtility("[LukseunClient][LogRecorder][run]->Thread["+str(param2)+"]:connecting error:"+str(self.port),"failed", True,True)
	def HeaderSolution(self):
		pass
	def SendHeader(self,s,TestMessage):
		des = EncryptionAlgorithm.DES(DESKey,DESVector)
		TestMessage = des.encrypt(TestMessage)
		LogRecorder.LogUtility("[LukseunClient][LogRecorder][run]->send encrypted message: "+ bytes.decode(TestMessage))
		#send header
		headertool = AnalysisHeader.Header()
		message = headertool.MakeHeader(self.header,str(len(TestMessage)))
		s.send(message)
		data = s.recv(32)
		return data
	def SendMessage(self,s,TestMessage):
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
		data = s.recv(1024)
		LogRecorder.LogUtility("[LukseunClient][LogRecorder][run]->recived encrypted message: "+str(data))
		des = EncryptionAlgorithm.DES(DESKey,DESVector)
		byteData = des.decrypt(data)
		LogRecorder.LogUtility("[LukseunClient][LogRecorder][run]-> decrypted message: "+str(byteData))
def main():
	global PortQuantity
	global TotalThread
	threads = [PressureTest(args=((10000+n,""))) for n in range(0,PortQuantity)]
	for t in threads:
		t.start()
	for t in threads:
	 	t.join()
	DebugUtility.ErrorRate(TotalProcesses,TotalThread,PortQuantity)
class PressureTest(threading.Thread):
	def run(self):
		ct = LukseunClient("workingcat","{\"MacAddress\":\"ACDE48001122\", \"Function\":\"CheckIn\",\"UserName\":\"abc\", \"Random\":\"774\"}",self._args[0])
		#ct.SingalMessage()
		ct.MultMessage()
		LogRecorder.LogUtility("[LukseunClient][LogRecorder][run]->finished port1:"+str(self._args[0]))
def AdaptationTest():
	global TotalThread
	global PortQuantity
	totalthreadNum = TotalThread
	for i in range(1,11):
		count = totalthreadNum*i
		PortQuantity=1
		for n in range(PortQuantity,11):
			TotalThread = int(count/n)
			PortQuantity = n
			print(TotalThread)
			print(PortQuantity)
			main()
if __name__ == '__main__':
	#print(PythonLocation())
	if os.path.isfile(PythonLocation()+"/WorkingCat/failed"):
		os.remove(PythonLocation()+"/WorkingCat/failed")
	if os.path.isfile(PythonLocation()+"/WorkingCat/success"):
		os.remove(PythonLocation()+"/WorkingCat/success")
	if os.path.isfile(PythonLocation()+"/WorkingCat/ErrorRate"):
		os.remove(PythonLocation()+"/WorkingCat/ErrorRate")
	AdaptationTest()
	DebugUtility.GetErrorRate()
	#main()


