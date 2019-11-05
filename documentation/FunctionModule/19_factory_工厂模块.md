## 方法列表

* [`refresh_factory`](#refresh_factory)
* [`upgrade_factory`](#upgrade_factory)
* [`set_armor_factory`](#set_armor_factory)
* [`get_config_factory`](#get_config_factory)
* [`buy_worker_factory`](#buy_worker_factory)
* [`increase_worker_factory`](#increase_worker_factory)
* [`decrease_worker_factory`](#decrease_worker_factory)
* [`buy_acceleration_factory`](#buy_acceleration_factory)
* [`activate_wishing_pool_factory`](#activate_wishing_pool_factory)

## refresh_factory

刷新工厂，获取刷新工厂的信息，任何会变化工厂算法结构的操作都会重新执行一次刷新工厂方法

##### 发送消息JSON格式

```json
{
	"world"   : 0, 
	"function": "refresh_factory",
	"data"    :
	{
		"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
	}
}
```

##### 接受消息JSON格式

> `steps`: the number of steps since the last refresh
>
> `resource`: contains FOOD, IRON, CRYSTAL factories.
>
>			`remaining`: is the total amount
>	
>			`reward`: is the change since the last time
>
> `armor`: contains ARMOR factory
>
>			`aid`: the armor id that the factory is producing
>	
>			`remaining`: total quantity of level 1 armor with given aid
>	
>			`reward`: the quantity gained since the last time
>
> `worker`: information regarding the distribution of workers across all factories
>
>			`unassigned`: the number of available free workers
>	
>			`total`: the number of all assigned and unassigned workers
>	
>			`Factory ID` : `number of assigned workers`
>
> `level`: information regarding the distribution of levels across all factories
>
>			`Factory ID` : `level`
>
> `pool` : number of seconds remaining until the wishing pool refreshes

```json
{
	"status" : 0, 
	"message": "factory refreshed",
	"data"   :
	{
		"steps"    : 28,
		"resource" :
		{
			"remaining" :
			{
				"0" : 253,
				"1" :   2,
				"2" : 182
			},
			"reward" :
			{
				"0" : -53,
				"1" :   1,
				"2" :  10
			}
		},
		"armor" :
		{
			"aid"       : 2,
			"remaining" : 5,
			"reward"    : 1
		},
		"worker" :
		{
			"unassigned" : 1,
			"total"      : 4,
			"0"          : 1,
			"1"          : 1,
			"2"          : 1,
			"3"          : 1
		},
		"level" :
		{
			"0"  : 3,
			"1"  : 1,
			"2"  : 2,
			"3"  : 5,
			"-2" : 1,
		},
		"pool" : 15530
	}
}
```

## upgrade_factory

升级工厂需要水晶，工厂的水晶消耗列表参考`factory.json`，水晶的消耗量根据工厂等级来。

##### 发送消息JSON格式

```json
{
	"world"   : 0, 
	"function": "upgrade_factory",
	"data"    :
	{
		"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9",
		"fid"  : 2
	}
}
```

##### 接受消息JSON格式

```json
{
	"status" : 0, 
	"message": "upgrade success",
	"data"   :
	{
		"refresh" :
		{
			"resource" :
			{
				"remaining" :
				{
					"0" : 253,
					"1" :   2,
					"2" : 182
				},
				"reward" :
				{
					"0" : -53,
					"1" :   1,
					"2" :  10
				}
			},
			"armor" :
			{
				"aid"       : 2,
				"remaining" : 5,
				"reward"    : 1
			}
		},
		"upgrade" :
		{
			"cost"  : 800,
			"fid"   : 2,
			"level" : 4
		}
	}
}
```

```json
{
	"status" : 98, 
	"message": "insufficient funds",
	"data"   :
	{
		"refresh" :
		{
			"resource" :
			{
				"remaining" :
				{
					"0" : 253,
					"1" :   2,
					"2" : 182
				},
				"reward" :
				{
					"0" : -53,
					"1" :   1,
					"2" :  10
				}
			},
			"armor" :
			{
				"aid"       : 2,
				"remaining" : 5,
				"reward"    : 1
			}
		}
	}
}
```

```json
{
	"status" : 97, 
	"message": "max level",
	"data"   :
	{
		"refresh" :
		{
			"resource" :
			{
				"remaining" :
				{
					"0" : 253,
					"1" :   2,
					"2" : 182
				},
				"reward" :
				{
					"0" : -53,
					"1" :   1,
					"2" :  10
				}
			},
			"armor" :
			{
				"aid"       : 2,
				"remaining" : 5,
				"reward"    : 1
			}
		}
	}
}
```

[获得失败]()
>
> * 99: invalid fid
> * 98: insufficient funds
> * 97: max level
>

## set_armor_factory

设置需要生产的护甲，如果已经设置过护甲，需要把以前的护甲结算之后再设置新护甲

##### 发送消息JSON格式

> aid: 护甲的id值

```json
{
	"world"   : 0, 
	"function": "set_armor_factory",
	"data"    :
	{
		"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9",
		"aid"  : 2
	}
}
```

##### 接受消息JSON格式

> aid: 护甲的id值

```json
{
	"status" : 0, 
	"message": "successfully set armor",
	"data"   :
	{
		"aid" : 2
	}
}
```

## get_config_factory

返回工厂的配置信息，主要内容为工厂的等级信息和消耗详情, 返回的配置文件来自factory.json

#####发送消息JSON格式

> 无

```json
{
	"world"   : 0, 
	"function": "get_config_factory",
	"data"    :
	{
		"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
	}
}
```

##### 接受消息JSON格式

>
> `data` contains the configuration file
>

```json
{
	"status" : 0, 
	"message": "success",
	"data"   :
	{
	}
}
```

## buy_worker_factory

##### 发送消息JSON格式

购买工人，工人的价格表参考`factory.json`，购买工人需要消耗食物

```json
{
	"world"   : 0, 
	"function": "buy_worker_factory",
	"data"    :
	{
		"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
	}
}
```

##### 接受消息JSON格式

> worker：工人的详细内容，`unassigned`没有工作的工人，`total`工人总数
>
> food: 食物的详细信息，`remaining`剩余食物，`reward`食物改变量

```json
{
	"status" : 0, 
	"message": "success",
	"data"   :
	{
		"worker" :
		{
			"unassigned" : 3,
			"total"      : 10
		},
		"food" :
		{
			"remaining" : 2530,
			"reward"    : -140
		}
	}
}
```

[获得失败]()
>
> * 99: already have max workers
> * 98: insufficient food
>

## increase_worker_factory

##### 发送消息JSON格式

向工厂添加工人，添加工人会改变工厂的算法结构，所以需要先结算后添加

> fid: 工厂id
>
> num: 工人的数量

```json
{
	"world"   : 0, 
	"function": "increase_worker_factory",
	"data"    :
	{
		"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9",
		"fid"  : 2,
    "num" : 1
	}
}
```

##### 接受消息JSON格式

> resource: 资源的配置情况
>
> reward: 资源的变化情况
>
> armor：护甲的变化情况
>
> worker：工人的情况

```json
{
	"status" : 0, 
	"message": "success",
	"data"   :
	{
		"refresh" :
		{
			"resource" :
			{
				"remaining" :
				{
					"0" : 253,
					"1" :   2,
					"2" : 182
				},
				"reward" :
				{
					"0" : -53,
					"1" :   1,
					"2" :  10
				}
			},
			"armor" :
			{
				"aid"       : 2,
				"remaining" : 5,
				"reward"    : 1
			}
		},
		"worker" :
		{
			"unassigned" : 3,
			"workers"    : 5
		}
	}
}
```

[失败]()

>
> * 99: insufficient unassigned workers
> * 98: can not increase past max worker limit
> * 97: invalid fid
>

## decrease_worker_factory

##### 发送消息JSON格式

向工厂减少工人，添加工人会改变工厂的算法结构，所以需要先结算后添加

> fid: 工厂的id
>
> num：工人的数量

```json
{
	"world"   : 0, 
	"function": "decrease_worker_factory",
	"data"    :
	{
		"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9",
		"fid"  : 2,
    "num" : 1
	}
}
```

##### 接受消息JSON格式

> resource: 资源的配置情况
>
> reward: 资源的变化情况
>
> armor：护甲的变化情况
>
> worker：工人的情况

```json
{
	"status" : 0, 
	"message": "success",
	"data"   :
	{
		"refresh" :
		{
			"resource" :
			{
				"remaining" :
				{
					"0" : 253,
					"1" :   2,
					"2" : 182
				},
				"reward" :
				{
					"0" : -53,
					"1" :   1,
					"2" :  10
				}
			},
			"armor" :
			{
				"aid"       : 2,
				"remaining" : 5,
				"reward"    : 1
			}
		},
		"worker" :
		{
			"unassigned" : 5,
			"workers"    : 4
		}
	}
}
```

[获得失败]()
>
> * 99: insufficient assigned workers
> * 97: invalid fid
>

## buy_acceleration_factory

##### 发送消息JSON格式

> resource: 资源的配置情况
>
> reward: 资源的变化情况
>
> armor：护甲的变化情况
>
> worker：工人的情况

购买工厂加速，加速工厂需要消耗钻石，钻石的消耗数量依据factory.json的配置信息

```json
{
	"world"   : 0, 
	"function": "buy_acceleration_factory",
	"data"    :
	{
		"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
	}
}
```

##### 接受消息JSON格式

```json
{
	"status" : 0, 
	"message": "success",
	"data"   :
	{
		"refresh" :
		{
			"resource" :
			{
				"remaining" :
				{
					"0" : 253,
					"1" :   2,
					"2" : 182
				},
				"reward" :
				{
					"0" : -53,
					"1" :   1,
					"2" :  10
				}
			},
			"armor" :
			{
				"aid"       : 2,
				"remaining" : 5,
				"reward"    : 1
			}
		},
		"time" : "2019-12-03 02:51:37",
		"remaining" : 
		{
			"diamond" : 1530
		},
		"reward" :
		{
			"diamond" : -230
		}
	}
}
```

[获得失败]()
>
> * 99: insufficient funds
>

## activate_wishing_pool_factory

##### 发送消息JSON格式

```json
{
	"world"   : 0, 
	"function": "activate_wishing_pool_factory",
	"data"    :
	{
		"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9",
		"wid"  : 5
	}
}
```

##### 接受消息JSON格式

> 

```json
{
	"status" : 0, 
	"message": "success",
	"data"   :
	{
		"pool" : 3130,
		"remaining" :
		{
			"wid" : 5,
			"seg" : 2350,
			"diamond : 3323
		},
		"reward" :
		{
			"wid" : 5,
			"seg" : 3,
			"diamond" : -350
		}
	}
}
```

[获得失败]()
>
> * 99: insufficient funds
>
