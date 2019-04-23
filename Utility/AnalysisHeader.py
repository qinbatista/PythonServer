import base64
import pyDes
import binascii
import EncryptionAlgorithm
import LogRecorder
class Header:
	#IV必须是 8 字节长度的十六进制数
	iv = ''
	#key加密密钥长度，24字节
	key = ''
	def __init__(self, msg=b""):
		msg = bytes.decode(msg)
		self.md5 = self.ShowMD5Message(msg)
		self.size = self.ShowMessageSize(msg)
		self.Legal = self.isLegalMessage(self.md5)
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
	def HideMsgSize(self,data):
		"""
		hide buffer size in md5 string, insert 4 number to position 1,3,5,7
		"""
		number = data[32:]
		md5string = data[:32]
		md5string = md5string[:1]+number[0]+md5string[1:]
		md5string = md5string[:3]+number[1]+md5string[3:]
		md5string = md5string[:5]+number[2]+md5string[5:]
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
		return size
	def ShowMD5Message(self,data):
		"""
		delete size message from string, only md5 message
		"""
		MD5Message = data[0:1]+data[2:3]+data[4:5]+data[6:7]+data[8:9]+data[9:]
		return MD5Message
	def isLegalMessage(self, md5String):
		if md5String=="6275e26419211d1f526e674d97110e15":#md5 of string of "natasha"
			LogRecorder.LogUtility("[AnalysisHeader][isLegalMessage]Get Natasha message, pass")
			return True
		else:
			return False


if __name__ == "__main__":
	byteMsg = b"natasha,4"
	StringMsg = "natasha,4"
	# print(bytes.decode(byteMsg))
	listString = bytes.decode(byteMsg).split(",")
	# print(listString)
	des = EncryptionAlgorithm.DES()
	string = des.MD5Encrypt("natasha")
	print(string)
	num = string+"2048"
	tool = Header()
	newMessage = tool.HideMsgSize(num)
	print(newMessage)
	my = Header(str.encode(newMessage))
	print(my.Legal)
	print(my.md5)
	print(my.size)

