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
  --hostname-override=192.168.0.3 \
  --cluster_dns=10.10.0.10 \
  --cluster_domain=cluster.local \
  --kubeconfig=/etc/kubernetes/worker-kubeconfig.yaml \
  --tls-cert-file=/etc/kubernetes/ssl/worker.pem \
  --tls-private-key-file=/etc/kubernetes/ssl/worker-key.pem \
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
> proxy.log 2>&1 &
```