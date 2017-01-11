k8s-with-systemd.md

# Apiserver

```
启动命令
hyperkube apiserver \
--bind-address=0.0.0.0 \
--insecure-bind-address=127.0.0.1 \
--etcd-servers=http://192.168.0.2:2379 \
--allow-privileged=true \
--service-cluster-ip-range=10.10.0.0/16 \
--secure-port=443 \
--advertise-address=192.168.0.2 \
--admission-control=NamespaceLifecycle,LimitRanger,ServiceAccount,DefaultStorageClass,ResourceQuota \
--runtime-config=extensions/v1beta1/networkpolicies=true \
--tls-cert-file=/etc/kubernetes/ssl/apiserver.pem \
--tls-private-key-file=/etc/kubernetes/ssl/apiserver-key.pem \
--client-ca-file=/etc/kubernetes/ssl/ca.pem \
--token-auth-file=/etc/kubernetes/token \
--anonymous-auth=false \
> apiserver.log 2>&1 &

--kubelet-timeout=5s // 默认为5s, log里一直出现超时，设为 60s 试试; 没有用，现在是每60s出现一次panic log. 看来问题可能是在 kubelet 上。

/etc/kubernetes/token, 格式为 token,username,uid
1234token,kube-admin,kube-admin

访问如下：
// 使用 CA 签证的 公钥私钥组合
curl https://192.168.0.2/api/v1beta3/namespaces/default/pods -cert=/etc/kubernetes/ssl/admin.pem -key=/etc/kubernetes/ssl/admin-key.pem -H 'Authorization: Bearer 1234token'

// 使用 CA 公钥 访问
curl -H 'Authorization: Bearer 1234token' -v --cacert /etc/kubernetes/ssl/ca.pem https://192.168.0.2/api/v1beta3/namespaces/default/pods

[Service]
Environment=KUBELET_VERSION=v1.5.1
ExecStartPre=/usr/bin/mkdir -p /etc/kubernetes/ssl
ExecStartPre=/usr/bin/mkdir -p /etc/kubernetes/manifests
ExecStart=/usr/local/binhyperkube apiserver \
--bind-address=0.0.0.0 \
--insecure-bind-address=127.0.0.1 \
--etcd-servers=http://192.168.0.2:2379 \
--allow-privileged=true \
--service-cluster-ip-range=10.10.0.0/16 \
--secure-port=443 \
--advertise-address=192.168.0.2 \
--admission-control=NamespaceLifecycle,LimitRanger,ServiceAccount,DefaultStorageClass,ResourceQuota \
--tls-cert-file=/etc/kubernetes/ssl/apiserver.pem \
--tls-private-key-file=/etc/kubernetes/ssl/apiserver-key.pem \
--client-ca-file=/etc/kubernetes/ssl/ca.pem \
--runtime-config=extensions/v1beta1/networkpolicies=true \
--anonymous-auth=false 
Restart=always
RestartSec=10
```

# Controller

```
mkdir -p /etc/kubernetes/ca
cp /etc/kubernetes/ssl/ca.pem /etc/kubernetes/ca/ca.pem
cp /etc/kubernetes/ssl/ca-key.pem /etc/kubernetes/ca/ca.key

hyperkube controller-manager \
--master=http://127.0.0.1:8080 \
--leader-elect=true \
--service-account-private-key-file=/etc/kubernetes/ssl/apiserver-key.pem \
--root-ca-file=/etc/kubernetes/ssl/ca.pem \
> controller.log 2>&1 &
```

# Scheduler

```
hyperkube scheduler \
--master=http://127.0.0.1:8080 \
--leader-elect=true \
> scheduler.log 2>&1 &
```

# Kubelet

```
hyperkube kubelet \
  --api-servers=https://192.168.0.2 \
  --container-runtime=docker \
  --register-node=true \
  --allow-privileged=true \
  --hostname-override=192.168.0.4 \
  --cluster_dns=10.10.0.10 \
  --cluster_domain=cluster.local \
  --kubeconfig=/etc/kubernetes/worker-kubeconfig.yaml \
  --tls-cert-file=/etc/kubernetes/ssl/worker.pem \
  --tls-private-key-file=/etc/kubernetes/ssl/worker-key.pem \
  --network-plugin-dir=/etc/cni/net.d \
  --network-plugin=cni \
  > kubelet.log 2>&1 &


/etc/kubernetes/worker-kubeconfig.yaml:

apiVersion: v1
kind: Config
clusters:
- name: local
  cluster:
    certificate-authority: /etc/kubernetes/ssl/ca.pem
    server: 192.168.0.2
    
users:
- name: kube-admin
  user:
    client-certificate: /etc/kubernetes/ssl/admin.pem
    client-key: /etc/kubernetes/ssl/admin-key.pem
    token: 1234token
contexts:
- context:
    cluster: local
    user: kube-admin
  name: kubelet-context
current-context: kubelet-context
```

# Proxy

```
hyperkube proxy \
--master=https://192.168.0.2 \
--kubeconfig=/etc/kubernetes/worker-kubeconfig.yaml \
--proxy-mode=iptables \
--cluster-cidr=10.10.0.0/16 \
--hostname-override=192.168.0.4 \
> proxy.log 2>&1 &
```

Warning: clusterCIDR not specified, unable to distinguish between internal and external traffic

--proxy-mode=userspace | iptables

# Gateway: Traefik

https://docs.traefik.io/user-guide/kubernetes/#deploy-trfk

文档中有部署配置， 值得一提的是， pod 启动时， 会自动把 token, ca.crt, namespace 映射到 /var/run/secrets/kubernetes.io/ 下，traefik 正是利用了这几个文件和 apiserver 进行的通信。 apiserver 的host信息， 是通过环境变量的形式映射到pod内部的。


# Calico

启动kubelet之前需要创建一下文件，kubelet 启动需要设置 
--network-plugin-dir=/etc/cni/net.d \
--network-plugin=cni \
这两个配置项.

```
mkdir -p /etc/cni/net.d

cat >/etc/cni/net.d/10-calico.conf <<EOF
{
    "name": "calico-k8s-network",
    "type": "calico",
    "etcd_endpoints": "http://192.168.0.2:2379",
    "log_level": "info",
    "ipam": {
        "type": "calico-ipam"
    },
    "policy": {
        "type": "k8s"
    }
}
EOF

注意 calico/xxx 的版本，我手动设为了 master, policy controller 之前的版本不兼容 k8s 1.5.1


```

确实可以访问，但是，policy-controller 一直报错：

2017-01-10 12:15:06,568 5 ERROR Unahandled exception killed NetworkPolicy manager
Traceback (most recent call last):
  File "<string>", line 295, in _manage_resource
  File "<string>", line 400, in _sync_resources
TypeError: object of type 'NoneType' has no len()
2017-01-10 12:15:06,569 5 WARNING Re-starting watch on resource: NetworkPolicy

解决了，是镜像版本不对的问题，升级到 master 就可以了.

# DNS

和之前一样，把 `--kube-master-url=http://192.168.0.2:8080` 这行注释掉，因为使用了 https。
测试发现跨节点的 DNS 不能用。 是CNI没有配置对的问题。proxy mode 使用了 iptables, 但是 calico 没有配置对。 结果就是 iptalbes 转发的位置不对。

# Prometheus

https://coreos.com/assets/blog/promk8s/prometheus-deployment.yaml

镜像换成了 prom/prometheus:v1.4.1 , 运行发现 apiserver 没有连通，有点奇怪。
config 文件中的 insecure_skip_verify 设为了 true 也没效果。。
