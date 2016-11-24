# Usage of consul

$ consul agent -dev // 如果启动一个单点实例，必须加 -dev , 否则会报错

$ consul members -detailed

Node   Address             Status  Type    Build  Protocol  DC
bogon  192.168.1.100:8301  alive   server  0.6.4  2         dc1

$ tmp curl localhost:8500/v1/catalog/nodes
[{"Node":"bogon","Address":"192.168.1.100","TaggedAddresses":{"wan":"192.168.1.100"},"CreateIndex":3,"ModifyIndex":4}]

$ dig @127.0.0.1 -p 8600 bogon.node.consul

$ echo '{"service": {"name": "web", "tags": ["rails"], "port": 80}}' > consul.d/config.json
$ consul agent -dev -config-dir=./consul.d

$ dig @127.0.0.1 -p 8600 web.service.consul
TAG.NAME.service.consul
$ dig @127.0.0.1 -p 8600 rails.web.service.consul SRV


$ curl http://localhost:8500/v1/catalog/service/web
$ curl 'http://localhost:8500/v1/health/service/web?passing'

$ echo '{"check": {"name": "ping", "script": "ping -c1 baidu.com >/dev/null", "interval": "10s"}}' > consule.d/ping.json

echo '{"service": {"name": "web", "tags": ["rails"], "port": 80, "check": {"script": "curl localhost >/dev/null 2>&1", "interval": "10s"}}}' > consul.d/config.json

$ curl http://localhost:8500/v1/health/state/critical


## UI
$ consul agent -ui -ui-dir=consul_0.6.4_web_ui -data-dir=consul_0.6.4_web_ui