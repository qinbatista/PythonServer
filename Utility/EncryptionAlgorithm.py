import base64
import pyDes
import binascii

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
		d = k.decrypt(base64.decodebytes(data))
		return d