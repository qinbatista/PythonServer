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
The "iron" field should provide the amount of iron that the client is willing to spend on leveling up their weapon.
It currently takes 20 iron to level up a single time.
If the client makes a request with '100' iron, they will attempt to level up 5 total times.
The max level per weapon is level 100.

Status codes and meaning:

- 0 - Success
- 1 - User does not have that weapon
- 2 - Insufficient materials, upgrade failed
- 3 - Database operation error
- 9 - Weapon already max level



##### Sample Request
```json
{
	"world" : 0,
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
				"keys" : [ head ],
				"values" : [ values ]
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
	"world" : 0,
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
				"keys" : [ head ],
				"values" : [ values ]
			 }
}
```




### reset\_weapon\_skill\_point

Resets all weapon's skill points.
All removed skill points are refunded to the user.
Costs coins.

Status codes and meaning:

- 0 - Weapon reset skill point success
- 1 - User does not have that weapon
- 2 - Insufficient gold coins, upgrade failed
- 3 - Database operation error



##### Sample Request
```json
{
	"world" : 0,
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
				"keys" : [ head ],
				"values" : [ values ]
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
	"world" : 0,
	"function" : "level_up_weapon_star",
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
				"keys" : [ head ],
				"values" : [ values ]
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
	"world" : 0,
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
				"keys" : [ keys ],
				"values" : [ values ]
			 }
}
```











## ========   level\_up\_skill   ========

Consume a skill scroll for a chance to level up the given skill.
The skill must already be unlocked (not level 0).
Different tiers of skill scrolls provide different chances to successfully level up the skill. 


Status codes and meaning:

- 0 - Success  （upgrade=0 升级成功， upgrade=1升级失败）
- 1 - User does not have that skill
- 2 - Invalid scroll id
- 4 - User does not have enough scrolls
- 9 - Skill already at max level

The UPGRADE\_SUCCESS value in the server's response can be either 0 or 1 depending upon whether or not the skill actually leveled up.
A failure here does not mean a failed API call - it means that the scroll skill did not yield a level up.
Different levels of scroll skills have different success rates.

##### Sample Request
```json
{
	"world" : 0,
	"function" : "level_up_skill",
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
				"values" : [skill_level, scroll_quantity]
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
	"world" : 0, 
	"function" : "level_up_scroll",
	"data" : {
				"token" : "TOKEN",
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



## ========   pass\_stage   ========

Let the player enter the next stage and give the reward.
The clear\_time parameter is a string representing the time it took to clear the level.

Status codes and meaning:

- 0 - passed customs
- 1 - database operation error
- 9 - abnormal data!

##### Sample Request

```json
{
	"world" : 0,
	"function" : "pass_stage"
	"data" : {
				"token" : "TOKEN",
    			"stage" : "int",
				"clear_time" : "str"
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
	"world" : 0,
	"function" : "get_all_skill_level"
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
	"world" : 0,
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





## ========   get\_all\_supplies   ========

获取player表中的所有属性及值，包括energy和recover_time，

获取到的数据发送到客户端，客户端再详细筛选

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "get_all_supplies",
	"data" : {
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

## ========   add\_supplies   ========

#### add\_supplies  => coin or iron or diamond or ...

Increases the user's material by the given amount.

Status codes and meaning:

- 0 - Success
- 1 - Failure


##### Sample Request
```json
{
	"world" : 0,
	"function" : "add_supplies",
	"data" : {
				"token" : "TOKEN",
				"supply" : "SUPPLY",
				"value" : int
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


## ========   get\_all\_head   ========

Internal use function.

Returns all the column names of the table specified. Performs no error checking.

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "get_all_head",
	"data" : {
				"table" : "TABLE NAME"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"remaining" : [ list of column names ]
}
```



## ========   get\_all\_material   ========

Internal use function.

Returns all the items in the player bag for the specified player. Performs no error checking.

Status codes and meaning:

- 0 - Success


##### Sample Request
```json
{
	"world" : 0,
	"function" : "get_all_material",
	"data" : {
				"token" : "TOKEN"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"remaining" : [ list of values of items in bag ]
}
```



## ========   basic\_summon   ========

Attempts to summon using the basic chance range.

Current valid cost items are the following: **diamond**,**coin**,**basic_summon_scroll** ,**pro_summon_scroll**,**friend_gift**


Status codes and meaning:

- 0 - Unlocked new weapon
- 1 - get segments success
- 96-weapons opeartion error
- 97-insufficient materials


##### Sample Request
```json
{
	"world" : 0,
	"function" : "basic_summon",
	"data" : {
				"token" : "TOKEN",
				"cost_item" : "COST ITEM"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
					"remaining":
					{
						"weapon":try_result['data']["values"][0],
						"star":try_result['data']["values"][1],
						"segment":try_result['data']["values"][2]
					},
					"reward":
					{
						"weapon":try_result['data']["values"][0],
						"segment":self._standard_segment_count
					}
			 }
}
```


## ========   pro\_summon   ========

Attempts to summon using the pro chance range.

Current valid cost items are the following: **diamond**,**coin**,**basic_summon_scroll** ,**pro_summon_scroll**,**friend_gift**

Status codes and meaning:

- 0 - Unlocked new skill or weapon
- 1 - Received free scroll or segments
- 2 - Invalid skill name
- 3 - Database operation error
- 4 - Insufficient material
- 5 - Cost item error


##### Sample Request
```json
{
	"world" : 0,
	"function" : "pro_summon",
	"data" : {
				"token" : "TOKEN",
				"cost_item" : "COST ITEM"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"remaining":
					{
						"weapon":try_result['data']["values"][0],
						"star":try_result['data']["values"][1],
						"segment":try_result['data']["values"][2]
					},
					"reward":
					{
						"weapon":try_result['data']["values"][0],
						"segment":self._standard_segment_count
					}
			 }
}
```



## ========   friend\_summon   ========

Attempts to summon using the friend chance range.

Current valid cost items are the following: **diamond**,**coin**,**basic_summon_scroll** ,**pro_summon_scroll**,**friend_gift**


Status codes and meaning:

- 0 - Unlocked new skill or weapon
- 1 - Received free scroll or segments
- 2 - Invalid skill name
- 3 - Database operation error
- 4 - Insufficient material
- 5 - Cost item error


##### Sample Request
```json
{
	"world" : 0,
	"function" : "friend_summon",
	"data" : {
				"token" : "TOKEN",
				"cost_item" : "COST ITEM"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"remaining":
					{
						"weapon":try_result['data']["values"][0],
						"star":try_result['data']["values"][1],
						"segment":try_result['data']["values"][2]
					},
					"reward":
					{
						"weapon":try_result['data']["values"][0],
						"segment":self._standard_segment_count
					}
			 }
}
```

## ========   start\_hang\_up   ========

Documentation needed. Author: HouYao


Status codes and meaning:

- 0 - Hang up success
- 1 - Repeated hang up successfully
- 2 - Database operation error


##### Sample Request
```json
{
	"world" : 0,
	"function" : "start_hang_up",
	"data" : {
				"token" : "TOKEN",
				"stage" : int
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"keys": [ keys ],
				"values" : [ values ],
				"hang_rewards" : [ rewards ]
			 }
}
```


## ========   get\_hang\_up\_reward   ========

Documentation needed. Author: HouYao


Status codes and meaning:

- 0 - Settlement reward success
- 1 - Temporarily no on-hook record


##### Sample Request
```json
{
	"world" : 0,
	"function" : "get_hang_up_reward",
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
				"keys": [ keys ],
				"values" : [ values ],
				"hang_rewards" : [ rewards ]
			 }
}
```


## ========   fortune\_wheel\_basic   ========

Documentation needed. Author: Qin

Spin the wheel of fortune to get a reward. Chance level basic.

Current valid cost items are the following: **diamond**,**coin **,**fortune_wheel_ticket_basic**, **fortune_wheel_ticket_pro**,**basic_summon_scroll** ,**pro_summon_scroll**


Status codes and meaning:

- 0 - get energy success
- 1 - get weapon item success
- 2 - get skill item success
- 3 - get resource success, resource contain,coin,energy,diamond,iron,skill_scroll_10,skill_scroll_30,skill_scroll_100
- 96 - item name error
- 97 - database opeartion error
- 98 - insufficient material
- 99 - cost_item error


##### Sample Request
```json
{
	"world" : 0,
	"function" : "get_hang_up_reward",
	"data" : {
				"token" : "TOKEN",
				"cost_item" : "COST_ITEM"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"remaining" : {
					"keys" : [ COST_ITEM ],
					"values" : [ remaining amount ]
				},
				"reward" : {
						"remaining":
						{
							"scroll_id":try_result['data']["keys"][0],
							"scroll_quantity":try_result['data']["values"][0]
						},
						"reward":
						{
							"scroll_id":try_result['data']["values"][0],
							"scroll_quantity":1
						}
				}
			 }
}
```


## ========   fortune\_wheel\_pro   ========

Documentation needed. Author: Qin

Spin the wheel of fortune to get a reward. Chance level pro.

Current valid cost items are the following: **diamond**,**coin **,**fortune_wheel_ticket_basic**, **fortune_wheel_ticket_pro**,**basic_summon_scroll** ,**pro_summon_scroll**


Status codes and meaning:

- 0 - get energy success
- 1 - get weapon item success
- 2 - get skill item success
- 3 - get resource success, resource contain,coin,energy,diamond,iron,skill_scroll_10,skill_scroll_30,skill_scroll_100
- 96 - item name error
- 97 - database opeartion error
- 98 - insufficient material
- 99 - cost_item error


##### Sample Request
```json
{
	"world" : 0,
	"function" : "get_hang_up_reward",
	"data" : {
				"token" : "TOKEN",
				"cost_item" : "COST_ITEM"
			 }
}
```

##### Sample Response
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"remaining" : {
					"keys" : [ COST_ITEM ],
					"values" : [ remaining amount ]
				},
				"reward" : {
						"remaining":
						{
							"scroll_id":try_result['data']["keys"][0],
							"scroll_quantity":try_result['data']["values"][0]
						},
						"reward":
						{
							"scroll_id":try_result['data']["values"][0],
							"scroll_quantity":1
						}
				}
			 }
}
```

## ========   get_all_friend_info   ========

Documentation needed. Author: Qin

get all friend information to, users information contain user_id, user_name, user_level, user_recovery_time

Status codes and meaning:

- 0 - get all information success

##### Sample Request

```json
{
	"world" : 0,
	"function" : "get_hang_up_reward",
	"data" : {
				"token" : "TOKEN",
				"cost_item" : "COST_ITEM"
			 }
}
```

##### Sample Response

```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"remaining" : {
					"keys" : [ COST_ITEM ],
					"values" : [ remaining amount ]
				},
				"remaining" : {
                  {
                    "f_list_id":f_id_list,
                    "f_name":f_name_list,
                    "f_level":f_level_list,
                    "f_recovery_time":f_recovery_time_list
                }
				}
			 }
}
```



## ========   send_all_friend_gift   ========

Documentation needed. Author: Qin

send all friend gitf  to users, callback will give reuslt of send sccuess friends list , callback contain user_id, user_name, user_level, user_recovery_time

Status codes and meaning:

- 0 - get all information success

##### Sample Request

```json
{
	"world" : 0,
	"function" : "get_hang_up_reward",
	"data" : {
				"token" : "TOKEN",
				"cost_item" : "COST_ITEM"
			 }
}
```

##### Sample Response

```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"remaining" : {
					"keys" : [ COST_ITEM ],
					"values" : [ remaining amount ]
				},
				"remaining" : {
                  {
                    "f_list_id":f_id_list,
                    "f_name":f_name_list,
                    "f_level":f_level_list,
                    "f_recovery_time":f_recovery_time_list
                }
				}
			 }
}
```



## ========   send_friend_gift   ========

Documentation needed. Author: Qin

send friend gift  to one friend, result will give  friend information containing user_id, user_name, user_level, user_recovery_time

Status codes and meaning:

- 0 - send friend gift success because of f_recovering_time is empty
- 1 - send friend gift success because time is over 1 day
- 99 - send friend gift failed, because not cooldown time is not finished

##### Sample Request

```json
{
	"world" : 0,
	"function" : "get_hang_up_reward",
	"data" : {
				"token" : "TOKEN",
				"cost_item" : "COST_ITEM"
			 }
}
```

##### Sample Response

```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"remaining" : {
					"keys" : [ COST_ITEM ],
					"values" : [ remaining amount ]
				},
				"remaining" : {
                  {
                    "f_list_id":f_id,
                    "f_name":f_name,
                    "f_level":f_level,
                    "f_recovery_time":f_recovery_time
                }
				}
			 }
}
```



