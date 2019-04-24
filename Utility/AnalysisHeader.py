import base64
import pyDes
import binascii
import EncryptionAlgorithm
import LogRecorder
class Header:
	def __init__(self, msg=b"6275e26419211d1f526e674d97110e152222"):
		msg = bytes.decode(msg)
		self.md5 = self.ShowMD5Message(msg)
		self.size = self.ShowMessageSize(msg)
		self.Legal = self.isLegalMessage(self.md5)

	def HideMsgSize(self,data):
		"""
		hide buffer size in md5 string, insert 4 number to position 1,3,5,7
		"""
		number = data[32:]
		md5string = data[:32]
		self.MessageSize = len(number)
		if self.MessageSize>=1:
			md5string = md5string[:1]+number[0]+md5string[1:]
		if self.MessageSize>=2:
			md5string = md5string[:3]+number[1]+md5string[3:]
		if self.MessageSize>=3:
			md5string = md5string[:5]+number[2]+md5string[5:]
		if self.MessageSize>=4:
			md5string = md5string[:7]+number[3]+md5string[7:]
		return md5string
	def ShowMessageSize(self,data):
		"""
		get size message from 36 byte message
		"""
		size = data[1:2]
		size = size+data[3:4]
		size = size+ data[5:6]
		size = size+data[7:8]
		return size.replace("#","")
	def ShowMD5Message(self,data):
		"""
		delete size message from string, only md5 message
		"""
		MD5Message = data[0:1]+data[2:3]+data[4:5]+data[6:7]+data[8:9]+data[9:]
		return MD5Message
	def isLegalMessage(self, md5String):
		if md5String=="6275e26419211d1f526e674d97110e15":#md5 of string of "natasha"
			LogRecorder.LogUtility("[AnalysisHeader][isLegalMessage]Get Natasha message, pass")
			return "natasha"
		elif md5String=="7e1bd1f7a5fb2e316fafb6a4bf5d174e":#md5 of string of "natasha"
			LogRecorder.LogUtility("[AnalysisHeader][isLegalMessage]Get Natasha message, pass")
			return "workingcat"
		else:
			return ""
	def MakeHeader(self,KeyString,StringLength):
		des = EncryptionAlgorithm.DES()
		MD5 = des.MD5Encrypt(KeyString)
		DigitsAs4 = "#"*(4-len(StringLength))+StringLength
		ReturnString = self.HideMsgSize(MD5+DigitsAs4)
		return str.encode(ReturnString)





if __name__ == "__main__":
	byteMsg = b"natasha,4"
	StringMsg = "natasha,4"

	tool = Header()
	newMessage = tool.MakeHeader("natasha","24")
	print(newMessage)
	my = Header(str.encode(newMessage))
	print(my.Legal)
	print(my.md5)
	print(my.size)

