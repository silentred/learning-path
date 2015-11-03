# PHP IPC

## socket and stream
最常用，并且不局限于单机

## signal
信号不能传递数据，只能根据信号设置回调。
需要 declare(tick=1);

## msg_queue and semaphore
模块名称为 sysvmsg, sysvsem, sysvshm
队列能传递数据。

## pipe
有一些限制，用 pcntl_fork 的子进程没办法得到 $fd, 貌似是因为子进程的$fd是从父进程复制而来。 
貌似需要用 proc_open 打开的进程才能得到 $fd

## shared memory
模块名称为 shmop， 但是默认没有提供同步的机制，只有 shmop_open 的参数 $flag为 "n"时，会先检测同key的内存是否存在，存在则不创建。 set, get 的同步操作，貌似可以借助 sem_get, sem_remove, sem_acquire, sem_release 来实现。信号量机制是原子操作。
sem_get 创建信号量
sem_remove 删除信号量（一般不用）
sem_acquire 请求得到信号量
sem_release 释放信号量。和 sem_acquire 成对使用。

int ftok ( string $pathname , string $proj ) 文件名一般使用项目中的文件，必须是existing, accessable的文件。$proj 项目id必须为单字符字符串。 文件名使用 /tmp 这一类系统路径也是可以，只不过可能会和其他进程重复，只剩下id作为区分，出了问题难以排查。

## sync 模块
安装： pecl install sync
包含了 SyncMutex, SyncSemaphore, SyncReaderWriter, SyncEvent 四个类。 读写锁，互斥锁，信号量貌似是sysvsem模块的封装。Event 不知道什么作用。

## pthreads
也包含了一个 Metex 类。还有 Cond, Pool。 貌似只有静态方法。只针对 thread?









