## 方法列表

* [`get_achievement_reward`](##get_achievement_reward)
* [`get_all_achievement`](##get_all_achievement)

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

> item：物资的改变信息item_id：5表示钻石，remaining:表示剩余钻石数量，reward表示改变量
>
> achievement：任务的的详细信息，aid表示任务的id，value表示成就的完成次数为多少，reward代表奖励次数是多少，奖励的内容来自achievement_config.json

```json
{
	"status": 0,
	"message": "get reward success",
	"data": {
		"item": {
			"item_id": 5,
			"remaining": 242460,
			"reward": 30
		},
		"achievement": {
			"value": 1,
			"reward": 1,
			"aid": 1
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




