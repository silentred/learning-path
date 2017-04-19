# Fabio 

## 功能

- 支持协议: http, https, websocket, tcp, tcp+sni
- 支持 host, prefix 的路由区分
- 支持权重，tag区分后端服务
- 路由信息支持 file, static, consul
- 统计信息 (Circonus, Graphite, StatsD, DataDog)
- 简单web admin

代码量比较小, 代码比较清晰，容易理解. 目前不支持 k8s ingress. 

---

# traefik

## 功能

- http, https, websocket
- basic auth; digest auth; 
- 支持 host, prefix 的路由区分; 正则; url rewrite
- 熔断器, 负载均衡
- 统计信息
- web admin
- 端口探活

代码量大，抽象比较多，不容易二次开发。

---

# Tyk

## 功能

- 支持http, https, websocket
- 安全验证(basic auth; token; 等)
- 速率限制(redis, mem; quota)，大小限制
- 请求，返回改写(header, body), url rewirte
- 缓存
- 服务发现： etcd, consul, mesos, eruka
- 负载均衡，熔断( %x 访问 /path 失败，则 y 时间内不请求后端 ), 探活统计
- 监控，事件，webhook
- 日志接口(sentry, logstash, graylog, syslog)
- 插件: python, lua


付费

---

# 阿里云

## 功能

- 支持 http, https
- 监控（调用量、流量、响应时间、错误分布），告警，流控
- 校验; 参数映射（API级别）
- 不支持body修改

请求 header 必须包含 X-Ca-Key, X-Ca-Signature;
并发限制: 单用户QPS峰值不超过100，API调用单IP不超过100QPS;

付费

