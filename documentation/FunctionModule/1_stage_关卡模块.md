## 方法列表

* [`start_hang_up`](##start_hang_up)
* [`get_hang_up_reward`](##get_hang_up_reward)
* [`get_hang_up_info`](##get_hang_up_info)
* [`enter_stage`](##enter_stage)
* [`pass_stage`](##pass_stage)

## start_hang_up

##### 发送消息JSON格式

开始挂机，玩家在`通过`关卡以后才能开始挂机，挂机的奖励列表来自`hang_reward_config.json`配置表，只有普通关卡比如，1，2，3，4，5才能挂机。

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
	"status": 0,
	"message": "hang up success",
	"data": {
        "start_hang_up_reward": [],
		"hang_up_info": {
			"hang_stage": 2,
      		"time":"10:00:00"
		}
	}
}
```

[挂机关卡不同]()

>  start_hang_up_reward：获取资源列表 `iid`商品列表，`remaining`剩余资源，`reward`增加的资源

>  hang_up_info: 挂机信息, `time`挂机的时长（小时制），`hang_stage`挂机的关卡

```json
{
	"status": 1,
	"message": "Settlement reward success",
	"data": {
		"start_hang_up_reward": [
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

[挂机关卡相同]()

> 挂机相同关卡不需要结算资源，直接返回即可

```json
{
	"status": 2,
	"message": "same stage"
}
```

[挂机关卡失败]()

* 99: 关卡参数错误













## get_hang_up_reward

##### 发送消息JSON格式

获取挂机奖励，`会`立即结算资源到玩家的物品栏

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



## get_hang_up_info（暂时未用）

##### 发送消息JSON格式

获取挂机奖励，`不会`立即结算资源到玩家的物品栏，只是作为挂机资源的显示

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
	"message": "Successfully get hook information",
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





## enter_stage

##### 发送消息JSON格式

进入关卡，玩家在扣除相应的资源后即可进入关卡，消耗的资源列表来自`entry_consumables_config.json`配置表，消耗的体力来自`player_config.json`配置表，关切对应表如下：

普通关卡：1,2,3,4,5,6,7....

冲塔关卡：1001，1002，1003，1004，1005，1006，1007，1008，1009.....

活动关卡：2001，2002，2003，2004，2005，2006，2007，2008，2009.....

世界boss：3001，3002，3003，3004，3005，3006，3007，3008，3009....

`需要创建完整的枚举类型与客户端保持对应`

> 关卡特征：
>
> * 普通关卡：可以挂机，可以随意进出，资源可以重复获取
> * 冲塔关卡：不可挂机，只可顺序闯关，资源不可重复，特定时间刷新
> * 活动关卡：不可挂机，特定时间进入，资源不可重复，特定`时间段`刷新
> * 世界boss：不可挂机，限定条件进入（boss血量不为0），资源邮件发放，特定时间刷新，一天挑战3次（次数服务器控制）

进入关卡时会`记录`进入关卡的id，相应离开关卡也会对比进入关卡的id，如果匹配则表示正常，不匹配，则提示数据异常，数据异常需要清除玩家token，客户端重新启动，并记录重新记录进入关卡次数和离开关卡次数

> stage：需要进入的关卡编号

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
>
> *world_boss: 进入世界boss需要返回，需要返回世界boss再次挑战的时间（一天挑战3次），剩余挑战次数

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
		"world_boss": {
    		"time":"23:20:00",
            'remaining' : 2,
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
* 96: 进入关卡不等于离开，有开挂嫌疑，清除缓存重新进入游戏



## pass_stage

##### 发送消息JSON格式

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


