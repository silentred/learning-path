# kubeadm

## Ubuntu 16.04

```
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF > /etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt-get update
# Install docker if you don't have it already.
apt-get install -y docker.io
apt-get install -y kubelet kubeadm kubectl kubernetes-cni
```
## Centos 7

```
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=http://yum.kubernetes.io/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg
       https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF
setenforce 0
yum install -y docker kubelet kubeadm kubectl kubernetes-cni
systemctl enable docker && systemctl start docker
systemctl enable kubelet && systemctl start kubelet
```

## 操作

```
master# kubeadm init
node1# kubeadm join --token=311971.7260777a25d70ac8 45.55.11.138

# if forget token, run:
kubectl -n kube-system get secret clusterinfo -o yaml | grep token-map | awk '{print $2}' | base64 -d | sed "s|{||g;s|}||g;s|:|.|g;s/\"//g;" | xargs echo

对于v1.6.0不适用了，可能是secret改变了名称; 目前在 bootstrap-token.token-id 和 bootstrap-token.token-secret 中
kubectl -n kube-system get secret bootstrap-token-db4706 -o yaml | grep 'token-id|token-secret' | awk '{print $2}' | base64 -d

db4706.517accfc0a418a16

kubectl -n kube-system get secret bootstrap-token-db4706 -o yaml | grep -E "token-id|token-secret" | awk '{print $2}' | while read line; do echo $line | base64 --decode | awk '{print $1}'; done | tr '\n' '.' | awk '{print $1"\n"}'
```

在master运行init之后，可能会遇到 kube-dns起不来的情况，错误日志为：

```
Error syncing pod, skipping: failed to "SetupNetwork" for "kube-dns-2924299975-pg7p8_kube-system" with SetupNetworkError: "Failed to setup network for pod \"kube-dns-2924299975-pg7p8_kube-system(d3e52b68-fc28-11e6-b98a-1a8821bd5ed6)\" using network plugins \"cni\": cni config unintialized; Skipping pod"
```

这时可以运行来解决：
kubectl apply -f https://git.io/weave-kube

kubectl apply -f https://git.io/weave-kube-1.6

weave net 是CNI 的一种，和flannel类似。

# CPU不足的情况下，会创建多个 Kube-dns pod 失败，删除失败的pod：
kubectl get pods --all-namespaces --show-all | grep OutOfcpu | awk -F ' ' '{print $2}' | xargs kubectl delete -n=kube-system pod


```
# 为前端机器打标签
kubectl label node centos-1gb-sfo2-01-node2 role=frontend
kubectl label node centos-1gb-sfo2-01-node2 k8s-app=traefik-ingress-lb

# for calico v2.0; kubeadm默认会打上这个label，所以可以不用执行
# kubectl label node ubuntu-512mb-sfo1-01 kubeadm.alpha.kubernetes.io/role=master


# 部署 calico
kubectl apply -f http://docs.projectcalico.org/v2.0/getting-started/kubernetes/installation/hosted/kubeadm/calico.yaml

# for 1.6 
kubectl apply -f http://docs.projectcalico.org/v2.1/getting-started/kubernetes/installation/hosted/kubeadm/1.6/calico.yaml


```


# Bug

```
vi /etc/systemd/system/kubelet.service.d/10-kubeadm.conf 
添加  --cgroup-driver=systemd
sudo systemctl daemon-reload && sudo systemctl restart kubelet.service

# 另开一个 session
mkdir .kube
cp /etc/kubernetes/admin.conf .kube/config
curl -sSL https://rawgit.com/coreos/flannel/master/Documentation/kube-flannel.yml | kubectl create -f -
```

# kubelet auth

```
vim /etc/systemd/system/kubelet.service.d/10-kubeadm.conf

add --authentication-token-webhook argument for kubelet
这个参数的解释： Use the TokenReview API to determine authentication for bearer tokens.

sudo systemctl daemon-reload && sudo systemctl restart kubelet.service
```
这样 kubelet:10250 端口会用 beaer token 作为验证


关于验证，还需要注意 deployment 的 service account 是否被绑定了 role， 参考 rolebinding.yaml


# Node failure

如果节点挂了，controller manager 会负责把pod重新调度到其他节点 (先 evict, 在 bind), 启动参数中有:

```
--node-eviction-rate float32

Number of nodes per second on which pods are deleted in case of node failure when a zone is healthy (see --unhealthy-zone-threshold for definition of healthy/unhealthy). Zone refers to entire cluster in non-multizone clusters. (default 0.1)

--pod-eviction-timeout duration

The grace period for deleting pods on failed nodes. (default 5m0s)

```

# check route list

```
# ip route list

root@iZ2zegw6nmd5t5qxy35lh0Z:~# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         47.93.163.247   0.0.0.0         UG    0      0        0 eth1
10.0.0.0        10.30.251.247   255.0.0.0       UG    0      0        0 eth0 // this one 
10.30.248.0     0.0.0.0         255.255.252.0   U     0      0        0 eth0
47.93.160.0     0.0.0.0         255.255.252.0   U     0      0        0 eth1
100.64.0.0      10.30.251.247   255.192.0.0     UG    0      0        0 eth0
172.16.0.0      10.30.251.247   255.240.0.0     UG    0      0        0 eth0
172.17.0.0      0.0.0.0         255.255.255.0   U     0      0        0 docker0
192.168.31.128  0.0.0.0         255.255.255.192 U     0      0        0 *
```

根据参数删除某一条规则:

```
// del
route del -net 10.0.0.0 gw 10.27.219.247 netmask 255.0.0.0 dev eth0
route del -net 10.0.0.0 gw 10.30.251.247 netmask 255.0.0.0 dev eth0

// add
route del -net 10.30.0.0 gw 10.27.219.247 netmask 255.255.0.0 dev eth0
route add -net 10.27.0.0 gw 10.30.251.247 netmask 255.255.0.0 dev eth0

```
