# personal home

## API

### 个人主页
GET v2/users/{id}

response:
{
	'uid' => $uid,
    'avatar' => UserService::avatar($user->avatar),
    'cover' => UserService::cover($user->cover),
    'fullname' => $user->fullname,
    'intro' => $user->intro,
    'description' => $user->description,
    'country' => $user->country,
    'country_code' => $user->country_code,
    'province' => $user->province,
    'city' => $user->city,
    'email' => $user->email,
    'mobile' => $user->mobile,
    'sex' => $user->sex,
    'age' => $user->age,
    'constellation' => $user->constellation,
    'truthful' => $user->truthful,
    'follows' => $user->follow_count,
    'fans' => $user->fans_count,
    'share_url' => 'http://'.env('M_DOMAIN').'/share/user?id='.$uid,
    'qrcode_url' => 'http://'.env('M_DOMAIN').'/users/qrcode?id='.$uid,
    'formatted_address' => $user->formatted_address,
    'planet_id' => intval($user->planet_id),
    'is_friend',
    'is_block',
    'in_contacts',
    'is_follow',
    'praise_count',
    'allow_add_friend',
	'more_medal', int
	'medal_url', string
}

去除了 itinerary, itinerary_count, medals, albums
添加了 more_medal, has_story, has_album, medal_url

### 我的故事，分页接口
GET v1/stories

{
	uid: 可选, int, 为空代表操作者自己的uid
	start: 可选, int, timestamp
	limit: 可选, int，默认3
}

response:
{
	list: story array
	next: int, timestamp
}

单个story结构：
{
	'id',
	'title',
	'cover',
	'praise_count',
}

### 图片视频，分页接口 (已有)
GET v1/albums

get query parameters:
{
	type: 可选, int
	uid: 可选, int
	start: 可选, int, timestamp
	limit: 可选, int， 默认10
}

reposne:
{
	result: 图片视频list array
	next: int, timestamp
}

图片视频list中单个item结构为：
{
	id: int
	photo: string
	video: string
	meta: json string
	title: string
}

### Feed分页接口

GET v1/feeds

{
	uid: 可选, int
}

response
{
	list: array
	next: int, timestamp
}

array item:
{
	id: int
	user: {
		'uid' => $user->id,
        'fullname' => $user->fullname,
        'avatar' => UserService::avatar($user->avatar),
        'sex' => $user->sex,
        'truthful' => $user->truthful,
        'age' => $user->age,
        'intro' => $user->intro,
	},
	text: string
	cover: string
	type: int, 类型，图片，视频，服务（玩法，技能，等）
 	video: string
	pictures: string
	praise_count: int
	collect_count: int
}

### 服务分页接口

GET v1/services

{
	uid: 可选, int
}

response
{
	list: array
	next: int, timestamp
}

array item:
{
	id: int
	title: string
	cover: string
	video: string
	pictures: string
	praise_count: int
	collect_count: int
}


## Feed 表：
{
	id: int
	uid: int
	parent_id: int // 转发自；原创为0
	root_id: int // 原创内容的id；原创为0
	text: string
	cover: string
	type: tiny int // 1 图片，2 视频，3 直播
*	service_type: int // 服务（1 玩法，2 技能，3 美食等）
	video: string
	pictures: string
	praise_count: int
	collect_count: int
	long: float // 发表时的经度， 可能为0
	lat: float // 纬度，可能为0
*	location: string // 地点文字
	millisencond: int
	created_at: datetime
	updated_at: datetime
	became_service: bool // 是否已经升级为服务，0 为否，1 为是
	service_id: int //

}

## Service 表, 就用itineraries表添加以下字段
{
	feed_id: int // 从哪条feed升级而来
	type: int // 玩法，技能，美食等
}

## Story 表
{
	id: int
	uid: int
	title: string
	cover: string
	intro: string

}

## Feed 接口

POST /v1/feeds
request:
{
	text: string // 可选，Feed文字
	cover: string // 可选，用户图片或默认图片 七牛key
	type: int 必选，1 图片，2 视频 ，3 直播， 4 服务
	service_type: int 必选 1 一日游，2 技能，3 美食
	video: string 可选，视频 七牛key
	pictures: string, json array
	long: float, 可选 经度
	lat: float, 可选 纬度
	location: string 可选，当前位置
}

response:
{
	id: int
	uid: int
	parent_id: int // 转发自；原创为0
	root_id: int // 原创内容的id；原创为0
	text: string
	cover: string
	type: tiny int // 1 图片，2 视频，3 直播
*	service_type: int // 服务（1 玩法，2 技能，3 美食等）
	video: string
	pictures: array 
	praise_count: int
	collect_count: int
	long: float // 发表时的经度， 可能为0
	lat: float // 纬度，可能为0
*	location: string // 地点文字
	millisencond: int
	created_at: datetime
	updated_at: datetime
	became_service: bool // 是否已经升级为服务，0 为否，1 为是
	service_id: int //
}
