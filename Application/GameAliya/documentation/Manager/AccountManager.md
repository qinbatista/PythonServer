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

**Note - AccountManager API does not require the 'world' parameter to be present in requests**

---

### login\_unique

Tries to log the user in using only their unique\_id.
A user can log in using just their unique\_id if they have not yet bound their account.
The game can only be played until a certain point with an unbound account.
If called with a unique\_id not found in the database, create a new account.

Returns an authorized token to the user.

Status codes and meaning:

- 0 - Success
- 1 - Success, new account created
- 2 - The account has already been bound before, log in using a different method


##### Sample Request
```json
{
	"function" : "login_unique",
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


### login

Attempts to log the user in using the specified credentials.
The 'identifier' specifies which identifying information the user will try to use to log in. 
If the email or phone\_number fields in the response are empty that means those identifiers have not yet been bound to the account.

Valid identifiers are: **account**, **email**, **phone\_number**. 

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
				"token" : "generated token",
				"account" : "ACCOUNT",
				"email" : "EMAIL",
				"phone_number" : "PHONE"
			 }
}
```


### bind\_account

Binds a user account with the provided information.

Minimally, a valid account name and password must be provided when binding.
Email and phone number are optional, and should be left empty if omitted.
This function can be called again to bind previously unbound items such as email or phone.

Data validation for all parameters as follows:
- password - any combination of normal ascii characters. 6-30 length.
- account - starts with a **letter**, followed by any combination of **letter**s, **number**s, **\_**, **.**, **@**, and **-**. 6-25 length.
- email - any valid email address
- phone - any valid phone number, including country code

Status codes and meaning:

- 0 - Success
- 1 - Invalid account name
- 2 - Invalid email
- 3 - Invalid phone
- 4 - Invalid password
- 5 - Account already exists
- 6 - Email already exists
- 7 - Phone already exists
- 8 - Email already bound
- 9 - Phone already bound



##### Sample Request
```json
{
	"function" : "bind_account",
	"data" : {
				"token" : "TOKEN",
				"account" : "ACCOUNT_NAME",
				"password" : "PASSWORD",
				"email" : "EMAIL",
				"phone_number" : "PHONE_NUMBER"
			 }
}
```

```json
{
	"function" : "bind_account",
	"data" : {
				"token" : "TOKEN",
				"account" : "ACCOUNT_NAME",
				"password" : "PASSWORD",
				"email" : "",
				"phone_number" : ""
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



