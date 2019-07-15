# A token server based on the JWT token standard, with a few modifications.
#
# The token server should keep a log of all issued tokens until they expire.
# If a user tries to log in from a different device, any previous tokens issued
# should be invalidated. A token can be invalidated by quarantining it until its
# natural expiration time.
#
# Tokens are only deemed to be valid if they are both not yet expired, and they
# have not been invalidated.
#
# The server provides the following API calls:
#
#	-	POST /login {identifier: str, value: str, password: str}
#		The identifier tells the server which type of credential the client supplied.
#		Valid identifiers are ONLY the following: 'account', 'email', 'phone_number'.
#		The value is the value corresponding to the type of identifier supplied. For example,
#		if the identifier is 'account', then the value would be the account name.
#
#		200 OK
#		Returns a new token if the credentials could be verified.
#		Previously issued tokens for the corresponding unique_id are invalidated.
#
#		400 Bad Request
#		The credentials could not be verified.
#
#
#	-	POST /login_unique {unique_id: str}
#		This API call will only return a token if the user has not already bound their account.
#		If the unique_id can not be found, a new user will be created and a token returned.
#
#		200 OK
#		Returns a new token.
#		Previously issued tokens for the unique_id are invalidated.
#
#		400 Bad Request
#		The unique_id could not be found, or the unique_id has already been bound.
#
#
#	-	GET /validate
#		HEADER		Authorization: <token>
#		A request to this method should include the token in the Authorization header.
#
#		200 OK
#		The token is valid. Returns the unique_id of the token holder.
#
#		400 Bad Request
#		The token is not valid.
#
#
#####################################################################################

import jwt
import json

from Application.GameAliya import _05_Manager_User as UserManager
# import UserManager

from aiohttp import web
from datetime import datetime, timedelta

# NOTE THIS IS NOT PRODUCTION READY
# SECRET SHOULD BE READ FROM ENVIRONMENT VARIABLE
SECRET = 'password'
ALG = 'HS256'
DELTA = 360
ROUTES = web.RouteTableDef()
if __name__ == '__main__':
	USER_MANAGER = UserManager.UserManager()
INVALIDATED = set()


class InvalidatedTokenError(Exception):
	pass


def run(port):
	app = web.Application()
	app.add_routes(ROUTES)
	web.run_app(app, port=port)


@ROUTES.post('/login_unique')
async def _login_unique(request: web.Request) -> web.Response:
	post = await request.post()
	exists = await USER_MANAGER.check_exists('unique_id', post['unique_id'])
	if not exists:  # create a new account
		await USER_MANAGER.register_unique_id(post['unique_id'])
		token = await _issue_new_token(post['unique_id'])
		return _json_response({'status': 1, 'message': 'new account created', 'data': {'token': token.decode('utf-8')}})
	bound = await USER_MANAGER.account_is_bound(post['unique_id'])
	if bound:
		return _json_response({'status': 2,'message': 'The account corresponding to this unique_id has already been bound. Please log in using a different method.', 'data': {}}, status=400)
	token = await _issue_new_token(post['unique_id'])
	return _json_response({'status': 0, 'message': 'success', 'data': {'token': token.decode('utf-8')}})


@ROUTES.post('/login')
async def _login(request: web.Request) -> web.Response:
	post = await request.post()
	try:
		await USER_MANAGER.validate_credentials(post['password'], post['identifier'], post['value'])
		unique_id = await USER_MANAGER.fetch_unique_id(post['identifier'], post['value'])
		token = await _issue_new_token(unique_id)
	except UserManager.CredentialError:
		return _json_response({'status': 1, 'message': 'Invalid credentials', 'data': {}}, status=400)
	return _json_response({'status': 0, 'message': 'success', 'data': {'token': token.decode('utf-8')}})


@ROUTES.get('/validate')
async def _validate(request: web.Request) -> web.Response:
	token = request.headers.get('authorization', None)
	try:
		_check_invalidated(token)
		payload = jwt.decode(token, SECRET, algorithms=[ALG])
	except (jwt.DecodeError, jwt.ExpiredSignatureError):
		return _json_response({'message': 'Token expired or could not be decoded'}, status=400)
	except InvalidatedTokenError:
		return _json_response({'message': 'Invalidated token'}, status=400)
	return _json_response({'unique_id': payload['unique_id']}, status=200)


async def _issue_new_token(unique_id: str) -> str:
	'''
	Issues a new token for the unique_id.
	Records the latest issued token for this user.
	'''
	payload = {'exp': datetime.utcnow() + timedelta(seconds=DELTA), 'unique_id': unique_id}
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
	run(8000)
