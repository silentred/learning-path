#!/bin/bash

# etcd
docker run -d --network=host flynn/etcd

# master
hyperkube apiserver --service-cluster-ip-range=172.17.17.1/24 --insecure-bind-address=127.0.0.1 --etcd_servers=http://localhost:4001 --v=2 > /dev/null 2>&1 &
hyperkube scheduler --master=127.0.0.1:8080 --v=2 > /dev/null 2>&1 &
hyperkube controller-manager --master=127.0.0.1:8080 --v=2 > /dev/null 2>&1 &

# worker
hyperkube kubelet --api_servers=http://127.0.0.1:8080 --v=2 --address=0.0.0.0 --enable_server > /dev/null 2>&1 &
hyperkube proxy --master=http://127.0.0.1:8080 --v=2 > /dev/null 2>&1 &