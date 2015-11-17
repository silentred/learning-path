# 关于VPN搭建

## SoftEther VPN
快捷搭建 L2TP, PPTP 等协议vpn。有docker镜像。

## FreeRadius
开源计费系统
教程如下
http://safesrv.net/install-and-setup-freeradius-on-centos-5/

## FreeRadius Web Manager
Daloradius
mysql -u root -p radius < mysql-daloradius.sql
vim /home/www/daloradius/library/daloradius.conf.php Change the database password $configValues['CONFIG_DB_PASS'] = 'password'


## 手动搭建VPN

declare DDnsClient
{
		bool Disabled true
		byte Key Jpx1ip89qQzF8TGngubiUOLPUVY=
		string LocalHostname www
		string ProxyHostName $
		uint ProxyPort 0
		uint ProxyType 0
		string ProxyUsername $
}

client vpn1 {
	ipaddr = 172.16.1.220
	secret		= testing123
	require_message_authenticator = no
	nastype     = other
}

## Accounting

yum install syslog-ng syslog-ng-libdbi

```
source net { udp(); };
destination remote { file("/var/log/remote/${FULLHOST}/${YEAR}/${MONTH}/${DAY}/${HOST}_${YEAR}_${MONTH}_${DAY}.log" create-dirs(yes)); };
log { source(net); destination(remote); };

filter acctstart_172.16.1.220_VPN { host("172.16.1.220") and message("VPN") and message("The new session"); };
destination acctstart { program("php /usr/local/softether-radacct/acctstart.php" flags(no_multi_line) flush_lines(1) flush_timeout(1000)); };
log { source(net); filter(acctstart_172.16.1.220_VPN); destination(acctstart); };

filter acctstop_172.16.1.220_VPN { host("172.16.1.220") and message("VPN") and message("The session has been terminated"); };
destination acctstop { program("php /usr/local/softether-radacct/acctstop.php" flags(no_multi_line) flush_lines(1) flush_timeout(1000)); };
log { source(net); filter(acctstop_172.16.1.220_VPN); destination(acctstop); };
```

```
<?php
$apipass = "123456"; // softether hub password
$radiussrv = "172.16.1.220"; // radius server address
$radiuspass = "testing123"; // radius secret
$radiusport = "1813"; // radius server accounting port 
$database = "/var/radius/sessions.db"; // temporary database location
$tmpdir = "/tmp"; // temporary directory
$hubname = "VPN"; // softether hub name
$softetherip = "172.16.1.220"; // softether hub address
$vpncmd = "/usr/local/vpnserver/vpncmd";
?>
```


for vpn in /proc/sys/net/ipv4/conf/*; do echo 0 > $vpn/accept_redirects; echo 0 > $vpn/send_redirects; done