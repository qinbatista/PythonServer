# ConfigurationManager

The ConfigurationManager is responsible for handling requests pertaining to the user's application configuration.

See the General Server documentation for more information on request format.


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



### example api

Example documentation

Status codes and meaning:

- 0 - Success
- 1 - User does not have that weapon
- 2 - Insufficient materials, upgrade failed
- 9 - Weapon already max level



##### Sample Request
```json
{
	"function" : "level_up_weapon",
	"data" : {
				"token" : "valid token here",
				"weapon" : "WEAPON_NAME_HERE",
				"iron" : "100"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"weapon_bag1" : [ entire row of weapon bag ],
				"item1" : ['iron', remaining_iron_after_upgrade]
			 }
}
```

