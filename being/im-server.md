# IM server

10w client 对应 3.8G 内存
32G 内存的机器，大约 50 - 60 w 连接

系统开销 一个连接大约是 2k, 

50w 大约是 1000 000 k, 1G 系统开销，加上内存碎片，乘以3，大约3G

32-3 = 29G

3.8 x 5 = 20 G

3000 => nsqd 1400 MB
10 => 36 MB

nsqd 消耗内存太多，不适合用在多 topic, 多client的场景


查一下 kafka 内存消耗如何？


如果一个comet 就一个 consumer?



每个 comet 一个ID， 对应一个 topic, 例如cometID = "C001", 那么他订阅topic "IM/C001", channel 为 "Game" (App 名称)

当有用户连接时，用户传入他的ID， 例如 "100101", 那么他需要去 KV 更新他登录了哪台 comet, 这样router 才能知道push到哪个topic,也就是哪台comet.

单聊：
A 发送给 B, 请求到了 router, router 去KV找 B当前的在线状态，如果在线，B在哪台comet, 假设找到 "C001", 他就把消息push 到 "IM/C001" 去

群聊：
A 发送给 Group001, 请求到了router, router去KV找，Group001当前有哪些人，找到了100个人，在去KV 找这100人分别在哪些 comet 上，例如，发现有 10 人在 "C001", 50 人在 "C002", 40人在"C003", 那么就把3条消息+ group信息，发给三台comet, comet收到的信息包含了消息body和group信息，comet拥有当前连接用户group 信息， group001 => [1001, 1002, 1003, ...] 这样的映射

接收用户不在线：
以上两种情况，有可能接收不在线，那么，就把这条消息存到 KV的用户session中，用户下次登录时，会按顺序去把消息推给用户。


// 收款付款的系统：
先扣款，后加款。

扣款



用户默认订阅的 topic: user/1230110 (uid)
例如， 1001 给 1002 发消息，就发送消息到 topic: user/1002

group/001 (group ID)
用户订阅的群topic
1001 发送消息到群 , 就是发送消息到 topic: group/0001

username = app-{uid}
用户登录时，需要提供 username, 这个必须和用户ID 相关，例如





