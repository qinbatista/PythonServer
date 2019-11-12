## 方法列表

* [`get_all_market`](##get_all_market)
* [`refresh_market`](##refresh_market)
* [`darkmarket_transaction`](##darkmarket_transaction)

## get_all_market

##### 发送消息json格式


```json
{
	"world": 0,
	"function": "get_all_market",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息json格式

[抽取成功]()

> dark_markets：黑市物品信息，`pid`商品位置信息，`gid`物品类别id，`mid`此类物品的商品id，`qty`商品数量，`cid`交换货物的id，`amt`交换货物数量
>
> refresh_time: 免费刷新的倒计时，标准时间为3小时自动刷新一次 The number of seconds remaining until the next refresh
>
> refreshable：剩余免费的刷新次数，一天免费可以刷新3次
>
> config：配置信息
>
> - diamond：钻石刷新需要消耗的钻石数量

```json
{
	"status": 1,
	"message": "Get all black market information",
	"data": {
		"dark_markets": [
			{
				"pid": 0,
				"gid": 0,
				"mid": 2,
				"qty": 5,
				"cid": 1,
				"amt": 675
			},
            ...
			{
				"pid": 1,
				"gid": 1,
				"mid": 30,
				"qty": 1,
				"cid": 5,
				"amt": 61
			}
		],
		"refresh_time": 3058,
		"refreshable": 3,
		"config": {
			"refresh_diamond": 100
		}
	}
}
```



## refresh_market

##### 发送消息json格式

> 获取黑市的配置信息，只需要获得免费刷新的时间，手动刷新的钻石，免费刷新次数和物品信息等，参数来源`player_config.json`，产生的物品为9个（目前是8个），标准未来可以更改。此方法包含免费刷新与钻石刷新，判断条件根据程序内部判断

```json
{
	"world": 0,
	"function": "basic_summon",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息json格式

[抽取成功]()

> dark_markets：黑市物品信息，`pid`商品位置信息，`gid`物品类别id，`mid`此类物品的商品id，`qty`商品数量，`cid`交换货物的id，`amt`交换货物数量
>
> refresh_time: 免费刷新的倒计时，标准时间为3小时自动刷新一次 the number of seconds remaining until the next refresh
>
> refreshable：剩余免费的刷新次数，一天免费可以刷新3次
>
> refresh_diamond：刷新需要消耗的钻石

```json
{
	"status": 1,
	"message": "get all black market information",
	"data": {
		"dark_markets": [
			{
				"pid": 0,
				"gid": 0,
				"mid": 27,
				"qty": 1,
				"cid": 5,
				"amt": 52
			},
			.....,
			{
				"pid": 7,
				"gid": 0,
				"mid": 4,
				"qty": 1,
				"cid": 1,
				"amt": 701
			}
		],
		"diamond" :
		{
			"remaining" : 3250,
			"reward"    : 0,
		},
		"refresh_time": 3400,
		"refreshable": 2,
		"refresh_diamond" : 100
	}
}
```



## darkmarket_transaction

##### 发送消息JSON格式

普通抽奖

> pid，需要交换物品的位置id，只需给位置id即可，指定物品id会根据配置表进行物品交换

```json
{
	"world": 0, 
	"function": "get_config_lottery",
	"data": {
		"token": "my toekn ^_^",
		"pid": 1
	}
}
```

##### 接受消息JSON格式

* 0: 获得商品

[抽取成功]()

> remaining：`pid`商品位置信息，`gid`物品类别id，`mid`此类物品的商品id，`qty`商品数量，`cid`交换货物的id，`amt`交换货物数`量拥有`的量
>
> reward：商品id的表示与上述一样，此值均为变化量

```json
{
	"status": 0,
	"message": "Purchase success",
	"data": {
		"remaining": {
			"gid": 0,
			"mid": 26,
			"qty": 2,
			"cid": 1,
			"amt": 2067
		},
		"reward": {
			"pid": 3,
			"gid": 0,
			"mid": 26,
			"qty": 2,
			"cid": 1,
			"amt": 803
		}
	}
}
```

[抽取失败]()

* 99: 商品位置id错误
* 98: 你还没有商品
* 97: 这个物品已经被购买
* 96: 交换物资不足
* 95: 你已经有此技能
* 94: 商品列表id错误


