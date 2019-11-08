## 方法列表
* [`exchange_card`](##exchange_card)

## exchange_card
交换各种物品的卡片，如果物品的卡片与自己的等级有关, 可以交换的物品为，金币卡，经验卡，食物卡，铁卡，水金卡，钻石卡，卡的枚举类型来自Item
##### 发送消息JSON格式
```json
{
	"world": 0, 
	"function": "exchange_card",
	"data": {
		"token": "my toekn ^_^",
    "card_id": 18
	}
}
```
##### 接受消息JSON格式
[成功]()

> remaining： 累积的物品数量，iid：物品的id：value物品的数量
>
> reward：变化的物品数量
```json
{
	"status": 0,
	"message": "exchange successful",
	"data": {
		"remaining": "3:2:1999000",
		"reward": "3:2:1000"
    }
	}
} 
```
[失败]()

* 99: 卡片数量不足
* 98: 卡片id不对

