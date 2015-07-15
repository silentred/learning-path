## tcpdump使用

### 参数
- `-n`: 不显示hostname，只显示ip
- `-X`: 显示包中的内容，16进制和ascii
- `-S`: 把sequence number由相对值转换为绝对值

tcpdump默认只会读取每个包前96byte的数据，如果想要
读取更多，需要加上参数`-s number`, 其中number是byte数。
0代表snaplength，就是抓取所有数据。

### 其他常用参数
- `-i any`: 监听所有interface（网卡），或者也可以指定某一个网卡
，例如`-i eth0`
- `-D`: 显示所有网卡
- `-nn`: 不要解析hostname和port
- `-q`: 展示更少内容
- `-XX`: 与`-X`相同,额外展示 ethernet header
- `-v`,`-vv`, `-vvv`: 显示更多内容，与`-q`相反
- `-c`: 只获取x个包,并停止
- `icmp`: 只获取ICMP包
- `-s`: 每个包抓取byte长度,默认96;`-s 0`代表所有byte,或者使用`-s 1514`
- `-E`: 提供秘钥来解码IPSEC

### 表达式
- 类型： `host`, `net`, `port`
- 方向： `src`, `dst`
- `proto`： 值包含`tcp`, `udp`, `icmp`等
- `and`, `or`, `not`



`tcpdump -nXSvv -i venet0 host 50.117.7.122 and dst port 80`
表示host为50.117.7.122并且发向80端口的包

`tcpdump -nXSvv -i venet0 src port 80 or dst port 80`
表示从80端口来或者到80端口去的包
