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

kubectl run testgo --image=silentred/hello:v1 --port=9090
创建一个 Deployment

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

### Nodes

Every Kubernetes Node runs at least:

Kubelet, a process responsible for communication between the Kubernetes Master and the Nodes; it manages the Pods and the containers running on a machine.
Kubelet 和 Master 通信，管理 node 上的 Pods

A container runtime (like Docker, rkt) responsible for pulling the container image from a registry, unpacking the container, and running the application.

kubectl get - list resources
kubectl describe $POD_NAME - show detailed information about a resource
kubectl logs $POD_NAME - print the logs from a container in a pod
kubectl exec $POD_NAME CMD - execute a command on a container in a pod

### Service

A Kubernetes Service is an abstraction layer which defines a logical set of Pods and enables external traffic exposure, load balancing and service discovery for those Pods.
抽象层，定义了Pods的逻辑集合，暴露接口给外部，还有 LB, SD 的功能。

Labels are key/value pairs that are attached to objects, such as Pods and you can think of them as hashtags from social media.

kubectl expose deployment/kubernetes-bootcamp --type="NodePort" --port 9090
kubectl describe services/testgo

export NODE_PORT=$(kubectl get services/testgo -o go-template='{{(index .spec.ports 0).nodePort}}')

kubectl describe deployment // See the Label
kubectl get pods -l run=kubernetes-bootcamp
kubectl get services -l run=kubernetes-bootcamp

kubectl label pod $POD_NAME app=v1 // add Label
kubectl get pods -l app=v1 // search again

kubectl delete service -l run=kubernetes-bootcamp // delete service

kubectl exec -ti $POD_NAME curl localhost:9090

### Scale

kubectl scale deployments/kubernetes-bootcamp --replicas=4
kubectl get deployments // desired 变为 4
kubectl get pods -o wide // 展示出 4 个 pod

### Rolling Update

kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=jocatalin/kubernetes-bootcamp:v2 

kubectl rollout status deployments/kubernetes-bootcamp // 回退





