import sys
import json
import time
import os
import codecs
import threading
def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
from Utility import LogRecorder,EncryptionAlgorithm
DESKey = "67891234"
DESVector = "6789123467891234"
MessageList=[
	"{\"status\":\"00\",\"message\":\"get null message\"}",
	"{\"status\":\"01\",\"message\":\"Check in\",\"time\":\"%s\",}",
	"{\"status\":\"02\",\"message\":\"Check out\",\"time\":\"%s\",}",
	"{\"status\":\"03\",\"message\":\"Message is illegal\"}",
	"{\"status\":\"04\",\"message\":\"your all personal data\"}",
	"{\"status\":\"05\",\"message\":\"server is busy\"}",
	"{\"status\":\"06\",\"message\":\"Update time\",\"time\":\"%s\",}",
]
class WorkingTimeRecoderClass():
	def __init__(self, *args, **kwargs):
		pass
	def CheckTime_SQL(self,session,IPAdress,UserName):
		return 3
	def CheckTime_Json(self,session,IPAdress,UserName):
		DataBaseJsonLocation = PythonLocation()+"/DataBase/"+time.strftime("%Y-%m", time.localtime())+".json"
		if not os.path.isfile(DataBaseJsonLocation):
			codecs.open(DataBaseJsonLocation, 'w', 'UTF-8').write("{}")
		try:
			readed = json.load(open(DataBaseJsonLocation, 'r',encoding="UTF-8"))
		except:
			print("The service is busy. . .")
			return 5
		JsonChannelList = readed
		ReciveTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		ReciveData = time.strftime("%Y-%m-%d", time.localtime())
		if session not in readed:
			addirc = {session:{ReciveData:{"CheckIn": "", "CheckOut": "", "IP": "", "UserName": ""}}}
			JsonChannelList.update(addirc)
		if ReciveData not in readed[session]:
			ReciveData = time.strftime("%Y-%m-%d", time.localtime())
			adddirc = {session: {ReciveData: {"CheckIn": "", "CheckOut": "", "IP": "", "UserName": ""}}}
			JsonChannelList[session].update(adddirc[session])
		if JsonChannelList[session][ReciveData] != "":
			adddirc = JsonChannelList[session][ReciveData]
			if adddirc["CheckIn"] == "":
				adddirc["CheckIn"] = ReciveTime
				status = 1
			else:
				adddirc["CheckOut"] = ReciveTime
				status = 2
			adddirc["IP"] = IPAdress
			adddirc["UserName"] = UserName
			LogRecorder.LogUtility("[Server][WorkingTimeRecoder][StaffCheckIn]["+IPAdress+"]->IP:"+IPAdress+" UserName->"+UserName+" status:"+str(status))
			JsonChannelList[session][ReciveData].update(adddirc)
		with open(DataBaseJsonLocation, 'w',encoding="UTF-8") as json_file:
			json_file.write(json.dumps(JsonChannelList,ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':')))
		LogRecorder.LogUtility("[Server][WorkingTimeRecoder][StaffCheckIn]["+IPAdress+"] encrypted MessageList[status]: "+MessageList[status])
		return MessageList[status] % (ReciveTime)
	def get_days_hours_second(self, readed, session):
		totall_day = 0
		temp_hours_sum = 0
		temp_second_sum = 0

		if session in readed:  # 判断服务器上是否有这台设备的资源
			session_dict = readed[session]  # 获取这台设备的所有打卡信息
			for data in session_dict.keys():  # data是日期
				totall_day += 1  # 存在一个日期就证明上班过一天
				if session_dict[data]["CheckOut"].replace(" ", "") == "":  # 判断当天有没有签出，就是下班的签到
					temp_hours_sum += 8  # 没有就默认加8个小时
				else:  # 有就分割小时、分钟、秒钟
					CheckInList = (session_dict[data]["CheckIn"][session_dict[data]["CheckIn"].find(" ") + 1:]).split(
						":")
					CheckOutList = (
					session_dict[data]["CheckOut"][session_dict[data]["CheckOut"].find(" ") + 1:]).split(":")
					CheckIn_totall_second = int(CheckInList[0]) * 60 * 60 + int(CheckInList[1]) * 60 + int(
						CheckInList[2])
					CheckOut_totall_second = int(CheckOutList[0]) * 60 * 60 + int(CheckOutList[1]) * 60 + int(
						CheckOutList[2])
					temp_second_sum += (CheckOut_totall_second - CheckIn_totall_second)
					temp_hours_sum += temp_second_sum // 3600
					temp_second_sum = temp_second_sum % 3600
		return totall_day, temp_hours_sum, temp_second_sum
	def get_total_time_Json(self, session):
		"""
		通过用户id获取所有月份的工作天数和工作时间
		工作天数可以通过读取文件下所有json文件的打卡天数
		工作时间通过每一天的时间差求和计算，返回的结果为
		 {"status":"04",
			"message":
					{
						"totall_day":"40",
						"totall_hours":"320"
					}
		 }
		"""
		totall_day = 0
		hours_sum = 0# 记录的是小时数
		second_sum = 0# 记录的是秒钟数

		path = PythonLocation()+"/DataBase/"
		files = os.listdir(path)
		file_list = []
		for file in files:
			if ".json" in file:
				file_list.append(file)
		for file in file_list:
			try:
				readed = json.load(open(path + file, 'r', encoding="UTF-8"))
				days, temp_hours_sum, temp_second_sum = self.get_days_hours_second(readed, session)
				totall_day += days
				hours_sum += temp_hours_sum
				second_sum += temp_second_sum

				hours_sum += second_sum//3600
				second_sum = second_sum%3600
			except:print(path + file + "文件读取有错！！！")
		totall_hours = str(hours_sum) + ":" + (str(second_sum // 60) if (second_sum // 60 > 10) else (
				"0" + str(second_sum // 60))) + ":" + (str(second_sum % 60) if (second_sum % 60 > 10) else (
				"0" + str(second_sum % 60)))
		message ="{\"status\":\"04\",\"message\":{\"totall_day\":\"%s\",\"totall_hours\":\"%s\"}}"%(str(totall_day), str(totall_hours))
		return message
	def get_month_data_Json(self,session,month):
		"""
		通过用户id和需要获取的月份，获取工作天数和工作时间，
		工作天数可以通过读取文件下该月份json文件的打卡天数
		工作时间通过每一天的时间差求和计算，返回的结果为
		 {"status":"04",
			"message":
					{
						"month_day":"21",
						"monyh_hours":"160"
					}
		 }
		"""
		totall_day = 0
		temp_hours_sum = 0# 记录的是小时数
		temp_second_sum = 0# 记录的是秒钟数
		ReciveData = time.strftime("%Y-", time.localtime())
		ReciveData = (ReciveData + str(month)) if int(month) > 10 else (ReciveData + "0" + str(month))
		try:
			readed = json.load(open(PythonLocation() + "/DataBase/" + ReciveData + ".json", "r", encoding="utf-8"))
			totall_day, temp_hours_sum, temp_second_sum = self.get_days_hours_second(readed, session)
		except:print("没有%s的信息！" % ReciveData)
		totall_hours = str(temp_hours_sum) + ":" + (str(temp_second_sum // 60) if (temp_second_sum // 60 > 10) else (
					"0" + str(temp_second_sum // 60))) + ":" + (str(temp_second_sum % 60) if (temp_second_sum % 60 > 10) else (
					"0" + str(temp_second_sum % 60)))
		message = "{\"status\":\"04\",\"message\":{\"month_day\":\"%s\",\"month_day\":\"%s\"}}" % (str(totall_day), str(totall_hours))
		return message
	def VerifyMessageIntegrity(self,message,IPAdress):
		LogRecorder.LogUtility("[Server][WorkingTimeRecoder][StaffCheckIn]["+IPAdress+"]->recived encrypted message:"+str(message))
		des = EncryptionAlgorithm.DES(DESKey,DESVector)
		message = des.decrypt(message)  #decrypt byte message
		message = bytes.decode(message) #byte to string
		LogRecorder.LogUtility("[Server][WorkingTimeRecoder][StaffCheckIn]["+IPAdress+"]->decrypted message:"+message)
		if message == "":
			session="error"
			user_name="error"
			function="error"
			return session,user_name,function
		message_dic  = eval(message)
		if "session" in message_dic.keys():
			session = message_dic["session"]
		if "function" in message_dic.keys():
			function = message_dic["function"]
		if "data" in message_dic.keys():
			user_name = message_dic["data"]["user_name"]
		return session,user_name,function
	def ResolveMsg(self, message, IPAdress):# 客户端的数据、IP地址
		mutex = threading.Lock()
		mutex.acquire()
		des = EncryptionAlgorithm.DES(DESKey,DESVector)
		session,UserName,function = self.VerifyMessageIntegrity(message,IPAdress)
		if function == "GetTime":
			callback_message = MessageList[6] % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		if function == "CheckTime":
			callback_message = self.CheckTime_Json(session,IPAdress,UserName)#really message
			# status = 2 #test message
		if function == "GetMyAlldata":# 获取全部数据
			callback_message = self.get_total_time_Json(session)
		if function == "GetMyMonthdata":# 获取全部数据
			callback_message = self.get_month_data_Json(session, 5)
		retval = des.encrypt(str.encode(str(callback_message)))
		mutex.release()
		return retval

if __name__ == "__main__":
	pass
