## Tutorial

### Concept

#### Master

The Master is responsible for managing the cluster.
- scheduling app
- maintaining app's desired state?
- scaling app

#### Node

A node is a VM or a physical computer that serves as a worker machine in a Kubernetes cluster.
- each has a kubelet
- has container tool, e.g. Docker, rkt


### minikube

install:
download from github release
$ curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.12.1/minikube-darwin-amd64 && chmod +x minikube && mv minikube /usr/local/bin

start:
minikube version
minikube start // start a VM, and a Kubernetes cluster is now running in that VM

### kubectl

kubectl version // tool version
kubectl cluster-info // get cluster info
kubectl get nodes // get nodes info

deployment:

pods:

nodes:



