# K8S in Production

## Create TLS Cert

### CA Root

```
ROOT CA

openssl genrsa -out ca-key.pem 2048 // ca pk
openssl req -x509 -new -nodes -key ca-key.pem -days 10000 -out ca.pem -subj "/CN=kube-ca" // ca public key

```

### Apiserver 

```
openssl.cnf

[req]
req_extensions = v3_req
distinguished_name = req_distinguished_name
[req_distinguished_name]
[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names
[alt_names]
DNS.1 = kubernetes
DNS.2 = kubernetes.default
DNS.3 = kubernetes.default.svc
DNS.4 = kubernetes.default.svc.cluster.local
IP.1 = 10.10.0.1
IP.2 = 192.168.0.2

// IP.1 = Service IP, 是cluster_ip_range 地址段的首个地址，在启动 apiserver 时设置的值，我们设置的是
// 10.10.0.0/16 , 所以这里是 10.10.0.1

API sever

openssl genrsa -out apiserver-key.pem 2048 // apiserver pk
openssl req -new -key apiserver-key.pem -out apiserver.csr -subj "/CN=kube-apiserver" -config openssl.cnf // 生成 CSR, 请求签名, 

openssl x509 -req -in apiserver.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out apiserver.pem -days 3650 -extensions v3_req -extfile openssl.cnf // 用CA的私钥，公钥给 CSR签名，得到 apiserver 证书
```

### Admin

```
Admin

openssl genrsa -out admin-key.pem 2048
openssl req -new -key admin-key.pem -out admin.csr -subj "/CN=kube-admin"
openssl x509 -req -in admin.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out admin.pem -days 3650  // 步骤和上面类似，有一点疑问，为什么CA 签过名的证书，就可以让 Admin 和 API Server 通信？

```

### Worker

```
Worker

在 node 机器上创建

worker-openssl.cnf :

[req]
req_extensions = v3_req
distinguished_name = req_distinguished_name
[req_distinguished_name]
[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names
[alt_names]
IP.1 = $ENV::WORKER_IP

// 这里如果不用这个config，不知道行不行，原理部分还是有些模糊, 这里的worker_ip 不知道是什么作用

openssl genrsa -out worker-key.pem 2048
WORKER_IP=${WORKER_IP} openssl req -new -key worker-key.pem -out worker.csr -subj "/CN=kube-worker" -config worker-openssl.cnf // 
WORKER_IP=${WORKER_IP} openssl x509 -req -in worker.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out worker.pem -days 3650 -extensions v3_req -extfile worker-openssl.cnf //  ca 给 worker 签名证书
```

## Setup Master Server

apiserver.yaml, controller.yaml, scheduler.yaml, calico.yaml
四个文件放入 /etc/kubernetes/manifests 中。

mkdir -p /etc/kubernetes/cni/net.d // 目前不知道什么作用

start kubelet, 注意 kubelet 的版本，测试环境忘了升级到 1.5.1 了
```
hyperkube kubelet \
  --api-servers=http://127.0.0.1:8080 \
  --register-schedulable=false \
  --container-runtime=docker \
  --allow-privileged=true \
  --pod-manifest-path=/etc/kubernetes/manifests \
  --cni-conf-dir=/etc/kubernetes/cni/net.d \
  --network-plugin=cni \
  --hostname-override=192.168.0.2 \
  --cluster_dns=10.10.0.10 \
  --cluster_domain=cluster.local >kubelet.log 2>&1 &
```

貌似 rs/calico-policy-controller 没有启动成功，一直在 waiting 的状态，describe 的日志只有一行 
Created pod: calico-policy-controller-znfls ;
describe calico-policy-controller-znfls 后发现，是因为没有node可以调度, 日志为 
Warning    FailedScheduling    no nodes available to schedule pods

## Config Kubectl

```
设置 kubectl 的验证

CA_CERT=/etc/kubernetes/ssl/ca.pem
ADMIN_KEY=/etc/kubernetes/ssl/admin-key.pem
ADMIN_CERT=/etc/kubernetes/ssl/admin.pem
MASTER_HOST=192.168.0.2

kubectl config set-cluster default-cluster --server=https://${MASTER_HOST} --certificate-authority=${CA_CERT}
kubectl config set-credentials default-admin --certificate-authority=${CA_CERT} --client-key=${ADMIN_KEY} --client-certificate=${ADMIN_CERT}
kubectl config set-context default-system --cluster=default-cluster --user=default-admin
kubectl config use-context default-system


前两个命令替换后：
kubectl config set-cluster default-cluster --server=https://192.168.0.2 --certificate-authority=/etc/kubernetes/ssl/ca.pem
kubectl config set-credentials default-admin --certificate-authority=/etc/kubernetes/ssl/ca.pem --client-key=/etc/kubernetes/ssl/admin-key.pem --client-certificate=/etc/kubernetes/ssl/admin.pem
```

## Setup Node Server

Node kubelet

```
hyperkube kubelet \
  --api-servers=https://192.168.0.2 \
  --cni-conf-dir=/etc/kubernetes/cni/net.d \
  --network-plugin=cni \
  --container-runtime=docker \
  --register-node=true \
  --allow-privileged=true \
  --pod-manifest-path=/etc/kubernetes/manifests \
  --hostname-override=192.168.0.3 \
  --cluster_dns=10.10.0.10 \
  --cluster_domain=cluster.local \
  --kubeconfig=/etc/kubernetes/worker-kubeconfig.yaml \
  --tls-cert-file=/etc/kubernetes/ssl/worker.pem \
  --tls-private-key-file=/etc/kubernetes/ssl/worker-key.pem \
  > kubelet.log 2>&1 &

  #--api-servers=https://192.168.0.2 \ // 废弃了?
```

Node manifests:

kubelet-proxy
```
apiVersion: v1
kind: Pod
metadata:
  name: kube-proxy
  namespace: kube-system
spec:
  hostNetwork: true
  containers:
  - name: kube-proxy
    image: gcr.io/google_containers/hyperkube-amd64:v1.5.1
    command:
    - /hyperkube
    - proxy
    - --master=192.168.0.2
    - --kubeconfig=/etc/kubernetes/worker-kubeconfig.yaml
    securityContext:
      privileged: true
    volumeMounts:
    - mountPath: /etc/ssl/certs
      name: "ssl-certs"
    - mountPath: /etc/kubernetes/worker-kubeconfig.yaml
      name: "kubeconfig"
      readOnly: true
    - mountPath: /etc/kubernetes/ssl
      name: "etc-kube-ssl"
      readOnly: true
  volumes:
  - name: "ssl-certs"
    hostPath:
      path: "/usr/share/ca-certificates"
  - name: "kubeconfig"
    hostPath:
      path: "/etc/kubernetes/worker-kubeconfig.yaml"
  - name: "etc-kube-ssl"
    hostPath:
      path: "/etc/kubernetes/ssl"
```

/etc/kubernetes/worker-kubeconfig.yaml

```
apiVersion: v1
kind: Config
clusters:
- name: local
  cluster:
    certificate-authority: /etc/kubernetes/ssl/ca.pem
    server: https://192.168.0.2
users:
- name: kubelet
  user:
    client-certificate: /etc/kubernetes/ssl/worker.pem
    client-key: /etc/kubernetes/ssl/worker-key.pem
contexts:
- context:
    cluster: local
    user: kubelet
  name: kubelet-context
current-context: kubelet-context
```








