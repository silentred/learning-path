## reactor线程
event loop 的进程，数量一般与核心

## worker
工作进程

## task_worker
异步任务进程

## $server->start()
启动server。在start之前可以调用的函数为: set, on, addListener, addProcess, listen, handler, 其余函数都必须在start之后调用，也就是server内部调用。
start 启动 worker_num+2 个进程，分别为 主进程， Manager进程， worker_num个worker进程

主进程中有多个reactor线程，基于epoll/kqueue进行网络事件轮询。收到数据后转发到worker进程去处理

Manager进程 管理所有woker进程，负责创建和回收。

worker进程负责对接收到的数据处理，包括协议解析和响应请求。开启log_file设置日志路径。

## 柔性终止/重启worker进程
柔性是指防止在worker工作到一半的时候结束，而是等所有worker生命周期走完才重启.
默认设置了三个信号量， 
- SIGTERM : 终止服务器；server提供的方法为 $server->shutdown()
- SIGUSR1: 重启所有worker/task_workder; $server->reload()
- SIGUSR2: 仅仅重启task_worker

平滑重启只对onWorkerStart或onReceive等在Worker进程中include/require的PHP文件有效，Server启动前就已经include/require的PHP文件，不能通过平滑重启重新加载
对于Server的配置即$serv->set()中传入的参数设置，必须关闭/重启整个Server才可以重新加载
Server可以监听一个内网端口，然后可以接收远程的控制命令，去重启所有worker（addListener起作用了）

如果PHP开启了APC/OpCache，reload重载入时会受到影响，有2种解决方案：
打开APC/OpCache的stat检测，如果发现文件更新APC/OpCache会自动更新OpCode
在onWorkerStart中执行apc_clear_cache或opcache_reset刷新OpCode缓存


## tick/after()
tick()定时执行回调，是 swoole_timer_tick() 的别名。
after() 是 swoole_timer_after 的别名。
tick, after 两个函数不能在 task_worker 中使用。worker 和 task_worker 都是worker, 所以在启动(线程？)的时候，都会调用 onWorkStart回调，这时候可以用 $server->taskworker 这个属性来判断究竟启动的是哪一类 worker。

clearTimer 是 swoole_timer_clear的别名。

```
$i = 0;
$res = swoole_timer_tick(1000, function($id) {
        global $i;
        echo "timer_id is {$id} \n";
        $i++;
        if($i > 3){
                $ret = swoole_timer_clear($id);
                echo "result is $ret \n";
                exit();
        }
    });

var_dump($res);
```

## $server->send()
TCP 2M, UDP 64K

TCP服务器
send操作具有原子性，多个进程同时调用send向同一个连接发送数据，不会发生数据混杂
如果要发送超过2M的数据，可以将数据写入临时文件，然后通过sendfile接口进行发送

UDP服务器
send操作会直接在worker进程内发送数据包，不会再经过主进程转发
使用fd保存客户端IP，from_id保存from_fd和port
如果在onReceive后立即向客户端发送数据，可以不传$from_id
如果向其他UDP客户端发送数据，必须要传入from_id
在外网服务中发送超过64K的数据会分成多个传输单元进行发送，如果其中一个单元丢包，会导致整个包被丢弃。所以外网服务，建议发送1.5K以下的数据包

## sendwait
阻塞等待连接可写再发送，防止某些特殊需求下连续大量数据发送会导致内存发送队列塞满，send是异步的。

## sendMessage / onPipeMessage
可以向任意worker进程或者task进程发送消息。在 非主进程 和 Manager进程 中可调用。收到消息的进程会触发onPipeMessage事件, 所以必须注册onPipeMessage事件回调函数




## swoole_process

// SIGCHLD 是当子进程stop或者 terminate的时候，发送给父进程的信号。默认行为是忽略它。
swoole_process::signal(SIGCHLD, function(){
    //表示子进程已关闭，回收它
    $status = swoole_process::wait();
    echo "Worker#{$status['pid']} exit\n";
});