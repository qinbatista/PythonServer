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



## get_new_mail

##### 发送消息JSON格式

获取所有新邮件

```json
{
	"world": 0,
	"function": "get_new_mail",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[成功]()

> mail：所有的新邮件
>
> - read：0未读，1已读
> - body：邮件内容
> - time：邮件收到的时间
> - from：来自的玩家游戏名
> - type：邮件类型
> - subj：邮件主题
> - key：用于读邮件需要发送的key
>
> count：邮件数量
>
> - cur：邮件总数量
> - max：邮箱最大容量

```
{
    "status": 0,
    "message": "success",
    "data": {
        "mail": [
            {
                "read": 0,
                "body": "\u5185\u5bb91\n",
                "time": "2019-12-16 17:00:33",
                "from": "name_h0",
                "type": "0",
                "subj": "\u4e3b\u98981",
                "key": "1576486833.M917814P3900Q560.debian"
            }
        ],
        "count": {
            "cur": 1,
            "max": 100
        }
    }
}
```



## get_all_mail

##### 发送消息JSON格式

获取所有邮件，包括所有新邮件

```json
{
	"world": 0,
	"function": "get_all_mail",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[成功]()

> mail：所有的新邮件
>
> - read：0未读，1已读
> - body：邮件内容
> - time：邮件收到的时间
> - from：来自的玩家游戏名
> - type：邮件类型
> - subj：邮件主题
> - key：用于读邮件需要发送的key
>
> count：邮件数量
>
> - cur：邮件总数量
> - max：邮箱最大容量

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "mail": [
            {
                "read": 0,
                "body": "\u5185\u5bb91\n",
                "time": "2019-12-16 17:00:33",
                "from": "name_h0",
                "type": "0",
                "subj": "\u4e3b\u98981",
                "key": "1576486833.M917814P3900Q560.debian"
            }
        ],
        "count": {
            "cur": 1,
            "max": 100
        }
    }
}
```

[失败]()



## delete_mail

##### 发送消息JSON格式

删除指定邮件

> 

```json
{
	"world": 0,
	"function": "delete_mail",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[成功]()

> 

```json

```

[失败]()

* 99







## delete_read_mail

##### 发送消息JSON格式

删除所有已读邮件

> 

```json
{
	"world": 0,
	"function": "delete_read_mail",
	"data": {
		"token": "my token"
	}
}
```

##### 接受消息JSON格式

[成功]()

> 

```json

```

[失败]()

* 99

