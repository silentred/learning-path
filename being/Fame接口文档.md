# Fame 接口

## Inbox list
GET v1/snap/inbox 
```
query: 
{
	start: unix timestamp
	limit: 20
	msg_id: 123 // 客户端最新的 object_id , 请求包含此字段则增量返回返回最新的limit条记录
}

response:
{
	list: [
		{
			object_type: 1 // 1 图片，2 视频
			object_id: 123
			object: {
				id: 123,
				content: {url:xxx, w:123, h: 123}, 若type为视频，多一个 d 字段，表示时长，单位为秒
				type: 1代表图片，2代表视频
				text: {'c': xxx, 'o': 50.03 },  // c是content内容，o是offset (float) 
				price: 123, // 看图片需要的金币
				reply_price: 123, // 回复需要的金币
				deadline: unix timestamp, 时间点为发表后24小时
				created_at: datetime
				view_second: 5 // 可看时间，单位为秒
				status: 1, // 暂时无用
				can_reply: 0, // 0 or 1 能否回复
				replied: 1, // 0 or 1 是否已经回复
				read: 1 // 0 or 1 是否已读
				receiver_income: 123 // reply列表中需要显示这条回复给receiver带来了多少收入
				reply_discount: 123 // 回复这条msg时，可以得到的折扣
				presents: [
					{'id': 0, 'name': 'Heel', 'price': 100, 'cover': 'http://f1.being.com/gift/cover/1-heel.png', 'animation' : 'http://f1.being.com/gift/resource/1-heel.apng', 'w':454, 'h': 461, 'fullscreen':0, count: 2},
					...
				]
				user: {
					uid: 100143,
					username: xxx,
					fullname: xxx,
					gender: 1
					avatar: http://xxxx
					cover: http://xxx
					description: xxxx
					follower_count: 123
					following_count: 123
				},
			}
		}
	],
	next: unix timestamp
}
```

## Reply list

GET v1/snap/reply
query, response 和 Inbox list 一样

## View image and pay for it

GET v1/snap/message/{id}

```
response:
{
	{
		id: 123,
		content: {url:xxx, w:123, h: 123}, 若type为视频，多一个 d 字段，表示时长，单位为秒
		type: 1代表图片，2代表视频
		text: {'c': xxx, 'o': 50.03 },  // c是content内容，o是offset (float) 
		price: 123, // 看图片需要的金币
		reply_price: 123, // 回复需要的金币
		deadline: unix timestamp, 时间点为发表后24小时
		created_at: datetime
		view_second: 5 // 可看时间，单位为秒
		status: 1, // 暂时无用
		can_reply: 0, // 0 or 1 能否回复
		replied: 1, // 0 or 1 是否已经回复
		read: 1 // 0 or 1 是否已读
		receiver_income: 123 // reply列表中需要显示这条回复给receiver带来了多少收入
		reply_discount: 123 // 回复这条msg时，可以得到的折扣
		user: {
			uid: 100143,
			username: xxx,
			fullname: xxx,
			gender: 1
			avatar: http://xxxx
			cover: http://xxx
			description: xxxx
			follower_count: 123
			following_count: 123
		},
	}
}
```
## Publish Message

POST v1/snap/message
```
query:
{
	image: url // 图片或者视频类型，都需要传. (视频表示封面)
	video: url // 图片类型不传；视频类型表示视频地址
	width: 123
	height: 123
	duration: 123 // video需要
	send_ids: "all" or "100143,100144"
	pre_price: 100 // 发表msg时，用户的希望收入; 如果回复消息，不传该值
	view_second: 9 // 用户设置的可看时长，视频就为视频时长
	text: xxx //内容
	text_offset: 50.03 // offset, float
}

response:
{
	result: ok
}
```


## Reply Message

POST v1/snap/message/reply
```
query:
{
	image: url
	video: url
	width: 123
	height: 123
	duration: 123 // video需要
	send_ids: "all" or "100143,100144"
	view_second: 9 // 用户设置的可看时长，视频就为视频时长
	text: xxx //内容
	text_offset: 50.03 // offset, float
	pay_coin: 200 // 回复时，用户的出价
	reply_msg_id: 123 // 回复必须填写
}

response:
{
	result: ok
}
```

## Send Present Message

POST v1/snap/message/present
```
query:
{
	image: url
	video: url
	width: 123
	height: 123
	duration: 123 // video需要
	send_ids: "all" or "100143,100144"
	view_second: 9 // 用户设置的可看时长，视频就为视频时长
	text: xxx //内容
	text_offset: 50.03 // offset, float
	presents : [{"id":1, "c": 99}, {...}] // id是礼物id，c是礼物数量
}

response:
{
	result: ok
}
```

## Get Present List

GET v1/snap/presents

```
response:
{

}
```

## transactions

GET v1/snap/transactions

response:
```
[
	{
		message: "xxxx",
		balance: 123,
		created_at: 144xxxxx (unix timestamp)
	},
]
```

## Report

POST v1/snap/report

```
query:
{
	object_type: 1 // 1: user 
	object_id: 123
}
```

```
response:
{
	result: "ok"
}
```

## Present List

GET v1/snap/presents

```
query:
{
	start: 0 // 可以不传, 用于分页。返回值中 next 不为空string时，把next值赋给start传入.
	all: 1 or 0 // 1 表示全部礼物， 0 表示当前可以赠送的礼物
}

response:
{
	list: [
		{'id': 0, 'name': 'Heel', 'price': 100, 'cover': 'http://f1.being.com/gift/cover/1-heel.png', 'animation' : 'http://f1.being.com/gift/resource/1-heel.apng', 'w':454, 'h': 461, 'fullscreen':0}
		...
	],
	next: ''
}
```

## Wechat Pay Qrcode

POST v1/snap/pay/wechat

```
query:
{
	uid: 1232123,
	product_id: "com.being.fame.2375" // must be valid
}

response:

Qrcode image

```

## Set Notify Config

POST v1/snap/users/notify

```
query:
{
	receiver_view : 0|1,
    receiver_view_reply => 0|1,
    receiver_publish => 0|1,
    receiver_reply => 0|1,
    sender_reply => 0|1,
}

```

## Update Subscription

POST v1/snap/users/force-sub

```
query:
{
	action: add | del, string
	uid: int
}

```

## bind account

POST v1/snap/bind/account

```
query:
{
	type: int , FB: 1
	account_id: string, FB ID
	account_name: string, FB name
	friends: json string, [{"id": "123sdf", "name": "Tom"}, ...]
}

```

## get potential friends

GET v1/snap/friends/potential

```
response:
[
	{
		uid:
		username:
		fullname:
		gender:
		avatar:
		avatar_thumb:
		cover:
		description:
		follower_count:
		following_count:
		role:
		verify_name:
		is_verify
	}
]

```

**A 为普通人, B 为明星**

- **PUB_CF**
    - 默认值为 2; A 看 B 的消息, A需要付 B的pub_cf * B设定的价格; 
    - 假设 B（明星）发了一个 100 coin 的消息，A看到的价格为200

- **REPLY_CF**
    - 默认值为2；A 回复 B的消息, A需要付 B的reply_cf * B设定的回复价格; 
    - 假设B（明星）设置回复价格为100，A回复B看到的价格为200

- **WITHDRAW_CF**
    - 默认为12.50；B提现, 50000 / 12.5 = 4000 美分


- **PRESENT_CF**
    - 默认值为2；A送礼给B，B得到的礼物价值 ＝ 礼物的价值 / PRESENT_CF;
    - 假设A送了一个100金币的礼物给B（明星），B收到的金币是 50

- **PRESENT_COIN_CF**
    - 默认值为2；A送礼的同时送金币给B，B得到的礼物金币 ＝ 金币数 / PRESENT_COIN_CF;






## get user notify setting

GET v1/snap/users/settings/notify

```
response:
{
	"receiver_view": 1,
    "receiver_view_reply": 1,
    "receiver_publish": 1,
    "receiver_reply": 1,
    "sender_view_reply": 1, // 普通用户没有该字段， STAR用户有该字段
}

``` 

## get user subscription

GET v1/snap/users/settings/force-sub

```
request:
{
	uid: int
}

response:
{
	"is_subscription": 1|0
}

```  

## get bind account index

GET v1/snap/bind/account/index

```
response:
{
	"bind_types": [
      {
        "icon": "http://s0.nihao.com/",
        "title": "Import contacts",
        "type": "phone",
        "color": "7b52fb",
        "bind": 0
      }
    ],
    "featured_users": [
		{
	        uid:
	        username:
	        fullname:
	        gender:
	        avatar:
	        avatar_thumb:
	        cover:
	        description:
	        follower_count:
	        following_count:
	        role:
	        verify_name:
	        is_verify:
	        is_following:
	    }
    ]
}

```


## report 

POST v1/snap/report/log

```
reuqest:
{
	object_id: int
	object_type: int, 1 user| 2 message | 3 moment
}

```

## withdraw info
POST tw/v1/user/withdraw-info
```
request:
{
	pay_type: string, tw.wire | paypal
	sub_type: string
	receipt_info: json string
}

response:
{	
	error_code: 200,
	data: { result: "ok" }
}

```

## tw user info
GET tw/v1/users/{id}
```
成功返回:
{
    error_code: 200,
    data : {
        uid: int,
        username: string,
        avatar: string,
        cover: string,
        description: string,
        follower_count: int, // 关注我的总人数
        following_count: int, // 我关注的总人数
        push_notify: int, // 推送通知
        pay_prompt: int, // 支付提示
        reply_cost: int, // 回复价格
        recharge: int, // 充值金额
        earn: int, // 收入金额
        reward: int, // 奖励金额
        coin: int, // 总金币数
        cash_out_rate: int, // 提现比例
        min_withdraw: int, // 最小提现金额
        can_withdraw: bool, 
        withdraw_info: {
			uid: int,
			pay_type: string,
			sub_type: string,
			receipt_info: json string
    	}
    }
}
失败返回: 无

```











