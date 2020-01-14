## 方法列表

* [`refresh_factory`](#refresh_factory)
* [`upgrade_factory`](#upgrade_factory)
* [`^set_armor_factory`](#set_armor_factory)
* [`get_config_factory`](#get_config_factory)
* [`buy_worker_factory`](#buy_worker_factory)
* [`^update_worker_factory`](#update_worker_factory)
* [`buy_acceleration_factory`](#buy_acceleration_factory)
* [`^activate_wishing_pool_factory`](#activate_wishing_pool_factory)
* [`gather_resource_factory`](##gather_resource_factory)

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
> `resource`: contains FOOD, IRON, CRYSTAL factories.（含有食品、铁、水晶、盔甲工厂）
>
> - `remaining`: is the total amount（剩余的物资数量）
>
> - `reward`: is the change since the last time（物资变化量）
>
>
> `worker`:  information regarding the distribution of workers across all factories（工人信息）
>
> - `total`: the number of all assigned and unassigned workers（所有工人数量）
> - `unassigned`: the number of available free workers（可分配的工人数量，如下-1）
> - `Factory ID` : `number of assigned workers`（各个工厂工人数量，如下0-3）
>
> `level`: information regarding the distribution of levels across all factories（ 关于所有工厂级别分布的信息，其中3是盔甲制造盔甲的种类）
>
> `count`：许愿池已许愿次数
>
> `pool` : number of seconds remaining until the wishing pool refreshes（许愿池下次刷新的冷却时间）
>
> `pool_diamond`：下次许愿许愿消耗的钻石数
>
> `next_refresh`： 整个工厂下次刷新的剩余时间
>
> `time`：工厂加速剩余时间，例time：59，工厂加速59秒后结束

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "steps": 11,
        "resource": {
            "remaining": {
                "0": 5,
                "1": 2,
                "2": 19,
                "3": 0
            },
            "reward": {
                "0": 0,
                "1": 1,
                "2": 3,
                "3": 0
            }
        },
        "count": 4, 
        "pool": 0,
        "pool_diamond": 0,
        "next_refresh": 3,
        "worker": {
            "-1": 0,
            "total": 5,
            "2": 1,
            "3": 0,
            "1": 1,
            "0": 3
        },
        "level": {
            "3": 1,
            "0": 1,
            "1": 1,
            "2": 1,
            "-2": 1
        },
        "time": 0
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
    "status": 98,
    "message": "insufficient funds",
    "data": {
        "refresh": {
            "resource": {
                "remaining": {
                    "0": 5,
                    "1": 3,
                    "2": 43,
                    "3": 0
                },
                "reward": {
                    "0": 0,
                    "1": 1,
                    "2": 3,
                    "3": 0
                }
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

> aid: 设置要生产的盔甲id

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

> gather：是收集信息（详见gather_resource_factory方法data返回）
>
> aid：设置成的盔甲id

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "gather": {
            "remaining": [
                "4:1:0"
            ],
            "reward": [
                "4:1:0"
            ]
        },
        "aid": 3
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

>`data` contains the configuration file
>
>general：一般配置信息
>
>- step：刷新频率（10秒钟刷新一次）
>- acceleration_cost：购买工厂加速卡需要消耗的钻石数
>- costs：工厂产物生产需要消耗的基础物资
>  - 0：食物工厂生产食物无消耗品
>  - 1：矿山工厂生产铁需要消耗食物3个
>  - 2：水晶工厂生产水晶需要消耗食物1个，铁3个
>  - 3：盔甲工厂生产一级盔甲需要消耗20个铁
>- storage_limits：仓库限制
>  - 0：食物仓库每级的容量上限
>    - 1：1级食物仓库可以容纳4320个食物
>    - 2：2级食物仓库可以容纳8640个食物
>    - ... ...
>  - 1：矿山仓库每级的容量上限
>    - 1：1级矿山仓库可以容纳2880个铁
>    - 2：2级矿山仓库可以容纳5760个铁
>    - ... ...
>  - 2：水晶仓库每级的容量上限
>    - 1：1级水晶仓库可以容纳12960个水晶
>    - 2：2级水晶仓库可以容纳25920个水晶
>    - ... ...
>- worker_limits：工人上限限制
>  - 0：食物工厂每级工人协同工作上限
>    - 1：1级食物工厂最多可以放3个工人
>    - 2：2级食物工厂最多可以放6个工人
>    - ... ...
>  - 1：矿山工厂每级工人协同工作上限
>    - 1：1级矿山工厂最多可以放2个工人
>    - 2：2级矿山工厂最多可以放4个工人
>    - ... ...
>  - 2：水晶工厂每级工人协同工作上限
>    - 1：1级水晶工厂最多可以放1个工人
>    - 2：2级水晶工厂最多可以放2个工人
>    - ... ...
>- upgrade_cost：各个工厂升级消耗水晶数量
>  - -2：许愿池升级每级消耗水晶数
>    - 2：1级升到2级需要消耗200水晶
>    - 3：2级升到3级需要消耗400水晶
>    - ... ...
>  - 0：食物工厂升级每级消耗水晶数
>    - 2：1级升到2级需要消耗50水晶
>    - 3：2级升到3级需要消耗100水晶
>    - ... ...
>  - 1：矿山工厂升级每级消耗水晶数
>    - 2：1级升到2级需要消耗500水晶
>    - 3：2级升到3级需要消耗1000水晶
>    - ... ...
>  - 2：水晶工厂升级每级消耗水晶数
>    - 2：1级升到2级需要消耗5000水晶
>    - 3：2级升到3级需要消耗10000水晶
>    - ... ...
>
>workers：购买工人信息
>
>- max：购买超过最大值工人后消耗食物数不再变化（6000食物）
>- cost：购买少于最大值需要消耗的食物数
>  - 1：购买第一个工人需要消耗100个食物
>  - 2：购买第二个工人需要消耗110个食物
>  - ... ...
>  - 45：购买第二个工人需要消耗6000个食物
>
>wishing_pool：许愿池相关配置信息
>
>- base_segment：每次许愿得到的武器碎片数最少数量为1个
>- base_recover：需要之后需要等待的小时数，这里为49小时
>- base_diamond：没有结束冷却时间需要消耗基础钻石进行许愿（50*花钻石许愿次数）

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"general": {
			"step": 10,
			"acceleration_cost": 30,
			"costs": {
				"0": {},
				"1": {
					"0": 3
				},
				"2": {
					"0": 1,
					"1": 3
				},
				"3": {
					"1": 20
				}
			},
			"storage_limits": {
				"0": {
					"1": 4320,
					"2": 8640,
					"3": 12960,
					"4": 17280,
					"5": 21600,
					"6": 25920,
					"7": 30240,
					"8": 34560,
					"9": 38880,
					"10": 43200,
					"11": 47520,
					"12": 51840,
					"13": 56160,
					"14": 60480,
					"15": 64800,
					"16": 69120,
					"17": 73440,
					"18": 77760,
					"19": 82080,
					"20": 86400,
					"21": 90720,
					"22": 95040,
					"23": 99360,
					"24": 103680,
					"25": 108000,
					"26": 112320,
					"27": 116640,
					"28": 120960,
					"29": 125280,
					"30": 129600,
					"31": 133920,
					"32": 138240,
					"33": 142560,
					"34": 146880,
					"35": 151200,
					"36": 155520,
					"37": 159840,
					"38": 164160,
					"39": 168480,
					"40": 172800,
					"41": 177120,
					"42": 181440,
					"43": 185760,
					"44": 190080,
					"45": 194400,
					"46": 198720,
					"47": 203040,
					"48": 207360,
					"49": 211680,
					"50": 216000,
					"51": 220320,
					"52": 224640,
					"53": 228960,
					"54": 233280,
					"55": 237600,
					"56": 241920,
					"57": 246240,
					"58": 250560,
					"59": 254880,
					"60": 259200
				},
				"1": {
					"1": 2880,
					"2": 5760,
					"3": 8640,
					"4": 11520,
					"5": 14400,
					"6": 17280,
					"7": 20160,
					"8": 23040,
					"9": 25920,
					"10": 28800,
					"11": 31680,
					"12": 34560,
					"13": 37440,
					"14": 40320,
					"15": 43200,
					"16": 46080,
					"17": 48960,
					"18": 51840,
					"19": 54720,
					"20": 57600,
					"21": 60480,
					"22": 63360,
					"23": 66240,
					"24": 69120,
					"25": 72000,
					"26": 74880,
					"27": 77760,
					"28": 80640,
					"29": 83520,
					"30": 86400
				},
				"2": {
					"1": 12960,
					"2": 25920,
					"3": 38880,
					"4": 51840,
					"5": 64800,
					"6": 77760,
					"7": 90720,
					"8": 103680,
					"9": 116640,
					"10": 129600,
					"11": 142560,
					"12": 155520,
					"13": 168480,
					"14": 181440,
					"15": 194400
				}
			},
			"worker_limits": {
				"0": {
					"1": 3,
					"2": 6,
					"3": 9,
					"4": 12,
					"5": 15,
					"6": 18,
					"7": 21,
					"8": 24,
					"9": 27,
					"10": 30,
					"11": 33,
					"12": 36,
					"13": 39,
					"14": 42,
					"15": 45,
					"16": 48,
					"17": 51,
					"18": 54,
					"19": 57,
					"20": 60,
					"21": 63,
					"22": 66,
					"23": 69,
					"24": 72,
					"25": 75,
					"26": 78,
					"27": 81,
					"28": 84,
					"29": 87,
					"30": 90,
					"31": 93,
					"32": 96,
					"33": 99,
					"34": 102,
					"35": 105,
					"36": 108,
					"37": 111,
					"38": 114,
					"39": 117,
					"40": 120,
					"41": 123,
					"42": 126,
					"43": 129,
					"44": 132,
					"45": 135,
					"46": 138,
					"47": 141,
					"48": 144,
					"49": 147,
					"50": 150,
					"51": 153,
					"52": 156,
					"53": 159,
					"54": 162,
					"55": 165,
					"56": 168,
					"57": 171,
					"58": 174,
					"59": 177,
					"60": 180
				},
				"1": {
					"1": 2,
					"2": 4,
					"3": 6,
					"4": 8,
					"5": 10,
					"6": 12,
					"7": 14,
					"8": 16,
					"9": 18,
					"10": 20,
					"11": 22,
					"12": 24,
					"13": 26,
					"14": 28,
					"15": 30,
					"16": 32,
					"17": 34,
					"18": 36,
					"19": 38,
					"20": 40,
					"21": 42,
					"22": 44,
					"23": 46,
					"24": 48,
					"25": 50,
					"26": 52,
					"27": 54,
					"28": 56,
					"29": 58,
					"30": 60
				},
				"2": {
					"1": 1,
					"2": 2,
					"3": 3,
					"4": 4,
					"5": 5,
					"6": 6,
					"7": 7,
					"8": 8,
					"9": 9,
					"10": 10,
					"11": 11,
					"12": 12,
					"13": 13,
					"14": 14,
					"15": 15
				}
			},
			"upgrade_cost": {
				"-2": {
					"2": 200,
					"3": 400,
					"4": 800,
					"5": 1200,
					"6": 1600,
					"7": 2000,
					"8": 2400,
					"9": 2800,
					"10": 3200,
					"11": 3600,
					"12": 4400,
					"13": 5200,
					"14": 6000,
					"15": 6800,
					"16": 7600,
					"17": 8400,
					"18": 9200,
					"19": 10000,
					"20": 10800,
					"21": 11600,
					"22": 15600,
					"23": 19600,
					"24": 23600,
					"25": 27600,
					"26": 31600,
					"27": 35600,
					"28": 39600,
					"29": 43600,
					"30": 47600
				},
				"0": {
					"2": 50,
					"3": 100,
					"4": 150,
					"5": 200,
					"6": 250,
					"7": 300,
					"8": 350,
					"9": 400,
					"10": 450,
					"11": 550,
					"12": 650,
					"13": 750,
					"14": 850,
					"15": 950,
					"16": 1050,
					"17": 1150,
					"18": 1250,
					"19": 1350,
					"20": 1450,
					"21": 1950,
					"22": 2450,
					"23": 2950,
					"24": 3450,
					"25": 3950,
					"26": 4450,
					"27": 4950,
					"28": 5450,
					"29": 5950,
					"30": 6450,
					"31": 7950,
					"32": 9450,
					"33": 10950,
					"34": 12450,
					"35": 13950,
					"36": 15450,
					"37": 16950,
					"38": 18450,
					"39": 19950,
					"40": 21450,
					"41": 25450,
					"42": 29450,
					"43": 33450,
					"44": 37450,
					"45": 41450,
					"46": 45450,
					"47": 49450,
					"48": 53450,
					"49": 57450,
					"50": 61450,
					"51": 71450,
					"52": 81450,
					"53": 91450,
					"54": 101450,
					"55": 111450,
					"56": 121450,
					"57": 131450,
					"58": 141450,
					"59": 151450,
					"60": 161450
				},
				"1": {
					"2": 500,
					"3": 1000,
					"4": 1500,
					"5": 2000,
					"6": 2500,
					"7": 3000,
					"8": 3500,
					"9": 4000,
					"10": 4500,
					"11": 5500,
					"12": 6500,
					"13": 7500,
					"14": 8500,
					"15": 9500,
					"16": 10500,
					"17": 11500,
					"18": 12500,
					"19": 13500,
					"20": 14500,
					"21": 19500,
					"22": 24500,
					"23": 29500,
					"24": 34500,
					"25": 39500,
					"26": 44500,
					"27": 49500,
					"28": 54500,
					"29": 59500,
					"30": 64500
				},
				"2": {
					"2": 5000,
					"3": 10000,
					"4": 15000,
					"5": 20000,
					"6": 25000,
					"7": 30000,
					"8": 35000,
					"9": 40000,
					"10": 45000,
					"11": 55000,
					"12": 65000,
					"13": 75000,
					"14": 85000,
					"15": 95000
				}
			}
		},
		"workers": {
			"max": 45,
			"cost": {
				"1": 100,
				"2": 110,
				"3": 120,
				"4": 130,
				"5": 140,
				"6": 150,
				"7": 170,
				"8": 190,
				"9": 210,
				"10": 230,
				"11": 250,
				"12": 280,
				"13": 310,
				"14": 340,
				"15": 370,
				"16": 410,
				"17": 450,
				"18": 500,
				"19": 550,
				"20": 610,
				"21": 670,
				"22": 740,
				"23": 810,
				"24": 890,
				"25": 980,
				"26": 1080,
				"27": 1190,
				"28": 1310,
				"29": 1440,
				"30": 1580,
				"31": 1740,
				"32": 1910,
				"33": 2100,
				"34": 2310,
				"35": 2540,
				"36": 2790,
				"37": 3070,
				"38": 3380,
				"39": 3720,
				"40": 4090,
				"41": 4500,
				"42": 4950,
				"43": 5450,
				"44": 6000,
				"45": 6000
			}
		},
		"wishing_pool": {
			"base_segment": 1,
			"base_recover": 49,
			"base_diamond": 50
		}
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
> food: 食物的详细信息，`remaining`背包中剩余食物，`reward`背包中食物改变量

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "worker": {
            "-1": 1,
            "total": 6
        },
        "food": {
            "remaining": 11850,
            "reward": -150
        }
    }
}
```

[获得失败]()
>
> * 98: insufficient food
>

## update_worker_factory

更新工人情况

##### 发送消息JSON格式

> 0, 1, 2, 3分别对应各个工厂


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
			"2" : 2,
            "3" : 0
		}
	}
}
```

##### 接受消息JSON格式

> `refresh`：和刷新得到的信息一样

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"refresh": {
			"steps": 0,
			"resource": {
				"remaining": {
					"0": 2,
					"1": 0,
					"2": 0,
					"3": 0
				},
				"reward": {
					"0": 0,
					"1": 0,
					"2": 0,
					"3": 0
				}
			},
			"pool": 0,
			"pool_diamond": 0,
			"next_refresh": 2,
			"worker": {
				"-1": 1,
				"total": 5,
				"2": 1,
				"3": 1,
				"1": 1,
				"0": 1
			},
			"level": {
				"3": 1,
				"0": 1,
				"1": 1,
				"2": 1,
				"-2": 1
			},
			"time": 0
		}
	}
}
```

```json
{
    "status": 99,
    "message": "insufficient workers",
    "data": {
        "refresh": {
			"steps": 0,
			"resource": {
				"remaining": {
					"0": 2,
					"1": 0,
					"2": 0,
					"3": 0
				},
				"reward": {
					"0": 0,
					"1": 0,
					"2": 0,
					"3": 0
				}
			},
			"pool": 0,
			"pool_diamond": 0,
			"next_refresh": 2,
			"worker": {
				"-1": 1,
				"total": 5,
				"2": 1,
				"3": 1,
				"1": 1,
				"0": 1
			},
			"level": {
				"3": 1,
				"0": 1,
				"1": 1,
				"2": 1,
				"-2": 1
			},
			"time": 0
		}
    }
}
```

```json
{
    "status": 98,
    "message": "factory worker over limits",
    "data": {
        "refresh": {
			"steps": 0,
			"resource": {
				"remaining": {
					"0": 2,
					"1": 0,
					"2": 0,
					"3": 0
				},
				"reward": {
					"0": 0,
					"1": 0,
					"2": 0,
					"3": 0
				}
			},
			"pool": 0,
			"pool_diamond": 0,
			"next_refresh": 2,
			"worker": {
				"-1": 1,
				"total": 5,
				"2": 1,
				"3": 1,
				"1": 1,
				"0": 1
			},
			"level": {
				"3": 1,
				"0": 1,
				"1": 1,
				"2": 1,
				"-2": 1
			},
			"time": 0
		}
    }
}
```

```json
{
    "status": 97,
    "message": "invalid fid supplied",
    "data": {
        "refresh": {
			"steps": 0,
			"resource": {
				"remaining": {
					"0": 2,
					"1": 0,
					"2": 0,
					"3": 0
				},
				"reward": {
					"0": 0,
					"1": 0,
					"2": 0,
					"3": 0
				}
			},
			"pool": 0,
			"pool_diamond": 0,
			"next_refresh": 2,
			"worker": {
				"-1": 1,
				"total": 5,
				"2": 1,
				"3": 1,
				"1": 1,
				"0": 1
			},
			"level": {
				"3": 1,
				"0": 1,
				"1": 1,
				"2": 1,
				"-2": 1
			},
			"time": 0
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

> refresh: 资源刷新的配置情况
>
> remaining：剩余物资
>
> reward: 资源的变化情况
>
> time：剩余多久刷新一次许愿池

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
    "status": 0,
    "message": "success",
    "data": {
        "refresh": {
            "resource": {
                "remaining": {
                    "0": 1,
                    "1": 2,
                    "2": 69,
                    "3": 0
                },
                "reward": {
                    "0": -2,
                    "1": 2,
                    "2": 1,
                    "3": 0
                }
            }
        },
        "time": 172729,
        "remaining": {
            "diamond": 9991340
        },
        "reward": {
            "diamond": -30
        }
    }
}
```

[获得失败]()
>
> * 99: insufficient funds



## activate_wishing_pool_factory

许愿池每天可以许愿6次

##### 发送消息JSON格式

```json
{
	"world"   : 0, 
	"function": "activate_wishing_pool_factory",
	"data"    :
	{
		"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9",
		"wid"  : 6
	}
}
```

##### 接受消息JSON格式

>`count` : 已经许愿的次数（第一次免费）
>
>`pool`：许愿池剩余冷却时间
>
>`pool_diamond`：许愿池下次许愿需要消耗的钻石数
>
>`remaining`：武器碎片剩余情况和钻石剩余情况
>
>`reward`：武器碎片的改变情况和钻石消耗情况

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "pool": 172800,
        "count": 1,
        "pool_diamond": 50,
        "remaining": {
            "wid": 6,
            "seg": 22,
            "diamond": 9991400
        },
        "reward": {
            "wid": 6,
            "seg": 2,
            "diamond": 0
        }
    }
}
```

[获得失败]()
>
>* 99: insufficient diamonds
>* 98: The number of draws has reached the limit today



## gather_resource_factory

收集资源

##### 发送消息JSON格式

> resource：需要收集的资源（下面的这几种情况可以选取传）
>
> - 0：食物工厂下的物资数
> - 1：矿山工厂下的物资数
> - 2：水晶工厂下的物资数

```json
{
	"world"   : 0, 
	"function": "gather_resource_factory",
	"data"    :
	{
		"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9",
		"resource": {"1": 1888, "2": 18989}
	}
}
```

##### 接受消息JSON格式

>remaining：剩余的物资情况（gid:iid:qty）
>
>reward：改变的物资情况（gid:iid:qty）
>
>refresh：刷新的最新数据

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "remaining": [
            "3:3:12"
        ],
        "reward": [
            "3:3:3"
        ]
    }
}
```

[获得失败]()

>* 99: invalid resource