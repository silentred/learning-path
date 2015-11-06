## reactor线程
event loop 的进程，数量一般与核心

## worker
工作进程

## task_worker
异步任务进程, 但貌似onTask中是同步阻塞的，不能使用async的方法

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
`bool swoole_server->sendMessage(string $message, int $dst_worker_id);`
可以向`任意`worker进程或者task进程发送消息。在 非主进程 和 Manager进程 中可调用。收到消息的进程会触发onPipeMessage事件, 所以必须注册onPipeMessage事件回调函数
$dst_worker_id为目标进程的ID，范围是0 ~ (worker_num + task_worker_num - 1)

## task投递任务
bool swoole_server::task(mixed $data, int $dst_worker_id = -1) 
$task_id = $serv->task("some data");

AsyncTask功能在1.6.4版本增加，默认不启动task功能，需要在手工设置task_worker_num来启动此功能

$dst_worker_id可以制定要给投递给哪个task进程，传入ID即可，范围是0 - (serv->task_worker_num -1), $dst_worker_id可以制定要给投递给哪个task进程，传入ID即可，范围是0 - (serv->task_worker_num -1)

swoole_server->task/taskwait/finish 3个方法当传入的$data数据超过8K时会启用临时文件来保存。当临时文件内容超过 server->package_max_length 时底层会抛出一个警告。 `WARN: task package is too big.`

task操作的次数必须小于onTask处理速度，如果投递容量超过处理能力，task会塞满缓存区，导致worker进程发生阻塞。worker进程将无法接收新的请求。（看来task调用finish, wroker在 onFinish中接收完成信息 这种模式有时候是有必要的）

## 属性
setting, master_pid, manager_pid, worker_id, worker_pid, taskworker, connections

## 配置选项
reactor_num, cpu数量
worker_num, cpu 1-4倍左右，每个进程40M内存左右

max_request, 一个worker进程在处理完这个数值的任务后就自动退出，防止php进程内存溢出。只能用于同步阻塞的服务器，纯异步的server不应当设置这个参数。 如果不希望进程自动退出可以设置为0
当worker进程内发生致命错误或者人工执行exit时，进程会自动退出。主进程会重新启动一个新的worker进程来处理任务。

max_conn， 最大连接数，默认为 ulimit -n的数值

task_worker_num, 开启task功能，必须注册 onTask/ onFinish回调。task进程是同步阻塞的，task进程内不能用mysql-async/redis-async/swoole_event等异步IO函数

task_ipc_mode, task 与worker之间的通信方式
1, 使用unix socket通信
2, 使用消息队列通信
3, 使用消息队列通信，并设置为争抢模式
设置为3后，task/taskwait将无法指定目标进程ID

task_max_request， 与max_request相似。1.7.17之后默认为0，不会自动退出、

task_tmpdir, $server->task()如果投递的数据超过8192字节，将启用临时文件来保存数据

dispatch_mode, 
数据包分发策略。可以选择3种类型，默认为2
1，轮循模式，收到会轮循分配给每一个worker进程
2，固定模式，根据连接的文件描述符分配worker。这样可以保证同一个连接发来的数据只会被同一个worker处理
3，抢占模式，主进程会根据Worker的忙闲状态选择投递，只会投递给处于闲置状态的Worker
4，IP分配，根据TCP/UDP连接的来源IP进行取模hash，分配给一个固定的worker进程。可以保证同一个来源IP的连接数据总会被分配到同一个worker进程。算法为 ip2long(ClientIP) % worker_num
5，UID分配，需要用户代码中调用$serv->bind()将一个连接绑定1个uid。然后swoole根据UID的值分配到不同的worker进程。算法为 UID % worker_num，如果需要使用字符串作为UID，可以使用crc32(UID_STRING)
dispatch_mode 4,5两种模式，在 1.7.8以上版本可用
dispatch_mode=1/3时，底层会屏蔽onConnect/onClose事件，原因是这2种模式下无法保证onConnect/onClose/onReceive的顺序
非请求响应式的服务器程序，请不要使用模式1或3

dispatch_mode配置在BASE模式是无效的，因为BASE不存在投递任务。当reactor收到客户端发来的数据后会立即回调onReceive，不需要投递Worker进程。

message_queue_key, 设置消息队列的KEY，仅在ipc_mode = 2或task_ipc_mode = 2时使用。设置的Key仅作为队列的基数。此参数的默认值为ftok($php_script_file, 1)。实际使用的消息队列KEY为：
recv数据消息队列KEY为 message_queue_key
send数据消息队列KEY为 message_queue_key + 1
task数据消息队列KEY为 message_queue_key + 2
recv/send数据队列在server结束后，会自动销毁。task队列在server结束后不会销毁，重新启动程序后，task进程仍然会接着处理队列中的任务。


## swoole_process

// SIGCHLD 是当子进程stop或者 terminate的时候，发送给父进程的信号。默认行为是忽略它。
swoole_process::signal(SIGCHLD, function(){
    //表示子进程已关闭，回收它
    $status = swoole_process::wait();
    echo "Worker#{$status['pid']} exit\n";
});


## from qq group
A: tcp 中，客户端因为断网了 导致的tcp连接断开，服务端my_onClose能收到回调么
Q: 需要等待下一次心跳失败 才会 调用 close. 设置心跳检测间隔：heartbeat_check_interval

A: 我的 swoole tcp服务器连接数到 800左右就上不去了
WARN    swFactoryProcess_finish: send 45 byte failed, because session#1503 is closed
Q: 错误是因为客户端关闭了, 检查代码逻辑，检查服务器状态, ulimit -n 等。

A: 用户断网后，如何剔除该连接并回收资源？
Q: 心跳检测文档中说在剔除连接后会触发 onClose()事件，但是有人说没有触发； 那么可以自己定时检测，定时清理， tick(), exist()






