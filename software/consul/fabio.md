# fabio 使用

fabio 和 consul 结合比较紧密，流程为：

1. service在启动时向 consul 注册自己的信息，上报的 service 信息有一定的结构。包含 serviceID, ip:port, 等信息。 service会把自身的转发 prefix 放在tags中，一起上报给 consul.
可以结合 registrator ？ fabio 文档中好像有提到。

2. fabio 根据发现的服务，更新 config, 这个config同样存在 consul kv中。服务根据 serviceID来区分， 同一个serviceID被认为是一个服务，那么一个服务启动的多个容器就会被负载均衡。


## 部署方案

flannel 打通节点docker，那么每个容器服务只需要在启动时上报正确的 ip:port, 就可以了。

consul的service结构，定义了 ip , port，tags. 并且提供 DNS 来根据tag查询服务的ip和port。

例如，一个服务 127.0.0.1:5000 tags=urlprefix-/foo,svc-a , 这个服务包含了两个 tag, 其中一个为 svc-a, 
那么查询DNS的时候 `dig @localhost -p 8600 svc-a.service.consul SRV` 就能查到所有的svc



其次，服务发现需要根据
