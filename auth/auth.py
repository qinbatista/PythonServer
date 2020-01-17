'''
auth.py

The authentication server is responsible for handling the creation, distribution,
and validation on jwt login tokens.

Additionally, one-time-use keys (nonces) can be registered and redeemed.
'''

import jwt
import asyncio
import aioredis
import argparse

from aiohttp import web
from datetime import datetime, timedelta
from dateutil import tz


class Auth:
	algorithm = 'HS256'

	def __init__(self, secret, validity):
		self.redis    = None
		self.secret   = secret
		self.validity = validity

	async def init(self, aiohttp_app, redis_addr):
		self.redis = await aioredis.create_redis(f'redis://{redis_addr}', encoding = 'utf-8')
		aiohttp_app.router.add_post('/issue_token'   , self.issue_token)
		aiohttp_app.router.add_post('/redeem_nonce'  , self.redeem_nonce)
		aiohttp_app.router.add_post('/register_nonce', self.register_nonce)
		aiohttp_app.router.add_post('/validate_token', self.validate_token)
		return aiohttp_app

	async def issue_token(self, request):
		post  = await request.post()
		token = Auth.generate_token(post['uid'], self.secret, self.validity)
		if post['prev_token'] != '':
			await self.redis.set(f'auth.tokens.invalidated.{post["prev_token"]}', '',expire = self.validity)
		return web.json_response({'token' : token})

	async def validate_token(self, request):
		post = await request.post()
		try:
			uid = Auth.decode_token(post['token'], self.secret)
			if await self.redis.exists(f'auth.tokens.invalidated.{post["token"]}') == 0:
				return web.json_response({'status' : 0, 'data' : {'uid' : uid}})
		except (jwt.DecodeError, jwt.ExpiredSignatureError):
			pass
		return web.json_response({'status' : 1})

	async def register_nonce(self, request):
		post = await request.json()
		await self.redis.hmset_dict(f'auth.nonces.{post["nonce"]}', post['payload'])
		return web.json_response({'status' : 0})

	async def redeem_nonce(self, request):
		results = {}
		for nonce in (await request.json())['keys']:
			payload = await self.redis.hgetall(f'auth.nonces.{nonce}')
			results[nonce] = {'status' : 0, **payload} if len(payload) != 0 else {'status' : 1}
			await self.redis.delete(f'auth.nonces.{nonce}')
		return web.json_response(results)

	@staticmethod
	def generate_token(uid, secret, validity):
		tkn = jwt.encode({'exp' : datetime.now(tz = tz.gettz('Asia/Shanghai')) + \
				timedelta(seconds = validity), 'uid' : uid}, secret, Auth.algorithm)
		return tkn.decode('utf-8')

	@staticmethod
	def decode_token(token, secret):
		payload = jwt.decode(token, secret, algorithms = [Auth.algorithm])
		return payload['uid']



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('secret'       , type = str)
	parser.add_argument('-p', '--port' , type = int, default = 8001)
	parser.add_argument('--validity'   , type = int, default = 30 * 24 * 3600)
	parser.add_argument('--redis-addr' , type = str, default = 'redis')
	args = parser.parse_args()
	web.run_app(Auth(args.secret, args.validity).init(web.Application(), args.redis_addr), \
			port = args.port)

if __name__ == '__main__':
	main()
