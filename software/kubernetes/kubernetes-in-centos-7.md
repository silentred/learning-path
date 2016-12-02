# 手动搭建kubernetes集群

> 探索kubernetes系列的第三篇，主要记录手动搭建k8s集群的过程，部署dashboard, 部署DNS用作服务发现。顺便记录一下k8s中的一些资源的概念。

# 配置环境

这个步骤可以参考[《Flannel with Docker》](https://segmentfault.com/a/1190000007585313)文中的步骤，不想赘述了。用了 `centos/7` 这个镜像，需要多做一点工作。

## 安装 Guest Additions
`vagrant plugin install vagrant-vbguest` ,这时在 Vagrantfile 中不要设置目录映射, 添加以下配置

```
config.vbguest.auto_update = false
# do NOT download the iso file from a webserver
config.vbguest.no_remote = true
```

`vagrant up` 
`vagrant vbguest` 
这时会自动安装 Guest Additions， 再关闭vm，配置上目录映射，再up，就可以了. 家里的网络连接 centos 官方的源，速度还行， 可以不用改成国内源。

## 国内源

```
sudo cp /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak

wget http://mirrors.163.com/.help/CentOS7-Base-163.repo -O CentOS-Base.repo
mv CentOS-Base.repo /etc/yum.repos.d/

sudo yum makecache
sudo yum update
```

# Install Docker

```
sudo tee /etc/yum.repos.d/docker.repo <<-'EOF'
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/7/
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
EOF

sudo yum install docker-engine

sudo systemctl enable docker.service

sudo systemctl start docker
```

配置 http_proxy, 这步极为重要，一些必要的镜像要从谷歌的源下载, 感谢万恶的GWF:

vim /lib/systemd/system/docker.service 在[Service]中添加：
`EnvironmentFile=-/etc/docker/docker.conf`
这里的 减号 表示如果文件不存在，则忽略错误

vim /etc/docker/docker.conf 添加：

```
http_proxy=192.168.0.2:7777
https_proxy=192.168.0.2:7777
no_proxy=localhost,127.0.0.1,192.168.0.2
```
重启 dockerd

# Start etcd
`etcd --listen-client-urls 'http://0.0.0.0:2379,http://0.0.0.0:4001' --advertise-client-urls 'http://192.168.0.2:2379,http://192.168.0.2:4001'  > /dev/null 2>&1 &`

# Install Kubernetes
去 github release page 下载最新的版本. 大约 1G.

## Start Master 

启动 apiserver
`hyperkube apiserver --address=0.0.0.0 --etcd_servers=http://192.168.0.2:2379 --service-cluster-ip-range=10.10.0.0/16 --v=0 >apiserver.log 2>&1 &`

启动 controller-manager
`hyperkube controller-manager --master=127.0.0.1:8080 --logtostderr=true >cm.log 2>&1 &`

```
日志有有报错，pem 文件找不到，可能和下面这两个配置有关，需要搜索
--cluster-signing-cert-file string                                  Filename containing a PEM-encoded X509 CA certificate used to issue cluster-scoped certificates (default "/etc/kubernetes/ca/ca.pem")
--cluster-signing-key-file string                                   Filename containing a PEM-encoded RSA or ECDSA private key used to sign cluster-scoped certificates (default "/etc/kubernetes/ca/ca.key")
```

`hyperkube scheduler --master=127.0.0.1:8080 > scheduler.log 2>&1 &`

```
提示 Could not construct reference... due to: 'selfLink was empty, can't make reference'
```

## Start Node

启动 proxy:
`hyperkube proxy --master=192.168.0.2:8080 --logtostderr=true >proxy.log 2>&1 &`

安装DNS的部分有提到，kubelet 要添加两个启动参数, 完整的启动命令为：

`hyperkube kubelet --api_servers=192.168.0.2:8080 --address=0.0.0.0 --hostname_override=192.168.0.3 --healthz-bind-address=0.0.0.0 --logtostderr=true --cluster-dns=10.10.0.10 --cluster-domain=cluster.local >kubelet.log 2>&1 &`

# 基本操作
建议走一遍官网的 tutorial, 基本能了解常用的 资源类型， 我在github的仓库做了笔记，可以参考我的 [笔记](https://github.com/silentred/learning-path/blob/master/software/kubernetes/tutorial.md)

# Dashboard

在 kubernetes-src/cluster/addons/dashboard 中有 yaml 文件，使用 `kubectl create -f dashboard.yaml` 即可创建 dashboard deployment.

启动 dashboard 的之前，需要 打开一段注释，`args: - --apiserver-host=http://192.168.0.2:8080`,
否则 dashboard 无法启动

```
kubectl describe pods/kubernetes-dashboard-3985220203-j043h --namespace=kube-system
看到event信息报错, 启动其他 image 的时候也有这个错，需要查找, 
MissingClusterDNS, kubelet does not have ClusterDNS IP configured and cannot create Pod using "ClusterFirst" policy. Falling back to DNSDefault policy.
```

kubelet log显示 CPUAccounting not allowed , 
这个问题估计是 systemd 控制的

启动后界面如下：
![图片描述][1]

# 安装 skyDNS

进入 `kubernetes/cluster/addons/dns/` 目录， 需要使用到 `skydns-rc.yaml.in, skydns-svc.yaml.in`, 这两个文件。 

1. rc 需要替换的变量: 

    replica = 1
    dns_domain = cluster.local
    
    kube-dns 启动参数需要指定 master 的接口
    
    ```
    args:
    # command = "/kube-dns"
    - --kube-master-url=http://192.168.0.2:8080
    ```
    
2. svc 需要替换的变量：

    dns_server = 10.10.0.10 // 这个ip需要在 apiserver 的启动参数--service-cluster-ip-range设置的ip段 里面，随意定义一个.
    
    用kubectl create -f 启动 rc , svc.
    
    kubelet 启动参数需要加入 --cluster-dns=10.10.0.10 --cluster-domain=cluster.local

完整的启动命令为：

`hyperkube kubelet --api_servers=192.168.0.2:8080 --address=0.0.0.0 --hostname_override=bq-node1 --healthz-bind-address=0.0.0.0 --logtostderr=true --cluster-dns=10.10.0.10 --cluster-domain=cluster.local >kubelet.log 2>&1 &`

观察启动结果：

```
kubectl get rc --namespace=kube-system
kubectl get svc --namespace=kube-system
```

最后在 node机 上测试 DNS:
dig @10.10.0.10 hello.default.svc.cluster.local

```
;; ANSWER SECTION:
hello.default.svc.cluster.local. 30 IN  A   10.10.83.26
```

这里 hello 是 之前起的一个deploy，配置文件如下。建议还是分开两个文件写，hello-service.yaml, hello-deploy.yaml

```
kind: Service
apiVersion: v1
metadata:
  labels:
    app: hello
  name: hello
spec:
  ports:
  - port: 9090
  selector:
    run: hello
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: hello
spec:
  replicas: 1
  template:
    metadata:
      labels:
        run: hello
    spec:
      containers:
      - name: hello
        image: silentred/alpine-hello:v1
        ports:
        - containerPort: 9090
```

如果想升级 image:
`kubectl set image deploy/hello hello=silentred/alpine-hello:v2`

其实还有更好的办法： `kubectl replace -f `, 后面会提到.

这里有一个点需要注意：
只有service会被注册到 kube-dns 中，按照上面的service的定义，每个类型的服务都需要创建一个service， 因此每个类型的服务都会创建一个 clusterIP，clusterIP 的 backends 就是 EndPoints 的服务，默认是 round-robin 轮询。

这样虽然省事，但是clusterIP在任意node节点上都是可以访问的，有些内部的RPC只希望在集群container内部访问，而不想暴露到外部。还有有些服务，就只起一个实例， --replicas永远为1，那么就不需要再分配一个 clusterIP了， 减少耦合。 这样的话，可以使用 Headless Service, 就是把 `spec.clusterIP` 设为 `None`, 这样就不会给service分配clusterIP， 如果使用了 selector, dns里查到的就是容器的ip。 
详情看[文档](http://kubernetes.io/docs/user-guide/services/#dns)

## 服务发现

进入容器内部:
```
docker exec -it CONTAINER_ID bash

// resolv.conf 的内容，估计是 dns 插件自动生成的
bash-4.4# cat /etc/resolv.conf
search default.svc.cluster.local svc.cluster.local cluster.local pek2.qingcloud.com.
nameserver 10.10.0.10
options ndots:5
```

安装完kube-dns插件后，在容器内部使用DNS查找到的ip为该 service 的 clusterIP, 在容器内部ping自身的name(hello)可以看到解析出来的ip, 但是ping的包全部丢失了，文档解释是只支持 tcp/udp 通信。 [doc](http://kubernetes.io/docs/user-guide/services/#virtual-ips-and-service-proxies) 
这表示，在程序中直接使用 dial("default.svc.cluster.local"), 就能通过 service 去轮询各个 container, 可以不用实现 grpc 的 LB 策略了。

## 结合 Flannel

如果使用了 Headless Service, 那么就必须保证容器间的网络连通，可以采用 flannel。
flannel 配置的子网范围 不能和 apiserver 的 clusterIP 一致。


# 资源类型

## ConfigMap

用于容器镜像和配置文件之间的解耦, 可以用 kubectl create configmaps 来创建，也可以用yaml来创建，贴一个文档上的例子：

```
apiVersion: v1
data:
  game.properties: |-
    enemies=aliens
    lives=3
  ui.properties: |
    color.good=purple
    color.bad=yellow
kind: ConfigMap
metadata:
  creationTimestamp: 2016-02-18T18:34:05Z
  name: game-config
  namespace: default
  resourceVersion: "407"-
  selfLink: /api/v1/namespaces/default/configmaps/game-config
  uid: 30944725-d66e-11e5-8cd0-68f728db1985
```

在容器中使用有多种方式：
1 定义为环境变量，下面有例子，定义了环境变量，还可以用作启动参数

```
apiVersion: v1
kind: Pod
metadata:
  name: dapi-test-pod
spec:
  containers:
    - name: test-container
      image: gcr.io/google_containers/busybox
      command: [ "/bin/sh", "-c", "echo $(SPECIAL_LEVEL_KEY) $(SPECIAL_TYPE_KEY)" ]
      env:
        - name: SPECIAL_LEVEL_KEY
          valueFrom:
            configMapKeyRef:
              name: special-config
              key: special.how
        - name: SPECIAL_TYPE_KEY
          valueFrom:
            configMapKeyRef:
              name: special-config
              key: special.type
  restartPolicy: Never
```

2 作为volume使用，mount到镜像的指定目录：

```
apiVersion: v1
kind: Pod
metadata:
  name: dapi-test-pod
spec:
  containers:
    - name: test-container
      image: gcr.io/google_containers/busybox
      command: [ "/bin/sh", "-c", "cat /etc/config/special.how" ]
      volumeMounts:
      - name: config-volume
        mountPath: /etc/config
  volumes:
    - name: config-volume
      configMap:
        name: special-config
  restartPolicy: Never
```

### 测试
定义一个 ConfigMap:
```
kind: ConfigMap
apiVersion: v1
metadata:
  creationTimestamp: 2016-02-18T19:14:38Z
  name: my-config
  namespace: default
data:
  example.foo: bar
  example.long_file: |-
    test.1=value-1
    test.2=value-2
```

修改 hello-deploy.yaml:

```
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: hello
spec:
  replicas: 1
  template:
    metadata:
      labels:
        run: hello
    spec:
      containers:
      - name: hello
        image: silentred/alpine-hello:v2
        ports:
        - containerPort: 9090
        env:
          - name: CONFIG_FOO
            valueFrom:
              configMapKeyRef:
                name: my-config
                key: example.foo
```

替换原来的deployment, `kubectl replace -f hello-deploy.yaml`, 在运行这个命令之前可以在 node 机上 用 docker ps 观察一下 hello container的 id， 运行后在看一下，会发现两者是不一样的，说明container 重启了。

这时，再次进入 hello container 内部，`env | grep FOO` 可以看到效果。
```
bash-4.4# env | grep FOO
CONFIG_FOO=bar
```

## Secret

和 configmap 类似，只是 value 是 base64 encoded. 创建：
```
apiVersion: v1
data:
  password: MWYyZDFlMmU2N2Rm
  username: YWRtaW4=
kind: Secret
metadata:
  creationTimestamp: 2016-01-22T18:41:56Z
  name: mysecret
  namespace: default
  resourceVersion: "164619"
  selfLink: /api/v1/namespaces/default/secrets/mysecret
  uid: cfee02d6-c137-11e5-8d73-42010af00002
type: Opaque
```

同样可以选择 mount 到 path或者 环境变量:
```
apiVersion: v1
kind: Pod
metadata:
  name: secret-env-pod
spec:
  containers:
    - name: mycontainer
      image: redis
      env:
        - name: SECRET_USERNAME
          valueFrom:
            secretKeyRef:
              name: mysecret
              key: username
        - name: SECRET_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysecret
              key: password
  restartPolicy: Never
```

### imagePullSecrets

在从私有registry 拉取镜像时，可以用 secret 来设定 username, password, 参考[文档](http://kubernetes.io/docs/user-guide/images/#specifying-imagepullsecrets-on-a-pod)

### 限制
1. 对于依赖secret 的pod，必须先设定secret
2. secret跨namespace不可见
3. 单个secret 1MB 大小限制
4. kubelets只支持从API server 创建的pod使用 secret. 不支持通过 kubelets --manifest-url,  --config 创建的pod // 需要查下有什么区别

对于第一点：pod在被创建前，不会检查 secret是否存在，当pod被调度创建时，会先去apiserver取secret，如果失败（网络，不存在）则会重复尝试，直到得到secret，并mount成功。

## DaemonSet

待续

## ReplicaSet

待续


  [1]: /img/bVGmq9