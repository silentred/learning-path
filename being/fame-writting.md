# 文案

## 交易明细

### 英文

Tom是人物名称，不需要翻译.

```
奖励： 1000 Free Bonus Coins
回复他人, 不带 tip： You replied to Tom for 100 coins
回复他人, 带 tip： You replied to Tom for 100 coins and tipped for 100 coins
他人回复你, 不带 tip： Tom replied to your message for 100 coins
他人回复你, 带 tip： Tom replied to your message for 100 coins and tipped for 100 coins
你看了消息：You viewed a message from Tom for 100 coins
他人看了你的消息：Tom viewed your message for 100 coins
充值：You purchased 1000 coins for $10
提现：You made a withdraw request for 1000 coins worth $10

```

## 错误提示

翻译单引号中的文字，例如英文版本写为：
ErrorCode::INVALID_PARAM => '参数不合法',
ErrorCode::INVALID_PARAM => 'Invalid parameters',

```
ErrorCode::VERSION_SUPPORT => '您的版本过低,请升级',
ErrorCode::INVALID_PARAM => '参数不合法',
ErrorCode::SIGN => '登录失效,请重新登录',
ErrorCode::USER_SAVE => '保存用户信息失败',
ErrorCode::USER_NOT_FOUND => '用户不存在',
ErrorCode::PASSWORD => '邮箱或密码错误',
ErrorCode::USER_UPDATE => '更新用户信息失败',
ErrorCode::MSG_SAVE_FAILED => '保存消息失败',
ErrorCode::MSG_EXPIRE => '消息已过期',
ErrorCode::COIN_NOT_ENOUGH => '金币不足,请充值',
ErrorCode::FOLLOW_SAVE => '关注失败,请重试',
ErrorCode::SEND_EMAIL => '发送邮件失败',
ErrorCode::EMAIL_NOT_FOUND => '邮箱不存在',
ErrorCode::TRANSACTION => '保存交易信息失败',
ErrorCode::USERNAME_FORMAT => '用户名5-16个字符且只允许字母数字下划线',
ErrorCode::PASSWORD_FORMAT => '密码6-18长度',
ErrorCode::GENDER_FORMAT => '请选择性别',
ErrorCode::EMAIL_FORMAT => '邮箱格式不正确',
ErrorCode::REPLY_FAILED => '回复失败,请重试',
ErrorCode::EMAIL_EXISTS => '邮箱已被注册',
ErrorCode::USERNAME_EXISTS => '用户名已被注册',
ErrorCode::PASSWORD_SAVE => '保存密码失败',
ErrorCode::EMAIL_CODE => '验证码不正确',
ErrorCode::INBOX_UPDATE_FAILED => '删除失败',
ErrorCode::NETWORK_BAD => '网络超时,请重试',
ErrorCode::HOTFIX_NOT_FOUND => '没有可使用的补丁',
ErrorCode::BLOCK_FAILED => '保存黑名单失败',
```

## 推送提示

```
默认提示：'You have received a message.'
Tom看了你的免费消息： 'Tom viewed your message'
Tom看了你的付费消息: 'Tome viewed your message for 100 coins'
Tom发了一条新消息： 'Tom just sent you a message!'
Tom回复了消息: 'Tom just sent you a reply!'
```

