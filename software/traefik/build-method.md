# Build 

1. git clone github.com/containous/traefik

2. apt-get install mercurial

3. glide install

4. go get github.com/jteeuwen/go-bindata

5. go install github.com/jteeuwen/go-bindata/go-bindata

6. go generate github.com/containous/traefik

7. grep -r 'log_dir' . 

会发现有些package下包含了vendor目录，所以重复引入了 glog 包， 需要删除多余的 glog 包

8. go test .

总算成功了.

go get 究竟做了哪些操作？