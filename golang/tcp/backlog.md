# Backlog作用

当socket被设为LISTEN状态之后，必须为其指定一个backlog。就是incoming connection的限长队列。

因为TCP三次握手的关系，connection 需要经历 SYN RECEIVED 之后才能到达 ESTABLISHED 状态。然后才能被 accept。

实现1:
backlog是系统调用listen的参数，用于设置队列的大小。队列未满时，当一个SYN包被接收，立刻返回一个 SYN/ACK ， 并将 connection 加入队列。等待接收  ACK 包，收到后，connection 转为 ESTABLISHED状态。 所以队列中会有两种状态的 connection (SYN RECEIVED, ESTABLISHED)，只有 ESTABLISHED的连接才能被 accept。

实现2：
用两个队列。一个 SYN 队列（未完成的连接），一个 accept 队列（完整的连接）. SYN RECEIVED的连接加入 SYN queue, 等到收到ACK包后状态转为 ESTABLISHED 并移入 accept queue. 这种实现中 backlog 指定的是 accept queue 的大小。

http://veithen.github.io/2014/01/01/how-tcp-backlog-works-in-linux.html

BSD一般都是第一种实现。当队列满时，系统不会发送 SYN/ACK 回应 SYN， 并且通常都会抛弃 SYN包，这导致 client会retry。

目前的Linux一般都是实现2.

