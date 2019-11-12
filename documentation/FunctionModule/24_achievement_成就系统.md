## 方法列表

* [`get_achievement_reward`](##get_achievement_reward)
* [`get_all_achievement`](##get_all_achievement)
* 内部方法[`record_achievement`](##record_achievement（内部方法）)

## get_achievement_reward

##### 发送消息JSON格式

获取此任务的奖励，完成任务获得的奖励表参考`task.json`，客户端需要告知服务器需要那个任务的奖励，task_id为任务的id,任务的id需要参考枚举

```json
{
	"world": 0, 
	"function": "get_achievement_reward",
	"data": {
		"token": "my toekn ^_^",
   		"achievement_id":1
	}
}
```

##### 接受消息JSON格式

[成功]()

> remaining：剩余的数量，item_id：5表示钻石，item_value表示钻石数量，aid表示任务的id，value表示成就的完成次数
>
> reward：变化量，item_id：5表示钻石，item_value表示钻石获得的数量，aid表示任务的id，value完成这个成就需要的次数，这个次数是已经达标并领取了奖励的次数

```json
{
	"status": 0,
	"message": "get reward success",
	"data": {
		"remaining": {
			"item_id": 5,
			"item_value": 241480,
			"aid": 1,
			"value": 999999
		},
		"reward": {
			"item_id": 5,
			"item_value": 310,
			"aid": 1,
			"value": 987
		}
	}
}
```

[失败]()

* 99: 这个成就没有奖励
* 98: 成就配置表有错





## get_all_achievement

##### 发送消息JSON格式

获取挂机奖励，`会`立即结算资源到玩家的物品栏

```json
{
	"world": 0, 
	"function": "get_all_achievement",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

[成功]()

> achievements：任务详情的数组，aid代表任务id，value代表是否完成，reward代表奖励
>

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"achievements": [
			{
				"aid": 1,
				"value": 1,
				"reward": 1
			},
			{
				"aid": 2,
				"value": 1,
				"reward": 0
			},
			{
				"aid": 3,
				"value": 1,
				"reward": 0
			}
		]
	}
}
```





## record_achievement（内部方法）

##### 发送消息JSON格式

内部使用记录每日任务的方法

> kwargs：传入需要的任务id和任务值，tid为任务id，可以从枚举中获得，task_value为任务值，0表示未完成，1表示完成
>
> record_task：uid为玩家的唯一id

```json
kwargs.update({"tid": enums.achievement.TOTAL_LOGIN, "task_value": 1})
record_achievement(uid,**kwargs)
```



