## 使用SSH上传文件

### 配置SSH
一般使用方法：
```shell
ssh user@host
ssh -i ~/.ssh/private_key.pem user@host
```

可以把信息存在配置文件中`~/.ssh/config`
```
Host dev
    HostName dev.hostname.com
    User dev

Host aws
    HostName 64.92.157.36
    User user
    IdentityFile ~/.ssh/private_key.pem
```
这样只需要：`ssh aws`，便可进入aws主机了

### scp命令
一旦完成配置，可以用如下命令上传文件：
`scp <file-to-upload> aws:/tmp/file`

该命令会把<file-to-upload>上传到aws主机的/tmp目录下，重命名为file

### 上传public key
`cat ~/.ssh/id_rsa.pub | ssh myUser@remoteHost.com '>> .ssh/authorized_keys'`
