#!/bin/bash

quayImages=(
    kube-policy-controller:v0.5.4
    node:v1.1.0
    cni:v1.6.1   
)

fullQuayImages=( "${quayImages[@]/#/'quay.io/calico/'}" )

#gcr.io/google_containers/{img_name}
gcrImages=(
    kube-proxy-amd64:v1.6.0
    kube-controller-manager-amd64:v1.6.0
    kube-apiserver-amd64:v1.6.0
    kube-scheduler-amd64:v1.6.0

    etcd-amd64:3.0.17
    etcd:2.2.1
    pause-amd64:3.0

    k8s-dns-sidecar-amd64:1.14.1
    k8s-dns-kube-dns-amd64:1.14.1
    k8s-dns-dnsmasq-nanny-amd64:1.14.1
    heapster-amd64:v1.3.0-beta.1
)

fullGcrImages=( "${gcrImages[@]/#/'gcr.io/google_containers/'}" )

function download {
    # pull images
    printf "%s\n" "${gcrImages[@]}" | xargs -i docker pull gcr.io/google_containers/'{}'
    printf "%s\n" "${quayImages[@]}" | xargs -i docker pull quay.io/calico/'{}'
    #docker save
    for imageName in ${gcrImages[@]} ; do
        docker save -o gcr-gk-$imageName.tar gcr.io/google_containers/$imageName
    done

    for imageName in ${quayImages[@]} ; do
        docker save -o quay-clc-$imageName.tar quay.io/calico/$imageName
    done
}

function import {
    for imageName in ${gcrImages[@]} ; do
        docker load < gcr-gk-$imageName.tar
    done

    for imageName in ${quayImages[@]} ; do
        docker load < quay-clc-$imageName.tar
    done
}

case "$1" in
	download)
		download
		;;
    import)
        import
        ;;
	*)
		echo "Usage: $0 {download|import}" >&2
		exit 3
		;;
esac

#for imageName in ${gcrImages[@]} ; do
#    docker pull registry.cn-hangzhou.aliyuncs.com/magina-k8s/$imageName
#    docker tag registry.cn-hangzhou.aliyuncs.com/magina-k8s/$imageName gcr.io/google_containers/$imageName
#    docker rmi registry.cn-hangzhou.aliyuncs.com/magina-k8s/$imageName
#done

