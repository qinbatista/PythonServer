## 方法列表

* [`get_task_reward`](##get_task_reward)
* [`get_all_task`](##get_all_task)
* 内部方法[`record_task`](##record_task)

## get_task_reward

##### 发送消息JSON格式

获取此任务的奖励，完成任务获得的奖励表参考`task.json`，客户端需要告知服务器需要那个任务的奖励，task_id为任务的id,任务的id需要参考枚举

```json
{
	"world": 0, 
	"function": "get_task_reward",
	"data": {
		"token": "my toekn ^_^",
    	"task_id":1
	}
}
```

##### 接受消息JSON格式

[成功]()

> reward：物资改变信息，5表示物品的item，value表示物品的数量，reward表示物品的改变量
>
> task：任务的id

```json
{
	"status": 0,
	"message": "get reward success",
	"data": {
		"reward": [
			{
				"5": {
					"value": 242430,
					"reward": 30
				}
			}
		],
		"task": 1
	}
}
```

[失败]()

* 99: no reward for this task
* 98: task id type error





## get_all_task

##### 发送消息JSON格式

获取挂机奖励，`会`立即结算资源到玩家的物品栏

```json
{
	"world": 0, 
	"function": "get_all_task",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

[成功]()

> tasks：任务详情的数组，tid代表任务id，task_value代表是否完成，reward代表奖励，timer代表完成时间
>

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"tasks": [
			{
				"tid": 1,
				"task_value": 1,
				"reward": 1,
				"timer": "2019-10-28 11:17:54"
			},
			{
				"tid": 2,
				"task_value": 1,
				"reward": 0,
				"timer": "2019-11-02 11:43:51"
			},
			{
				"tid": 3,
				"task_value": 1,
				"reward": 0,
				"timer": "2019-11-05 15:37:28"
			},
			{
				"tid": 5,
				"task_value": 1,
				"reward": 0,
				"timer": "2019-11-04 12:17:07"
			},
			{
				"tid": 6,
				"task_value": 1,
				"reward": 0,
				"timer": "2019-11-04 15:36:27"
			},
			{
				"tid": 9,
				"task_value": 1,
				"reward": 0,
				"timer": "2019-11-04 18:25:51"
			},
			{
				"tid": 10,
				"task_value": 1,
				"reward": 0,
				"timer": "2019-10-28 11:17:54"
			},
			{
				"tid": 11,
				"task_value": 1,
				"reward": 0,
				"timer": "2019-10-27 16:10:28"
			},
			{
				"tid": 12,
				"task_value": 1,
				"reward": 0,
				"timer": "2019-10-28 11:17:54"
			}
		]
	}
}
```



## record_task

##### 发送消息JSON格式

内部使用记录每日任务的方法

> **kwargs：传入需要的任务id和任务值，tid为任务id，可以从枚举中获得，task_value为任务值，0表示未完成，1表示完成
>
> record_task：uid为玩家的唯一id

```json
kwargs.update({"tid": enums.Task.CHECK_IN, "task_value": 1})
record_task(uid,**kwargs)
```



