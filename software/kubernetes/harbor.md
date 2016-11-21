# Harbor

# install epel

yum install epel-release

# install pip for docker-compose

yum install python-pip -y

# download 
wget -c https://github.com/vmware/harbor/releases/download/0.4.5/harbor-offline-installer-0.4.5.tgz

# config

open harbor.cfg

hostname = 119.254.102.192 (或者 domain)

# Prerequisites
python, pip, docker, docker-compose

# install harbor
./install.sh

# visit web ui
http://119.254.102.192
创建user : jason
创建project: libs

# push
需要重启 dockerd, 加上 --insecure-registry="119.254.102.192", 否则当 login 的时候，会用https去访问

docker login 119.254.102.192 -u jason -p Jason123

docker tag bash:latest 119.254.102.192/libs/bash:v1

docker push 119.254.102.192/libs/bash:v1



