## 方法列表

- [`purchase_success`](##purchase_success)
- [`get_merchandise`](##`get_merchandise)
- [`exchange`](##`exchange)

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
  .....
  "pid":"VIP_CARD_NORMAL",
  "order_id":"9282909831001123",
  "channel":"apple",
  "user_name":"小郡肝",
  "currency":"RMB" 
  ....
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
	"message": "purchase success",
  "remaining": {
			"0": {
				"wid": 1,
				"level": 3,
				"sp": 3
			},
			"3": {
				"iid": 2,
				"value": 4176
			}
		},
  "reward": {
			"0": {
				"wid": 1,
				"level": 1,
				"sp": 1
			},
			"3": {
				"iid": 2,
				"value": 60
			}
		},
  "pid":"VIP_CARD_NORMAL"
}
```

[失败]()

99: 第三方服务器错误

98: 第三方武器没响应 



## get_merchandise

##### 发送消息JSON格式

领取所有未被领取的道具，返回`未领取道具列表`以及`不可重复购买道具`

> token: 用户的token
>

```json
{
	"world": 0,
	"function": "get_all_weapon",
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
  	"EXPERIENCE_POTION_PLENTY",
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
    "exchange_id":"IOJwlawOIWBMzjJw"
	}
}
```

##### 接受消息JSON格式

一次只能兑换一个物品

[成功]()

> remaining: 兑换之后，购买物品的剩余量
>
> reward: 兑换之后，购买物品的变化量
>
> pid：兑换的商品id

```json
{
  "status": 0,
	"message": "purchase success",
  "remaining": "3:2:2990",
	"reward": "3:2:1000"
}
```

[失败]()

99: 验证码错误

98: 验证码已经被用过

