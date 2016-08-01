# 用户

## 注册用户

### request
$rule = [
    'username' => 'required|size:20', // bin2hex(openssl_random_pseudo_bytes(10)); 需要保证唯一
    'unionid' => 'required',
    'avatar'=> 'required', // ["pic-on-qiniu"]
    'fullname'=> 'required', // 微信的昵称(nickname)
    'sex'=> 'required|in:0,1,2', // 1 男，2 女， 0 未知
    'province'=> 'required',
    'city'=> 'required',
    'country'=> 'required'
];

### response
返回新建用户的所有字段
{
	"id": 123,
	"fullname": "xxx",
	...
}

## 用户登陆

### request
$rule = [
	'unionid' => 'required',
];

### response
返回对应user的所有字段
{
	"id": 123,
	"fullname": "xxx",
	...
}

## 用户数据修改

### request
$rule = [
	'id' => '',
	'unionid' => '' // 也是唯一的，不会和id同时出现，若出现以id为准；微信回调时返回付款者的是否订阅
	'wechat' => '', // 微信号，等
	...
];

### response
修改完的user完整字段


# 关于User表

建议user表加上三个字段：

- from，表示注册来自哪里，微信或者app；
- is_main，表示是否是主账号（0，1），用app绑定前，微信注册和app注册都是主账号，绑定微信后，app为主账号，微信为辅助账号。无论微信还是app都只能登陆主账号。
- bind_status，表示当前账号的绑定情况，作用是登陆主账号后判断是否需要去读取辅助账号。 用位来判断，例如 00000001 表示app，00000011 表示app+微信。



# 玩法


## 玩法列表

### request
$rule = [
	'biggest_id' => '' // 每次取小于此id的 limit 个玩法；第一页次指为空。
	'limit' => '', // default 5
	'city' => '', // nullable，'北京市'
	'uid' => ''// nullable, 取出该用户（主账号，次账号）发表的玩法
	'wish' => '' // boolean, 必须有uid才有意义，表示改用户想玩的玩法
	'order' => 'desc', // 可以考虑添加排序，默认为 orderBy(id, desc)
	'field' => 'id'
];

### response
玩法数组，每个玩法包含了发布者信息, 发布者信息至少要给出 avatar, nickname, intro, unionid

可以用 eloquent relation 来简化查询, 例如

```php
$builder = Itinerary::where(function ($query) use ($city) {
    if ($city) {
        $query->where('city', $city);
    }
})->where('status', '!=', 2);

$itineraries = $builder->with([
    'user' => function ($query) {
        $query->select(['avatar', 'nickname', 'intro', 'unionid']);
    }
])->orderBy('id', 'desc')->limit($per_page)->get();

$total_count = $builder->count();
```


## 发布玩法

### request
$rule = [
	'uid' => 'required|numeric',
	'title' => 'required',
	'cover' => 'required', // "pic-on-qiniu.jpg"
	'price' => 'required',
	'content' => 'required', // json
	'country' => '',  // 微信没有要求填这两个数据
	'province' => '',
	'city' => 'required',
	'is_free' => 'required',
	'width' => 'required', // 封面的宽高，用七牛截图时需要
	'height' => 'required',
];

### response
返回新建的玩法和发表人
{
	"title": "xxxx",
	"user": {"id":123, "fullname": "xxx"},
	...
}


## 更新玩法

### request
比发布多一个 'id' 字段

### response
返回修改完的完整玩法，包含发表人

### 相对频繁更新的字段
`share_count`, `bought_count`, `wish_count`, `views`
目前app itineraries 表 没有这些字段，share, wish 需要记录是user和itinerary的关系，是否由微信项目自行维护？



# 订单

## 产生订单

### request

$rule = [
	'object_id' => 'required|numeric', // 玩法id
	'servicer_uid' => 'required|numeric',
	'consumer_uid' => 'required|numeric',
	'total' => 'required',
	'out_trade_no' => 'required',
	'pay_type' => '',  // 公众号暂时没有余额支付，该字段固定为 wechat
];

### response
新插入的订单的完整字段


## 查询单个订单(防止重复下单；我的收入明细)

### request

$rule = [
	"servicer_id" : 1,
	"consumer_id" : 2,
	"object_id": 1,
	"pay_status": 1, // 以上四个是用于判断重复购买的，同时存在

	"out_trade_no" // 此值是唯一的，直接查询

	"id": 1, // 或者 直接根据id查询，我的收入明细中查看单个交易的情况
];

### response
第一种查重复的情况只需要返回订单字段即可；第二种需要 订单+该订单对应的玩法，卖家，买家的信息；
可以考虑加上一个 "level" : "normal|detail" 来判断是否获取详细信息；或者全部返回详细信息，减少复杂



## 列表 (我约别人；别人约我; 我的收入明细)

### request
$rule = [
	"uid" => 123,
	"role" => "seller|buyer", // 根据uid身份来取列表
	"page" => '', // nullable, 如果page，limit都为空，则展示全部，不用分页
	"limit" => '', // nullable, default 5
	"status"=> '', //  nullable，status等于某个值的条件
	"pay_status"=> '' // nullable
];

### response
订单列表，包含该订单对应的玩法，卖家，买家的信息
[
	{
		"id": 1,
		"object_id": 1,
		"total" : 100,
		....
		"itinerary": {
			"title" : "abc",
			...
		},
		"buyer": {
			"uid": 123,
			...
		},
		"seller": {
			"uid" : 125,
			...
		},
	},
	...
]


## 更新订单

### request
{
	"pay_status": 1,
	"status": 2,
	"payid" : "xxx" // 微信支付成功后返回的 transaction_id
	"out_refund_no": "xxx" // 微信退款成功后，out_trade_no 赋给 out_refund_no
	"updated_at": '...' // 每次更新此时间
}

### response
修改后的订单，不需要对应玩法，卖家买家。
