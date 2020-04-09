## 方法列表
* [`check_in_sign`](##check_in_sign)
* [`check_in_supplement`](##check_in_supplement)
* [`check_in_all`](##check_in_all)

<font color=#00ccFF>返回状态码集合如下：</font>

```python
# 99 - You have already signed in today
# 98 - no day missing
# 97 - materials insufficient
# 0 - success
```



## check_in_sign
签到功能
##### 发送消息JSON格式
```json
{
	"world": 0, 
	"function": "check_in_sign",
	"data": {
		"token": "my toekn ^_^"
	}
}
```
##### 接受消息JSON格式
[成功]()

> remain： 剩余物资
>
> reward：变化物资
```json
{
    "status": 0,
    "message": "Sign-in success",
    "data": {
        "remain": [
            "3:5:100"
        ],
        "reward": [
            "3:5:100"
        ]
    }
}
```
[失败]()

```python
# 99 - You have already signed in today
```



## check_in_supplement

补签功能

##### 发送消息JSON格式

```json
{
	"world": 0, 
	"function": "check_in_supplement",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

[成功]()

> remain： 剩余物资
>
> reward：变化物资
>
> supplement：补签情况

```json
{
    "status": 0,
    "message": "Successful signing",
    "data": {
        "supplement": {
            "01": {
                "remain": [
                    "3:18:3"
                ],
                "reward": [
                    "3:18:1"
                ]
            },
            "02": {
                "remain": [
                    "3:5:999080"
                ],
                "reward": [
                    "3:5:100"
                ]
            },
            "03": {
                "remain": [
                    "3:9:200"
                ],
                "reward": [
                    "3:9:100"
                ]
            },
            "04": {
                "remain": [
                    "3:33:300"
                ],
                "reward": [
                    "3:33:100"
                ]
            },
            "05": {
                "remain": [
                    "2:101:10"
                ],
                "reward": [
                    "2:101:5"
                ]
            },
            "06": {
                "remain": [
                    "0:101:10"
                ],
                "reward": [
                    "0:101:5"
                ]
            },
            "07": {
                "remain": [
                    "3:33:400"
                ],
                "reward": [
                    "3:33:100"
                ]
            },
            "08": {
                "remain": [
                    "3:18:4"
                ],
                "reward": [
                    "3:18:1"
                ]
            }
        },
        "remain": [
            "3:5:998980"
        ],
        "reward": [
            "3:5:640"
        ]
    }
}
```

[失败]()

```python
# 98 - no day missing
# 97 - materials insufficient
```



## check_in_all

获取签到信息

##### 发送消息JSON格式

```json
{
	"world": 0, 
	"function": "check_in_all",
	"data": {
		"token": "my toekn ^_^"
	}
}
```

##### 接受消息JSON格式

[成功]()

> history： 签到历史情况
>
> today：服务器当天日期
>
> cd：剩余多久到第二天

```json
{
    "status": 0,
    "message": "Successfully obtained all check-in status this month",
    "data": {
        "today": 9,
        "cd": 30897,
        "history": {
            "01": {
                "date": "2020-04-01",
                "reward": 1
            },
            "02": {
                "date": "2020-04-02",
                "reward": 1
            },
            "03": {
                "date": "2020-04-03",
                "reward": 1
            },
            "04": {
                "date": "2020-04-04",
                "reward": 1
            },
            "05": {
                "date": "2020-04-05",
                "reward": 1
            },
            "06": {
                "date": "2020-04-06",
                "reward": 1
            },
            "07": {
                "date": "2020-04-07",
                "reward": 1
            },
            "08": {
                "date": "2020-04-08",
                "reward": 1
            },
            "09": {
                "date": "2020-04-09",
                "reward": 1
            }
        }
    }
}
```

[失败]()

无



## 

