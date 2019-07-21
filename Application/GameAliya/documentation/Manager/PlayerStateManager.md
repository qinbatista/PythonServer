# PlayerStateManager

The PlayerStateManager is responsible for handling requests pertaining to the current player's state. The player state includes the bag, player status, and skills.

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

#### skill\_level\_up

Consume a skill scroll for a chance to level up the given skill. The skill must already be unlocked (not level 0). Different tiers of skill scrolls provide different chances to successfully level up the skill. 


Status codes and meaning:

- 0 - Success  （upgrade=0 升级成功， upgrade=1升级失败）
- 1 - User does not have that skill
- 2 - Invalid scroll id
- 4 - User does not have enough scrolls
- 9 - Skill already at max level

The UPGRADE\_SUCCESS value in the server's response can be either 0 or 1 depending upon whether or not the skill actually leveled up. A failure here does not mean a failed API call - it means that the scroll skill did not yield a level up. Different levels of scroll skills have different success rates.

##### Sample Request
```json
{
	"function" : "skill_level_up",
	"data" : {
				"token" : "TOKEN",
				"skill_id" : "SKILL ID",
				"scroll_id" : "SCROLL ID"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys": [skill_id, scroll_id],
				"values" : [skill_level, scroll_quantity],
				"upgrade" : "UPGRADE_SUCCESS"
			 }
}
```



#### get\_all\_skill\_level

Returns all the current skill levels.

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"function" : "get_all_skill_level"
	"data" : {
				"token" : "TOKEN",
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys": [skill_name1, skill_name2, ......, skill_nameN],
        		"values": [skill_value1, skill_value2, ......, skill_valueN]
		 }
}
```




#### get\_skill

Returns the requested skill level.

Status codes and meaning:

- 0 - Success
- 1 - Invalid skill name


##### Sample Request
```json
{
	"function" : "get_skill",
	"data" : {
				"token" : "TOKEN",
				"skill_id" : "SKILL_ID"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys": [skill_id], 
        		"values": [level]
			 }
}
```



#### DANGEROUS random\_gift\_skill

Gives a chance to unlock a new skill if it doesn't already exist. If it does exist, the user gets a free skill scroll instead.

Status codes and meaning:

- 0 - Success  或者 You already have that skill, you got a new scroll for free!
- 2 - invalid skill name
- 3 - database operation error


##### Sample Request
```json
{
	"function" : "random_gift_skill"
	"data" : {
				"token" : "TOKEN",
			 }
}
```

##### Sample Responses
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys": [skill_id],
				"values": [skill_value]
			 }
}
```

```json
{
	"status" : "0",
	"message": "You already have that skill, you get a new scroll for free",
	"data" : {
        		"keys": [skill_scroll_id],
				"values": [scroll_skill_quantity]
			 }
}
```




#### DANGEROUS add_supplies  ===> coin or iron or diamond or ...

Increases the user's material by the given amount.

Status codes and meaning:

- 0 - Success
- 1 - Failure


##### Sample Request
```json
{
	"function" : "increase_energy",
	"data" : {
				"token" : "TOKEN",
				"key": "key",
        		"value": "value"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
        		"keys": [key],
        		"values": [remaining]
    		 }
}
```



#### decrease\_energy

Decreases the user's energy.

Status codes and meaning:

- 0 - Success
- 1 - Energy error


##### Sample Request
```json
{
	"function" : "decrease_energy"
	"data" : {
				"token" : "TOKEN",
				"energy": "ENERGY"
			 }
}
```

======================================================

======================================================

======================================================

##### Sample Response

```json
{
	"status" : "0",
	"message": "success",
	"data" : {
			 }
}
```



#### pass\_level

Advances the player to the next level.

Status codes and meaning:

- 0 - Success
- 1 - Invalid state - the server could not confirm player beat the level


##### Sample Request
```json
{
	"function" : "pass_level"
	"data" : {
				"token" : "TOKEN"
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




#### level\_up\_scroll

Combine several existing low level scrolls to make one higher level scroll.

(3) 10% skill scrolls -> (1) 30% skill scroll

(3) 30% skill scrolls -> (1) 100% skill scroll

Status codes and meaning:

- 0 - Success
- 1 - Not enough scrolls to complete conversion


##### Sample Request
```json
{
	"function" : "level_up_scroll"
	"data" : {
				"token" : "valid token here",
				"scroll_id" : "SCROLL_ID"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"item1" : [ scroll_id, remaining_amount ],
				"item2" : [ converted_scroll_id, resulting_amount ]
			 }
}
```




#### DANGEROUS random\_gift\_segment

Gives the user a chance at getting random segments, or a new weapon.

Status codes and meaning:

- 0 - Success,Unlocked new weapon!或者Weapon already unlocked, got free segment!
- 1 - Success, gained a new weapon


##### Sample Request
```json
{
	"function" : "random_gift_segment"
	"data" : {
				"token" : "valid token here"
			 }
}
```

##### Sample Response 1
```json
{
	"status" : "0",
	"message": "Unlocked new weapon!",
	"data" : {"keys": ["weapon"], "values": [weapon]}
}
```

##### Sample Response 2

```json
{
	"status" : "0",
	"message": "Weapon already unlocked, got free segment!",
	"data" : {"keys": ['weapon', 'segment'], "values": [weapon, segment]}
}
```



#### get\_all\_supplies

Returns all the supplies in the user's bag.

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"function" : "get\_all\_supplies"
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
				"item1" : [item_name, item_quantity],
				.
				.
				"itemN" : [item_name, item_quantity]
			 }
}
```




#### DANGEROUS increase\_supplies

Increases the quantity of the given supplies.

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"function" : "increase_supplies"
	"data" : {
				"token" : "valid token here",
				"supplies" : [supply0, supply1, ..., supplyN],
				"amount" : [amount0, amount1, ..., amountN]
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"supplies" : [supply0, supply1, ..., supplyN],
				"amount" : [amount0, amount1, ..., amountN]
			 }
}
```








