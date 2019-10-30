## 方法列表

* [`create_family`](##create_family)
* [`leave_family`](##leave_family)
* [`remove_user_family`](##remove_user_family)
* [`invite_user_family`](##invite_user_family)
* [`request_join_family`](##request_join_family)
* [`respond_family`](##respond_family)
* [`get_all_family`](##get_all_family)
* [`get_store_family`](##get_store_family)
* [`market_purchase_family`](##market_purchase_family)
* [`set_notice_family`](##set_notice_family)
* [`set_blackboard_family`](##set_blackboard_family)
* [`set_role_family`](##set_role_family)
* [`change_name_family`](##change_name_family)
* [`disband_family`](##disband_family)
* [`cancel_disband_family`](##cancel_disband_family)

## create_family

Creates a new family with the given name.
The cost to create a family is determined by `family.json` configuration file.

##### 发送消息JSON格式

```json
{
	"world": 0, 
	"function": "start_hang_up",
	"data": {
		"token": "my token ^_^",
		"name": "family name" 
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
		"iid"  : 4,
		"value": 230
	}
}
```

[挂机关卡失败]()

* 99: invalid family name
* 98: already in a family
* 97: insufficient materials


## leave_family

Leave your current family.
The family owner can not leave.

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

```json
{
	"status": 0,
	"message": "left family",
	"data": {
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

```json
{
	"status": 0,
	"message": "removed user",
	"data": {
		"gn" : "matthew"
	}
}
```

[调整关卡失败]()

* 99: not in a family
* 98: target is not in your family
* 97: insufficient permissions


## invite_user_family

Invite a user to your family.
Only the Owner and Admins can invite users.
An invitation will be sent the the user's mailbox.

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
* 97: invitation could not be sent to mailbox

## request_join_family

Request to join a family.
The request will be sent to the family Owner and all Admins.
If any of them accept the invitation, user will be added to the family.

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

##### 发送消息JSON格式

[挂机关卡不同]()

> key: the key of the invitation or request mail

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
		"timer" : "2019-10-29 19:43:27"
	}
}
```

[调整关卡失败]()

* 99: not in a family


## get_store_family

Retrieves the items listed on the family store.

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
			{"item" : "3:5:10,  "cost" : "3:2:200"},
			{"item" : "3:1:100, "cost" : "3:4:20"},
		]
	}
}
```


## market_purchase_family

Purchase an item from the family store.

##### 发送消息JSON格式

> Example purchasing item 3:5:10 which costs 3:2:200

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



## set_notice_family

Update the family notice.
Only the family Owner and Admins may update the family notice.

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


## change_name_family

Change the name of the family.
Only Admins and above can change the family name.
The cost to change the family name is determined by `family.json` configuration file.

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
		"timer" : "2019-10-30 06:30:24"
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



