import sys, os
import threading
import time
import uuid
import socket
sys.path.insert(0,sys.path[0]+"/Utility")
import EncryptionAlgorithm
import LogRecorder
"""
发送消息内容为：
mac地址,签到状态,用户名

比如：
ac:de:48:00:11:22,1,覃于澎

总消息长不能超过2048个字节
"""
#host  = 'magicwandai.com' # 这是服务器的电脑的ip
host  = '192.168.1.183' # 这是服务器的电脑的ip
port = 2002 #接口选择大于10000的，避免冲突
DESKey = "67891234"
DESVector = "6789123467891234"
def main():
	thread1 = threading.Thread(target=run,name="ThreadClient",args=("123","123"))
	thread1.start()
def get_mac_address():
	mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
	return ":".join([mac[e:e+2] for e in range(0,11,2)])
def run(param1,param2):
	address = (host, port)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(address)
	des = EncryptionAlgorithm.DES(DESKey,DESVector)
	mssage = "{\"MacAddress\":\"ACDE48001122\", \"UserName\":\"abc\", \"Random\":\"774\"}"
	LogRecorder.LogUtility("["+str(param2)+"][LogRecorder][run]->send encrypted message: "+mssage)
	s.send(des.encrypt(mssage.encode(encoding="utf-8")))
	data = s.recv(2048)
	LogRecorder.LogUtility("["+str(param2)+"][LogRecorder][run]->recived encrypted message: "+str(data))
	byteData = des.decrypt(data)
	LogRecorder.LogUtility("["+str(param2)+"][LogRecorder][run]-> decrypted message: "+str(byteData))
	s.close()
	LogRecorder.LogUtility("["+str(param2)+"][LogRecorder][run]->Thread["+str(param2)+"]:Successed")


if __name__ == '__main__':
	# 开始时间
	start = time.time()

	threadpool = []

	for num in range(1,10000):
		th = threading.Thread(target=run, args=(run, num))
		threadpool.append(th)
	for th in threadpool:
		th.start()
	for th in threadpool:
		threading.Thread.join(th)

	# 结束时间
	end = time.time()
	print("完成的时间为：" + str(end - start))

	# main()
