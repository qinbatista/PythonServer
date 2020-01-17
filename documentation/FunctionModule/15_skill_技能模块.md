## 方法列表

* [`get_all_skill`](##get_all_skill)
* [`level_up_skill`](##level_up_skill)

## get_all_skill

##### 发送消息JSON格式

获取和技能相关的所有信息，技能等级的信息，卷轴的基础信息，配置文件来自于skill_level_up_config.json

> 无
>

```json
{
	"world": 0,
	"function": "get_all_skill",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[成功]()

> skills：返回所有技能的信息以及技能的等级
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
		]
	}
}
```



## level_up_skill

##### 发送消息JSON格式

选择需要升级的卷轴以及需要升级的技能，服务器会返回对应的等级以及参数，skill_level_up_config.json包含卷轴升级的概率。

> skill: 技能id
>
> item：卷轴的id

```json
{
	"world": 0, 
	"function": "level_up_skill",
	"data": {
		"token": "my toekn ^_^",
    	"skill": 1,
    	"item": 6
	}
}
```

##### 接受消息JSON格式

升级技能返回的结果。

[成功]()

> 按`git:iid:qty`解析

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"remain": [
			"3:8:10095",
			"1:1:3"
		],
		"reward": [
			"3:8:3",
			"1:1:1"
		]
	}
}
```

```json
{
	"status": 1,
	"message": "unlucky",
	"data": {
		"remain": [
			"3:8:10095",
			"1:1:3"
		],
		"reward": [
			"3:8:3",
			"1:1:0"
		]
	}
}
```

[失败]()

* 99: 等级已经达到最大值
* 98: 材料不足
* 97: 卷轴id不对
* 96: 技能未解锁


