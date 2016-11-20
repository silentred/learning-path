# Flannel Test

# Vagrant file

设置为NAT 网络：
config.vm.network "private_network", type: "dhcp"
这样两台虚拟机可以互通

# 切换ali apt源

vim /etc/apt/source.list

deb http://mirrors.aliyun.com/ubuntu/ vivid main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ vivid-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ vivid-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ vivid-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ vivid-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ vivid main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ vivid-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ vivid-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ vivid-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ vivid-backports main restricted universe multiverse

更新看看速度：
sudo apt-get update
sudo apt-get upgrade

# install git

sudo apt-get install git

# install go

# compile flannel
make dist/flanneld

# install docker

sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

echo "deb https://apt.dockerproject.org/repo ubuntu-precise main" | sudo tee /etc/apt/sources.list.d/docker.list

sudo apt-get update
sudo apt-get install docker-engine

# install etcd
curl -L  https://github.com/coreos/etcd/releases/download/v2.1.0-rc.0/etcd-v2.1.0-rc.0-linux-amd64.tar.gz -o etcd-v2.1.0-rc.0-linux-amd64.tar.gz

etcd --listen-client-urls 'http://0.0.0.0:2379,http://0.0.0.0:4001' --advertise-client-urls 'http://172.28.128.3:2379,http://172.28.128.3:4001'  > /dev/null 2>&1


# delete docker0 iface
(如果这里选择删除docker0， 那么下面启动dockerd之前 设置docker0的ip就可以省略。 dockerd会根据bip再次创建一个docker0, 效果一样)
sudo ifconfig docker0 down
sudo brctl delbr docker0

# set flannel config in etcd

etcdctl rm /coreos.com/network/ --recursive
etcdctl mk /coreos.com/network/config '{"Network":"11.0.0.0/16"}'

# start flannel
sudo flanneld -etcd-endpoints='http://172.28.128.3:2379,http://172.28.128.3:4001' -iface=eth1 &

source /run/flannel/subnet.env

# start docker

sudo ifconfig docker0 ${FLANNEL_SUBNET}
sudo dockerd --bip=${FLANNEL_SUBNET} --mtu=${FLANNEL_MTU} &

# new container
sudo docker run -it bash


# dockerd 中有一些令人在意的参数
```
--registry-mirror=[]                     Preferred Docker registry mirror
-s, --storage-driver                     Storage driver to use
```


