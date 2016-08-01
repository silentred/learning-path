# Worker Architecture

## API

- 负责发现worker服务的 ip:port，根据请求的 key， 去寻找当前是否有对应的worker服务。
这样各种类型的 event , 都请求到这里，由 API 分发。
- Http 接口，接收event data. 转发给对应的worker
- 对于同一类worker的多个实例，使用负载均衡（random, round robin）

## Worker

- Http 接口，接受 event data, 格式化为Job后 push 到本地的queue中
- 从 本地queue 中消费Job
- 上报 http 接口的 ip:port 给registry，API可以感知，这样增减worker实例都能实时生效。
- 提供一个 检测 worker 状态的端口, 例如：负载，queue中任务数


Level 1: Nginx
Level 2: API，作为 Gateway, 也可以自由扩展
Level 3: Worker 接受 event data,


# 进化路线

1. 先实现worker. mqtt-worker, apns-worker, gcm-worker