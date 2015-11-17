##服务端安装shadowsocks

### python版本
```
yum install python-setuptools && easy_install pip
pip install shadowsocks
```
配置文件
```json
{
	"server":"50.117.7.122",
	"server_port":8388,
	"local_address": "127.0.0.1",
	"local_port":1080,
	"password":"789456123",
	"timeout":300,
	"method":"aes-256-cfb",
	"fast_open": false
}
```

在后台运行 `ssserver -c config.json -d start`

### nodejs版本
下载nodejs版本, 找到bin文件夹
```
nohup node ssserver -c config.json > /dev/null 2>&1 &
```
node版本被废弃了，有内存泄露问题。

### C版本

下载源码编译, 测试可用

## linux运行客户端

启动python客户端
```
sslocal -c config.json -d start
```

用curl测试效果
```
curl --socks 127.0.0.1:1080 www.google.com
```

## 关于全局使用SOCKS5
貌似是用iptables把 output的包全部转发到 ss监听的端口：
http://serverfault.com/questions/332473/configuring-ubuntu-for-global-socks5-proxy