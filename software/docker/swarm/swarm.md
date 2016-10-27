## create image
docker build -t jason/hello:v1 .

## test
docker run -P -d jason/hello:v1
docker ps -a

## run swarm
docker swarm init
docker service create --publish 9090:9090 --name hello-service jason/hello:v1

