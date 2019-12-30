## 方法列表

* [`get_config_lottery`](##get_config_lottery)

* [`basic_summon`](##basic_summon)

* [`pro_summon`](##pro_summon)

* [`friend_summon`](##friend_summon)

* [`basic_summon_skill`](##basic_summon_skill)

* [`pro_summon_skill`](##pro_summon_skill)

* [`friend_summon_skill`](##friend_summon_skill)

* [`basic_summon_role`](##basic_summon_role)

* [`pro_summon_role`](##pro_summon_role)

* [`friend_summon_rolel`](##friend_summon_rolel)

* [`basic_summon_10_times`](##basic_summon_10_times)

* [`pro_summon_10_times`](##pro_summon_10_times)

* [`friend_summon_10_times`](##friend_summon_10_times)

* [`basic_summon_skill_10_times`](##basic_summon_skill_10_times)

* [`pro_summon_skill_10_times`](##pro_summon_skill_10_times)

* [`friend_summon_skill_10_times`](##friend_summon_skill_10_times)

* [`basic_summon_role_10_times`](##basic_summon_role_10_times)

* [`pro_summon_role_10_times`](##pro_summon_role_10_times)

* [`friend_summon_role_10_times`](##friend_summon_role_10_times)

* ## <font color=#FFBB00>以下方法为新增方法</font>

* [`refresh_diamond_store`](##refresh_diamond_store)

* [`refresh_coin_store`](##refresh_coin_store)

* [`refresh_gift_store`](##refresh_gift_store)

* [`single_pump_diamond`](##single_pump_diamond)

* [`single_pump_coin`](##single_pump_coin)

* [`single_pump_gift`](##single_pump_gift)

* [`dozen_pump_diamond`](##dozen_pump_diamond)

  

## get_config_lottery

##### 发送消息JSON格式

获得抽奖配置用于客户端展示，主要用于客户端，消耗物品数量展示，配置文件来自`lottery.json`

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

[挂机关卡不同]()

> config：每一类物品所需消耗的资源，使用此类物品抽奖需要消耗的数量
>

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"config": {
			"skills": {
				"BASIC": {
					"3:1": 100,
					"3:5": 100,
					"3:11": 1,
					"3:16": 10,
					"3:13": 1,
					"3:12": 1
				},
				"PRO": {
					"3:1": 1000,
					"3:5": 1000,
					"3:11": 10,
					"3:16": 100,
					"3:13": 10,
					"3:12": 10
				},
				"FRIEND": {
					"3:1": 100,
					"3:5": 100,
					"3:11": 1,
					"3:16": 10,
					"3:13": 1,
					"3:12": 1
				},
				"PROPHET": {
					"3:1": 100,
					"3:5": 100,
					"3:11": 1,
					"3:16": 10,
					"3:13": 1,
					"3:12": 1
				}
			},
			"weapons": {
				"BASIC": {
					"3:1": 100,
					"3:5": 100,
					"3:11": 1,
					"3:16": 10,
					"3:13": 1,
					"3:12": 1
				},
				"PRO": {
					"3:1": 1000,
					"3:5": 1000,
					"3:11": 10,
					"3:16": 100,
					"3:13": 10,
					"3:12": 10
				},
				"FRIEND": {
					"3:1": 100,
					"3:5": 100,
					"3:11": 1,
					"3:16": 10,
					"3:13": 1,
					"3:12": 1
				},
				"PROPHET": {
					"3:1": 100,
					"3:5": 100,
					"3:11": 1,
					"3:16": 10,
					"3:13": 1,
					"3:12": 1
				}
			},
			"roles": {
				"BASIC": {
					"3:1": 100,
					"3:5": 100,
					"3:11": 1,
					"3:16": 10,
					"3:13": 1,
					"3:12": 1
				},
				"PRO": {
					"3:1": 1000,
					"3:5": 1000,
					"3:11": 10,
					"3:16": 100,
					"3:13": 10,
					"3:12": 10
				},
				"FRIEND": {
					"3:1": 100,
					"3:5": 100,
					"3:11": 1,
					"3:16": 10,
					"3:13": 1,
					"3:12": 1
				},
				"PROPHET": {
					"3:1": 100,
					"3:5": 100,
					"3:11": 1,
					"3:16": 10,
					"3:13": 1,
					"3:12": 1
				}
			},
			"fortune_wheel": {
				"BASIC": {
					"3:1": 100,
					"3:5": 100,
					"3:11": 1,
					"3:16": 10,
					"3:13": 1,
					"3:12": 1
				},
				"PRO": {
					"3:1": 1000,
					"3:5": 1000,
					"3:11": 10,
					"3:16": 100,
					"3:13": 10,
					"3:12": 10
				},
				"FRIEND": {
					"3:1": 100,
					"3:5": 100,
					"3:11": 1,
					"3:16": 10,
					"3:13": 1,
					"3:12": 1
				},
				"PROPHET": {
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
}
```



## basic_summon

##### 发送消息JSON格式

基础召唤武器，

> item：表示需要消耗的物品，物品列表为item类，参考enums.py，常用有1（金币），5（钻石），11，12（基础召唤，高级召唤），如果`有此武器`则为`30`碎片，如果`没有此武器`，则奖励武器。不同的抽奖方式只是获得的概率不同，概率可以参考`lottery.json`

* 2: 获得武器成功
* 3: 获得碎片成功

```json
{
	"world": 0,
	"function": "basic_summon",
	"data": {
		"token": "my token",
    	"item":5
	}
}
```

##### 接受消息JSON格式

[抽取成功]()

> remaining：抽取之后资源的总量
>
> reward: 抽取之后资源的变化量

```json
{
	"status": 2,
	"message": "new weapon unlocked",
	"data": {
		"remaining": {
			"weapon": 10,
			"star": 1,
			"segment": 0,
			"cost_item": 1,
			"cost_quantity": 12670
		},
		"reward": {
            "weapon": 10,
            "star": 1,
            "segment": 0,
            "cost_item": 1,
			"cost_quantity": 100
		}
	}
}
```

[调整关卡失败]()

- 97：需要消耗的物品id类型不对
- 98：需要消耗的物品id不对

* 99：资源不足



## pro_summon

##### 发送消息JSON格式

基础召唤武器，

> item：表示需要消耗的物品，物品列表为item类，参考enums.py，常用有1（金币），5（钻石），11，12（基础召唤，高级召唤），如果`有此武器`则为30碎片，如果`没有此武器`，则奖励武器。不同的抽奖方式只是获得的概率不同，概率可以参考`lottery.json`

* 2: 获得武器成功
* 3: 获得碎片成功

```json
{
	"world": 0,
	"function": "pro_summon",
	"data": {
		"token": "my token",
    	"item":5
	}
}
```

##### 接受消息JSON格式

[抽取成功]()

> remaining：抽取之后资源的总量
>
> reward: 抽取之后资源的变化量

```json
{
	"status": 2,
	"message": "new weapon unlocked",
	"data": {
		"remaining": {
			"weapon": 10,
			"star": 1,
			"segment": 0,
			"cost_item": 11,
			"cost_quantity": 12670
		},
		"reward": {
			"weapon": 10,
			"star": 1,
      		"segment": 0,
      		"cost_item": 11,
			"cost_quantity": 100
		}
	}
}
```

[调整关卡失败]()

- 97：需要消耗的物品id类型不对
- 98：需要消耗的物品id不对

* 99：资源不足



## friend_summon

##### 发送消息JSON格式

基础召唤武器，

> item：表示需要消耗的物品，物品列表为item类，参考enums.py，常用有1（金币），5（钻石），11，12（基础召唤，高级召唤），如果`有此武器`则为30碎片，如果`没有此武器`，则奖励武器。不同的抽奖方式只是获得的概率不同，概率可以参考`lottery.json`

* 2: 获得武器成功
* 3: 获得碎片成功

```json
{
	"world": 0,
	"function": "friend_summon",
	"data": {
		"token": "my token",
    	"item":5
	}
}
```

##### 接受消息JSON格式

[抽取成功]()

> remaining：抽取之后资源的总量
>
> reward: 抽取之后资源的变化量

```json
{
	"status": 2,
	"message": "new weapon unlocked",
	"data": {
		"remaining": {
			"weapon": 10,
			"star": 1,
			"segment": 0,
			"cost_item": 11,
			"cost_quantity": 12670
		},
		"reward": {
			"weapon": 10,
			"star": 1,
      		"segment": 0,
      		"cost_item": 11,
			"cost_quantity": 100
		}
	}
}
```

[调整关卡失败]()

- 97：需要消耗的物品id类型不对
- 98：需要消耗的物品id不对

* 99：资源不足



## basic_summon_skill

##### 发送消息JSON格式

基础召唤武器，

> item：表示需要消耗的物品，物品列表为item类，参考enums.py，常用有1（金币），5（钻石），11，12（基础召唤，高级召唤），如果`有此技能`则奖励卷轴，如果`没有此技能`，则奖励技能。不同的抽奖方式只是获得的概率不同，概率可以参考`lottery.json`

* 0: 获得技能成功
* 1: 获得`30%`卷轴成功

```json
{
	"world": 0,
	"function": "basic_summon_skill",
	"data": {
		"token": "my token",
    	"item":5
	}
}
```

##### 接受消息JSON格式

[抽取成功]()

> remaining：抽取之后资源的总量
>
> reward: 抽取之后资源的变化量

```json
{
	"status": 0,
	"message": "new skill unlocked",
	"data": {
		"remaining": {
			"skill": 13,
			"level": 1,
            "scroll_id":-1,
            "scroll_quantity":-1,
			"cost_item": 11,
			"cost_quantity": 999999997
		},
		"reward": {
			"skill": 13,
			"level": 1,
            "scroll_id":-1,
            "scroll_quantity":-1,
			"cost_item": 11,
			"cost_quantity": 10
		}
	}
}
```

[调整关卡失败]()

- 97：需要消耗的物品id类型不对
- 98：需要消耗的物品id不对

* 99：资源不足



## pro_summon_skill

##### 发送消息JSON格式

基础召唤武器，

> item：表示需要消耗的物品，物品列表为item类，参考enums.py，常用有1（金币），5（钻石），11，12（基础召唤，高级召唤），如果`有此技能`则奖励卷轴，如果`没有此技能`，则奖励技能。不同的抽奖方式只是获得的概率不同，概率可以参考`lottery.json`

* 0: 获得技能成功
* 1: 获得`100%`卷轴成功

```json
{
	"world": 0,
	"function": "pro_summon_skill",
	"data": {
		"token": "my token",
    	"item":5
	}
}
```

##### 接受消息JSON格式

[抽取成功]()

> remaining：抽取之后资源的总量
>
> reward: 抽取之后资源的变化量

```json
{
	"status": 0,
	"message": "new skill unlocked",
	"data": {
		"remaining": {
			"skill": 13,
			"level": 1,
			"cost_item": 11,
			"cost_quantity": 999999997,
            "scroll_id":0,
            "scroll_quantity":0
		},
		"reward": {
			"skill": 13,
			"level": 1,
			"cost_item": 11,
			"cost_quantity": 10,
            "scroll_id":0,
            "scroll_quantity":0
		}
	}
}
```

[调整关卡失败]()

- 97：需要消耗的物品id类型不对
- 98：需要消耗的物品id不对

* 99：资源不足



## friend_summon_skill

##### 发送消息JSON格式

基础召唤武器，

> item：表示需要消耗的物品，物品列表为item类，参考enums.py，常用有1（金币），5（钻石），11，12（基础召唤，高级召唤），如果`有此技能`则奖励卷轴，如果`没有此技能`，则奖励技能。不同的抽奖方式只是获得的概率不同，概率可以参考`lottery.json`

* 0: 获得技能成功
* 1: 获得`10%`卷轴成功

```json
{
	"world": 0,
	"function": "friend_summon_skill",
	"data": {
		"token": "my token",
    	"item":5
	}
}
```

##### 接受消息JSON格式

[抽取成功]()

> remaining：抽取之后资源的总量
>
> reward: 抽取之后资源的变化量

```json
{
	"status": 0,
	"message": "new skill unlocked",
	"data": {
		"remaining": {
			"skill": 13,
			"level": 1,
			"cost_item": 11,
			"cost_quantity": 999999997,
      		"scroll_id": -1,
      		"scroll_quantity": -1
		},
		"reward": {
			"skill": 13,
			"level": 1,
			"cost_item": 11,
			"cost_quantity": 10,
      		"scroll_id": -1,
      		"scroll_quantity": -1
		}
	}
}
```

[调整关卡失败]()

- 97：需要消耗的物品id类型不对
- 98：需要消耗的物品id不对

* 99：资源不足



## basic_summon_role

##### 发送消息JSON格式

基础召唤武器，

> item：表示需要消耗的物品，物品列表为item类，参考enums.py，常用有1（金币），5（钻石），11，12（基础召唤，高级召唤），如果`有此武器`则为`30`碎片，如果`没有此武器`，则奖励武器。不同的抽奖方式只是获得的概率不同，概率可以参考`lottery.json`

* 4: 获得角色成功
* 5: 角色重复，获得碎片

```json
{
	"world": 0,
	"function": "basic_summon_role",
	"data": {
		"token": "my token",
    	"item":5
	}
}
```

##### 接受消息JSON格式

[抽取成功]()

> remaining：抽取之后资源的总量
>
> reward: 抽取之后资源的变化量

```json
{
	"status": 4,
	"message": "new role unlocked",
	"data": {
		"remaining": {
			"role": 10,
			"star": 1,
			"segment": 0,
			"cost_item": 1,
			"cost_quantity": 12670
		},
		"reward": {
			"role": 10,
			"star": 1,
			"segment": 0,
			"cost_item": 11,
			"cost_quantity": 1
		}
	}
}
```

[调整关卡失败]()

- 97：需要消耗的物品id类型不对
- 98：需要消耗的物品id不对

* 99：资源不足





## pro_summon_role

##### 发送消息JSON格式

基础召唤武器，

> item：表示需要消耗的物品，物品列表为item类，参考enums.py，常用有1（金币），5（钻石），11，12（基础召唤，高级召唤），如果`有此武器`则为`30`碎片，如果`没有此武器`，则奖励武器。不同的抽奖方式只是获得的概率不同，概率可以参考`lottery.json`

* 4: 获得角色成功
* 5: 角色重复，获得碎片

```json
{
	"world": 0,
	"function": "basic_summon_role",
	"data": {
		"token": "my token",
    	"item":5
	}
}
```

##### 接受消息JSON格式

[抽取成功]()

> remaining：抽取之后资源的总量
>
> reward: 抽取之后资源的变化量

```json
{
	"status": 0,
	"message": "new skill unlocked",
	"data": {
		"remaining": {
			"role": 10,
			"star": 1,
			"segment": 0,
			"cost_item": 11,
			"cost_quantity": 12670
		},
		"reward": {
			"role": 10,
			"star": 1,
			"segment": 0,
			"cost_item": 11,
			"cost_quantity": 1
		}
	}
}
```

[调整关卡失败]()

- 97：需要消耗的物品id类型不对
- 98：需要消耗的物品id不对
- 99：资源不足



## friend_summon_role

##### 发送消息JSON格式

基础召唤武器，

> item：表示需要消耗的物品，物品列表为item类，参考enums.py，常用有1（金币），5（钻石），11，12（基础召唤，高级召唤），如果`有此武器`则为`30`碎片，如果`没有此武器`，则奖励武器。不同的抽奖方式只是获得的概率不同，概率可以参考`lottery.json`

* 4: 获得角色成功
* 5: 角色重复，获得碎片

```json
{
	"world": 0,
	"function": "basic_summon_role",
	"data": {
		"token": "my token",
    	"item":5
	}
}
```

##### 接受消息JSON格式

[抽取成功]()

> remaining：抽取之后资源的总量
>
> reward: 抽取之后资源的变化量

```json
{
	"status": 0,
	"message": "new skill unlocked",
	"data": {
		"remaining": {
			"role": 10,
			"star": 1,
			"segment": 0,
			"cost_item": 11,
			"cost_quantity": 12670
		},
		"reward": {
			"role": 10,
			"star": 1,
			"segment": 0,
			"cost_item": 11,
			"cost_quantity": 1
		}
	}
}
```

[调整关卡失败]()

- 97：需要消耗的物品id类型不对
- 98：需要消耗的物品id不对
- 99：资源不足



## basic_summon_10_times

## pro_summon_10_times

## friend_summon_10_times

##### 发送消息JSON格式

基础召唤武器，

> item：表示需要消耗的物品，物品列表为item类，参考enums.py，常用有1（金币），5（钻石），11，12（基础召唤，高级召唤），如果`有此武器`则为30碎片，如果`没有此武器`，则奖励武器。不同的抽奖方式只是获得的概率不同，概率可以参考`lottery.json`，返回的物品相比单词抽取只是多了列表形式

```json
{
	"world": 0,
	"function": "basic_summon_10_times",
	"data": {
		"token": "my token",
    	"item":5
	}
}
```

##### 接受消息JSON格式

[抽取成功]()

> remaining：抽取之后资源的总量
>
> reward: 抽取之后资源的变化量

```json
{
	"status": 2,
	"message": "new weapon unlocked",
	"data": {
		"remaining": {
            "0":{
                "weapon": 10,
                "star": 1,
                "segment": 0,
                "cost_item": 1,
                "cost_quantity": 12670
            },
            "1":{
                "weapon": 10,
                "star": 1,
                "segment": 0,
                "cost_item": 1,
                "cost_quantity": 12670
            },
      
      .......
      
            "10":{
                "weapon": 10,
                "star": 1,
                "segment": 0,
                "cost_item": 1,
                "cost_quantity": 12670
        	}
		},
		"reward": {
            "0":{
                "weapon": 10,
                "star": 1,
                "segment": 0,
                "cost_item": 1,
                "cost_quantity": 100
            },
     	  	"1":{
                "weapon": 10,
                "star": 1,
                "segment": 0,
                "cost_item": 1,
                "cost_quantity": 100
        	},
      
      ........
      
            "10":{
                "weapon": 10,
                "star": 1,
                "segment": 0,
                "cost_item": 1,
                "cost_quantity": 100
            },
		}
	}
}
```

[调整关卡失败]()

- 97：需要消耗的物品id类型不对
- 98：需要消耗的物品id不对

* 99：资源不足

##

- ## basic_summon_skill_10_times

- ## pro_summon_skill_10_times

- ## friend_summon_skill_10_times

##### 发送消息JSON格式

基础召唤武器，

> item：表示需要消耗的物品，物品列表为item类，参考enums.py，常用有1（金币），5（钻石），11，12（基础召唤，高级召唤），如果`有此技能`则奖励卷轴，如果`没有此技能`，则奖励技能。不同的抽奖方式只是获得的概率不同，概率可以参考`lottery.json，返回的物品相比单词抽取只是多了列表形式`

```json
{
	"world": 0,
	"function": "basic_summon_10_times",
	"data": {
		"token": "my token",
    	"item":5
	}
}
```

##### 接受消息JSON格式

[抽取成功]()

> remaining：抽取之后资源的总量
>
> reward: 抽取之后资源的变化量

```json
{
	"status": 2,
	"message": "success",
	"data": {
		"remaining": {
            "0":{
                "skill": 13,
                "level": 1,
                "cost_item": 11,
                "cost_quantity": 999999997,
                "scroll_id": -1,
                "scroll_quantity": -1
            },
            "1":{
                "skill": 13,
                "level": 1,
                "cost_item": 11,
                "cost_quantity": 999999997,
                "scroll_id": -1,
                "scroll_quantity": -1
      		},
      
      .......

           "10":{
                "skill": 13,
                "level": 1,
                "cost_item": 11,
                "cost_quantity": 999999997,
                "scroll_id": -1,
                "scroll_quantity": -1
            }
		},
		"reward": {
            "0":{
                "skill": 13,
                "level": 1,
                "cost_item": 11,
                "cost_quantity": 1,
                "scroll_id": -1,
                "scroll_quantity": -1
            },
            "1":{
                "skill": 13,
                "level": 1,
                "cost_item": 11,
                "cost_quantity": 1,
                "scroll_id": -1,
                "scroll_quantity": -1
            },
      
      ........

            "10":{
                "skill": 13,
                "level": 1,
                "cost_item": 11,
                "cost_quantity": 1,
                "scroll_id": -1,
                "scroll_quantity": -1
            },
		}
	}
}
```

[调整关卡失败]()

- 97：需要消耗的物品id类型不对
- 98：需要消耗的物品id不对

* 99：资源不足



- ## basic_summon_role_10_times

- ## pro_summon_role_10_times

- ## friend_summon_role_10_times

##### 发送消息JSON格式

基础召唤武器，

> item：表示需要消耗的物品，物品列表为item类，参考enums.py，常用有1（金币），5（钻石），11，12（基础召唤，高级召唤），如果`有此角色`则为30碎片，如果`没有此角色`，则奖励武器。不同的抽奖方式只是获得的概率不同，概率可以参考`lottery.json`，返回的物品相比单词抽取只是多了列表形式

```json
{
	"world": 0,
	"function": "basic_summon_10_times",
	"data": {
		"token": "my token",
    	"item":5
	}
}
```

##### 接受消息JSON格式

[抽取成功]()

> remaining：抽取之后资源的总量
>
> reward: 抽取之后资源的变化量

```json
{
	"status": 2,
	"message": "new weapon unlocked",
	"data": {
		"remaining": {
      		"0":{
                "role": 10,
                "star": 1,
                "segment": 0,
                "cost_item": 11,
                "cost_quantity": 12670
      		},
           "1":{
                "role": 10,
                "star": 1,
                "segment": 0,
                "cost_item": 11,
                "cost_quantity": 12670
          	},
      
      .......
      
           "10":{
                "role": 10,
                "star": 1,
                "segment": 0,
                "cost_item": 11,
                "cost_quantity": 12670
          	}
		},
		"reward": {
            "0":{
                "role": 10,
                "star": 1,
                "segment": 0,
                "cost_item": 11,
                "cost_quantity": 100
            },
            "1":{
                "role": 10,
                "star": 1,
                "segment": 0,
                "cost_item": 11,
                "cost_quantity": 100
            },
      
      ........
      
            "10":{
                "role": 10,
                "star": 1,
                "segment": 0,
                "cost_item": 11,
                "cost_quantity": 100
            },
		}
	}
}
```

[调整关卡失败]()

- 97：需要消耗的物品id类型不对
- 98：需要消耗的物品id不对

* 99：资源不足



## <font color=#FFBB00>以下方法为新增方法</font>

- ## refresh_diamond_store

- ## refresh_coin_store

- ## refresh_gift_store

##### 发送消息JSON格式

> 刷新或者是获取全部随机商城信息

```json
{
	"world": 0,
	"function": "refresh_coin_store",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[成功]()

> status为0是刷新，为1是获取所有信息
>
> refresh：刷新之后获得的所有商品情况
>
> - cid：消耗品iid（1代表金币，5代表钻石，16代表朋友礼物）
> - pid：商品位置id（0-11）
> - mid：商品信息："gid:iid:qty"
> - wgt：权重值，权重越大，抽中的概率越大
> - isb：商品是否被购买（0未被购买，1已被购买）
>
> cooling: 冷却时间，剩下多少秒之后会再次刷新商城，当商城的商品被抽完之后这个值不起作用，并立刻刷新

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "refresh": [
            {
                "cid": 1,
                "pid": 11,
                "mid": "2:16:20",
                "wgt": 30,
                "isb": 0
            },
            {
                "cid": 1,
                "pid": 4,
                "mid": "1:22:1",
                "wgt": 10,
                "isb": 0
            },
            {
                "cid": 1,
                "pid": 8,
                "mid": "1:16:1",
                "wgt": 300,
                "isb": 0
            },
            {
                "cid": 1,
                "pid": 3,
                "mid": "1:22:1",
                "wgt": 300,
                "isb": 0
            },
            {
                "cid": 1,
                "pid": 2,
                "mid": "3:12:20",
                "wgt": 500,
                "isb": 0
            },
            {
                "cid": 1,
                "pid": 5,
                "mid": "3:10:20",
                "wgt": 500,
                "isb": 0
            },
            {
                "cid": 1,
                "pid": 10,
                "mid": "1:32:1",
                "wgt": 300,
                "isb": 0
            },
            {
                "cid": 1,
                "pid": 6,
                "mid": "0:1:20",
                "wgt": 200,
                "isb": 0
            },
            {
                "cid": 1,
                "pid": 9,
                "mid": "0:28:20",
                "wgt": 200,
                "isb": 0
            },
            {
                "cid": 1,
                "pid": 7,
                "mid": "0:8:20",
                "wgt": 200,
                "isb": 0
            },
            {
                "cid": 1,
                "pid": 0,
                "mid": "0:20:20",
                "wgt": 200,
                "isb": 0
            },
            {
                "cid": 1,
                "pid": 1,
                "mid": "3:19:20",
                "wgt": 500,
                "isb": 0
            }
        ],
        "cooling": 172800
    }
}
```

[失败]()

- 98：The configuration file does not exist

* 99：cid error



## single_pump_diamond

##### 发送消息JSON格式

> 刷新或者是获取全部随机商城信息

```json
{
	"world": 0,
	"function": "single_pump_gift",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[成功]()

> status为0是刷新，为1是获取所有信息
>
> remaining：物品剩余情况
>
> reward：物品的改变情况
>
> pid: 抽中的物品位置id
>
> constraint：部分约束
>
> - limit：抽奖的次数，为0时消耗的是免费次数，为1时消耗的是半价次数，后面的仅仅是今天抽奖的次数减一
> - cooling：剩余冷却时间，时间结束则刷新limit次数，时间范围0-86400

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "remaining": [
            "3:5:80",
            "3:12:20",
            "3:44:263"
        ],
        "reward": [
            "3:5:10",
            "3:12:20",
            "3:44:1"
        ],
        "pid": 3,
        "constraint": {
            "limit": 10,
            "cooling": 34623
        }
    }
}
```

[失败]()

* 98：diamond insufficient



## single_pump_coin

##### 发送消息JSON格式

> 刷新或者是获取全部随机商城信息

```json
{
	"world": 0,
	"function": "single_pump_gift",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[成功]()

> status为0是刷新，为1是获取所有信息
>
> remaining：物品剩余情况
>
> reward：物品的改变情况
>
> pid: 抽中的物品位置id
>
> constraint：部分约束
>
> - limit：剩余可抽奖的次数
> - cooling：剩余冷却时间，时间结束则刷新limit次数，时间范围0-86400

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "remaining": [
            "3:1:80",
            "3:12:20",
            "3:44:263"
        ],
        "reward": [
            "3:1:10",
            "3:12:20",
            "3:44:1"
        ],
        "pid": 3,
        "constraint": {
            "limit": 10,
            "cooling": 34623
        }
    }
}
```

[失败]()

- 96：Insufficient number of lucky draw

* 98：coin insufficient



## single_pump_gift

##### 发送消息JSON格式

> 刷新或者是获取全部随机商城信息

```json
{
	"world": 0,
	"function": "single_pump_gift",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[成功]()

> status为0是刷新，为1是获取所有信息
>
> remaining：物品剩余情况
>
> reward：物品的改变情况
>
> pid: 抽中的物品位置id
>
> constraint：部分约束
>
> - limit：剩余可抽奖的次数
> - cooling：剩余冷却时间，时间结束则刷新limit次数，时间范围0-86400

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "remaining": [
            "3:16:80",
            "3:12:20",
            "3:44:263"
        ],
        "reward": [
            "3:16:10",
            "3:12:20",
            "3:44:1"
        ],
        "pid": 3
    }
}
```

[失败]()

* 98：friend gift insufficient



## dozen_pump_diamond

##### 发送消息JSON格式

> 钻石12抽，一次性获取所有的物资，同时积分得到双倍

```json
{
	"world": 0,
	"function": "dozen_pump_diamond",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[成功]()

> status为0是刷新，为1是获取所有信息
>
> remaining：物品剩余情况
>
> reward：物品的改变情况
>
> pid：这个是象征性的返回，代表所有物品被清空购买并再次刷新
>
> refresh：同时刷新所有商品得到的商品信息
>
> cooling：冷却时间，剩下多少秒之后会再次刷新商城，当商城的商品被抽完之后这个值不起作用，并立刻刷新

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "remaining": [
            "3:5:2800",
            "2:16:40",
            "0:24:40",
            "0:18:60",
            "2:22:20",
            "0:22:20",
            "3:43:80",
            "0:19:40",
            "2:2:20",
            "0:21:40",
            "2:4:20",
            "1:21:1",
            "2:24:40",
            "3:44:383"
        ],
        "reward": [
            "3:5:2400",
            "2:16:20",
            "0:24:20",
            "0:18:20",
            "2:22:20",
            "0:22:20",
            "3:43:20",
            "0:19:20",
            "2:2:20",
            "0:21:20",
            "2:4:20",
            "1:21:1",
            "2:24:20",
            "3:44:120"
        ],
        "pid": [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11
        ],
        "refresh": [
            {
                "cid": 5,
                "pid": 5,
                "mid": "0:18:20",
                "wgt": 30,
                "isb": 0
            },
            {
                "cid": 5,
                "pid": 4,
                "mid": "0:23:20",
                "wgt": 10,
                "isb": 0
            },
            {
                "cid": 5,
                "pid": 8,
                "mid": "2:18:20",
                "wgt": 30,
                "isb": 0
            },
            {
                "cid": 5,
                "pid": 10,
                "mid": "2:24:20",
                "wgt": 10,
                "isb": 0
            },
            {
                "cid": 5,
                "pid": 2,
                "mid": "1:29:1",
                "wgt": 5,
                "isb": 0
            },
            {
                "cid": 5,
                "pid": 11,
                "mid": "3:43:20",
                "wgt": 25,
                "isb": 0
            },
            {
                "cid": 5,
                "pid": 7,
                "mid": "3:10:20",
                "wgt": 500,
                "isb": 0
            },
            {
                "cid": 5,
                "pid": 9,
                "mid": "3:18:20",
                "wgt": 500,
                "isb": 0
            },
            {
                "cid": 5,
                "pid": 1,
                "mid": "3:2:20",
                "wgt": 500,
                "isb": 0
            },
            {
                "cid": 5,
                "pid": 3,
                "mid": "0:15:20",
                "wgt": 200,
                "isb": 0
            },
            {
                "cid": 5,
                "pid": 6,
                "mid": "3:10:20",
                "wgt": 500,
                "isb": 0
            },
            {
                "cid": 5,
                "pid": 0,
                "mid": "3:22:20",
                "wgt": 500,
                "isb": 0
            }
        ],
        "cooling": 172800
    }
}
```

[失败]()

* 99：diamond insufficient
* 98：Less than {GRID} grid