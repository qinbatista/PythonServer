# A token server based on the JWT token standard, with a few modifications.
#
# The token server should keep a log of all issued tokens until they expire.
# If a user tries to log in from a different device, any previous tokens issued
# should be invalidated. A token can be invalidated by quarantining it until it's
# natural expiration time.
#
# Tokens are only deemed to be valid if they are both not yet expired, and they
# have not been invalidated.
#
# The server should provide the following API calls:
#
#	-	POST /login {account: str, email: str, password: str, unique_id: str}
#		
#		200 OK
#		Returns a new token if the email and password could be verified,
#		or if the email and str are empty but a unique_id was supplied.
#		Previously issued tokens for the same email / password are invalidated.
#
#		400 Bad Request
#		Occurs when the email or password could not be verified.
#
#
#	-	GET /validate with header Authorization: TOKEN
#
#		200 OK
#		The token is valid.
#
#		400 Bad Request
#		The token is not valid.
#
#
#####################################################################################

import jwt
import json

from aiohttp import web
from datetime import datetime, timedelta

from Utility import UserManager

# NOTE THIS IS NOT PRODUCTION READY
# SECRET SHOULD BE READ FROM ENVIRONMENT VARIABLE
SECRET = 'password'
ALG    = 'HS256'
DELTA  = 200
ROUTES = web.RouteTableDef()
if __name__ == '__main__':
	USER_MANAGER = UserManager.UserManager()
INVALIDATED = set()


class InvalidatedTokenError(Exception):
	pass

def run():
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app)

@ROUTES.post('/login_unique')
async def _login_unique(request: web.Request) -> web.Response:
	post = await request.post()
	try:
		await USER_MANAGER.check_exists('unique_id', post['unique_id'], raise_error = True)
		bound = await USER_MANAGER.account_is_bound(post['unique_id'])
		if bound:
			return _json_response({'message' : 'The account corresponding to this unique_id has already been bound. Please log in using a different method.'}, status = 400)
		token = await _issue_new_token(post['unique_id'])
	except (UserManager.CredentialError):
		return _json_response({'message' : 'Unrecognized unique id'}, status = 400)
	return _json_response({'token' : token.decode('utf-8')})


@ROUTES.post('/login')
async def _login(request: web.Request) -> web.Response:
	post = await request.post()
	try:
		await USER_MANAGER.validate_credentials(post['password'], post['identifier'], post['value'])
		unique_id = await USER_MANAGER.fetch_unique_id(post['identifier'], post['value'])
		token = await _issue_new_token(unique_id)
	except UserManager.CredentialError:
		return _json_response({'message' : 'Invalid credentials'}, status = 400)
	return _json_response({'token' : token.decode('utf-8')})


@ROUTES.get('/validate')
async def _validate(request: web.Request) -> web.Response:
	token = request.headers.get('authorization', None)
	try:
		_check_invalidated(token)
		payload = jwt.decode(token, SECRET, algorithms=[ALG])
	except (jwt.DecodeError, jwt.ExpiredSignatureError, InvalidatedTokenError):
		return _json_response({'message' : 'Token invalid'}, status = 400)
	return _json_response({'unique_id' : payload['unique_id']}, status = 200)


async def _issue_new_token(unique_id: str) -> str:
	'''
	Issues a new token for the unique_id.
	Records the latest issued token for this user.
	TODO: Invalidate old issued tokens
	'''
	payload = {'exp' : datetime.utcnow() + timedelta(seconds = DELTA), 'unique_id' : unique_id}
	token = jwt.encode(payload, SECRET, ALG)
	await _invalidate_previous_token(unique_id)
	await USER_MANAGER.update_token(unique_id, token.decode('utf-8'))
	return token

async def _invalidate_previous_token(unique_id: str) -> None:
	'''
	Invalidates the most recently issued token for the unique_id.
	'''
	previous_token = await USER_MANAGER.fetch_token(unique_id)
	if previous_token:
		INVALIDATED.add(previous_token)
		print(INVALIDATED)

def _check_invalidated(token: str) -> None:
	'''
	Raises InvalidatedTokenError if the token has been invalidated.
	'''
	if token in INVALIDATED:
		raise InvalidatedTokenError

def _json_response(body: str = '', **kwargs) -> web.Response:
	'''
	A simple wrapper for aiohttp.web.Response where we dumps body to json
	and assign the correct content_type.
	'''
	kwargs['body'] = json.dumps(body or kwargs['kwargs']).encode('utf-8')
	kwargs['content_type'] = 'text/json'
	return web.Response(**kwargs)

if __name__ == '__main__':
	run()








