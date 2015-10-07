## 使用SSH上传文件

### 配置SSH
一般使用方法：
```shell
ssh user@host
ssh -i ~/.ssh/private_key.pem user@host
```

可以把信息存在配置文件中`~/.ssh/config`
```
Host sam
        HostName 50.62.213.12
        User stanford
        IdentityFile ~/.ssh/id_rsa

Host lifome
        HostName 162.249.4.210
        Port 7822
        User jason
        IdentityFile ~/.ssh/id_rsa
```
这样只需要：`ssh aws`，便可进入aws主机了

### scp命令
一旦完成配置，可以用如下命令上传文件：
`scp <file-to-upload> aws:/tmp/file`

该命令会把<file-to-upload>上传到aws主机的/tmp目录下，重命名为file

### 上传public key
`cat ~/.ssh/id_rsa.pub | ssh myUser@remoteHost.com '>> .ssh/authorized_keys'`

### 禁用密码登陆ssh
1. 编辑sshd_config文件 `vim /etc/ssh/sshd_config`
2. 禁用密码验证 `PasswordAuthentication no`

### 无法使用key验证的问题
1. 检查权限，`.ssh`为700, `authorized_keys`为600
2. 检查SeLinux，getenforce ； 暂时关闭 setenforce 0

### 动态端口转发
`ssh -N -f -D 8000 root@50.117.7.122`，监听8000端口，转发到50.117.7.122机器上。
服务器代理设置为 127.0.0.1:8000, SOCK4
