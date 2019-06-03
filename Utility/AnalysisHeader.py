import base64
import pyDes
import binascii
import random
from Utility import EncryptionAlgorithm, LogRecorder
import json


class Header:
	def __init__(self, msg=b"6275e26419211d1f526e674d97110e152222"):
		msg = bytes.decode(msg)
		self.md5 = self.ShowMD5Message(msg)
		self.size = self.ShowMessageSize(msg)
		self.App = self.isAPPMessage(self.md5)

	def HideMsgSize(self, data):
		"""
		hide buffer size in md5 string, insert 4 number to position 1,3,5,7
		"""
		number = data[32:]  # 32个字节之后的数据
		md5string = data[:32]
		self.MessageSize = len(number)
		if self.MessageSize >= 1:
			md5string = md5string[:1] + number[0] + md5string[1:]  # 1号位置插入数字长度
		if self.MessageSize >= 2:
			md5string = md5string[:3] + number[1] + md5string[3:]
		if self.MessageSize >= 3:
			md5string = md5string[:5] + number[2] + md5string[5:]
		if self.MessageSize >= 4:
			md5string = md5string[:7] + number[3] + md5string[7:]
		return md5string  # 1 3 5 7是字符串长度的插入位置

	def ShowMessageSize(self, data):
		"""
		get size message from 36 byte message
		"""
		size = data[1] + data[3] + data[5] + data[7]
		return size.replace("#", "")

	def ShowMD5Message(self, data):
		"""
		delete size message from string, only md5 message
		"""
		MD5Message = data[0] + data[2] + data[4] + data[6] + data[8:]
		return MD5Message

	def isAPPMessage(self, md5String):
		if md5String == "e3cb970693574ea75d091a6049f8a3ff":  # md5 of string of "natasha"
			LogRecorder.LogUtility("[AnalysisHeader][isLegalMessage]Get aliya message, pass")
			return "aliya"
		elif md5String == "7e1bd1f7a5fb2e316fafb6a4bf5d174e":  # md5 of string of "natasha"
			LogRecorder.LogUtility("[AnalysisHeader][isLegalMessage]Get workingcat message, pass")
			return "workingcat"
		else:
			return ""

	def MakeHeader(self, KeyString, StringLength):  # 软件名字，加密数据的长度
		des = EncryptionAlgorithm.DES()
		MD5 = des.MD5Encrypt(KeyString)  # 加密软件名字 32个字节
		# 这里保证了数据等长为4
		DigitsAs4 = "#" * (4 - len(StringLength)) + StringLength  # （4-加密数据的长度的长度）个#字符 + 加密数据的长度
		ReturnString = self.HideMsgSize(MD5 + DigitsAs4)  # 36 个字符，中间包含了md5算法和详细数据的长度
		return str.encode(ReturnString)


def message_constructor(status, message, data=None):
	result = '{"status":"%s","message":"%s","random":"%s","data":"null"}' % (
	status, message, str(random.randint(-1000, 1000)))
	# 分段保存字符串
	if data: result = result.replace('"null"', json.dumps(data))
	return result


if __name__ == "__main__":
	byteMsg = b"natasha,4"
	StringMsg = "natasha,4"

	tool = Header()
	newMessage = tool.MakeHeader("natasha", "24")
	print(newMessage)
	my = Header(str.encode(newMessage))
	print(my.App)
	print(my.md5)
	print(my.size)
