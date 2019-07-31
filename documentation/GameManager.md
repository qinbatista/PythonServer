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

## ========   level\_up\_weapon   ========

Documentation needed. Author: HouYao

Used to level up a particular weapon.
Currently only supports leveling up a single weapon at a time.
The "iron" field should provide the amount of iron that the client is willing to spend on leveling up their weapon.
It currently takes 20 iron to level up a single time.
If the client makes a request with '100' iron, they will attempt to level up 5 total times.
The max level per weapon is level 100.

Status codes and meaning:

- 0 - Success
- 95 - User does not have that weapon
- 96 - Incoming materials are not upgraded enough
- 97 - Insufficient materials, upgrade failed
- 98 - Database operation error
- 99 - Weapon already max level



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
				"remaining" : 
                {
                    "weapon": "string",
                    "weapon_level": "int",
                    "passive_skill_1_level": "int",
                    "passive_skill_2_level": "int",
                    "passive_skill_3_level": "int",
                    "passive_skill_4_level": "int",
                    "skill_point": "int",
                    "segment": "int",
                    "iron": "int"
                }
			 }
}
```




## ========   level\_up\_passive   ========

Documentation needed. Author: HouYao

Used to level up a the passive skill of a particular weapon.

Status codes and meaning:

- 0 - Success
- 96 - User does not have that weapon
- 97 - Insufficient skill points, upgrade failed
- 98 - Database operation error
- 99 - Passive skill does not exist



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
				"remaining" : 
                {
                    "weapon": "string",
                    "weapon_level": "int",
                    "passive_skill_1_level": "int",
                    "passive_skill_2_level": "int",
                    "passive_skill_3_level": "int",
                    "passive_skill_4_level": "int",
                    "skill_point": "int",
                    "segment": "int"
                }
			 }
}
```




## ========   reset\_weapon\_skill\_point   ========

Documentation needed. Author: HouYao

Resets all weapon's skill points.
All removed skill points are refunded to the user.
Costs coins.

Status codes and meaning:

- 0 - Weapon reset skill point success
- 97 - User does not have that weapon
- 98 - Insufficient gold coins, upgrade failed
- 99 - Database operation error



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
				"remaining" : 
                {
                    "weapon": "string",
                    "weapon_level": "int",
                    "passive_skill_1_level": "int",
                    "passive_skill_2_level": "int",
                    "passive_skill_3_level": "int",
                    "passive_skill_4_level": "int",
                    "skill_point": "int",
                    "segment": "int",
                    "coin": "int"
                }
			 }
}
```




## ========   level\_up\_weapon\_star   ========

Documentation needed. Author: HouYao

Levels up the weapon star of the specified weapon. Costs segments.

Status codes and meaning:

- 0 - Weapon upgrade success
- 98 - Insufficient segments, upgrade failed
- 99 - Skill has been reset or database operation error!



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
				"remaining" : 
                {
                    "weapon": "string",
                    "weapon_level": "int",
                    "passive_skill_1_level": "int",
                    "passive_skill_2_level": "int",
                    "passive_skill_3_level": "int",
                    "passive_skill_4_level": "int",
                    "skill_point": "int",
                    "segment": "int",
                    "star": "int"
                }
			 }
}
```




## ========   get\_all\_weapon   ========

Documentation needed. Author: HouYao

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
				"remaining" : 
                {
                    "weapon1": 
                    {
                        "star": "int",
                        "weapon_level": "int",
                        "passive_skill_1_level": "int",
                        "passive_skill_2_level": "int",
                        "passive_skill_3_level": "int",
                        "passive_skill_4_level": "int",
                        "skill_point": "int",
                        "segment": "int"
                    },
                    "weapon2": 
                    {
                        "star": "int",
                        "weapon_level": "int",
                        "passive_skill_1_level": "int",
                        "passive_skill_2_level": "int",
                        "passive_skill_3_level": "int",
                        "passive_skill_4_level": "int",
                        "skill_point": "int",
                        "segment": "int"
                    }
                }
			 }
}
```











## ========   level\_up\_skill   ========

Documentation needed. Author: HouYao

Consume a skill scroll for a chance to level up the given skill.
The skill must already be unlocked (not level 0).
Different tiers of skill scrolls provide different chances to successfully level up the skill. 


Status codes and meaning:

- 0 - upgrade success
- 1 - upgrade unsuccessful
- 96 - User does not have that skill
- 97 - Invalid scroll id
- 98 - User does not have enough scrolls
- 99 - Skill already at max level

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
        		"remaining": 
        		{
                    "skill_id": "int", 
                    "scroll_id": "int"
                }
			 }
}
```



## ========   level\_up\_scroll ========

Documentation needed. Author: HouYao

Combine several existing low level scrolls to make one higher level scroll.

(3) 10% skill scrolls -> (1) 30% skill scroll

(3) 30% skill scrolls -> (1) 100% skill scroll

Status codes and meaning:

- 0 - level up scroll success
- 95 - advanced reels are not upgradeable
- 96 - insufficient scroll
- 97 - unexpected parameter --> scroll_id
- 98 - parameter error
- 99 - database operation error

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
        		"remaining": 
        		{
                    "skill_scroll_10": "int", 
                    "skill_scroll_30": "int"
                }
			 }
}
```

##### Sample Response 2

```json
{
	"status" : "0",
	"message": "level up scroll success",
	"data" : {
        		"remaining": 
        		{
                    "skill_scroll_30": "int", 
                    "skill_scroll_100": "int"
                }
			 }
}
```



## ========   enter_stage   ========

Documentation needed. Author: HouYao

Let the player enter the next stage and give the reward.
The clear\_time parameter is a string representing the time it took to clear the level.

Status codes and meaning:

- 0 - passed customs
- 97 - database operation error
- 98 - key insufficient
- 99 - parameter error

##### Sample Request

```json
{
	"world" : 0,
	"function" : "enter_stage"
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
        		"remaining": 
                {
                    "iron": 13375, 
                    "coin": 17896, 
                    "energy": 118
                }
			 }
}
```



## ========   pass\_stage   ========

Documentation needed. Author: HouYao

Let the player enter the next stage and give the reward.
The clear\_time parameter is a string representing the time it took to clear the level.

Status codes and meaning:

- 0 - passed customs
- 98 - database operation error
- 99 - abnormal data!

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
        		"remaining": 
                {
                    "stage": 40, 
                    "experience_potion": 6485, 
                    "experience": 340, 
                    "iron": 10820, 
                    "coin": 9521, 
                    "small_energy_potion": 48
                }, 
                "reward": 
                {
                    "experience_potion": 225, 
                    "experience": 10, 
                    "iron": 225, 
                    "coin": 675, 
                    "small_energy_potion": 1
                }
			 }
}
```



## ========   enter_tower   ========

Documentation needed. Author: HouYao

Let the player enter the next stage and give the reward.
The clear\_time parameter is a string representing the time it took to clear the level.

Status codes and meaning:

- 0 - passed customs
- 97 - database operation error
- 98 - key insufficient
- 99 - parameter error

##### Sample Request

```json
{
	"world" : 0,
	"function" : "enter_tower"
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
        		"remaining": 
                {
                    "iron": 13385, 
                    "coin": 17926, 
                    "energy": 119
                }
			 }
}
```



## ========   pass_tower   ========

Documentation needed. Author: HouYao

Let the player enter the next stage and give the reward.
The clear\_time parameter is a string representing the time it took to clear the level.

Status codes and meaning:

- 0 - Earn rewards success
- 1 - Successfully unlock new skills
- 2 - Gain a scroll
- 3 - Gain weapon fragments
- 94 - weapon -> database operating error
- 95 - skill -> database operating error
- 96 - Accidental prize -> key
- 97 - pass_tower_data -> database operation error
- 99 - parameter error

##### Sample Request

```json
{
	"world" : 0,
	"function" : "pass_tower"
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
        		"remaining": 
        		{
                    "iron": 13685, 
                    "coin": 18116, 
                    "energy": 121, 
                    "tower_stage": 10
                }, 
        		"reward": 
        		{
                    "iron": 310, 
                    "coin": 220, 
                    "energy": 3
    			}
			}
}
```



## ========   get\_all\_skill\_level   ========

Documentation needed. Author: HouYao

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
        		"remaining": 
                {
                    "m1_level": 5, 
                    "m11_level": 1, 
                    "m12_level": 1, 
                    "m13_level": 10, 
                    "m111_level": 1	
                }
    		}
}
```



## ========   get\_skill   ========

Documentation needed. Author: HouYao

Returns the requested skill level.

Status codes and meaning:

- 0 - Success
- 99 - Invalid skill name


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
				"remaining": 
        		{
                    "m1_level": 5
                }
			 }
}
```



## ========   show_energy   ========

Documentation needed. Author: HouYao

Get the energy value or the energy consumption value.

Status codes and meaning:

- 2 - 获取能量成功 
  - Get energy successfully
- 4 - 能源已全面恢复，能源更新成功
  - Energy has been fully restored, successful energy update
- 5 - 能源尚未完全恢复，能源更新成功
  -  Energy has not fully recovered, successful energy update
- 97 - 参数错误 
  - Parameter error
- 98 - 无足够能量消耗 
  - Not enough energy consumption
- 99 - 数据库操作错误
  - Database operation error

##### Sample Request

```json
{
	"function" : "show_energy",
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
        		"remaining":
        		{
                    "energy": 0, 
                    "recover_time": "", 
                    "cooling_time": -1
                }
			 }
}
```





## ========   get\_all\_supplies   ========

Documentation needed. Author: HouYao

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
        		"remaining": 
        		{
                    "game_name": "", 
                    "coin": 2541, 
                    "iron": 5235, 
                    "diamond": 3244, 
                    "energy": 0, 
                    "experience": 0
                }
    		 }
}
```



## DANGEROUS 

## ========   add\_supplies   ========

Documentation needed. Author: HouYao

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
				"remaining" :
                {
                    "supply": 0
                }
			 }
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
- 98 - database operating error
- 99 - Parameter error


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

##### Sample Response1
```json
{
	"status" : "0",
	"message": "success",
	"data" : {
				"remaining":
                {
					"iron": 5235, 
                    "coin": 2541, 
                    "hang_stage": 0, 
                    "hang_up_time": "2019-07-31 17:33:37"
                }
        	}
}
```

##### Sample Response2

```json
{
	"status" : "0",
	"message": "success",
	"data" : {
        		"remaining": 
        		{
                    "iron": 5545, 
                    "coin": 3471, 
                    "hang_stage": 2, 
                    "hang_up_time": "2019-07-31 17:40:03"
                }, 
        		"reward": 
        		{
                    "iron": 300, 
                    "coin": 900,
                    "hang_stage": 1, 
                    "hang_up_time": "2019-07-31 17:10:03"
                }
        	}
}
```

## 



## ========   get\_hang\_up\_reward   ========

Documentation needed. Author: HouYao


Status codes and meaning:

- 0 - Settlement reward success
- 99 - Temporarily no on-hook record


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
        		"remaining": 
        		{
                    "iron": 5545, 
                    "coin": 3471, 
                    "hang_stage": 2, 
                    "hang_up_time": "2019-07-31 17:40:03"
                }, 
        		"reward": 
        		{
                    "iron": 300, 
                    "coin": 900,
                    "hang_stage": 2, 
                    "hang_up_time": "2019-07-31 17:10:03"
                }
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



