import sys, os
import os.path
import threading
import socket
from time import ctime
import time
import json
port = 2002
def main():
	thread1 = threading.Thread(target=run,name="thread",args=("paramMessage1","paramMessage2"))
	thread1.start()
def StaffCheckIn(message,IPAdress):
	status=""
	if message=="":
		return  {"status":"-1","message":"get null message"}
	MessageDic = json.loads(message)
	MacAdress = MessageDic["MacAdress"]
	UserName = MessageDic["UserName"]
	print("Recive  MacAdres   From:"+IPAdress+"->["+MacAdress+"]")
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
	s.bind(('',port))
	s.listen(10)
	while True:
		cs,address = s.accept()
		ra=cs.recv(2048)
		message = ra.decode(encoding='utf-8')
		IPAdress = str(list(address)[0])
		status = StaffCheckIn(message,IPAdress)
		cs.send(str(status).encode(encoding="utf-8"))
	cs.close()
if __name__ == '__main__':
	main()