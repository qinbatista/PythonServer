## 方法列表

* [`start_hang_up`](##start_hang_up)
* [`get_hang_up_reward`](##get_hang_up_reward)
* [`get_hang_up_info`](##get_hang_up_info)
* [`enter_stage`](##enter_stage)
* [`pass_stage`](##pass_stage)
* [`check_boss_status`](##check_boss_status)
* [`get_top_damage`](##get_top_damage)
* [`enter_world_boss_stage`](##enter_world_boss_stage(enter_stage))
* [`leave_world_boss_stage`](##leave_world_boss_stage(pass_stage))
* [`get_config_boss`](##get_config_boss)

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
>
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
			"time": 32
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
				"remaining": 2195,
				"reward": 620
			},
			{
				"iid": "1",
				"remaining": 162047,
				"reward": 1860
			},
			{
				"iid": "11",
				"remaining": 41,
				"reward": 3
			}
		],
		"hang_up_info": {
			"hang_stage": 2,
			"time": 1893
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
			"time": 20000,
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
* 96: 没有该关卡的配置文件信息
* 95: 进入关卡不等于离开，有开挂嫌疑，清除缓存重新进入游戏



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
* 96: 没有该关卡的配置文件信息

- 98: 关卡错误（stage error）





## check_boss_status

##### 发送消息JSON格式

获取世界boss的详细情况，返回的消息内容为所有boss的血量（目前为10个世界boss），挑战次数，刷新挑战次数时间，此方法只作为客户端显示实用，boss的生命值来自配置文件world_boss_config.json，玩家上传的分数会直接和配置文件的数值相减，配置文件boss的生命值每个月会刷新一次，生命值耗尽继续挑战下一个boss，世界boss打死之后服务器会在一天之内给所有玩家发送邮件礼物，每个月一号会刷新所有世界boss

```json
{
	"world": 0,
	"function": "check_boss_status",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[成功]()

> world_boss
>
> - remaining：剩余挑战boss的次数
> - time：刷新挑战次数的时间，今天剩余时间
> - month_time：所有boss刷新剩余时间
>
> boss_life_ratio: 各个boss的生命值百分比

```json
{
	"status": 0,
	"message": "Successfully get hook information",
	"data": {
		"world_boss": {
			"remaining": 3,
			"time": 32393,
			"month_time": 1933193
		},
		"boss_life_ratio": {
			"boss0": "1.00",
			"boss1": "1.00",
			"boss2": "1.00",
			"boss3": "1.00",
			"boss4": "1.00",
			"boss5": "1.00",
			"boss6": "1.00",
			"boss7": "1.00",
			"boss8": "1.00",
			"boss9": "1.00"
		}
	}
}
```



## get_top_damage

##### 发送消息JSON格式

获取世界boss的伤害排行榜，一次只会获取10个人的伤害排行榜

>page: 排行序数，比如1就是排行1～10名的信息，2就是排行11～20的信息依次类推，页码从1开始

```json
{ 
	"world": 0,
	"function": "get_top_damage",
	"data": {
		"token": "my token",
    	"page":1
	}
}
```

##### 接受消息JSON格式

[成功消息]()

> damange: 玩家造成的最高伤害
>
> ranking: 玩家的排名，不存在则返回-1
>
> rank：排名玩家的信息
>
> - NO：名次
> - name：游戏名字
> - damage：最高伤害
> - fid：家族名字
> - level：玩家等级

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"page": 2,
		"damage": 4872,
		"ranking": 5,
		"rank": [
			{
				"NO": 11,
				"name": "name_1",
				"damage": 112,
				"fid": "",
				"level": 1
			},
			{
				"NO": 12,
				"name": "name_17",
				"damage": 17,
				"fid": "",
				"level": 1
			},
			{
				"NO": 13,
				"name": "name_12",
				"damage": 12,
				"fid": "",
				"level": 1
			},
			{
				"NO": 14,
				"name": "name_10",
				"damage": 10,
				"fid": "",
				"level": 1
			}
		]
	}
}
```

[失败消息]()

* 99: 关卡数量不对
* 98: 这页没有数据



## enter_world_boss_stage(enter_stage)

##### 发送消息JSON格式

进入世界boss房间

```json
{ 
	"world": 0,
	"function": "enter_stage",
	"data": {
		"token": "my token",
        "stage": 3000
	}
}
```

##### 接受消息JSON格式

[成功消息]()

> energy：剩余能量点数
>
> cooling_time：能量恢复时间剩余秒数（-1代表满能量状态不需要恢复）
>
> consume：本次消耗的能量
>
> times: 剩余挑战boss次数
>
> cd_time：刷新挑战次数的冷却剩余时间

```json
{
	"status": 0,
	"message": "enter world boss success",
	"data": {
		"energy": 9960,
		"cooling_time": -1,
		"consume": -10,
		"times": 1,
        "cd_time": 5565
	}
}
```

- 99：boss已全部死亡
- 98：没有挑战次数
- 97：能量不够
- 96：没有配置文件



## leave_world_boss_stage(pass_stage)

##### 发送消息JSON格式

离开世界boss房间，更新世界boss最高伤害，stage为3000-3999为世界boss关卡离开

```json
{ 
	"world": 0,
	"function": "pass_stage",
	"data": {
		"token": "my token",
        "stage": 3000, 
        "damange": 110000
	}
}
```

##### 接受消息JSON格式

[成功消息]()

>new_record: 是否是最新记录，0代表不是最新记录，1代表是最新记录
>
>highest_damage: 造成的最高伤害
>
>boss_life_ratio: 各个boss的生命值

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"new_record": 0,
		"highest_damage": 110000,
		"boss_life_ratio": {
			"boss0": "0.00",
			"boss1": "0.00",
			"boss2": "1.00",
			"boss3": "1.00",
			"boss4": "1.00",
			"boss5": "1.00",
			"boss6": "1.00",
			"boss7": "1.00",
			"boss8": "1.00",
			"boss9": "1.00"
		}
	}
}
```

- 98：stage error（关卡错误）
- 99：abnormal data（数据错误）



## get_config_boss

获取world_boss_config.json的配置文件信息

##### 发送消息JSON格式

```json
{
	"world": 0, 
	"function": "get_config_boss",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

[成功]()

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"config": {
			"max_enter_time": 3,
			"max_upload_damage": 200000,
			"boss1": {
				"life_value": 10000
			},
			"boss2": {
				"life_value": 100000
			},
			"boss3": {
				"life_value": 100000
			},
			"boss4": {
				"life_value": 100000
			},
			"boss5": {
				"life_value": 100000
			},
			"boss6": {
				"life_value": 100000
			},
			"boss7": {
				"life_value": 100000
			},
			"boss8": {
				"life_value": 100000
			},
			"boss9": {
				"life_value": 100000
			},
			"boss10": {
				"life_value": 100000
			}
		}
	}
}
```

















