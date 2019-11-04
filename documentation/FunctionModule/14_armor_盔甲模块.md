## 方法列表

* [`upgrade_armor`](##upgrade_armor)
* [`get_all_armor`](##get_all_armor)

##upgrade_armor

##### 发送消息JSON格式

升级护甲, 指定`等级`，指定`种类`, 此方法会把`所有`该等级的护甲，按照3:1的比例升级为高等级护甲,

> aid: 护甲的id
>
> level: 护甲的等级

```json
{
	"world": 0,
	"function": "get_all_weapon",
	"data": {
		"token": "my token",
    "aid":1,
    "level":1
	}
}
```

##### 接受消息JSON格式

[成功]()

> armors：返回所有关于护甲的信息
>
> resource：消耗护甲的当前量
>
> production：升级护甲的当前量

```json
{
	"status": 0,
	"message": "success",
	"data": {
		"armors": {
			"resource": {
				"aid": 1,
				"level": 4,
				"quantity": 0
			},
			"production": {
				"aid": 1,
				"level": 5,
				"quantity": 182714
			}
		}
	}
}
```

[失败]()

* 99: 盔甲不足

##get_all_armor

##### 发送消息JSON格式

获取所有盔甲的信息

```json
{
	"world": 0, 
	"function": "level_up_weapon",
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
				"quantity": 0
			},
			{
				"aid": 1,
				"level": 2,
				"quantity": 0
			},
			{
				"aid": 1,
				"level": 3,
				"quantity": 2
			},
			{
				"aid": 1,
				"level": 4,
				"quantity": 0
			},
			{
				"aid": 1,
				"level": 5,
				"quantity": 2
			},
			{
				"aid": 1,
				"level": 6,
				"quantity": 160903
			}
		]
	}
}
```

[失败]()

* 如果没有护甲，返回的列表为空
* 98: 邮箱有问题
* 97: 没有此人
* 96: 一天只能申请6个人
* 95: 已经成为朋友或已经申请过这个人为朋友


