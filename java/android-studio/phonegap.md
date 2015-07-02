## 记录下红米安装phonegap developer的惨痛经历

1. root。几乎每个root软件都会附带安装各种软件。
2. 去小米应用商店中下载 应用汇
3. 应用汇中下载 谷歌安装器
4. 打开 谷歌安装器， 安装， 会重启
5. 重启后自动安装了 google play store
6. 安装 shadowsocks 翻墙，打开设置。
7. 打开 google play store， 搜索phonegap, 下载安装。

## cordova安装插件

1. git clone https://git-wip-us.apache.org/repos/asf/cordova-plugin-camera.git
https://git-wip-us.apache.org/repos/asf/cordova-plugin-dialogs.git
2. cordova plugin add /path/to/cordova-plugin-camera
3. cordova plugins 查看安装了哪些插件

## cordova服务器

cordova serve android 8080 默认端口为8000

## phonegap create

在%HOME%中使用phonegap create 可以成功创建，在D:\下就会提示失败


## 指定usb device
adb devices 查看连接的设备代号
phonegap run android --device=G6YHSCNFFAFMYPJZ
