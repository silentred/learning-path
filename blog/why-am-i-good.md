您好:

我叫汪扬，很高兴在今年的 gopherchina 再次看到了 Grab 团队。高超老师的演讲非常精彩，我在会后和高老师聊了下 opentracing 的存储问题, 还有 serverless 的实现。结合演讲中的介绍，感觉 Grab 是一个技术驱动的公司，我非常喜欢这样有技术氛围的公司。以下是我自认为的一些优势。

参与开源:

1. TiDB: 提交内容为 mysql 内置函数的实现，大约提交了4个左右。
2. MQTT Broker: 公司在使用一个 nodejs 的开源版本，读完协议后，忍不住写了一个单机版的 Go 实现，打算参考 bilibili/goim 的实现扩展为分布式的应用，很惭愧一直没有时间做。
3. Web 开发框架: 公司需要一个统一的 api 开发工具，主要处理 依赖注入，配置，Log，数据库，中间件，测试(配合DI实现)
4. Micro-service 框架: 利用etcd作为服务发现，grpc 负载均衡, 中间件(tracing, auth), HTTP协议转换, 和会上ezbuy的架构有些类似。
5. Worker/Consumer 框架: 队列消费者，凑巧也用了 Harbor的演讲者 在会议上说的 worker pool 的模型
6. K8S Tutorial: 自己研究了一套 K8S 部署微服务的架构，包括 路由自动发现注册，日志自动收集，监控。
7. Chatroom 玩具: 一个 websocket 的聊天服务器，无聊时的产物

以上项目都在我的 [github](https://github.com/silentred)

阅读:

阅读源码是兴趣使然的事，通常是对某部分实现感兴趣，包含但不限于以下项目, redis , bilibili/bfs, bilibili/goim, leveldb, baidu/bfs。
还有就是阅读论文，这方面相对少一些，去年读过 raft, facebook Haystack, 这两个项目都尝试在 github 上提交了一些代码，很遗憾都没有完全实现。

英文熟练:

长期使用google，技术问题只用英文搜索。
stackoverflow 上有122分。
前年因为对ios开发感兴趣，翻译了swift语言的教程。
kubernetes team slack上积极参与提问。kubeadm v1.6.0 风波; calico/node 风波 都是在 github 提 issue 解决的。
领域知识内的口语也还可以。

博客:

[segmentfault](https://segmentfault.com/blog/silentred) 上有几篇拙文

比较希望能从事有创新性，有挑战的工作，例如 分布式应用，中间件等。
希望周围能有非常优秀的同事，向他们多学习，在技术驱动的公司快乐的编程。
听说 Grab team 会 review 开发者的每一行代码，这也是我对贵公司心仪的重要原因。

