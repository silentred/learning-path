# 基于容器的后端服务架构

> 在探索kubernetes的应用时，调研了几个gateway，发现fabio支持发现服务，自动生成路由，结合consul，registrator, 可以很容易的部署一套服务，比较轻量，很容易玩起来。

结构大致为：


## Start Consul

安装 consul, 如果检测到多个 private ip, 会报错，可以用 -advertise 指定一个ip.
```
sudo docker run -d --name=consul --net=host gliderlabs/consul-server -bootstrap -advertise=172.28.128.3 -ui

curl 172.28.128.3:8500/v1/catalog/services
```

## Start Registrator

启动 registrator, 因为需要调用docker api， 所以需要把docker.sock 映射到容器内部，如果你使用了tcp， 那么需要设置对应的url。 

如果你希望上报容器内部ip:port, 那么需要在启动参数中加入 `-internal=true`, 这样注册的 Service, 都是容器内部的ip, 而port对于同一个service而言，一般是固定的，例如 一个hello服务的两个实例分别为 10.10.1.12:9090, 10.10.1.13:9090. 这样的话，就需要配置一个容器跨host的网络方案，例如 flannel, 等。 可以参考上一篇 [Flannel with Docker](https://segmentfault.com/a/1190000007585313)

为了简便测试，这里就不配置flannel了。`-ip`是指定注册service时候使用的ip，建议要指定，选取当前机器的内网 private ip即可。我这里是 `172.28.128.3`.

```
sudo docker run -d --name=registrator --volume=/var/run/docker.sock:/tmp/docker.sock gliderlabs/registrator:latest -ip=172.28.128.3 consul://172.28.128.3:8500 
```

## Start service

启动服务，这里需要注意的是这些环境变量，作用是 override Registrator的默认值，见名知意，在 registrator 文档中有详细介绍。例如 `SERVICE_9090_NAME` 就是指 端口为 9090 的service 的 name。

需要注意的是 tags 这个字段，`urlprefix-/foo,hello`, 这里 `urlprefix-` 是 gateway 的一种配置，意思为 把访问 /foo 为前缀的请求转发到当前应用来。他能够匹配到例如 `/foo/bar`, `footest`, 等。如果你想加上域名的限制，可以这样 `urlprefix-mysite.com/foo`。 后面还有一个 `hello`, 作用是给这个service打一个标记，可以用作查询用。

```
sudo docker run -d -P -e SERVICE_9090_CHECK_HTTP=/foo/healthcheck -e SERVICE_9090_NAME=hello -e SERVICE_CHECK_INTERVAL=10s -e SERVICE_CHECK_TIMEOUT=5s -e SERVICE_TAGS=urlprefix-/foo,hello silentred/alpine-hello:v2

curl 172.28.128.3:8500/v1/catalog/services
//现在应该能看到刚启动的hello服务了
{"consul":[],"hello":["urlprefix-mysite.com/foo","hello","urlprefix-/foo"]}
```

测试 DNS
```
sudo yum install bind-utils
dig @172.28.128.3 -p 8600 hello.service.consul SRV
```

## Start Gateway

前端Gateway 根据 consul中注册的 service，生成对应的路由规则，把流量分发到各个节点。 这个项目还有一个 ui 管理 route信息，端口为 9998。

创建一个配置文件 fabio.properties
```
registry.consul.addr = 172.28.128.3:8500
```
在当前目录运行
```
docker run -d -p 9999:9999 -p 9998:9998 -v $PWD/fabio.properties:/etc/fabio/fabio.properties magiconair/fabio
```

## Health Check

```
sudo ifdown eth1

curl http://localhost:8500/v1/health/state/critical

[
    {
        "Node":"localhost.localdomain",
        "CheckID":"service:afa2769cd049:loving_shannon:9090",
        "Name":"Service 'hello' check",
        "Status":"critical",
        "Notes":"",
        "Output":"Get http://172.28.128.6:32768/foo/healthcheck: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)",
        "ServiceID":"afa2769cd049:loving_shannon:9090",
        "ServiceName":"hello",
        "CreateIndex":379,
        "ModifyIndex":457
    }
]

sudo ifup eth1
```

在启动 consul的时候，我们使用了`-ui` 参数，我们可以在 `172.28.128.3:8500/ui` 访问到consul的web ui管理界面，看到各个服务的状态.

## 对比

注册容器外IP：
每个注册的service的port都是变化的，并且因为映射内部port到了host，外部可以随意访问，私密性较弱。

注册容器内IP：
每个注册的service的port都是固定的，只能从容器内部访问。如果用 flannel，可能有一些性能损失。
