# gopub

## Tag＝版本
版本为空因为没有添加 tag, 这是基于 tag 的发布系统

## 一个bug
service/task.go 97行：应该改为

```
//task.PubTime = time.Date(0, 0, 0, 0, 0, 0, 0, time.UTC)
task.PubTime = time.Now().Add(12 * time.Hour)
```
go1.7 中发现问题，注释中的写法会导致生成非法的datetime, 例如 '00:-23:00' 这种负数，导致task插入失败


## 跳板机的设置
发布新的task 后，实际会在跳板机的配置目录中新建一个 task-xx 目录， 其中生成了一个 publish.sh 文件，用于把 www_root 中的文件 rsync 到实际的机器.

那么这里生成的 publish.sh 必须有执行权限，修改 ~/.bashrc, 加入 umask 022 ， 这样新建的文件权限为 755.【错误】
linux新建文件最大权限为 666, umask=022的情况下，新建的文件为 644，也是没有执行权限的。这时候使用 /bin/bash script.sh 是可以执行该文件的。

