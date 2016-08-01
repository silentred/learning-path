# Feed设计

## 存储

mysql:
feeds (id, uid, object_id, `object_type`, millisecond, `created_at`, `updated_at`)

redis:

未读 sorted set: 
key: unread_set:100143
score	    value
`millisec`  `feed_id`

已读 sorted set:
key: read_set:100143
score		value
`millisec`  `feed_id`

某人自己的feed set:
key: feeds:{uid}
score		value
`millisec`	`feed_id`

## 流程

### 发布新的 Feed 时：
1. mysql Feed表插入数据，假设id为 13
2. 查询关注者的 uid 集合, 遍历uid, 插入未读set： 
zadd unread_set:{uid} NX {millisec} 13, NX表示只新添加member,不update.
同时，得到该uid未读set中的条数，mqtt 推送给他。

### 删除Feed：


### 查看消息：
1. 查看当前用户的未读set，取出所有值，放入已读队列。 
`zunionstore read_set:{uid} 2 unread_set:{uid} read_set:{uid} AGGREGATE MAX` ; 取并集
del unread_set:{uid}

2. 已读分页操作 
`zrevrangebyscore read_set:{uid} +inf -inf 0 10`, 根据 score 从大到小排序, offset = 0, perPage=10, +inf 可以用当前时间 millisecond 来代替。
第二页为上一次查询结果的 最小millisecond。

### 关注某人：
添加关注关系
`zunionstore read_set:{uid} 2 feeds:{pub_uid} read_set:{uid} AGGREGATE MAX`; 取并集

### 取消关注某人：
删除关注关系
取出某人所有Feed id, 遍历，从 read_set:{uid} 中删除



# 直播

## mysql
streams (

)

videos
{
	id: int,
	uid: int,
	name: string (uid-startSecond),
	type: uint (1:直播录像, 2: 保留),
	is_live: uint (直播是否完成),
	encode_finished: uint (转码保存是否完成， 1: 完成，0: 未完成), 
	url: string (m3u8),
	target_url: string (mp4),
	persistent_id: string,
	start: int (second),
	end: int (second),
	duration: int (second),
	cover: string (url),
	title: string (''),
	tags: string (a,b,c)
}

GET /v1/live/push
{
	'stream_json': "xxx"
}

GET /v1/live/pull/{id}
{
	'rtmp_live_url' : 'xxx'
}


.array(1) {
  ["ORIGIN"]=>
  string(52) 
}
push: "rtmp://pili-publish.nihao.com/beingnihao-PL/100143?key=10658a8b7536657a"
pull: "rtmp://pili-live-rtmp.nihao.com/beingnihao-PL/100143"


[2016-03-17 04:50:26] lumen.INFO: {"message":"streamStatus","updatedAt":"2016-03-17T12:50:26.071277707+08:00","data":{"id":"z1.beingnihao-PL.100143","url":"rtmp:\/\/123.59.63.1\/beingnihao-PL\/100143?key=10658a8b7536657a","status":"connected"}}

[2016-03-17 04:51:06] lumen.INFO: {"message":"streamStatus","updatedAt":"2016-03-17T12:51:06.056680665+08:00","data":{"id":"z1.beingnihao-PL.100143","url":"rtmp:\/\/123.59.63.1\/beingnihao-PL\/100143?key=10658a8b7536657a","status":"disconnected"}}



## 目前Feed的情况

### 写入

- Feed::store
- Service::store
- Live::onConnected

- Service::update
- Live::onDisconnected
- Service::delete
- Feed::delete

- mongodb, status::update

### 读取

- Feed::subscribe （where uid in, where status or (uid=xx and status in)）
- Feed::new 
- Feed::nearby ()
- 服务列表
- live列表


toMongoDoc(object) // 返回存入mongo的




 

