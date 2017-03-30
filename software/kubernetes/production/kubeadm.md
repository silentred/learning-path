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
```

在master运行init之后，可能会遇到 kube-dns起不来的情况，错误日志为：

```
Error syncing pod, skipping: failed to "SetupNetwork" for "kube-dns-2924299975-pg7p8_kube-system" with SetupNetworkError: "Failed to setup network for pod \"kube-dns-2924299975-pg7p8_kube-system(d3e52b68-fc28-11e6-b98a-1a8821bd5ed6)\" using network plugins \"cni\": cni config unintialized; Skipping pod"
```

这时可以运行来解决：
kubectl apply -f https://git.io/weave-kube

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


```


# Bug

```
/etc/systemd/system/kubelet.service.d/10-kubeadm.conf

暂时删除 
Environment="KUBELET_NETWORK_ARGS=--network-plugin=cni --cni-conf-dir=/etc/cni/net.d --cni-bin-dir=/opt/cni/bin"

添加 
--cgroup-driver=systemd

sudo systemctl daemon-reload && sudo systemctl restart kubelet.service
```
但是apiserver 还是起不来，不知道原因
