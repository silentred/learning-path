app绑定微信时的问题

假设场景：

1. A在微信，app分别注册了账号，分别发布来玩法，分别产生了交易。此时A点击了App中的”绑定微信“按钮。会发生什么？

按照目前user表的来看，绑定前数据库中是这样的

用户表
uid    unionid    username    password
1      ''         from-app    xxxx
2      xx_abcd    from-wechat 1234


玩法表
id    uid    title
1     1      玩法1-来自app
2     2      玩法2-来自微信


交易表
id    servicer_id    consumer_id     object_id
1     1              99              1
2     2              98              2


方案一：

用户表
uid    unionid    username    password
1      xx_abcd    from-app    xxxx
2      ''         from-wechat 1234

登陆时候，微博和app都会登陆用户1.
但是，这种方式切断了用户 1，2的关联（不可逆），而且必须修改 玩法表， 交易表 来保证历史玩法和交易存在（这些操作必须放在一个事务中操作），`不建议`使用。



方案二：

用户表
uid    unionid    username    password    is_active
1      xx_abcd    from-app    xxxx        1
2      xx_abcd    from-wechat 1234        0

用户1，2通过unionid来关联，登陆的时候判断 is_active，来确定登陆用户1.
public玩法列表中，就需要判断发布者的 is_active，如果是0，就要通过 unionid 去找 is_active 为1的用户，也就是 用户1. 展示出来。这样别人购买，都是和app上的用户1进行交互。

个人主页的列表，用户1根据自己的unionid不为空可以判断自己已经绑定了微信，可以把 uid为1，2的玩法都取出来。

已经完成的历史订单，展示的时候用户1，2的信息都是完整的，没有问题。
正在交易的订单，展示的用户不变，交易状态的改变时的通知，根据各自的平台来决定。微信的逻辑（模板消息，客服消息，短信）

未来产生的订单，需要制定不同平台的用户的交流模式，暂时可以不考虑。







