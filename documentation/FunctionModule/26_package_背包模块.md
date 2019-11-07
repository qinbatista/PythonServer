## 方法列表

* [`exchange_card`](##_exchange_card)



## check_in

签到按照`每月当天`进行签到，签到的奖励对照`check_in.json`,签到的内容为7天一循环(`1号为第一天天`)

##### 发送消息JSON格式

```json
{
	"world": 0, 
	"function": "start_hang_up",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

[签到成功]()

> remaining：物品剩余的数据 3:18:2分别表示 种类id : 商品id : 商品数量，所以3:18: 2表示金币2个
>
> reward：变化的量

```json
{
	"status": 0,
	"message": "Sign-in success",
	"data": {
		"remaining": [
			"3:18:2"
		],
		"reward": [
			"3:18:1"
		]
	}
} 
```

[签到失败]()

* 99: 已签到，不会重复获得奖励





## supplement_check_in

##### 发送消息JSON格式

补签功能，把之前没有签到的天数用钻石进行补签，`补钱一天`消耗的钻石数量在配置表`check_in.json`

```json
{
	"world": 0, 
	"function": "start_hang_up",
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



## get_all_check_in_table

获取签到表的情况，只是获取数据，`不改变`任何服务器数值

```json
{
	"world": 0,
	"function": "get_all_check_in_table",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[获取资源成功]()

> remaining：数字1，2，3，4表示当月的日期，reward则表示是否领取奖励(签到)
>
> today: 当前日期
>
> time：距离下次签到的时间（如果提示玩家还有多久可以进行下次签到，这个时间可以派上用场）