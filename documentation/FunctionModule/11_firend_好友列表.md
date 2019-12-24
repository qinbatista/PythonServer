## 方法列表

* [`get_all_friend`](##get_all_friend)
* [`request_friend`](##request_friend)
* [`remove_friend`](##remove_friend)
* [`send_gift_friend`](##send_gift_friend)
* [`send_gift_all`](##send_gift_all)
* [`find_person`](##find_person)

## get_all_friend

##### 发送消息JSON格式

> 获取所有朋友的信息

```json
{
	"world": 0,
	"function": "get_all_friend",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[成功]()

> friends：返回玩家的个人信息，返回方式为列表形式，每一个索引代表每一个朋友，其中`gn`表示玩家个名字，`exp`表示经验值（需要客户端自行计算等级），`recover`表示发送爱心的时间，`since`表示成为好朋友的日期，`fid`表示朋友的家族id，`intro`表示玩家的个人签名， `icon`头像id

```json
{
	"status": 0,
	"message": "got all friends",
	"data": {
		"friends": [
			{
				"gn": "妻雾脓翟纽屉",
				"exp": 0,
				"recover": "2019-11-03",
				"since": "2019-10-28",
				"fid": "",
				"intro": "",
				"icon": 0
			},
			{
				"gn": "222",
				"exp": 200,
				"recover": "2019-11-03",
				"since": "2019-10-28",
				"fid": "",
				"intro": "",
				"icon": 0
			}
		]
	}
}
```

[失败]()

* 没有朋友会返回空列表

## request_friend

##### 发送消息JSON格式

向某一个陌生人发送邮件要求，发送之后，对方玩家会收到一封邮件，每日可以发送好友申请的上限为6此，添加好友后会立即单方加好友，如果对方没同意，则会一直保持单方加好友

> gn_target：需要添加的玩家名字

```json
{
	"world": 0, 
	"function": "request_friend",
	"data": {
		"token": "my toekn ^_^",
    	"gn_target": "后起之秀"
	}
}
```

##### 接受消息JSON格式

[成功]()

> gn：发送成功则会返回玩家的名字，并且在自己好友栏会显示此好友，除了无法发送消息，其余均正常
>

```json
{
	"status": 0,
	"message": "request sent",
	"data": {
		"gn": "后起之秀"
	}
}
```

[失败]()

* 99: 自己给自己发邮件
* 98: 邮箱有问题 (internal mail error)
* 97: 没有此人
* 96: 一天只能申请6个人
* 95: 已经成为朋友或已经申请过这个人为朋友
* 94: target's mailbox is full



## remove_friend

##### 发送消息JSON格式

删除好友列表中的朋友

> gn_target：需要删除朋友的名字，删除朋友只会执行删除操作，如果没有朋友也不会有所不同

```json
{
	"world": 0, 
	"function": "remove_friend",
	"data": {
		"token": "my toekn ^_^",
    	"gn_target": "后起之秀"
	}
}
```

##### 接受消息JSON格式

[成功]()

> gn：玩家的名字
>

```json
{
	"status": 0,
	"message": "removed target",
	"data": {
		"gn": "后起之秀"
	}
}
```

[失败]()

* 99: 不能自己删除自己



## send_gift_friend

##### 发送消息JSON格式

升级被动，武器等级与技能点总数保持一致

> gn_target：朋友名字

```json
{
	"world": 0, 
	"function": "send_gift_friend",
	"data": {
		"token": "my toekn ^_^",
    	"gn_target":"后起之秀"
	}
}
```

##### 接受消息JSON格式

[升级成功]()

> data：没有任何返回消息
>

```json
{
	"status": 0,
	"message": "success",
	"data": {}
}
```

[抽取失败]()

* 99: 不是朋友
* 98: 礼物冷却中
* 97: 邮箱错误 (internal mailbox error)
* 96: target's mailbox full



## send_gift_all

##### 发送消息JSON格式

向所有好友发送爱心，不会发给单方面加好友的玩家

```json
{
	"world": 0, 
	"function": "send_gift_all",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

[成功]()

> data：返回玩家好友添加成功的列表，如果
>

```json
{
	"status": 0,
	"message": "you send all friend gift success",
	"data": [
		"哈哈",
		"我v"
	]
}
```

[失败]()

* 99: 没有朋友可以发送，一个朋友也没有



## find_person

##### 发送消息JSON格式

查找特定玩家的信息

> gn_target : 查找指定玩家的名字

```json
{
	"world": 0, 
	"function": "find_person",
	"data": {
		"token": "my toekn ^_^",
    	"gn_target": 1,
	}
}
```

##### 接受消息JSON格式

[抽取成功]()

> data：包含玩家的所有信息，`gn`游戏名字，`intro`玩家个人签名，`fid`家庭id，`exp`玩家经验，`stage`通过的最大关卡，`role`玩家使用的角色，`isfriend`是否是朋友, `canfamily`是否能邀请进入家族
>

```json
{
	"status": 0,
	"message": "find person success",
	"data": {
		"gn": "后起之秀",
		"intro": "",
		"fid": "",
		"exp": 40,
		"stage": 0,
		"role": 1,
		"isfriend": "True",
		"canfamily": "False"
	}
}
```

[抽取失败]()

* 99: 没有此人
* 98: 不能添加自己

