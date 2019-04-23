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
"""
发送消息内容为：
mac地址,签到状态,用户名

比如：
ac:de:48:00:11:22,1,覃于澎

总消息长不能超过2048个字节
"""
#host  = 'magicwandai.com' # 这是服务器的电脑的ip
#host  = '155.138.222.30' # 这是服务器的电脑的ip
host = "192.168.1.183"
port = 2002 #接口选择大于10000的，避免冲突
DESKey = "67891234"
DESVector = "6789123467891234"
TotalProcesses = 100
TotalThread = 100
def main():
	thread1 = threading.Thread(target=run,name="ThreadClient",args=("123","123"))
	thread1.start()
def get_mac_address():
	mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
	return ":".join([mac[e:e+2] for e in range(0,11,2)])
def ThreadRunClass(p1, p2):
	threadpool = []
	for num in range(0,TotalThread):
		th = threading.Thread(target=run, args=(run, num))
		threadpool.append(th)
	for th in threadpool:
		th.start()
	for th in threadpool:
		threading.Thread.join(th)
def run(param1,param2):
	Finished=True
	while Finished:
		try:
			address = (host, port)
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(10)
			s.connect(address)
			des = EncryptionAlgorithm.DES(DESKey,DESVector)
			TestMessage = "{\"MacAddress\":\"ACDE48001122\", \"UserName\":\"abc\", \"Random\":\"774\"}"
			TestMessage = des.encrypt(TestMessage)
			LogRecorder.LogUtility("["+str(param2)+"][LogRecorder][run]->send encrypted message: "+ bytes.decode(TestMessage))
			#send header
			headertool = AnalysisHeader.Header()
			message = headertool.MakeHeader("natasha",str(len(TestMessage)))
			s.send(message)
			data = s.recv(4)
			
			#send really message
			#s.send(des.encrypt(mssage.encode(encoding="utf-8")))
			#data = s.recv(2048)
			sizebuffer = len(TestMessage)
			while sizebuffer!=0:
				if int(sizebuffer)>2048:
					data =data+ s.send(TestMessage[0:2048])# 返回得到的数据，最多接受2048个字节
					TestMessage = TestMessage[2048:]
					sizebuffer=sizebuffer-2048
				else:
					s.send(TestMessage)
					sizebuffer = 0
			data = s.recv(1024)
			LogRecorder.LogUtility("["+str(param2)+"][LogRecorder][run]->recived encrypted message: "+str(data))
			byteData = des.decrypt(data)
			LogRecorder.LogUtility("["+str(param2)+"][LogRecorder][run]-> decrypted message: "+str(byteData))
			s.settimeout(None)
			s.close()
			LogRecorder.LogUtility("["+str(param2)+"][LogRecorder][run]->Thread["+str(param2)+"]:Successed","test",True)
			Finished=False
		except socket.error:
			s.close()
			time.sleep(5)
			LogRecorder.LogUtility("["+str(param2)+"][LogRecorder][run]->Thread["+str(param2)+"]:connecting error")
def ConnectingRequest(param1,param2):
	pass
def SingalMessage():
	run("","")
def MultMessage():
	start = time.time()
	pool = multiprocessing.Pool(processes=TotalProcesses)
	for i in range(TotalProcesses):
		pool.apply_async(ThreadRunClass, (i, i))
	pool.close()
	pool.join()
	end = time.time()
	print("Total time：" + str(end - start))
if __name__ == '__main__':
	SingalMessage()
	#MultMessage()
