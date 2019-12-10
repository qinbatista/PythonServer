## 方法列表

* [`get_all_role`](##get_all_role)
* [`level_up_role`](##level_up_role)
* [`level_up_star_role`](##level_up_star_role)
* [`get_config_role`](##get_config_role)

## get_all_role

##### 发送消息JSON格式

> 获取玩家的角色信息表，只会返回玩家拥有物品的数据，不会返回没有物品的数据

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

> roles：玩家的角色详细数据，`rid`角色id，`star`角色星数，`level`角色等级，`seg`角色碎片

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"roles": [
			{
				"rid": 1,
				"star": 1,
				"level": 0,
				"seg": 20
			},
			{
				"rid": 3,
				"star": 1,
				"level": 0,
				"seg": 0
			},
			{
				"rid": 4,
				"star": 1,
				"level": 0,
				"seg": 0
			},
			{
				"rid": 5,
				"star": 1,
				"level": 0,
				"seg": 30
			},
			{
				"rid": 6,
				"star": 1,
				"level": 0,
				"seg": 420
			},
			{
				"rid": 7,
				"star": 1,
				"level": 0,
				"seg": 0
			},
			{
				"rid": 10,
				"star": 1,
				"level": 0,
				"seg": 60
			},
			{
				"rid": 11,
				"star": 1,
				"level": 0,
				"seg": 30
			},
			{
				"rid": 12,
				"star": 1,
				"level": 0,
				"seg": 0
			},
			{
				"rid": 14,
				"star": 1,
				"level": 0,
				"seg": 30
			},
			{
				"rid": 15,
				"star": 1,
				"level": 0,
				"seg": 0
			},
			{
				"rid": 16,
				"star": 1,
				"level": 0,
				"seg": 60
			},
			{
				"rid": 17,
				"star": 1,
				"level": 0,
				"seg": 0
			},
			{
				"rid": 20,
				"star": 1,
				"level": 0,
				"seg": 30
			},
			{
				"rid": 25,
				"star": 1,
				"level": 0,
				"seg": 0
			},
			{
				"rid": 26,
				"star": 1,
				"level": 0,
				"seg": 0
			},
			{
				"rid": 27,
				"star": 1,
				"level": 0,
				"seg": 0
			},
			{
				"rid": 30,
				"star": 1,
				"level": 0,
				"seg": 0
			}
		],
		"config": {
			"seg": 25,
			"exp_pot": 5
		}
	}
}
```





## level_up_role

##### 发送消息JSON格式

升级武器等级，升级武器消耗的铁参考weapon_config.json

> role：指定需要升级的角色id

```json
{
	"world": 0,
	"function": "level_up_role",
	"data": {
		"token": "my token",
		"role": 24,
		"amount": 20
	}
}
```

##### 接受消息JSON格式

[成功]()

> data：原文中的2表示group为角色，其rid就是角色id为5，level就是角色等级100，3表示group为物品，iid就是物品id为9（经验药水），value就是价值为506
>

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"2": {
			"rid": 5,
			"level": 100
		},
		"3": {
			"iid": 9,
			"value": 506
		}
	}
}
```

[失败]()

* 99: 非法的角色id
* 98: 材料过少或者等级已满
* 97: 材料不足
* 96: 没有此角色



## level_up_star_role

##### 发送消息JSON格式

角色的升级需要消耗该角色的碎片，角色碎片的消耗量参考role_config.json

> role：角色的id

```json
{
	"world": 0, 
	"function": "level_up_star_role",
	"data": {
		"token": "my toekn ^_^",
		"role": 1
	}
}
```

##### 接受消息JSON格式

[抽取成功]()

> remaining：`rid`角色id，`star`物品的星数，`seg`该角色的碎片
>
> reward：与上述一样，此值均为变化量

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"remaining": {
			"rid": 1,
			"star": 3,
			"seg": 175
		},
		"reward": {
			"rid": 1,
			"star": 1,
			"seg": 75
		}
	}
}
```

[抽取失败]()

* 99: 物品名错误
* 98: 材料不足
* 97: 已经满级



## get_config_role

##### 发送消息JSON格式

升级被动，武器等级与技能点总数保持一致

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
>
> seg：角色突破需要消耗的碎片基础数据
>
> exp_pot：角色升级需要消耗的经验

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"role_config": {
			"standard_costs" :
			{
				"exp_pot" : 5,
				"seg" : 25
			}
		}
	}
}
```




