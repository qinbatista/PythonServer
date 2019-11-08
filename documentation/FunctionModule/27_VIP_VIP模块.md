## 方法列表

* [`get_config_vip`](##get_config_vip)
* [`get_vip_package`](##get_vip_package)
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

> config：vip的配置表
>
> daily_reward：发送每日奖励是否成功，0成功，1失败

```json
{
	"status": 0,
	"message": "Sign-in success",
	"data": {
		"config": 
    {
      ......
    },
		"daily_reward": 0
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

