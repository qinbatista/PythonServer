import sys
import json
import time
import os
import codecs
import threading
import pymysql
import datetime
import random

def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
from Utility import LogRecorder,EncryptionAlgorithm
from Utility.LogRecorder import LogUtility as Log
from Utility.sql_manager import working_cat as wcsql

DESKey = "67891234"
DESVector = "6789123467891234"

MessageList=[
	"{\"status\":\"00\",\"message\":\"get null message\"}",
	"{\"status\":\"01\",\"message\":\"Check in\",\"time\":\"%s\",}",
	"{\"status\":\"02\",\"message\":\"Check out\",\"time\":\"%s\",}",
	"{\"status\":\"03\",\"message\":\"Message is illegal\"}",
	"{\"status\":\"04\",\"message\":%s}",
	"{\"status\":\"05\",\"message\":\"server is busy\"}",
	"{\"status\":\"06\",\"message\":\"Update time\",\"time\":\"%s\",}",
]
class WorkingTimeRecoderClass():
	def __init__(self, *args, **kwargs):
		pass
	def _get_staff_current_status(self):
		"""
		get all staff status in nowdays
		"""
		day = datetime.datetime.now().strftime("%Y-%m-%d")
		# sql = "SELECT IFNULL(u.user_name,t.unique_id) AS account,t.check_in,t.check_out,t.data_time " + "FROM timeinfo t JOIN userinfo u ON t.unique_id = u.unique_id " +"WHERE t.data_time ='" + day + "';"
		sql = "SELECT u.user_name, t.unique_id, t.check_in, t.check_out, t.data_time " + "FROM timeinfo t JOIN userinfo u ON t.unique_id = u.unique_id " +"WHERE t.data_time ='" + day + "';"
		ss=wcsql(sql)
		print("a"*10+str(len(ss)))
		mystaff = []
		# mystaff = ""
		for staff in ss:
			temp_dict = {
				"user_name": "None" if staff[0] is None else staff[0],
				"unique_id": "None" if staff[1] is None else staff[1],
				"check_in": "None" if staff[2] is None else staff[2],
				"check_out": "None" if staff[3] is None else staff[3],
				"data_time": "None" if staff[4] is None else staff[4],
			}
			mystaff.append(temp_dict)
			# for value in staff:
			# 	if value==None:
			# 		value=""
			# 	if mystaff =="":
			# 		mystaff=value
			# 	else:
			# 		if value!="":
			# 			mystaff=mystaff+","+value
		print((MessageList[4] % mystaff).replace("\'", "\""))
		return (MessageList[4] % mystaff).replace("\'", "\"")
	def _check_time_sql(self,message,session):
		"""
		check in and check out
		"""
		result = self._is_user_exist(session)
		if len(result)>0:
			day = datetime.datetime.now().strftime("%Y-%m-%d")
			time = datetime.datetime.now().strftime("%H:%M:%S")
			if self._is_checked_in(result[0][0],result[0][1],day) == False:
				wcsql("INSERT INTO timeinfo(account,unique_id,check_in,data_time) " + "VALUES ('"+str(result[0][0])+"','"+str(result[0][1])+"','"+time+"','"+day+"')")
				return MessageList[1] % (day+" "+time)
			else:
				wcsql("UPDATE timeinfo SET check_out='"+time+"' WHERE data_time='"+day+"' and account ='"+result[0][0]+"' and unique_id ='"+result[0][1]+"'")
				return MessageList[2] % (day+" "+time)
		return MessageList[2] % ("user is not exist")
	def _create_session(self,message_info):
		message_dic  = eval(message_info)
		session = ""
		if "data" in message_dic.keys():
			unique_id = message_dic["data"]["unique_id"]
			account = message_dic["data"]["account"]
			password = message_dic["data"]["password"]
			if account=="":
				condition = "unique_id='"+unique_id+"'"
				Log("[WorkingTimeRecoder][_create_session] use unique_id for seesion")
			else:
				condition = "account='"+account +"' and password='"+password+"'"
				Log("[WorkingTimeRecoder][_create_session] use account for seesion")
			ss=wcsql("select session from userinfo where "+condition)
			if len(ss)<=0:
				session = unique_id+"_session"
				wcsql("INSERT INTO userinfo(unique_id,account,password,session) VALUES ('"+unique_id+"','"+account+"','"+password+"','"+session+"')")
			else:
				session = str(ss[0][0])
			base_data = {
			"session": session,
			"random": str(random.randint(-1000, 1000))
			}
			return self.MessageConstructor("0","aaaaaa  login as visitor",base_data)
		else:
			return "{\"status\":\"1\",\"message\":\"this phone is already binded a account,please login as account\"}"
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
	def get_total_day_sql(self, session):
		#1:判断用户的session是否存在，如果不存在返回用户不存在消息
		#2:如果存在用户id，如果没有用户id返回唯一表示符，用这个标识符来查询用户的所有数据
		#3:天数进行总计数，有10条数据就累计上班10天
		return "10"
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
		message_dic  = eval(message)
		if "session" in message_dic.keys():
			session = message_dic["session"]
		if "function" in message_dic.keys():
			function = message_dic["function"]
		return session,function,message
	def _ResolveMsg(self, message, ip_address):# 客户端的数据、IP地址
		mutex = threading.Lock()
		mutex.acquire()
		des = EncryptionAlgorithm.DES(DESKey,DESVector)
		session,function,msg_data = self.VerifyMessageIntegrity(message,ip_address)
		callback_message=""
		if function == "get_time":
			callback_message = MessageList[6] % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		if function == "check_time":
			callback_message = self._check_time_sql(msg_data,session)
		if function == "get_total_day":
			callback_message = self.get_total_day_sql(session)
		# if function == "GetMyAlldata":# 获取全部数据
		# 	callback_message = self.get_total_time_Json(user_id)
		# if function == "GetMyMonthdata":# 获取全部数据
		# 	callback_message = self.get_month_data_Json(user_id, 5)
		if function == "get_staff_current_status":
			callback_message = self._get_staff_current_status()
		if function == "login":
			callback_message = self._create_session(msg_data)
		Log("[WorkingTimeRecoder][ResolveMsg] callback_message="+callback_message)
		retval = des.encrypt(str.encode(str(callback_message)))
		mutex.release()
		return retval
	def _is_checked_in(self,account,unique_id,day):
		"""
			check if user checked before.
		"""
		if account=="":
			result = wcsql("select check_in from timeinfo where unique_id = '"+unique_id+"' and data_time='"+day+"'")
		else:
			result = wcsql("select check_in from timeinfo where account = '"+account+"' and data_time='"+day+"'")
		if len(result)<=0:
			print("false")
			return False
		else:
			print("true")
			return True
	def _is_user_exist(self,session):
		"""
			Verify if that user exists
		"""
		result = wcsql("select account,unique_id from userinfo where session='"+session+"'")
		return result
	def _add_new_user(self,session,ip,user_name,gender,email,phone_number):
		"""
			add new user
		"""
		# 像数据库中插入新的用户信息
		user = "INSERT INTO userinfo(session,ip,user_name,gender,email,phone_number) " + "VALUES ('"+session+"','"+ip+"','"+user_name+"','"+gender+"','"+email+"','"+phone_number+"')"
		wcsql(user)
	def _is_visitor(self,session):
		"""
			if user have account in server
		"""
		result = wcsql("select account from userinfo where session = '"+session+"'")
		if len(result)<=0:
			return False
		else:
			return True
	def MessageConstructor(self,status, message, data=""):
		w_data = {
			"status": status,
			"message": message,
			"data": data
		}
		# 分段保存字符串
		if not w_data['data']:
			result = "{" + '"status":"{0}","message":"{1}"'.format(w_data['status'], w_data['message']) + "}"
			return result
		else:
			json_str = json.dumps(data)
			data_str = '"status":"{0}","message":"{1}",'.format(w_data['status'], w_data['message'])
			result = "{" + data_str + '"data":' + json_str + "}"
			return result
if __name__ == "__main__":
	pass

