import sys, os
from socket import *
import threading
import time
import uuid
import socket
#host  = 'magicwandai.com' # 这是服务器的电脑的ip
host  = '192.168.0.102' # 这是服务器的电脑的ip
port = 200 #接口选择大于10000的，避免冲突
bufsize = 1024  #定义缓冲大小
addr = (host,port) # 元祖形式
udpClient = socket.socket(AF_INET,SOCK_DGRAM) #创建客户端
def main():
	thread1 = threading.Thread(target=run,name="线程1",args=("123","123"))
	thread1.start()
def get_mac_address(): 
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:] 
    return ":".join([mac[e:e+2] for e in range(0,11,2)])
def get_host_ip():
    try:
        s = socket.socket(AF_INET,SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
def run(param1,param2):
	global addr
	checkStatus = "1"
	while True:
		data = get_mac_address()+","+checkStatus
		print(data)
		data = data.encode(encoding="utf-8") 
		udpClient.sendto(data,addr) # 发送数据
		time.sleep(10)
	udpClient.close()

if __name__ == '__main__':
	address = ('192.168.0.102', 2000)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(address)
	mssage = "hihi"
	s.send(mssage.encode(encoding="utf-8"))
	data = s.recv(512)
	print('the data received is',data.decode(encoding="utf-8"))
	
	s.close()