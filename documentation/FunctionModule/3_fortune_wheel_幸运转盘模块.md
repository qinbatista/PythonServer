## 方法列表

* [`get_fortune_wheel_config`](##get_fortune_wheel_config)
* [`fortune_wheel_basic`](##fortune_wheel_basic)
* [`fortune_wheel_pro`](##fortune_wheel_pro)



## get_config_lottery

##### 发送消息JSON格式

获取抽奖信息

> 获取各个抽奖的参数，参数来源`lottery.json`,抽奖的物品根据配置表设置而获得，高级抽和低级抽`内容一样`，`概率不一样`,配置表需要做相应的修改

```json
{
	"world": 0,
	"function": "get_config_lottery",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[抽取成功]()

> config：幸运转盘的配置表，包括多少消耗品，概率，奖励物品等
>
> timer: 表示免费抽奖的倒计时，如果没有倒计时，说明可以免费抽奖，如果有倒计时，则表示需要相应的物品才能抽奖, `一天之能免费抽一次`。

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"config": {
			"skills": {
				"3:1": 100,
				"3:5": 100,
				"3:11": 1,
				"3:16": 10,
				"3:13": 1,
				"3:12": 1
			},
			"weapons": {
				"3:1": 100,
				"3:5": 100,
				"3:11": 1,
				"3:16": 10,
				"3:13": 1,
				"3:12": 1
			},
			"roles": {
				"3:1": 100,
				"3:5": 100,
				"3:11": 1,
				"3:16": 10,
				"3:13": 1,
				"3:12": 1
			},
			"fortune_wheel": {
				"3:1": 100,
				"3:5": 100,
				"3:11": 1,
				"3:16": 10,
				"3:13": 1,
				"3:12": 1
			}
		}
	}
}
```



## fortune_wheel_basic

##### 发送消息JSON格式

普通抽奖

> 转盘抽奖可以获得游戏内大部分物品，其中`武器`和`角色`均以`碎片`的形式存在，其余物品按照正常数值相加相减即可，抽奖每天第一天可以免费抽取。想要知道抽奖信息，抽奖概率，有哪些物品等信息获取抽奖信息需要调用get_fortune_wheel_config才能知道具体的信息

```json
{
	"world": 0, 
	"function": "fortune_wheel_basic",
	"data": {
		"token": "my toekn ^_^",
    	"item": 1,
	}
}
```

##### 接受消息JSON格式

* 0: 获得新技能
* 1: 获得重复，变为卷轴
* 2: 获得新武器
* 3: 获得武器碎片
* 4: 获得新角色
* 5: 获得角色碎片
* 6: 获得通用物品

[抽取成功]()

> remaining：变化数据的总和，`group_id`物品的分类id，`enum_id`此分类下的物品id, `item_quantity`物品的数量，
>
> reward：数据的改变量

***0，1通用格式***

```json
{
	"status": 1,
	"message": "get scroll",
	"data": {
		"remaining": {
			"skill": -1,
			"level": -1,
			"scroll_id": 6,
			"scroll_quantity": 24,
			"cost_item": 5,
			"cost_quantity": 297780
		},
		"reward": {
			"skill": -1,
			"level": -1,
			"scroll_id": 6,
			"scroll_quantity": 1,
			"cost_item": 5,
			"cost_quantity": 100
		}
	}
}
```

***2，3通用格式***

```json
{
	"status": 3,
	"message": "get segment",
	"data": {
		"remaining": {
			"weapon": 1,
			"star": 1,
			"segment": 40,
			"cost_item": 5,
			"cost_quantity": 296780
		},
		"reward": {
			"weapon": 1,
			"star": 0,
			"segment": 30,
			"cost_item": 5,
			"cost_quantity": 100
		}
	}
}
```

***4，5通用格式***

```json
{
	"status": 5,
	"message": "get segment",
	"data": {
		"remaining": {
			"role": 6,
			"star": 1,
			"segment": 300,
			"cost_item": 5,
			"cost_quantity": 255080
		},
		"reward": {
			"role": 6,
			"star": 0,
			"segment": 30,
			"cost_item": 5,
			"cost_quantity": 100
		}
	}
}
```

***6通用格式***


```json
{
	"status": 6,
	"message": "get item",
	"data": {
		"remaining": {
			"item_id": "6",
			"item_quantity": 22,
			"cost_item": 5,
			"cost_quantity": 297980
		},
		"reward": {
			"item_id": "6",
			"item_quantity": 1,
			"cost_item": 5,
			"cost_quantity": 100
		}
	}
}
```


[抽取失败]()

* 99: 资源不足



## fortune_wheel_pro

##### 发送消息JSON格式

高级抽奖

> item：表示需要消耗的物品，物品列表为item类，参考enums.py，常用有1（金币），5（钻石），11，12（基础召唤，高级召唤），如果`有此武器`则为`30`碎片，如果`没有此武器`，则奖励武器。不同的抽奖方式只是获得的概率不同，概率可以参考`lottery.json`

```json
{
	"world": 0,
	"function": "fortune_wheel_pro",
	"data": {
		"token": "my token",
    "item":5
	}
}
```

##### 接受消息JSON格式

* 0: 获得新技能
* 1: 获得重复，变为卷轴
* 2: 获得新武器
* 3: 获得武器碎片
* 4: 获得新角色
* 5: 获得角色碎片
* 6: 获得通用物品

[抽取成功]()

> remaining：抽取之后资源的总量
>
> reward: 抽取之后资源的变化量

***0，1通用格式***

```json
{
	"status": 1,
	"message": "get scroll",
	"data": {
		"remaining": {
			"skill": -1,
			"level": -1,
			"scroll_id": 6,
			"scroll_quantity": 24,
			"cost_item": 5,
			"cost_quantity": 297780
		},
		"reward": {
			"skill": -1,
			"level": -1,
			"scroll_id": 6,
			"scroll_quantity": 1,
			"cost_item": 5,
			"cost_quantity": 100
		}
	}
}
```

***2，3通用格式***

```json
{
	"status": 3,
	"message": "get segment",
	"data": {
		"remaining": {
			"weapon": 1,
			"star": 1,
			"segment": 40,
			"cost_item": 5,
			"cost_quantity": 296780
		},
		"reward": {
			"weapon": 1,
			"star": 0,
			"segment": 30,
			"cost_item": 5,
			"cost_quantity": 100
		}
	}
}
```

***4，5通用格式***

```json
{
	"status": 5,
	"message": "get segment",
	"data": {
		"remaining": {
			"role": 6,
			"star": 1,
			"segment": 300,
			"cost_item": 5,
			"cost_quantity": 255080
		},
		"reward": {
			"role": 6,
			"star": 0,
			"segment": 30,
			"cost_item": 5,
			"cost_quantity": 100
		}
	}
}
```

***6通用格式***


```json
{
	"status": 6,
	"message": "get item",
	"data": {
		"remaining": {
			"item_id": "6",
			"item_quantity": 22,
			"cost_item": 5,
			"cost_quantity": 297980
		},
		"reward": {
			"item_id": "6",
			"item_quantity": 1,
			"cost_item": 5,
			"cost_quantity": 100
		}
	}
}
```

[抽取失败]()

* 99: 资源不足


