## Tutorial

### Concept

#### Master

The Master is responsible for managing the cluster. 负责管理
- scheduling app 调度
- maintaining app's desired state? 维护状态
- scaling app 扩展

#### Node

A node is a VM or a physical computer that serves as a worker machine in a Kubernetes cluster. 
- each has a kubelet
- has container tool, e.g. Docker, rkt

#### minikube

install:
download from github release
$ curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.12.1/minikube-darwin-amd64 && chmod +x minikube && mv minikube /usr/local/bin

start:
minikube version
minikube start // start a VM, and a Kubernetes cluster is now running in that VM

#### kubectl

kubectl version // tool version
kubectl cluster-info // get cluster info
kubectl get nodes // get nodes info


### Deployment:

The Deployment is responsible for creating and updating instances of your application.
This provides a self-healing mechanism to address machine failure or maintenance.
负责创建，升级 app实例，有自我修复机制。

### Pods:

A Pod is a group of one or more application containers (such as Docker or rkt) and includes shared storage (volumes), IP address and information about how to run them.
一个或多个 app container 的集合，这些实例共享 storage, IP address, 等资源。

Pods are the atomic unit on the Kubernetes platform. 
Pods 是 原子单位

We create Deployment, then deployment creates Pods. 

Each Pod is tied to the Node where it is scheduled, and remains there until termination (according to restart policy) or deletion. In case of a Node failure, identical Pods are scheduled on other available Nodes in the cluster.
每个 Pod 和 Node 相绑定，直到Pod销毁，或被删除。如果Node不可用了，相同的Pods会被调度到其他可用Node。

Containers should only be scheduled together in a single Pod if they are tightly coupled and need to share resources such as disk.
如果多个container关联很大，那么应该把他们放到同一个Pod中。

nodes:



