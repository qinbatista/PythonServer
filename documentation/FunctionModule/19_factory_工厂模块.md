## 方法列表

* [`refresh_factory`](#refresh_factory)
* [`upgrade_factory`](#upgrade_factory)
* [`set_armor_factory`](#set_armor_factory)
* [`get_config_factory`](#get_config_factory)
* [`buy_worker_factory`](#buy_worker_factory)
* [`update_worker_factory`](#update_worker_factory)
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

> `steps`: the number of steps since the last refresh（ 上次刷新的步骤数 ）
>
> `resource`: contains FOOD, IRON, CRYSTAL factories.（含有食品、铁、水晶的工厂）
>
> - `remaining`: is the total amount（剩余的物资数量）
>
> - `reward`: is the change since the last time（物资变化量）
>
> `armor`: contains ARMOR factory（盔甲信息）
>
> - `aid`: the armor id that the factory is producing（盔甲id）
>
> - `remaining`: total quantity of level 1 armor with given aid（盔甲剩余数量）
>
> - `reward`: the quantity gained since the last time（盔甲变化量）
>
>
> `worker`:  information regarding the distribution of workers across all factories（工人信息）
>
> - `total`: the number of all assigned and unassigned workers（所有工人数量）
> - `unassigned`: the number of available free workers（可分配的工人数量，如下-1）
> - `Factory ID` : `number of assigned workers`（各个工厂工人数量，如下0-3）
>
> `level`: information regarding the distribution of levels across all factories（ 关于所有工厂级别分布的信息）
>
> - `Factory ID` : `level`
>
> `pool` : number of seconds remaining until the wishing pool refreshes（许愿池刷新之前剩余的秒数）
>
> next_refresh：更新剩余时间（秒）

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"steps": 0,
		"resource": {
			"remaining": {
				"0": 0,
				"1": 0,
				"2": 0
			},
			"reward": {
				"0": 0,
				"1": 0,
				"2": 0
			}
		},
		"armor": {
			"aid": 1,
			"remaining": 0,
			"reward": 0
		},
		"pool": 0,
		"next_refresh": 10,
		"worker": {
			"-1": 5,
			"total": 5,
			"2": 0,
			"3": 0,
			"1": 0,
			"0": 0
		},
		"level": {
			"0": 1,
			"1": 1,
			"2": 1,
			"-2": 1
		}
	}
}
```

## upgrade_factory

升级工厂需要水晶，工厂的水晶消耗列表参考`factory.json`，水晶的消耗量根据工厂等级来。

> fid：工厂id

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

> refresh：刷新的数据
>
> - resource：资源变化情况
> - armor：盔甲变化情况
>
> upgrade：升级工厂的部分信息
>
> - cost：消耗品消耗数量
> - fid：工厂id
> - level：工厂现在的等级

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

> aid: 盔甲id

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

> refresh: 更新获得的数据信息
>
> - resource：资源最后结果
> - reward：资源改变信息
>
> armor：盔甲信息
>
> - aid：基础盔甲id
> - remaining：盔甲剩余量
> - reward：盔甲改变量
>
> aid：转换成的盔甲id

```json
{
	"status" : 0, 
	"message": "successfully set armor",
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
				"aid"       : 1,
				"remaining" : 5,
				"reward"    : 1
			}
		},
		"aid" : 2
	}
}
```

## get_config_factory

返回工厂的配置信息，主要内容为工厂的等级信息和消耗详情, 返回的配置文件来自factory.json

##### 发送消息JSON格式

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

> worker：工人的详细内容，`unassigned`（`-1`）没有工作的工人，`total`工人总数
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
			"-1"    : 3,
			"total" : 10
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
> * 98: insufficient food
>

## update_worker_factory

##### 发送消息JSON格式


```json
{
	"world"   : 0, 
	"function": "update_worker_factory",
	"data"    :
	{
		"token"   : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9",
		"worker" :
		{
			"0" : 3,
			"1" : 1,
			"2" : 2
		}
	}
}
```

##### 接受消息JSON格式

> `resource`: 资源的配置情况
>
> `reward`: 资源的变化情况
>
> `armor`：护甲的变化情况
>
> `worker`：工人的情况
>
> `next_refresh`：the number of seconds remaining until the server calculates the next STEP
>
> Even if there is an error, the server will return the number of workers the SERVER says the client has.
>
> 服务器计算下一步之前剩余的秒数，即使出现错误，服务器也会返回客户机所拥有的worker的数量。

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
		"next_refresh" : 4,
		"worker" :
		{
			"-1" : 5,
			"0"  : 4,
			"1"  : 2,
			"2"  : 1
		}
	}
}
```

```json
{
	"status" : 99, 
	"message": "insufficient workers",
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
		"next_refresh" : 4,
		"worker" :
		{
			"-1" : 5,
			"0"  : 4,
			"1"  : 2,
			"2"  : 1
		}
	}
}
```

```json
{
	"status" : 98, 
	"message": "factory worker over limits",
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
		"next_refresh" : 4,
		"worker" :
		{
			"-1" : 5,
			"0"  : 4,
			"1"  : 2,
			"2"  : 1
		}
	}
}
```

```json
{
	"status" : 97, 
	"message": "invalid fid supplied",
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
		"next_refresh" : 4,
		"worker" :
		{
			"-1" : 5,
			"0"  : 4,
			"1"  : 2,
			"2"  : 1
		}
	}
}
```

[获得失败]()
>
> * 99: insufficient workers
> * 98: factory worker over limits
> * 97: invalid fid supplied
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

##### 接受消息JSON格式

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
		"time" : 70580,
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

>`count`   : the number of times the non-free wishing pool has been used（ 使用免费许愿池的次数 ）
> `diamond` : the cost of the next non-free wishing pool（下一个非免费许愿池的消耗数量）
> 
> pool：许愿池剩余冷却时间

```json
{
	"status" : 0, 
	"message": "success",
	"data"   :
	{
		"pool" : 3130,
		"count" : 0,
		"diamond" : 50,
		"remaining" :
		{
			"wid" : 5,
			"seg" : 2350,
			"diamond" : 3323
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
