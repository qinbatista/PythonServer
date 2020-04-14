## 方法列表

* ## <font color=#FFBB00>以下方法为新增方法</font>

* [`stage_enter_general`](##stage_enter_general)

* [`stage_victory_general`](##stage_victory_general)

* [`stage_enter_endless`](##stage_enter_endless)

* [`stage_victory_endless`](##stage_victory_endless)

* [`stage_enter_boss`](##stage_enter_boss)

* [`stage_victory_boss`](##stage_victory_boss)

* [`stage_enter_coin`](##stage_enter_coin)

* [`stage_victory_coin`](##stage_victory_coin)

* [`stage_enter_exp`](##stage_enter_exp)

* [`stage_victory_exp`](##stage_victory_exp)

* [`stage_refresh_boss`](##stage_refresh_boss)

* [`stage_all_infos`](##stage_all_infos)

* [`stage_damage_ranking`](##stage_damage_ranking)

* [`stage_hang_up`](##stage_hang_up)

* [`stage_mopping_up`](##stage_mopping_up)



## <font color=#FFBB00>以下方法为新增方法</font>

##### <font color=#00ccFF>返回状态码集合如下：</font>

```python
# 99 - Do not sweep until you pass this checkpoint
# 98 - There is no configuration information for this stage
# 97 - energy insufficient
# 96 - Can only be a positive integer
# 95 - materials insufficient
# 94 - stage mismatch
# 93 - abnormal damage
# 92 - no more ticket, try tomorrow
# 91 - stage error
# 90 - level insufficient
# 89 - Page number error
# 88 - No data for this page
# 87 - You didn't go pass
# 86 - You never hung up before
# 0 - success
```



## stage_enter_general

##### 发送消息JSON格式

进入普通模式关卡<font color=#cc36ee>**1-999**</font>

> stage：进去关卡
>

```json
{
	"world": 0, 
	"function": "stage_enter_general",
	"data": {
		"token": "toekn",
		"stage": 8
	}
}
```

##### 接受消息JSON格式

[成功]()

> remain：剩余物资
>
> reward：改变物资
>
> addition：附加返回的信息
>
> energy：体力变化情况
>
> - cooling：距离下次体力恢复剩余时间
> - remain：剩余体力
> - reward：体力改变值
>

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "remain": [],
        "reward": [],
        "addition"：{},
        "energy": {
            "cooling": -1,
            "remain": 4724,
            "reward": -6
        }
    }
}
```

[失败]()

```python
# 98 - There is no configuration information for this stage
# 97 - energy insufficient
# 95 - materials insufficient
# 94 - stage mismatch
# 92 - no more ticket, try tomorrow
# 91 - stage error
# 90 - level insufficient
```



## stage_victory_general

##### 发送消息JSON格式

通过普通模式关卡<font color=#cc36ee>**1-999**</font>

> stage：通过关卡

```json
{
	"world": 0, 
	"function": "stage_victory_general",
	"data": {
		"token": "toekn",
		"stage": 8
	}
}
```

##### 接受消息JSON格式

[成功]()

> boss：BOSS模式下会用到的BOSS相关信息
>
> remain：物品剩余情况
>
> reward：物品获得情况
>
> exp_info：玩家经验信息
>
> - exp：总经验值
> - level：玩家等级
> - need：距下次升级需要经验值
> - reward：本次通关获得的经验值
>
> max_stage：通关最高关卡

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "boss": {},
        "remain": [
            "3:9:1026325",
            "3:2:152025",
            "3:1:100058375",
            "3:10:5"
        ],
        "reward": [
            "3:9:125",
            "3:2:125",
            "3:1:375",
            "3:10:1"
        ],
        "exp_info": {
            "exp": 37340,
            "level": 25,
            "need": 1660,
            "reward": 500
        },
        "max_stage": 1004
    }
}
```

[失败]()

```python
# 94 - stage mismatch
# 91 - stage error
```



## stage_enter_endless

##### 发送消息JSON格式

进入无尽模式关卡<font color=#cc36ee>**1001-1999**</font>

> stage：进去关卡

```json
{
	"world": 0, 
	"function": "stage_enter_endless",
	"data": {
		"token": "toekn",
		"stage": 1001
	}
}
```

##### 接受消息JSON格式

[成功]()

> remain：剩余物资
>
> reward：改变物资
>
> addition：附加返回的信息
>
> energy：体力变化情况
>
> - cooling：距离下次体力恢复剩余时间
> - remain：剩余体力
> - reward：体力改变值

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "remain": [],
        "reward": [],
        "addition": {
            "els": [
                {
                    "Enemy1": {
                        "LV": 1,
                        "HP": 5000,
                        "MP": 105,
                        "Attack": 9,
                        "PhysicalDefend": 10,
                        "Strength": 21,
                        "Vitality": 19,
                        "Mentality": 24,
                        "Agility": 29,
                        "FlameDefend": 10,
                        "FrozenDefend": 10,
                        "PoisonDefend": 10,
                        "LightningDefend": 10,
                        "Flame": 10,
                        "Frozen": 10,
                        "Poison": 10,
                        "Lightning": 10,
                        "Sacredness": 0,
                        "AttackSpeed": 100,
                        "MoveSpeed": 300,
                        "RotationSpeed": 0,
                        "AttackRange": 50,
                        "CriticalLevel": 1,
                        "CriticalDefend": 1,
                        "AvoidanceRate": 30,
                        "HitRate": 100,
                        "AttackRate": 100,
                        "Exp": 0,
                        "HPRecoverPerSecond": 10,
                        "MPRecoverPerSecond": 0,
                        "LaunchWPRate": 100,
                        "MagicWPRate": 100,
                        "MeleeWPRate": 100,
                        "MissileWPRate": 100,
                        "QuantumWPRate": 100,
                        "CDRate": 100,
                        "baseElementDamageRate": 100,
                        "baseElementDefendRate": 100
                    }
                },
                {
                    "ZombieKid": {
                        "LV": 1,
                        "HP": 5000,
                        "MP": 105,
                        "Attack": 9,
                        "PhysicalDefend": 10,
                        "Strength": 21,
                        "Vitality": 19,
                        "Mentality": 24,
                        "Agility": 29,
                        "FlameDefend": 10,
                        "FrozenDefend": 10,
                        "PoisonDefend": 10,
                        "LightningDefend": 10,
                        "Flame": 10,
                        "Frozen": 10,
                        "Poison": 10,
                        "Lightning": 10,
                        "Sacredness": 0,
                        "AttackSpeed": 100,
                        "MoveSpeed": 300,
                        "RotationSpeed": 0,
                        "AttackRange": 50,
                        "CriticalLevel": 1,
                        "CriticalDefend": 1,
                        "AvoidanceRate": 30,
                        "HitRate": 100,
                        "AttackRate": 100,
                        "Exp": 0,
                        "HPRecoverPerSecond": 10,
                        "MPRecoverPerSecond": 0,
                        "LaunchWPRate": 100,
                        "MagicWPRate": 100,
                        "MeleeWPRate": 100,
                        "MissileWPRate": 100,
                        "QuantumWPRate": 100,
                        "CDRate": 100,
                        "baseElementDamageRate": 100,
                        "baseElementDefendRate": 100
                    }
                }
            ],
            "monsters": {
                "ZombieKid": {
                    "LV": 1,
                    "HP": 5000,
                    "MP": 105,
                    "Attack": 9,
                    "PhysicalDefend": 10,
                    "Strength": 21,
                    "Vitality": 19,
                    "Mentality": 24,
                    "Agility": 29,
                    "FlameDefend": 10,
                    "FrozenDefend": 10,
                    "PoisonDefend": 10,
                    "LightningDefend": 10,
                    "Flame": 10,
                    "Frozen": 10,
                    "Poison": 10,
                    "Lightning": 10,
                    "Sacredness": 0,
                    "AttackSpeed": 100,
                    "MoveSpeed": 300,
                    "RotationSpeed": 0,
                    "AttackRange": 50,
                    "CriticalLevel": 1,
                    "CriticalDefend": 1,
                    "AvoidanceRate": 30,
                    "HitRate": 100,
                    "AttackRate": 100,
                    "Exp": 0,
                    "HPRecoverPerSecond": 10,
                    "MPRecoverPerSecond": 0,
                    "LaunchWPRate": 100,
                    "MagicWPRate": 100,
                    "MeleeWPRate": 100,
                    "MissileWPRate": 100,
                    "QuantumWPRate": 100,
                    "CDRate": 100,
                    "baseElementDamageRate": 100,
                    "baseElementDefendRate": 100
                },
                "Enemy1": {
                    "LV": 1,
                    "HP": 5000,
                    "MP": 105,
                    "Attack": 9,
                    "PhysicalDefend": 10,
                    "Strength": 21,
                    "Vitality": 19,
                    "Mentality": 24,
                    "Agility": 29,
                    "FlameDefend": 10,
                    "FrozenDefend": 10,
                    "PoisonDefend": 10,
                    "LightningDefend": 10,
                    "Flame": 10,
                    "Frozen": 10,
                    "Poison": 10,
                    "Lightning": 10,
                    "Sacredness": 0,
                    "AttackSpeed": 100,
                    "MoveSpeed": 300,
                    "RotationSpeed": 0,
                    "AttackRange": 50,
                    "CriticalLevel": 1,
                    "CriticalDefend": 1,
                    "AvoidanceRate": 30,
                    "HitRate": 100,
                    "AttackRate": 100,
                    "Exp": 0,
                    "HPRecoverPerSecond": 10,
                    "MPRecoverPerSecond": 0,
                    "LaunchWPRate": 100,
                    "MagicWPRate": 100,
                    "MeleeWPRate": 100,
                    "MissileWPRate": 100,
                    "QuantumWPRate": 100,
                    "CDRate": 100,
                    "baseElementDamageRate": 100,
                    "baseElementDefendRate": 100
                }
            }
        },
        "energy": {
            "cooling": -1,
            "remain": 4712,
            "reward": -6
        }
    }
}

```

[失败]()

```python
# 98 - There is no configuration information for this stage
# 97 - energy insufficient
# 95 - materials insufficient
# 94 - stage mismatch
# 92 - no more ticket, try tomorrow
# 91 - stage error
# 90 - level insufficient
```



## stage_victory_endless

##### 发送消息JSON格式

通过关卡<font color=#cc36ee>**1001-1999**</font>

> stage：通过关卡

```json
{
	"world": 0, 
	"function": "stage_victory_endless",
	"data": {
		"token": "toekn",
		"stage": 1001
	}
}
```

##### 接受消息JSON格式

[成功]()

> boss：BOSS模式下会用到的BOSS相关信息
>
> remain：物品剩余情况
>
> reward：物品获得情况
>
> exp_info：玩家经验信息
>
> - exp：总经验值
> - level：玩家等级
> - need：距下次升级需要经验值
> - reward：本次通关获得的经验值

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "boss": {},
        "remain": [
            "3:9:1026325",
            "3:2:152025",
            "3:1:100058375",
            "3:10:5"
        ],
        "reward": [
            "3:9:125",
            "3:2:125",
            "3:1:375",
            "3:10:1"
        ],
        "exp_info": {
            "exp": 37340,
            "level": 25,
            "need": 1660,
            "reward": 500
        },
        "max_stage": 1004
    }
}
```

[失败]()

```python
# 94 - stage mismatch
# 91 - stage error
```



## stage_enter_boss

##### 发送消息JSON格式

进入BOSS模式关卡<font color=#cc36ee>**3001-3999**</font>

> stage：进去关卡

```json
{
	"world": 0, 
	"function": "stage_enter_boss",
	"data": {
		"token": "toekn",
		"stage": 3001
	}
}
```

##### 接受消息JSON格式

[成功]()

> BOSS：boss门票剩余情况
>
> remain：剩余物资
>
> reward：改变物资
>
> addition：附加返回的信息
>
> energy：体力变化情况
>
> - cooling：距离下次体力恢复剩余时间
> - remain：剩余体力
> - reward：体力改变值

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "remain": [],
        "reward": [],
        "BOSS": {
            "limits": {
                "18": 2
            },
            "cd": 31280
        },
        "addition"：{},
        "energy": {
            "cooling": -1,
            "remain": 4892,
            "reward": -6
        }
    }
}

```

[失败]()

```python
# 98 - There is no configuration information for this stage
# 97 - energy insufficient
# 95 - materials insufficient
# 94 - stage mismatch
# 92 - no more ticket, try tomorrow
# 91 - stage error
# 90 - level insufficient
```



## stage_victory_boss

##### 发送消息JSON格式

通过关卡<font color=#cc36ee>**3001-3999**</font>

> stage：通过关卡
>
> damage：最高伤害

```json
{
	"world": 0, 
	"function": "stage_victory_boss",
	"data": {
		"token": "toekn",
		"stage": 3001,
        "damage": 10000
	}
}
```

##### 接受消息JSON格式

[成功]()

> boss：BOSS模式下会用到的BOSS相关信息
>
> - stage：当前关卡
> - record：1代表是新记录，0代表不是新记录
> - bds：boss的部分信息
>    - damage：造成的最高伤害，不是本次造成的伤害
>    - ratio：boss的血量百分比
>    - total：玩家对当前BOSS造成的总伤害
>    - hp：boss当前的剩余血量
>
> remain：物品剩余情况
>
> reward：物品获得情况
>
> exp_info：玩家经验信息
>
> - exp：总经验值
> - level：玩家等级
> - need：距下次升级需要经验值
> - reward：本次通关获得的经验值

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "boss": {
            "record": 0,
            "stage": 3001,
            "bds": {
                "hp": 9994500,
                "ratio": "1.00",
                "damage": 5500,
                "total": 21000
            }
        },
        "remain": [
            "3:9:1500",
            "3:2:1500",
            "3:1:4500",
            "3:10:12"
        ],
        "reward": [
            "3:9:125",
            "3:2:125",
            "3:1:375",
            "3:10:1"
        ],
        "exp_info": {
            "exp": 420000,
            "level": 84,
            "need": 8400,
            "reward": 0
        },
        "max_stage": 3001
    }
}
```

[失败]()

```python
# 94 - stage mismatch
# 93 - abnormal damage
# 91 - stage error
```



## stage_enter_coin

##### 发送消息JSON格式

进入金币挑战模式关卡<font color=#cc36ee>**4001-4149**</font>

> stage：进去关卡

```json
{
	"world": 0, 
	"function": "stage_enter_coin",
	"data": {
		"token": "toekn",
		"stage": 4001
	}
}
```

##### 接受消息JSON格式

[成功]()

> remain：剩余物资
>
> reward ：改变物资
>
> COIN：金币挑战门票情况
>
> - limits：门票剩余情况
>
>   - 19：金币挑战模式剩余门票数
>
>   - 20：剩余可购买门票数
> - cd：剩余刷新金币挑战门票的时间
>
> addition：附加返回的信息
>
> energy：体力变化情况
>
> - cooling：距离下次体力恢复剩余时间
> - remain：剩余体力
> - reward：体力改变值

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "remain": [],
        "reward": [],
        "COIN": {
            "limits": {
                "19": 0,
                "20": 3
            },
            "cd": 30471
        },
		"addition"：{},        
        "energy": {
            "cooling": -1,
            "remain": 4886,
            "reward": -6
        }
    }
}
```

[失败]()

```python
# 98 - There is no configuration information for this stage
# 97 - energy insufficient
# 95 - materials insufficient
# 94 - stage mismatch
# 92 - no more ticket, try tomorrow
# 91 - stage error
# 90 - level insufficient
```



## stage_victory_coin

##### 发送消息JSON格式

通过关卡<font color=#cc36ee>**4001-4149**</font>

> stage：通过关卡

```json
{
	"world": 0, 
	"function": "stage_victory_coin",
	"data": {
		"token": "toekn",
		"stage": 4001
	}
}
```

##### 接受消息JSON格式

[成功]()

> boss：BOSS模式下会用到的BOSS相关信息
>
> remain：物品剩余情况
>
> reward：物品获得情况
>
> exp_info：玩家经验信息
>
> - exp：总经验值
> - level：玩家等级
> - need：距下次升级需要经验值
> - reward：本次通关获得的经验值

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "boss": {},
        "remain": [
            "3:1:100064875",
            "3:18:2"
        ],
        "reward": [
            "3:1:5000",
            "3:18:1"
        ],
        "exp_info": {
            "exp": 39340,
            "level": 26,
            "need": 2780,
            "reward": 0
        },
        "max_stage": 1004
    }
}
```

[失败]()

```python
# 94 - stage mismatch
# 91 - stage error
```



## stage_enter_exp

##### 发送消息JSON格式

进入经验挑战模式关卡<font color=#cc36ee>**4151-4199**</font>

> stage：进去关卡

```json
{
	"world": 0, 
	"function": "stage_enter_exp",
	"data": {
		"token": "toekn",
		"stage": 4151
	}
}
```

##### 接受消息JSON格式

[成功]()

> remain：剩余物资
>
> reward：改变物资
>
> EXP：经验挑战门票情况
>
> - limits：门票剩余情况
>
>   - 21：经验挑战模式剩余门票数
>
>   - 22：剩余可购买门票数
> - cd：剩余刷新经验挑战门票的时间
>
> addition：附加返回的信息
>
> energy：体力变化情况
>
> - cooling：距离下次体力恢复剩余时间
> - remain：剩余体力
> - reward：体力改变值

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "remain": [],
		"reward": [],
        "EXP": {
            "limits": {
                "21": 1,
                "22": 2
            },
            "cd": 30061
        },
		"addition"：{},
        "energy": {
            "cooling": -1,
            "remain": 4880,
            "reward": -6
        }
    }
}
```

[失败]()

```python
# 98 - There is no configuration information for this stage
# 97 - energy insufficient
# 95 - materials insufficient
# 94 - stage mismatch
# 92 - no more ticket, try tomorrow
# 91 - stage error
# 90 - level insufficient
```



## stage_victory_exp

##### 发送消息JSON格式

通过关卡<font color=#cc36ee>**4151-4199**</font>

> stage：通过关卡

```json
{
	"world": 0, 
	"function": "stage_victory_exp",
	"data": {
		"token": "toekn",
		"stage": 4151
	}
}
```

##### 接受消息JSON格式

[成功]()

> boss：BOSS模式下会用到的BOSS相关信息
>
> remain：物品剩余情况
>
> reward：物品获得情况
>
> exp_info：玩家经验信息
>
> - exp：总经验值
> - level：玩家等级
> - need：距下次升级需要经验值
> - reward：本次通关获得的经验值

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "boss": {},
        "remain": [
            "3:9:1031825",
            "3:19:1"
        ],
        "reward": [
            "3:9:5000",
            "3:19:1"
        ],
        "exp_info": {
            "exp": 39340,
            "level": 26,
            "need": 2780,
            "reward": 0
        },
        "max_stage": 1004
    }
}
```

[失败]()

```python
# 94 - stage mismatch
# 91 - stage error
```



## stage_refresh_boss

##### 发送消息JSON格式

刷新boss情况，同时更新自己可挑战boss的情况

stage：刷新获取当前关卡的BOSS伤害信息

```json
{
	"world": 0, 
	"function": "stage_refresh_boss",
	"data": {
		"token": "toekn"
	}
}
```

##### 接受消息JSON格式

[成功]()

> total：对BOSS造成的累计伤害
>
> limit：今天可挑战BOSS模式的次数
>
> cd：今天刷新挑战BOSS模式次数的剩余时间
>
> mcd：刷新所有BOSS血量的剩余时间
>
> bds：boss的相关信息和自己对此BOSS的伤害信息
>
> - damage：自己对BOSS造成的最高伤害
>
> - ratio：BOSS的血量情况
>
> - hp：BOSS的剩余血量情况
>
> - total：当前关卡下对BOSS造成的总伤害

```json
{
    "status": 0,
    "message": "Successfully get hook information",
    "data": {
        "bds": {
            "3001": {
                "hp": 10000000,
                "ratio": "1.00",
                "damage": 5500,
                "total": 10000
            },
            "3002": {
                "hp": 30000000,
                "ratio": "1.00",
                "damage": 0,
                "total": 0
            }
        },
        "limit": 1,
        "cd": 45882,
        "mcd": 1428282
    }
}
```

[失败]()

无



## stage_all_infos

##### 发送消息JSON格式

返回所有关卡的最新信息

```json
{
	"world": 0, 
	"function": "stage_all_infos",
	"data": {
		"token": "toekn"
	}
}
```

##### 接受消息JSON格式

[成功]()

> infos：关卡最大关卡的信息
>
> - sid：max stage
>
> limits：关卡模式下的部分限制信息
>
> - sid：{lid：val}

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "infos": {
            "0": 1,
            "1": 1000,
            "3": 3001,
            "4": 4000,
            "5": 4150
        },
        "limits": {
            "3": {
                "18": 1
            },
            "4": {
                "19": 2,
                "20": 3
            },
            "5": {
                "21": 2,
                "22": 3
            }
        }
    }
}
```

[失败]()

无



## stage_damage_ranking

##### 发送消息JSON格式

获取世界boss的伤害排行榜，一次只会获取10个人的伤害排行榜

>page: 排行序数，比如1就是排行1～10名的信息，2就是排行11～20的信息依次类推，页码从1开始
>
>stage：需要排行的关卡BOSS

```json
{
	"world": 0,
	"function": "stage_damage_ranking",
	"data": {
		"token": "my token",
    	"page":1,
        "stage": 3001
	}
}
```

##### 接受消息JSON格式

[成功消息]()

> damange: 玩家造成的最高伤害
>
> own_rank: 玩家自己的排名伤害等信息，不存在则返回-1
>
> rank：排名玩家的信息
>
> - NO：名次
> - name：游戏名字
> - damage：最高伤害
> - fid：家族名字
> - level：玩家等级

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "page": 1,
        "own_rank": {
            "1": {
                "damage": 4500,
                "rank": 1
            },
            "3001": {
                "damage": 18000,
                "rank": 1
            }
        },
        "rank": [
            {
                "NO": 1,
                "name": "gnt100",
                "damage": 18000,
                "fid": "",
                "level": 84
            }
        ]
    }
}
```

[失败消息]()

```python
# 89 - Page number error
# 88 - No data for this page
```



## stage_hang_up

##### 发送消息JSON格式

获取最高无尽模式下的关卡下的奖励，每次无尽关卡通关获取一次奖励

```json
{
	"world": 0,
	"function": "stage_hang_up",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[成功消息]()

> remain: 物资剩余信息
>
> reward: 物资奖励信息
>
> exp_info：玩家经验变化信息
>

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "remain": [
            "3:1:100072585"
        ],
        "reward": [
            "3:1:0"
        ],
        "exp_info": {
            "exp": 40900,
            "level": 26,
            "need": 1220,
            "reward": 0
        }
    }
}
```

[失败消息]()

```python
# 87 - You didn't go pass
# 86 - You never hung up before
```



## stage_mopping_up

##### 发送消息JSON格式

扫荡关卡，扣取体力并立即获得物资
> stage：需要扫荡的关卡
>
> count：扫荡的次数
>
> ```json
> {
> 	"world": 0, 
> 	"function": "stage_mopping_up",
> 	"data": {
> 		"token": "my toekn ^_^",
> 		"stage": 8,
>         	"count": 1
> 	}
> }
> ```
>
> ##### 接受消息JSON格式
>
> [成功]()
>
> > remain：剩余物资情况
> >
> > reward：物资改变情况
> >
> > energy：体力变化情况
> >
> > - cooling：距离下次体力恢复剩余时间
> > - remain：剩余体力
> > - reward：体力改变值
> >
> > exp_info：经验信息变化情况
> >
> > - exp：当前经验
> > - level：当前角色等级
> > - need：升到下一级需要的经验
> > - reward：经验改变情况

```python
{
    "status": 0,
    "message": "success",
    "data": {
        "energy": {
            "cooling": -1,
            "remain": 4730,
            "reward": -6
        },
        "remain": [
            "3:9:1002800",
            "3:1:100059350",
            "3:2:156220"
        ],
        "reward": [
            "3:9:100",
            "3:1:200",
            "3:2:200"
        ],
        "exp_info": {
            "exp": 45520,
            "level": 28,
            "need": 3200,
            "reward": 120
        }
    }
}
```















