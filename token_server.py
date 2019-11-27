import jwt
import time
import enum
import json
import random
import secrets
import requests
import configparser


from aiohttp import web
from collections import defaultdict
from datetime import datetime, timedelta

# NOTE THIS IS NOT PRODUCTION READY
# SECRET SHOULD BE READ FROM ENVIRONMENT VARIABLE


class MailType(enum.IntEnum):
	SIMPLE = 0
	GIFT = 1
	FRIEND_REQUEST = 2
	FAMILY_REQUEST = 3

class TokenServer:
	def __init__(self):
		self._invalidated = set()
		self._secret = 'password'
		self._alg = 'HS256'
		self._delta = 3600*24*30
		self._nonce_table = defaultdict(dict)

	
	async def issue_token(self, unique_id: str, prev_token: str) -> dict:
		self._invalidated.add(prev_token)
		payload = {'exp': datetime.utcnow() + timedelta(seconds=self._delta), 'unique_id': unique_id}
		token = jwt.encode(payload, self._secret, self._alg)
		return {'token' : token.decode('utf-8')}


	async def validate(self, token: str) -> dict:
		if token in self._invalidated:
			return self._message_typesetting(1, 'invalid token')
		try:
			payload = jwt.decode(token, self._secret, algorithms = [self._alg])
		except (jwt.DecodeError, jwt.ExpiredSignatureError):
			return self._message_typesetting(1, 'invalid token')
		else:
			return self._message_typesetting(0, 'authorized', {'unique_id' : payload['unique_id']})
	
	async def generate_nonce(self, mtype: str, **kwargs) -> dict:
		try:
			nonce = self._generate_nonce()
			if mtype == 'gift':
				self._nonce_table[nonce]['items'] = kwargs['items']
				self._nonce_table[nonce]['quantities'] = kwargs['quantities']
			elif mtype == 'friend_request':
				self._nonce_table[nonce]['uid_sender'] = kwargs['uid_sender']
				self._nonce_table[nonce]['sender'] = kwargs['sender']
			elif mtype == 'family_request':
				self._nonce_table[nonce]['fid'] = kwargs['fid']
				self._nonce_table[nonce]['uid'] = kwargs['uid']
				self._nonce_table[nonce]['target'] = kwargs['target']
			self._nonce_table[nonce]['type'] = mtype
		except KeyError:
			return self._message_typesetting(-1, 'invalid request format')
		return self._message_typesetting(0, 'success', {'nonce' : nonce})


	async def register_nonce(self, nonce, mtype: str, **kwargs) -> dict:
		try:
			if MailType(int(mtype)) == MailType.GIFT:
				self._nonce_table[nonce]['items'] = kwargs['items']
			elif MailType(int(mtype)) == MailType.FRIEND_REQUEST:
				self._nonce_table[nonce]['uid_sender'] = kwargs['uid_sender']
			elif MailType(int(mtype)) == MailType.FAMILY_REQUEST:
				self._nonce_table[nonce]['name'] = kwargs['name']
				self._nonce_table[nonce]['uid_target'] = kwargs['uid_target']
			self._nonce_table[nonce]['type'] = mtype
		except KeyError:
			return self._message_typesetting(-1, 'invalid request format')
		return self._message_typesetting(0, 'success', {'nonce' : nonce})

	async def redeem_nonce(self, types: [str], nonces: [str]) -> dict:
		results = {}
		for t, n in zip(types, nonces):
			if n not in self._nonce_table:
				results[n] = {'status' : 1, 'type' : t}
			else:
				results[n] = {'status' : 0, **self._nonce_table.pop(n)}
		return results

	async def redeem_nonce_new(self, nonces: [str]) -> dict:
		results = {}
		for nonce in nonces:
			if nonce not in self._nonce_table:
				results[nonce] = {'status' : 1}
			else:
				results[nonce] = {'status' : 0, **self._nonce_table.pop(nonce)}
		return results



	def _message_typesetting(self, status: int, message: str, data: dict = {}) -> dict:
		return {'status' : status, 'message' : message, 'random' : random.randint(-1000, 1000), 'data' : data}

	def _generate_nonce(self) -> str:
		return str(secrets.randbits(256))

def get_config() -> configparser.ConfigParser:
	'''
	Fetches the server's configuration file from the config server.
	Waits until the configuration server is online.
	'''
	while True:
		try:
			r = requests.get('http://localhost:8000/get_server_config_location')
			parser = configparser.ConfigParser()
			parser.read(r.json()['file'])
			return parser
		except requests.exceptions.ConnectionError:
			print('Could not find configuration server, retrying in 5 seconds...')
			time.sleep(5)

def _json_response(body: dict = '', **kwargs) -> web.Response:
	'''
	A simple wrapper for aiohttp.web.Response where we dumps body to json
	and assign the correct content_type.
	'''
	kwargs['body'] = json.dumps(body or kwargs['kwargs']).encode('utf-8')
	kwargs['content_type'] = 'text/json'
	return web.Response(**kwargs)

ROUTES = web.RouteTableDef()
@ROUTES.post('/issue_token')
async def __issue_token(request: web.Request) -> web.Response:
	post = await request.post()
	data = await (request.app['MANAGER']).issue_token(post['unique_id'], post['prev_token'])
	return _json_response(data)


@ROUTES.post('/validate')
async def __issue_token(request: web.Request) -> web.Response:
	post = await request.post()
	data = await (request.app['MANAGER']).validate(post['token'])
	return _json_response(data)

@ROUTES.post('/generate_nonce')
async def __generate_nonce(request: web.Request) -> web.Response:
	post = await request.json()
	kwargs = {k : v for k, v in post.items() if k != 'type'}
	return _json_response(await (request.app['MANAGER']).generate_nonce(post['type'], **kwargs))

@ROUTES.post('/register_nonce')
async def __register_nonce(request: web.Request) -> web.Response:
	post = await request.json()
	kwargs = {k : v for k, v in post.items() if k != 'type' and k != 'nonce'}
	return _json_response(await (request.app['MANAGER']).register_nonce(post['nonce'], post['type'], **kwargs))

@ROUTES.post('/redeem_nonce')
async def __redeem_nonce(request: web.Request) -> web.Response:
	post = await request.json()
	return _json_response(await (request.app['MANAGER']).redeem_nonce(post['type'], post['nonce']))

@ROUTES.post('/redeem_nonce_new')
async def __redeem_nonce_new(request: web.Request) -> web.Response:
	post = await request.json()
	return _json_response(await (request.app['MANAGER']).redeem_nonce_new(post['nonce']))

def run():
	app = web.Application()
	app.add_routes(ROUTES)
	app['MANAGER'] = TokenServer()

	#config = get_config()
	#print(f'starting token_server on port {config.getint("token_server", "port")}...')
	web.run_app(app, port = 8001)

if __name__ == '__main__':
	run()






