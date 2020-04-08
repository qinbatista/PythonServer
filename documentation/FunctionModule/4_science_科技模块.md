## 方法列表

* [`science_infos`](##science_infos)
* [`science_up`](##science_up)



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

> science：科技所有情况（{ssa:level}）

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "science": {
            "65536": 1,
            "65792": 1
        }
    }
}
```

[失败]()

无



## science_up

##### 发送消息JSON格式

> 升级科技信息
>
> ssa：移位复合键

```json
{
	"world": 0, 
	"function": "science_up",
	"data": {
		"token": "toekn",
        "ssa": 65536
	}
}
```

##### 接受消息JSON格式

[成功]()

> remain：剩余物资
>
> reward：改变物资
>
> science：科技所有情况（{ssa:level}：ssa是移位得到的合并键）
>
> rws：科技升级情况（{ssa:level}）

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "science": {
            "65536": 1,
            "65792": 1
        },
        "rws": {
            "65792": 1
        },
        "remain": [
            "3:4:999900",
            "3:1:999000"
        ],
        "reward": [
            "3:4:100",
            "3:1:1000"
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


