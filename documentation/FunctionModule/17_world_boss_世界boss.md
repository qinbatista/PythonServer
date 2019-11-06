

## check_boss_status

##### 发送消息JSON格式

获取世界boss的详细情况，返回的消息内容为所有boss的血量（目前为10个世界boss），挑战次数，刷新挑战次数时间，此方法只作为客户端显示实用，boss的生命值来自配置文件world_boss_config.json，玩家上传的分数会直接和配置文件的数值相减，配置文件boss的生命值每个月会刷新一次，生命值耗尽继续挑战下一个boss，世界boss打死之后服务器会在一天之内给所有玩家发送邮件礼物，每个月一号会刷新所有世界boss

```json
{
	"world": 0,
	"function": "enter_stage",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[进入关卡成功]()

> world_boss：刷新挑战次数的时间，剩余挑战boss的次数，
>
> boss_life_ratio: 各个boss的生命值

```json
{
	"status": 0,
	"message": "success",
	"data": {
			"world_boss": {
				"time": "23:20:00",
				"remaining": 2
			},
			"boss_life_ratio": {
				"boss1": "0.12",
				"boss2": "1",
				"boss3": "1",
				"boss4": "1",
				"boss5": "1",
				"boss6": "1",
				"boss7": "1",
				"boss8": "1",
				"boss9": "1",
				"boss10": "1"
			}
	}
}
```

[调整关卡失败]()

* 99: 关卡数量不对

## get_top_damage

##### 发送消息JSON格式

获取世界boss的伤害排行榜，一次只会获取10个人的伤害排行榜

>rank: 排行序数，比如1就是排行1～10名的信息，2就是排行11～20的信息依次类推

```json
{ 
	"world": 0,
	"function": "get_top_damage",
	"data": {
		"token": "my token",
    	"rank":1
	}
}
```

##### 接受消息JSON格式

[成功消息]()

> rank：排名玩家的名字和伤害
>

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"rank": [
			{
				"name": "大哥大",
				"damange": 200000
			},
			{
				"name": "a",
				"damange": 199999
			},
			{
				"name": "ljs",
				"damange": 2222222
			},
			{
				"name": "waaaa",
				"damange": 111111
			},
			{
				"name": "是否",
				"damange": 9
			},
			{
				"name": "个呃呃",
				"damange": 8
			},
			{
				"name": "呜呜呜",
				"damange": 7
			},
			{
				"name": "啊啊啊啊",
				"damange": 6
			},
			{
				"name": "大肉肉肉",
				"damange": 5
			},
			{
				"name": "特恶",
				"damange": 4
			}
		]
	}
}
```

[失败消息]()

* 99: 关卡数量不对



## leave_world_boss_stage

##### 发送消息JSON格式

离开世界boss房间，更新世界boss最高伤害

```json
{ 
	"world": 0,
	"function": "leave_world_boss_stage",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[成功消息]()

>new_record: 是否是最新记录，0代表不是最新记录，1代表是最新记录
>
>highest_damage: 造成的最高伤害

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"new_record": 1,
		"highest_damage": 999999
	}
}
```

























