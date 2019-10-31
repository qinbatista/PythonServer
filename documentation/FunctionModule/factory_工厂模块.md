> ## 方法列表
>
> * [`refresh_factory`](##refresh_factory)
> * [`increase_worker_factory`](##increase_worker_factory)
> * [`buy_worker_factory`](##buy_worker_factory)
> * [`upgrade_factory`](##upgrade_factory)
> * [`decrease_worker_factory`](##decrease_worker_factory)
> * [`activate_wishing_pool_factory`](##activate_wishing_pool_factory)
> * [`get_config_factory`](##get_config_factory)
> * [`purchase_acceleration_factory`](##purchase_acceleration_factory)
> * [`set_armor_factory`](##set_armor_factory)
>
> ## activate_wishing_pool_factory
>
> ##### 发送消息JSON格式
>
> 玩家选择自己想要的武器后直接许愿即可获得，只获得碎片，`不会`获得武器
>
> ```json
> {
> 	"world": 0, 
> 	"function": "start_hang_up",
> 	"data": {
> 		"token": "my token ^_^",
> 		"wid": 1
> 	}
> }
> ```
>
> ##### 接受消息JSON格式
>
> [获得物品成功]()
>
> > remaining：获得武器的情况，`wid`武器id，`seg`碎片总数量，`diamond`钻石总数量
> >
> > reward：获得武器的情况，`wid`武器id，`seg`碎片变化量，`diamond`变化量
>
> ```json
> {
> 	"status": 0,
> 	"message": "success",
> 	"data": {
> 		"remaining":
> 		{
> 		"wid": 1,
> 		"seg": 19,
> 		"diamond": 994069
> 		},
> 		"reward":
> 		{
> 			"wid": 1,
> 			"seg": 2,
> 			"diamond": -90
> 		}
> 	}
> }
> ```
>
> [获得失败]()
>
> * 99: 关卡参数错误
>
> 
>
> 
>
> ## purchase_acceleration_factory
>
> ##### 发送消息JSON格式
>
> 玩家选择自己想要的武器后直接许愿即可获得，只获得碎片，不会获得武器
>
> ```json
> {
> 	"world": 0, 
> 	"function": "start_hang_up",
> 	"data": {
> 		"token": "my token ^_^",
> 	}
> }
> ```
>
> ##### 接受消息JSON格式
>
> [获得物品成功]()
>
> > remaining：获得武器的情况，`diamond`钻石总数量
> >
> > reward：获得武器的情况，`diamond`变化量
> >
> > time: 剩余时间倒计时
>
> ```json
> {
> 	"status": 0,
> 	"message": "success",
> 	"data": {
> 		"remaining":
> 		{
> 			"diamond": 993539
> 		},
> 		"reward":
> 		{
> 			"diamond": -70
> 		},
> 		"time":"23:43:21"
> 	}
> }
> ```
>
> [获得失败]()
>
> * 99: 关卡参数错误
>
> 
>
> ## refresh_factory
>
> ##### 发送消息JSON格式
>
> 玩家选择自己想要的武器后直接许愿即可获得，只获得碎片，不会获得武器
>
> ```json
> {
> 	"world": 0, 
> 	"function": "start_hang_up",
> 	"data": {
> 		"token": "my token ^_^",
> 	}
> }
> ```
>
> ##### 接受消息JSON格式
>
> 刷新工厂会刷新已经获得的资源，并给到客户端所有资源的增长量和存储量，也会更新许愿池的时间，如果许愿池
>
> [获得物品成功]()
>
> > resource：各个资源详细参数，0，1，2分别代表食品，铁，水晶工厂，`remaining`代表当前剩余，`reward`表示变化量
> >
> > armor：盔甲的获得情况，每次刷新工厂会直接把盔甲给到用户的背包`remaining`代表当前剩余，`reward`表示变化量
> >
> > pool: 许愿池的倒计时
> >
> > worker: 工人的现有情况，`unassigned`空闲工人,`total`工人总数，`factory`工厂的工人情况
>
> ```json
> {
> 	"status": 0,
> 	"message": "success",
> 	"data": 
>   	"resource":{
>   						"remaining":{
>                         "0": 555,
>                         "1": 0,
>                         "2": 0
> 											},
> 							"reward":{
>                 				"0": 555,
>                         "1": 0,
>                         "2": 0
>              				}
>             	},
> 		"armor":
> 						{
>               	"remaining":{
>                         "aid": 555,
>                         "quantity": 0
> 											},
> 								"reward":{
>                 				 "aid": 555,
>                         "quantity": 0
>              				}
>             },
> 		"pool":
> 				{
>           "time":"24:11:23"
>         }
> 		"worker":
> 					{
>             "unassigned": 5,
> 						"total": 7,
>             "facotry":
>             {
>               "worker"
>               {
>                 "0":5,
>                 "1":5,
>                 "2":5,
>                 "3":5
>             	},
>             	"level":
>             	{
>                 "0":1,
>                 "1":1,
>                 "2":1,
>                 "3":1
>               }
>             }
>           }
> 	}
> }
> ```
>
> [获得失败]()
>
> * 99: 关卡参数错误
>
> 
>
> ## increase_worker_factory
>
> ##### 发送消息JSON格式
>
> 选择需要添加的工厂添加工人，添加工人之后需要结算当前的资源，以免算法出错
>
> > fid: 工厂id
> >
> > num：需要添加工人的数量
>
> ```json
> {
> 	"world": 0, 
> 	"function": "start_hang_up",
> 	"data": {
> 		"token": "my token ^_^",
>     "fid": 0,
>     "num": 1,
> 	}
> }
> ```
>
> ##### 接受消息JSON格式
>
> 刷新工厂会刷新已经获得的资源，并给到客户端所有资源的增长量和存储量，也会更新许愿池的时间，如果许愿池
>
> [获得物品成功]()
>
> > worker：工人的变化情况，`fid`工厂id，`unassigned`剩余工人，`workers`工厂拥有的工人
> >
> > refresh：所有和工人相关的工厂其资源的结算情况
>
> ```json
> {
> 	"status": 0,
> 	"message": "success",
> 	"data": {
> 		"worker": {
> 			"fid": 0,
> 			"unassigned": 3,
> 			"workers": 2
> 		},
> 		"refresh": {
> 			"resource": {
> 				"remaining": {
> 					"0": 555,
> 					"1": 0,
> 					"2": 0
> 				},
> 				"reward": {
> 					"0": 555,
> 					"1": 0,
> 					"2": 0
> 				}
> 			},
> 			"armor": {
> 				"remaining": {
> 					"aid": 555,
> 					"quantity": 0
> 				},
> 				"reward": {
> 					"aid": 555,
> 					"quantity": 0
> 				}
> 			}
> 		}
> 	}
> }
> ```
>
> [获得失败]()
>
> * 99: 关卡参数错误
>
> 
>
> ## decrease_worker_factory
>
> ##### 发送消息JSON格式
>
> 选择需要添加的工厂添加工人，添加工人之后需要结算当前的资源，以免算法出错
>
> > fid: 工厂id
> >
> > num：需要添加工人的数量
>
> ```json
> {
> 	"world": 0, 
> 	"function": "start_hang_up",
> 	"data": {
> 		"token": "my token ^_^",
>     "fid": 0,
>     "num": 1,
> 	}
> }
> ```
>
> ##### 接受消息JSON格式
>
> 刷新工厂会刷新已经获得的资源，并给到客户端所有资源的增长量和存储量，也会更新许愿池的时间，如果许愿池
>
> [获得物品成功]()
>
> > worker：工人的变化情况，`fid`工厂id，`unassigned`剩余工人，`workers`工厂拥有的工人
> >
> > refresh：所有和工人相关的工厂其资源的结算情况
>
> ```json
> {
> 	"status": 0,
> 	"message": "success",
> 	"data": {
> 		"worker": {
> 			"fid": 0,
> 			"unassigned": 3,
> 			"workers": 2
> 		},
> 		"refresh": {
> 			"resource": {
> 				"remaining": {
> 					"0": 555,
> 					"1": 0,
> 					"2": 0
> 				},
> 				"reward": {
> 					"0": 555,
> 					"1": 0,
> 					"2": 0
> 				}
> 			},
> 			"armor": {
> 				"remaining": {
> 					"aid": 555,
> 					"quantity": 0
> 				},
> 				"reward": {
> 					"aid": 555,
> 					"quantity": 0
> 				}
> 			}
> 		}
> 	}
> }
> ```
>
> [获得失败]()
>
> * 99: 关卡参数错误
>
> 
>
> ## buy_worker_factory
>
> ##### 发送消息JSON格式
>
> 选择需要添加的工厂添加工人，添加工人之后需要结算当前的资源，以免算法出错，目前工人只能一个一个买
>
> > fid: 工厂id
> >
> > num：需要添加工人的数量
>
> ```json
> {
> 	"world": 0, 
> 	"function": "start_hang_up",
> 	"data": {
> 		"token": "my token ^_^"
> 	}
> }
> ```
>
> ##### 接受消息JSON格式
>
> 刷新工厂会刷新已经获得的资源，并给到客户端所有资源的增长量和存储量，也会更新许愿池的时间，如果许愿池
>
> [获得物品成功]()
>
> > worker：工人的变化情况，`fid`工厂id，`unassigned`剩余工人，`workers`工厂拥有的工人
> >
> > refresh：所有和工人相关的工厂其资源的结算情况
>
> ```json
> {
> 	"status": 0,
> 	"message": "success",
> 	"data": {
> 		"worker": {
> 			"unassigned": 5,
> 			"total": 7,
> 			"food": {
> 				"remaining": 22333,
> 				"reward": 2300
> 			}
> 		}
> 	}
> }
> ```
>
> [获得失败]()
>
> * 99: 关卡参数错误
>
> 
>
> ## upgrade_factory
>
> ##### 发送消息JSON格式
>
> 升级工厂，提高存储上限，提高工人上限
>
> > fid: 工厂id
>
> ```json
> {
> 	"world": 0, 
> 	"function": "start_hang_up",
> 	"data": {
> 		"token": "my token ^_^",
>     "fid":1
> 	}
> }
> ```
>
> ##### 接受消息JSON格式
>
> 刷新工厂会刷新已经获得的资源，并给到客户端所有资源的增长量和存储量，也会更新许愿池的时间，如果许愿池
>
> [获得物品成功]()
>
> > worker：工人的变化情况，`fid`工厂id，`unassigned`剩余工人，`workers`工厂拥有的工人
> >
> > refresh：所有和工人相关的工厂其资源的结算情况
>
> ```json
> {
> 	"status": 0,
> 	"message": "success",
> 	"data": {
> 		"factory": 0,
> 		"level": 5
> 	}
> }
> ```
>
> [获得失败]()
>
> * 99: 关卡参数错误
>
> 
>
> ## get_config_factory
>
> ##### 发送消息JSON格式
>
> 获取关卡的配置文件，配置文件来自`factory.json`
>
> ```json
> {
> 	"world": 0, 
> 	"function": "start_hang_up",
> 	"data": {
> 		"token": "my token ^_^"
> 	}
> }
> ```
>
> ##### 接受消息JSON格式
>
> 直接下载配置资源到本地，涉及到所有的参数情况
>
> [获取成功]()
>
> ```json
> {
> 	"status": 0,
> 	"message": "success",
> 	"data": {
> 		......
> 	}
> }
> ```
>
> [获得失败]()
>
> * 99: 关卡参数错误
>
> 
>
> ## set_armor_factory
>
> ##### 发送消息JSON格式
>
> 获取关卡的配置文件，配置文件来自`factory.json`
>
> ```json
> {
> 	"world": 0, 
> 	"function": "start_hang_up",
> 	"data": {
> 		"token": "my token ^_^",
>     "aid":1
> 	}
> }
> ```
>
> ##### 接受消息JSON格式
>
> 直接下载配置资源到本地，涉及到所有的参数情况
>
> [获取成功]()
>
> ```json
> {
> 	"status": 0,
> 	"message": "success",
> 	"data": {
> 		"old": {
> 			"remaining": {
> 				"aid": 555,
> 				"quantity": 0
> 			},
> 			"reward": {
> 				"aid": 555,
> 				"quantity": 0
> 			}
> 		},
> 		"now": {
> 			"remaining": {
> 				"aid": 555,
> 				"quantity": 0
> 			},
> 			"reward": {
> 				"aid": 555,
> 				"quantity": 0
> 			}
> 		}
> 	}
> }
> ```
>
> [获得失败]()
>
> * 99: 关卡参数错误
