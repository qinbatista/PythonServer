import jwt
import json
import random
import configparser


from aiohttp import web
from datetime import datetime, timedelta

# NOTE THIS IS NOT PRODUCTION READY
# SECRET SHOULD BE READ FROM ENVIRONMENT VARIABLE

class TokenServer:
	def __init__(self):
		self._invalidated = set()
		self._secret = 'password'
		self._alg = 'HS256'
		self._delta = 500

	
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


	def _message_typesetting(self, status: int, message: str, data: dict = {}) -> dict:
		return {'status' : status, 'message' : message, 'random' : random.randint(-1000, 1000), 'data' : data}

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


def run():
	app = web.Application()
	app.add_routes(ROUTES)
	app['MANAGER'] = TokenServer()

	config = configparser.ConfigParser()
	config.read('Configuration/server/1.0/server.conf')

	web.run_app(app, port = config.getint('token_server', 'port'))

if __name__ == '__main__':
	run()






