## 方法列表

* [`get_all_role`](##get_all_role)
* [`level_up_role`](##level_up_role)
* [`level_up_star_role`](##level_up_star_role)
* [`unlock_passive_role`](##unlock_passive_role)
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

> roles：玩家的角色详细数据，`rid`角色id，`star`角色星数，`level`角色等级，`seg`角色碎片，p101-p199为角色被动技能，p后面的数值为被动技能代号，0代表未解锁，1代表已解锁

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "roles": [
            {
                "rid": 1,
                "star": 1,
                "level": 18,
                "seg": 0,
                "101": 1,
                "102": 0,
                "103": 0,
                "104": 0,
                "105": 0,
                "106": 0,
                "107": 0,
                "108": 0,
                "109": 0,
                "110": 0
            }
        ]
    }
}
```





## level_up_role

##### 发送消息JSON格式

升级武器等级，升级武器消耗的铁参考weapon_config.json

> role：指定需要升级的角色id
>
> delta：角色需要升级的增量，只能为正整数

```json
{
	"world": 0,
	"function": "level_up_role",
	"data": {
		"token": "my token",
		"role": 24,
		"delta": 1
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
		"remaining": {
			"2": {
				"rid": 1,
				"level": 120
			},
			"3": [
				{
					"iid": 9,
					"value": 101013190
				}
			]
		},
		"reward": {
			"2": {
				"rid": 1,
				"level": 1
			},
			"3": [
				{
					"iid": 9,
					"value": -1303290
				}
			]
		}
	}
}
```

[失败]()

* 99: 非法的角色id
* 98: 材料过少或者等级已满
* 97: 材料不足
* 96: 没有此角色
* 95: 你的角色已达到满级



## level_up_star_role

##### 发送消息JSON格式

角色的升级需要消耗该角色的碎片，角色碎片的消耗量参考roles.json

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



## unlock_passive_role

##### 发送消息JSON格式

解锁角色被动技能

> rid：角色的id
>
> pid：角色被动技能id

```json
{
	"world": 0, 
	"function": "unlock_passive_role",
	"data": {
		"token": "my toekn ^_^",
		"rid": 1,
        "pid": 101
	}
}
```

##### 接受消息JSON格式

[成功]()

> `rid`角色id，`pid`最新解锁的被动技能id
>
> consume：消耗品信息，分别拼接的是组id，物品id，剩余量，消耗量

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "rid": 1,
        "pid": 102,
        "consume": "3:1:90000:10000"
    }
}
```

[失败]()

* 99: Role id error
* 98: Passive skill id error
* 97: invalid target
* 96: You don't have the role
* 95: Your role level has not reached the unlock level
* 94: This passive is unlocked
* 93: insufficient coin




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

返回转盘和抽奖的消耗信息，配置文件来自roles.json

[成功]()

> roles：返回roles.json
>
> seg：角色突破需要消耗的碎片基础数据
>
> exp_pot：角色升级需要消耗的经验

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"roles": {
			"standard_costs" :
			{
				"exp_pot" : 5,
				"seg" : 25
			}
		}
	}
}
```




