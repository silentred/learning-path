# Registrator

## Quick Start

## Run Reference


安装 consul, 如果检测到多个 private ip, 会报错，可以用 -advertise 指定一个ip

sudo docker run -d --name=consul --net=host gliderlabs/consul-server -bootstrap -advertise=172.28.128.3

curl 172.28.128.3:8500/v1/catalog/services

sudo docker run -d --name=registrator --volume=/var/run/docker.sock:/tmp/docker.sock gliderlabs/registrator:latest -ip=172.28.128.3 consul://172.28.128.3:8500 

sudo docker run -d -P -e SERVICE_9090_CHECK_HTTP=/foo/healthcheck -e SERVICE_9090_NAME=hello -e SERVICE_CHECK_INTERVAL=10s -e SERVICE_CHECK_TIMEOUT=5s -e SERVICE_TAGS=urlprefix-/foo,hello silentred/alpine-hello:v2

curl 172.28.128.3:8500/v1/catalog/services

# 测试 DNS
sudo yum install bind-utils

dig @172.28.128.3 -p 8600 hello.service.consul SRV