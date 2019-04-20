import sys, os
import threading
import time
import uuid
import socket
"""
发送消息内容为：
mac地址,签到状态,用户名

比如：
ac:de:48:00:11:22,1,覃于澎

签到状态1表示签入
起到状态2表示签出

总消息长不能超过2048个字节
"""
#host  = 'magicwandai.com' # 这是服务器的电脑的ip
host  = '192.168.1.155' # 这是服务器的电脑的ip
port = 2002 #接口选择大于10000的，避免冲突
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
	checkStatus = "0"
	UserName = "覃于澎"
	mssage = get_mac_address()+","+checkStatus+","+UserName
	s.send(mssage.encode(encoding="utf-8"))
	data = s.recv(2048)
	MessageDict = eval(data.decode(encoding="utf-8"))
	print('Message Status',MessageDict["status"])
	if MessageDict["status"]=="1":
		print("签到成功")
	else:
		print("签到失败")
	s.close()

if __name__ == '__main__':
	main()
