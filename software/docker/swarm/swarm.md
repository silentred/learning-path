## create image
docker build -t jason/hello:v1 .

## test
docker run -P -d jason/hello:v1
docker ps -a

## run swarm
docker swarm init
docker service create --publish 9090:9090 --name hello-service jason/hello:v1


## 不使用集群管理工具

### 手动指定 Host Address
docker run -p 9090:9090 -d image:tag --host xxx 

### docker API 获取 port 信息
docker run -P -d image:tag --host xxx
或者 host 可以 从 ENV 传入容器内，一台物理机只需要配置一次 env

## 使用 k8s

