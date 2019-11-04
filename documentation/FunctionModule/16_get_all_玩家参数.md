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

##get_all_skill

##### 发送消息JSON格式

获取和技能相关的所有信息，技能等级的信息，卷轴的基础信息，配置文件来自于skill_level_up_config.json

> 无
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

[成功]()

> skills：返回所有技能的信息以及技能的等级
>
> config：返回升级卷轴的概率和卷轴id
>

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"skills": [
			{
				"sid": 0,
				"level": 1
			},
			{
				"sid": 1,
				"level": 1
			},
			{
				"sid": 2,
				"level": 1
			},
			{
				"sid": 3,
				"level": 1
			},
			{
				"sid": 13,
				"level": 1
			},
			{
				"sid": 14,
				"level": 1
			},
			{
				"sid": 15,
				"level": 1
			},
			{
				"sid": 16,
				"level": 1
			},
			{
				"sid": 25,
				"level": 1
			},
			{
				"sid": 26,
				"level": 1
			},
			{
				"sid": 27,
				"level": 1
			},
			{
				"sid": 28,
				"level": 1
			},
			{
				"sid": 29,
				"level": 1
			},
			{
				"sid": 31,
				"level": 1
			},
			{
				"sid": 32,
				"level": 1
			},
			{
				"sid": 33,
				"level": 1
			},
			{
				"sid": 35,
				"level": 1
			}
		],
		"config": {
			"skill_scroll_id": [
				"6",
				"7",
				"8"
			],
			"upgrade_chance": {
				"6": 0.1,
				"7": 0.3,
				"8": 1
			}
		}
	}
}
```

[失败]()

* 99: 盔甲不足

##level_up_skill

##### 发送消息JSON格式

选择需要升级的卷轴以及需要升级的技能，服务器会返回对应的等级以及参数，skill_level_up_config.json包含卷轴升级的概率。

> skill: 技能id
>
> item：卷轴的id

```json
{
	"world": 0, 
	"function": "level_up_weapon",
	"data": {
		"token": "my toekn ^_^",
    "skill": 2,
    "item": 5
	}
}
```

##### 接受消息JSON格式

升级护甲返回的结果。

[成功]()

> sid：技能的id
>
> level：技能的等级
>
> iid：卷轴的数字id
>
> value：卷轴的数量

```json
{
	"status": 1,
	"message": "unlucky",
	"data": {
		"sid": 13,
		"level": 1,
		"iid": 6,
		"value": 54
	}
}
```

[失败]()

* 99: 等级已经达到最大值
* 98: 材料不足
* 97: 卷轴id不对
* 96: 技能未解锁


