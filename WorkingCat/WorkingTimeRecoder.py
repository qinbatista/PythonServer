import sys
import json
import time
import os

def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,sys.path[0]+"/Utility")
import LogRecorder
import EncryptionAlgorithm
DESKey = "67891234"
DESVector = "6789123467891234"
MessageList=[
	"{\"status\":\"0\",\"message\":\"get null message\"}",
	"{\"status\":\"1\",\"message\":\"Check in\"}",
	"{\"status\":\"2\",\"message\":\"Check out\"}",
	"{\"status\":\"3\",\"message\":\"get null message\"}",
	"{\"status\":\"4\",\"message\":\"get null message\"}",
	"{\"status\":\"5\",\"message\":\"get null message\"}",
]
DataBaseJsonLocation = PythonLocation()+"/package.json"
def StaffCheckIn(message,IPAdress):
	global MessageList
	LogRecorder.LogUtility("[WorkingTimeRecoder][StaffCheckIn]->recived encrypted message:"+str(message))
	des = EncryptionAlgorithm.DES(DESKey,DESVector)
	# message = str.encode(message)	#string to byte
	message = des.decrypt(message)	#decrypt byte message
	message = bytes.decode(message) #byte to string
	LogRecorder.LogUtility("[WorkingTimeRecoder][StaffCheckIn]->decrypted message:"+message)
	if message=="":
		return  des.encrypt(str.encode(MessageList[0]))
	status=0
	MessageDic = json.loads(message)
	MacAdress = MessageDic["MacAddress"]
	UserName = MessageDic["UserName"]
	global DataBaseJsonLocation
	JsonChannelList = {}
	if os.path.isfile(DataBaseJsonLocation):
		readed = json.load(open(DataBaseJsonLocation, 'r',encoding="UTF-8"))
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
			LogRecorder.LogUtility("[WorkingTimeRecoder][StaffCheckIn]->IP:"+IPAdress+" UserName->"+UserName+" status:"+str(status))
			JsonChannelList[MacAdress][ReciveData].update(adddirc)
	with open(DataBaseJsonLocation, 'w',encoding="UTF-8") as json_file:
		json_file.write(json.dumps(JsonChannelList,ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':')))
	LogRecorder.LogUtility("[WorkingTimeRecoder][StaffCheckIn] encrypted MessageList[status]: "+MessageList[status])
	return  des.encrypt(str.encode(MessageList[status]))

if __name__ == "__main__":
	pass