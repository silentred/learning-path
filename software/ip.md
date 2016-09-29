ubuntu:
ip route get 1 | awk '{print $NF;exit}'

centos:
ip route get 1 | awk '{print $NF;exit}'

mac:
ifconfig | grep inet | awk '/broadcast/ {print $2}'
ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' 

