# GameManager

The Game Manager is responsible for handling all requests pertaining to the game.
This includes requests for the current number of resources, or leveling up a weapon.
Each Game Manager is responsible for a range of game worlds.

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
				"weapon_bag1" : [ entire row of weapon bag,unique_id replaced with weapon ],
				"item1" : ['iron', remaining_iron_after_upgrade]
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
				"weapon_bag1" : [ entire row of weapon bag,unique_id replaced with weapon ]
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
				"weapon_bag1" : [ entire row of weapon bag，unique_id replaced with weapon ],
				"item1" : ["coin", REMAINING_COINS]
			 }
}
```




### level\_up\_weapon\_star

Levels up the weapon star of the specified weapon. Costs segments.

Status codes and meaning:

- 0 - Weapon upgrade success
- 1 - User does not have that weapon
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
				"weapon_bag1" : [ entire row of weapon bag and WEAPON_STAR ]
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
				"weapon_bag1" : [ entire row of weapon bag and weapon star ],
        		"weapon_bag2" : [ entire row of weapon bag and weapon star ],
        		...
        		...
        		...
        		"weapon_bagN" : [ entire row of weapon bag and weapon star ]
			 }
}
```










## DANGEROUS 

## ========   random\_gift\_skill   ========

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
    			"world" : "str 1 or 2 or 3....",
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



## DANGEROUS

## ========   random\_gift\_segment   ========

Gives the user a chance at getting random segments, or a new weapon.

Status codes and meaning:

- 0 - Unlocked new weapon
- 0 - Weapon already unlocked, got free segment!
- 1 - no weapon

##### Sample Request

```json
{
	"function" : "random_gift_segment"
	"data" : {
    			"world" : "str 1 or 2 or 3....",
				"token" : "valid token here"
			 }
}
```

##### Sample Response 1

```json
{
	"status" : "0",
	"message": "Unlocked new weapon!",
	"data" : {
        		"keys": ["weapon"],
              	"values": [weapon]
             }
}
```

##### Sample Response 2

```json
{
	"status" : "0",
	"message": "Weapon already unlocked, got free segment!",
	"data" : {
                "keys": ['weapon', 'segment'], 
                "values": [weapon, segment]
    		 }
}
```



## ========   level_up_skill   ========

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
	"function" : "level_up_skill",
	"data" : {
    			"world" : "str 1 or 2 or 3....",
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



## ========   level\_up\_scroll ========

Combine several existing low level scrolls to make one higher level scroll.

(3) 10% skill scrolls -> (1) 30% skill scroll

(3) 30% skill scrolls -> (1) 100% skill scroll

Status codes and meaning:

- 0 - level up scroll success
- 1 - advanced reels are not upgradeable
- 2 - insufficient scroll
- 3 - unexpected parameter --> scroll_id
- 4 - parameter error
- 9 - database operation error

##### Sample Request

```json
{
	"function" : "level_up_scroll"
	"data" : {
    			"world" : "str 1 or 2 or 3....",
				"token" : "valid token here",
				"scroll_id" : "SCROLL_ID"
			 }
}
```

##### Sample Response 1

```json
{
	"status" : "0",
	"message": "level up scroll success",
	"data" : {
				"keys" : [ "skill_scroll_10", "skill_scroll_30" ],
				"values" : [ "value10", "value30" ]
			 }
}
```

##### Sample Response 2

```json
{
	"status" : "0",
	"message": "level up scroll success",
	"data" : {
				"keys" : [ "skill_scroll_30", "skill_scroll_100" ],
				"values" : [ "value30", "value100" ]
			 }
}
```



## ========   pass_stage   ========

Let the player enter the next stage and give the reward.

Status codes and meaning:

- 0 - passed customs
- 1 - database operation error
- 9 - abnormal data!

##### Sample Request

```json
{
	"function" : "pass_stage"
	"data" : {
    			"world" : "str 1 or 2 or 3....",
				"token" : "TOKEN",
    			"stage" : "int"
			 }
}
```

##### Sample Response

```json
{
	"status" : "0",
	"message": "passed customs",
	"data" : {
        		"keys": [], 
        		"values": [], 
        		"rewards": []
			 }
}
```



## ========   get\_all\_skill\_level   ========

Returns all the current skill levels.

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"function" : "get_all_skill_level"
	"data" : {
    			"world" : "str 1 or 2 or 3....",
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



## ========   get\_skill   ========

Returns the requested skill level.

Status codes and meaning:

- 0 - Success
- 1 - Invalid skill name


##### Sample Request
```json
{
	"function" : "get_skill",
	"data" : {
    			"world" : "str 1 or 2 or 3....",
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



## ========   update_energy   ========

Get the energy value or the energy consumption value.

Status codes and meaning:

- 0 - 获取能量成功 
  - Get energy successfully
- 0 - 能量已消耗，能量值及恢复时间更新成功 
  - Energy has been consumed, energy value and recovery time updated successfully
- 0 - 能量已恢复，获取能量成功 
  -  Energy has been recovered and energy is successfully acquired

- 0 - 能量刷新后已消耗，能量值及恢复时间更新成功
  - After refreshing the energy, the energy value and recovery time are successfully updated.
- 0 - 能量已刷新，未恢复满，已消耗能量，能量值及恢复时间更新成功
  - Energy has been refreshed, not fully recovered, energy has been consumed, energy value and recovery time updated successfully

- 1 - 参数错误 
  - Parameter error
- 2 - 无足够能量消耗 
  - Not enough energy consumption

##### Sample Request

```json
{
	"function" : "update_energy",
	"data" : {
    			"world" : "str 1 or 2 or 3....",
				"token" : "TOKEN",
				"amount" : "int"
			 }
}
```

##### Sample Response

```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys": ['energy', 'recover_time'], 
        		"values": [current_energy, recover_time]
			 }
}
```





## ========   get_all_supplies   ========

获取player表中的所有属性及值，包括energy和recover_time，

获取到的数据发送到客户端，客户端再详细筛选

- 0 - Success


##### Sample Request
```json
{
	"function" : "get_all_supplies",
	"data" : {
    			"world" : "str 1 or 2 or 3....",
				"token" : "TOKEN"
			 }
}
```

##### Sample Response

```json
{
	"status" : "0",
	"message": "get supplies success",
	"data" : {
        		"keys": [heads],
              	"values": [content]
    		 }
}
```



## DANGEROUS 

## ========   add_supplies   ========

#### add_supplies  => coin or iron or diamond or ...

Increases the user's material by the given amount.

Status codes and meaning:

- 0 - Success
- 1 - Failure


##### Sample Request
```json
{
	"function" : "add_supplies"
	"data" : {
    			"world" : "str 1 or 2 or 3....",
				"token" : "valid token here",
				"key" : "material_name",
				"value" : "material_value"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys" : [key],
				"values" : [value]
			 }
}
```








