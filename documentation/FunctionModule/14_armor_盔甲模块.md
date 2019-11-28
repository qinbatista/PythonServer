## 方法列表

* [`upgrade_armor`](##upgrade_armor)
* [`get_all_armor`](##get_all_armor)

## upgrade_armor

##### 发送消息JSON格式

升级护甲, 指定`等级`，指定`种类`, 此方法会把`所有`该等级的护甲，按照3:1的比例升级为高等级护甲,

> aid: 护甲的id
>
> level: 护甲的等级
>
> num: 需要升级成的件数(可以不传，默认生成一个)

```json
{
	"world": 0,
	"function": "upgrade_armor",
	"data": {
		"token": "my token",
    	"aid":1,
    	"level":1
	}
}
```

##### 接受消息JSON格式

[成功]()

> aid：盔甲id
>
> remaining：盔甲等级下的实际数量
>
> reward：盔甲等级下的数量改变情况

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"aid": 1,
		"remaining": {
			"1": 1,
			"2": 91,
			"3": 4,
			"4": 1,
			"5": 27336,
			"6": 0,
			"7": 0,
			"8": 0,
			"9": 0,
			"10": 121
		},
		"reward": {
			"1": 0,
			"2": -3,
			"3": 1,
			"4": 0,
			"5": 0,
			"6": 0,
			"7": 0,
			"8": 0,
			"9": 0,
			"10": 0
		}
	}
}
```

[失败]()

* 99：无效升级等级
* 98：无效盔甲id
* 97：基础盔甲不足

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


