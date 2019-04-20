import sys, os
import os.path
import threading
import socket
from time import ctime
import time
import json
import base64
import pyDes
import binascii
port = 2002
DESKey = "67891234"
DESVector = "6789123467891234"
def main():
	# target：调用的方法名
	# args：方法中传递的参数
	# name：线程名字
	thread1 = threading.Thread(target=run,name="thread",args=("paramMessage1","paramMessage2"))
	thread1.start()
def StaffCheckIn(message,IPAdress):
	print("StaffCheckIn")
	status=""
	des = DES(DESKey,DESVector)
	# message = str.encode(message)
	message = des.decrypt(message)
	message = bytes.decode(message) 
	print("[StaffCheckIn]->decrypt="+message)
	if message=="":
		return  {"status":"-1","message":"get null message"}
	MessageDic = json.loads(message)
	MacAdress = MessageDic["MacAddress"]
	UserName = MessageDic["UserName"]
	print("Recive  MacAddress   From:"+IPAdress+"->["+MacAdress+"]")
	print("Recive  UserName   From:"+IPAdress+"->["+UserName+"]")
	JsonLocation  = "package.json"
	JsonChannelList = {}
	if os.path.isfile(JsonLocation):
		readed = json.load(open(JsonLocation, 'r',encoding="UTF-8"))
		JsonChannelList = readed
		ReciveTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		ReciveData = time.strftime("%Y-%m-%d", time.localtime())
		if MacAdress not in readed:
			addirc = {MacAdress:{ReciveData:{"CheckIn":"","CheckOut":"","IP":"","UserName":""}}}
			JsonChannelList.update(addirc)
		if ReciveData not in readed[MacAdress]:
			ReciveData = time.strftime("%Y-%m-%d", time.localtime())
			adddirc = {MacAdress:{ReciveData:{"CheckIn":"","CheckOut":"","IP":"","UserName":""}}}
			JsonChannelList[MacAdress].update(adddirc[MacAdress])
		if JsonChannelList[MacAdress][ReciveData]!="":
			adddirc = JsonChannelList[MacAdress][ReciveData]
			if adddirc["CheckIn"]=="":
				adddirc["CheckIn"]=ReciveTime
				status="1"
			else:
				adddirc["CheckOut"]=ReciveTime
				status="0"
			adddirc["IP"]=IPAdress
			adddirc["UserName"]=UserName
			JsonChannelList[MacAdress][ReciveData].update(adddirc)
	with open(JsonLocation, 'w',encoding="UTF-8") as json_file:
		json_file.write(json.dumps(JsonChannelList,ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':')))
	return  {"status":status,"message":"Send Success"}
def run(param1,param2):
	s=socket.socket()
	s.bind(('',port))#server (ipAdress,port)
	s.listen(10)# 监听最多10个连接请求 (Monitor up to 10 connection requests)
	while True:
		# cs include laddr is server and raddr is client
		cs,address = s.accept()# wait client connect # 阻塞等待链接,创建新链接对象（obj)和客户端地址（addr)
		ra=cs.recv(2048)# 每次传送的字节数
		# message = ra.decode(encoding='utf-8')
		IPAdress = str(list(address)[0])
		status = StaffCheckIn(ra,IPAdress)
		cs.send(str(status).encode(encoding="utf-8"))# 通过新链接对象发送数据
	cs.close()
class DES:
	#IV必须是 8 字节长度的十六进制数
	iv = ''
	#key加密密钥长度，24字节
	key = ''
	def __init__(self, iv, key):
		self.iv = iv
		self.key = key
	def encrypt(self, data):
		k = pyDes.triple_des(self.key, pyDes.CBC, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)
		d = k.encrypt(data)
		d = base64.encodestring(d)
		return d
	def decrypt(self, data):
		k = pyDes.triple_des(self.key, pyDes.CBC, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)
		data = base64.decodebytes(data)
		d = k.decrypt(data)
		return d

if __name__ == '__main__':
# 	data = "{\"MacAdress\":\"ACDE48001122\", \"UserName\":\"abc\", \"Random\":\"774\"}"
# 	des = DES(DESKey,DESVector)
# 	encryptdata = des.encrypt(data.encode('utf-8'))
# 	encryptdataString =bytes.decode(encryptdata)
# 	print(encryptdataString)
# 	encryptdata = str.encode(encryptdataString)
# 	print(encryptdata)
# 	decryptdata = des.decrypt(encryptdata)
# 	print(decryptdata)
	main()