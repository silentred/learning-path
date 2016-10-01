Udp丢包排查过程

1. 查看udp丢包，cat /proc/net/snmp | grep Udp（比netstat –su效果好）
2. 查看网卡丢包(ifconfig 或者ethtool –S eth1)
3. Netstat –alupt 查看队列里现存的包数，如果过多说明有问题。
4. 查看socket队列长度，cat /proc/sys/net/core/rmem_default (wmem_default是写队列长度)
5. 查看网卡队列长度， ethtool -g eth1 
6. 查看cpu负载情况，top，vmstat 1（或者mpstat –P ALL 1）
7. 如果是arp缓存导致的丢包，查看arp缓存队列长度，/proc/sys/net/ipv4/neigh/eth1/unres_qlen