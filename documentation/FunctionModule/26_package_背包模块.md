## 方法列表

* [`exchange_card`](##_exchange_card)
* [`use_item`](##use_item)

- [`get_config_exchange`](##get_config_exchange)

## exchange_card

卡片交换，公式为角色当前等级×卡片交换的基础数量（base num=>bnum），详见配置表`package.json`

##### 发送消息JSON格式

> card_id：卡片id（属于item枚举，范围18-23）
>
> qty：兑换的卡片数

```json
{
	"world": 0, 
	"function": "exchange_card",
	"data": {
		"token": "my toekn ^_^",
        "card_id": 18,
        "qty": 1
	}
}
```

##### 接受消息JSON格式

[成功]()

> remaining：剩余量
>
> - sql_table：操作的数据库表名
> - mid：物品id
> - mnum：物品剩余数量
> - cid：卡片id（card id）存在item表中
> - cnum：卡片剩余数量
>
> reward：变化量
>
> - sql_table：操作的数据库表名
> - mid：物品id
> - mnum：物品增加数量
> - cid：卡片id（card id）存在item表中
> - cnum：卡片消耗数量
>
> exp_info：经验信息
>
> - exp：目前的经验
> - level：目前的等级
> - need：升到下级需要的经验

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"remaining": {
			"sql_table": "item",
			"mid": 1,
			"mnum": 204784,
			"cid": 18,
			"cnum": 1
		},
		"reward": {
			"sql_table": "item",
			"mid": 1,
			"mnum": 2000,
			"cid": 18,
			"cnum": -1
		},
		"exp_info": {
			"exp": 40,
			"level": 1,
			"need": 20
		}
	}
}
```

[失败]()

* 99：物品id错误
* 98：卡片id错误
* 97：配置表中数据库表名设置错误
* 96：数量只能为正数
* 95：卡片数量不足



## use_item

##### 发送消息json格式

> item_id：兑换的消耗品格式为  组id:物品id:数量（这里的组id都是3，暂时没有其他组，数量暂时不会用，传多少过来都只是解析组id和物品id）
>
> exchange_id：兑换的成品格式为  组id:物品id:数量（这个参数可以随着item_id变换，如果兑换的消耗品为万能碎片则需要传这个参数，否则传不传都不会解析这个参数，是万能碎片必须传组id是角色还是武器，并且指定对应星数的武器或者角色才能兑换成功，这里的数量也不会做解析，所以是暂时留下占位的）（item_id指定万能碎片时exchange_id为【[0,2]:4[0-2]:\d+】）
>
> - 非万能碎片兑换的发送json格式
```json
{
	"world": 0,
	"function": "use_item",
	"data": {
		"token": "token",
		"item_id": "3:38:1",
		"exchange_id": ""
	}
}
```

>- 万能碎片兑换的发送json格式

```
{
	"world": 0,
	"function": "use_item",
	"data": {
		"token": "token",
		"item_id": "3:41:1",
		"exchange_id": "2:21:1"
	}
}
```



##### 接收消息json格式

>remaining：剩余物品
>
>reward：改变的物品
>
- 兑换体力药水的接收json格式
```json
{
	"status": 0,
	"message": "success",
	"data": {
		"remaining": {
			"item": "3:33:8",
			"energy": 1100,
			"cooling_time": -1
		},
		"reward": {
			"item": "3:33:-1",
			"energy": 50
		}
	}
}
```
- 武器碎片兑换的接收json格式（角色返回格式相同，status为2时为角色）
```json
{
	"status": 1,
	"message": "success",
	"data": {
		"remaining": {
			"item": "3:38:96",
			"eitem": "0:18:561"
		},
		"reward": {
			"item": "3:38:-1",
			"eitem": "0:18:20"
		}
	}
}
```
- 万能碎片兑换的接收json格式

```json
{
	"status": 3,
	"message": "success",
	"data": {
		"remaining": {
			"item": "3:41:98",
			"eitem": "2:21:320"
		},
		"reward": {
			"item": "3:41:-1",
			"eitem": "2:21:20"
		}
	}
}
```
- 卷轴升级的接收json格式

```json
{
    "status": 3,
    "message": "success",
    "data": {
        "remaining": {
            "item": "3:6:922",
            "eitem": "3:7:23"
        },
        "reward": {
            "item": "3:6:-12",
            "eitem": "3:7:4"
        }
    }
}
```

- 99：意外消耗品iid
- 98：兑换成品类型错误
- 97：兑换碎片类型不匹配
- 96：兑换消耗品不足



## get_config_exchange

返回卡片兑换的配置信息，详见配置表`package.json`

##### 发送消息JSON格式

```json
{
	"world": 0, 
	"function": "get_config_exchange",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

[成功]()

> config：卡片兑换配置信息
>
> - sqltable：操作的数据库表
> - mid：物品id
> - bnum：卡片交换获得的物品基础数量（base num=>bnum）
>
> exchange_item：兑换其他物品配置信息

```
{
	"status": 0,
	"message": "success",
	"data": {
		"config": {
			"exchange_card": {
				"COIN_CARD": {
					"sqltable": "item",
					"mid": 1,
					"bnum": 2000
				},
				"EXP_CARD": {
					"sqltable": "progress",
					"mid": "exp",
					"bnum": 1000
				},
				"FOOD_CARD": {
					"sqltable": "item",
					"mid": 3,
					"bnum": 200
				},
				"MINE_CARD": {
					"sqltable": "item",
					"mid": 24,
					"bnum": 100
				},
				"CRYSTAL_CARD": {
					"sqltable": "item",
					"mid": 4,
					"bnum": 20
				},
				"DIAMOND_CARD": {
					"sqltable": "item",
					"mid": 5,
					"bnum": 10
				}
			},
			"exchange_item": {
				"energy_potion_s_min": 50,
				"energy_potion_s_max": 100,
				"role4_universal_segment": 30,
				"role5_universal_segment": 15,
				"weapon4_universal_segment": 20,
				"weapon5_universal_segment": 10,
				"universal4_segment": 30,
				"universal5_segment": 20,
				"universal6_segment": 10
			}
		}
	}
}
```

