- [`check_boss_status`](##check_boss_status)
- [`get_top_damage`](##get_top_damage)
- [`enter_stage`](##enter_world_boss_stage(enter_stage))
- [`pass_stage`](##leave_world_boss_stage(pass_stage))

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

> world_boss：刷新挑战次数的时间，剩余挑战boss的次数，
>
> boss_life_ratio: 各个boss的生命值

```json
{
	"status": 0,
	"message": "Successfully get hook information",
	"data": {
		"world_boss": {
			"remaining": 0,
			"time": 2120
		},
		"boss_life_ratio": {
			"boss0": "0.00",
			"boss1": "0.00",
			"boss2": "0.00",
			"boss3": "0.00",
			"boss4": "0.00",
			"boss5": "0.70",
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

> damage: 玩家造成的最高伤害
>
> ranking: 玩家的排名，不存在则返回-1
>
> rank：排名玩家的名字和伤害

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"damage": 0,
		"ranking": -1,
		"rank": [
			{
				"name": "keepo",
				"damage": 8373
			},
			{
				"name": "name_0",
				"damage": 7919
			},
			{
				"name": "name_test9000",
				"damage": 7416
			},
			{
				"name": "name_q99",
				"damage": 7258
			},
			{
				"name": "name_1",
				"damage": 6325
			},
			{
				"name": "name_9",
				"damage": 6222
			},
			{
				"name": "name_q1",
				"damage": 4606
			},
			{
				"name": "name_2",
				"damage": 4290
			},
			{
				"name": "name_5",
				"damage": 2638
			},
			{
				"name": "name_7",
				"damage": 1645
			}
		]
	}
}
```

[失败消息]()

- 98: 此页面无数据

* 99: 页码错误



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

> times: 剩余挑战boss次数
>
> energy：剩余能量点数
>
> cooling_time：能量恢复时间剩余秒数（-1代表满能量状态不需要恢复）
>
> consume：本次消耗的能量

```json
{
	"status": 0,
	"message": "enter world boss success",
	"data": {
		"energy": 9960,
		"cooling_time": -1,
		"consume": -10,
		"times": 1
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
        "damage": 110000
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
- 99：abnormal data（数据异常）























