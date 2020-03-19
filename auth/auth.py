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
import contextlib

from aiohttp import web
from datetime import datetime, timedelta
from dateutil import tz


class Auth:
    algorithm = 'HS256'

    def __init__(self, secret, validity, redis_addr):
        self.redis = None
        self.secret = secret
        self.validity = validity
        self.redis_addr = redis_addr

    async def conn(self):
        print(f'Connect to the redis database {self.redis_addr} ......')
        self.redis = await aioredis.create_redis(f'redis://{self.redis_addr}',
                                                 encoding='utf-8')

    async def init(self, aiohttp_app):
        await self.conn()
        aiohttp_app.router.add_post('/issue_token', self.issue_token)
        aiohttp_app.router.add_post('/redeem_nonce', self.redeem_nonce)
        aiohttp_app.router.add_post('/register_nonce', self.register_nonce)
        aiohttp_app.router.add_post('/validate_token', self.validate_token)
        return aiohttp_app

    async def issue_token(self, request):
        not self.redis.closed or await self.conn()
        post = await request.post()
        token = Auth.generate_token(post['uid'], self.secret, self.validity)
        keys = ['auth', 'tokens', 'invalidated', post["uid"]]
        if post.get("is_session").__eq__('1'):
            keys.append('world')
        await self.redis.set('.'.join(keys), token, expire=self.validity)
        return web.json_response({'token': token})

    async def validate_token(self, request):
        post = await request.post()
        with contextlib.suppress(jwt.DecodeError, jwt.ExpiredSignatureError):
            uid = Auth.decode_token(post['token'], self.secret)
            tks = '.'.join(['auth', 'tokens', 'invalidated', uid])
            sks = '.'.join(['auth', 'tokens', 'invalidated', uid, 'world'])
            if await self.redis.exists(tks) and \
                    await self.redis.get(tks) == post['token'] or \
                    await self.redis.exists(sks) and \
                    await self.redis.get(sks) == post['token']:
                return web.json_response({'status': 0, 'data': {'uid': uid}})
        return web.json_response({'status': 1})

    async def register_nonce(self, request):
        post = await request.json()
        await self.redis.hmset_dict(f'auth.nonces.{post["nonce"]}',
                                    post['payload'])
        return web.json_response({'status': 0})

    async def redeem_nonce(self, request):
        results = {}
        for nonce in (await request.json())['keys']:
            payload = await self.redis.hgetall(f'auth.nonces.{nonce}')
            results[nonce] = {'status': 0, **payload} if len(
                payload) != 0 else {'status': 1}
            await self.redis.delete(f'auth.nonces.{nonce}')
        return web.json_response(results)

    @staticmethod
    def generate_token(uid, secret, validity):
        tkn = jwt.encode({'exp': datetime.now(
            tz=tz.gettz('Asia/Shanghai')) + timedelta(seconds=validity),
                          'uid': uid}, secret, Auth.algorithm)
        return tkn.decode('utf-8')

    @staticmethod
    def decode_token(token, secret):
        payload = jwt.decode(token, secret, algorithms=[Auth.algorithm])
        return payload['uid']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('secret', type=str)
    parser.add_argument('-p', '--port', type=int, default=8001)
    parser.add_argument('--validity', type=int, default=30 * 24 * 3600)
    parser.add_argument('--redis-addr', type=str, default='redis')
    args = parser.parse_args()
    web.run_app(Auth(args.secret, args.validity, args.redis_addr).init(
        web.Application()), port=args.port)


if __name__ == '__main__':
    main()
