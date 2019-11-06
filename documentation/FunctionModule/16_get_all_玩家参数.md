## 方法列表

* [`get_config_stage`](##get_config_stage)
* [`get_config_lottery`](##get_config_lottery)
* [`get_config_weapon`](##get_config_weapon)
* [`get_config_skill`](##get_config_skill)
* [`get_config_mall`](##get_config_mall)
* [`get_config_role`](##get_config_role)
* [`get_config_task`](##get_config_task)
* [`get_config_achievement`](##get_config_achievement)
* [`get_config_check_in`](##get_config_check_in)
* [`get_config_vip`](##get_config_vip)
* [`get_config_player`](##get_config_player)
* [`get_config_factory`](##get_config_factory)

## get_config_stage

##### 发送消息JSON格式

获取关卡的消耗列表与关卡的奖励列表entry_consumables_config.json,stage_reward_config.json 关卡 hang_reward_config.json挂机信息

> 无
>

```json
{
	"world": 0,
	"function": "get_config_stage",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[成功]()

> entry_consumables_config：返回entry_consumables_config.json
>
> stage_reward_config：返回stage_reward_config.json
>
> hang_reward_config: 返回hang_reward_config.json

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"entry_consumables_config": {
			"0": {
				"2": 0,
				"1": 0,
				"cost": 0
			},
			"1": {
				"2": 0,
				"1": 0,
				"cost": 1
			},
			"2": {
				"2": 0,
				"1": 0,
				"cost": 1
			},
			"3": {
				"2": 0,
				"1": 0,
				"cost": 1
			},
			"4": {
				"2": 0,
				"1": 0,
				"cost": 1
			},
			"5": {
				"2": 0,
				"1": 0,
				"cost": 1
			},
			"6": {
				"2": 0,
				"1": 0,
				"cost": 1
			},
			"7": {
				"2": 0,
				"1": 0,
				"cost": 1
			},
			"8": {
				"2": 0,
				"1": 0,
				"cost": 1
			},
			"1001": {
				"1": 3,
				"cost": 2
			},
			"1002": {
				"1": 3,
				"cost": 2
			},
			"1003": {
				"1": 3,
				"cost": 2
			},
			"1004": {
				"2": 210,
				"1": 220,
				"cost": 2
			},
			"1005": {
				"2": 250,
				"1": 220,
				"cost": 2
			},
			"1006": {
				"2": 3,
				"cost": 2
			}
		},
		"stage_reward_config": {
			"1": {
				"10": 1,
				"exp": 10
			},
			"2": {
				"9": 125,
				"exp": 10,
				"2": 125,
				"1": 375,
				"10": 1
			},
			"3": {
				"9": 150,
				"exp": 10,
				"2": 150,
				"1": 450,
				"10": 1
			},
			"4": {
				"9": 175,
				"exp": 10,
				"2": 175,
				"1": 525,
				"10": 1
			},
			"5": {
				"9": 200,
				"exp": 10,
				"2": 200,
				"1": 600,
				"10": 1
			},
			"6": {
				"9": 225,
				"exp": 10,
				"2": 225,
				"1": 675,
				"10": 1
			},
			"7": {
				"9": 250,
				"exp": 10,
				"2": 250,
				"1": 750,
				"10": 1
			},
			"8": {
				"9": 275,
				"exp": 10,
				"2": 275,
				"1": 825,
				"10": 1
			},
			"1001": {
				"2": 210,
				"1": 220,
				"exp": 220
			},
			"1002": {
				"2": 250,
				"1": 220,
				"9": 3
			},
			"1003": {
				"2": 310,
				"1": 220,
				"9": 3
			},
			"1004": {
				"2": 310,
				"1": 220,
				"9": 3
			},
			"1005": {
				"2": 310,
				"1": 220,
				"9": 3
			},
			"1006": {
				"2": 310,
				"1": 220,
				"9": 3
			},
			"1007": {
				"2": 310,
				"1": 220,
				"9": 3
			},
			"1008": {
				"2": 310,
				"1": 220,
				"9": 3
			},
			"1009": {
				"2": 310,
				"1": 220,
				"9": 3
			},
			"1010": [
				"skill_M0",
				"skill_P0",
				"skill_G0"
			],
			"1020": [
				"weapon1",
				"weapon2",
				"weapon3"
			],
			"1030": [
				"weapon4",
				"weapon5",
				"weapon6",
				"weapon7"
			],
			"1040": [
				"skill_M0",
				"skill_M1",
				"skill_M2",
				"skill_P0",
				"skill_P1",
				"skill_P2",
				"skill_G0",
				"skill_G1",
				"skill_G2"
			],
			"1050": [
				"weapon8",
				"weapon9",
				"weapon10"
			],
			"1060": [
				"skill_M3",
				"skill_M4",
				"skill_M5",
				"skill_M6",
				"skill_M7",
				"skill_M8",
				"skill_M9",
				"skill_M10",
				"skill_M11",
				"skill_M12"
			],
			"1070": [
				"weapon11",
				"weapon12",
				"weapon13",
				"weapon14",
				"weapon15",
				"weapon16",
				"weapon17",
				"weapon18",
				"weapon19",
				"weapon20"
			],
			"1080": [
				"skill_P3",
				"skill_P4",
				"skill_P5",
				"skill_P6",
				"skill_P7",
				"skill_P8",
				"skill_P9",
				"skill_P10",
				"skill_P11",
				"skill_P12"
			],
			"1090": [
				"weapon21",
				"weapon22",
				"weapon23",
				"weapon24",
				"weapon25",
				"weapon26",
				"weapon27",
				"weapon28",
				"weapon29",
				"weapon30"
			],
			"1100": [
				"weapon31",
				"weapon32",
				"weapon33",
				"weapon34",
				"weapon35",
				"weapon36",
				"weapon37",
				"weapon38",
				"weapon39",
				"weapon40",
				"skill_G0",
				"skill_G1",
				"skill_G2",
				"skill_G3",
				"skill_G4",
				"skill_G5",
				"skill_G6",
				"skill_G7",
				"skill_G8",
				"skill_G9",
				"skill_G10",
				"skill_G11",
				"skill_G12"
			],
			"skill_MPG": {
				"M": 0,
				"P": 13,
				"G": 26
			},
			"skill": [
				"skill_M0",
				"skill_M1",
				"skill_M2",
				"skill_M3",
				"skill_M4",
				"skill_M5",
				"skill_M6",
				"skill_M7",
				"skill_M8",
				"skill_M9",
				"skill_M10",
				"skill_M11",
				"skill_M12",
				"skill_P0",
				"skill_P1",
				"skill_P2",
				"skill_P3",
				"skill_P4",
				"skill_P5",
				"skill_P6",
				"skill_P7",
				"skill_P8",
				"skill_P9",
				"skill_P10",
				"skill_P11",
				"skill_P12",
				"skill_G0",
				"skill_G1",
				"skill_G2",
				"skill_G3",
				"skill_G4",
				"skill_G5",
				"skill_G6",
				"skill_G7",
				"skill_G8",
				"skill_G9",
				"skill_G10",
				"skill_G11",
				"skill_G12"
			],
			"weapon": [
				"weapon1",
				"weapon2",
				"weapon3",
				"weapon4",
				"weapon5",
				"weapon6",
				"weapon7",
				"weapon8",
				"weapon9",
				"weapon10",
				"weapon11",
				"weapon12",
				"weapon13",
				"weapon14",
				"weapon15",
				"weapon16",
				"weapon17",
				"weapon18",
				"weapon19",
				"weapon20",
				"weapon21",
				"weapon22",
				"weapon23",
				"weapon24",
				"weapon25",
				"weapon26",
				"weapon27",
				"weapon28",
				"weapon29",
				"weapon30",
				"weapon31",
				"weapon32",
				"weapon33",
				"weapon34",
				"weapon35",
				"weapon36",
				"weapon37",
				"weapon38",
				"weapon39",
				"weapon40"
			],
			"skill_scroll": [
				6,
				7,
				8
			],
			"scroll_range": [
				1,
				10
			],
			"weights": [
				0.5,
				0.3,
				0.2
			],
			"segment_range": [
				30,
				60
			]
		},
		"hang_reward_config": {
			"0": {
				"2": 0,
				"1": 0
			},
			"1": {
				"2": 10,
				"1": 30,
				"11": [
					1,
					12,
					100
				]
			},
			"2": {
				"2": 20,
				"1": 60,
				"11": [
					1,
					100,
					1000
				]
			},
			"3": {
				"2": 30,
				"1": 90
			},
			"4": {
				"2": 40,
				"1": 120
			},
			"5": {
				"2": 50,
				"1": 150
			},
			"6": {
				"2": 60,
				"1": 180
			},
			"7": {
				"2": 70,
				"1": 210
			},
			"8": {
				"2": 80,
				"1": 240
			},
			"probability_reward": [
				"11",
				"12",
				"13",
				"6",
				"7",
				"8"
			]
		}
	}
}
```

## get_config_lottery

获取lottery.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_lottery",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回转盘和抽奖的消耗信息，配置文件来自lottery.json

[成功]()

> lottery：返回lottery.json

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"config": {
			"skills": {
				"3:1": 100,
				"3:5": 100,
				"3:11": 1,
				"3:16": 10,
				"3:13": 1,
				"3:12": 1
			},
			"weapons": {
				"3:1": 100,
				"3:5": 100,
				"3:11": 1,
				"3:16": 10,
				"3:13": 1,
				"3:12": 1
			},
			"roles": {
				"3:1": 100,
				"3:5": 100,
				"3:11": 1,
				"3:16": 10,
				"3:13": 1,
				"3:12": 1
			},
			"fortune_wheel": {
				"3:1": 100,
				"3:5": 100,
				"3:11": 1,
				"3:16": 10,
				"3:13": 1,
				"3:12": 1
			}
		}
	}
}
```



## get_config_weapon

获取weapon_config.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_weapon",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回转盘和抽奖的消耗信息，配置文件来自weapon_config.json

[成功]()

> weapon_config：返回weapon_config.json

```json
{
	"status": 0,
	"message": "unlucky",
	"data": {
		"weapon_config": {....}
	}
}
```



##get_config_skill

获取skill_level_up_config.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_weapon",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回转盘和抽奖的消耗信息，配置文件来自skill_level_up_config.json

[成功]()

> skill_level_up_config：返回skill_level_up_config.json

```json
{
	"status": 0,
	"message": "unlucky",
	"data": {
		"skill_level_up_config": {....}
	}
}
```





##get_config_mall

获取mall_config.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_mall",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回转盘和抽奖的消耗信息，配置文件来自mall_config.json

[成功]()

> skill_level_up_config：返回skill_level_up_config.json

```json
{
	"status": 0,
	"message": "unlucky",
	"data": {
		"mall_config": {....}
	}
}
```



##get_config_role

获取role_config.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_role",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回转盘和抽奖的消耗信息，配置文件来自role_config.json

[成功]()

> role_config：返回role_config.json

```json
{
	"status": 0,
	"message": "unlucky",
	"data": {
		"role_config": {....}
	}
}
```



##get_config_task

获取task.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_task",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回转盘和抽奖的消耗信息，配置文件来自task.json

[成功]()

> task：返回task.json

```json
{
	"status": 0,
	"message": "unlucky",
	"data": {
		"task": {....}
	}
}
```





##get_config_achievement

获取achievement_config.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_achievement",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回转盘和抽奖的消耗信息，配置文件来自achievement_config.json

[成功]()

> achievement_config：返回achievement_config.json

```json
{
	"status": 0,
	"message": "unlucky",
	"data": {
		"achievement_config": {....}
	}
}
```





##get_config_check_in

获取check_in.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_check_in",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回转盘和抽奖的消耗信息，配置文件来自check_in.json

[成功]()

> check_in：返回check_in.json

```json
{
	"status": 0,
	"message": "unlucky",
	"data": {
		"check_in": {....}
	}
}
```



##get_config_vip

获取vip_config.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_vip",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回转盘和抽奖的消耗信息，配置文件来自vip_config.json

[成功]()

> vip_config：返回vip_config.json

```json
{
	"status": 0,
	"message": "unlucky",
	"data": {
		"vip_config": {....}
	}
}
```



## get_config_player

获取player_config.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_player",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回转盘和抽奖的消耗信息，配置文件来自player_config.json

[成功]()

> player_config：返回player_config.json

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"player_config": {....},
    	"energy": {
			"time": "0:20:00",
			"max_energy": 10
		},
        "exp_info": {
            "exp": 790,
            "level": 9,
            "need": 50
        },
    	"diamond":500,
    	"coin":100
	}
}
```



## get_config_factory

获取get_factory_config.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_factory",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回转盘和抽奖的消耗信息，配置文件来自get_factory_config.json

[成功]()

> get_factory_config：返回get_factory_config.json

```json
{
	"status": 0,
	"message": "unlucky",
	"data": {
		"get_factory_config": {....}
	}
}
```

