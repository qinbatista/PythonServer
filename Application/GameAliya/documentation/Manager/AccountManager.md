# AccountManager

The Account Manager is responsible for handling requests pertaining to the user's account information. Handles requests for logging in as well as binding accounts.

See the General Server documentation for more information on request and response format.


## API Documentation and Sample Requests

The following sections each describe supported function / API calls from the client to the server as well as their accompanying response. Internal Manager HTTP API calls are not described here.


Any function call that is not formatted correctly will receive the following response:
```json
{
	"status" : "10",
	"message": "invalid message format",
	"data" : {}
}
```

Any function call that requires a valid token and does not supply one will receive the following response:
```json
{
	"status" : "11",
	"message": "authorization required",
	"data" : {
				"bad_token" : "VALUE OF BAD TOKEN"
			 }
}
```

---

### login

Attempts to log the user in using the specified credentials. The 'identifier' specifies which identifying information the user will try to use to log in. 

Valid identifiers are: account, email, phone\_number. 

Returns an authorized token to the user.

Status codes and meaning:

- 0 - Success
- 1 - Invalid credentials



##### Sample Request
```json
{
	"function" : "login",
	"data" : {
				"identifier" : "IDENTIFIER",
				"value" : "VALUE_OF_IDENTIFIER",
				"password" : "PASSWORD"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"token" : "generated token"
			 }
}
```



### login\_unique

Tries to log the user in using their unique\_id. A user can log in using just their unique\_id if they have not yet bound their account. The game can only be played until a certain point with an unbound account. If it is a new unique\_id, create a new account and populate database tables with information. Returns an authorized token to the user.

Status codes and meaning:

- 0 - Success
- 1 - Success, new account created
- 2 - The account has already been bound before, log in using a different method



##### Sample Request
```json
{
	"function" : "login",
	"data" : {
				"unique_id" : "UNIQUE_ID"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"token" : "generated token"
			 }
}
```




### bind\_account

Binds the account specified with the unique\_id to the provided account name and password.

Status codes and meaning:

- 0 - Success
- 1 - Account name already exists
- 2 - The account has already been bound before
- 3 - Need to be logged in



##### Sample Request
```json
{
	"function" : "login",
	"data" : {
				"token" : "TOKEN",
				"account" : "ACCOUNT_NAME",
				"password" : "PASSWORD"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
			 }
}
```



