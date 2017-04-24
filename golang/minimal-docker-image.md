# 如何打包出最小镜像

## 静态编译

`CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o hello hello-app/*.go`

the -a flag means to rebuild all the packages we’re using, which means all the imports will be rebuilt with cgo disabled.
https://github.com/golang/go/issues/9344#issuecomment-69944514

建议使用 bash 作为 base image, 毕竟还有一些操作例如 mkdir, mv , cp 等需要执行。

如何查看 二进制文件 的 动态依赖?

```
# ldd hello

linux-vdso.so.1 =>  (0x00007ffde7df8000)
libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007ff931ae5000)
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007ff93171e000)
/lib64/ld-linux-x86-64.so.2 (0x00005637b0ae4000)


# readelf -d hello

Dynamic section at offset 0x697100 contains 19 entries:
  Tag        Type                         Name/Value
 0x0000000000000004 (HASH)               0xa959e0
 0x0000000000000006 (SYMTAB)             0xa95e60
 0x000000000000000b (SYMENT)             24 (bytes)
 0x0000000000000005 (STRTAB)             0xa95c40
 0x000000000000000a (STRSZ)              518 (bytes)
 0x0000000000000007 (RELA)               0xa95650
 0x0000000000000008 (RELASZ)             24 (bytes)
 0x0000000000000009 (RELAENT)            24 (bytes)
 0x0000000000000003 (PLTGOT)             0xa97000
 0x0000000000000015 (DEBUG)              0x0
 0x0000000000000001 (NEEDED)             Shared library: [libpthread.so.0] // 动态依赖库
 0x0000000000000001 (NEEDED)             Shared library: [libc.so.6] // 动态依赖库
 0x000000006ffffffe (VERNEED)            0xa95960
 0x000000006fffffff (VERNEEDNUM)         2
 0x000000006ffffff0 (VERSYM)             0xa95920
 0x0000000000000014 (PLTREL)             RELA
 0x0000000000000002 (PLTRELSZ)           648 (bytes)
 0x0000000000000017 (JMPREL)             0xa95680
 0x0000000000000000 (NULL)               0x0
```

## Alpine 编译

alpine linux 使用 musl libc，而 ubuntu, centos 使用的是 glibc, 所以在 ubuntu,centos下编译的文件一般不能直接使用在 alpine 环境。

```
# export WORKDIR=/go/src/hello-app

# docker run --rm -v $GOPATH/src:/go/src -v "$PWD":${WORKDIR} -w ${WORKDIR} golang:1.8-alpine go build -o hello-alpine hello-app/main.go

```

注意，编译的依赖package 被映射入了 /go/src 中; -w 表示 working directory. 

http://web-rat.com/posts/2016/09/06/compiling-go-for-alpine/

