# Final API Documentation

Documentation for the final versions of the API as will be used in the game.

See the General Server documentation for more information on request and response format.


## API Documentation and Sample Requests

The following sections each describe supported function / API calls from the client to the server as well as their accompanying response. 
Note that internal Manager HTTP API calls are not described here.


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


### Sample

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```



### Basic Summon

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "basic_summon",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```

### Pro Summon

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "pro_summon",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```


### Friendly Summon

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "friendly_summon",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```

### Phophet Summon

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "prophet_summon",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```


### Basic Summon Skill 

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "basic_summon_skill",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```


### Pro Summon Skill 

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "pro_summon_skill",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```


### Friend Summon Skill 

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "friend_summon_skill",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```


### Basic Summon Role 

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "basic_summon_role",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```


### Pro Summon Role

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "pro_summon_role",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```


### Friend Summon Role 

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "friend_summon_role",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```

### Start Hang Up 

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "start_hang_up",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```


### Get Hang Up Reward 

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "get_hang_up_reward",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```


### Enter Stage 

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "enter_stage",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```


### Pass Level Success 

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "friend_summon_role",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```

### Fortune Wheel Basic 

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "fortune_wheel_basic",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```

### Fortune Wheel Pro 

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "fortune_wheel_pro",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```


### Disintegrate Weapon 

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "disintegrate_weapon",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```

### Automatically Refresh Store

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "automatically_refresh_store",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```


### Manually Refresh Store

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "manually_refresh_store",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```


### Diamond Refresh Store

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "diamond_refresh_store",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```


### Black Market Transaction

Empty

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "black_market_transaction",
	"data" : {
    			"token" : "valid token here"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```
