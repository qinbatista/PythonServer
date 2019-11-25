## 方法列表

* √[`create_family`](##create_family)
* √[`leave_family`](##leave_family)
* √[`remove_user_family`](##remove_user_family)
* √[`invite_user_family`](##invite_user_family)
* *[`invite_link_family`](##invite_link_family)
* [`request_join_family`](##request_join_family)
* [`respond_family`](##respond_family)
* [`get_all_family`](##get_all_family)
* [`get_store_family`](##get_store_family)
* [`market_purchase_family`](##market_purchase_family)
* *[`welfare_purchase_family`](##welfare_purchase_family)
* [`set_notice_family`](##set_notice_family)
* [`set_blackboard_family`](##set_blackboard_family)
* [`set_role_family`](##set_role_family)
* [`change_name_family`](##change_name_family)
* [`disband_family`](##disband_family)
* [`cancel_disband_family`](##cancel_disband_family)
* *[`family_check_in`](##family_check_in)
* *[`abdicate_family`](##abdicate_family)
* *[`modify_icon_family`](##modify_icon_family)



## create_family

Creates a new family with the given name.
The cost to create a family is determined by `family.json` configuration file.

用给定的名称创建一个新的家庭。
创建一个家庭的成本由' `family.json`'配置文件决定, 创建公会需要传入`图标`与`工会名字`，创建公会必须满足`1: 玩家大于18级`，`2:有2000钻石`

##### 发送消息JSON格式

```json
{
	"world": 0, 
	"function": "start_hang_up",
	"data": {
		"token": "my token ^_^",
		"name": "family name",
    	"icon": 1
	}
}
```

##### 接受消息JSON格式


```json

{
	"status": 0,
	"message": "created family",
	"data": {
		"name" : "family name",
        "icon" : "icon",
        "remaining":{
            "iid"  : 4,
            "value": 230
        },
        "reward":{
            "iid"  : 4,
            "value": 230
        },
	}
}
```

[挂机关卡失败]()

* 99: invalid family name
* 98: already in a family
* 97: insufficient materials
* 96: name already exists!
* 95: 玩家等级未满开启等级




## leave_family

Leave your current family.
The family owner can not leave.

离开你现在的家庭。
这家族族长不能离开。

玩家退出工会之后24小时才能再次加入工会

玩家离开工会累计贡献清0，贡献数值保留，可以在其他工会兑换。

##### 发送消息JSON格式

```json
{
	"world": 0,
	"function": "leave_family",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

> cd_time：玩家离开家族后的冷却时间，冷却时间结束才能再次加入其他家族

```json
{
	"status": 0,
	"message": "left family",
	"data": {
        "cd_time": 2313
	}
}
```

[调整关卡失败]()

* 99: not in a family
* 98: family owner can not leave




## remove_user_family

Remove a user from the family.
The owner can remove anyone.
Admins can remove anyone with a role lower than Admin.

将用户从家庭中移除。

所有者可以移除任何人。

管理员可以删除任何角色低于管理员的人。

一天之内移除5个成员

##### 发送消息JSON格式

```json
{
	"world": 0,
	"function": "remove_user_family",
	"data": {
		"token": "my token",
		"gn_target" : "matthew"
	}
}
```

##### 接受消息JSON格式

> gn：移除的成员游戏名
>
> rmtimes：剩余可移除成员的次数
>
> cd_time：剩余恢复移除次数的冷却时间

```json
{
	"status": 0,
	"message": "removed user",
	"data": {
		"gn" : "matthew",
        "rmtimes": 4,
        "cd_time": 68900
	}
}
```

[调整关卡失败]()

* 99: not in a family
* 98: target is not in your family
* 97: insufficient permissions
* 96: You can't remove yourself
* 95: target doesn't have a family(对方没有家族)
* 94: 今天移除成员的次数已用完  cd_time: 剩余恢复移除次数的冷却时间




## invite_user_family

Invite a user to your family.
Only the Owner and Admins can invite users.
An invitation will be sent the the user's mailbox.

邀请一个用户到你的家庭。

只有所有者和管理员可以邀请用户。

一个邀请将被发送到用户的邮箱。

##### 发送消息JSON格式

```json
{
	"world": 0,
	"function": "invite_user_family",
	"data": {
		"token": "my token",
		"gn_target" : "matthew"
	}
}
```

##### 接受消息JSON格式


```json
{
	"status": 0,
	"message": "invitation sent",
	"data": {
		"gn" : "matthew"
	}
}
```

[挂机关卡失败]()

* 99: not in a family
* 98: insufficient permissions
* 97: mail could not be sent



##  invite_link_family

> 发送世界入会邀请，长cd。
>
> 向聊天窗发送入会邀请链接
>
> 会长和官员有这个权限

##### 发送消息JSON格式

> 

```json
{
	"world": 0,
	"function": "invite_link_family",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

> data包含家族信息

```json
{
	"status": 0,
	"message": "success",
	"data": {
	}
}
```



## request_join_family

Request to join a family.
The request will be sent to the family Owner and all Admins.
If any of them accept the invitation, user will be added to the family.

请求加入一个家庭。

请求将被发送到家庭所有者和所有管理员。

如果他们中的任何一个接受邀请，用户将被添加到家庭。

##### 发送消息JSON格式


```json
{
	"world": 0,
	"function": "request_join_family",
	"data": {
		"token": "my token",
		"name" : "family name"
	}
}
```

##### 接受消息JSON格式


```json
{
	"status": 0,
	"message": "request sent",
	"data": {
		"name" : "family name"
	}
}
```

[调整关卡失败]()

* 99: already in a family
* 98: invalid family
* 97: request could not be sent to mailbox



## respond_family

Respond to a family request or invitation.
Calling this function adds the user to the family.

回应家人的请求或邀请。
调用此函数将用户添加到家庭中。

##### 发送消息JSON格式

[挂机关卡不同]()

> key: the key of the invitation or request mail（ 邀请或请求邮件的密钥 ）

```json
{
	"world": 0,
	"function": "request_join_family",
	"data": {
		"token": "my token",
		"key" : "mail key"
	}
}
```

##### 接受消息JSON格式


```json
{
	"status": 0,
	"message": "success",
	"data": {
		"name"  : "family name",
		"icon"  : 0,
		"exp"   : 1337,
		"notice": "New members should buy family gift package",
		"board" : "Blackboard"
	}
}
```

[调整关卡失败]()

* 99: invalid nonce
* 98: target user is already in family
* 97: family no longer exists
* 96: family is full




## get_all_family

Gets all information regarding your family.

获取有关您家庭的所有信息。 

返回家族经验、等级、升下级需要多少经验

需要显示玩家的职务；最后登录的时间：在线显示在线，超过1天按天计，不超过1天按小时记；显示玩家累计贡献。

##### 发送消息JSON格式

```json
{
	"world": 0,
	"function": "get_all_family",
	"data": {
		"token": "my token",
	}
}
```

##### 接受消息JSON格式

> name: 家族名字
>
> icon:  家族icon
>
> exp: 家族经验值
>
> notice: 家族公告
>
> board：家族简介
>
> members：家族成员，`gn`家族名字，`role`使用角色(0，4，8，10)，`exp`经验值，`icon`使用icon
>
> news: 家族消息，主要是谁离开，谁加入等信息
>
> timer：家族正式解散的时间


```json
{
	"status": 0,
	"message": "success",
	"data": {
		"name"  : "family name",
		"icon"  : 0,
		"exp"   : 1337,
		"notice": "New members should buy family gift package",
		"board" : "Blackboard",
		"members" : [
			{"gn" : "matthew",  "role" : 10, "exp" : 420, "icon" : 0},
			{"gn" : "children", "role" :  8, "exp" : 240, "icon" : 1}
		],
		"news" : [
			["2019-10-30 06:30:24", "matthew added children."],
			["2019-10-31 07:24:31", "children purchased gift."]
		],
		"timer" : 85647
	}
}
```

[调整关卡失败]()

* 99: not in a family




## get_store_family

Retrieves the items listed on the family store, configuration depends on `family.json`

检索家庭存储中列出的项，配置取决于 `family.json`

##### 发送消息JSON格式

```json
{
	"world": 0,
	"function": "get_store_family",
	"data": {
		"token": "my token",
	}
}
```

##### 接受消息JSON格式


```json
{
	"status": 0,
	"message": "success",
	"data": {
		"merchandise" : [
			{"item" : "3:5:10",  "cost" : "3:2:200"},
			{"item" : "3:1:100", "cost" : "3:4:20"},
		]
	}
}
```



## market_purchase_family

 welfare_purchase_family

Purchase an item from the family store.

 从家庭商店购买一件物品。 

> 工会贡献可以在工会商店兑换资源
>
> 

##### 发送消息JSON格式

> Example purchasing item 3:5:10 which costs 3:2:200
>
>  购买项目3:5:10花费3:2:200 

```json
{
	"world": 0,
	"function": "market_purchase_family",
	"data": {
		"token": "my token",
		"item" : "3:5:10"
	}
}
```

##### 接受消息JSON格式

> The outer dictionary key is equal to enums.Group.ITEM.value
>
> Before purchase, user has 3:5:100 and 3:2:1000
>
> 外部字典键等于enums.Group.ITEM.value
> 购买前，用户有3:5:100和3:2:1000

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"3" : [
			{"iid" : 5, "value" : 110},
			{"iid" : 2, "value" : 800}
		]
	}
}
```


[调整关卡失败]()

* 99: not in a family
* 98: invalid item
* 97: insufficient funds



##  welfare_purchase_family

> 工会福利
>
> 有大佬玩家购买后，全工会人员都可以获得少量奖励，只有两种，一种是钻石购买，一种是RMB购买。每人每种每天限购1次。
>
> 钻石购买的可以获取金币和工会贡献，其他玩家可以领取少量钻石和工会贡献。
>
> RMB购买的可以获取金币和钻石和工会贡献。

##### 发送消息JSON格式

> Example purchasing item 3:5:10 which costs 3:2:200
>
> 购买项目3:5:10花费3:2:200 

```json
{
	"world": 0,
	"function": "welfare_purchase_family",
	"data": {
		"token": "my token",
		"item" : "3:5:10"
	}
}
```

##### 接受消息JSON格式

> The outer dictionary key is equal to enums.Group.ITEM.value
>
> Before purchase, user has 3:5:100 and 3:2:1000
>
> 外部字典键等于enums.Group.ITEM.value
> 购买前，用户有3:5:100和3:2:1000

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"3" : [
			{"iid" : 5, "value" : 110},
			{"iid" : 2, "value" : 800}
		]
	}
}
```



## set_notice_family

Update the family notice.
Only the family Owner and Admins may update the family notice.

更新家庭通知。
只有家庭所有者和管理员可以更新家庭通知。

需要有cd

##### 发送消息JSON格式


```json
{
	"world": 0,
	"function": "set_notice_family",
	"data": {
		"token": "my token",
		"msg"  : "This is my updated notice"
	}
}
```

##### 接受消息JSON格式


```json
{
	"status": 0,
	"message": "success",
	"data": {
		"notice" : "This is my updated notice"
	}
}
```


[调整关卡失败]()

* 99: not in a family
* 98: insufficient permissions



## set_blackboard_family

Update the family blackboard.
Only the family Owner and Admins may update the family blackboard.

更新家庭黑板。
只有家庭所有者和管理员可以更新家庭黑板。

##### 发送消息JSON格式


```json
{
	"world": 0,
	"function": "set_blackboard_family",
	"data": {
		"token": "my token",
		"msg"  : "This is my updated blackboard"
	}
}
```

##### 接受消息JSON格式


```json
{
	"status": 0,
	"message": "success",
	"data": {
		"board" : "This is my updated blackboard"
	}
}
```


[调整关卡失败]()

* 99: not in a family
* 98: insufficient permissions



## set_role_family

Modify the family role of the target user.
The family Owner can set the permissions of any users to any role that is not Owner to Admin or below.
The family Admins can set the permissions of any users whose role is Elite or lower to Elite or below.

修改目标用户的家庭角色。
家族所有者可以将任何用户的权限设置为不属于所有者的任何角色，并将其设置为Admin或以下。

家庭管理员可以将任何角色为精英或更低的用户的权限设置为精英或更低。

role级别只包括0，4，8，10

##### 发送消息JSON格式


```json
{
	"world": 0,
	"function": "set_role_family",
	"data": {
		"token": "my token",
		"gn_target"  : "children",
		"role" : 8
	}
}
```

##### 接受消息JSON格式


```json
{
	"status": 0,
	"message": "success",
	"data": {
		"gn" : "children",
		"role" : 8
	}
}
```

[调整关卡失败]()

* 99: can not modify self permissions
* 98: not in a family
* 97: target is not in your family
* 96: insufficient permissions
* 95: role  type error (级别类型错误)



## change_name_family

Change the name of the family.
Only Admins and above can change the family name.
The cost to change the family name is determined by `family.json` configuration file.

更改家庭名称。

只有管理员及以上的人才可以更改姓氏。

更改家族名字的成本由`family.json`配置文件决定。

##### 发送消息JSON格式


```json
{
	"world": 0,
	"function": "change_name_family",
	"data": {
		"token": "my token",
		"name" : "new family name"
	}
}
```

##### 接受消息JSON格式


```json
{
	"status": 0,
	"message": "success",
	"data": {
		"name" : "new family name",
		"iid"  : 5,
		"value": 2350
	}
}
```

[调整关卡失败]()

* 99: invalid family name
* 98: not in a family
* 97: insufficient permissions
* 96: insufficient funds



## disband_family

Starts the timer to disband the family.
Only Admins and above can initialize the disbanding of a family.

开始计时解散家庭。
只有管理员及以上才能初始化家族的解散。

##### 发送消息JSON格式


```json
{
	"world": 0,
	"function": "disband_family",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式


```json
{
	"status": 0,
	"message": "success",
	"data": {
		"timer" : 86400
	}
}
```

[调整关卡失败]()

* 99: not in a family
* 98: insufficient permissions
* 97: family already disbanded



## cancel_disband_family

Cancels the timer to disband the family.
Only Admins and above can cancel the disbanding of a family.

取消定时器来解散家庭。
只有管理员以上的人才可以取消一个家庭的解散。

取消后3天内不能解散

##### 发送消息JSON格式


```json
{
	"world": 0,
	"function": "cancel_disband_family",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式


```json
{
	"status": 0,
	"message": "success",
	"data": {
	}
}
```

[调整关卡失败]()

* 99: not in a family
* 98: insufficient permissions
* 97: family is not disbanded



## family_check_in

家族签到，一人签到一次加一点经验家族经验，经验表对照family.json, 公会等级，签到获取贡献值和金币奖励，工会等级的提高，奖励也会随着提高

##### 发送消息JSON格式


```json
{
	"world": 0,
	"function": "cancel_disband_family",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式


```json
{
	"status": 0,
	"message": "success",
	"data": {
	}
}
```

[调整关卡失败]()

* 99: not in a family
* 98: insufficient permissions
* 97: family is not disbanded



## abdicate_family

> 会长让位
>
> 会长转让会长位置给其他成员

##### 发送消息JSON格式

> 

```json
{
	"world": 0,
	"function": "abdicate_family",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

> 

```json
{
	"status": 0,
	"message": "success",
	"data": {
	}
}
```



##  modify_icon_family

> 族长和管理员才能修改工会图标

##### 发送消息JSON格式

> 

```json
{
	"world": 0,
	"function": "modify_icon_family",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

> 

```json
{
	"status": 0,
	"message": "success",
	"data": {
	}
}
```


