The immediate and mandatory fields are part of the AMQP specification, and are also covered in the RabbitMQ FAQ to clarify how its implementers interpreted their meaning:

Mandatory

This flag tells the server how to react if a message cannot be routed to a queue. Specifically, if mandatory is set and after running the bindings the message was placed on zero queues then the message is returned to the sender (with a basic.return). If mandatory had not been set under the same circumstances the server would silently drop the message.
Or in my words, "Put this message on at least one queue. If you can't, send it back to me."

Immediate

For a message published with immediate set, if a matching queue has ready consumers then one of them will have the message routed to it. If the lucky consumer crashes before ack'ing receipt the message will be requeued and/or delivered to other consumers on that queue (if there's no crash the messaged is ack'ed and it's all done as per normal). If, however, a matching queue has zero ready consumers the message will not be enqueued for subsequent redelivery on from that queue. Only if all of the matching queues have no ready consumers that the message is returned to the sender (via basic.return).
Or in my words, "If there is at least one consumer connected to my queue that can take delivery of a message right this moment, deliver this message to them immediately. If there are no consumers connected then there's no point in having my message consumed later and they'll never see it. They snooze, they lose."

http://www.rabbitmq.com/amqp-0-9-1-reference.html#domain.no-local

1 exchange to multiple queue

exchange type: 
1. fanout: 无脑发送到各个queue
2. direct: bind queue 时候指定 routing-key, 发送的时候传什么 routing-key 就发送到对应的 queue
3. topic: 通配符 #, *, 发送到匹配到的 queue

标志：
no-local: server 不向 sender 发送消息
no-wait: 发送消息，server不返回内容，如果出错，server抛出异常
exclusive: Exclusive queues may only be accessed by the current connection, and are deleted when that connection closes. Passive declaration of an exclusive queue by other connections are not allowed.

The server MUST support both exclusive (private) and non-exclusive (shared) queues.