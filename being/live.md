# 直播接口列表

## 主播
### 获取推流地址

GET /v1/live/push?title=xxx

返回：
{
	'stream_json': "xxx",
	"room_topic": "live_room/{uid}"
}


## 观众
### 得到观看地址


GET /v1/live/pull/{stream_id}

GET /v1/live/watch/{uid}

如果不在直播， 返回
{
	'is_live' : 0,
	'playback_url' : "xxx",
	"title": "xxx"
}

如果在直播：
{
	"is_live": 1,
	"rtmp_live_url": "xx",
	"owner": {uid:123, fullname:"xxx"， avatar:"xxx", sex:1, truthful:1, age: 23, intro: "xxx"},
	"audience_count": 23,
	"audience": [
		{uid:123, fullname:"xxx"， avatar:"xxx", sex:1, truthful:1, age: 23, intro: "xxx"}.
		...
	],
	"room_topic": "xxx",
	"title": "xxx"
}

