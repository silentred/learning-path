# new-msg-type

## FullscreenAdTpl

```json

{
	"msgid" : "3501ce9bd72255bc1049ad66ca9da09000cc037d",
	"type" : 1,
	"body": {
		"type" : -1,
		"content": {
			"img": "http://xxx.png",
			"w": 120,
			"h": 60,
			"url": "http://xxx",
			"msg": [
				{"t":"txt", "c":"xxx"}
			], // 富文本
			"action":[
				{"t":"txt", "c":"xxx"}
			] // 富文本
		}
	},
	"time": 1458727012,
	"context": {
		"uid":"100101",
		"fullname":"xxx",
		"avatar":"http:xxx.jpg",
		"sex":"1",
		"truthful":"3",
		"age":"0",
		"intro":""
	}
}

```

## ItemRecomCard

```json

{
	"msgid" : "3501ce9bd72255bc1049ad66ca9da09000cc037d",
	"type" : 1,
	"body": {
		"type" : 13,
		"content": {
			"title": "xxx",
			"img": "http://xxx.png",
			"w": 120,
			"h": 60,
			"url": "http://xxx",
			"user":{
				"fullname": "xxx",
				"avatar": "http://xxx.png"
			},
			"msg": [
				{"t":"txt", "c":"xxx"}
			],
			"action":[
				{"t":"txt", "c":"xxx"}
			]
		}
	},
	"time": 1458727012,
	"from": {
		"uid":"100101",
		"fullname":"xxx",
		"avatar":"http:xxx.jpg",
		"sex":"1",
		"truthful":"3",
		"age":"0",
		"intro":""
	}
	
}

```

## UserRecomCard

```json

{
	"msgid" : "3501ce9bd72255bc1049ad66ca9da09000cc037d",
	"type" : 1,
	"body": {
		"type" : 14,
		"content": {
			"user":{
				"fullname": "xxx",
				"avatar": "http://xxx.png",
				"cover": "http://x.png",
				"intro": "xxx",
				"uid": 123
			},
			"url": "http://xxx",
			"msg": [
				{"t":"txt", "c":"xxx"}
			],
			"action":[
				{"t":"txt", "c":"xxx"}
			]
		}
	},
	"time": 1458727012,
	"from": {
		"uid":"100101",
		"fullname":"xxx",
		"avatar":"http:xxx.jpg",
		"sex":"1",
		"truthful":"3",
		"age":"0",
		"intro":""
	}
	
}

```

## TitleMsgCard

```json

{
	"msgid" : "3501ce9bd72255bc1049ad66ca9da09000cc037d",
	"type" : 1,
	"body": {
		"type" : 15,
		"content": {
			"title": "xxxx",
			"url": "http://xxx",
			"msg": [
				{"t":"txt", "c":"xxx"}
			],
			"action":[
				{"t":"txt", "c":"xxx"}
			]
		}
	},
	"time": 1458727012,
	"from": {
		"uid":"100101",
		"fullname":"xxx",
		"avatar":"http:xxx.jpg",
		"sex":"1",
		"truthful":"3",
		"age":"0",
		"intro":""
	}
	
}

```


## ImgMsgCard

```json

{
	"msgid" : "3501ce9bd72255bc1049ad66ca9da09000cc037d",
	"type" : 1,
	"body": {
		"type" : 16,
		"content": {
			"img": "http://xxxx.png",
			"w": 120,
			"h": 60,
			"url": "http://xxx",
			"msg": [
				{"t":"txt", "c":"xxx"}
			],
			"action":[
				{"t":"txt", "c":"xxx"}
			]
		}
	},
	"time": 1458727012,
	"from": {
		"uid":"100101",
		"fullname":"xxx",
		"avatar":"http:xxx.jpg",
		"sex":"1",
		"truthful":"3",
		"age":"0",
		"intro":""
	}
	
}

```

## PaymentCardTpl

```json

{
	"msgid" : "3501ce9bd72255bc1049ad66ca9da09000cc037d",
	"type" : 1,
	"body": {
		"type" : -2,
		"content": {
			"title": "xxx",
			"timestamp": 1458727012,
			"payment": {
				"user":{
					"avatar": "http://xxx.png",
					"fullname": "xxx"
				},
				"pay_action": "支付金额",
				"fee": "299.00"
			},
			"pre_text": "xxxx",
			"content_text": [
				{"t":"txt", "c":"支付方式: ", "fc":"040404"},
				{"t":"txt", "c":"xxx \n"}
			],
			"suf_text": "xx",
			"url": "http://xxx",
			"action":[
				{"t":"txt", "c":"xxx"}
			]
		}
	},
	"time": 1458727012,
	"context": {
		"uid":"100101",
		"fullname":"xxx",
		"avatar":"http:xxx.jpg",
		"sex":"1",
		"truthful":"3",
		"age":"0",
		"intro":""
	}
}

```

钱包
分享
雷达

### 大视频
```
{
	"msgid" : "3501ce9bd72255bc1049ad66ca9da09000cc037d",
	"type" : 1,
	"body": {
		"type" : -1,
		"content": {
			"r": "xxx.mp4",
			"cover_r": "http://xxx.png",
			"w": 120,
			"h": 60,
			"l": 123, //时长，秒
			"s": 123 // 文件大小，optional
		}
	},
	"time": 1458727012,
	"from": {
		"uid":"100101",
		"fullname":"xxx",
		"avatar":"http:xxx.jpg",
		"sex":"1",
		"truthful":"3",
		"age":"0",
		"intro":""
	}
}
```


