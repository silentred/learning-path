Go项目如何部署测试环境

# 测试环境

1. 进入 /home/wangyang
2. npm install pm2
3. 配置应用文件 dcgo.yaml
    ```
    apps:
      - name: "dcgo"
        script : dcgo/dc-go
        args: ["-mode=dev"]
    ```
4. 启动 node_modules/pm2/bin/pm2 start dcgo.yaml

# 本地脚本

本地编译，scp 到 remote, ssh remote 执行shell, 最后删除本地编译文件

```
GOOS=linux GOARCH=amd64 go build -o dc-go .
scp dc-go luoji-dev2:~
ssh luoji-dev2 <<EOFSSH
mv dc-go dcgo/
node_modules/pm2/bin/pm2 restart dcgo
EOFSSH
rm dc-go
```
