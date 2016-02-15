## connection
session
will


## pub/sub

http://www.hivemq.com/blog/mqtt-essentials-part2-publish-subscribe

> Of course the broker is able to store messages for clients that are not online. (This requires two conditions: client has connected once and its session is persistent and it has subscribed to a topic with Quality of Service greater than 0)

broker保存消息的几个前提：
1. 客户端连接过，session是persistent的
2. 订阅过 QoS大于0的topic


## topic

- single
- star
- $SYS

## Qos


