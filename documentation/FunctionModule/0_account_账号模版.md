## 方法列表

* [`get_account_world_info`](##get_account_world_info)
* [`enter_world`](##enter_world)
* [`create_player`](##create_player)
* [`login_unique`](##login_unique)
* [`login`](##login)
* [`bind_account`](##bind_account)
* [`bind_email`](##bind_email)
* [`create_account`](##create_account)
* [`verify_email`](##verify_email)



## get_account_world_info

##### 接受消息JSON格式

获取玩家可以登陆的世界和每个世界的个人信息

```json
{
	"world": 0, 
	"function": "get_account_world_info",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

[世界获取成功]()

> worlds：每个世界的个人信息，`server_status`表示服务器状态，目前均为0, 未来繁忙程度会按照0,1,2,3依次表示服务器的繁忙程度. `world`为世界序号，`world_name`为世界的名字，`gn`游戏的名字，`exp`为玩家的经验
>

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"worlds": [
			{
				"server_status": 0,
				"world": "1",
				"world_name": "experimental_test1",
				"gn": "",
				"exp": ""
			},
			{
				"server_status": 0,
				"world": "2",
				"world_name": "experimental_test2",
				"gn": "",
				"exp": ""
			},
			{
				"server_status": 0,
				"world": "0",
				"world_name": "experimental",
				"gn": "",
				"exp": ""
			}
		]
	}
}
```

[世界获取失败]()

* 99: 关卡获取失败



## login_unique

游客登陆，直接用机器的唯一标识符登陆设备

> unique_id：玩家的唯一id，目前使用unity获取唯一标识符的方法获取唯一标识符

```json
{
	"world": 0,
	"function": "get_hang_up_reward",
	"data": {
		"unique_id": "my unique_id"
	}
}
```

##### 接受消息JSON格式

[获取资源成功]()

> token：通关发送的unique_id获得自己的token

* 0: 获得token成功
* 1: 新账号创建成功，也返回了token

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"token": "my token"
	}
}
```

[调整关卡失败]()

* 2: 账号已经被绑定，请用账户登陆



## create_player

创建玩家角色，玩家角色限制在10个字符串以内，不允许出现符号

> gn：输入游戏的名字

```json
{
	"world": 0,
	"function": "create_player",
	"data": {
		"token": "my token",
		"gn":"game name",
	}
}
```

##### 接受消息JSON格式

[获取资源成功]()

> gn：游戏的名字
>

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"gn": "name_q2"
	}
}
```

[调整关卡失败]()

* 99: 玩家uid或名字已存在
* 98: 玩家uid或者名字为空



## enter_world

玩家进入特定的世界，这个世界会返回是否允许该玩家进入世界，这个世界如果繁忙，或者世界不存在，玩家则需要重新选择世界，进入世界成功则会给予玩家进入世界成功的提示并开始加载参数

> stage：需要进入的关卡

```json
{
	"world": 0,
	"function": "enter_stage",
  "world": 1,
	"data": {
		"token": "my token",

	}
}
```

##### 接受消息JSON格式

[进入关卡成功]()

```json
{
	"status": 0,
	"message": "success",
	"data": {}
}
```

[挂机关卡失败]()

* 98: 此世界没有没有创建角色，需要创建好角色后再进入世界



## login

玩家使用账户和密码登陆账户

> identifier：表示用什么方式登陆，其值可以为`email`，`account`，`phone_number`
>
> identifier：identifier的值，如果是email则表示必须输入aaaa@email.com格式才能登陆
>
> password：用户的密码

```json
{
	"world": 0,
	"function": "enter_stage",
	"data": {
		"token": "my token",
		'identifier':"email", 
    "value":"account", 
    "password":"123456"
	}
}
```

##### 接受消息JSON格式

[进入关卡成功]()

> token：成功获取的token需要本地保存，方便下次直接登陆
>
> account: 账户id，只会在用此选择登陆才会返回值
>
> email：账户id，只会在用此选择登陆才会返回值
>
> phone_number：账户id，只会在用此选择登陆才会返回值

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"token": "my token",
		"account": "q1account",
		"email": "",
		"phone_number": ""
	}
}
```

[调整关卡失败]()

* 99: 关卡数量不对





## bind_account

此方法只有在玩家用游客登陆的时候才能使用，游客登陆玩家在设置里或者提示界面里使用此方法

> account：绑定用户的账号
>
> password：用户的密码

```json
{
	"world": 0,
	"function": "enter_stage",
	"data": {
		"token": "my token",
    "account":"account",
		'password':"123456", 

	}
}
```

##### 接受消息JSON格式

[绑定成功]()

> account：绑定成功只会返回账户的id
>

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"account": "q3account"
	}
}
```

[绑定失败]()

* 96：账户已被绑定
* 97：非法账户名字
* 98：非法密码
* 99：非法账户名字


## bind_email

```json
{
	"world": 0,
	"function": "enter_stage",
	"data": {
		"token": "my token",
		"email":"123451234@qq.com"
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

[绑定失败]()

* 99：account must be bound before binding email
* 98：email has already been bound to this account
* 97：email already exists
* 96：verification email could not be sent


## verify_email_code


```json
{
	"world": 0,
	"function": "enter_stage",
	"data": {
		"token": "my token",
		"code":"123456"

	}
}
```

##### 接受消息JSON格式


```json
{
	"status": 0,
	"message": "success",
	"data": {
		"email": "12341523@qq.com"
	}
}
```

[绑定失败]()

* 97：email already exists
* 98：account already has an email bound
* 99：invalid code



