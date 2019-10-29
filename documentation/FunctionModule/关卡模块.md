## 方法列表

* [`start_hang_up`](##start_hang_up)
* [`get_hang_up_reward`](##get_hang_up_reward)
* [`get_hang_up_info`](##get_hang_up_info)
* [`enter_stage`](##enter_stage)
* [`pass_stage`](##pass_stage)

##start_hang_up

开始挂机，玩家在`通过`关卡以后才能开始挂机，挂机的奖励列表来自`hang_reward_config.json`配置表。

```json
{
	"world": 0, 
	"function": "start_hang_up",
	"data": {
		"token": "my toekn ^_^",
		"stage": 0
	}
}
```

##### 接受消息JSON格式

[挂机关卡不同]()

> start_hang_up_reward：奖励的消耗列表，列表里面包含商品的id，值，变化量，`如果已有挂机关卡，则先结算，后挂新关卡`
>
> hang_up_info：挂机的信息，其中包含`当前`挂机的关卡和`上一关`挂机时长(小时制)

```json

{
	"status": 1,
	"message": "Repeated hang up successfully",
	"data": {
		"start_hang_up_reward": [
			{
				"iid": "2",
				"value": 2665,
				"increment": 20
			},
			{
				"iid": "1",
				"value": 7995,
				"increment": 60
			},
			{
				"iid": "11",
				"value": 0,
				"increment": 0
			}
		],
		"hang_up_info": {
			"hang_stage": 2,
      "time":"25:00:00"
		}
	}
}
```

[挂机关卡相同]()

> 挂机相同关卡不需要结算资源，直接返回即可

```json
{
	"status": 1,
	"message": "same stage"
}
```

[挂机关卡失败]()

* 99: 关卡参数错误













##get_hang_up_reward

获取挂机奖励，`会`立即结算资源到玩家的物品栏

> stage：需要离开的关卡

```json
{
	"world": 0,
	"function": "get_hang_up_reward",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[获取资源成功]()

> get_hang_up_rewards：获取资源列表 `iid`商品列表，`remaining`剩余资源，`reward`增加的资源
>
> hang_up_info: 挂机信息, `time`挂机的时长（小时制），`hang_stage`挂机的关卡

```json
{
	"status": 0,
	"message": "Settlement reward success",
	"data": {
		"get_hang_up_rewards": [
			{
				"iid": "2",
				"remaining": 4290,
				"reward": 1460
			},
			{
				"iid": "1",
				"remaining": 12870,
				"reward": 4380
			}
		],
		"hang_up_info": {
			"hang_stage": 1,
			"time": "17:14:17"
		}
	}
}
```

[调整关卡失败]()

* 99: 没有挂机关卡，无法获得挂机奖励















##get_hang_up_info

获取挂机奖励，`不会`立即结算资源到玩家的物品栏

> stage：

```json
{
	"world": 0,
	"function": "get_hang_up_reward",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[获取资源成功]()

> get_hang_up_rewards：获取资源列表 `iid`商品列表，`remaining`剩余资源，`reward`增加的资源
>
> hang_up_info: 挂机信息, `time`挂机的时长（小时制），`hang_stage`挂机的关卡

```json
{
	"status": 0,
	"message": "Settlement reward success",
	"data": {
		"get_hang_up_info": [
			{
				"iid": "2",
				"remaining": 4290,
				"reward": 1460
			},
			{
				"iid": "1",
				"remaining": 12870,
				"reward": 4380
			}
		],
		"hang_up_info": {
			"hang_stage": 1,
			"time": "17:14:17"
		}
	}
}
```

[调整关卡失败]()

* 99: 没有挂机关卡，无法获得挂机信息













##enter_stage

进入关卡，玩家在扣除相应的资源后即可进入关卡，消耗的资源列表来自`entry_consumables_config.json`配置表，消耗的体力来自`player_config.json`配置表

> stage：需要进入的关卡

```json
{
	"world": 0,
	"function": "enter_stage",
	"data": {
		"token": "my token",
		"stage": 1
	}
}
```

##### 接受消息JSON格式

[进入关卡成功]()

> enter_stages：进入关卡，消耗的物品变化，`iid`表示商品id, `remaining`表示剩余数量，`reward`表示变化值
>
> exp_info: 经验信息, `exp`当前经验，`level`当前等级，`need`升级剩余经验
>
> energy：能量信息，`time`下一点体力的恢复时间，`remaining`剩余体力，`reward`体力改变量
>
> enemy_layout：当前关卡信息
>
> monster：当前关卡的怪物信息

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"enter_stages": [
			{
				"iid": 2,
				"remaining": 2705,
				"reward": 0
			},
			{
				"iid": 1,
				"remaining": 8115,
				"reward": 0
			}
		],
		"exp_info": {
			"exp": 660,
			"level": 18,
			"need": 60
		},

		"energy": {
			"time": "0:20:00",
			"remaining": 9998,
			"reward": -2
		},
    "enemy_layout": [.....],
		"monster": [.....]
	}
}
```

[挂机关卡失败]()

* 99: 关卡不对
* 98: 材料不足
* 97: 能量不足













##pass_stage

进入关卡，玩家在扣除相应的资源后即可进入关卡，消耗的资源列表来自`stage_reward_config.json`配置表。

> stage：需要离开的关卡

```json
{
	"world": 0,
	"function": "enter_stage",
	"data": {
		"token": "my token",
		"stage": 1
	}
}
```

##### 接受消息JSON格式

[进入关卡成功]()

> pass_stages：进入关卡，获得的物品变化，`iid`表示商品id, `remaining`表示剩余数量，`reward`表示变化值
>
> exp_info: 经验信息, `remaining`当前经验，`reward`增加经验
>
> energy：能量信息，`time`下一点体力的恢复时间，`remaining`剩余体力，`reward`体力改变量
>
> p_stage：关卡状态，`finally`当前已通过最高关卡，`vary`关卡变化量

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"pass_stages": [
			{
				"iid": "10",
				"remaining": 43,
				"reward": 1
			}
		],
		"p_exp": {
			"remaining": 670,
			"reward": 10
		},
		"p_stage": {
			"finally": 2,
			"vary": 0
		}
	}
}
```

[调整关卡失败]()

* 99: 关卡数量不对



