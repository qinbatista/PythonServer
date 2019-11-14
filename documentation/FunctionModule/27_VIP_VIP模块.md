## 方法列表

* [`get_config_vip`](##get_config_vip)
* [`get_vip_daily_reward`](##get_vip_daily_reward)
* [`get_info_vip`](##get_info_vip)
* [`purchase_vip_gift`](##purchase_vip_gift)

- [`purchase_vip_card`](##purchase_vip_card)
- 内部方法[`check_card`](##check_card)

* 内部方法[`increase_exp`](##increase_exp)

* 内部方法[`increase_item`](##increase_item)

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
	"function": "get_info_vip",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

[成功]()

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
>
> cooling_time：VIP礼包领取后剩余的冷却时间

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
		"perpetual_card": "False",
        "cooling_time": 85160
	}
}
```



## purchase_vip_gift

##### 发送消息JSON格式

购买VIP特殊礼包

> tier：购买VIP礼包的层数，根据VIP等级计算（tier==VIP level）

```json
{
	"world": 0, 
	"function": "get_vip_card",
	"data": {
		"token": "my toekn ^_^",
        "tier": 1
	}
}
```

##### 接受消息JSON格式

[成功]()

> remaining：剩余物资
>
> - diamond：钻石剩余数量
> - gifts：物品剩余列表
>   - gid：组id
>   - mid：物品id
>   - qty：物品数量quantity
>
> reward：改变物资
>
> - diamond：钻石消耗数量
> - gifts：物品增加列表
>   - gid：组id
>   - mid：物品id
>   - qty：物品数量quantity
>
> exp_info：VIP经验信息
>
> - exp：VIP总经验
> - level：VIP等级
> - need：升到下一级需要经验

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"remaining": {
			"diamond": 198400,
			"gifts": [
				{
					"gid": 3,
					"mid": 10,
					"qty": 16
				},
				{
					"gid": 3,
					"mid": 29,
					"qty": 20
				}
			]
		},
		"reward": {
			"diamond": -300,
			"gifts": [
				{
					"gid": 3,
					"mid": 10,
					"qty": 4
				},
				{
					"gid": 3,
					"mid": 29,
					"qty": 20
				}
			]
		},
		"exp_info": {
			"exp": 130,
			"level": 1,
			"need": 170
		}
	}
}
```

[失败]()

* 98: Diamond insufficient（钻石不足）
* 99: You don't have enough VIP status（VIP等级不够，无法购买那一层的礼包）



## purchase_vip_card

##### 发送消息JSON格式

购买VIP卡（暂时无消耗，直接获得VIP月卡），购买之后会记录vip卡的过期时间，没有过期时无法再次购买

```json
{
	"world": 0, 
	"function": "purchase_vip_card",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

[成功]()

> cooling_time: 过期时间，数字为到期的秒数
>
> card_id：月卡id

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"cooling_time": 2678400,
		"card_id": 27
	}
}
```

[失败]()

* 99: card id error（卡id错误）
* 98: VIP card has not expired（VIP卡未过期）



## check_card

检查月卡等级，返回是否存在VIP月卡，月卡等级信息

##### 发送消息JSON格式

```python
await check_card(uid, **kwargs)
```

##### 接受消息JSON格式

```python
min_card, max_card, perpetual_card = True, True, True
```



## increase_exp

##### 发送消息JSON格式

增加VIP经验exp为0则获得经验，反之取绝对值增加经验，并返回总经验和等级，升到下一级需要的经验

```python
await increase_exp(uid, exp, **kwargs)
```

##### 接受消息JSON格式

[成功]()

> exp: VIP总经验
>
> level：VIP等级
>
> need：升到下一级需要经验

```json
{
    "exp": 130,
    "level": 1,
    "need": 170
}
```



## increase_item

##### 发送消息JSON格式

增加物品

> uid：用户id
>
> config：对应等级下的物品奖励信息

```python
await increase_item(uid, config, **kwargs)
```

##### 接受消息JSON格式

```python
remaining, reward = [], []
```

