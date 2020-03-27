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

* [`buy_refresh_diamond`](##buy_refresh_diamond)

* [`buy_refresh_coin`](##buy_refresh_coin)

* [`buy_refresh_gift`](##buy_refresh_gift)

* [`single_pump_diamond`](##single_pump_diamond)

* [`single_pump_coin`](##single_pump_coin)

* [`single_pump_gift`](##single_pump_gift)

* [`dozen_pump_diamond`](##dozen_pump_diamond)

* [`dozen_pump_coin`](##dozen_pump_coin)

* [`dozen_pump_gift`](##dozen_pump_gift)

- [`integral_convert`](##integral_convert)



### 错误集

```python
# 99 - insufficient materials
# 98 - error item
# 97 - error item, item type
# 96 - Less than 12 grid
# 95 - Insufficient number of lucky draw
# 94 - cid error
# 93 - The configuration file does not exist
```





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
> - pid：商品位置id（0-11）
> - mid：商品信息："gid:iid:qty"
> - wgt：权重值，权重越大，抽中的概率越大
> - isb：商品是否被购买（0未被购买，1已被购买）
>
> constraint：部分约束
>
> - limit：refresh_diamond_store下返回的是今天抽奖的次数，refresh_coin_store下返回的是抽奖剩余次数
> - cid：消耗品iid（1代表金币，5代表钻石，16代表朋友礼物）
> - cooling: 冷却时间，剩下多少秒之后会再次刷新商城，当商城的商品被抽完之后这个值不起作用，并立刻刷新
> - cooling_refresh：距离下一次可免费时间需要的冷却时间，小于等于0时可进行免费刷新
> - qty：购买单个物品需要的对应物品数量
> - refresh：手动刷新需要的钻石数量（当cooling_refresh小于等于0时可免费刷新）
> - acp：积分进度情况

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "refresh": [
            {
                "pid": 3,
                "mid": "2:18:20",
                "wgt": 30,
                "isb": 0
            },
            {
                "pid": 4,
                "mid": "1:25:1",
                "wgt": 10,
                "isb": 0
            },
            ... ...
            {
                "pid": 2,
                "mid": "3:7:5",
                "wgt": 500,
                "isb": 0
            }
        ],
        "constraint": {
            "cooling_refresh": 0,
            "cid": 1,
            "limit": 12,
            "qty": 10000,
            "refresh": 20,
            "cooling": 172800,
            "acp": 200
        }
    }
}
```

[失败]()

- 93：The configuration file does not exist

* 94：cid error




- ## buy_refresh_diamond

- ## buy_refresh_coin

- ## buy_refresh_gift

##### 发送消息JSON格式

> 刷新或者是获取全部随机商城信息

```json
{
	"world": 0,
	"function": "buy_refresh_diamond",
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
> - pid：商品位置id（0-11）
> - mid：商品信息："gid:iid:qty"
> - wgt：权重值，权重越大，抽中的概率越大
> - isb：商品是否被购买（0未被购买，1已被购买）
>
> constraint：部分约束
>
> - limit：refresh_diamond_store下返回的是今天抽奖的次数，refresh_coin_store下返回的是抽奖剩余次数
> - cid：消耗品iid（1代表金币，5代表钻石，16代表朋友礼物）
> - cooling: 冷却时间，剩下多少秒之后会再次刷新商城，当商城的商品被抽完之后这个值不起作用，并立刻刷新
> - cooling_refresh：距离下一次可免费时间需要的冷却时间，小于等于0时可进行免费刷新
> - qty：购买单个物品需要的对应物品数量
> - refresh：刷新需要的钻石数量
> - acp：积分进度情况
>
> consume：钻石消耗
>
> - remain_v：钻石剩余数量
> - value：钻石消耗的数量

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "refresh": [
            {
                "pid": 6,
                "mid": "0:16:20",
                "wgt": 30,
                "isb": 0
            },
            {
                "pid": 4,
                "mid": "3:22:1",
                "wgt": 10,
                "isb": 0
            },
            ... ...
            {
                "pid": 11,
                "mid": "0:22:20",
                "wgt": 200,
                "isb": 0
            }
        ],
        "constraint": {
            "cooling_refresh": 17629,
            "cid": 16,
            "qty": 10,
            "refresh": 20,
            "cooling": 172800,
            "acp": 200
        },
        "consume": {
            "remain_v": 0,
            "value": 0
        }
    }
}

```

[失败]()

- 93：The configuration file does not exist

* 94：cid error
* 99：insufficient materials



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
> - limit：当天抽奖的次数，第一次抽奖免费，第二次用钻石抽奖半价，12连抽不记录到当中，仅仅记录单抽次数
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

* 99：insufficient materials



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

- 95：Insufficient number of lucky draw

* 99：insufficient materials



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
        "pid": 3,
        "constraint": {
            "cooling": 172800
        }
    }
}
```

[失败]()

* 99：insufficient materials



## dozen_pump_diamond

##### 发送消息JSON格式

> 钻石12抽，一次性获取所有的物资，不足12次没有双倍积分，但可以连抽
>

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
> constraint：部分限制
>
> - cooling_refresh：距离下一次可免费时间需要的冷却时间，小于等于0时可进行免费刷新
> - limit：当天抽奖的次数，第一次抽奖免费，第二次用钻石抽奖半价，12连抽不记录到当中，仅仅记录单抽次数
>
> - cooling：冷却时间，剩下多少秒之后会再次刷新商城，当商城的商品被抽完之后这个值不起作用，并立刻刷新

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "remaining": [
            "3:5:2900",
            "3:6:10",
            "0:21:20",
            "3:43:80",
            "1:33:1",
            "2:29:20",
            "2:17:40",
            "2:22:40",
            "2:20:80",
            "3:45:5",
            "0:16:40",
            "1:26:1",
            "3:6:11",
            "3:44:238"
        ],
        "reward": [
            "3:5:2400",
            "3:6:1",
            "0:21:20",
            "3:43:20",
            "1:33:1",
            "2:29:20",
            "2:17:20",
            "2:22:20",
            "2:20:20",
            "3:45:5",
            "0:16:20",
            "1:26:1",
            "3:6:1",
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
                "pid": 0,
                "mid": "0:17:20",
                "wgt": 30,
                "isb": 0
            },
            {
                "pid": 2,
                "mid": "0:24:20",
                "wgt": 10,
                "isb": 0
            },
      		.......,
            {
                "pid": 7,
                "mid": "2:21:20",
                "wgt": 200,
                "isb": 0
            }
        ],
        "constraint": {
            "cooling_refresh": 17271,
            "cid": 5,
            "limit": 1,
            "qty": 200,
            "refresh": 50,
            "cooling": 172800
        }
    }
}
```

[失败]()

* 99：insufficient materials



## dozen_pump_coin

##### 发送消息JSON格式

> 金币12抽，不足12次依然可以连抽，不消耗今天抽奖次数
>

```json
{
	"world": 0,
	"function": "dozen_pump_coin",
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
> constraint：部分限制
>
> - cooling_refresh：距离下一次可免费时间需要的冷却时间，小于等于0时可进行免费刷新
> - limit：剩余可抽奖的次数
>
> - cooling：冷却时间，剩下多少秒之后会再次刷新商城，当商城的商品被抽完之后这个值不起作用，并立刻刷新

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "remaining": [
            "3:1:240000",
            "2:20:40",
            "3:22:17",
            "2:9:40",
            "2:20:60",
            "0:10:20",
            "3:6:8",
            "3:12:5",
            "3:6:9",
            "1:19:1",
            "2:17:20",
            "1:20:1",
            "0:11:20",
            "3:44:118"
        ],
        "reward": [
            "3:1:120000",
            "2:20:20",
            "3:22:5",
            "2:9:20",
            "2:20:20",
            "0:10:20",
            "3:6:1",
            "3:12:5",
            "3:6:1",
            "1:19:1",
            "2:17:20",
            "1:20:1",
            "0:11:20",
            "3:44:12"
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
                "pid": 11,
                "mid": "2:16:20",
                "wgt": 30,
                "isb": 0
            },
            {
                "pid": 1,
                "mid": "1:23:1",
                "wgt": 10,
                "isb": 0
            },
      		.......,
            {
                "pid": 5,
                "mid": "1:5:1",
                "wgt": 300,
                "isb": 0
            }
        ],
        "constraint": {
            "cooling_refresh": 17123,
            "cid": 1,
            "limit": 0,
            "qty": 10000,
            "refresh": 20,
            "cooling": 172800
        }
    }
}
```

[失败]()

* 99：insufficient materials
* 95：Insufficient number of lucky draw



## dozen_pump_gift

##### 发送消息JSON格式

> 朋友爱心12抽，不足12次依然可以连抽，不消耗今天抽奖次数

```json
{
	"world": 0,
	"function": "dozen_pump_gift",
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
> constraint：部分限制
>
> - cooling_refresh：距离下一次可免费时间需要的冷却时间，小于等于0时可进行免费刷新
>
> - cooling：冷却时间，剩下多少秒之后会再次刷新商城，当商城的商品被抽完之后这个值不起作用，并立刻刷新

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "remaining": [
            "3:16:880",
            "3:11:5",
            "1:36:1",
            "0:15:40",
            "0:20:60",
            "2:9:20",
            "0:16:20",
            "1:14:1",
            "3:18:10",
            "3:3:15",
            "3:22:12",
            "3:10:20",
            "3:15:5",
            "3:44:106"
        ],
        "reward": [
            "3:16:120",
            "3:11:5",
            "1:36:1",
            "0:15:20",
            "0:20:20",
            "2:9:20",
            "0:16:20",
            "1:14:1",
            "3:18:5",
            "3:3:5",
            "3:22:1",
            "3:10:5",
            "3:15:5",
            "3:44:12"
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
                "pid": 4,
                "mid": "0:16:20",
                "wgt": 30,
                "isb": 0
            },
            {
                "pid": 3,
                "mid": "3:22:1",
                "wgt": 10,
                "isb": 0
            },
      		.......,
            {
                "pid": 7,
                "mid": "2:1:20",
                "wgt": 200,
                "isb": 0
            }
        ],
        "constraint": {
            "cooling_refresh": 17045,
            "cid": 16,
            "qty": 10,
            "refresh": 20,
            "cooling": 172800
        }
    }
}
```

[失败]()

* 99：insufficient materials



## integral_convert

##### 发送消息JSON格式

> 积分兑换

```json
{
	"world": 0,
	"function": "integral_convert",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[成功]()

> status为0是获得新角色，为1是获取已有角色的碎片
>
> acp：积分进度，分别有0，200，400，600，800，1000
>
> rid：角色id
>
> star：角色星数
>
> remain_seg：角色剩余的碎片数
>
> reward_seg：角色得到的碎片数
>

```json
{
    "status": 1,
    "message": "You get 30 segments",
    "data": {
        "acp": 600,
        "rid": 25,
        "star": 1,
        "remain_seg": 90,
        "reward_seg": 30
    }
}
```
>acp：积分进度，分别有0，200，400，600，800，1000
>
>iid：物品id
>
>remain_seg：物品剩余的碎片数
>
>reward_seg：物品得到的碎片数

```json
{
    "status": 2,
    "message": "You get the universal segments",
    "data": {
        "acp": 1000,
        "iid": 17,
        "remain_v": 2,
        "reward_v": 1
    }
}
```

[失败]()

* 99：insufficient materials