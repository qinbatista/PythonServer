## 方法列表

* [`send_mail`](##send_mail)
* [`get_new_mail`](##get_new_mail)
* [`get_all_mail`](##get_all_mail)
* [`delete_mail`](##delete_mail)
* [`delete_read_mail`](##delete_read_mail)

## send_mail

##### 发送消息JSON格式

发送邮件

> gn_target：邮件接收对象
>
> subj：邮件主题
>
> body：邮件内容

```json
{
	"world": 0,
	"function": "send_mail",
	"data": {
		"token": "my token",
    	"gn_target": "玩家游戏名字",
        "subj": "主题",
        "body": "内容"
	}
}
```

##### 接受消息JSON格式

[成功]()

> sent：当天发送出的邮件数量

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "sent": 2
    }
}
```

[失败]()

* 99：今天发送的邮件已经达到上限
* 98：邮箱错误

















## get_all_armor

##### 发送消息JSON格式

获取所有盔甲的信息

```json
{
	"world": 0, 
	"function": "get_all_armor",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

[成功]()

> aid：护甲的id
>
> level：护甲的等级
>
> quantity：护甲的数量

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"armors": [
			{
				"aid": 1,
				"level": 1,
				"quantity": 1
			},
			{
				"aid": 1,
				"level": 2,
				"quantity": 3
			}
		]
	}
}
```

[失败]()

* 如果没有护甲，返回的列表为空


