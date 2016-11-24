# fabio 使用

fabio 和 consul 结合比较紧密，流程为：

1. service在启动时向 consul 注册自己的信息，上报的 service 信息有一定的结构。包含 serviceID, ip:port, 等信息。 service会把自身的转发 prefix 放在tags中，一起上报给 consul.
可以结合 registrator ？ fabio 文档中好像有提到。

2. fabio 根据发现的服务，更新 config, 这个config同样存在 consul kv中。服务根据 serviceID来区分， 同一个serviceID被认为是一个服务，那么一个服务启动的多个容器就会被负载均衡。


## 部署方案

flannel 打通节点docker，那么每个容器服务只需要在启动时上报正确的 ip:port, 就可以了。
