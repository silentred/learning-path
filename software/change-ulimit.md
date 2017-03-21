# 修改 ulimit

# 打开最大文件数
sysctl -w fs.file-max=500000
sysctl -p 


# 修改 `/etc/security/limits.conf`

```
root    hard    nofile  1000000
root    soft    nofile  1000000
```
如果是 root 以外用户，可用 * 代替， * 不对root生效.

# 修改 `/etc/pam.d/common-session`

`session required pam_limits.so`

重新进入shell，ulimit -Sn 查看修改效果