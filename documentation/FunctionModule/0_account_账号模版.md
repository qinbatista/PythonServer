## 方法列表

* [`login_unique`](##login_unique)
* [`login`](##login)
* [`account_all_info`](##account_all_info)
* [`bind_account`](##bind_account)
* [`bind_email`](##bind_email)
* [`unbind_email`](##unbind_email)
* [`bind_phone`](##bind_phone)
* [`unbind_phone`](##unbind_phone)
* [`verify_email_code`](##verify_email_code)
* [`verify_phone_code`](##verify_phone_code)

- [`create_player`](##create_player)

- [`enter_world`](##enter_world)



## login_unique

游客登陆，直接用机器的唯一标识符登陆设备

> unique_id：玩家的唯一id，目前使用unity获取唯一标识符的方法获取唯一标识符

```json
{
	"world": 0,
	"function": "login_unique",
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



## login

玩家使用账户和密码登陆账户

> identifier：表示用什么方式登陆，其值可以为`email`，`account`，`phone_number`
>
> value：identifier的值，如果是email则表示必须输入aaaa@email.com格式才能登陆
>
> password：用户的密码

```json
{
	"world": 0,
	"function": "enter_stage",
	"data": {
		"token": "my token",
		"identifier": "email", 
    	"value":"account", 
    	"password":"123456"
	}
}
```

##### 接受消息JSON格式

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



## account_all_info

获取所有的用户信息

```json
{
	"world": 0,
	"function": "account_all_info",
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
        "account": "account_h0",
        "email": "2428437133@qq.com",
        "phone_number": ""
    }
}
```



## bind_account

此方法只有在玩家用游客登陆的时候才能使用，游客登陆玩家在设置里或者提示界面里使用此方法

> account：绑定用户的账号
>
> password：用户的密码

```json
{
	"world": 0,
	"function": "bind_account",
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
	"function": "bind_email",
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
	"data": { }
}
```

[绑定失败]()

* 99：account is not bound
* 98：email has already been bound
* 97：email already exists
* 96：email could not be sent




## unbind_email

```json
{
	"world": 0,
	"function": "unbind_email",
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
	"data": { }
}
```

[绑定失败]()

* 99：account is not bound
* 98：你未绑定邮箱
* 97：email error
* 96：email could not be sent



## bind_phone

```json
{
	"world": 0,
	"function": "bind_phone",
	"data": {
		"token": "my token",
		"phone_number":"15000000000"
	}
}
```

##### 接受消息JSON格式

```json
{
	"status": 0,
	"message": "success",
	"data": { }
}
```

[绑定失败]()

* 99：account is not bound
* 98：phone has already been bound
* 97：phone already exists
* 96：phone could not be sent
* 95：今天发送短信次数已用完



## unbind_phone

解绑手机

```json
{
	"world": 0,
	"function": "unbind_phone",
	"data": {
		"token": "my token",
		"phone_number":"15000000000"
	}
}
```

##### 接受消息JSON格式

```json
{
	"status": 0,
	"message": "success",
	"data": { }
}
```

[绑定失败]()

* 99：account is not bound
* 98：你未绑定手机号
* 97：手机号错误
* 96：phone could not be sent
* 95：今天发送短信次数已用完



## verify_email_code

> status：0代表绑定邮箱验证，1代表解绑邮箱验证


```json
{
	"world": 0,
	"function": "verify_email_code",
	"data": {
		"token": "my token",
		"code":"123456",
        "status": 0
	}
}
```

##### 接受消息JSON格式


```json
{
	"status": 0,
	"message": "success, email verified",
	"data": {
		"email": "12341523@qq.com"
	}
}
```

```json
{
	"status": 1,
	"message": "unbind success, email verified",
	"data": {
		"email": "12341523@qq.com"
	}
}
```

[绑定失败]()

* 97：email already exists
* 98：account already has an email bound
* 99：invalid code
* 90：无效状态码





## verify_phone_code

> status：0代表绑定手机验证，1代表解绑手机验证


```json
{
	"world": 0,
	"function": "verify_phone_code",
	"data": {
		"token": "my token",
		"code":"1234",
        "status": 0
	}
}
```

##### 接受消息JSON格式


```json
{
	"status": 0,
	"message": "success, phone verified",
	"data": {
		"phone": "18323019610"
	}
}
```

```json
{
	"status": 1,
	"message": "unbind success, phone verified",
	"data": {
		"phone": "18323019610"
	}
}
```

[绑定失败]()

* 97：phone already exists
* 98：account already bound phone
* 99：invalid code
* 90：无效状态码



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

```json
{
	"world": 0,
	"function": "enter_world",
  	"world": 1,
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
	"data": {}
}
```

* 98: 此世界没有没有创建角色，需要创建好角色后再进入世界





