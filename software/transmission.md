## 安装transmission

### 编译环境
`yum groupinstall "Development Tools"`

`yum install gcc gcc-c++ m4 make automake libtool gettext openssl-devel pkgconfig libcurl intltool`

`export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig`


安装libevent, 需要大于2.0
`wget https://sourceforge.net/projects/levent/files/libevent/libevent-2.0/libevent-2.0.22-stable.tar.gz`

`tar xf libevent-2.0.22-stable.tar.gz && cd libevent-2.0.22-stable`

`./configure -q && make -s`
`sudo make install`

### 安装transmission

`wget http://download.transmissionbt.com/files/transmission-2.84.tar.xz`

`tar xf transmission-2.84.tar.xz && cd transmission-2.84`

`./configure -q --prefix=/usr/local/transmission && make -s
sudo make install`

`export PATH=$PATH:/usr/local/transmission/bin`

`transmission-cli --help`
`transmission-show --help`



### yum安装

yum install transmission transmission-cli transmission-common transmission-daemon

sudo service transmission-daemon start # to generate the following config file
sudo service transmission-daemon stop # 先停止，才可以编辑settings.json

配置文件位于 `/var/lib/transmission/.config/transmission/settings.json`

"rpc-whitelist": "*,127.0.0.1,50.62.213.12,104.168.174.83,45.55.11.138",
"rpc-password": "789456123", // 密码会自动 SHA1 
"rpc-username": "jason",

sudo service transmission-daemon start

[安装配置参考](https://help.ubuntu.com/community/TransmissionHowTo#Configure)
[配置列表](https://trac.transmissionbt.com/wiki/EditConfigFiles)
