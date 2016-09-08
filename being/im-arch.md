# IM Server 架构

## 组件
Comet (客户端连接), Logic (业务处理), Router (消息分发)

## Comet
- 负责连接客户端，需要实现 mqtt 协议 (sub/pub)； websocket，自定义cmd来实现 sub/pub.
- pub 的消息 通过 rpc 交给 logic 做修改 (敏感词过滤, 等)，最终push到 Queue 中，作为缓冲。
- 上报 comet_ip 和 topic 信息给 router
- 接收 router push来的message, 并根据 message 的topic，把消息分发给各个 client
- comet 只维护本机连接的client, topic, 所以支持水平扩展。给客户端提供接口查询可用ip, 客户端根据ping值选择连接
- 当本机订阅topic变化时，需要 上报 router。
- comet 故障时，及时通知 router， 可以借助 etcd

cleanSession=0 时，如何保存 user session? 历史消息如何保存; 下次登陆到其他comet上，session 如何转移
- user 退出登陆后，如果cleanSession=0, 则在本地新建一个user_offline_file, 记录离线消息, 向 Logic 注册离线时间，cometID。定时清理 user 和 offline_file。
- user 再次登陆时，向 Logic 询问 上次登陆的 cometID, ip。向之前的 comet 请求转移 user session. 

## Logic
- RPC server, 业务逻辑，修改 message (from user, message qos, message body, to topic)
- RPC 鉴权
- RPC 保存 user 登陆的信息 （登陆哪台机器，登陆时间，等）, 外部存储 redis

## Router
- 接受 Queue 中的message, 根据 msg.topic 分发到对应的 comet.
- 接受 comet 的信息上报，记录 哪些 comet_ip 对应哪些 topic
- 通过监听 etcd 上 services/comets 节点的变化，来及时的删除 comet 节点. 
- router 需要维护 topic[comet_ip] 这个 map, 如果需要水平扩展，则需要借助 raft 协议实现。

## Roadmap

### Step I
- comet 实现 mqtt 最简部分, qos=0, topic 不支持通配符, cleanSession=true
- router 单机部署

### Following Steps
- comet 实现 mqtt 全部协议
- router 应用 raft


> 参考b站 [goim 项目](https://github.com/Terry-Mao/goim), [文章](https://mp.weixin.qq.com/s?__biz=MjM5NzAwNDI4Mg==&mid=2652190998&idx=1&sn=5023e23660ede074c9eb48e166a8faf3&scene=4&uin=NjUwNjA2Njgx&key=305bc10ec50ec19b3be7fc02fb1e31e65fe4d6d9316142020c045362c0e1eafd1a78d57247eb2bc8dd1c23751e1e79de&devicetype=iMac+MacBookAir7%2C1+OSX+OSX+10.11.5+build(15F34)&version=11020201&lang=zh_CN&pass_ticket=jg6FcNlzsgy4ssoPzjNwvKBBxc05AQJUdzQP2P5PCP6XzqP%2FkXdem%2BzEuy7wuzDg)


