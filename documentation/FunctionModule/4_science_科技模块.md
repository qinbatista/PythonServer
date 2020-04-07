## 方法列表

* [`science_infos`](##science_infos)
* [`science_fr_up`](##science_fr_up)
* [`science_fm_up`](##science_fm_up)



##### <font color=#00ccFF>返回状态码集合如下：</font>

```python
# 99 - insufficient level
# 98 - max level
# 97 - config does not exist
# 96 - materials insufficient
# 95 - The level of science master is inadequate
# 0 - success
```



## science_infos

##### 发送消息JSON格式

> 获取科技信息
>

```json
{
	"world": 0, 
	"function": "science_infos",
	"data": {
		"token": "toekn"
	}
}
```

##### 接受消息JSON格式

[成功]()

> science：科技所有情况（{科技类别:{科技分支:科技等级}}）

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "science": {
            "1": {
                "1": 2
            }
        }
    }
}
```

[失败]()

无



## science_fr_up

##### 发送消息JSON格式

> 获取科技信息

```json
{
	"world": 0, 
	"function": "science_fr_up",
	"data": {
		"token": "toekn"
	}
}
```

##### 接受消息JSON格式

[成功]()

> remain：剩余物资
>
> reward：改变物资
>
> science：科技所有情况（{科技类别:{科技分支:科技等级}}）
>
> rws：科技升级情况（{科技类别:{科技分支:科技等级}}）

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "science": {
            "1": {
                "1": 3,
                "2": 3
            }
        },
        "rws": {
            "1": {
                "2": 1
            }
        },
        "remain": [
            "3:4:99100",
            "3:1:91000"
        ],
        "reward": [
            "3:4:500",
            "3:1:5000"
        ]
    }
}
```

[失败]()

```python
# 99 - insufficient level
# 98 - max level
# 97 - config does not exist
# 96 - materials insufficient
# 95 - The level of science master is inadequate
```



## science_fm_up

##### 发送消息JSON格式

> 获取科技信息

```json
{
	"world": 0, 
	"function": "science_fm_up",
	"data": {
		"token": "toekn"
	}
}
```

##### 接受消息JSON格式

[成功]()

> remain：剩余物资
>
> reward：改变物资
>
> science：科技所有情况（{科技类别:{科技分支:科技等级}}）
>
> rws：科技升级情况（{科技类别:{科技分支:科技等级}}）

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "science": {
            "1": {
                "1": 3
            }
        },
        "rws": {
            "1": {
                "1": 1
            }
        },
        "remain": [
            "3:4:99100"
        ],
        "reward": [
            "3:4:500"
        ]
    }
}
```

[失败]()

```python
# 99 - insufficient level
# 98 - max level
# 97 - config does not exist
# 96 - materials insufficient
# 95 - The level of science master is inadequate
```

