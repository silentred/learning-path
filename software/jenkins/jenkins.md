# Jenkins

## host install

```
sudo yum install epel-release
sudo yum update

sudo yum install java-1.8.0-openjdk.x86_64

sudo cp /etc/profile /etc/profile_backup
echo 'export JAVA_HOME=/usr/lib/jvm/jre-1.8.0-openjdk' | sudo tee -a /etc/profile
echo 'export JRE_HOME=/usr/lib/jvm/jre' | sudo tee -a /etc/profile
source /etc/profile

cd ~
sudo wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat-stable/jenkins.repo
sudo rpm --import http://pkg.jenkins-ci.org/redhat-stable/jenkins-ci.org.key
sudo yum install jenkins

sudo systemctl start jenkins.service
sudo systemctl enable jenkins.service

```

默认8080端口

## Setup First Job

安装插件； 新建 Freestyle Project;
勾选 Github project;
Source Code: 选 Git, 填上 git地址;
Build Trigger: 选 GitHub hook trigger for GITScm polling；这样当有push的时候，会触发job;

Build: 使用shell脚本：
```
export GOPATH=/go
make build
rm -rf /go/src/hello-ci
cp -r `pwd` /go/src
cd /go/src/hello-ci
make test
```


## 创建slave节点

进入 manage node -> new item -> 连接方式选择 java web start;

在host上运行如下命令, 启动slave镜像:

```
docker run -d -e JNLP_PROTOCOL_OPTS=-Dorg.jenkinsci.remoting.engine.JnlpProtocol3.disabled=false jenkinsci/jnlp-slave -url http://138.68.232.0:8080 3ededa31c250ac8c707f33958d0edb46732430a32a0a4f1dc31adc67b1314195 slave1
```

## 创建 go 测试环境

```
docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=root -d mysql:5.7

docker run --name go-test -p 2222:22 --link some-mysql:mysql -d silentred/go-test:v7
```

## Github webhook的验证方式

```
// If we have a Secret set, we should check the MAC
if s.Secret != "" {
    sig := req.Header.Get("X-Hub-Signature")

    if sig == "" {
        http.Error(w, "403 Forbidden - Missing X-Hub-Signature required for HMAC verification", http.StatusForbidden)
        return
    }

    mac := hmac.New(sha1.New, []byte(s.Secret))
    mac.Write(body)
    expectedMAC := mac.Sum(nil)
    expectedSig := "sha1=" + hex.EncodeToString(expectedMAC)
    if !hmac.Equal([]byte(expectedSig), []byte(sig)) {
        http.Error(w, "403 Forbidden - HMAC verification failed", http.StatusForbidden)
        return
    }
}
```
