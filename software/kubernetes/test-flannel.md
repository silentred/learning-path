# start etcd
etcd --listen-client-urls="http://0.0.0.0:2379,http://0.0.0.0:4001"


# Start flanneld

sudo ./flanneld -etcd-endpoints="http://192.168.1.19:4001" -iface=eth1
选择这个主机所在网络的iface, 例如这个主机所在的网络为 192.168.1.255, 那么就选这个ip对应的interface作为 iface 参数。

```
I1118 08:22:07.837670    4962 main.go:132] Installing signal handlers
I1118 08:22:07.839320    4962 manager.go:163] Using 192.168.1.15 as external interface
I1118 08:22:07.839870    4962 manager.go:164] Using 192.168.1.15 as external endpoint
I1118 08:22:07.861167    4962 local_manager.go:179] Picking subnet in range 172.1.1.0 ... 172.1.255.0
I1118 08:22:07.878228    4962 manager.go:246] Lease acquired: 172.1.46.0/24
I1118 08:22:07.890394    4962 network.go:98] Watching for new subnet leases
I1118 08:22:07.936195    4962 network.go:191] Subnet added: 172.1.7.0/24
```

ifconfig -a

```
eth1      Link encap:Ethernet  HWaddr 08:00:27:c7:13:a1
          inet addr:192.168.1.15  Bcast:192.168.1.255  Mask:255.255.255.0
          inet6 addr: fe80::a00:27ff:fec7:13a1/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:132112 errors:0 dropped:0 overruns:0 frame:0
          TX packets:2053 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:8189453 (8.1 MB)  TX bytes:145461 (145.4 KB)

flannel0  Link encap:UNSPEC  HWaddr 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00
          inet addr:172.1.46.0  P-t-P:172.1.46.0  Mask:255.255.0.0
          UP POINTOPOINT RUNNING NOARP MULTICAST  MTU:1472  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:500
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)
```

# start docker

$ source /run/flannel/subnet.env
$ sudo dockerd --bip=${FLANNEL_SUBNET} --mtu=${FLANNEL_MTU}

# create an network interface (不需要)

1. 先要确保 kernel 有 dummpy module ，这个模块是什么？
$ sudo lsmod | grep dummy
$ sudo modprobe dummy
$ sudo lsmod | grep dummy
dummy                  12960  0 

2. 创建 eth10

$ sudo ip link set name eth10 dev dummy0
确认
$ ip link show eth10
6: eth10: <BROADCAST,NOARP> mtu 1500 qdisc noop state DOWN mode DEFAULT group default 
    link/ether c6:ad:af:42:80:45 brd ff:ff:ff:ff:ff:ff

3. 修改 MAC地址（选）

$ sudo ifconfig eth10 hw ether 00:22:22:ff:ff:ff
$ ip link show eth10
6: eth10: <BROADCAST,NOARP> mtu 1500 qdisc noop state DOWN mode DEFAULT group default 
    link/ether 00:22:22:ff:ff:ff brd ff:ff:ff:ff:ff:ff

4. 绑定IP地址？

sudo ip addr add 172.1.1.1/24 brd + dev eth10

ifconfig -a

