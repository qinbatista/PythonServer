## 方法列表

* [`get_all_weapon`](##get_all_weapon)
* [`level_up_weapon`](##level_up_weapon)
* [`level_up_star_weapon`](##level_up_star_weapon)
* [`level_up_passive_weapon`](##level_up_passive_weapon)
* [`reset_skill_point_weapon`](##reset_skill_point_weapon)

## get_all_weapon

##### 发送消息JSON格式

> 获取玩家的武器信息表，只会返回玩家拥有物品的数据，不会返回没有物品的数据

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

[抽取成功]()

> weapons：玩家的武器列表信息，排名根据武器序号默认排名。`wid`武器id，`star`武器星数（星数为0无法使用此武器），`level`武器等级，`sp`武器的技能点（技能点于武器等级保持一致），`seg`（武器的碎片数量），`p1,p2,p3,p4`表示武器的被动技能等级。

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"weapons": [
			{
				"wid": 1,
				"star": 1,
				"level": 0,
				"sp": 0,
				"seg": 289,
				"p1": 0,
				"p2": 0,
				"p3": 0,
				"p4": 0
			},
			{
				"wid": 2,
				"star": 1,
				"level": 0,
				"sp": 0,
				"seg": 0,
				"p1": 0,
				"p2": 0,
				"p3": 0,
				"p4": 0
			},
			{
				"wid": 3,
				"star": 1,
				"level": 0,
				"sp": 0,
				"seg": 90,
				"p1": 0,
				"p2": 0,
				"p3": 0,
				"p4": 0
			}
		]
	}
}
```



## level_up_weapon

##### 发送消息JSON格式

升级武器等级，升级武器消耗的铁参考weapon_config.json

> weapon：指定需要升级的武器id
>
> delta：用户需要升级的增量，只能为正整数

```json
{
	"world": 0, 
	"function": "level_up_weapon",
	"data": {
		"token": "my toekn ^_^",
		"weapon": 1,
        "delta": 2
	}
}
```

##### 接受消息JSON格式

[升级成功]()

> remaining：商品的当前量，实例中`0`表示列表`id`，`0`表示武器类，`wid`表示武器id，`level`表示武器等级，`sp`表示武器的技能点数，`3`表示武物品类，`iid`表示物品id，`value`表示物品的总量
>
> reward：商品id的表示与上述一样，数值均为变化量

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"remaining": {
			"0": {
				"wid": 2,
				"level": 120,
				"sp": 120
			},
			"3": [
				{
					"iid": 2,
					"value": 98999500
				},
				{
					"iid": 1,
					"value": 98999500
				}
			]
		},
		"reward": {
			"0": {
				"wid": 2,
				"level": 1,
				"sp": 1
			},
			"3": [
				{
					"iid": 2,
					"value": 35700
				},
				{
					"iid": 1,
					"value": 35700
				}
			]
		}
	}
}
```

[抽取失败]()

* 99: 物品名错误
* 98: 材料不足
* 97: 材料不足
* 96: 你没有此武器
* 95: 武器已达到满级



## level_up_star_weapon

##### 发送消息JSON格式

武器的升级需要消耗该物品的碎片，武器碎片的消耗量参考weapon_config.json

> weapon：武器的id

```json
{
	"world": 0, 
	"function": "level_up_star_weapon",
	"data": {
		"token": "my toekn ^_^",
		"weapon": 1
	}
}
```

##### 接受消息JSON格式

[抽取成功]()

> remaining：`wid`武器id，`star`物品的星数，`seg`该武器的碎片
>
> reward：与上述一样，此值均为变化量

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"remaining":
		{
			"wid": 1,
			"star": 2,
			"seg": 239
		},
		"reward":
		{
			"wid": 1,
			"star": 2,
			"seg": 30
		}
	}
}
```

[抽取失败]()

* 99: 物品名错误
* 98: 材料不足
* 97: 武器已经突破到极限



## level_up_passive_weapon

##### 发送消息JSON格式

升级被动，武器等级与技能点总数保持一致

> weapon：武器的id
>
> passive：武器的被动id

```json
{
	"world": 0, 
	"function": "level_up_passive_weapon",
	"data": {
		"token": "my toekn ^_^",
		"weapon": 1,
		"passive": 1
	}
}
```

##### 接受消息JSON格式

[升级成功]()

> remaining：`wid`物品id，`pid`代表被动技能id，`level`代表当前被动技能等级，`sp`表示剩余技能点数
>
> reward：商品id的表示与上述一样，此值均为变化量

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"remaining": {
			"wid": 1,
			"pid": 2,
			"level": 1,
			"sp": 99
		},
		"reward": {
			"wid": 1,
			"pid": 2,
			"level": 1,
			"sp": 99
		}
	}
}
```

[抽取失败]()

* 99: 技能点数不足



## reset_skill_point_weapon

##### 发送消息JSON格式

重制技能点，消耗的物品与数量参考`weapon_config.json`，目前对物品为固定金币，未来需要根据配置表修改对其消耗品修改，比如改成钻石，卷轴等

> weapon : 给到指定的weapon id，对其进行技能重制

```json
{
	"world": 0, 
	"function": "reset_skill_point_weapon",
	"data": {
		"token": "token",
		"weapon": 1
	}
}
```

##### 接受消息JSON格式

[抽取成功]()

> remaining：0表示物品的物品种类为武器，`wid`表示武器的id，`sp`表示武器的被动技能点数，`3`表示物品种类为物品，`iid`表示物品id为1，`value`物品剩余量
>
> reward：表示与上述一样，此值均为变化量

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"remaining": {
			"0": {
				"wid": 1,
				"sp": 100
			},
			"3": {
				"iid": 1,
				"value": 1967
			}
		},
		"reward": {
			"0": {
				"wid": 1,
				"sp": 100
			},
			"3": {
				"iid": 1,
				"value": 100
			}
		}
	}
}
```

[抽取失败]()

* 99: 目标武器错误
* 98: 金币不足

