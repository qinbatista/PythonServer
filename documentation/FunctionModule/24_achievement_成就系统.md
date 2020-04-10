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

> remain：剩余物资
>
> reward：变化物资
>
> achievement："aid:val:rwv"

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "remain": [
            "3:5:999110"
        ],
        "reward": [
            "3:5:30"
        ],
        "achievement": "1:1:1"
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



