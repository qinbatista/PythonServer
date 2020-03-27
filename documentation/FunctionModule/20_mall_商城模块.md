## 方法列表

- [`purchase_success`](##purchase_success)
- [`get_merchandise`](##`get_merchandise)
- [`exchange`](##`exchange)
- [`get_config_mall`](##get_config_mall)

## purchase_success

##### 发送消息JSON格式

第三方支付服务器发送消息到游戏服务器，具体消息内容需要根据第三方服务器的消息方式进行解析，但我们始终会保留，服务器物品id，来发放对应的道具, 道具的解析在mall.json，如下消息是必须拥有的消息，一般第三方发过来的消息都会比下面列举的更多，第三方发送消息（伪代码）

> pid: 道具道具内部识别id
>
> order_id: 订单号
>
> channel: 渠道名字
>
> user_name: 用户名
>
> currency: 购买币种



```json
{
	"world": 0,
	"function": "purchase_success",
	"data": {
		"token": "my token",
		"pid": "VIP_CARD_NORMAL",
		"order_id": "9282909831001123",
		"channel": "apple",
		"user_name": "小郡肝",
		"currency": "RMB"
	}
}
```

##### 接受消息JSON格式

解析成功之后，数据库需要存储：订单号、用户uid、用户名字、购买币种、购买金额、商品id、商品数量、渠道名字、购买时间、是否为永久性物品、道具是否已领取道具(此游戏需要立即发放，单机游戏需要主动领取)。存储完数据之后，也需要给玩家发送相应道具，并返回道具的变化量。

注意：单机游戏玩家在收到第三方的支付成功回调时，服务器会主动获取一次已购买物品，获取方法为`get_merchandise()`

[成功]()

> remaining: 购买之后，购买物品的剩余量
>
> reward: 购买之后，购买物品的变化量

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"remaining": {
			"iid": 5,
			"qty": 460
		},
		"reward": {
			"iid": 5,
			"qty": 100
		}
	}
}
```

```json
{
	"status": 1,
	"message": "success",
	"data": {
		"cooling_time": 10693361,
		"card_id": 26
	}
}
```

[失败]()

99: username error

98: pid error

97: config error



## get_merchandise

##### 发送消息JSON格式

领取所有未被领取的道具，返回`未领取道具列表`以及`不可重复购买道具`

> token: 用户的token
>

```json
{
	"world": 0,
	"function": "get_merchandise",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

服务器会直接返回可以直接获得的物品，比如未领取物品或者永久性物品

[成功]()

> remaining: 购买之后，购买物品的剩余量
>
> reward: 购买之后，购买物品的变化量

```json
{
  "status": 0,
	"message": "purchase success",
  "pid_list":[ 
  	"EXP_POINT_PLENTY",
    "VIP_CARD_PERMANENT"]
}
```

[失败]()

99: 服务器错误



## exchange

##### 发送消息JSON格式

输入值特定的值，此值会兑换成相应的物品id给用户

> token: 用户的token

```json
{
	"world": 0,
	"function": "exchange",
	"data": {
		"token": "my token",
    	"game_id":"game id",
    	"exchange_id":"IOJwlawOIWBMzjJw"
	}
}
```

##### 接受消息JSON格式

一次只能兑换一个物品

[成功]()

> vip_card: vip卡购买信息
>
> item: 物品购买信息
>
> etime：兑换结束时间
>
> receive：剩余可兑换次数

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"vip_card": {},
		"item": {
			"remaining": {
				"iid": 5,
				"qty": 250
			},
			"reward": {
				"iid": 5,
				"qty": 100
			}
		},
		"etime": "2019-12-25 18:56:12",
		"receive": 1
	}
}
```

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"vip_card": {
			"cooling_time": 2678400,
			"card_id": 26
		},
		"item": {},
		"etime": "2019-12-25 18:56:12",
		"receive": 0
	}
}
```

[失败]()

99: 兑换码不存在

98: 兑换码已兑换完

97: 兑换码已过期

96: pid error

95: config error



## get_config_mall

##### 发送消息JSON格式

> token: 用户的token

```json
{
	"world": 0,
	"function": "get_config_mall",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"mall_config": {
			"VIP_CARD_NORMAL": {
				"quantity": 1,
				"price": {
					"RMB": 7,
					"USDollar": 1
				},
				"repeatable": "n"
			},
			"VIP_CARD_ULTIMATE": {
				"quantity": 1,
				"price": {
					"RMB": 7,
					"USDollar": 1
				},
				"repeatable": "n"
			}
		}
	}
}
```

