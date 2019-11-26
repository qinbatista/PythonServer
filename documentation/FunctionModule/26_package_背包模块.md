## 方法列表

* [`exchange_card`](##_exchange_card)

- [`get_config_card`](##get_config_card)

## exchange_card

卡片交换，公式为角色当前等级×卡片交换的基础数量（base num=>bnum），详见配置表`package.json`

##### 发送消息JSON格式

> card_id：卡片id（属于item枚举，范围18-23）

```json
{
	"world": 0, 
	"function": "exchange_card",
	"data": {
		"token": "my toekn ^_^",
        "card_id": 18
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



## get_config_card

返回卡片兑换的配置信息，详见配置表`package.json`

##### 发送消息JSON格式

```json
{
	"world": 0, 
	"function": "get_config_card",
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

```
{
	"status": 0,
	"message": "success",
	"data": {
		"config": {
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
		}
	}
}
```

