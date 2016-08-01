目录:
1. 注册
2. 登录
3. 获取个人信息
4. 修改个人信息
5. 获取他人信息
6. 搜索用户
7. 关注
8. 取消关注
9. 我关注的人
10. 关注我的人


1. 注册


POST /v1/snap/signup
{
	username: string, // 必须
	password: string, //必须
}
成功返回:
{data: {result: 'ok'}}
失败返回
error_code: 10108 参数错误
error_code: 10192 用户名已存在
error_code: 10132 保存用户失败


2. 登录
POST /v1/snap/signin
{
	username: string, // 必须
	password: string, // 必须
}
成功返回:
{
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
	}
}
失败返回:
error_code: 10133 用户不存在
error_code: 10134 密码错误

3. 获取个人信息
GET /v1/snap/users/profile
成功返回:
{
	data: {
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
	    coin: int, // 金币总数
	    cash_out_rate: int, // 提现比例
	    min_withdraw: int, // 最小提现金额
	}
}
失败返回:
error_code: 10133 用户不存在

4. 修改个人信息
POST /v1/snap/users/profile
{
	data: {
		avatar: string,
		cover: string,
		description: string,
		reply_cost: int,
		pay_prompt: int,
		push_notify: int,
	}
}
成功返回:
{data: {result: 'ok'}}
失败返回:
error_code: 10132 保存用户信息失败

5. 获取他人信息
GET /v1/snap/users/{id}
成功返回:
{
		data: {
		uid: int,
	    username: string,
	    avatar: string,
	    cover: string,
	    description: string,
	    follower_count: int, // 关注我的总人数
	    following_count: int, // 我关注的总人数
	    is_follow: int, // 是否关注
	}
}
失败返回:
error_code: 10133 用户不存在

6. 搜索用户
GET /v1/snap/users/search
{
	keyword: string
}
成功返回:
{
	data: {
		list: [
			{
				uid: int,
			    username: string,
			    avatar: string,
			    cover: string,
			    description: string,
			    follower_count: int, // 关注我的总人数
			    following_count: int, // 我关注的总人数
			}
		],
		next: string
	}
}
失败返回:
error_code: 10133 用户不存在

7. 关注
POST /v1/snap/follows
{
	uid: int
}
成功返回:
{data: {result: 'ok'}}
失败返回:
error_code: 10140 保存关注信息失败

8. 取消关注
POST /v1/snap/follows/{id}/delete
成功返回:
{data: {result: 'ok'}}
失败返回:
error_code: 10140 保存关注信息失败

9. 我关注的人
GET /v1/snap/followings
成功返回:
{
	data: {
		list: [
			{
				uid: int,
			    username: string,
			    avatar: string,
			    cover: string,
			    description: string,
			    follower_count: int, // 关注我的总人数
			    following_count: int, // 我关注的总人数
			}
		],
		next: string
	}
}
失败返回:
error_code: 10141 没有关注的人

10. 关注我的人
GET /v1/snap/followers
成功返回:
{
	data: {
		list: [
			{
				uid: int,
			    username: string,
			    avatar: string,
			    cover: string,
			    description: string,
			    follower_count: int, // 关注我的总人数
			    following_count: int, // 我关注的总人数
			}
		],
		next: string
	}
}
失败返回:
error_code: 10141 没有关注的人

