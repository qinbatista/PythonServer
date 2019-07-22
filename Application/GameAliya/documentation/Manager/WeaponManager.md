# WeaponManager

The WeaponManager is responsible for handling requests pertaining to weapons. This includes things such as weapon level ups.

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



### level\_up\_weapon

Used to level up a particular weapon.
Currently only supports leveling up a single weapon at a time.
The "iron" field should provide the amount of iron that the client is willing to spend on leveling up their weapon. It currently takes 20 iron to level up a single time. If the client makes a request with '100' iron, they will attempt to level up 5 total times. The max level per weapon is level 100.

Status codes and meaning:

- 0 - Success
- 1 - User does not have that weapon
- 2 - Insufficient materials, upgrade failed
- 3 - Database operation error
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
				"keys" : head is list,
				"values" : row is list
			 }
}
```




### level\_up\_passive

Used to level up a the passive skill of a particular weapon.

Status codes and meaning:

- 0 - Success
- 1 - User does not have that weapon
- 2 - Insufficient skill points, upgrade failed
- 3 - Database operation error
- 9 - passive skill does not exist



##### Sample Request
```json
{
	"function" : "level_up_passive",
	"data" : {
				"token" : "valid token here",
				"weapon" : "WEAPON_NAME_HERE",
				"passive" : "passive_skill_name_here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys": head is list, 
        		"values": row is list
			 }
}
```




### reset\_weapon\_skill\_point

Resets all weapon's skill points. All removed skill points are refunded to the user. Costs coins.

Status codes and meaning:

- 0 -Weapon reset skill point success
- 1 - User does not have that weapon
- 2 - Insufficient gold coins, upgrade failed
- 3 - Database operation error



##### Sample Request
```json
{
	"function" : "reset_weapon_skill_point"
	"data" : {
				"token" : "TOKEN",
				"weapon": "WEAPON NAME HERE"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys": head is list, 
        		"values": row is list
			 }
}
```




### level\_up\_weapon\_star

Levels up the weapon star of the specified weapon. Costs segments.

Status codes and meaning:

- 0 - Weapon upgrade success
- 2 - Insufficient segments, upgrade failed
- 3 - database operation error!



##### Sample Request
```json
{
	"function" : "level_up_weapon_star"
	"data" : {
				"token" : "valid token here",
				"weapon": "WEAPON"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys": head is list, 
        		"values": row is list
    		 }
}
```




### get\_all\_weapon

Returns the entire row of the weapon bag.

Status codes and meaning:

- 0 - Gain success


##### Sample Request
```json
{
	"function" : "get_all_weapon"
	"data" : {
				"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "gain success",
	"data" : {
        		"keys": [......],
        		"values": [[...], [...], ...]
			 }
}
```



