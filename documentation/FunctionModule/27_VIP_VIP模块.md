## 方法列表

* [`get_config_vip`](##get_config_vip)
* [`get_vip_daily_reward`](##get_vip_daily_reward)
* [`get_info_vip`](##get_info_vip)

- 后面的方法尚未完成

* 内部方法[`get_vip_card`](##get_vip_card)
* 内部方法[`increase_vip_exp`](##increase_vip_exp)
* 内部方法[`check_vip_daily_reward`](##check_vip_daily_reward)

## get_config_vip

获取的配置文件，同时会直接结算玩家的vip奖励，结算奖励调用check_vip_daily_reward

##### 发送消息JSON格式

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

[成功]()

> config：vip的配置文件
>

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"config": {
			"vip_level": {
				"experience": [
					60,
					300,
					940,
					1300,
					2000,
					2900,
					6500,
					11000,
					25000,
					50000,
					100000,
					300000,
					500000,
					1000000
				]
			},
			"vip_daily_reward": {
				"cooling_time": 86400,
				"1": {
					"1": 0,
					"20": 0,
					"21": 0,
					"22": 0,
					"23": 10,
					"25": 0
				},
				"2": {
					"1": 10000,
					"20": 0,
					"21": 0,
					"22": 0,
					"23": 20,
					"25": 0
				},
				"3": {
					"1": 10000,
					"20": 0,
					"21": 0,
					"22": 0,
					"23": 30,
					"25": 0
				},
				"4": {
					"1": 10000,
					"20": 0,
					"21": 0,
					"22": 0,
					"23": 40,
					"25": 1
				},
				"5": {
					"1": 10000,
					"20": 0,
					"21": 0,
					"22": 0,
					"23": 50,
					"25": 1
				},
				"6": {
					"1": 10000,
					"20": 10000,
					"21": 0,
					"22": 0,
					"23": 60,
					"25": 1
				},
				"7": {
					"1": 10000,
					"20": 10000,
					"21": 0,
					"22": 0,
					"23": 70,
					"25": 1
				},
				"8": {
					"1": 20000,
					"20": 10000,
					"21": 1000,
					"22": 0,
					"23": 80,
					"25": 1
				},
				"9": {
					"1": 20000,
					"20": 10000,
					"21": 1000,
					"22": 0,
					"23": 90,
					"25": 2
				},
				"10": {
					"1": 20000,
					"20": 20000,
					"21": 1000,
					"22": 0,
					"23": 100,
					"25": 2
				},
				"11": {
					"1": 20000,
					"20": 20000,
					"21": 2000,
					"22": 100,
					"23": 110,
					"25": 2
				},
				"12": {
					"1": 20000,
					"20": 20000,
					"21": 2000,
					"22": 200,
					"23": 120,
					"25": 2
				},
				"13": {
					"1": 20000,
					"20": 20000,
					"21": 2000,
					"22": 200,
					"23": 130,
					"25": 3
				},
				"14": {
					"1": 20000,
					"20": 30000,
					"21": 3000,
					"22": 300,
					"23": 140,
					"25": 3
				}
			},
			"vip_special_package": {
				"0": {
					"package": [
						"3:10:2"
					],
					"cast_diamond": 100
				},
				"1": {
					"package": [
						"3:10:4",
						"3:29:20"
					],
					"cast_diamond": 300
				},
				"2": {
					"package": [
						"3:10:6",
						"3:29:30",
						"3:30:30"
					],
					"cast_diamond": 500
				},
				"3": {
					"package": [
						"3:10:8",
						"3:29:40",
						"3:30:40"
					],
					"cast_diamond": 700
				},
				"4": {
					"package": [
						"3:10:10",
						"3:29:50",
						"3:30:50"
					],
					"cast_diamond": 900
				},
				"5": {
					"package": [
						"3:10:12",
						"3:29:60",
						"3:30:60"
					],
					"cast_diamond": 1100
				},
				"6": {
					"package": [
						"3:10:14",
						"3:29:70",
						"3:30:70",
						"3:31:20"
					],
					"cast_diamond": 1300
				},
				"7": {
					"package": [
						"3:10:16",
						"3:29:80",
						"3:30:80",
						"3:31:30",
						"3:32:30"
					],
					"cast_diamond": 1500
				},
				"8": {
					"package": [
						"3:10:18",
						"3:29:90",
						"3:30:90",
						"3:31:40",
						"3:32:40"
					],
					"cast_diamond": 1700
				},
				"9": {
					"package": [
						"3:10:20",
						"3:29:100",
						"3:30:100",
						"3:31:50",
						"3:32:50"
					],
					"cast_diamond": 1900
				},
				"10": {
					"package": [
						"3:10:22",
						"3:29:110",
						"3:30:110",
						"3:31:60",
						"3:32:60"
					],
					"cast_diamond": 2100
				},
				"11": {
					"package": [
						"3:10:24",
						"3:29:120",
						"3:30:120",
						"3:31:70",
						"3:32:70"
					],
					"cast_diamond": 2300
				},
				"12": {
					"package": [
						"3:10:26",
						"3:29:130",
						"3:30:130",
						"3:31:80",
						"3:32:80"
					],
					"cast_diamond": 2500
				},
				"13": {
					"package": [
						"3:10:28",
						"3:29:140",
						"3:30:140",
						"3:31:90",
						"3:32:90"
					],
					"cast_diamond": 2700
				},
				"14": {
					"package": [
						"3:10:30",
						"3:29:150",
						"3:30:150",
						"3:31:100",
						"3:32:100"
					],
					"cast_diamond": 3000
				}
			},
			"buy_energy_config": {
				"default": 2,
				"vip": [
					3,
					3,
					3,
					4,
					4,
					4,
					5,
					5,
					5,
					6,
					6,
					6,
					6,
					6
				]
			},
			"world_boss_challenge_times": {
				"default": 1,
				"vip": [
					1,
					1,
					1,
					1,
					1,
					1,
					1,
					1,
					1,
					1,
					1,
					1,
					2,
					3
				]
			},
			"card_increase_experience": {
				"min": 10,
				"max": 15,
				"permanent": 20
			}
		}
	}
}
```



## get_vip_daily_reward

##### 发送消息JSON格式

领取VIP今日奖励

```json
{
	"world": 0, 
	"function": "get_vip_daily_reward",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

[成功]()

购买月卡有小月卡、大月卡、永久卡（期限分别是31天、31天、永久），每日VIP奖励根据VIP等级获取，不会根据月卡类型而变化，月卡类型加经验不同（分别是10点、15点、20点），每种月卡只可以购买一张，购买一种月卡只获得一倍的奖励，两种则两倍，三种则三倍，VIP经验获得可叠加，通过此方法可以获得VIP经验，奖励属于获得经验后的VIP等级奖品。

> remaining：剩余物资
>
> - min_card：小月卡信息
>   - card：月卡是否失效
>   - item：物品剩余情况
> - max_card：大月卡信息
>   - card：月卡是否失效
>   - item：物品剩余情况
> - perpetual_card：永久月卡信息
>   - card：月卡是否失效
>   - item：物品剩余情况
> - exp_info：经验信息
>   - exp：总经验
>   - level：VIP等级
>   - need：升级需要经验
>
> reward：奖励信息
>
> - min_card：小月卡信息
>   - item：物品变化量信息
> - max_card：大月卡信息
>   - item：物品变化量信息
> - perpetual_card：永久月卡信息
>   - item：物品变化量信息

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"remaining": {
			"min_card": {
				"card": "True",
				"item": [
					{
						"iid": "1",
						"value": 205352
					},
					{
						"iid": "20",
						"value": 0
					},
					{
						"iid": "21",
						"value": 0
					},
					{
						"iid": "22",
						"value": 0
					},
					{
						"iid": "23",
						"value": 10
					},
					{
						"iid": "25",
						"value": 500
					}
				]
			},
			"max_card": {
				"card": "True",
				"item": [
					{
						"iid": "1",
						"value": 205352
					},
					{
						"iid": "20",
						"value": 0
					},
					{
						"iid": "21",
						"value": 0
					},
					{
						"iid": "22",
						"value": 0
					},
					{
						"iid": "23",
						"value": 20
					},
					{
						"iid": "25",
						"value": 500
					}
				]
			},
			"perpetual_card": {
				"card": "False"
			},
			"exp_info": {
				"exp": 105,
				"level": 1,
				"need": 195
			}
		},
		"reward": {
			"min_card": {
				"item": [
					{
						"iid": "1",
						"value": 0
					},
					{
						"iid": "20",
						"value": 0
					},
					{
						"iid": "21",
						"value": 0
					},
					{
						"iid": "22",
						"value": 0
					},
					{
						"iid": "23",
						"value": 10
					},
					{
						"iid": "25",
						"value": 0
					}
				]
			},
			"max_card": {
				"item": [
					{
						"iid": "1",
						"value": 0
					},
					{
						"iid": "20",
						"value": 0
					},
					{
						"iid": "21",
						"value": 0
					},
					{
						"iid": "22",
						"value": 0
					},
					{
						"iid": "23",
						"value": 10
					},
					{
						"iid": "25",
						"value": 0
					}
				]
			},
			"perpetual_card": {}
		}
	}
}
```

[失败]()

* 99: You're not a VIP（你不是VIP）
* 98: The cooling time is not over（你的冷却时间未结束）



## get_info_vip

##### 发送消息JSON格式

获取VIP信息

```json
{
	"world": 0, 
	"function": "get_vip_card",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

[获取资源成功]()

> exp_info: VIP经验信息
>
> min_card：小月卡是否失效
>
> max_card：大月卡是否失效
>
> perpetual_card：永久月卡是否失效
>
> min_seconds：小月卡过期剩余时间
>
> max_seconds：大月卡过期剩余时间

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"exp_info": {
			"exp": 105,
			"level": 1,
			"need": 195
		},
		"min_card": "True",
		"max_card": "True",
		"min_seconds": 2671833,
		"max_seconds": 2671936,
		"perpetual_card": "False"
	}
}
```



## get_vip_card

##### 发送消息JSON格式

获得vip经验卡，因为是内部方法，调用即可直接获得，如果重复获得，则会添加日期，比如多添加一个月，购买之后会记录vip卡的购买时间和过期时间

```json
{
	"world": 0, 
	"function": "get_vip_card",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

[获取资源成功]()

> expired_time: 过期时间，数字为到期的秒数
>

```json
{
	"status": 0,
	"message": "Successful signing",
	"data": {
		"expired_time": 25098397
		}
}
```

[调整关卡失败]()

* 99: 钻石不足
* 98: 没有一天漏掉，无法补钱





## increase_vip_exp

##### 发送消息JSON格式

执行之后直接添加vip的经验值

```json
{
	"world": 0, 
	"function": "increase_vip_exp",
	"data": {
		"token": "my toekn ^_^",
    "exp":222
	}
}
```

##### 接受消息JSON格式

[成功]()

> remaning: 剩余经验
>
> reward：获得经验

```json
{
	"status": 0,
	"message": "Successful signing",
	"data": {
    "remaning":{"exp":50000},
    "reward":{"exp":222}
	}
}
```



## get_vip_package

##### 发送消息JSON格式

用钻石获得vip礼包，玩家传入需要购买的vip礼包id即可计算礼包的数据

> pid: 给予礼包的id

```json
{
	"world": 0, 
	"function": "get_vip_package",
	"data": {
		"token": "my toekn ^_^",
    "pid": 1   
	}
}
```

##### 接受消息JSON格式

[获取资源成功]()

> cost: 表示消耗的钻石数量，消耗的内容固定为钻石，数量可变
>
> supplement：数字1，2，3，4表示补签的日期，内部则表示获得的物品与拥有的物品

```json
{
	"status": 0,
	"message": "Successful signing",
	"data": {
		"package": {
			"iid":2,
      "value":10
		},
		"remaining": {
			"diamond": 298080
		},
		"reward": {
			"diamond": 480
		}
	}
}
```

[调整关卡失败]()

* 99: 钻石不足



## check_vip_daily_reward

##### 发送消息JSON格式

补签功能，把之前没有签到的天数用钻石进行补签，`补钱一天`消耗的钻石数量在配置表`check_in.json`

```json
{
	"world": 0, 
	"function": "check_vip_daily_reward",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

[获取资源成功]()

> cost: 表示消耗的钻石数量，消耗的内容固定为钻石，数量可变
>
> supplement：数字1，2，3，4表示补签的日期，内部则表示获得的物品与拥有的物品

```json
{
	"status": 0,
	"message": "Successful signing",
	"data": {
		"supplement": {
			"1": {
				"remaining": [
					"3:18:5"
				],
				"reward": [
					"3:18:1"
				]
			},
			"2": {
				"remaining": [
					"3:5:298180"
				],
				"reward": [
					"3:5:100"
				]
			},
			"3": {
				"remaining": [
					"3:9:2006"
				],
				"reward": [
					"3:9:100"
				]
			},
			"4": {
				"remaining": [
					"3:25:400"
				],
				"reward": [
					"3:25:100"
				]
			},
			"5": {
				"remaining": [
					"2:1:20"
				],
				"reward": [
					"2:1:5"
				]
			}
		},
		"remaining": {
			"diamond": 298080
		},
		"reward": {
			"diamond": 480
		}
	}
}
```

[调整关卡失败]()

* 99: 钻石不足
* 98: 没有一天漏掉，无法补钱

