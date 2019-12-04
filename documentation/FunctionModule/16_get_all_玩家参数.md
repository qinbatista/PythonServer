## 方法列表

* [`get_config_version`](##get_config_version)
* [`get_config_stage`](##get_config_stage)
* [`get_config_boss`](##get_config_boss)
* [`get_config_lottery`](##get_config_lottery)
* [`get_config_weapon`](##get_config_weapon)
* [`get_config_skill`](##get_config_skill)
* [`get_config_mall`](##get_config_mall)
* [`get_config_role`](##get_config_role)
* [`get_config_task`](##get_config_task)
* [`get_config_achievement`](##get_config_achievement)
* [`get_config_check_in`](##get_config_check_in)
* [`get_config_vip`](##get_config_vip)
* [`get_config_player`](##get_config_player)
* [`get_config_factory`](##get_config_factory)
* [`get_config_family`](##get_config_family)
* [`get_config_exchange`](##get_config_exchange)

## get_config_version

##### 发送消息JSON格式

```json
{
	"world": 0,
	"function": "get_config_version",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[成功]()

>  version: 版本号

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"version": "1.0"
	}
}
```





## get_config_stage

##### 发送消息JSON格式

获取关卡的消耗列表与关卡的奖励列表entry_consumables_config.json, stage_reward_config.json 关卡 hang_reward_config.json挂机信息

> 无
>

```json
{
	"world": 0,
	"function": "get_config_stage",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[成功]()

> entry_consumables_config：返回entry_consumables_config.json
>
> stage_reward_config：返回stage_reward_config.json
>
> hang_reward_config: 返回hang_reward_config.json

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"entry_consumables_config": {
			"0": {
				"2": 0,
				"1": 0,
				"cost": 0
			},
			"1": {
				"2": 0,
				"1": 0,
				"cost": 1
			},
			"2": {
				"2": 0,
				"1": 0,
				"cost": 1
			},
			"3": {
				"2": 0,
				"1": 0,
				"cost": 1
			},
			"4": {
				"2": 0,
				"1": 0,
				"cost": 1
			},
			"5": {
				"2": 0,
				"1": 0,
				"cost": 1
			},
			"6": {
				"2": 0,
				"1": 0,
				"cost": 1
			},
			"7": {
				"2": 0,
				"1": 0,
				"cost": 1
			},
			"8": {
				"2": 0,
				"1": 0,
				"cost": 1
			},
			"1001": {
				"1": 3,
				"cost": 2
			},
			"1002": {
				"1": 3,
				"cost": 2
			},
			"1003": {
				"1": 3,
				"cost": 2
			},
			"1004": {
				"2": 210,
				"1": 220,
				"cost": 2
			},
			"1005": {
				"2": 250,
				"1": 220,
				"cost": 2
			},
			"1006": {
				"2": 3,
				"cost": 2
			}
		},
		"stage_reward_config": {
			"1": {
				"10": 1,
				"exp": 10
			},
			"2": {
				"9": 125,
				"exp": 10,
				"2": 125,
				"1": 375,
				"10": 1
			},
			"3": {
				"9": 150,
				"exp": 10,
				"2": 150,
				"1": 450,
				"10": 1
			},
			"4": {
				"9": 175,
				"exp": 10,
				"2": 175,
				"1": 525,
				"10": 1
			},
			"5": {
				"9": 200,
				"exp": 10,
				"2": 200,
				"1": 600,
				"10": 1
			},
			"6": {
				"9": 225,
				"exp": 10,
				"2": 225,
				"1": 675,
				"10": 1
			},
			"7": {
				"9": 250,
				"exp": 10,
				"2": 250,
				"1": 750,
				"10": 1
			},
			"8": {
				"9": 275,
				"exp": 10,
				"2": 275,
				"1": 825,
				"10": 1
			},
			"1001": {
				"2": 210,
				"1": 220,
				"exp": 220
			},
			"1002": {
				"2": 250,
				"1": 220,
				"9": 3
			},
			"1003": {
				"2": 310,
				"1": 220,
				"9": 3
			},
			"1004": {
				"2": 310,
				"1": 220,
				"9": 3
			},
			"1005": {
				"2": 310,
				"1": 220,
				"9": 3
			},
			"1006": {
				"2": 310,
				"1": 220,
				"9": 3
			},
			"1007": {
				"2": 310,
				"1": 220,
				"9": 3
			},
			"1008": {
				"2": 310,
				"1": 220,
				"9": 3
			},
			"1009": {
				"2": 310,
				"1": 220,
				"9": 3
			},
			"1010": [
				"skill_M0",
				"skill_P0",
				"skill_G0"
			],
			"1020": [
				"weapon1",
				"weapon2",
				"weapon3"
			],
			"1030": [
				"weapon4",
				"weapon5",
				"weapon6",
				"weapon7"
			],
			"1040": [
				"skill_M0",
				"skill_M1",
				"skill_M2",
				"skill_P0",
				"skill_P1",
				"skill_P2",
				"skill_G0",
				"skill_G1",
				"skill_G2"
			],
			"1050": [
				"weapon8",
				"weapon9",
				"weapon10"
			],
			"1060": [
				"skill_M3",
				"skill_M4",
				"skill_M5",
				"skill_M6",
				"skill_M7",
				"skill_M8",
				"skill_M9",
				"skill_M10",
				"skill_M11",
				"skill_M12"
			],
			"1070": [
				"weapon11",
				"weapon12",
				"weapon13",
				"weapon14",
				"weapon15",
				"weapon16",
				"weapon17",
				"weapon18",
				"weapon19",
				"weapon20"
			],
			"1080": [
				"skill_P3",
				"skill_P4",
				"skill_P5",
				"skill_P6",
				"skill_P7",
				"skill_P8",
				"skill_P9",
				"skill_P10",
				"skill_P11",
				"skill_P12"
			],
			"1090": [
				"weapon21",
				"weapon22",
				"weapon23",
				"weapon24",
				"weapon25",
				"weapon26",
				"weapon27",
				"weapon28",
				"weapon29",
				"weapon30"
			],
			"1100": [
				"weapon31",
				"weapon32",
				"weapon33",
				"weapon34",
				"weapon35",
				"weapon36",
				"weapon37",
				"weapon38",
				"weapon39",
				"weapon40",
				"skill_G0",
				"skill_G1",
				"skill_G2",
				"skill_G3",
				"skill_G4",
				"skill_G5",
				"skill_G6",
				"skill_G7",
				"skill_G8",
				"skill_G9",
				"skill_G10",
				"skill_G11",
				"skill_G12"
			],
			"skill_MPG": {
				"M": 0,
				"P": 13,
				"G": 26
			},
			"skill": [
				"skill_M0",
				"skill_M1",
				"skill_M2",
				"skill_M3",
				"skill_M4",
				"skill_M5",
				"skill_M6",
				"skill_M7",
				"skill_M8",
				"skill_M9",
				"skill_M10",
				"skill_M11",
				"skill_M12",
				"skill_P0",
				"skill_P1",
				"skill_P2",
				"skill_P3",
				"skill_P4",
				"skill_P5",
				"skill_P6",
				"skill_P7",
				"skill_P8",
				"skill_P9",
				"skill_P10",
				"skill_P11",
				"skill_P12",
				"skill_G0",
				"skill_G1",
				"skill_G2",
				"skill_G3",
				"skill_G4",
				"skill_G5",
				"skill_G6",
				"skill_G7",
				"skill_G8",
				"skill_G9",
				"skill_G10",
				"skill_G11",
				"skill_G12"
			],
			"weapon": [
				"weapon1",
				"weapon2",
				"weapon3",
				"weapon4",
				"weapon5",
				"weapon6",
				"weapon7",
				"weapon8",
				"weapon9",
				"weapon10",
				"weapon11",
				"weapon12",
				"weapon13",
				"weapon14",
				"weapon15",
				"weapon16",
				"weapon17",
				"weapon18",
				"weapon19",
				"weapon20",
				"weapon21",
				"weapon22",
				"weapon23",
				"weapon24",
				"weapon25",
				"weapon26",
				"weapon27",
				"weapon28",
				"weapon29",
				"weapon30",
				"weapon31",
				"weapon32",
				"weapon33",
				"weapon34",
				"weapon35",
				"weapon36",
				"weapon37",
				"weapon38",
				"weapon39",
				"weapon40"
			],
			"skill_scroll": [
				6,
				7,
				8
			],
			"scroll_range": [
				1,
				10
			],
			"weights": [
				0.5,
				0.3,
				0.2
			],
			"segment_range": [
				30,
				60
			]
		},
		"hang_reward_config": {
			"0": {
				"2": 0,
				"1": 0
			},
			"1": {
				"2": 10,
				"1": 30,
				"11": [
					1,
					12,
					100
				]
			},
			"2": {
				"2": 20,
				"1": 60,
				"11": [
					1,
					100,
					1000
				]
			},
			"3": {
				"2": 30,
				"1": 90
			},
			"4": {
				"2": 40,
				"1": 120
			},
			"5": {
				"2": 50,
				"1": 150
			},
			"6": {
				"2": 60,
				"1": 180
			},
			"7": {
				"2": 70,
				"1": 210
			},
			"8": {
				"2": 80,
				"1": 240
			},
			"probability_reward": [
				"11",
				"12",
				"13",
				"6",
				"7",
				"8"
			]
		}
	}
}
```





## get_config_boss

获取world_boss_config.json的配置文件信息

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_boss",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

[成功]()

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"config": {
			"max_enter_time": 3,
			"max_upload_damage": 200000,
			"boss1": {
				"life_value": 10000
			},
			"boss2": {
				"life_value": 100000
			},
			"boss3": {
				"life_value": 100000
			},
			"boss4": {
				"life_value": 100000
			},
			"boss5": {
				"life_value": 100000
			},
			"boss6": {
				"life_value": 100000
			},
			"boss7": {
				"life_value": 100000
			},
			"boss8": {
				"life_value": 100000
			},
			"boss9": {
				"life_value": 100000
			},
			"boss10": {
				"life_value": 100000
			}
		}
	}
}
```



## get_config_lottery

获取lottery.json的配置文件信息

##### 发送消息JSON格式

> 无

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

返回转盘和抽奖的消耗信息，配置文件来自lottery.json

[成功]()

> lottery：返回lottery.json

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



## get_config_weapon

获取weapon_config.json的配置文件信息

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_weapon",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回武器升级、突破、重置技能等消耗信息和配置文件信息weapon_config.json

[成功]()

> weapon_config：返回weapon_config.json

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"seg": 25,
		"reset": 100,
		"cost": 40,
		"weapon_config": {
			"standard_iron_count": 20,
			"standard_segment_count": 30,
			"standard_reset_weapon_skill_coin_count": 100,
			"valid_passive_skills": [
				"passive_skill_1_level",
				"passive_skill_2_level",
				"passive_skill_3_level",
				"passive_skill_4_level"
			],
			"weapons": [
				"weapon1",
				"weapon2",
				"weapon3",
				"weapon4",
				"weapon5",
				"weapon6",
				"weapon7",
				"weapon8",
				"weapon9",
				"weapon10",
				"weapon11",
				"weapon12",
				"weapon13",
				"weapon14",
				"weapon15",
				"weapon16",
				"weapon17",
				"weapon18",
				"weapon19",
				"weapon20",
				"weapon21",
				"weapon22",
				"weapon23",
				"weapon24",
				"weapon25",
				"weapon26",
				"weapon27",
				"weapon28",
				"weapon29",
				"weapon30",
				"weapon31",
				"weapon32",
				"weapon33",
				"weapon34",
				"weapon35",
				"weapon36",
				"weapon37",
				"weapon38",
				"weapon39",
				"weapon40"
			]
		}
	}
}
```



## get_config_skill

获取skill_level_up_config.json的配置文件信息

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_weapon",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回技能配置信息，配置文件来自skill_level_up_config.json

[成功]()

> skill_config：返回skill_level_up_config.json

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"skill_config": {
			"skill_scroll_id": [
				"6",
				"7",
				"8"
			],
			"upgrade_chance": {
				"6": 0.1,
				"7": 0.3,
				"8": 1
			}
		}
	}
}
```





## get_config_mall

获取mall_config.json的配置文件信息

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_mall",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回黑市配置信息，配置文件来自mall_config.json

[成功]()

> mall_config：返回mall_config.json

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"mall_config": {
			"diamond": {
				"merchandise_type": [
					"energy",
					"coin",
					"basic_summon_scroll",
					"pro_summon_scroll",
					"skill_scroll_10",
					"skill_scroll_30",
					"skill_scroll_100"
				],
				"energy": {
					"package_type": [
						"1",
						"2"
					],
					"1": {
						"c_quantity": 30,
						"m_quantity": 10
					},
					"2": {
						"c_quantity": 87,
						"m_quantity": 100
					}
				},
				"coin": {
					"package_type": [
						"1",
						"2",
						"3"
					],
					"1": {
						"c_quantity": 30,
						"m_quantity": 4800
					},
					"2": {
						"c_quantity": 87,
						"m_quantity": 14400
					},
					"3": {
						"c_quantity": 270,
						"m_quantity": 43200
					}
				},
				"basic_summon_scroll": {
					"package_type": [
						"1",
						"2",
						"3"
					],
					"1": {
						"c_quantity": 10,
						"m_quantity": 1
					},
					"2": {
						"c_quantity": 90,
						"m_quantity": 10
					},
					"3": {
						"c_quantity": 800,
						"m_quantity": 100
					}
				},
				"pro_summon_scroll": {
					"package_type": [
						"1",
						"2"
					],
					"1": {
						"c_quantity": 30,
						"m_quantity": 1
					},
					"2": {
						"c_quantity": 270,
						"m_quantity": 10
					}
				},
				"skill_scroll_10": {
					"package_type": [
						"1",
						"2",
						"3"
					],
					"1": {
						"c_quantity": 30,
						"m_quantity": 10
					},
					"2": {
						"c_quantity": 87,
						"m_quantity": 30
					},
					"3": {
						"c_quantity": 270,
						"m_quantity": 100
					}
				},
				"skill_scroll_30": {
					"package_type": [
						"1",
						"2",
						"3"
					],
					"1": {
						"c_quantity": 30,
						"m_quantity": 10
					},
					"2": {
						"c_quantity": 87,
						"m_quantity": 30
					},
					"3": {
						"c_quantity": 270,
						"m_quantity": 100
					}
				},
				"skill_scroll_100": {
					"package_type": [
						"1",
						"2",
						"3"
					],
					"1": {
						"c_quantity": 30,
						"m_quantity": 10
					},
					"2": {
						"c_quantity": 87,
						"m_quantity": 30
					},
					"3": {
						"c_quantity": 270,
						"m_quantity": 100
					}
				}
			},
			"coin": {
				"merchandise_type": [
					"energy",
					"coin",
					"basic_summon_scroll",
					"pro_summon_scroll",
					"skill_scroll_10",
					"skill_scroll_30",
					"skill_scroll_100"
				],
				"energy": {
					"package_type": [
						"1",
						"2"
					],
					"1": {
						"c_quantity": 30,
						"m_quantity": 10
					},
					"2": {
						"c_quantity": 87,
						"m_quantity": 100
					}
				},
				"coin": {
					"package_type": [
						"1",
						"2",
						"3"
					],
					"1": {
						"c_quantity": 30,
						"m_quantity": 4800
					},
					"2": {
						"c_quantity": 87,
						"m_quantity": 14400
					},
					"3": {
						"c_quantity": 270,
						"m_quantity": 43200
					}
				},
				"basic_summon_scroll": {
					"package_type": [
						"1",
						"2",
						"3"
					],
					"1": {
						"c_quantity": 10,
						"m_quantity": 1
					},
					"2": {
						"c_quantity": 90,
						"m_quantity": 10
					},
					"3": {
						"c_quantity": 800,
						"m_quantity": 100
					}
				},
				"pro_summon_scroll": {
					"package_type": [
						"1",
						"2"
					],
					"1": {
						"c_quantity": 30,
						"m_quantity": 1
					},
					"2": {
						"c_quantity": 270,
						"m_quantity": 10
					}
				},
				"skill_scroll_10": {
					"package_type": [
						"1",
						"2",
						"3"
					],
					"1": {
						"c_quantity": 30,
						"m_quantity": 10
					},
					"2": {
						"c_quantity": 87,
						"m_quantity": 30
					},
					"3": {
						"c_quantity": 270,
						"m_quantity": 100
					}
				},
				"skill_scroll_30": {
					"package_type": [
						"1",
						"2",
						"3"
					],
					"1": {
						"c_quantity": 30,
						"m_quantity": 10
					},
					"2": {
						"c_quantity": 87,
						"m_quantity": 30
					},
					"3": {
						"c_quantity": 270,
						"m_quantity": 100
					}
				},
				"skill_scroll_100": {
					"package_type": [
						"1",
						"2",
						"3"
					],
					"1": {
						"c_quantity": 30,
						"m_quantity": 10
					},
					"2": {
						"c_quantity": 87,
						"m_quantity": 30
					},
					"3": {
						"c_quantity": 270,
						"m_quantity": 100
					}
				}
			},
			"rmb": {
				"merchandise_type": [
					"diamond",
					"energy",
					"coin",
					"basic_summon_scroll",
					"pro_summon_scroll",
					"skill_scroll_10",
					"skill_scroll_30",
					"skill_scroll_100"
				],
				"diamond": {
					"package_type": [
						"1",
						"2",
						"3",
						"4",
						"5"
					],
					"1": {
						"c_quantity": 1,
						"m_quantity": 80
					},
					"2": {
						"c_quantity": 5,
						"m_quantity": 500
					},
					"3": {
						"c_quantity": 10,
						"m_quantity": 1200
					},
					"4": {
						"c_quantity": 20,
						"m_quantity": 2500
					},
					"5": {
						"c_quantity": 100,
						"m_quantity": 14000
					}
				},
				"energy": {
					"package_type": [
						"1",
						"2"
					],
					"1": {
						"c_quantity": 30,
						"m_quantity": 10
					},
					"2": {
						"c_quantity": 87,
						"m_quantity": 100
					}
				},
				"coin": {
					"package_type": [
						"1",
						"2",
						"3"
					],
					"1": {
						"c_quantity": 30,
						"m_quantity": 4800
					},
					"2": {
						"c_quantity": 87,
						"m_quantity": 14400
					},
					"3": {
						"c_quantity": 270,
						"m_quantity": 43200
					}
				},
				"basic_summon_scroll": {
					"package_type": [
						"1",
						"2",
						"3"
					],
					"1": {
						"c_quantity": 10,
						"m_quantity": 1
					},
					"2": {
						"c_quantity": 90,
						"m_quantity": 10
					},
					"3": {
						"c_quantity": 800,
						"m_quantity": 100
					}
				},
				"pro_summon_scroll": {
					"package_type": [
						"1",
						"2"
					],
					"1": {
						"c_quantity": 30,
						"m_quantity": 1
					},
					"2": {
						"c_quantity": 270,
						"m_quantity": 10
					}
				},
				"skill_scroll_10": {
					"package_type": [
						"1",
						"2",
						"3"
					],
					"1": {
						"c_quantity": 30,
						"m_quantity": 10
					},
					"2": {
						"c_quantity": 87,
						"m_quantity": 30
					},
					"3": {
						"c_quantity": 270,
						"m_quantity": 100
					}
				},
				"skill_scroll_30": {
					"package_type": [
						"1",
						"2",
						"3"
					],
					"1": {
						"c_quantity": 30,
						"m_quantity": 10
					},
					"2": {
						"c_quantity": 87,
						"m_quantity": 30
					},
					"3": {
						"c_quantity": 270,
						"m_quantity": 100
					}
				},
				"skill_scroll_100": {
					"package_type": [
						"1",
						"2",
						"3"
					],
					"1": {
						"c_quantity": 30,
						"m_quantity": 10
					},
					"2": {
						"c_quantity": 87,
						"m_quantity": 30
					},
					"3": {
						"c_quantity": 270,
						"m_quantity": 100
					}
				}
			}
		}
	}
}
```



## get_config_role

获取role_config.json的配置文件信息

##### 发送消息JSON格式

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

返回角色配置信息，配置文件来自role_config.json

[成功]()

> role_config：返回role_config.json

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"seg": 25,
		"exp_pot": 5,
		"role_config": {
			"standard_experience_potion_count": 20,
			"standard_segment_count": 30,
			"standard_reset_role_skill_coin_count": 100,
			"valid_passive_skills": [
				"passive_skill_1_level",
				"passive_skill_2_level",
				"passive_skill_3_level",
				"passive_skill_4_level"
			],
			"roles": [
				"role1",
				"role2",
				"role3",
				"role4",
				"role5",
				"role6",
				"role7",
				"role8",
				"role9",
				"role10",
				"role11",
				"role12",
				"role13",
				"role14",
				"role15",
				"role16",
				"role17",
				"role18",
				"role19",
				"role20",
				"role21",
				"role22",
				"role23",
				"role24",
				"role25",
				"role26",
				"role27",
				"role28",
				"role29",
				"role30",
				"role31",
				"role32",
				"role33",
				"role34",
				"role35",
				"role36",
				"role37",
				"role38",
				"role39",
				"role40"
			]
		}
	}
}
```



## get_config_task

获取task.json的配置文件信息

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_task",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回任务配置信息信息，配置文件来自task.json

[成功]()

> task：返回task.json

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"task_config": {
			"login": {
				"item_id": 5,
				"quantity": 30
			},
			"check_in": {
				"item_id": 5,
				"quantity": 30
			},
			"role_level_up": {
				"item_id": 5,
				"quantity": 30
			},
			"weapon_level_up": {
				"item_id": 5,
				"quantity": 30
			},
			"pass_main_stage": {
				"item_id": 5,
				"quantity": 30
			},
			"pass_special_stage": {
				"item_id": 5,
				"quantity": 30
			},
			"pass_world_boss": {
				"item_id": 5,
				"quantity": 30
			},
			"basic_summoning": {
				"item_id": 5,
				"quantity": 30
			},
			"pro_summoning": {
				"item_id": 5,
				"quantity": 30
			},
			"check_factory": {
				"item_id": 5,
				"quantity": 30
			},
			"get_friend_gift": {
				"item_id": 5,
				"quantity": 30
			},
			"family_check_in": {
				"item_id": 5,
				"quantity": 30
			},
			"done_10_task": {
				"item_id": 5,
				"quantity": 30
			}
		}
	}
}
```





## get_config_achievement

获取achievement_config.json的配置文件信息

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_achievement",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回广告配置信息，配置文件来自achievement_config.json

[成功]()

> achievement_config：返回achievement_config.json

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"achievement_config": {
			"total_login": {
				"quantity": [
					1,
					2,
					3,
					5,
					8,
					13,
					21,
					34,
					55,
					89,
					144,
					233,
					377,
					610,
					987
				],
				"diamond": [
					30,
					50,
					70,
					90,
					110,
					130,
					150,
					170,
					190,
					210,
					230,
					250,
					270,
					290,
					310
				]
			},
			"keeping_login": {
				"quantity": [
					0,
					3,
					5,
					7,
					9,
					11,
					13,
					15,
					17,
					19,
					21,
					23,
					25,
					27,
					29,
					31
				],
				"diamond": [
					0,
					30,
					50,
					70,
					90,
					110,
					130,
					150,
					170,
					190,
					210,
					230,
					250,
					270,
					290,
					310
				]
			},
			"vip_level": {
				"quantity": [
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
					11,
					12,
					13,
					14,
					15
				],
				"diamond": [
					0,
					50,
					100,
					150,
					200,
					250,
					300,
					350,
					400,
					450,
					500,
					550,
					600,
					650,
					700,
					750
				]
			},
			"get_4_star_role": {
				"quantity": [
					0,
					1,
					3,
					5,
					10,
					15,
					20
				],
				"diamond": [
					0,
					50,
					100,
					150,
					200,
					250,
					300
				]
			},
			"get_5_star_role": {
				"quantity": [
					0,
					1,
					3,
					5,
					10,
					15,
					20
				],
				"diamond": [
					0,
					100,
					200,
					300,
					400,
					500,
					600
				]
			},
			"get_6_star_role": {
				"quantity": [
					0,
					1,
					3,
					5
				],
				"diamond": [
					0,
					200,
					500,
					1000
				]
			},
			"level_up_role": {
				"quantity": [
					0,
					10,
					50,
					100,
					200,
					300,
					400,
					500,
					600,
					700,
					800,
					900,
					1000,
					2000
				],
				"diamond": [
					0,
					10,
					20,
					30,
					40,
					50,
					60,
					70,
					80,
					90,
					100,
					110,
					120,
					130,
					200
				]
			},
			"get_4_star_weapon": {
				"quantity": [
					0,
					1,
					3,
					5,
					10,
					15,
					20
				],
				"diamond": [
					0,
					50,
					100,
					150,
					200,
					250,
					300
				]
			},
			"get_5_star_weapon": {
				"quantity": [
					0,
					1,
					3,
					5,
					10,
					15,
					20
				],
				"diamond": [
					0,
					100,
					200,
					300,
					400,
					500,
					600
				]
			},
			"get_6_star_weapon": {
				"quantity": [
					0,
					1,
					3,
					5
				],
				"diamond": [
					0,
					200,
					500,
					1000
				]
			},
			"level_up_weapon": {
				"quantity": [
					0,
					10,
					50,
					100,
					200,
					300,
					400,
					500,
					600,
					700,
					800,
					900,
					1000,
					2000
				],
				"diamond": [
					0,
					10,
					20,
					30,
					40,
					50,
					60,
					70,
					80,
					90,
					100,
					110,
					120,
					130,
					200
				]
			},
			"pass_stage": {
				"quantity": [
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
					11,
					12,
					13,
					14,
					15,
					16,
					17,
					18,
					19,
					20,
					21,
					22,
					23,
					24,
					25,
					26,
					27,
					28,
					29,
					30,
					31,
					32,
					33,
					34,
					35,
					36,
					37,
					38,
					39,
					40
				],
				"diamond": [
					0,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20,
					20
				]
			},
			"collect_food": {
				"quantity": [
					0,
					10,
					100,
					1000,
					10000,
					100000,
					100000
				],
				"diamond": [
					0,
					100,
					200,
					300,
					400,
					500,
					600
				]
			},
			"collect_mine": {
				"quantity": [
					0,
					10,
					100,
					1000,
					10000,
					100000,
					100000
				],
				"diamond": [
					0,
					100,
					200,
					300,
					400,
					500,
					600
				]
			},
			"collect_crystal": {
				"quantity": [
					0,
					10,
					100,
					1000,
					10000,
					100000,
					100000
				],
				"diamond": [
					0,
					100,
					200,
					300,
					400,
					500,
					600
				]
			},
			"upgrade_food_factory": {
				"quantity": [
					0,
					2,
					5,
					10,
					20,
					30,
					40,
					50,
					60
				],
				"diamond": [
					0,
					10,
					20,
					30,
					40,
					50,
					60,
					70,
					100
				]
			},
			"upgrade_mine_factory": {
				"quantity": [
					0,
					2,
					5,
					10,
					15,
					20,
					25,
					30
				],
				"diamond": [
					0,
					40,
					60,
					80,
					100,
					120,
					140,
					200
				]
			},
			"upgrade_crystal_factory": {
				"quantity": [
					0,
					2,
					4,
					6,
					9,
					12,
					15
				],
				"diamond": [
					0,
					90,
					120,
					150,
					180,
					210,
					300
				]
			},
			"summon_times": {
				"quantity": [
					0,
					10,
					20,
					30,
					40,
					50,
					60,
					70,
					80,
					90,
					100,
					110,
					120,
					200,
					300,
					500
				],
				"diamond": [
					0,
					10,
					20,
					30,
					40,
					50,
					60,
					70,
					80,
					90,
					100,
					110,
					120,
					200,
					300,
					500
				]
			},
			"summon_3_star_weapon_times": {
				"quantity": [
					0,
					1,
					10,
					50,
					100,
					500
				],
				"diamond": [
					0,
					10,
					20,
					40,
					80,
					200
				]
			},
			"summon_4_star_weapon_times": {
				"quantity": [
					0,
					1,
					10,
					50,
					100,
					500
				],
				"diamond": [
					0,
					20,
					40,
					80,
					160,
					400
				]
			},
			"summon_5_star_weapon_times": {
				"quantity": [
					0,
					1,
					10,
					50,
					100,
					500
				],
				"diamond": [
					0,
					30,
					60,
					120,
					240,
					600
				]
			},
			"summon_3_star_role_times": {
				"quantity": [
					0,
					1,
					10,
					50,
					100,
					500
				],
				"diamond": [
					0,
					10,
					20,
					40,
					80,
					200
				]
			},
			"summon_4_star_role_times": {
				"quantity": [
					0,
					1,
					10,
					50,
					100,
					500
				],
				"diamond": [
					0,
					20,
					40,
					80,
					160,
					400
				]
			},
			"summon_5_star_role_times": {
				"quantity": [
					0,
					1,
					10,
					50,
					100,
					500
				],
				"diamond": [
					0,
					30,
					60,
					120,
					240,
					600
				]
			},
			"pro_summon_times": {
				"quantity": [
					0,
					10,
					50,
					100,
					200,
					300,
					400,
					500,
					600,
					700,
					800,
					900,
					1000,
					2000,
					5000,
					10000
				],
				"diamond": [
					0,
					10,
					20,
					30,
					40,
					50,
					60,
					70,
					80,
					90,
					100,
					110,
					120,
					200,
					300,
					500
				]
			},
			"friend_request": {
				"quantity": [
					0,
					1,
					10,
					30,
					50
				],
				"diamond": [
					0,
					20,
					30,
					50,
					100
				]
			},
			"friend_gift": {
				"quantity": [
					0,
					1,
					10,
					50,
					100,
					200,
					500,
					1000,
					2000,
					3000,
					5000
				],
				"diamond": [
					0,
					10,
					20,
					30,
					40,
					50,
					60,
					70,
					80,
					90,
					100
				]
			},
			"check_in_family": {
				"quantity": [
					0,
					1,
					3,
					5,
					10,
					20,
					30,
					40,
					50,
					100
				],
				"diamond": [
					0,
					30,
					40,
					50,
					60,
					70,
					80,
					90,
					100,
					200
				]
			}
		}
	}
}
```





## get_config_check_in

获取check_in.json的配置文件信息

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_check_in",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回签到奖励等配置信息，配置文件来自check_in.json

[成功]()

> check_in_config：返回check_in.json

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"check_in_config": {
			"1": "3:18:1",
			"2": "3:5:100",
			"3": "3:9:100",
			"4": "3:25:100",
			"5": "2:1:5",
			"6": "0:1:5",
			"0": "3:25:100",
			"patch_diamond": 80
		}
	}
}
```



## get_config_vip

获取vip_config.json的配置文件信息

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_vip",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回VIP配置信息，配置文件来自vip_config.json

[成功]()

> vip_config：返回vip_config.json

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"vip_config": {
			"vip_level": {
				"experience": [
					60,
					300,
					940,
					1300,
					2000,
					2900,
					6500,
					11000,
					25000,
					50000,
					100000,
					300000,
					500000,
					1000000
				]
			},
			"vip_dialy_reward": {
				"cooling_time": 86400,
				"1": {
					"diamond_card": 10,
					"coin": 0,
					"small_energy_potion": 0,
					"food_card": 0,
					"mine_card": 0,
					"crystal_card": 0
				},
				"2": {
					"diamond_card": 20,
					"coin": 10000,
					"small_energy_potion": 0,
					"food_card": 0,
					"mine_card": 0,
					"crystal_card": 0
				},
				"3": {
					"diamond_card": 30,
					"coin": 10000,
					"small_energy_potion": 0,
					"food_card": 0,
					"mine_card_card": 0,
					"crystal_card": 0
				},
				"4": {
					"diamond_card": 40,
					"coin": 10000,
					"small_energy_potion": 1,
					"food_card": 0,
					"mine_card": 0,
					"crystal_card": 0
				},
				"5": {
					"diamond_card": 50,
					"coin": 10000,
					"small_energy_potion": 1,
					"food_card": 0,
					"mine_card": 0,
					"crystal_card": 0
				},
				"6": {
					"diamond_card": 60,
					"coin": 10000,
					"small_energy_potion": 1,
					"food_card": 10000,
					"mine_card": 0,
					"crystal_card": 0
				},
				"7": {
					"diamond_card": 70,
					"coin": 10000,
					"small_energy_potion": 1,
					"food_card": 10000,
					"mine_card": 0,
					"crystal_card": 0
				},
				"8": {
					"diamond_card": 80,
					"coin": 20000,
					"small_energy_potion": 1,
					"food_card": 10000,
					"mine_card": 1000,
					"crystal_card": 0
				},
				"9": {
					"diamond_card": 90,
					"coin": 20000,
					"small_energy_potion": 2,
					"food_card": 10000,
					"mine_card": 1000,
					"crystal_card": 0
				},
				"10": {
					"diamond_card": 100,
					"coin": 20000,
					"small_energy_potion": 2,
					"food_card": 20000,
					"mine_card": 1000,
					"crystal_card": 100
				},
				"11": {
					"diamond_card": 110,
					"coin": 20000,
					"small_energy_potion": 2,
					"food_card": 20000,
					"mine_card": 2000,
					"crystal_card": 100
				},
				"12": {
					"diamond_card": 120,
					"coin": 20000,
					"small_energy_potion": 2,
					"food_card": 20000,
					"mine_card": 2000,
					"crystal_card": 200
				},
				"13": {
					"diamond_card": 130,
					"coin": 20000,
					"small_energy_potion": 3,
					"food_card": 20000,
					"mine_card": 2000,
					"crystal_card": 200
				},
				"14": {
					"diamond_card": 140,
					"coin": 20000,
					"small_energy_potion": 3,
					"food_card": 30000,
					"mine_card": 3000,
					"crystal_card": 300
				}
			},
			"vip_speical_package": {
				"1": {
					"reward": {
						"small_energy_potion": 4,
						"universal_segment": 20,
						"universal_segment_6": 0
					},
					"diamond": 300
				},
				"2": {
					"reward": {
						"small_energy_potion": 6,
						"universal_segment": 60,
						"universal_segment_6": 0
					},
					"diamond": 500
				},
				"3": {
					"reward": {
						"small_energy_potion": 8,
						"universal_segment": 80,
						"universal_segment_6": 0
					},
					"diamond": 700
				},
				"4": {
					"reward": {
						"small_energy_potion": 10,
						"universal_segment": 100,
						"universal_segment_6": 0
					},
					"diamond": 900
				},
				"5": {
					"reward": {
						"small_energy_potion": 12,
						"universal_segment": 120,
						"universal_segment_6": 0
					},
					"diamond": 1100
				},
				"6": {
					"reward": {
						"small_energy_potion": 14,
						"universal_segment": 140,
						"universal_segment_6": 20
					},
					"diamond": 1300
				},
				"7": {
					"reward": {
						"small_energy_potion": 16,
						"universal_segment": 160,
						"universal_segment_6": 60
					},
					"diamond": 1500
				},
				"8": {
					"reward": {
						"small_energy_potion": 18,
						"universal_segment": 180,
						"universal_segment_6": 80
					},
					"diamond": 1700
				},
				"9": {
					"reward": {
						"small_energy_potion": 20,
						"universal_segment": 200,
						"universal_segment_6": 100
					},
					"diamond": 1900
				},
				"10": {
					"reward": {
						"small_energy_potion": 22,
						"universal_segment": 220,
						"universal_segment_6": 120
					},
					"diamond": 2100
				},
				"11": {
					"reward": {
						"small_energy_potion": 24,
						"universal_segment": 240,
						"universal_segment_6": 140
					},
					"diamond": 2300
				},
				"12": {
					"reward": {
						"small_energy_potion": 26,
						"universal_segment": 260,
						"universal_segment_6": 160
					},
					"diamond": 2500
				},
				"13": {
					"reward": {
						"small_energy_potion": 28,
						"universal_segment": 280,
						"universal_segment_6": 180
					},
					"diamond": 2700
				},
				"14": {
					"reward": {
						"small_energy_potion": 30,
						"universal_segment": 300,
						"universal_segment_6": 200
					},
					"diamond": 3000
				}
			},
			"buy_energy_config": {
				"default": 2,
				"vip": [
					3,
					3,
					3,
					4,
					4,
					4,
					5,
					5,
					5,
					6,
					6,
					6,
					6,
					6
				]
			},
			"world_boss_challange_times": {
				"defualt": 1,
				"vip": [
					1,
					1,
					1,
					1,
					1,
					1,
					1,
					1,
					1,
					1,
					1,
					1,
					2,
					3
				]
			},
			"coin_card_base_amount": 2000,
			"exp_card_base_amount": 1000,
			"food_card_base_amount": 200,
			"mine_card_base_amount": 100,
			"crystal_card_base_amount": 20,
			"diamond_card_base_amount": 10,
			"base_month_vip_car_exp": 10,
			"pro_month_vip_car_exp": 15,
			"permanent_month_vip_car_exp": 20,
			"card_cooling_time": {
				"base": 30,
				"pro": 90,
				"permanent": 36500
			},
			"card_increase_experience": {
				"base": 10,
				"pro": 15,
				"permanent": 20
			}
		}
	}
}
```



## get_config_player

获取player_config.json的配置文件 抽奖和转盘

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_player",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回角色配置信息和当前角色的经验钻石金币等信息，配置文件来自player_config.json

[成功]()

> player_config：返回player_config.json
>
> energy：能量的配置信息
>

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"player_config": {
			"player_level": {
				"max_level": 200,
				"experience": [
					0,
					60,
					120,
					180,
					240,
					360,
					480,
					600,
					720,
					840,
					1020,
					1260,
					1560,
					1920,
					2340,
					2820,
					3360,
					3960,
					4620,
					5340,
					6180,
					7140,
					8220,
					9420,
					10740,
					12180,
					13740,
					15420,
					17220,
					19140,
					21180,
					23340,
					25620,
					28020,
					30540,
					33180,
					35940,
					38820,
					41820,
					44940,
					48180,
					51540,
					55020,
					58620,
					62340,
					66180,
					70140,
					74220,
					78420,
					82740,
					87240,
					91920,
					96780,
					101820,
					107040,
					112440,
					118020,
					123780,
					129720,
					135840,
					142140,
					148620,
					155280,
					162120,
					169140,
					176340,
					183720,
					191280,
					199020,
					206940,
					215040,
					223320,
					231780,
					240420,
					249240,
					258240,
					267420,
					276780,
					286320,
					296040,
					306000,
					316200,
					326640,
					337320,
					348240,
					359400,
					370800,
					382440,
					394320,
					406440,
					418800,
					431400,
					444240,
					457320,
					470640,
					484200,
					498000,
					512040,
					526320,
					540840,
					555660,
					570780,
					586200,
					601920,
					617940,
					634260,
					650880,
					667800,
					685020,
					702540,
					720360,
					738480,
					756900,
					775620,
					794640,
					813960,
					833580,
					853500,
					873720,
					894240,
					915060,
					936180,
					957600,
					979320,
					1001340,
					1023660,
					1046280,
					1069200,
					1092420,
					1115940,
					1139820,
					1164060,
					1188660,
					1213620,
					1238940,
					1264620,
					1290660,
					1317060,
					1343820,
					1370940,
					1398420,
					1426260,
					1454460,
					1483020,
					1511940,
					1541220,
					1570860,
					1600860,
					1631220,
					1661940,
					1693020,
					1724460,
					1756260,
					1788420,
					1820940,
					1853820,
					1887060,
					1920660,
					1954620,
					1988940,
					2023680,
					2058840,
					2094420,
					2130420,
					2166840,
					2203680,
					2240940,
					2278620,
					2316720,
					2355240,
					2394180,
					2433540,
					2473320,
					2513520,
					2554140,
					2595180,
					2636640,
					2678520,
					2720820,
					2763540,
					2806740,
					2850420,
					2894580,
					2939220,
					2984340,
					3029940,
					3076020,
					3122580,
					3169620,
					3217140,
					3265140,
					3313620,
					3362580,
					3412020,
					3461940,
					3512340,
					3563220,
					3614580,
					3666420,
					3718740
				]
			}
		},
		"energy": {
			"time": 1200,
			"max_energy": 10
		}
	}
}
```



## get_config_factory

获取factory.json的配置文件信息

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_factory",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回工厂配置信息，配置文件来自factory.json

[成功]()

> get_factory_config：返回factory.json

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

## get_config_family

获取family.json的配置文件信息

##### 发送消息JSON格式

> 无

```json
{
	"world": 0, 
	"function": "get_config_family",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

返回工厂配置信息，配置文件来自factory.json

[成功]()

> config：配置信息
>
> - general：普通配置信息
>   - costs：消耗品
>   - rewards：签到奖励
>   - members：成员限制
> - store：商店配置信息
>   - items：商品信息（购买消耗等）
>   - gift：礼物信息
> - experience：家族等级信息
>   - max：最大等级
>   - exp：每级需要的总经验列表

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"config": {
			"general": {
				"costs": {
					"create": "3:5:2000",
					"change_name": "3:5:500"
				},
				"rewards": {
					"check_in": "3:1:100"
				},
				"members": {
					"base": 30,
					"max": 50,
					"inc": 2
				}
			},
			"store": {
				"items": {
					"3:6:1": "3:1:80"
				},
				"gift": [
					"3:5:10"
				]
			},
			"level": {
				"max": 10,
				"exp": [
					0,
					20,
					70,
					170,
					370,
					870,
					1870,
					3870,
					6870,
					10870,
					15870
				]
			}
		}
	}
}
```

## get_config_exchange

返回卡片兑换的配置信息，详见配置表`package.json`

##### 发送消息JSON格式

```json
{
	"world": 0, 
	"function": "get_config_exchange",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

[成功]()

> exchange_card：卡片兑换配置信息
>
> - sqltable：操作的数据库表
> - mid：物品id
> - bnum：卡片交换获得的物品基础数量（base num=>bnum）
>
> exchange_item：兑换其他物品配置信息

```
{
	"status": 0,
	"message": "success",
	"data": {
		"config": {
			"exchange_card": {
				"COIN_CARD": {
					"sqltable": "item",
					"mid": 1,
					"bnum": 2000
				},
				"EXP_CARD": {
					"sqltable": "progress",
					"mid": "exp",
					"bnum": 1000
				},
				"FOOD_CARD": {
					"sqltable": "item",
					"mid": 3,
					"bnum": 200
				},
				"MINE_CARD": {
					"sqltable": "item",
					"mid": 24,
					"bnum": 100
				},
				"CRYSTAL_CARD": {
					"sqltable": "item",
					"mid": 4,
					"bnum": 20
				},
				"DIAMOND_CARD": {
					"sqltable": "item",
					"mid": 5,
					"bnum": 10
				}
			},
			"exchange_item": {
				"energy_potion_s_min": 50,
				"energy_potion_s_max": 100,
				"role4_universal_segment": 30,
				"role5_universal_segment": 15,
				"weapon4_universal_segment": 20,
				"weapon5_universal_segment": 10,
				"universal4_segment": 30,
				"universal5_segment": 20,
				"universal6_segment": 10
			}
		}
	}
}
```

