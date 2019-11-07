## 方法列表
* [`exchange_card`](##exchange_card)

## exchange_card
交换各种物品的卡片，如果物品的卡片与自己的等级有关
##### 发送消息JSON格式
```json
{
	"world": 0, 
	"function": "start_hang_up",
	"data": {
		"token": "my toekn ^_^"
	}
}
```
##### 接受消息JSON格式
[签到成功]()
> remaining：物品剩余的数据 3:18:2分别表示 种类id : 商品id : 商品数量，所以3:18: 2表示金币2个
>
> reward：变化的量
```json
{
	"status": 0,
	"message": "Sign-in success",
	"data": {
		"remaining": [
			"3:18:2"
		],
		"reward": [
			"3:18:1"
		]
	}
} 
```
[签到失败]()
* 99: 已签到，不会重复获得奖励

