# kubernetes in centos 7 

# 安装 Guest Additions

vagrant plugin install vagrant-vbguest
#这时在 Vagrantfile 中不要设置目录映射, 添加以下配置

```
config.vbguest.auto_update = false
# do NOT download the iso file from a webserver
config.vbguest.no_remote = true
```

vagrant up
vagrant vbguest
// 这时会自动安装 Guest Additions， 再关闭vm，配置上目录映射，再up，就可以了
// 家里的网络连接 centos 官方的源，速度还行， 可以不用改成国内源。


# 国内源

sudo cp /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak

wget http://mirrors.163.com/.help/CentOS7-Base-163.repo -O CentOS-Base.repo
mv CentOS-Base.repo /etc/yum.repos.d/

sudo yum makecache
sudo yum update

# install docker

sudo tee /etc/yum.repos.d/docker.repo <<-'EOF'
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/7/
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
EOF

sudo yum install docker-engine

sudo systemctl enable docker.service

sudo systemctl start docker
