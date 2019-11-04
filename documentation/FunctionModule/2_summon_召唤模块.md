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

* [`friend_summon_rolel_10_times`](##friend_summon_rolel_10_times)

  

##get_config_lottery

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

> 挂机相同关卡不需要结算资源，直接返回即可

```json
{
	"status": 1,
	"message": "same stage"
}
```

[挂机关卡失败]()

* 99: 关卡参数错误



##basic_summon

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

* 99: 资源不足



##pro_summon

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

* 99: 资源不足



##friend_summon

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

* 99: 资源不足



##basic_summon_skill

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

* 99: 资源不足



##pro_summon_skill

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

* 99: 资源不足



##friend_summon_skill

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

* 99: 资源不足



##basic_summon_role

##### 发送消息JSON格式

基础召唤武器，

> item：表示需要消耗的物品，物品列表为item类，参考enums.py，常用有1（金币），5（钻石），11，12（基础召唤，高级召唤），如果`有此武器`则为`30`碎片，如果`没有此武器`，则奖励武器。不同的抽奖方式只是获得的概率不同，概率可以参考`lottery.json`

* 4: 获得角色成功
* 3: 角色重复，获得碎片

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
			"cost_item": 1,
			"cost_quantity": 12670
		},
		"reward": {
			"role": 10,
			"star": 1,
			"segment": 0,
			"cost_item": 1,
			"cost_quantity": 12670
		}
	}
}
```

[调整关卡失败]()

* 99: 资源不足





##pro_summon_role

##### 发送消息JSON格式

基础召唤武器，

> item：表示需要消耗的物品，物品列表为item类，参考enums.py，常用有1（金币），5（钻石），11，12（基础召唤，高级召唤），如果`有此武器`则为`30`碎片，如果`没有此武器`，则奖励武器。不同的抽奖方式只是获得的概率不同，概率可以参考`lottery.json`

* 4: 获得角色成功
* 3: 角色重复，获得碎片

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
			"cost_item": 1,
			"cost_quantity": 12670
		},
		"reward": {
			"role": 10,
			"star": 1,
			"segment": 0,
			"cost_item": 1,
			"cost_quantity": 12670
		}
	}
}
```

[调整关卡失败]()

* 99: 资源不足



##friend_summon_role

##### 发送消息JSON格式

基础召唤武器，

> item：表示需要消耗的物品，物品列表为item类，参考enums.py，常用有1（金币），5（钻石），11，12（基础召唤，高级召唤），如果`有此武器`则为`30`碎片，如果`没有此武器`，则奖励武器。不同的抽奖方式只是获得的概率不同，概率可以参考`lottery.json`

* 4: 获得角色成功
* 3: 角色重复，获得碎片

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
			"cost_item": 1,
			"cost_quantity": 12670
		},
		"reward": {
			"role": 10,
			"star": 1,
			"segment": 0,
			"cost_item": 1,
			"cost_quantity": 12670
		}
	}
}
```

[调整关卡失败]()

* 99: 资源不足



##basic_summon_10_times

##pro_summon_10_times

##friend_summon_10_times

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

* 99: 资源不足

##

- ##basic_summon_skill_10_times

- ##pro_summon_skill_10_times

- ##friend_summon_skill_10_times

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
	"message": "new weapon unlocked",
	"data": {
		"remaining": {
      "0":{
			"skill": 13,
			"level": 1,
			"cost_item": 11,
			"cost_quantity": 999999997,
      "scroll_id":0,
      "scroll_quantity":0
      },
       "1":{
			"skill": 13,
			"level": 1,
			"cost_item": 11,
			"cost_quantity": 999999997,
      "scroll_id":0,
      "scroll_quantity":0
      },
      
      .......
      
       "10":{
			"skill": 13,
			"level": 1,
			"cost_item": 11,
			"cost_quantity": 999999997,
      "scroll_id":0,
      "scroll_quantity":0
      }
		},
		"reward": {
        "0":{
         "skill": 13,
          "level": 1,
          "cost_item": 11,
          "cost_quantity": 999999997,
          "scroll_id":0,
          "scroll_quantity":0
        },
     	  "1":{
          "skill": 13,
          "level": 1,
          "cost_item": 11,
          "cost_quantity": 999999997,
          "scroll_id":0,
          "scroll_quantity":0
        },
      
      ........
      
      	"10":{
          "skill": 13,
          "level": 1,
          "cost_item": 11,
          "cost_quantity": 999999997,
          "scroll_id":0,
          "scroll_quantity":0
        },
		}
	}
}
```

[调整关卡失败]()

* 99: 资源不足

##

- ##basic_summon_role_10_times

- ##pro_summon_role_10_times

- ##friend_summon_role_10_times

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
			"cost_item": 1,
			"cost_quantity": 12670
      },
       "1":{
			"role": 10,
			"star": 1,
			"segment": 0,
			"cost_item": 1,
			"cost_quantity": 12670
      },
      
      .......
      
       "10":{
			"role": 10,
			"star": 1,
			"segment": 0,
			"cost_item": 1,
			"cost_quantity": 12670
      }
		},
		"reward": {
        "0":{
          "role": 10,
          "star": 1,
          "segment": 0,
          "cost_item": 1,
          "cost_quantity": 100
        },
     	  "1":{
          "role": 10,
          "star": 1,
          "segment": 0,
          "cost_item": 1,
          "cost_quantity": 100
        },
      
      ........
      
      	"10":{
          "role": 10,
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

* 99: 资源不足

