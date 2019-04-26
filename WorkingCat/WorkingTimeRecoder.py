import sys
import json
import time
import os
import codecs
import threading
def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,sys.path[0]+"/Utility")
import LogRecorder
import EncryptionAlgorithm
DESKey = "67891234"
DESVector = "6789123467891234"
MessageList=[
	"{\"status\":\"00\"}",#\"message\":\"get null message\"}",
	"{\"status\":\"01\"}",#\"message\":\"Check in\"}",
	"{\"status\":\"02\"}",#\"message\":\"Check out\"}",
	"{\"status\":\"03\"}",#\"message\":\"Message is illegal\"}",
	"{\"status\":\"04\"}",#\"message\":\"get null message\"}",
	"{\"status\":\"05\"}",#\"message\":\"get null message\"}",
]
class WorkingTimeRecoderClass():
	def SendSQLMessage(self):
		pass
	def SendJsonMessage(self):
		pass
	def ResolveMsg(self,message,IPAdress):
		mutex = threading.Lock()
		mutex.acquire()
		global MessageList
		LogRecorder.LogUtility("[Server][WorkingTimeRecoder][StaffCheckIn]["+IPAdress+"]->recived encrypted message:"+str(message))
		des = EncryptionAlgorithm.DES(DESKey,DESVector)
		message = des.decrypt(message)	#decrypt byte message
		message = bytes.decode(message) #byte to string
		LogRecorder.LogUtility("[Server][WorkingTimeRecoder][StaffCheckIn]["+IPAdress+"]->decrypted message:"+message)
		if message=="":
			return  des.encrypt(str.encode(MessageList[0]))
		status=0
		MessageDic = json.loads(message)
		if "session" in MessageDic:
			MacAdress = MessageDic["session"]
		else:
			return  des.encrypt(str.encode(MessageList[3]))
		if "UserName" in MessageDic:
			UserName = MessageDic["UserName"]
		else:
			return  des.encrypt(str.encode(MessageList[3]))
		DataBaseJsonLocation = PythonLocation()+"/DataBase/"+time.strftime("%Y-%m", time.localtime())+".json"
		if os.path.isfile(DataBaseJsonLocation)==False:
			f=codecs.open(DataBaseJsonLocation,'w', 'UTF-8')
			f.close()
		OpenError = True
		while OpenError:
			try:
				readed = json.load(open(DataBaseJsonLocation, 'r',encoding="UTF-8"))
				OpenError=False
			except:
				OpenError=True
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
				status=1
			else:
				adddirc["CheckOut"]=ReciveTime
				status=2
			adddirc["IP"]=IPAdress
			adddirc["UserName"]=UserName
			LogRecorder.LogUtility("[Server][WorkingTimeRecoder][StaffCheckIn]["+IPAdress+"]->IP:"+IPAdress+" UserName->"+UserName+" status:"+str(status))
			JsonChannelList[MacAdress][ReciveData].update(adddirc)
		with open(DataBaseJsonLocation, 'w',encoding="UTF-8") as json_file:
			json_file.write(json.dumps(JsonChannelList,ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':')))
		LogRecorder.LogUtility("[Server][WorkingTimeRecoder][StaffCheckIn]["+IPAdress+"] encrypted MessageList[status]: "+MessageList[status])
		mutex.release()
		return  des.encrypt(str.encode(MessageList[status]))

if __name__ == "__main__":
	pass