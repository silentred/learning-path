# Docker with Flannel

> Flannel 是用于组建容器间通信的网络的工具，用于解决跨主机的docker containers之间的连通性问题。最近在尝试手动部署kubernetes集群，这是这个系列的第一篇。

## 准备工作

首先安装vagrant, 用来创建虚拟节点。我们需要两台虚拟机. 

Vagrantfile 如下：
```
Vagrant.configure(2) do |config|
  config.vm.box = "centos/7"
  config.vm.network "private_network", type: "dhcp"
  vb.memory = "1024"
end
```
 
创建一个 centos 目录，把 Vagrantfile 放置其中，运行:
```
vagrant up
vagrant ssh
```

进入后，可以先更新一下 yum源，yum makecache, yum update 一下。ip addr 看下本机的ip。

另一台虚拟机的过程类似。

两台ip分别为： 172.28.128.3， 172.28.128.4

## 安装 Docker

docker官网有详细的步骤，大致如下：

```
$ sudo tee /etc/yum.repos.d/docker.repo <<-'EOF'
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/7/
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
EOF

$ sudo yum install docker-engine

$ sudo systemctl enable docker.service

$ sudo systemctl start docker
```

确认安装完成: `sudo docker version`, 然后关闭 dockerd, `sudo systemctl stop docker.service`

## 安装 golang 编译环境

编译 flannel 会需要，如果你的vagrant 使用了host的共享目录，那么这个步骤只需要在其中一台虚拟机执行就行，第二台虚拟机直接拷贝文件就可以了。 如果你的host机有golang的编译环境，直接在host编译即可，记得使用 GOOS=linux GOARCH=amd64 作为编译时候的环境变量。

如果你选择在虚拟机中编译，那么内存最好设置为 2G.

```
wget -c https://storage.googleapis.com/golang/go1.7.3.linux-amd64.tar.gz
tar xf go1.7.3.linux-amd64.tar.gz
```

把解压出来的 go 目录放到合适的位置，并把 go/bin 加入 PATH 环境变量, 并设置 GOPATH 环境变量。

## 安装 Flannel

```
$ sudo yum install linux-libc-dev gcc
$ git clone https://github.com/coreos/flannel
$ cd flannel
$ make dist/flanneld
```
编译完成后的文件在 dist 目录中, 可以拷贝到 /usr/local/bin/ 下

## 安装 etcd

```
$ curl -L  https://github.com/coreos/etcd/releases/download/v3.0.15/etcd-v3.0.15-linux-amd64.tar.gz

$ tar xf etcd-v3.0.15-linux-amd64.tar.gz
```
把 etcd, etcdctl 拷贝到 /usr/local/bin 下

## 运行

IP: 172.28.128.3 

首先运行etcd: `$ etcd --listen-client-urls 'http://0.0.0.0:2379,http://0.0.0.0:4001' --advertise-client-urls 'http://172.28.128.3:2379,http://172.28.128.3:4001'  >/dev/null 2>&1`

设置flannel子网范围：
```
etcdctl rm /coreos.com/network/ --recursive
etcdctl mk /coreos.com/network/config '{"Network":"11.0.0.0/16"}'
```

IP: 172.28.128.3, 172.28.128.4 两台机器

ifconfig 查看一下，ip为172.28.128.3 的 interface 的名称，我的情况为 eth1. 运行 flannel. subnet.env是根据 etcd中的配置自动生成的环境变量，需要导出一下.
```
sudo flanneld -etcd-endpoints='http://172.28.128.3:2379,http://172.28.128.3:4001' -iface=eth1 &
source /run/flannel/subnet.env
```

修改docker0 网络的ip, 并开启 dockerd
```
sudo ifconfig docker0 ${FLANNEL_SUBNET}
sudo dockerd --bip=${FLANNEL_SUBNET} --mtu=${FLANNEL_MTU} &
```

## 测试连通性

在两台机器上分别 `sudo docker run -it bash`

进入bash后，ip addr 查看各自ip，互相 ping 一下对方的ip，应该是可以ping通的。

