## 方法列表

* [`get_config_stage`](##get_config_stage)
* [`get_config_lottery`](##get_config_lottery)
* [`get_config_weapon`](##get_config_weapon)
* [`get_config_skill`](##get_config_skill)
* [`get_config_mall`](##get_config_mall)
* [`get_config_role`](##get_config_role)
* [`get_config_task`](##get_config_task)
* [`get_config_achievement`](##get_config_achievement)
* [`get_config_check_in`](##get_config_check_in)
* [`get_config_vip`](##get_config_vip)
* [`get_config_player`](##get_config_player)
* [`get_config_factory`](##get_config_factory)

##get_config_stage

##### 发送消息JSON格式

获取关卡的消耗列表与关卡的奖励列表entry_consumables_config.json,stage_reward_config.json 关卡 hang_reward_config.json挂机信息

> 无
>

```json
{
	"world": 0,
	"function": "get_config_stage",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[成功]()

> entry_consumables_config：返回entry_consumables_config.json
>
> stage_reward_config：返回stage_reward_config.json
>
> hang_reward_config: 返回hang_reward_config.json

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"entry_consumables_config": {.....},
    "stage_reward_config": {.....},
    "hang_reward_config": {.....}
		}
}
```

##get_config_lottery

获取lottery.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_lottery",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回转盘和抽奖的消耗信息，配置文件来自lottery.json

[成功]()

> lottery：返回lottery.json

```json
{
	"status": 0,
	"message": "get_config_lottery",
	"data": {
		"lottery": {....}
	}
}
```



##get_config_weapon

获取weapon_config.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_weapon",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回转盘和抽奖的消耗信息，配置文件来自weapon_config.json

[成功]()

> weapon_config：返回weapon_config.json

```json
{
	"status": 0,
	"message": "unlucky",
	"data": {
		"weapon_config": {....}
	}
}
```



##get_config_skill

获取skill_level_up_config.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_weapon",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回转盘和抽奖的消耗信息，配置文件来自skill_level_up_config.json

[成功]()

> skill_level_up_config：返回skill_level_up_config.json

```json
{
	"status": 0,
	"message": "unlucky",
	"data": {
		"skill_level_up_config": {....}
	}
}
```





##get_config_mall

获取mall_config.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_mall",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回转盘和抽奖的消耗信息，配置文件来自mall_config.json

[成功]()

> skill_level_up_config：返回skill_level_up_config.json

```json
{
	"status": 0,
	"message": "unlucky",
	"data": {
		"mall_config": {....}
	}
}
```



##get_config_role

获取role_config.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_role",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回转盘和抽奖的消耗信息，配置文件来自role_config.json

[成功]()

> role_config：返回role_config.json

```json
{
	"status": 0,
	"message": "unlucky",
	"data": {
		"role_config": {....}
	}
}
```



##get_config_task

获取task.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_task",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回转盘和抽奖的消耗信息，配置文件来自task.json

[成功]()

> task：返回task.json

```json
{
	"status": 0,
	"message": "unlucky",
	"data": {
		"task": {....}
	}
}
```





##get_config_achievement

获取achievement_config.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_achievement",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回转盘和抽奖的消耗信息，配置文件来自achievement_config.json

[成功]()

> achievement_config：返回achievement_config.json

```json
{
	"status": 0,
	"message": "unlucky",
	"data": {
		"achievement_config": {....}
	}
}
```





##get_config_check_in

获取check_in.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_check_in",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回转盘和抽奖的消耗信息，配置文件来自check_in.json

[成功]()

> check_in：返回check_in.json

```json
{
	"status": 0,
	"message": "unlucky",
	"data": {
		"check_in": {....}
	}
}
```



##get_config_vip

获取vip_config.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

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

返回转盘和抽奖的消耗信息，配置文件来自vip_config.json

[成功]()

> vip_config：返回vip_config.json

```json
{
	"status": 0,
	"message": "unlucky",
	"data": {
		"vip_config": {....}
	}
}
```



##get_config_player

获取player_config.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_player",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回转盘和抽奖的消耗信息，配置文件来自player_config.json

[成功]()

> player_config：返回player_config.json

```json
{
	"status": 0,
	"message": "unlucky",
	"data": {
		"player_config": {....},
    "energy": {
			"time": "0:20:00",
			"remaining": 9998,
			"reward": -2
		},
    "diamond":500,
    "coin":100
	}
}
```



##get_config_factory

获取get_factory_config.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_factory",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回转盘和抽奖的消耗信息，配置文件来自get_factory_config.json

[成功]()

> get_factory_config：返回get_factory_config.json

```json
{
	"status": 0,
	"message": "unlucky",
	"data": {
		"get_factory_config": {....}
	}
}
```

